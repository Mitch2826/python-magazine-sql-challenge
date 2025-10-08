from lib.database_utils import create_tables
from lib.author import Author
from lib.magazine import Magazine
from lib.article import Article

create_tables()
print("Database tables created!\n")

author1 = Author("Wanjiku Mwangi")
author1.save()
print(f"Created: {author1}")

author2 = Author("Kamau Njoroge")
author2.save()
print(f"Created: {author2}")

author3 = Author("Akinyi Ochieng")
author3.save()
print(f"Created: {author3}\n")

print("Creating test magazines...")
mag1 = Magazine("Nairobi Times", "News")
mag1.save()
print(f"Created: {mag1}")

mag2 = Magazine("East Africa", "Culture")
mag2.save()
print(f"Created: {mag2}")

mag3 = Magazine("Tech Hub KE", "Technology")
mag3.save()
print(f"Created: {mag3}\n")

print("Creating test articles...")
article1 = Article("Matatu Culture and Urban Transport in Nairobi", author1, mag1)
article1.save()
print(f"Created: {article1}")

article2 = Article("The Rise of Mpesa and Digital Banking", author1, mag3)
article2.save()
print(f"Created: {article2}")

article3 = Article("Safari Rally Returns to Kenya", author2, mag1)
article3.save()
print(f"Created: {article3}")

article4 = Article("Kenya's ethnic diversity and cultures", author2, mag2)
article4.save()
print(f"Created: {article4}")

article5 = Article("Nairobi Silicon Savannah Innovation", author3, mag3)
article5.save()
print(f"Created: {article5}\n")

#relationships
print("=" * 60)
print("TESTING AUTHOR RELATIONSHIPS")
print("=" * 60)
print(f"\nArticles by {author1.name}:")
for article in author1.articles():
    print(f"  - {article.title}")

print(f"\nMagazines {author1.name} has written for:")
for magazine in author1.magazines():
    print(f"  - {magazine.name} ({magazine.category})")

print(f"\nTopic areas for {author1.name}: {author1.topic_areas()}\n")

#magazine relationships
print("=" * 60)
print("TESTING MAGAZINE RELATIONSHIPS")
print("=" * 60)
print(f"\nArticles in {mag1.name}:")
for article in mag1.articles():
    print(f"  - {article.title}")

print(f"\nContributors to {mag1.name}:")
for contributor in mag1.contributors():
    print(f"  - {contributor.name}")

print(f"\nArticle titles in {mag1.name}:")
titles = mag1.article_titles()
if titles:
    for title in titles:
        print(f"  - {title}")
print()

#add articles
print("=" * 60)
print("TESTING ADD_ARTICLE METHOD")
print("=" * 60)
print(f"\nAdding new article by {author1.name} to {mag2.name}...")
new_article = author1.add_article(mag2, "Swahili Language Revival in Modern Kenya")
print(f"Created: {new_article}")
print(f"Updated topic areas for {author1.name}: {author1.topic_areas()}\n")

#contributing authors
print(f"\nContributing authors for {mag1.name} (>2 articles):")
contributors = mag1.contributing_authors()
if contributors:
    for author in contributors:
        print(f"  - {author.name}")
else:
    print("  None yet")
print()

#add articles to magazines
print("Adding more articles to test top publisher...")
author2.add_article(mag3, "Kenyan Startups Attracting Investment")
author2.add_article(mag3, "Blockchain Technology in Agriculture")
author2.add_article(mag3, "AI Solutions for Healthcare in Kenya")
author3.add_article(mag3, "Coding Bootcamps in Nairobi")
print()

# Test top_publisher
print("=" * 60)
print("TESTING TOP PUBLISHER")
print("=" * 60)
top_mag = Magazine.top_publisher()
if top_mag:
    article_count = len(top_mag.articles())
    print(f"Top publisher: {top_mag.name}")
    print(f"Category: {top_mag.category}")
    print(f"Total articles: {article_count}")
print()

#finding by ID
print("=" * 60)
print("TESTING FIND BY ID")
print("=" * 60)
found_author = Author.find_by_id(1)
print(f"Found author with ID 1: {found_author.name}")

found_magazine = Magazine.find_by_id(2)
print(f"Found magazine with ID 2: {found_magazine.name}")

found_article = Article.find_by_id(3)
print(f"Found article with ID 3: {found_article.title}")
print()

#final 
print("=" * 60)
print("SUMMARY")
print("=" * 60)
print(f"Total authors created: 3")
print(f"Total magazines created: 3")
print(f"Total articles created: {len(Article.find_by_id(1).author.articles()) + len(Article.find_by_id(3).author.articles()) + len(Article.find_by_id(5).author.articles())}")
print()

print("=" * 60)
print("Setup complete! You can now use ipdb to debug.")
print("Example: import ipdb; ipdb.set_trace()")
print("=" * 60)