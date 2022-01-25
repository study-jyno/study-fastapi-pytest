import logging

import app.auth.models as auth_models
import app.log.models as log_models
import app.item.models as item_models
from app.database.core import engine

log = logging.getLogger(__file__)

# 생성해야 하는 순서대로 작성
db_model_list = [
    auth_models,
    item_models,
    log_models,
]


def create_all():
    for db_model in db_model_list:
        db_model.Base.metadata.create_all(bind=engine)


def delete_all():
    for db_model in db_model_list[-1:]:
        db_model.Base.metadata.drop_all(bind=engine)
