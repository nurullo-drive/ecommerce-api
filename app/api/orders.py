from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app import models, schemas
from app.api import auth
from app.database import get_db

router = APIRouter(prefix="/orders", tags=["Orders"])

@router.post("/checkout", response_model=schemas.OrderResponse)
def checkout(
    order_data: schemas.OrderCreate,
    current_user: models.User = Depends(auth.get_current_active_user),
    db: Session = Depends(get_db)
):
    """Convert cart to order and checkout"""
    
    # Check if user has cart with items
    if not current_user.cart or not current_user.cart.items:
        raise HTTPException(status_code=400, detail="Cart is empty")
    
    cart = current_user.cart
    
    # Verify stock for all items
    for item in cart.items:
        if item.quantity > item.product.stock:
            raise HTTPException(
                status_code=400, 
                detail=f"Not enough stock for {item.product.name}. Available: {item.product.stock}"
            )
    
    # Create order
    order = models.Order(
        user_id=current_user.id,
        total_amount=cart.total,
        shipping_address=order_data.shipping_address
    )
    db.add(order)
    db.flush()  # Get order ID without committing
    
    # Create order items and reduce stock
    for item in cart.items:
        # Create order item
        order_item = models.OrderItem(
            order_id=order.id,
            product_id=item.product_id,
            quantity=item.quantity,
            price_at_time=item.product.price
        )
        db.add(order_item)
        
        # Reduce stock
        item.product.stock -= item.quantity
    
    # Clear the cart
    cart.items.clear()
    
    db.commit()
    db.refresh(order)
    
    return order

@router.get("/", response_model=List[schemas.OrderResponse])
def get_user_orders(
    current_user: models.User = Depends(auth.get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get all orders for current user"""
    orders = db.query(models.Order).filter(
        models.Order.user_id == current_user.id
    ).order_by(models.Order.created_at.desc()).all()
    return orders

@router.get("/{order_id}", response_model=schemas.OrderResponse)
def get_order(
    order_id: int,
    current_user: models.User = Depends(auth.get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get specific order by ID"""
    order = db.query(models.Order).filter(
        models.Order.id == order_id,
        models.Order.user_id == current_user.id
    ).first()
    
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    return order

@router.post("/{order_id}/cancel", response_model=schemas.OrderResponse)
def cancel_order(
    order_id: int,
    current_user: models.User = Depends(auth.get_current_active_user),
    db: Session = Depends(get_db)
):
    """Cancel an order (only if pending)"""
    order = db.query(models.Order).filter(
        models.Order.id == order_id,
        models.Order.user_id == current_user.id
    ).first()
    
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    if order.status != schemas.OrderStatus.PENDING:
        raise HTTPException(status_code=400, detail="Only pending orders can be cancelled")
    
    # Restore stock
    for item in order.items:
        product = db.query(models.Product).filter(models.Product.id == item.product_id).first()
        if product:
            product.stock += item.quantity
    
    order.status = schemas.OrderStatus.CANCELLED
    db.commit()
    db.refresh(order)
    
    return order

# Admin endpoints
@router.get("/admin/all", response_model=List[schemas.OrderResponse])
def get_all_orders(
    current_user: models.User = Depends(auth.get_current_admin_user),
    db: Session = Depends(get_db)
):
    """Get all orders (admin only)"""
    orders = db.query(models.Order).order_by(models.Order.created_at.desc()).all()
    return orders

@router.put("/admin/{order_id}/status", response_model=schemas.OrderResponse)
def update_order_status(
    order_id: int,
    status: schemas.OrderStatus,
    current_user: models.User = Depends(auth.get_current_admin_user),
    db: Session = Depends(get_db)
):
    """Update order status (admin only)"""
    order = db.query(models.Order).filter(models.Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    order.status = status
    db.commit()
    db.refresh(order)
    
    return order
