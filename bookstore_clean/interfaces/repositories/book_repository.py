"""Book repository interface"""
from abc import ABC, abstractmethod
from typing import List, Optional
from domain.entities.book import Book


class BookRepository(ABC):
    """Interface for book repository"""
    
    @abstractmethod
    def get_all(self) -> List[Book]:
        """Get all books"""
        pass
    
    @abstractmethod
    def get_by_id(self, book_id: int) -> Optional[Book]:
        """Get book by id"""
        pass
