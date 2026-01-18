"""Book domain entity"""
from dataclasses import dataclass
from typing import Optional
from decimal import Decimal


@dataclass
class Book:
    """Book domain entity"""
    id: Optional[int]
    title: str
    author: str
    price: Decimal
    stock: int

    def __post_init__(self):
        if not self.title:
            raise ValueError("Book title is required")
        if not self.author:
            raise ValueError("Book author is required")
        if self.price < 0:
            raise ValueError("Book price must be non-negative")
        if self.stock < 0:
            raise ValueError("Book stock must be non-negative")
    
    def is_available(self) -> bool:
        """Check if book is available"""
        return self.stock > 0
