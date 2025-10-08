import pytest

from lib.author import Author
from lib.magazine import Magazine


def test_magazine_validation():
    # name must be str between 2 and 16
    with pytest.raises(Exception):
        Magazine(1, "Cat")
    with pytest.raises(Exception):
        Magazine("A", "Cat")
    with pytest.raises(Exception):
        Magazine("A" * 17, "Cat")

    # category must be non-empty string
    with pytest.raises(Exception):
        Magazine("ValidName", 123)
    with pytest.raises(Exception):
        Magazine("ValidName", "")

    # valid
    m = Magazine("AB", "Cat")
    assert m.name == "AB"
    assert m.category == "Cat"


def test_magazine_persistence_and_find_by_id():
    m = Magazine("TechDigest", "Tech")
    m.save()
    assert m.id is not None

    fetched = Magazine.find_by_id(m.id)
    assert fetched is not None
    assert fetched.id == m.id
    assert fetched.name == "TechDigest"
    assert fetched.category == "Tech"

    assert Magazine.find_by_id(99999) is None


def test_magazine_articles_contributors_titles_contributing_authors_top_publisher():
    # setup authors and magazines
    a1 = Author("Alpha")
    a1.save()
    a2 = Author("Beta")
    a2.save()
    a3 = Author("Gamma")
    a3.save()

    m1 = Magazine("DailyTech", "Technology")
    m1.save()
    m2 = Magazine("CultureMag", "Culture")
    m2.save()

    # initially no articles => article_titles returns None
    assert m1.article_titles() is None

    # create articles
    a1.add_article(m1, "Edge AI Devices in 2025")
    a1.add_article(m1, "Quantum Computing Basics")
    a2.add_article(m1, "DevOps Trends")

    a3.add_article(m2, "Modern Art Movements")

    # verify articles retrieval
    titles_m1 = {a.title for a in m1.articles()}
    assert titles_m1 == {"Edge AI Devices in 2025", "Quantum Computing Basics", "DevOps Trends"}

    # contributors unique
    contrib_names = {a.name for a in m1.contributors()}
    assert contrib_names == {"Alpha", "Beta"}

    # article_titles produces list of titles (order not guaranteed by SQL query, so compare as set)
    assert set(m1.article_titles()) == titles_m1

    # contributing authors: >2 articles in same magazine
    assert m1.contributing_authors() is None  # no author has >2 yet

    # add more articles for a1 to exceed threshold
    a1.add_article(m1, "Intro to Cloud Native")

    contrib_gt2 = m1.contributing_authors()
    assert contrib_gt2 is not None
    assert {a.name for a in contrib_gt2} == {"Alpha"}

    # top_publisher should be m1 because it has more articles than m2
    top = Magazine.top_publisher()
    assert isinstance(top, Magazine)
    assert top.id == m1.id
    assert top.name == m1.name
    assert top.category == m1.category
