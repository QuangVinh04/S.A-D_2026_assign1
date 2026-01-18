"""Book repository implementation using Django ORM"""
from typing import List, Optional
from domain.entities.book import Book
from interfaces.repositories.book_repository import BookRepository
from infrastructure.database.models import BookModel


class DjangoBookRepository(BookRepository):
    """Django ORM implementation of BookRepository"""
    
    def get_all(self) -> List[Book]:
        """Get all books"""
        book_models = BookModel.objects.all()
        return [self._to_domain(model) for model in book_models]
    
    def get_by_id(self, book_id: int) -> Optional[Book]:
        """Get book by id"""
        try:
            book_model = BookModel.objects.get(id=book_id)
            return self._to_domain(book_model)
        except BookModel.DoesNotExist:
            return None
    
    def _to_domain(self, model: BookModel) -> Book:
        """Convert Django model to domain entity"""
        return Book(
            id=model.id,
            title=model.title,
            author=model.author,
            price=model.price,
            stock=model.stock
        )
