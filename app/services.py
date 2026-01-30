import uuid
from datetime import datetime
from dataclasses import dataclass, field, asdict
from typing import List, Optional

@dataclass
class PurchaseItem:
    product_id: str
    price: float
    quantity: int

@dataclass
class Purchase:
    user_id: str
    items: List[PurchaseItem]
    total: float
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    created_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    status: str = "CONFIRMED"

    def to_dict(self):
        return asdict(self)

class PurchaseService:
    def __init__(self):
        # Simulación de base de datos en memoria
        self._db: List[Purchase] = []

    def create_purchase(self, user_id: str, raw_items: List[dict]) -> Purchase:
        """Procesa una compra calculando totales y guardándola."""
        items = []
        total = 0.0

        for item in raw_items:
            price = float(item.get('price', 0.0))
            qty = int(item.get('quantity', 1))
            
            # Validación básica de negocio
            if price < 0 or qty <= 0:
                raise ValueError(f"Invalid price or quantity for product {item.get('product_id')}")

            total += price * qty
            items.append(PurchaseItem(
                product_id=item.get('product_id', 'unknown'),
                price=price,
                quantity=qty
            ))

        purchase = Purchase(user_id=user_id, items=items, total=round(total, 2))
        self._db.append(purchase)
        return purchase

    def get_purchase_by_id(self, purchase_id: str) -> Optional[Purchase]:
        return next((p for p in self._db if p.id == purchase_id), None)

# Singleton para usar en la app
purchase_service = PurchaseService()