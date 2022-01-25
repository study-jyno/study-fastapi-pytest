from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, Text
from sqlalchemy.orm import relationship

from app.database.core import Base


class Item(Base):
    __tablename__ = 'item'

    id = Column(Integer, primary_key=True, index=True)
    item_data = Column(Text)

    user_list = relationship("User", back_populates="item",
                             cascade="all, delete", passive_deletes=True)

    def get_name_to_log(self):
        return self.company_name


class ItemParentItemChild(Base):
    __tablename__ = 'item_parent_item_child'
    item_child_id = Column(ForeignKey('item_child.id'), primary_key=True)
    item_parent_id = Column(ForeignKey('item_parent.id'), primary_key=True)
    item_child = relationship("ItemChild", back_populates="item_parent_list", passive_deletes=True)
    item_parent = relationship("ItemParent", back_populates="item_child_list")


class ItemParent(Base):
    __tablename__ = 'item_parent'
    id = Column(Integer, primary_key=True)
    data = Column(Text)
    item_child_list = relationship("ItemParentItemChild", back_populates="item_parent",
                                   cascade="all, delete", passive_deletes=True)


class ItemChild(Base):
    __tablename__ = 'item_child'
    id = Column(Integer, primary_key=True)
    data = Column(Text)
    item_parent_list = relationship("ItemParentItemChild", back_populates="item_child",
                                    cascade="all, delete", passive_deletes=True)


'''
class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.User

    name = "John Doe"

class GroupFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Group

    name = "Admins"

class GroupLevelFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.GroupLevel

    user = factory.SubFactory(UserFactory)
    group = factory.SubFactory(GroupFactory)
    rank = 1

class UserWithGroupFactory(UserFactory):
    membership = factory.RelatedFactory(
        GroupLevelFactory,
        factory_related_name='user',
    )

class UserWith2GroupsFactory(UserFactory):
    membership1 = factory.RelatedFactory(
        GroupLevelFactory,
        factory_related_name='user',
        group__name='Group1',
    )
    membership2 = factory.RelatedFactory(
        GroupLevelFactory,
        factory_related_name='user',
        group__name='Group2',
    )
'''
