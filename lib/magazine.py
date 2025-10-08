from .database_utils import get_connection

class Magazine:
    def __init__(self, name, category, id=None):
        self._id = id
        self.name = name
        self.category = category
        
    @property
    def id(self):
        return self._id
    @property
    def name(self):
        return self._name
    @name.setter
    def name(self, value):
        #name must be a string
        if not isinstance(value, str):
            raise Exception("Name must be a string")
        #name must be between 2 and 16 characters
        if not (2 <= len(value) <= 16):
            raise Exception("Name must be between 2 and 16 characters")
        self._name = value
        
    @property
    def category(self):
        return self._category
    @category.setter
    def category(self, value):
        """
        Validate category:
        - Must be a string
        - Must have length > 0
        """
        if not isinstance(value, str):
            raise Exception("Category must be a string")
        if len(value) == 0:
            raise Exception("Category must have length greater than 0")
        self._category = value
        
    @classmethod
    def new_from_db(cls, row):
        return cls(name=row[1], category=row[2], id=row[0])
    @classmethod
    def find_by_id(cls, id):
       conn = get_connection()
       cursor = conn.cursor()
       #find magazine by id
       cursor.execute("SELECT * FROM magazines WHERE id = ?", (id,))
       row = cursor.fetchone()
       conn.close()
       
       if row:
           return cls.new_from_db(row)
       return None
    def save(self):
        
        conn = get_connection()
        cursor = conn.cursor()
        
        if self._id is None:
            # INSERT a new magazine
            cursor.execute(
                "INSERT INTO magazines (name, category) VALUES (?, ?)",
                (self._name, self._category)
            )
            self._id = cursor.lastrowid
        else:
            # UPDATE an existing magazine
            cursor.execute(
                "UPDATE magazines SET name = ?, category = ? WHERE id = ?",
                (self._name, self._category, self._id)
            )
        
        conn.commit()
        conn.close()
    def articles(self):
        from .article import Article
        
        conn = get_connection()
        cursor = conn.cursor()
        #get all articles published in this magazine
        cursor.execute("SELECT * FROM articles WHERE magazine_id = ?", (self._id,))
        rows = cursor.fetchall()
        conn.close()
        
        return [Article.new_from_db(row) for row in rows]
    def contributors(self):
        from .author import Author
        
        conn = get_connection()
        cursor = conn.cursor()
        #get all unique authors who have contributed to this magazine
        cursor.execute('''
            SELECT DISTINCT authors.*
            FROM authors
            INNER JOIN articles ON authors.id = articles.author_id
            WHERE articles.magazine_id = ?
        ''', (self._id,))
        rows = cursor.fetchall()
        conn.close()
        
        return [Author.new_from_db(row) for row in rows]
    def article_titles(self):
        conn = get_connection()
        cursor = conn.cursor()
        #get all article titles published in this magazine
        cursor.execute("SELECT title FROM articles WHERE magazine_id = ?", (self._id,))
        rows = cursor.fetchall()
        conn.close()
        
        if not rows:
            return None
        
        return [row[0] for row in rows]
    
    def contributing_authors(self):
        from .author import Author
        
        conn = get_connection()
        cursor = conn.cursor()
        #get all authors who have written more than 2 articles for this magazine
        cursor.execute('''
            SELECT authors.*
            FROM authors
            INNER JOIN articles ON authors.id = articles.author_id
            WHERE articles.magazine_id = ?
            GROUP BY authors.id
            HAVING COUNT(articles.id) > 2
        ''', (self._id,))
        rows = cursor.fetchall()
        conn.close()
        
        if not rows:
            return None
        
        return [Author.new_from_db(row) for row in rows]
    def __repr__(self):
        return f"<Magazine id={self._id} name='{self._name}' category='{self._category}'>"
    
                

        
        
        
        