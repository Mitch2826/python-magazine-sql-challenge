from lib import database_utils
from lib.author import Author


def test_create_tables_idempotent():
    # calling create_tables again should not fail
    database_utils.create_tables()

    # and we should be able to perform basic inserts
    a = Author("OnceMore")
    a.save()
    assert a.id is not None
