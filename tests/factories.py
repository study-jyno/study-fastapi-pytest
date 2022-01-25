import uuid

import factory
from pytz import UTC
from datetime import datetime

from faker import Faker

from factory import Sequence, post_generation, SubFactory, LazyAttribute
from factory.alchemy import SQLAlchemyModelFactory
from factory.fuzzy import FuzzyChoice, FuzzyText, FuzzyDateTime, FuzzyInteger

from app.auth.models import User, UserCertification  # noqa
from app.item.models import Item, ItemChild, ItemParent, ItemParentItemChild
from app.log.models import Log

from .database import Session


class BaseFactory(SQLAlchemyModelFactory):
    """Base Factory."""

    class Meta:
        """Factory configuration."""

        abstract = True
        sqlalchemy_session = Session
        sqlalchemy_session_persistence = "commit"


class TimeStampBaseFactory(BaseFactory):
    """Timestamp Base Factory."""

    created_at = FuzzyDateTime(datetime(2020, 1, 1, tzinfo=UTC))
    updated_at = FuzzyDateTime(datetime(2020, 1, 1, tzinfo=UTC))


class ItemFactory(BaseFactory):
    """Item Factory."""

    item_data = FuzzyText()

    class Meta:
        """Factory Configuration."""
        model = Item


class UserFactory(BaseFactory):
    """User Factory."""
    username = Faker().ascii_email()
    password = Faker().password(length=12)
    first_name = Faker().first_name()
    last_name = Faker().last_name()
    is_admin = False
    is_certification = False
    is_deleted = False

    # User : Item = 1 : N
    item = SubFactory(ItemFactory)

    class Meta:
        """Factory Configuration."""

        model = User


class UserCertificationFactory(BaseFactory):
    """User Factory."""
    certification_string = FuzzyText()

    # User : UserCertificationFactory = 1 : 1
    user = SubFactory(UserFactory)

    class Meta:
        """Factory Configuration."""
        model = UserCertification


class LogFactory(BaseFactory):
    """User Factory."""
    certification_string = FuzzyText()
    object_id = FuzzyInteger(low=0, high=100)  # 액션이 발생한 object의 아이디
    object_name = FuzzyText()  # 액션이 발생한 object의 이름(delete 된 경우 불러올 수 없으니 따로 저장해 두는거)
    object_type = FuzzyText()  # 액션이 발생한 object의 타입('Control', 'Control_attribute')
    action = FuzzyChoice(['DELETE', 'UPDATE', 'CREATE'])  # 어떤 액션인지 지정 DELETE UPDATE CREATE
    created_alarm = False  # 알람 생성 여부
    message = FuzzyText()  # 로그 상세 설명
    actor = SubFactory(UserFactory)

    class Meta:
        """Factory Configuration."""
        model = Log


class ItemParentFactory(BaseFactory):
    data = FuzzyText()

    class Meta:
        """Factory Configuration."""
        model = ItemParent


class ItemChildFactory(BaseFactory):
    data = FuzzyText()

    class Meta:
        """Factory Configuration."""
        model = ItemChild


class ItemParentItemChildFactory(BaseFactory):
    item_child = SubFactory(ItemChildFactory)
    item_parent = SubFactory(ItemParentFactory)

    class Meta:
        """Factory Configuration."""
        model = ItemParentItemChild
