from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app import models, schemas
from app.api import auth  # This imports the router AND the functions
from app.database import get_db

router = APIRouter(prefix="/cart", tags=["Cart"])

def get_or_create_cart(user: models.User, db: Session):
    """Helper to get or create a cart for the user"""
    if not user.cart:
        cart = models.Cart(user_id=user.id)
        db.add(cart)
        db.commit()
        db.refresh(cart)
        return cart
    return user.cart

@router.get("/", response_model=schemas.CartResponse)
def get_cart(
    current_user: models.User = Depends(auth.get_current_active_user),  # This now works
    db: Session = Depends(get_db)
):
    """Get current user's cart"""
    cart = get_or_create_cart(current_user, db)
    return cart


@router.post("/items", response_model=schemas.CartResponse)
def add_to_cart(
    item: schemas.CartItemCreate,
    current_user: models.User = Depends(auth.get_current_active_user),
    db: Session = Depends(get_db)
):
    """Add item to cart"""
    # Check if product exists and is active
    product = db.query(models.Product).filter(
        models.Product.id == item.product_id,
        models.Product.is_active == True
    ).first()
    
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    if product.stock < item.quantity:
        raise HTTPException(status_code=400, detail="Insufficient stock")
    
    # Get or create cart
    cart = get_or_create_cart(current_user, db)
    
    # Check if item already in cart
    cart_item = db.query(models.CartItem).filter(
        models.CartItem.cart_id == cart.id,
        models.CartItem.product_id == item.product_id
    ).first()
    
    if cart_item:
        # Update quantity
        cart_item.quantity += item.quantity
    else:
        # Create new cart item
        cart_item = models.CartItem(
            cart_id=cart.id,
            product_id=item.product_id,
            quantity=item.quantity
        )
        db.add(cart_item)
    
    db.commit()
    db.refresh(cart)
    return cart

@router.put("/items/{item_id}", response_model=schemas.CartResponse)
def update_cart_item(
    item_id: int,
    item_update: schemas.CartItemUpdate,
    current_user: models.User = Depends(auth.get_current_active_user),
    db: Session = Depends(get_db)
):
    """Update item quantity in cart"""
    cart_item = db.query(models.CartItem).join(models.Cart).filter(
        models.CartItem.id == item_id,
        models.Cart.user_id == current_user.id
    ).first()
    
    if not cart_item:
        raise HTTPException(status_code=404, detail="Item not found in cart")
    
    if item_update.quantity <= 0:
        db.delete(cart_item)
    else:
        if cart_item.product.stock < item_update.quantity:
            raise HTTPException(status_code=400, detail="Insufficient stock")
        cart_item.quantity = item_update.quantity
    
    db.commit()
    return get_or_create_cart(current_user, db)

@router.delete("/items/{item_id}", response_model=schemas.CartResponse)
def remove_from_cart(
    item_id: int,
    current_user: models.User = Depends(auth.get_current_active_user),
    db: Session = Depends(get_db)
):
    """Remove item from cart"""
    cart_item = db.query(models.CartItem).join(models.Cart).filter(
        models.CartItem.id == item_id,
        models.Cart.user_id == current_user.id
    ).first()
    
    if not cart_item:
        raise HTTPException(status_code=404, detail="Item not found in cart")
    
    db.delete(cart_item)
    db.commit()
    
    return get_or_create_cart(current_user, db)

@router.delete("/clear", response_model=schemas.CartResponse)
def clear_cart(
    current_user: models.User = Depends(auth.get_current_active_user),
    db: Session = Depends(get_db)
):
    """Clear entire cart"""
    if current_user.cart:
        current_user.cart.items.clear()
        db.commit()
    
    return get_or_create_cart(current_user, db)