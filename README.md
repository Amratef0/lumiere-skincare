# Lumière Skincare

A full-stack e-commerce web application for a skincare brand, built with Flask and MySQL.


---

## Tech Stack

- **Frontend:** HTML, CSS, JavaScript
- **Backend:** Python / Flask (served by Gunicorn)
- **Database:** MySQL
- **Containerization:** Docker & Docker Compose
- **CI:** GitHub Actions
- **Deployment:** Railway

---

## Features

- :shopping_bags: Browse and filter products by category
- 🛒 Add to cart (guest & logged-in users)
- 👤 User registration & login
- 📦 Checkout and order placement
- 👑 Admin panel — Add / Edit / Delete products
- 📩 Contact form saved to database
- :mobile_phone: Responsive design

---

## Project Structure

```
web_final_project/
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

- `users` — registered customers
- `categories` — product categories
- `products` — product catalogue
- `cart` — shopping cart per user/guest
- `cart_items` — items inside each cart
- `orders` — placed orders
- `order_items` — items inside each order
- `contact_messages` — contact form submissions

---

## Run with Docker (recommended)

The quickest way to get the app and its MySQL database running. Requires [Docker](https://docs.docker.com/get-docker/) with Compose v2.

1. Clone the repo:

```bash
git clone https://github.com/Amratef0/lumiere-skincare.git
cd lumiere-skincare
```

2. Create your environment file (optional, defaults work out of the box):

```bash
cp .env.example .env
```

3. Put your SQL schema in the `db/` folder (e.g. `db/schema.sql`). MySQL runs every `*.sql` file in that folder automatically the first time the database volume is created.

4. Build and start everything:

```bash
docker compose up --build
```

5. Open <http://localhost:5000>

Useful commands:

```bash
docker compose up -d --build     # run in the background
docker compose logs -f web       # follow app logs
docker compose down              # stop containers (keeps the data)
docker compose down -v           # stop and delete the database volume
```

> **Re-running the schema:** init scripts only run on an empty database. After editing `db/*.sql`, run `docker compose down -v` and start again.

### Environment variables

The app reads its database settings from the environment (the same names Railway's MySQL plugin provides):

| Variable        | Description              | Compose default |
| --------------- | ------------------------ | --------------- |
| `MYSQLHOST`     | Database host            | `db`            |
| `MYSQLPORT`     | Database port            | `3306`          |
| `MYSQLUSER`     | Database user            | `lumiere`       |
| `MYSQLPASSWORD` | Database password        | `lumiere_pass`  |
| `MYSQLDATABASE` | Database name            | `lumiere`       |
| `SECRET_KEY`    | Flask session secret     | `change-me`     |
| `PORT`          | Port Gunicorn listens on | `5000`          |

Make sure `get_db()` in `app.py` uses them:

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

## Run Locally (without Docker)

1. Clone the repo:

```bash
git clone https://github.com/Amratef0/lumiere-skincare.git
cd lumiere-skincare
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Set up MySQL and run the SQL schema.

4. Export your local MySQL credentials (see the environment variables table above), or edit `get_db()` in `app.py`.

5. Run the app:

```bash
py -m flask run
```

6. Open <http://127.0.0.1:5000>

---

## Continuous Integration

Every push to `main` and every pull request triggers the workflow in `.github/workflows/ci.yml`:

1. **Lint & validate** — installs dependencies, runs Flake8 (syntax errors and undefined names), byte-compiles the code and validates `docker-compose.yml`.
2. **Build Docker image** — builds the image with Buildx (with layer caching). On pushes to `main` the image is also published to GitHub Container Registry:

```bash
docker pull ghcr.io/amratef0/lumiere-skincare:latest
```

---

## Admin Access

Register with `admin@lumiere.com` to access the admin panel at `/admin`.

---

## Project Requirements Met

| Requirement                      | Status                                             |
| -------------------------------- | -------------------------------------------------- |
| At least 4 pages                 | ✅ 12 pages                                         |
| At least 2 forms                 | ✅ Login, Register, Checkout, Contact, Product form |
| Data saved in MySQL              | ✅                                                  |
| Data retrieved from MySQL        | ✅                                                  |
| No hardcoded data in HTML        | ✅                                                  |
| Add / View / Update / Delete     | ✅ Admin panel                                      |
| External CSS file                | ✅ style.css                                        |
| JavaScript validation            | ✅ All forms validated                              |
| Flask routes handle all requests | ✅                                                  |
| MySQL tables created by student  | ✅                                                  |

---

*Made with 💖 for every skin story.*
