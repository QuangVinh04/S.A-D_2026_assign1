"""Get book catalog use case"""
from typing import List
from domain.entities.book import Book
from interfaces.repositories.book_repository import BookRepository


class GetBookCatalogUseCase:
    """Use case for getting book catalog"""
    
    def __init__(self, book_repository: BookRepository):
        self.book_repository = book_repository
    
    def execute(self) -> List[Book]:
        """Get all books"""
        return self.book_repository.get_all()
