# 🎬 BookMySeat - Movie Booking System

BookMySeat is a full-stack movie ticket booking web application built with **Django**.  
It allows users to browse movies, select theaters, reserve seats, complete payments, and receive instant booking confirmations.

---

## ✨ Key Features

### 🎥 Browse & Filter Movies
Search movies by genre, language, or keywords.

### 🎞️ Watch Trailers
Embedded YouTube trailers for quick previews.

### ⏳ Seat Reservation System
- Seats are temporarily reserved for **5 minutes**
- If payment is successful → seats are confirmed
- If payment fails or times out → seats are automatically released

### 💳 Stripe Payment Integration
Secure checkout system using Stripe with retry support.

### 📧 Email Notifications
Automatic booking confirmation emails sent to users.

### 📊 Admin Dashboard
Interactive analytics using Chart.js:
- Total revenue
- Most popular movies
- Busiest theaters
- Detailed booking tables

---

## 🛠️ Tech Stack

- **Backend:** Django (Python)
- **Frontend:** Bootstrap, Chart.js
- **Database:** SQLite
- **Payments:** Stripe Checkout
- **Email Service:** SendGrid

---

## ⚙️ Important Notes

### 👤 Admin Access
Every registered user is marked as staff (`is_staff=True`) to access dashboard features.

### 🔗 Admin Panel

### 💳 Stripe Test Cards
- ✅ Success: `4242 4242 4242 4242`
- ❌ Failure: `4000 0000 0000 0002`

### ⏱️ Seat System
Reserved seats are automatically released after **5 minutes** if payment is not completed.

### 📧 Email Confirmation
Check inbox (and spam folder) for booking confirmation emails.

---

## 🚀 Deployment

This project can be deployed on:
- Render
- Railway
- Heroku

---

## 👩‍💻 Author

**Priyanka Yadav**

- GitHub: https://github.com/priyankayadav15  
- Email: priyanka111010@gmail.com  

---

## 📄 License

This project is for educational and personal use.