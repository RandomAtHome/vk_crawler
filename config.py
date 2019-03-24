# -*- coding: utf-8 -*-
from vk_api import VkUserPermissions
from datetime import date

SCOPE = (VkUserPermissions.OFFLINE | VkUserPermissions.GROUPS)
LOGIN_ATTEMPTS_LIMITS = 3
APP_ID = 6912112
MEMBER_LIMIT = 100
CURRENT_DATE = date.today()
