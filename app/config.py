import logging
import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

log = logging.getLogger(__name__)

ROOT_PATH = str(Path(os.path.realpath(__file__)).parent.parent.absolute())

ACCESS_TOKEN_EXPIRES_TIME = int(os.getenv("ACCESS_TOKEN_EXPIRES_TIME"))  # Minutes

LOG_LEVEL = os.getenv("LOG_LEVEL")

JWT_SECRET = os.getenv("JWT_SECRET")
JWT_ALG = os.getenv("JWT_ALG")
JWT_EXP = os.getenv("JWT_EXP")  # Minutes

# Database Type 1. SQLITE, 2. MYSQL
DATABASE_TYPE = os.getenv('DATABASE_TYPE')

# database
DATABASE_HOSTNAME = os.getenv("DATABASE_HOSTNAME")
DATABASE_USER = os.getenv("DATABASE_CREDENTIALS")
DATABASE_PASSWORD = os.getenv("DATABASE_CREDENTIALS")
DATABASE_NAME = os.getenv("DATABASE_NAME")
DATABASE_PORT = os.getenv("DATABASE_PORT")
DATABASE_CHARSET = os.getenv("DATABASE_PORT_CHARSET")

# Email
MAIL_USERNAME = os.getenv('MAIL_USERNAME')
MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
MAIL_FROM = os.getenv('MAIL_FROM')
MAIL_PORT = int(os.getenv('MAIL_PORT'))
MAIL_SERVER = os.getenv('MAIL_SERVER')
MAIL_FROM_NAME = os.getenv('MAIN_FROM_NAME')


# Elastic Search
ES_HOST = os.getenv('ES_HOST')
ES_PORT = os.getenv('ES_PORT')
ES_USER = os.getenv('ES_USER')
ES_PASSWORD = os.getenv('ES_PASSWORD')
