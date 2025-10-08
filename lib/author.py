from .database_utils import get_connection

class Author:
    def __init__(self, name, id=None):
        self._id = id
        self.name = name
        
    @property
    def id(self):
        return self._id
    @property
    def name(self):
        return self._name
    @name.setter
    def name(self, value):
        #name can only be set once
        if self._name is not None:
            raise Exception("Name cannot be changed after initialization")
        #name must be a string
        if not isinstance(value, str):
            raise Exception("Name must be a string")
        #name must have lenght > 0
        if len(value) == 0:
            raise Exception("Name must have length greater than 0")
        self._name = value
        
    @classmethod
    #create an Author object from a database row
    def new_from_db(cls, row):
        return cls(name=row[1], id=row[0]) #row format is(id, name)
    
    @classmethod
    #find an author by id in the db
    def find_by_id(cls, id):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM authors WHERE id = ?", (id,))
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return cls.new_from_db(row)
        else:
            return None

    #save the author to the database   
    def save(self):
        conn = get_connection()
        cursor = conn.cursor()
        #insert new author if id is None
        if self.id is None:
            cursor.execute("INSERT INTO authors (name) VALUES (?)", (self._name,))
            self._id = cursor.lastrowid
        else:
            #update an existing author
            cursor.execute("UPDATE authors SET name = ? WHERE id = ?", (self._name, self._id))
            
        conn.commit()
        conn.close()
        
    def articles(self):
        from .article import Article
        
        conn = get_connection()
        cursor = conn.cursor()
        #get all articles by this author
        cursor.execute("SELECT * FROM articles WHERE author_id = ?", (self._id,))
        rows = cursor.fetchall()
        conn.close()
        
        return [Article.new_from_db(row) for row in rows]
    def magazines(self):
        from .magazine import Magazine
        
        conn = get_connection()
        cursor = conn.cursor()
        #get all unique magazines this author has contributed to
        cursor.execute('''
            SELECT DISTINCT magazines.*
            FROM magazines
            INNER JOIN articles ON magazines.id = articles.magazine_id
            WHERE articles.author_id = ?
        ''', (self._id,))
        rows = cursor.fetchall()
        conn.close()
        
        return [Magazine.new_from_db(row) for row in rows]
    def add_article(self, magazine, title):
        from .article import Article
        #create a new article for this author for a magazine
        article = Article(title=title, author=self, magazine=magazine)
        article.save()
        return article
    def topic_areas(self):
        #get specific categories of magazines this author has contributed to
        magazines = self.magazines()
        if not magazines:
            return None
        # return the unique categories
        categories = list(set(mag.category for mag in magazines))
        return categories
    def __repr__(self):
        return f"<Author id={self._id} name='{self._name}'>"