from app.auth.service import service_user, service_user_certification


def test_user_get(session, user):
    user_list = service_user.get_multi(db=session)
    search_user = service_user.get(db=session, id=user_list[0].id)
    assert search_user, user_list[0]


def test_user_get_multi(session, user):
    user_list = service_user.get_multi(db=session)
    assert len(user_list), 1


def test_user_create(user):
    print()


def test_user_update(user):
    print()


def test_user_delete(user):
    print()
