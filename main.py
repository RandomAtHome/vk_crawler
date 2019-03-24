# -*- coding: utf-8 -*-
import vk_api
import getpass
import config


def try_login():
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


def main():
    vk_session = None
    attempts = 0
    while vk_session is None and attempts < config.LOGIN_ATTEMPTS_LIMITS:
        attempts += 1
        vk_session = try_login()
    if vk_session is None:
        print("Failed to login!")
        return

    vk = vk_session.get_api()
    response = vk.wall.get(count=1)

    if response['items']:
        print(response['items'][0])


if __name__ == '__main__':
    main()
