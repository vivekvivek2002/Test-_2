# AURA — Minimalist High-End E-Commerce Platform

A production-ready full-stack Django e-commerce platform inspired by the Apple Store aesthetic, featuring original brand design, frosted glass styling, database-driven hero banners, and a customized administration suite.

> **Project Constraint Note:** Built strictly as a product showcase and portfolio platform. Contains **no cart, no checkout/payment gateways, and no reviews**.

---

## Technical Assignment Submission Summary

| # | Submission Item | Details |
|---|---|---|
| **1** | **Live Demo URL** | `https://aura-store.onrender.com` *(Replace with your live Render URL upon deployment)* |
| **2** | **Admin Panel URL** | `https://aura-store.onrender.com/admin/` *(Local: `http://127.0.0.1:8000/admin/`)* |
| **3** | **Admin Credentials** | Username: `admin` \| Password: `AdminPass123!` |
| **4** | **Test User Credentials** | Username: `customer` \| Password: `CustomerPass123!` |
| **5** | **GitHub Repository** | `https://github.com/<your-username>/aura-store` *(Push local repo to GitHub)* |
| **6** | **Technologies Used** | Python 3, Django 4.2 LTS, Django Admin, Django Auth, Tailwind CSS, Gunicorn, WhiteNoise, Pillow |
| **7** | **Database Used** | SQLite (Local Development) / PostgreSQL (Production via `dj-database-url`) |
| **8** | **Major Features** | Database-driven homepage & hero carousel, category listing, product detail with specs, user auth (register/login/logout), protected profile edit, customized admin with image previews & `is_active` toggling |
| **9** | **Third-Party Libraries** | `dj-database-url`, `psycopg2-binary`, `Pillow`, `whitenoise`, `gunicorn`, `python-dotenv`, `django-cloudinary-storage`, `cloudinary` |

---

## 1. Technologies & Architecture

- **Backend Framework**: Python 3.9+ & Django 4.2 LTS
- **Database**:
  - **Local Development**: SQLite (`db.sqlite3`)
  - **Production**: PostgreSQL (configured dynamically via `dj-database-url`)
- **Frontend & Styling**: Plain HTML5, Tailwind CSS (via CDN), custom CSS with glassmorphism blur filters, and lightweight vanilla JavaScript for hero carousel interactions.
- **Media Storage**:
  - **Local Development**: Local filesystem storage via `MEDIA_ROOT`
  - **Production**: Cloudinary integration (`django-cloudinary-storage`) triggered when `CLOUDINARY_URL` is set
- **Static Assets Serving**: WhiteNoise (`whitenoise.middleware.WhiteNoiseMiddleware`) with `CompressedManifestStaticFilesStorage`
- **WSGI Application Server**: Gunicorn
- **Deployment Platform**: Render (`render.yaml`, `build.sh`, `Procfile`)

---

## 2. Third-Party Libraries

| Package | Version | Purpose & Rationale |
|---|---|---|
| `Django` | `^4.2` | Core web framework, ORM, authentication, and admin engine |
| `dj-database-url` | `^3.0` | 12-factor database URL configuration (SQLite dev / PostgreSQL prod) |
| `psycopg2-binary` | `^2.9` | High-performance PostgreSQL database adapter for production |
| `Pillow` | `^11.0` | Image processing, validation, and sample asset generation for `ImageField` |
| `whitenoise` | `^6.11` | Self-contained static asset serving directly from Gunicorn without Nginx |
| `gunicorn` | `^23.0` | High-concurrency production WSGI HTTP server |
| `python-dotenv` | `^1.2` | Loads local environment variables from `.env` |
| `django-cloudinary-storage` | `^0.3` | Seamless cloud media upload and CDN hosting for production |
| `cloudinary` | `^1.46` | Official Cloudinary Python SDK |

---

## 3. Data Models & Public Visibility

### App: `store`
- **`Category`**: `name`, `slug` (unique), `image`, `is_active`, `created_at`
- **`Product`**: `name`, `slug` (unique), `description`, `price`, `image`, `category` (ForeignKey), `is_active`, `is_featured`, `created_at`
- **`Banner`**: `title`, `subtitle`, `image`, `button_text`, `button_link`, `is_active`, `order`

### App: `accounts`
- Leverages Django's built-in `User` model (`username`, `first_name`, `last_name`, `email`, `password`, `is_active`, `is_staff`, `date_joined`).
- Protected Profile page for viewing and editing `first_name`, `last_name`, and `email`.

> **Immediate Reflection Rule**: All public views strictly query `is_active=True`. Changes made by administrators in the Django Admin immediately appear or disappear from the public storefront.

---

## 4. Key Features Implemented

