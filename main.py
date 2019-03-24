# -*- coding: utf-8 -*-
import vk_api
import getpass
import config


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
    tools = vk_api.tools.VkTools(vk_session)
    return filter(lambda x: x["members_count"] <= config.MEMBER_LIMIT, tools.get_all_iter(method="groups.get", values={
        "extended": 1,
        "fields": "members_count"
    }, max_count=1000))


def main():
    vk_session = None
    attempts = 0
    while vk_session is None and attempts < config.LOGIN_ATTEMPTS_LIMITS:
        attempts += 1
        vk_session = get_vk_session()
    if vk_session is None:
        print("Failed to login!")
        return

    print("Names of groups:")
    for group in get_small_groups_iter(vk_session):
        print(group["name"])


if __name__ == '__main__':
    main()
