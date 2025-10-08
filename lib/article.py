from .database_utils import get_connection

class Article:
    def __init__(self, title, author, magazine, id=None):
        self._id = id
        self._title = None
        
        self._author = author
        self._magazine = magazine
        
    @property
    def id(self):
        return self._id
    @property
    def title(self):
        return self._title
    @title.setter
    def title(self, value):
        if self._title is not None:
            raise Exception("Title cannot be changed after initialization")
        if not isinstance(value, str):
            raise Exception("Title must be a string")
        if not (5 <= len(value) <= 50):
            raise Exception("Title must be between 5 and 50 characters")
        self._title = value
    @property
    def author(self):
        #return the author object associated with this article
        if isinstance(self._author, int):
            #if we only have the author id, fetch the Author
            from .author import Author
            self._author = Author.find_by_id(self._author)
        return self._author
    @property
    def magazine(self):
        #return the magazine object associated with this article
        if isinstance(self._magazine, int):
            #if we only have the magazine id, fetch the Magazine
            from .magazine import Magazine
            self._magazine = Magazine.find_by_id(self._magazine)
        return self._magazine
    @classmethod
    def new_from_db(cls, row):
        article = cls.__new__(cls)  
        article._id = row[0]
        article._title = row[1]
        article._author = row[2]  
        article._magazine = row[3]
        return article
    @classmethod
    def find_by_id(cls, id):
        conn = get_connection()
        cursor = conn.cursor()
        #find article by id
        cursor.execute("SELECT * FROM articles WHERE id = ?", (id,))
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return cls.new_from_db(row)
        return None
    def save(self):
        conn = get_connection()
        cursor = conn.cursor()
        # get the IDs from the author and magazine objects
        author_id = self._author.id if hasattr(self._author, 'id') else self._author
        magazine_id = self._magazine.id if hasattr(self._magazine, 'id') else self._magazine
        
        if self._id is None:
            # insert a new article
            cursor.execute(
                "INSERT INTO articles (title, author_id, magazine_id) VALUES (?, ?, ?)",
                (self._title, author_id, magazine_id)
            )
            self._id = cursor.lastrowid
        else:
            # update an existing article
            cursor.execute(
                "UPDATE articles SET title = ?, author_id = ?, magazine_id = ? WHERE id = ?",
                (self._title, author_id, magazine_id, self._id)
            )
        
        conn.commit()
        conn.close()
    
    def __repr__(self):
        return f"<Article id={self._id} title='{self._title}'>"
        
        
        
        
        