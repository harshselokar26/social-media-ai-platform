# 🚀 AI Social Media Automation Platform

> Full-stack AI-powered social media management platform for creating, generating, scheduling, and publishing content across Facebook and Instagram.

---

## ✨ What This Project Does

The platform allows users to:

- 🔐 Register and securely authenticate
- 👤 Maintain isolated user accounts
- 🏢 Work with organizations and memberships
- 🤖 Generate captions using AI
- 🎨 Generate AI-assisted images
- ☁️ Upload and store media using Cloudinary
- 🔵 Connect Facebook Pages
- 📸 Connect Instagram accounts
- 📤 Publish posts to social platforms
- 📅 Schedule posts
- 📊 View published, scheduled, and failed posts
- 🗑️ Delete posts
- 🔒 Enforce user-level authorization and data isolation

---

# 🏗️ Architecture

```text
                         ┌──────────────────────┐
                         │       Browser        │
                         │   Next.js Frontend   │
                         └──────────┬───────────┘
                                    │
                                    │ REST API
                                    ▼
                         ┌──────────────────────┐
                         │     FastAPI API      │
                         │      Backend         │
                         └──────────┬───────────┘
                                    │
              ┌─────────────────────┼─────────────────────┐
              │                     │                     │
              ▼                     ▼                     ▼
       ┌──────────────┐      ┌──────────────┐      ┌──────────────┐
       │ PostgreSQL   │      │ AI Providers │      │  Cloudinary  │
       │              │      │              │      │              │
       │ Users        │      │ OpenAI       │      │ Media        │
       │ Posts        │      │ Gemini       │      │ Storage      │
       │ Organizations│      │              │      │              │
       └──────────────┘      └──────────────┘      └──────────────┘

                                    │
                                    ▼
                         ┌──────────────────────┐
                         │    Meta Platform     │
                         │                      │
                         │ Facebook + Instagram │
                         └──────────────────────┘
```

---

# 🛠️ Technology Stack

### Frontend

- Next.js 16
- React 19
- TypeScript
- Zustand
- Axios
- React Hook Form
- Zod
- Tailwind CSS

### Backend

- Python 3.11
- FastAPI
- SQLAlchemy 2
- Pydantic
- JWT Authentication
- bcrypt / passlib
- Alembic

### Database

- PostgreSQL

### External Services

- OpenAI
- Google Gemini
- Cloudinary
- Meta / Facebook
- Instagram
- ngrok
- Render

---

# 📁 Project Structure

```text
social-media-ai-platform/
│
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   └── v1/
│   │   │       └── endpoints/
│   │   ├── constants/
│   │   ├── core/
│   │   ├── db/
│   │   ├── exceptions/
│   │   ├── middleware/
│   │   ├── models/
│   │   ├── repositories/
│   │   ├── schemas/
│   │   ├── services/
│   │   ├── tasks/
│   │   └── utils/
│   ├── alembic/
│   ├── tests/
│   ├── requirements.txt
│   ├── alembic.ini
│   └── main.py
│
├── frontend/
│   └── frontend/
│       ├── public/
│       ├── src/
│       │   ├── app/
│       │   │   ├── accounts/
│       │   │   ├── calendar/
│       │   │   ├── create-post/
│       │   │   ├── dashboard/
│       │   │   ├── login/
│       │   │   └── posts/
│       │   └── lib/
│       │       ├── api.ts
│       │       └── auth.ts
│       ├── package.json
│       ├── next.config.ts
│       └── tsconfig.json
│
├── docs/
│   ├── SETUP.md
│   └── DEPLOYMENT_AND_TESTING.md
│
└── README.md
```

---

# ⚡ Quick Start

> For complete setup instructions, see [`docs/SETUP.md`](docs/SETUP.md).

## 1. Clone

```bash
git clone <REPOSITORY_URL>
cd social-media-ai-platform
```

## 2. Backend

