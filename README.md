# 🛒 E-Commerce API

A production-ready RESTful API for e-commerce platforms built with FastAPI and PostgreSQL.

## ✨ Features

- ✅ **User Authentication** - JWT-based register/login with password hashing
- ✅ **Product Management** - Full CRUD operations for products
- ✅ **Shopping Cart** - Add/remove items, update quantities, auto-calculate totals
- ✅ **Database Integration** - PostgreSQL with SQLAlchemy ORM
- ✅ **API Documentation** - Auto-generated Swagger UI
- ✅ **Security** - Password hashing, JWT tokens, CORS configured

## 🛠️ Tech Stack

| Technology | Purpose |
|------------|---------|
| **FastAPI** | Web framework |
| **PostgreSQL** | Database |
| **SQLAlchemy** | ORM |
| **JWT** | Authentication |
| **bcrypt** | Password hashing |
| **Pydantic** | Data validation |

## 📋 API Endpoints

### 🔐 Authentication
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/auth/register` | Register new user |
| POST | `/api/auth/login` | Login & get JWT token |
| GET | `/api/auth/me` | Get current user info |

### 📦 Products
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/products` | List all products |
| GET | `/api/products/{id}` | Get product by ID |
| POST | `/api/products` | Create product |
| PUT | `/api/products/{id}` | Update product |
| DELETE | `/api/products/{id}` | Delete product |

### 🛒 Shopping Cart (Protected)
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/cart` | View cart |
| POST | `/api/cart/items` | Add item to cart |
| PUT | `/api/cart/items/{id}` | Update quantity |
| DELETE | `/api/cart/items/{id}` | Remove item |
| DELETE | `/api/cart/clear` | Empty cart |

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- PostgreSQL
- Git

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/nurullo-drive/ecommerce-api.git
cd ecommerce-api

## 📦 New Features Added

- ✅ **Complete Orders System** - Checkout, order history, status tracking
- ✅ **Admin Dashboard** - View all orders, update order status
- ✅ **Stock Management** - Automatic stock reduction on checkout
- ✅ **Cart Auto-Clear** - Cart empties automatically after successful order
- ✅ **Fixed bcrypt** - Permanent fix for password hashing
