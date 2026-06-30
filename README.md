# 🛒 Bajar - Django E-Commerce Website

Bajar is a full-featured e-commerce web application built with **Python**, **Django**, **HTML**, **CSS**, **Bootstrap**, and **JavaScript**. It provides a complete online shopping experience where users can browse products, manage their shopping cart, place orders, and make payments through an integrated payment gateway.

---

## 🚀 Features

### User Features

* User registration with email verification
* Secure login and logout
* Password reset via email
* User dashboard
* Profile management
* Browse products by category
* Product search
* Product detail page
* Product image gallery
* Product variations (size, color, etc.)
* Add products to cart
* Update cart quantity
* Remove items from cart
* Checkout process
* Place orders
* Order history
* Order summary
* Payment integration (PayPal Sandbox)
* Invoice generation
* Responsive design for desktop and mobile

---

### Admin Features

* Django Admin Panel
* Product management
* Category management
* Variation management
* Order management
* User management
* Payment management

---

## 🛠️ Technologies Used

### Backend

* Python
* Django

### Frontend

* HTML5
* CSS3
* Bootstrap
* JavaScript

### Database

* SQLite3

### Other Libraries

* Pillow
* Django Authentication System
* Django Messages Framework
* PayPal Sandbox Integration

---

## 📂 Project Structure

```text
Bajar/
│
├── accounts/
├── carts/
├── category/
├── orders/
├── store/
├── templates/
├── static/
├── media/
├── manage.py
├── requirements.txt
└── README.md
```

---

## ⚙️ Installation

### Clone the repository

```bash
git clone https://github.com/Mahessh01/Bajar.git
```

```bash
cd Bajar
```

---

### Create a virtual environment

Windows

```bash
python -m venv venv
```

Activate it

```bash
venv\Scripts\activate
```

---

### Install dependencies

```bash
pip install -r requirements.txt
```

---

### Apply migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

---

### Create a superuser

```bash
python manage.py createsuperuser
```

---

### Run the development server

```bash
python manage.py runserver
```

Open your browser and visit

```
http://127.0.0.1:8000/
```

---

## 📧 Email Configuration

Configure your email credentials in your environment variables or settings file for:

* Account verification
* Password reset emails

---

## 💳 Payment Gateway

The project currently uses **PayPal Sandbox** for testing payments.

To use it:

* Create PayPal Sandbox Buyer and Seller accounts.
* Add your Sandbox Client ID and Secret to your project settings.
* Use Sandbox accounts for testing transactions.

---

## 🔐 Authentication Features

* Email verification
* Secure authentication
* Login required for checkout
* Password reset using email token
* Session-based authentication

---

## 📸 Screens

The project includes pages such as:

* Home
* Store
* Product Details
* Cart
* Checkout
* Payment
* Order Complete
* User Dashboard
* Login
* Register
* Password Reset
* Admin Panel

---

## 📈 Future Improvements

* Wishlist
* Product reviews and ratings
* Coupon system
* Online payment gateways (Stripe, Khalti, eSewa)
* Order tracking
* User profile image upload
* Product recommendations
* Sales analytics dashboard
* Inventory notifications
* REST API
* Mobile application

---

## 📄 Requirements

Generate the requirements file using:

```bash
pip freeze > requirements.txt
```

Install packages using:

```bash
pip install -r requirements.txt
```

---


## 👨‍💻 Author

**Mahesh Pharswan**

GitHub: https://github.com/Mahessh01/Bajar

---

## 📜 License

This project is created for learning purposes and personal portfolio development.

Feel free to use, modify, and improve it for educational purposes.
