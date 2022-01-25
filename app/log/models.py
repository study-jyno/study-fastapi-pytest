from datetime import datetime

from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship

from app.database.core import Base


class Log(Base):
    __tablename__ = 'logs'

    log_id = Column(Integer, primary_key=True, index=True)
    object_id = Column(Integer)  # 액션이 발생한 object의 아이디
    object_name = Column(String)  # 액션이 발생한 object의 이름(delete 된 경우 불러올 수 없으니 따로 저장해 두는거)
    object_type = Column(String)  # 액션이 발생한 object의 타입('Control', 'Control_attribute')
    action = Column(String)  # 어떤 액션인지 지정 DELETE UPDATE CREATE
    time = Column(DateTime, default=datetime.now)

    created_alarm = Column(Boolean)  # 알람 생성 여부
    message = Column(String)  # 로그 상세 설명

    actor_id = Column(Integer, ForeignKey('user.id'))
    actor = relationship("User", back_populates="log_list")