```powershell
cd backend
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Create:

```text
backend/app/.env
```

Configure the required environment variables.

## 3. Database

Create a PostgreSQL database and configure:

```env
DATABASE_URL=postgresql://USERNAME:PASSWORD@HOST:PORT/DATABASE_NAME
```

Then:

```powershell
alembic upgrade head
alembic current
```

## 4. Start Backend

```powershell
uvicorn main:app --reload
```

Backend:

```text
http://127.0.0.1:8000
```

Swagger:

```text
http://127.0.0.1:8000/docs
```

Health:

```text
http://127.0.0.1:8000/api/v1/health
```

Expected:

```json
{
  "status": "ok"
}
```

## 5. Frontend

Open another terminal:

```powershell
cd frontend\frontend
npm install
```

Create:

```text
frontend/frontend/.env.local
```

Add:

```env
NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1
```

Start:

```powershell
npm run dev
```

Frontend:

```text
http://localhost:3000
```

---

# 🔑 Required Services

## Core Application

- Git repository
- PostgreSQL
- Render for production deployment

## AI

- OpenAI API access
- Google Gemini API access

## Media

- Cloudinary account

## Social Integrations

- Meta Developer application
- Facebook account
- Facebook Page
- Eligible Instagram Professional/Business/Creator account

## Local OAuth

- ngrok account

---

# 🔐 Environment Variables

Backend environment file:

```text
backend/app/.env
```

Template:

```env
PROJECT_NAME=AI Social Media Automation Platform
API_V1_STR=/api/v1
ENVIRONMENT=development

DATABASE_URL=postgresql://USERNAME:PASSWORD@HOST:PORT/DATABASE_NAME

JWT_SECRET=GENERATE_A_LONG_RANDOM_SECRET
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=

OPENAI_API_KEY=
GEMINI_API_KEY=

CLOUDINARY_NAME=
CLOUDINARY_API_KEY=
CLOUDINARY_API_SECRET=

AYRSHARE_API_KEY=

META_APP_ID=
META_APP_SECRET=
META_REDIRECT_URI=

INSTAGRAM_APP_ID=
INSTAGRAM_APP_SECRET=
INSTAGRAM_REDIRECT_URI=

TEST_PUBLISH_CAPTION=Unified AI Social Media Platform Test
TEST_PUBLISH_IMAGE_URL=
FACEBOOK_TEST_PAGE_ID=
```

Frontend environment file:

```text
frontend/frontend/.env.local
```

```env
NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1
```

> Never commit real secrets, API keys, passwords, OAuth secrets, database credentials, or access tokens.

Generate a JWT secret with:

```powershell
python -c "import secrets; print(secrets.token_urlsafe(64))"
```

---

# 🔄 Database Migrations

The project uses Alembic.

Check migration:

```powershell
alembic current
```

Check schema consistency:

```powershell
alembic check
```

Apply migrations:

```powershell
alembic upgrade head
```

Create a migration only after intentionally changing SQLAlchemy models:

```powershell
alembic revision --autogenerate -m "describe change"
alembic upgrade head
```

For normal setup and deployment:

```powershell
alembic upgrade head
```

---

# 🔌 API Overview

The backend API is versioned under:

```text
/api/v1
```

Main areas include:

```text
Authentication
    POST   /auth/register
    POST   /auth/login
    GET    /auth/me

Health
    GET    /health

Meta / Facebook OAuth
    GET    /auth/meta
    GET    /auth/meta/callback
    GET    /auth/meta/pages

Instagram
    GET    /auth/instagram
    GET    /auth/instagram/callback
    GET    /auth/instagram/account
    GET    /auth/instagram/media
    POST   /auth/instagram/publish

Media
    POST   /media/upload

Posts
    POST   /posts/publish
    POST   /posts/schedule
    POST   /posts/test-publish
    GET    /posts
    GET    /posts/{post_id}
    DELETE /posts/{post_id}

Facebook Page Operations
    GET    /facebook/pages/{page_id}
    GET    /facebook/pages/{page_id}/posts
    GET    /facebook/posts/{post_id}/comments
    GET    /facebook/pages/{page_id}/insights
    POST   /facebook/pages/{page_id}/posts
    POST   /facebook/pages/{page_id}/image-posts
    DELETE /facebook/posts/{post_id}

AI
    AI generation endpoints
```

For the authoritative API definition, use:

```text
http://127.0.0.1:8000/docs
```

---

# 🔒 Authentication

Authentication uses JWT.

Typical flow:

```text
Register
   ↓
Login
   ↓
JWT Access Token
   ↓
Authenticated API Request
   ↓
