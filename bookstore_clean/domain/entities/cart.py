"""Cart domain entities"""
from dataclasses import dataclass, field
from typing import Optional, List
from datetime import datetime


@dataclass
class CartItem:
    """Cart item domain entity"""
    id: Optional[int]
    book_id: int
    quantity: int
    book_title: str = ""
    book_price: float = 0.0
    
    def __post_init__(self):
        if self.quantity <= 0:
            raise ValueError("Quantity must be positive")
    
    @property
    def subtotal(self) -> float:
        """Calculate subtotal for this item"""
        return self.book_price * self.quantity


@dataclass
class Cart:
    """Cart domain entity"""
    id: Optional[int]
    customer_id: int
    items: List[CartItem] = field(default_factory=list)
    created_at: Optional[datetime] = None
    
    def add_item(self, item: CartItem):
        """Add item to cart"""
        # Check if item already exists
        existing_item = next(
            (i for i in self.items if i.book_id == item.book_id),
            None
        )
        if existing_item:
            existing_item.quantity += item.quantity
        else:
            self.items.append(item)
    
    def remove_item(self, item_id: int):
        """Remove item from cart"""
        self.items = [item for item in self.items if item.id != item_id]
    
    @property
    def total(self) -> float:
        """Calculate total price"""
        return sum(item.subtotal for item in self.items)
