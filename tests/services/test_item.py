import factory

from app.item.service import service_item
from tests.factories import ItemParentItemChildFactory, UserFactory, UserCertificationFactory


def test_item_get(dummy_session, item):
    item_list = service_item.get_multi(db=dummy_session)
    search_user = service_item.get(db=dummy_session, id=item_list[0].id)
    assert search_user, item_list[0]


def test_user_get_multi(dummy_session, user):
    user_list = service_item.get_multi(db=dummy_session)
    assert len(user_list), 1


def test_user_create(user):
    print()


def test_user_update(user):
    print()


def test_user_delete(user):
    print()


def test_item_nm(item_parent_item_child):
    test = ItemParentItemChildFactory()
    print()


def test_create_dummy_data(dummy_session):
    test = ItemParentItemChildFactory()
    test_1 = UserFactory(username='test_1')
    test_2 = UserFactory(username='test_2')
    test_5 = UserCertificationFactory(user=test_2)
    print()
