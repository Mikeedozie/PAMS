"""Basic Products API (minimal)"""
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from sqlalchemy.orm import Session

from ..database_simple import SessionLocal
from .. import models

router = APIRouter(prefix="/api/products", tags=["products"])


def get_db():
	db = SessionLocal()
	try:
		yield db
	finally:
		db.close()


class ProductCreate(BaseModel):
	sku: str
	name: str
	category: str
	current_stock: int = 0
	reorder_point: int = 0
	manufacturer: Optional[str] = None
	unit_cost: Optional[float] = None


class ProductResponse(BaseModel):
	id: int
	sku: str
	name: str
	category: str
	current_stock: int
	reorder_point: int
	manufacturer: Optional[str] = None
	unit_cost: Optional[float] = None
	status: Optional[str] = None

	class Config:
		from_attributes = True


@router.get("/", response_model=List[ProductResponse])
def list_products(db: Session = Depends(get_db)):
	return db.query(models.Product).limit(500).all()


@router.post("/", response_model=ProductResponse, status_code=201)
def create_product(payload: ProductCreate, db: Session = Depends(get_db)):
	if db.query(models.Product).filter(models.Product.sku == payload.sku).first():
		raise HTTPException(status_code=400, detail="SKU already exists")
	product = models.Product(
		sku=payload.sku,
		name=payload.name,
		category=payload.category,
		current_stock=payload.current_stock,
		reorder_point=payload.reorder_point,
		manufacturer=payload.manufacturer,
		unit_cost=payload.unit_cost,
		status="active"
	)
	db.add(product)
	db.commit()
	db.refresh(product)
	return product

