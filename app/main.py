from fastapi import FastAPI
from app.api import products, auth, cart, orders 

app = FastAPI(title="E-Commerce API", version="1.0.0")

# Include routers
app.include_router(products.router, prefix="/api")
app.include_router(auth.router, prefix="/api")
app.include_router(cart.router, prefix="/api")  
app.include_router(orders.router, prefix="/api")

@app.get("/")
def root():
    return {
        "message": "Welcome to E-Commerce API",
        "endpoints": {
            "products": "/api/products",
            "auth": "/api/auth",
            "cart": "/api/cart",  
	    "orders": "/api/orders",		
        }
    }

@app.get("/health")
def health_check():
    return {"status": "healthy", "database": "connected"}
