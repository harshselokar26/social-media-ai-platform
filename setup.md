# Setup Guide

## 1. Prerequisites

Before installing the application, make sure the following software is
installed.

### Required

- Git
- Python 3.11+
- PostgreSQL
- A Meta Developer Account
- A Facebook account with administrator access to the Facebook Page

### Recommended

- Visual Studio Code
- Postman
- Chrome / Chromium-based browser

---

# 2. Clone the Repository

Clone the project repository:

```bash
git clone https://github.com/harshselokar26/social-media-ai-platform.git 

Move into the project:

cd social-media-ai-platform

Move into the backend:

cd backend
----------------------------------------------------------------------------------------------------------------------------
# 3 Create a virtual environment:

python -m venv venv
Windows
venv\Scripts\activate
macOS / Linux
source venv/bin/activate

After activation, the terminal should show:

(venv)
-------------------------------------------------------------------------------------------------------------------------------

4. Install Dependencies

Install the backend dependencies:

pip install -r requirements.txt
--------------------------------------------------------------------------------------------------------------------------------
5. Configure PostgreSQL

Create a PostgreSQL database for the application.

Example:

Database:
social_media_platform

Create a database user and password with permission to access the database.

The application requires the PostgreSQL connection details in the environment
configuration.
--------------------------------------------------------------------------------------------------------------------------------
6. Configure Environment Variables

Create a .env file inside the backend directory.

Example:

PROJECT_NAME=

API_V1_STR=

DATABASE_URL=

JWT_SECRET=

JWT_ALGORITHM=

ACCESS_TOKEN_EXPIRE_MINUTES=

OPENAI_API_KEY=

CLOUDINARY_NAME=
CLOUDINARY_API_KEY=
CLOUDINARY_API_SECRET=

AYRSHARE_API_KEY=

META_APP_ID=
META_APP_SECRET=
META_REDIRECT_URI=
META_REDIRECT_URI=




ENVIRONMENT=

FACEBOOK_TEST_PAGE_ID=
-------------------------------------------------------------------------------------------------------------------------------
7. Database Setup

Run the project's database migration/setup process.

The exact command depends on the migration configuration used by the project.

After setup, verify that the required tables exist.

Important tables currently used by the Meta integration include:

meta_connections
facebook_pages

The Facebook Page record stores information required by the backend to make
Page-level API requests.

-------------------------------------------------------------------------------------------------------------------------------
8. Start the Backend

From the backend directory:

uvicorn app.main:app --reload

The backend should start at:

http://127.0.0.1:8000
-------------------------------------------------------------------------------------------------------------------------------

9. Open API Documentation

FastAPI automatically provides Swagger documentation.

Open:

http://127.0.0.1:8000/docs

The Swagger interface can be used to test the API without requiring Postman.

-------------------------------------------------------------------------------------------------------------------------------
10. Authentication

The application uses authenticated API requests.

A user must first authenticate with the application and obtain a JWT token.

Swagger can then use the JWT token for protected endpoints.

The Meta integration is separate from application authentication.

There are two different authentication layers:

Application authentication
Meta platform authorization
-------------------------------------------------------------------------------------------------------------------------------
11. Connect Meta

The application uses Meta OAuth to allow a user to authorize access to
their Facebook Page.

The general flow is:

User
↓
Application
↓
Meta OAuth
↓
User grants permissions
↓
Meta returns authorization information
↓
Application obtains Meta access token
↓
Application retrieves available Pages
↓
Page access token is obtained
↓
Page information is stored
↓
Application can access the Page through the Meta Graph API

See:

META_SETUP.md

for the Meta Developer configuration.
-------------------------------------------------------------------------------------------------------------------------------
12. Verify Facebook Connection

After connecting a Facebook Page, verify that the Page is stored correctly.

The system should have a record containing:

Page ID
Page Name
Page Access Token
Meta Connection
Active Status
-------------------------------------------------------------------------------------------------------------------------------
13. Test Facebook API

Open:

http://127.0.0.1:8000/docs

Find:

Facebook

Available endpoints currently include:

GET    /api/v1/facebook/pages/{page_id}
GET    /api/v1/facebook/pages/{page_id}/posts
GET    /api/v1/facebook/posts/{post_id}/comments
GET    /api/v1/facebook/pages/{page_id}/insights
POST   /api/v1/facebook/pages/{page_id}/posts
DELETE /api/v1/facebook/posts/{post_id}

Test them in this order:

Get Page
Get Posts
Create test post
Get Posts again
Copy the created post ID
Delete the test post
Verify deletion
14. Production Configuration

For production deployment:

Use HTTPS
Use production PostgreSQL
Store secrets in a secure secret manager
Never expose Meta App Secret
Never expose Page Access Tokens
Disable development/debug configuration
Configure production OAuth redirect URLs
Configure appropriate Meta application permissions
Enable proper application logging
15. Security

Never commit the following to Git:

.env
Meta App Secret
Meta Access Token
Page Access Token
JWT Secret
Database Password

--------------------------------------------------------------------------------------------------------------------------------


---

# 3. `META_SETUP.md`


```md
# Meta Developer Setup

## Overview

The application integrates with Meta through the official Meta Graph API.

A Meta Developer application is required before the platform can connect to
Facebook Pages.

The Meta application acts as the bridge between our application and the
customer's Facebook Page.

---

# 1. Requirements

Before configuring Meta, the customer needs:

- A Facebook account
- A Facebook Page
- Appropriate administrative access to the Page
- A Meta Developer account
- A Meta application
- An OAuth redirect URL provided by the application
- Required permissions approved/granted for the Meta application

---

# 2. Create Meta Developer Application

Create a Meta Developer application from the Meta developer platform.

The application will provide:

```text
App ID
App Secret

These values are used by the backend during the Meta authentication process.