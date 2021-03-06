#!venv/bin/python3.7
# -*- coding: utf-8 -*-
import getpass

import vk_api

import config
import db_functions


def get_vk_session():
    """
    Request login and password and try to login
    :return: None if authentication failed, VkApi object otherwise
    """
    login = input("Enter login/phone number\n").strip()
    password = getpass.getpass()
    vk_session = vk_api.VkApi(login, password, app_id=config.APP_ID, scope=config.SCOPE)
    try:
        vk_session.auth(token_only=True)
    except vk_api.AuthError as error_msg:
        print(error_msg)
        return None
    return vk_session


def get_small_groups_iter(vk_session):
    """
    Take current session, get iterator over all groups and then filter them
    This is more memory efficient (even though all groups from request are stored in tools's memory)
    :param vk_session: current session
    :return: iterator over groups with not more than 100 members
    """

    def match(group):
        return group["members_count"] <= config.MEMBER_LIMIT

    tools = vk_api.VkTools(vk_session)
    return filter(match, tools.get_all_iter(method="groups.get", values={
        "extended": 1,
        "fields": "members_count"
    }, max_count=1000))


def get_matching_users_iter(vk_session, group):
    """
    Take current session and vk group object, get iterator over all users in group and then filter them
    :param vk_session: current session
    :param group: vk object that describes group's parameters
    :return: iterator over matched users in given group
    """

    def match(user):
        if any(key not in user for key in ("sex", "bdate")):
            return False
        if user["sex"] != 1:
            return False
        date_elems = [int(i) for i in user["bdate"].split(".")]  # bdate is stored or in DD.MM.YYYY format, or in DD.MM
        if len(date_elems) != 3:
            return False

        years_old = config.CURRENT_DATE.year - date_elems[2]
        years_old -= ((config.CURRENT_DATE.month, config.CURRENT_DATE.day) < (date_elems[1], date_elems[0]))
        return 20 <= years_old <= 22

    tools = vk_api.VkTools(vk_session)
    group_id = group["id"]
    return filter(match, tools.get_all_iter(method="groups.getMembers", values={
        "group_id": group_id,
        "fields": "sex,bdate"
    }, max_count=1000))


def work_with_db(vk_session, cursor, groups):
    """
    Add matching users from every group in groups to DB that cursor points to
    :param vk_session: vk session
    :param cursor: cursor to SQLite DB
    :param groups: list of vk group objects
    """

    def transform(user):
        return {'vk_id': user["id"],
                'first_name': user["first_name"],
                'last_name': user["last_name"]}

    for group in groups:
        if config.VERBOSE:
            print("Now parsing:", group["name"])
        db_functions.update_db(cursor, map(transform, get_matching_users_iter(vk_session, group)))


def main():
    vk_session = None
    attempts = 0
    while vk_session is None and attempts < config.LOGIN_ATTEMPTS_LIMITS:
        attempts += 1
        vk_session = get_vk_session()
    if vk_session is None:
        print("Failed to login!")
        return

    groups = list(get_small_groups_iter(vk_session))  # to avoid further requests to server
    print("List of groups:")
    for group in groups:
        print(group["name"])
    print()

    conn = db_functions.connect_to_db()
    work_with_db(vk_session, conn.cursor(), groups)
    print("Current list of users")
    for row in conn.execute("SELECT * FROM Users"):
        print(*row)  # test results
    conn.commit()
    conn.close()


if __name__ == '__main__':
    main()
