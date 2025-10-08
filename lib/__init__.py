from .author import Author
from .magazine import Magazine
from .article import Article
from .database_utils import create_tables, get_connection

__all__ = ['Author', 'Magazine', 'Article', 'create_tables', 'get_connection']