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
    item_child_child_list = relationship("ItemChildChild", back_populates="item_child",
                                         cascade="all, delete", passive_deletes=True)


class ItemChildChild(Base):
    __tablename__ = 'item_child_child'
    id = Column(Integer, primary_key=True)
    data = Column(Text)

    item_child_id = Column(ForeignKey('item_child.id'), primary_key=True)
    item_child = relationship("ItemChild", back_populates="item_child_child_list",
                              cascade="all, delete", passive_deletes=True)
