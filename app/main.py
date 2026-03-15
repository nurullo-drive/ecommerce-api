from fastapi import FastAPI
from app.api import products, auth, cart  # Add cart

app = FastAPI(title="E-Commerce API", version="1.0.0")

# Include routers
app.include_router(products.router, prefix="/api")
app.include_router(auth.router, prefix="/api")
app.include_router(cart.router, prefix="/api")  # NEW

@app.get("/")
def root():
    return {
        "message": "Welcome to E-Commerce API",
        "endpoints": {
            "products": "/api/products",
            "auth": "/api/auth",
            "cart": "/api/cart"  # NEW
        }
    }

@app.get("/health")
def health_check():
    return {"status": "healthy", "database": "connected"}