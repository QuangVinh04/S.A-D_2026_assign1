"""Customer domain entity"""
from dataclasses import dataclass
from typing import Optional


@dataclass
class Customer:
    """Customer domain entity"""
    id: Optional[int]
    name: str
    email: str
    password_hash: str

    def __post_init__(self):
        if not self.name:
            raise ValueError("Customer name is required")
        if not self.email:
            raise ValueError("Customer email is required")
        if not self.password_hash:
            raise ValueError("Password hash is required")
