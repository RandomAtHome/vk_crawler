# -*- coding: utf-8 -*-
from datetime import date

from vk_api import VkUserPermissions

SCOPE = (VkUserPermissions.OFFLINE | VkUserPermissions.GROUPS)
LOGIN_ATTEMPTS_LIMITS = 3
APP_ID = 6912112
MEMBER_LIMIT = 100
CURRENT_DATE = date.today()  # Today's date (in order to avoid calculating it for every person/group
DB_NAME = "ladies.db"        # Name of DB we connect to
VERBOSE = True               # Print name of the group being processed
