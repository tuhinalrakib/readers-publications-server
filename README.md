# ⚙️ Readers Publication - Backend API Server

[![Django](https://img.shields.io/badge/Django-6.0.x-092E20?style=for-the-badge&logo=django)](https://www.djangoproject.com/)
[![Django REST Framework](https://img.shields.io/badge/DRF-3.17.x-red?style=for-the-badge&logo=django)](https://www.django-rest-framework.org/)
[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python)](https://www.python.org/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-5432-4169E1?style=for-the-badge&logo=postgresql)](https://www.postgresql.org/)
[![Celery](https://img.shields.io/badge/Celery-Async_Tasks-37814A?style=for-the-badge&logo=celery)](https://docs.celeryq.dev/)
[![Docker](https://img.shields.io/badge/Docker-Ready-2496ED?style=for-the-badge&logo=docker)](https://www.docker.com/)

**Readers Publication Server** is a robust, scalable RESTful API backend built with **Django 6.0**, **Django REST Framework (DRF)**, and **PostgreSQL**. It powers the entire Readers Publication platform, handling user authentication, catalog management, order processing, payment gateway integration, shipping logistics, asynchronous task queues, media processing with Cloudinary, and SMS/Email notifications.

---

## 🚀 Key Features

- **🔐 Authentication & Authorization**:
  - JWT Authentication via `djangorestframework-simplejwt` (Access & Refresh tokens).
  - Custom User model with role-based access control (RBAC).
  - Social Auth integration (Google OAuth).
  - Phone number verification & OTP SMS via Twilio.

- **📚 Catalog & Publication Management**:
  - Book management (categories, tags, digital downloads/preview links, pricing).
  - Author profile management and bio highlights.
  - Blog publishing module with rich text editor (`django-ckeditor-5`).

- **🛒 E-Commerce Engine**:
  - Shopping Cart & Checkout operations (`cart`, `order`, `shipping`).
  - Integrated Payment gateway handlers (`payment`).
  - Invoice generation and order status updates.

- **⚡ Async Task Queue & Media**:
  - Background task execution powered by **Celery**.
  - Cloudinary cloud storage integration with auto-conversion to WEBP format.
  - SMTP Email notifications for user verification & order receipts.

- **🎛️ Modern Admin & API Documentation**:
  - Customized, modern admin dashboard using **Django Unfold**.
  - Interactive API documentation powered by **DRF Yasg (Swagger & ReDoc)**.

---

## 🛠️ Tech Stack

| Component | Technology |
| :--- | :--- |
| **Framework** | Django 6.0 & Django REST Framework (DRF) |
| **Database** | PostgreSQL |
| **Auth** | SimpleJWT, PyJWT, Google OAuth |
| **Async Queue** | Celery & Kombu / AMQP |
| **Admin Theme** | Django Unfold |
| **Media Storage** | Cloudinary & `django-cloudinary-storage` |
| **Notification Services** | Twilio (SMS/OTP) & SMTP (Zoho/SendGrid) |
| **API Specs** | DRF Yasg (Swagger / ReDoc) |
| **Deployment** | Docker, Docker Compose, Vercel ready |

---

## 📁 Architecture & App Structure

```text
readers-publication-server/
├── config/             # Core project configuration (settings, urls, wsgi, asgi)
├── user/               # User model, authentication, profile management, JWT views
├── book/               # Book models, views, categories, digital library content
├── author/             # Author profiles, published works, biographies
├── cart/               # Shopping cart management
├── order/              # Order lifecycle, line items, order status tracking
├── payment/            # Payment gateway integration & webhook endpoints
├── shipping/           # Delivery addresses, shipping rules, & rates
├── blog/               # News, articles, & publication blog posts
├── core/               # Shared base models, mixins, & global utilities
├── utils/              # Helper utilities (Cloudinary helpers, SMS, email services)
├── manage.py           # Django management script
├── Dockerfile          # Container configuration
└── docker-compose.yml  # Multi-container service definitions
```

---

## ⚙️ Environment Variables

Create a `.env` file in the project root based on `sample.env`:

```env
# Core Django Settings
DEBUG=True
SECRET_KEY=your_django_secret_key_here
DJANGO_ENV=development

# Database Settings
DB_NAME=readers_publication
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=127.0.0.1
DB_PORT=5432

# Host URLs
BACKEND_SITE_HOST=http://127.0.0.1:8000
FRONTEND_SITE_HOST=http://127.0.0.1:3000

# Email Provider Configuration (SMTP)
EMAIL_HOST=smtp.zoho.eu
EMAIL_PORT=587
EMAIL_HOST_USER=your_email@domain.com
EMAIL_HOST_PASSWORD=your_email_password
FROM_EMAIL=readers@domain.com

# Twilio (SMS / OTP)
MY_ACCOUNT_SID=your_twilio_account_sid
TWILIO_AUTH_TOKEN=your_twilio_auth_token
MY_TWILIO_NUMBER=+1234567890

# Cloudinary (Media Storage)
CLOUDINARY_CLOUD_NAME=your_cloud_name
CLOUDINARY_API_KEY=your_api_key
CLOUDINARY_API_SECRET=your_api_secret
CLOUDINARY_FOLDER=readers-publication
CLOUDINARY_IMAGE_QUALITY=85
CLOUDINARY_IMAGE_FORMAT=WEBP
```

---

## 💻 Local Setup & Development

### Prerequisites

- **Python**: `3.10+`
- **PostgreSQL**: Running instance or Docker container
- **Redis / RabbitMQ**: (Optional, for Celery task processing)

### Installation Steps

1. **Clone the repository**:
   ```bash
   git clone https://github.com/your-username/readers-publication.git
   cd readers-publication/readers-publication-server
   ```

2. **Create and activate a virtual environment**:
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On Linux/macOS:
   source venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure `.env`**:
   ```bash
   cp sample.env .env
   ```

5. **Run migrations**:
   ```bash
   python manage.py migrate
   ```

6. **Create a superuser**:
   ```bash
   python manage.py createsuperuser
   ```

7. **Start the development server**:
   ```bash
   python manage.py runserver
   ```

8. Access the server endpoints:
   - **API Base**: [http://127.0.0.1:8000](http://127.0.0.1:8000)
   - **Admin Portal**: [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)
   - **Swagger Docs**: [http://127.0.0.1:8000/swagger/](http://127.0.0.1:8000/swagger/)
   - **ReDoc**: [http://127.0.0.1:8000/redoc/](http://127.0.0.1:8000/redoc/)

---

## 🐳 Docker Deployment

### Run with Docker Compose (Development / Production)

```bash
# Build and start PostgreSQL, Django, and Celery containers
docker compose up -d --build
```

To run database migrations inside Docker:
```bash
docker compose exec web python manage.py migrate
```

---

## 📖 API Documentation

Once the server is running, interactive API documentation is automatically served at:
- **Swagger UI**: `/swagger/`
- **ReDoc**: `/redoc/`

---

## 📄 License

This project is proprietary and all rights are reserved by **Readers Publication**.
