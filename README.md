Lumière Skincare

A full-stack e-commerce web application for a skincare brand, built with Flask and MySQL.

---

## Tech Stack

- **Frontend:** HTML, CSS, JavaScript
- **Backend:** Python / Flask
- **Database:** MySQL
- **Deployment:** Railway

---

## Features

- :shopping_bags: Browse and filter products by category
- :shopping_cart: Add to cart (guest & logged-in users)
- :bust_in_silhouette: User registration & login
- :package: Checkout and order placement
- :crown: Admin panel — Add / Edit / Delete products
- :envelope_with_arrow: Contact form saved to database
- :mobile_phone: Responsive design

---

## Project Structure

```
web_final_project/
├── app.py              # Flask routes & backend logic
├── Procfile            # Gunicorn config for deployment
├── requirements.txt    # Python dependencies
├── templates/          # Jinja2 HTML templates
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

## :file_cabinet: Database Schema

- `users` — registered customers
- `categories` — product categories
- `products` — product catalogue
- `cart` — shopping cart per user/guest
- `cart_items` — items inside each cart
- `orders` — placed orders
- `order_items` — items inside each order
- `contact_messages` — contact form submissions

---

## Run Locally

1. Clone the repo:

```bash
git clone https://github.com/Amratef0/lumiere-skincare.git
cd lumiere-skincare
```

2. Install dependencies:

```bash
pip install flask mysql-connector-python gunicorn
```

3. Set up MySQL and run the SQL schema.

4. Update `get_db()` in `app.py` with your local MySQL credentials.

5. Run the app:

```bash
py -m flask run
```

6. Open [http://127.0.0.1:5000](http://127.0.0.1:5000)

---

## Admin Access

Register with `admin@lumiere.com` to access the admin panel at `/admin`.

---

## Project Requirements Met

| Requirement                      | Status                                                              |
| -------------------------------- | ------------------------------------------------------------------- |
| At least 4 pages                 | :white_check_mark: 12 pages                                         |
| At least 2 forms                 | :white_check_mark: Login, Register, Checkout, Contact, Product form |
| Data saved in MySQL              | :white_check_mark:                                                  |
| Data retrieved from MySQL        | :white_check_mark:                                                  |
| No hardcoded data in HTML        | :white_check_mark:                                                  |
| Add / View / Update / Delete     | :white_check_mark: Admin panel                                      |
| External CSS file                | :white_check_mark: style.css                                        |
| JavaScript validation            | :white_check_mark: All forms validated                              |
| Flask routes handle all requests | :white_check_mark:                                                  |
| MySQL tables created by student  | :white_check_mark:                                                  |

---

_Made with :sparkling_heart: for every skin story._
