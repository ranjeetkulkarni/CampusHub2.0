# Campus Hub

Campus Hub is a full-featured web application for campus communities, built with **Flask** and **SQLite**. It provides two main platforms:

- **Lost & Found:** Report, search, and manage lost or found items.
- **Marketplace:** Post, browse, and manage items for sale or rent.

The project includes user authentication, email verification, image uploads, feedback/comments, and admin utilities.

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
- [License](#license)

---

## Features

### User Management
- **Registration & Login:** Secure registration and login with SHA-256-hashed passwords.
- **Email Verification:** Users must verify their email via Flask-Mail before accessing both platforms.
- **Roles:** Supports `admin`, `student`, and `guest` roles.
- **Session Management:** Persistent sessions using Flask-Session.

### Lost & Found Platform
- **Add Lost/Found Items:** Users can report lost or found items with details, images, and location.
- **Browse & Search:** Filter and sort items by category, status, and priority.
- **Feedback/Comments:** Users can comment on items for more information.

### Marketplace Platform
- **Post for Sale/Rent:** Users can list items for sale or rent with price, description, and images.
- **Browse & Search:** Filter and sort marketplace items by category, price, or condition.
- **Feedback/Comments:** Users can comment on marketplace items to inquire or negotiate.

### Admin Utilities
- **Database Reset Script:** `reset_db.py` to reset and initialize the database with default users, categories, and sample data.
- **Default Admin Account:** Pre-configured `admin/admin123` for management and testing.

### Image Handling
- **Upload & Resize:** Images are uploaded, resized, and compressed for efficiency.
- **Allowed Formats:** PNG, JPG, JPEG, WEBP.
- **Image Validation:** `allowed_file()` utility to check file extensions.

---

## Project Structure

```
Campus-Hub/
├── Main.py                # Main Flask application entry point
├── config.py              # Configuration settings (database, mail, sessions, etc.)
├── models.py              # Database models and core functionality
├── reset_db.py            # Script to reset/initialize the database
├── extensions.py          # Flask extensions (e.g., mail)
├── blueprints/            # Flask blueprints for modular routes
│   ├── auth/
│   ├── lost_and_found/
│   └── marketplace/
├── static/
│   └── images/            # Directory for uploaded user images
├── templates/             # HTML templates (Jinja2)
│   ├── base.html
│   ├── 404.html, 500.html
│   ├── auth/
│   ├── lost_and_found/
│   └── marketplace/
├── flask_session/         # Session files (auto-generated)
└── lostnfound.db          # SQLite database file
```

---

## Setup Instructions

1. **Clone the Repository**

   ```powershell
   git clone <your-repo-url>
   cd Campus-Hub
   ```

2. **Create & Activate a Virtual Environment (Recommended)**

   ```powershell
   python -m venv venv
   .\venv\Scripts\activate
   ```

3. **Install Dependencies**

   ```powershell
   pip install flask flask-login flask-session flask-mail pillow
   ```

4. **Configuration**

   Open `config.py` and update the following as needed:
   - `DB_PATH` (default: lostnfound.db)
   - `MAIL_SERVER`, `MAIL_PORT`, `MAIL_USERNAME`, `MAIL_PASSWORD`, `MAIL_USE_TLS`, `MAIL_USE_SSL`
   - `SECRET_KEY` (change for production)
   - `UPLOAD_FOLDER`, `ALLOWED_EXTENSIONS`, `MAX_IMAGE_SIZE`, `QUALITY`
   - `SESSION_TYPE`, `SESSION_FILE_DIR`, `SESSION_PERMANENT`

5. **Initialize the Database**

   ```powershell
   python reset_db.py
   ```
   This script will:
   - Create all tables (`user`, `lost_found_item`, `marketplace_item`, `category`, `feedback`)
   - Insert default users (`admin/admin123`, `temp/temp123`)
   - Insert default categories for both "lost_found" and "marketplace"

6. **Run the Application**

   ```powershell
   python Main.py
   ```
   Open your browser and navigate to:
   [http://127.0.0.1:5000/](http://127.0.0.1:5000/)

---

## Configuration

All configuration values are managed in `config.py`. Below is a quick overview:

| Key                | Description                                                      |
|--------------------|------------------------------------------------------------------|
| DB_PATH            | Path to the SQLite database file (e.g., lostnfound.db).           |
| UPLOAD_FOLDER      | Directory where uploaded images will be stored (static/images).   |
| ALLOWED_EXTENSIONS | Set of allowed image extensions (e.g., {'png','jpg','jpeg','webp'}). |
| MAX_IMAGE_SIZE     | Maximum size (in pixels) for uploaded images.                    |
| QUALITY            | Compression quality for resized images (0–100).                  |
| MAIL_SERVER        | SMTP server address (e.g., smtp.gmail.com).                      |
| MAIL_PORT          | SMTP port (e.g., 587 for TLS).                                   |
| MAIL_USERNAME      | Email address used for sending verification emails.              |
| MAIL_PASSWORD      | Password or app-specific password for the mail account.          |
| MAIL_USE_TLS       | True to enable TLS encryption.                                   |
| MAIL_USE_SSL       | True to enable SSL encryption.                                   |
| SESSION_TYPE       | Session type (e.g., filesystem).                                 |
| SESSION_FILE_DIR   | Directory where session files will be stored.                    |
| SESSION_PERMANENT  | True if sessions should be permanent.                            |
| SECRET_KEY         | Flask secret key (change to a random value for production).      |

---

## Database Schema

### Tables & Fields

#### 1. user
| Column      | Type     | Description                                 |
|-------------|----------|---------------------------------------------|
| id          | INTEGER  | Primary key (auto-increment).               |
| username    | TEXT     | Unique username.                            |
| password    | TEXT     | SHA-256 hashed password.                    |
| email       | TEXT     | Unique user email.                          |
| role        | TEXT     | User role (admin, student, guest).          |
| created_at  | DATETIME | Timestamp of registration.                  |
| is_admin    | BOOLEAN  | True if user is an admin.                   |
| is_confirmed| BOOLEAN  | True if email is verified.                  |

#### 2. lost_found_item
| Column       | Type     | Description                                 |
|--------------|----------|---------------------------------------------|
| id           | INTEGER  | Primary key (auto-increment).               |
| name         | TEXT     | Name/title of the item.                     |
| description  | TEXT     | Detailed description.                       |
| category     | TEXT     | Category name (foreign key to category).    |
| status       | TEXT     | "lost" or "found".                        |
| priority     | INTEGER  | Priority level (e.g., 1=High, 2=Medium, 3=Low). |
| image_path   | TEXT     | File path of uploaded image.                |
| date         | DATE     | Date when reported.                         |
| location     | TEXT     | Location details.                           |
| contact_info | TEXT     | Contact details of reporter/finder.         |
| latitude     | REAL     | Latitude coordinate (optional).             |
| longitude    | REAL     | Longitude coordinate (optional).            |
| user_id      | INTEGER  | Foreign key to user.id.                     |
| found_by     | INTEGER  | User ID who found the item (nullable).      |
| claimed_by   | INTEGER  | User ID who claimed the item (nullable).    |

#### 3. marketplace_item
| Column       | Type     | Description                                 |
|--------------|----------|---------------------------------------------|
| id           | INTEGER  | Primary key (auto-increment).               |
| name         | TEXT     | Name/title of the item.                     |
| description  | TEXT     | Detailed description.                       |
| price        | REAL     | Price of the item.                          |
| category     | TEXT     | Category name (foreign key to category).    |
| condition    | TEXT     | Condition (e.g., "New," "Used").         |
| status       | TEXT     | "available," "sold," or "rented."        |
| image_path   | TEXT     | File path of uploaded image.                |
| date         | DATE     | Date when posted.                           |
| location     | TEXT     | Location details.                           |
| contact_info | TEXT     | Contact details of seller.                  |
| user_id      | INTEGER  | Foreign key to user.id.                     |

#### 4. category
| Column | Type    | Description                                   |
|--------|---------|-----------------------------------------------|
| id     | INTEGER | Primary key (auto-increment).                 |
| name   | TEXT    | Category name (e.g., "Electronics," "Books").|
| type   | TEXT    | Either lost_found or marketplace.             |

#### 5. feedback
| Column    | Type     | Description                                 |
|-----------|----------|---------------------------------------------|
| id        | INTEGER  | Primary key (auto-increment).               |
| user_id   | INTEGER  | Foreign key to user.id.                     |
| item_type | TEXT     | Either lost_found or marketplace.           |
| item_id   | INTEGER  | ID of the associated item in its table.     |
| comment   | TEXT     | User’s feedback or comment.                 |
| date      | DATETIME | Timestamp when comment was posted.          |

---

## Core Functionality

All database operations and core logic are implemented in `models.py`.

### User Functions
- `create_user(username, email, password)`: Register a new user (password is hashed).
- `verify_user(username, password)`: Authenticate user credentials.
- `get_user_by_id(id)`, `get_user_by_username(username)`, `get_user_by_email(email)`: Retrieve user information.
- `confirm_user(user_id)`: Mark a user’s email as verified.

### Lost & Found Functions
- `create_lost_found_item(item_data)`: Add a new lost/found item.
- `get_lost_found_items(order_by=None, filters=None)`: List items with optional filters and sorting.
- `get_lost_found_item(item_id)`: Get details for a specific lost/found item.
- `update_lost_found_item(item_id, item_data)`: Edit an existing lost/found item.
- `delete_lost_found_item(item_id)`: Remove a lost/found item.

### Marketplace Functions
- `create_marketplace_item(item_data)`: Add a new marketplace item.
- `get_marketplace_items(order_by=None, filters=None)`: List marketplace items with optional filters and sorting.
- `get_marketplace_item(item_id)`: Get details for a specific marketplace item.
- `update_marketplace_item(item_id, item_data)`: Edit an existing marketplace item.
- `delete_marketplace_item(item_id)`: Remove a marketplace item.

### Feedback Functions
- `create_feedback(user_id, item_type, item_id, comment)`: Add a comment to a lost/found or marketplace item.
- `get_feedback_for_item(item_type, item_id)`: List all comments for a specific item.

### Category Functions
- `get_categories(type=None)`: List all categories, or filter by type (lost_found or marketplace).

### Utility Functions
- `allowed_file(filename)`: Check if an uploaded file has an allowed image extension.

---

## Usage Guide

### 1. User Registration & Login
- Register a new account or use the default admin:
  - **Username:** `admin`
  - **Password:** `admin123`
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
  - **Reset Database:** Run `reset_db.py` to wipe and reinitialize tables (default users, categories, sample data).
  - **Manage Users & Items:** Edit or delete any user, lost/found item, or marketplace item.

---

## Security & Best Practices

- **Password Hashing:** SHA-256 is used to store passwords securely.
- **Session Security:** Sessions are stored on the filesystem (Flask-Session) with a secret key.
- **CSRF Protection:** Enabled via Flask-WTF for all forms.
- **Image Uploads:**
  - Restricted to allowed extensions (png, jpg, jpeg, webp).
  - Images are resized and compressed to reduce storage and load times.
- **Email Verification:** SMTP credentials are kept in environment variables or `config.py` (do not commit real credentials).
- **Configuration Management:** Use environment variables or a `.env` file (with python-dotenv) for sensitive data (e.g., `MAIL_PASSWORD`, `SECRET_KEY`).

---

## Extending the App

- **Add New Blueprints:** Create additional Flask blueprints for new features (e.g., Events, Forums).
- **Extend Models & Templates:**
  - Add new fields or tables in `models.py` and update related templates.
  - Customize HTML/CSS in `templates/` and `static/`.
- **Advanced Search & Analytics:** Integrate full-text search (e.g., Elasticsearch) or data analytics (e.g., integrate with Tableau).
- **Notifications:** Add real-time notifications using WebSockets (Flask-SocketIO).
- **REST API Endpoints:** Expose CRUD operations via a RESTful API (Flask-RESTful or Flask-API).

---

## License

Campus Hub is provided for educational purposes. If you plan to redistribute or deploy this project, please add your own license (e.g., MIT, Apache 2.0) at the root of the repository.

