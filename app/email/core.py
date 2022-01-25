from fastapi_mail import FastMail, ConnectionConfig
from app.config import MAIL_USERNAME, MAIL_PASSWORD, MAIL_FROM, MAIL_PORT, MAIL_SERVER, MAIL_FROM_NAME
from pathlib import Path

conf = ConnectionConfig(
    MAIL_USERNAME=MAIL_USERNAME,
    MAIL_PASSWORD=MAIL_PASSWORD,
    MAIL_FROM=MAIL_FROM,
    MAIL_PORT=MAIL_PORT,
    MAIL_SERVER=MAIL_SERVER,
    MAIL_FROM_NAME=MAIL_FROM_NAME,
    MAIL_TLS=False,
    MAIL_SSL=True,
    USE_CREDENTIALS=True,
    TEMPLATE_FOLDER=Path(__file__).parent / 'templates'
)


def get_fm():
    fm_session = FastMail(conf)
    try:
        yield fm_session
    finally:
        pass

# fm.config.SUPPRESS_SEND = 0  # 0: 전송함 1: 전송 하지 않음
