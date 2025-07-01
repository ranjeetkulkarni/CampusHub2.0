# Campus Hub 2.0

Campus Hub 2.0 is a modern, production-ready web application for campus communities, built with Flask, SQLAlchemy ORM, and Supabase (PostgreSQL for data, Supabase Storage for images). It provides two main platforms:

- **Lost & Found:** Report, search, and manage lost or found items.
- **Marketplace:** Post, browse, and manage items for sale or rent.

The project includes user authentication, email verification, image uploads to Supabase Storage, feedback/comments, and admin utilities. All legacy SQLite, PIL, and local file upload logic have been removed for a fully cloud-native experience.

---

## Table of Contents
- [Features](#features)
- [Project Structure](#project-structure)
- [Setup Instructions](#setup-instructions)
- [Configuration](#configuration)
- [Database Schema](#database-schema)
- [Core Functionality](#core-functionality)
- [Usage Guide](#usage-guide)
- [Security & Best Practices](#security--best-practices)
- [Extending the App](#extending-the-app)
- [Dockerization & Deployment](#dockerization--deployment)
- [License](#license)

---

## Features

### User Management
- **Registration & Login:** Secure registration and login with hashed passwords (Werkzeug).
- **Email Verification:** Users must verify their email via Flask-Mail before accessing both platforms.
- **Roles:** Supports admin, student, and guest roles.
- **Session Management:** Persistent sessions using Flask-Session.

### Lost & Found Platform
- **Add Lost/Found Items:** Users can report lost or found items with details, images (stored in Supabase), and location.
- **Browse & Search:** Filter and sort items by category, status, and priority.
- **Feedback/Comments:** Users can comment on items for more information.

### Marketplace Platform
- **Post for Sale/Rent:** Users can list items for sale or rent with price, description, and images (stored in Supabase).
- **Browse & Search:** Filter and sort marketplace items by category, price, or condition.
- **Feedback/Comments:** Users can comment on marketplace items to inquire or negotiate.

### Admin Utilities
- **Category Management:** Script to initialize default categories.
- **Default Admin Account:** Pre-configured admin/admin123 for management and testing.

### Image Handling
- **Upload to Supabase Storage:** Images are uploaded directly to Supabase Storage buckets.
- **Allowed Formats:** PNG, JPG, JPEG, WEBP.
- **Image Validation:** Only valid image types are accepted.

---

## Project Structure

```
Campus-Hub-2.0/
├── Main.py                # Main Flask application entry point
├── config.py              # Configuration settings (Supabase, mail, sessions, etc.)
├── models.py              # SQLAlchemy ORM models and core logic
├── extensions.py          # Flask extensions (e.g., mail)
├── blueprints/            # Flask blueprints for modular routes
│   ├── auth/
│   ├── lost_and_found/
│   └── marketplace/
├── static/
│   └── images/            # (Legacy, not used; images now in Supabase)
├── templates/             # HTML templates (Jinja2)
│   ├── base.html
│   ├── 404.html, 500.html
│   ├── auth/
│   ├── lost_and_found/
│   └── marketplace/
├── flask_session/         # Session files (auto-generated)
├── lostnfound.db          # (Legacy, not used)
├── requirements.txt       # Python dependencies
├── .env                   # Environment variables (Supabase, DB, mail, secret)
└── init_categories.py     # Script to initialize default categories
```

---

## Setup Instructions

### 1. Clone the Repository
```sh
git clone <your-repo-url>
cd Campus-Hub-2.0
```

### 2. Create & Activate a Virtual Environment (Recommended)
```sh
python -m venv venv
# On Windows:
venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate
```

### 3. Install Dependencies
```sh
pip install -r requirements.txt
```

### 4. Configuration
- Copy `.env.example` to `.env` and fill in your Supabase/PostgreSQL, Supabase Storage, and mail credentials.
- Edit `config.py` if you need to override any settings.

### 5. Initialize Categories (Optional, recommended for first run)
```sh
python init_categories.py
```

### 6. Run the Application
```sh
python Main.py
```
- Open your browser and navigate to: http://127.0.0.1:5000/

---

## Configuration
All configuration values are managed in `.env` and `config.py`. Key settings include:

| Key                      | Description                                      |
|--------------------------|--------------------------------------------------|
| POSTGRES_URI             | PostgreSQL connection string (Supabase)          |
| SUPABASE_URL             | Supabase project URL                             |
| SUPABASE_KEY             | Supabase service key                             |
| SUPABASE_LOSTFOUND_BUCKET| Supabase Storage bucket for lost/found images    |
| SUPABASE_MARKETPLACE_BUCKET| Supabase Storage bucket for marketplace images |
| MAIL_SERVER, MAIL_PORT   | SMTP server and port                             |
| MAIL_USERNAME, MAIL_PASSWORD | Email credentials for Flask-Mail           |
| SECRET_KEY               | Flask secret key (change for production)         |
| SESSION_TYPE, SESSION_FILE_DIR, SESSION_PERMANENT | Flask-Session settings |

---

## Database Schema (PostgreSQL via SQLAlchemy ORM)

### Tables & Fields

#### 1. user
| Column      | Type      | Description                        |
|-------------|-----------|------------------------------------|
| id          | INTEGER   | Primary key                        |
| username    | TEXT      | Unique username                    |
| password    | TEXT      | Hashed password                    |
| email       | TEXT      | Unique user email                  |
| role        | TEXT      | User role (admin, student, guest)  |
| created_at  | DATETIME  | Timestamp of registration          |
| is_admin    | BOOLEAN   | True if user is an admin           |
| is_confirmed| BOOLEAN   | True if email is verified          |

#### 2. lost_found_item
| Column      | Type      | Description                        |
|-------------|-----------|------------------------------------|
| id          | INTEGER   | Primary key                        |
| name        | TEXT      | Name/title of the item             |
| description | TEXT      | Detailed description               |
| category    | TEXT      | Category name                      |
| status      | TEXT      | "lost" or "found"                  |
| priority    | INTEGER   | Priority level                     |
| date        | DATE      | Date when reported                 |
| location    | TEXT      | Location details                   |
| contact_info| TEXT      | Contact details                    |
| latitude    | REAL      | Latitude coordinate (optional)     |
| longitude   | REAL      | Longitude coordinate (optional)    |
| user_id     | INTEGER   | Foreign key to user.id             |
| found_by    | INTEGER   | User ID who found the item         |
| claimed_by  | INTEGER   | User ID who claimed the item       |
| is_deleted  | BOOLEAN   | Soft delete flag                   |

#### 3. marketplace_item
| Column      | Type      | Description                        |
|-------------|-----------|------------------------------------|
| id          | INTEGER   | Primary key                        |
| name        | TEXT      | Name/title of the item             |
| description | TEXT      | Detailed description               |
| price       | NUMERIC   | Price of the item                  |
| category    | TEXT      | Category name                      |
| condition   | TEXT      | Condition (e.g., "New", "Used")    |
| status      | TEXT      | "available", "sold", or "rented"    |
| date        | DATE      | Date when posted                   |
| location    | TEXT      | Location details                   |
| contact_info| TEXT      | Contact details of seller          |
| user_id     | INTEGER   | Foreign key to user.id             |
| is_deleted  | BOOLEAN   | Soft delete flag                   |

#### 4. category
| Column      | Type      | Description                        |
|-------------|-----------|------------------------------------|
| id          | INTEGER   | Primary key                        |
| name        | TEXT      | Category name                      |
| type        | TEXT      | Either lost_found or marketplace   |
| description | TEXT      | Category description (optional)    |

#### 5. item_image
| Column      | Type      | Description                        |
|-------------|-----------|------------------------------------|
| id          | INTEGER   | Primary key                        |
| item_type   | TEXT      | 'lost_found' or 'marketplace'      |
| item_id     | INTEGER   | ID of the associated item          |
| image_url   | TEXT      | Public URL in Supabase Storage     |
| uploaded_at | DATETIME  | Timestamp of upload                |

#### 6. feedback
| Column      | Type      | Description                        |
|-------------|-----------|------------------------------------|
| id          | INTEGER   | Primary key                        |
| user_id     | INTEGER   | Foreign key to user.id             |
| item_type   | TEXT      | Either lost_found or marketplace   |
| item_id     | INTEGER   | ID of the associated item          |
| comment     | TEXT      | User’s feedback or comment         |
| rating      | INTEGER   | Optional rating                    |
| date        | DATETIME  | Timestamp when comment was posted  |

---

## Core Functionality
All database operations and core logic are implemented in `models.py` using SQLAlchemy ORM. All image uploads are handled via Supabase Storage.

---

## Usage Guide

### 1. User Registration & Login
- Register a new account or use the default admin:
  - Username: admin
  - Password: admin123
- Email verification is required — check your inbox for the confirmation link.
- Log in to access both Lost & Found and Marketplace platforms.

### 2. Lost & Found Platform
- **Add Item:** Click “Add Lost/Found Item”, fill in details (name, description, category, status, location), and upload an image.
- **Browse/Search:** Use filters (category, status) and sorting to find items.
- **Comment:** Click on an item to view details and add feedback/comments.

### 3. Marketplace Platform
- **Add Item:** Navigate to “Add Marketplace Item”, fill in details (name, description, price, category, condition), and upload an image.
- **Browse/Search:** Filter by category, price range, or condition to find listings.
- **Comment:** Click on a listing to view details and leave feedback or inquiries.

### 4. Admin Dashboard
- Log in as admin to access special utilities:
  - Manage categories and users.
  - Edit or delete any user, lost/found item, or marketplace item.

---

## Security & Best Practices
- **Password Hashing:** Passwords are securely hashed using Werkzeug.
- **Session Security:** Sessions are stored on the filesystem (Flask-Session) with a secret key.
- **CSRF Protection:** Enabled via Flask-WTF for all forms.
- **Image Uploads:**
  - Restricted to allowed extensions (png, jpg, jpeg, webp).
  - Images are uploaded directly to Supabase Storage.
- **Email Verification:** SMTP credentials are kept in environment variables or `.env` (do not commit real credentials).
- **Configuration Management:** Use environment variables or a `.env` file for sensitive data (e.g., SUPABASE_KEY, MAIL_PASSWORD, SECRET_KEY).

---

## Extending the App
- **Add New Blueprints:** Create additional Flask blueprints for new features (e.g., Events, Forums).
- **Extend Models & Templates:**
  - Add new fields or tables in `models.py` and update related templates.
  - Customize HTML/CSS in `templates/` and `static/`.
- **Advanced Search & Analytics:** Integrate full-text search or analytics tools.
- **Notifications:** Add real-time notifications using WebSockets (Flask-SocketIO).
- **REST API Endpoints:** Expose CRUD operations via a RESTful API (Flask-RESTful or Flask-API).

---

## Dockerization & Deployment

### Docker Build & Run

1. **Build the Docker image:**
   ```sh
   docker build -t campus-hub .
   ```
2. **Run the container:**
   ```sh
   docker run --env-file .env -p 5000:5000 campus-hub
   ```

Or use Docker Compose:

```sh
docker-compose up --build
```

### Production Deployment (CI/CD)

- This project includes a GitHub Actions workflow for CI/CD (`.github/workflows/deploy.yml`).
- On every push to `main`, it will:
  - Build and push the Docker image to DockerHub.
  - Optionally deploy to your server via SSH (edit the workflow as needed).

**Secrets required in your GitHub repo:**
- `DOCKERHUB_USERNAME`, `DOCKERHUB_TOKEN` (for DockerHub push)
- `SERVER_HOST`, `SERVER_USER`, `SERVER_SSH_KEY` (for remote deploy)

**On your server:**
- Ensure Docker is installed and your `.env` file is present.
- The workflow will pull the latest image and restart the container automatically.

---

## License
MIT License