1. **Database-Driven Homepage (`/`)**:
   - Dynamic sticky navigation with categories loaded from the database via context processor.
   - Hero banner carousel with auto-play (5.5s), pause on hover, manual next/previous navigation, and indicator dots.
   - Value propositions bar (complimentary shipping, 2-year warranty, 14-day evaluation).
   - "Featured Innovations" grid highlighting active featured products.
   - "Browse Categories" card grid with active product counts.
   - Promotional design philosophy callout section.
   - Clean 4-column Apple-style footer.
2. **Category Product Listing (`/category/<slug>/`)**:
   - Breadcrumb navigation (`Home / Categories / Category Name`).
   - Category header hero banner with live active model count.
   - Responsive grid of active products in that category.
   - Immediate 404 response if the category is disabled (`is_active=False`).
3. **Product Detail View (`/product/<slug>/`)**:
   - Large studio product image showcase.
   - Category badge, title, formatted price, and full description.
   - Structured technical specifications (hardware identifier, chassis engineering, what's in the box, release date).
   - Authorized retailer availability notice.
   - "Related in Category" recommendation grid.
   - Immediate 404 response if product or its parent category is deactivated.
4. **User Authentication & Protected Profile**:
   - **Registration (`/accounts/register/`)**: custom registration form with unique email validation and automatic sign-in.
   - **Login (`/accounts/login/`)**: authentication form with error handling and `next` parameter redirection.
   - **Logout (`/accounts/logout/`)**: clean session termination with feedback banner.
   - **Profile (`/accounts/profile/`)**: `@login_required` view to inspect account details and edit `first_name`, `last_name`, and `email`.
5. **Customized Django Admin (`/admin/`)**:
   - Custom branding: "AURA Administration" & "Store Management & Catalog Control".
   - Categories: image thumbnail previews, `list_editable = ('is_active',)` for 1-click toggling, total products count, and slug auto-population.
   - Products: image thumbnail previews, `list_editable = ('is_active', 'is_featured')`, category and featured filters, search by name/description.
   - Banners: image previews, `list_editable = ('order', 'is_active')`, re-ordering.
   - Users: customized `UserAdmin` with `list_editable = ('is_active',)`.
6. **Data Seeding**:
   - `python manage.py seed_data` command to generate default superuser, test customer, categories, hero banners, 12 products, and image assets using Pillow.

---

## 5. Local Setup Instructions

### 1. Clone the repository & navigate into workspace
```bash
git clone <repo-url>
cd task_2
```

### 2. Create and activate a Python virtual environment
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure environment variables (Optional for local dev)
```bash
cp .env.example .env
```
*(By default, SQLite is used locally if `DATABASE_URL` is not set)*

### 5. Apply migrations
```bash
python manage.py migrate
```

### 6. Populate database with sample categories, products, and banners
```bash
python manage.py seed_data
```

### 7. Run the development server
```bash
python manage.py runserver
```
Visit `http://127.0.0.1:8000/` in your browser.

---

## 6. Pre-Configured Test Credentials

| Role | Username | Password | Email | Purpose |
|---|---|---|---|---|
| **Superuser / Admin** | `admin` | `AdminPass123!` | `admin@aurastore.com` | Access Django Admin at `/admin/` |
| **Test Customer** | `customer` | `CustomerPass123!` | `customer@aurastore.com` | Test Login & Profile at `/accounts/login/` |

---

## 7. Render Deployment Instructions

### Automatic Deployment via `render.yaml` (Blueprint)
1. Push this repository to GitHub or GitLab.
2. In the Render Dashboard, select **New +** → **Blueprint**.
3. Connect your repository. Render will automatically detect `render.yaml` and configure:
   - A Python Web Service running `./build.sh` and `gunicorn aura_core.wsgi:application`.
   - A managed PostgreSQL instance linked via `DATABASE_URL`.
4. In the Render Web Service settings, add your `CLOUDINARY_URL` (if using Cloudinary for media uploads).
5. Once deployed, open the Render SSH Shell or run a one-off command to seed the catalog:
   ```bash
   python manage.py seed_data
   ```

### Manual Service Setup
- **Build Command**: `./build.sh`
- **Start Command**: `gunicorn aura_core.wsgi:application`
- **Environment Variables**:
  - `SECRET_KEY`: `<generate-random-secret>`
  - `DEBUG`: `False`
  - `ALLOWED_HOSTS`: `.onrender.com`
  - `DATABASE_URL`: `postgres://...`
  - `CLOUDINARY_URL`: `cloudinary://...` (optional, for persistent media)

---

## 8. Automated Test Suite

Run the full automated test suite (covering models, admin, storefront views, permissions, and authentication):
```bash
python manage.py test
```
All 14 unit tests pass cleanly out of the box.
