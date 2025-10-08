import pytest

from lib.author import Author
from lib.magazine import Magazine
from lib.article import Article


def test_author_name_validation_and_immutability():
    # valid init
    a = Author("John Doe")
    assert a.name == "John Doe"

    # name can be set once post-init (per current implementation)
    a.name = "Jane Doe"
    assert a.name == "Jane Doe"

    # changing again should raise
    with pytest.raises(Exception):
        a.name = "Another Name"

    # invalid name types/values
    with pytest.raises(Exception):
        Author(123)  # not a string
    with pytest.raises(Exception):
        Author("")  # empty


def test_author_persistence_and_find_by_id():
    a = Author("Alice")
    a.save()
    assert a.id is not None

    fetched = Author.find_by_id(a.id)
    assert fetched is not None
    assert fetched.id == a.id
    assert fetched.name == "Alice"

    assert Author.find_by_id(99999) is None


def test_author_relationships_magazines_and_topic_areas():
    author = Author("Reporter")
    author.save()

    # No articles yet => topic_areas returns None
    assert author.topic_areas() is None

    mag1 = Magazine("TechNews", "Technology")
    mag1.save()
    mag2 = Magazine("DailyLife", "Lifestyle")
    mag2.save()

    author.add_article(mag1, "AI in Healthcare Today")
    author.add_article(mag2, "Morning Routines That Work")

    titles = {a.title for a in author.articles()}
    assert titles == {"AI in Healthcare Today", "Morning Routines That Work"}

    mags = {m.name for m in author.magazines()}
    assert mags == {"TechNews", "DailyLife"}

    areas = set(author.topic_areas())
    assert areas == {"Technology", "Lifestyle"}


def test_author_add_article_returns_saved_article():
    author = Author("Contributor")
    author.save()

    mag = Magazine("WorldNews", "News")
    mag.save()

    article = author.add_article(mag, "Global Markets Update")
    assert isinstance(article, Article)
    assert article.id is not None
    assert article.title == "Global Markets Update"
    assert article.author.id == author.id
    assert article.magazine.id == mag.id
