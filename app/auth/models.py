from datetime import datetime

from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, Text, UniqueConstraint, event, DateTime
from sqlalchemy.orm import relationship, object_session

from app.database.core import Base


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(16), unique=True)
    password = Column(Text)
    first_name = Column(Text)
    last_name = Column(Text)
    is_admin = Column(Boolean)
    is_certification = Column(Boolean, default=False)
    is_deleted = Column(Boolean, default=False)

    # User : Company = 1 : 1
    item_id = Column(Integer, ForeignKey('item.id', ondelete='CASCADE'))
    item = relationship("Item", back_populates="user_list", passive_deletes=True)

    # User - UserCertification
    user_certification = relationship("UserCertification", uselist=False, back_populates="user",
                                      cascade="all, delete", passive_deletes=True)

    # User : Log = 1 : N
    log_list = relationship("Log", back_populates="actor")

    def get_name_to_log(self):
        return self.username

    def get_full_name(self):
        return self.first_name + self.last_name


class UserCertification(Base):
    __tablename__ = 'user_certification'
    id = Column(Integer, primary_key=True, index=True)

    user = relationship("User", back_populates="user_certification", passive_deletes=True)
    user_id = Column(Integer, ForeignKey('user.id', ondelete='CASCADE'))

    created_time = Column(DateTime, default=datetime.now)
    certification_string = Column(String)

    def get_name_to_log(self):
        pass