FastAPI validates token
   ↓
Current User
```

Protected requests use:

```text
Authorization: Bearer <token>
```

The frontend maintains authentication state using Zustand persistence.

---

# 👥 User Isolation

The application must enforce user-level data isolation.

Example:

```text
User A
 ├── Posts
 ├── Organization
 ├── Facebook connection
 └── Instagram connection

User B
 ├── Posts
 ├── Organization
 ├── Facebook connection
 └── Instagram connection
```

User B must never be able to access User A's:

- Posts
- Social connections
- Organization data
- Publishing records

This must be verified during QA.

---

# 📱 Social Publishing Flow

```text
User
 ↓
Create Post
 ↓
Upload Media
 ↓
Cloudinary
 ↓
Select Platform
 ↓
Facebook / Instagram OAuth
 ↓
Connected Account
 ↓
Publish
 ↓
Social Platform
 ↓
Store Publishing Result
```

---

# 🌐 Local OAuth with ngrok

Facebook and Instagram OAuth callbacks require a publicly accessible HTTPS URL during local development.

Start the backend:

```powershell
uvicorn main:app --reload
```

In another terminal:

```powershell
ngrok http 8000
```

Use the HTTPS forwarding URL in the appropriate Meta/Instagram OAuth configuration.

Verify the public backend:

```powershell
curl.exe -i https://YOUR-NGROK-DOMAIN/api/v1/health
```

Expected:

```json
{
  "status": "ok"
}
```

> ngrok is for local OAuth development/testing. It is not the production deployment architecture.

---

# 🧪 Testing Workflow

Follow this order:

```text
1. Backend health
       ↓
2. Frontend startup
       ↓
3. Registration
       ↓
4. Login
       ↓
5. User isolation
       ↓
6. AI generation
       ↓
7. Media upload
       ↓
8. Facebook OAuth
       ↓
9. Facebook publishing
       ↓
10. Instagram OAuth
       ↓
11. Instagram publishing
       ↓
12. Combined publishing
       ↓
13. Scheduling
       ↓
14. Post deletion
       ↓
15. Production deployment
       ↓
16. Production E2E test
```

---

# ✅ Local QA Checklist

```text
[ ] PostgreSQL running
[ ] Environment variables configured
[ ] Alembic migrations applied
[ ] Backend starts
[ ] /api/v1/health returns 200
[ ] Swagger loads
[ ] Frontend starts
[ ] Registration works
[ ] Login works
[ ] Dashboard loads
[ ] User A created
[ ] User B created
[ ] User isolation verified
[ ] AI generation works
[ ] Image upload works
[ ] Facebook OAuth works
[ ] Facebook publishing works
[ ] Instagram OAuth works
[ ] Instagram publishing works
[ ] Combined publishing works
[ ] Scheduling works
[ ] Calendar works
[ ] Post deletion works
```

---

# 🚀 Production Deployment

Production deployment uses Render.

Expected architecture:

```text
                    ┌─────────────────┐
                    │     Render      │
                    │    Frontend     │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │     Render      │
                    │     Backend     │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │    PostgreSQL   │
                    │     Render      │
                    └─────────────────┘
```

Production requires:

```text
[ ] Production PostgreSQL
[ ] Production DATABASE_URL
[ ] Production JWT_SECRET
[ ] Production AI credentials
[ ] Production Cloudinary credentials
[ ] Production Meta credentials
[ ] Production Instagram credentials
[ ] Production CORS configuration
[ ] Production frontend URL
[ ] Production backend URL
[ ] Production OAuth callbacks
[ ] Production E2E testing
```

Complete deployment instructions:

[`docs/DEPLOYMENT_AND_TESTING.md`](docs/DEPLOYMENT_AND_TESTING.md)

---

# 📚 Documentation

## Setup

[`docs/SETUP.md`](docs/SETUP.md)

Fresh machine → local working application.

## Deployment & Testing

[`docs/DEPLOYMENT_AND_TESTING.md`](docs/DEPLOYMENT_AND_TESTING.md)

OAuth → E2E testing → deployment → production QA.

### Recommended reading order

```text
README.md
    ↓
docs/SETUP.md
    ↓
Run application locally
    ↓
docs/DEPLOYMENT_AND_TESTING.md
    ↓
