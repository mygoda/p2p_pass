# -*- coding: utf-8 -*-
# __author__ = xutao

from __future__ import division, unicode_literals, print_function

# DB
DB_NORMAL_LENGTH = 32
DB_PLACE_LENGTH = 64
DB_TITLE_LENGTH = 128

DB_CONTENT_LENGTH = 2056

DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"
DATE_FORMAT = "%Y-%m-%d"
TIME_FORMAT = "%H:%M"

URL_ID = "(?P<id>[0-9]+)"
URL_UUID = "(?P<id>[^//]+)"

TICKET_ID = "(?P<ticket_id>[0-9]+)"

TEACHER_ID = "(?P<teacher_id>[0-9]+)"

CLASS_ID = "(?P<school_class_id>[0-9]+)"

TYPE = "(?P<type>[0-9]+)"

TERM_ID = "(?P<term_id>[0-9]+)"


TEST_DATA_CENTER = "YFCLOUD"

TEST_USER_NAME = "administrator@yf.local"

TEST_USER_PASSWORD = "P@$$w0rd"

TEST_SERVER_IP = "172.16.0.4"

CORE_HOST = "172.16.0.171"
CORE_USERNAME = "root"
CORE_PASSWORD = "cds-china"
CORE_DATABASE = "automatic_product"

TASK_ID = "(?P<task_id>\S+)"

TOKEN = "TEST"

OVF_TOKEN = "OVF_TEST"

CALLBACK_TOKEN = "CALLBACK_TEST"

OVA_PATH = "/data/transmission-daemon/downloads"

# 目前部署在兆维
P2P_CENTER_HOST = "101.251.255.234:9999"

TORRENT_DOWNLOAD_DIR = "/var/tmp/downloads"


