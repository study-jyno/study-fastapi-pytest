from datetime import datetime
from sqlalchemy.orm import Session

from app.auth.service import get_current_user
from app.database.core import Base
from app.elasticsearch.core import get_open_search_client, index_name
from app.log.schemas import CreateLog, BaseLog
from app.log.models import Log
from app.logging import get_log_message_by_function_name
from app.service.base import ServiceBase, ModelType


class ServiceLog:
    def create(self, db_obj: Base, **kwargs):
        """
        object_name 이 db와 다를 경우 매개변수로 넣어주세요
        """
        object_name = db_obj.get_name_to_log()

        if "object_name" in kwargs:
            object_name = kwargs['object_name']

        massage = get_log_message_by_function_name(**kwargs)
        if massage is None:  # log massage가 없는 경우
            return

        document = {
            'object_id': db_obj.id,
            'object_name': object_name,
            'object_type': db_obj.__tablename__,
            'action': kwargs['action'],
            'time': datetime.now(),
            'actor_name': kwargs['actor_name'],
            'message': massage,
        }

        get_open_search_client().index(
            index=index_name,
            body=document,
            refresh=True
        )


service_log = ServiceLog()