OAuth + E2E testing
    ↓
Render deployment
    ↓
Production QA
```

---

# 🐛 Troubleshooting

## Backend does not start

Check:

```powershell
python --version
pip --version
```

Then:

```powershell
alembic current
```

Verify `backend/app/.env`.

---

## Database connection fails

Check:

```env
DATABASE_URL=postgresql://USERNAME:PASSWORD@HOST:PORT/DATABASE_NAME
```

Confirm PostgreSQL is running and the host, port, database, username, and password are correct.

---

## Frontend cannot reach backend

Check:

```env
NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1
```

Then verify:

```text
http://localhost:8000/api/v1/health
```

---

## OAuth fails

Check:

```text
[ ] Meta App ID
[ ] Meta App Secret
[ ] Redirect URI
[ ] ngrok HTTPS URL
[ ] Meta application configuration
[ ] Facebook permissions
[ ] Instagram permissions
[ ] Correct test account
```

---

## Publishing fails

Check in this order:

```text
Browser Network Response
        ↓
Backend Logs
        ↓
Database Record
        ↓
OAuth Connection
        ↓
Social Platform Response
```

Do not immediately modify code before checking the actual HTTP response and backend logs.

---

# 🔐 Security Rules

Never commit:

```text
.env
.env.local
API keys
API secrets
JWT secrets
OAuth secrets
Database passwords
Access tokens
Private keys
```

Never use production credentials for local testing.

Never use the original developer's social accounts for final isolation testing.

Always perform final E2E testing with a fresh user.

---

# 📌 Common Development Commands

## Backend

```powershell
cd backend
.\venv\Scripts\Activate.ps1
uvicorn main:app --reload
```

## Frontend

```powershell
cd frontend\frontend
npm run dev
```

## Database

```powershell
cd backend

alembic current
alembic check
alembic upgrade head
```

## Production Frontend Build

```powershell
npm run build
```

## ngrok

```powershell
ngrok http 8000
```

---

# 🎯 Deployment Readiness

The project should be considered ready for deployment only after:

```text
                 ┌─────────────────────┐
                 │     CODE READY      │
                 └──────────┬──────────┘
                            ↓
                 ┌─────────────────────┐
                 │   DATABASE READY    │
                 └──────────┬──────────┘
                            ↓
                 ┌─────────────────────┐
                 │    AUTH READY       │
                 └──────────┬──────────┘
                            ↓
                 ┌─────────────────────┐
                 │ AI + MEDIA READY    │
                 └──────────┬──────────┘
                            ↓
                 ┌─────────────────────┐
                 │     META READY      │
                 └──────────┬──────────┘
                            ↓
                 ┌─────────────────────┐
                 │  INSTAGRAM READY    │
                 └──────────┬──────────┘
                            ↓
                 ┌─────────────────────┐
                 │   E2E TEST PASSED   │
                 └──────────┬──────────┘
                            ↓
                 ┌─────────────────────┐
                 │ PRODUCTION DEPLOYED │
                 └──────────┬──────────┘
                            ↓
                 ┌─────────────────────┐
                 │   FINAL QA PASSED   │
                 └─────────────────────┘
```

---

# 👨‍💻 Handover Principle

A new developer should be able to:

```text
Clone repository
      ↓
Read README
      ↓
Follow SETUP.md
      ↓
Start local application
      ↓
Follow DEPLOYMENT_AND_TESTING.md
      ↓
Configure integrations
      ↓
Run E2E tests
      ↓
Deploy
      ↓
Verify production
```

without requiring the original developer to manually explain every step.

---

# 📄 Documentation Entry Points

**Setup**

[`docs/SETUP.md`](docs/SETUP.md)

**Deployment & Testing**

[`docs/DEPLOYMENT_AND_TESTING.md`](docs/DEPLOYMENT_AND_TESTING.md)

---

## 🏁 Final Note

This README is the **entry point** to the project.

The detailed operational instructions remain in the two documentation files:

```text
README.md
    ↓
SETUP.md
    ↓
DEPLOYMENT_AND_TESTING.md
```

Keep the README focused on understanding, navigation, quick start, and project architecture. Keep detailed setup, OAuth, testing, and deployment procedures in the documentation files.
