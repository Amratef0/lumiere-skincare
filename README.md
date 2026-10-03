# 🧴 Lumière Skincare

![CI](https://github.com/Amratef0/lumiere-skincare/actions/workflows/ci.yml/badge.svg)
![Python](https://img.shields.io/badge/Python-3.x-3776AB?logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-Gunicorn-000000?logo=flask)
![MySQL](https://img.shields.io/badge/MySQL-Database-4479A1?logo=mysql&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-ready-2496ED?logo=docker&logoColor=white)

A full-stack e-commerce web application for a skincare brand, built with **Flask** and **MySQL**. Customers can browse products, manage a cart (as a guest or a logged-in user), and place orders, while an admin panel manages the product catalogue.

---

## 📌 Table of Contents

- [Tech Stack](#-tech-stack)
- [Features](#-features)
- [Quick Start (Docker)](#-quick-start-docker)
- [Environment Variables](#-environment-variables)
- [Running without Docker](#-running-without-docker)
- [CI/CD](#-cicd)
- [Project Structure](#-project-structure)
- [Database Schema](#️-database-schema)
- [Admin Access](#-admin-access)

---

## 🚀 Tech Stack

| Layer | Technology |
|---|---|
| Frontend | HTML, CSS, JavaScript, Jinja2 templates |
| Backend | Python / Flask, served by Gunicorn |
| Database | MySQL |
| Containerization | Docker & Docker Compose |
| CI/CD | GitHub Actions, GitHub Container Registry (GHCR) |
| Deployment | Railway |

---

## ✨ Features

- 🛍️ Browse and filter products by category
- 🛒 Shopping cart for both guests and logged-in users
- 👤 User registration and login
- 📦 Checkout and order placement
- 👑 Admin panel — add, edit, and delete products
- 📩 Contact form saved to the database
- 📱 Responsive design
- ✅ Client-side validation on all forms (login, register, checkout, contact, product form)

---

## 🐳 Quick Start (Docker)

**Requirements:** [Docker](https://docs.docker.com/get-docker/) with Compose v2 — no Python or MySQL installation needed.

```bash
# 1. Clone the repository
git clone https://github.com/Amratef0/lumiere-skincare.git
cd lumiere-skincare

# 2. Create your environment file (optional — the defaults work out of the box)
cp .env.example .env

# 3. Build and start the app + MySQL
docker compose up --build
```

Open **http://localhost:5000**

**Database initialization**

Every `*.sql` file placed in the `db/` folder runs automatically the first time the MySQL volume is created. Init scripts only run on an empty database, so after editing them:

```bash
docker compose down -v
docker compose up --build
```

**Useful commands**

```bash
docker compose up -d --build     # run in the background
docker compose logs -f web       # follow app logs
docker compose down              # stop containers (keeps the data)
docker compose down -v           # stop and delete the database volume
```

---

## 🔑 Environment Variables

The app reads its database settings from environment variables (the same names Railway's MySQL plugin provides), so the same code runs locally, in Docker, and in production.

| Variable | Description | Compose default |
|---|---|---|
| `MYSQLHOST` | Database host | `db` |
| `MYSQLPORT` | Database port | `3306` |
| `MYSQLUSER` | Database user | `lumiere` |
| `MYSQLPASSWORD` | Database password | `lumiere_pass` |
| `MYSQLDATABASE` | Database name | `lumiere` |
| `SECRET_KEY` | Flask session secret | `change-me` |
| `PORT` | Port Gunicorn listens on | `5000` |

> Set a strong `SECRET_KEY` and different database credentials before deploying anywhere public.

The database connection in `app.py` follows this pattern:

```python
import os
import mysql.connector

def get_db():
    return mysql.connector.connect(
        host=os.environ.get("MYSQLHOST", "localhost"),
        port=int(os.environ.get("MYSQLPORT", 3306)),
        user=os.environ.get("MYSQLUSER", "root"),
        password=os.environ.get("MYSQLPASSWORD", ""),
        database=os.environ.get("MYSQLDATABASE", "lumiere"),
    )
```

---

## 💻 Running without Docker

**Prerequisites:** Python 3.x and a running MySQL server.

```bash
# 1. Clone and enter the project
git clone https://github.com/Amratef0/lumiere-skincare.git
cd lumiere-skincare

# 2. (Optional) create a virtual environment
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt
```

4. Create the database and run the SQL schema from `db/`.
5. Export your MySQL credentials (see [Environment Variables](#-environment-variables)).
6. Run the app:

```bash
flask run
```

Open **http://127.0.0.1:5000**

---

## 🔄 CI/CD

Every push to `main` and every pull request triggers the **GitHub Actions** workflow in `.github/workflows/ci.yml`:

1. **Lint & validate** — installs dependencies, runs Flake8 (syntax errors and undefined names), byte-compiles the code, and validates `docker-compose.yml`.
2. **Build Docker image** — builds the image with Buildx (with layer caching). On pushes to `main`, the image is also published to GitHub Container Registry:

```bash
docker pull ghcr.io/amratef0/lumiere-skincare:latest
```

---

## 📁 Project Structure

```
lumiere-skincare/
├── app.py                  # Flask routes & backend logic
├── Procfile                # Gunicorn config for deployment
├── requirements.txt        # Python dependencies
├── Dockerfile              # Multi-stage image for the Flask app
├── docker-compose.yml      # App + MySQL for local development
├── .dockerignore           # Files excluded from the Docker build context
├── .env.example            # Template for Docker environment variables
├── db/                     # *.sql files here run on first MySQL startup
├── .github/
│   └── workflows/
│       └── ci.yml          # Lint, validate, build (and push) Docker image
├── templates/              # Jinja2 HTML templates
│   ├── index.html
│   ├── shop.html
│   ├── product.html
│   ├── cart.html
│   ├── checkout.html
│   ├── thankyou.html
│   ├── login.html
│   ├── register.html
│   ├── admin.html
│   ├── product-form.html
│   ├── contact.html
│   └── about.html
└── static/
    ├── css/
    │   └── style.css
    ├── js/
    │   ├── base.js
    │   ├── main.js
    │   ├── login.js
    │   ├── register.js
    │   ├── checkout.js
    │   ├── contact.js
    │   └── add-products.js
    └── images/
```

---

## 🗄️ Database Schema

| Table | Description |
|---|---|
| `users` | Registered customers |
| `categories` | Product categories |
| `products` | Product catalogue |
| `cart` | Shopping cart per user / guest |
| `cart_items` | Items inside each cart |
| `orders` | Placed orders |
| `order_items` | Items inside each order |
| `contact_messages` | Contact form submissions |

---

## 👑 Admin Access

The admin panel is available at `/admin`. For the demo, registering with `admin@lumiere.com` creates an admin account.

> ⚠️ Demo-only behavior: in a real deployment, admin roles should be assigned manually in the database, not granted by email at registration.

---

## 👤 Author

**Amr Atef** — [@Amratef0](https://github.com/Amratef0)

*Made with 💖 for every skin story.*
