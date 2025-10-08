import pytest

from lib.author import Author
from lib.magazine import Magazine
from lib.article import Article


def test_article_title_validation_and_immutability():
    a = Author("Writer")
    a.save()
    m = Magazine("ShortNews", "News")
    m.save()

    with pytest.raises(Exception):
        Article("abcd", a, m)  # too short (<5)

    with pytest.raises(Exception):
        Article("x" * 51, a, m)  # too long (>50)

    art = Article("Valid Title Here", a, m)
    art.save()
    assert art.id is not None

    with pytest.raises(Exception):
        art.title = "New Title"  # immutable after first set


def test_article_find_by_id_and_relationship_resolution():
    a = Author("Resolver")
    a.save()
    m = Magazine("ResolverMag", "Ref")
    m.save()

    art = Article("Resolving Relationships", a, m)
    art.save()

    fetched = Article.find_by_id(art.id)
    assert fetched is not None
    assert fetched.id == art.id
    assert fetched.title == art.title

    # new_from_db loads foreign keys as ints; properties resolve to objects on access
    assert fetched.author.id == a.id
    assert fetched.author.name == "Resolver"
    assert fetched.magazine.id == m.id
    assert fetched.magazine.name == "ResolverMag"

    assert Article.find_by_id(99999) is None
