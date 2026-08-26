# AI Social Media Automation Platform
## Setup Guide

This document explains how to set up the AI Social Media Automation Platform from a fresh clone.

---

# 1. Project Overview

The AI Social Media Automation Platform is a full-stack application that allows users to:

- Register and authenticate.
- Create and manage social-media posts.
- Generate captions using AI.
- Generate images using AI.
- Upload media.
- Connect Facebook Pages.
- Connect Instagram accounts.
- Publish content to connected platformss.
- Schedule posts.
- View scheduled, published, and failed posts.
- Delete posts.
- Manage connected social accounts.

## Technology Stack

| Component | Technology |
|---|---|
| Frontend | Next.js 16 |
| UI | React 19 |
| Language | TypeScript |
| State Management | Zustand |
| HTTP Client | Axios |
| Backend | FastAPI |
| Backend Language | Python 3.11 |
| ORM | SQLAlchemy 2 |
| Database | PostgreSQL |
| Migrations | Alembic |
| Authentication | JWT |
| Password Hashing | bcrypt / passlib |
| Media Storage | Cloudinary |
| AI | OpenAI + Google Gemini |
| Social Integrations | Meta/Facebook + Instagram |
| Local OAuth | ngrok |
| Production | Render |

## Tested Runtime Versions

```text
Python 3.11.8
Node.js 22.12.0
npm 11.1.0
```

---

# 2. Repository Structure

```text
social-media-ai-platform/
│
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   └── v1/
│   │   │       └── endpoints/
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
│   │
│   ├── alembic/
│   ├── tests/
│   ├── alembic.ini
│   ├── requirements.txt
│   └── ...
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
│       │
│       ├── package.json
│       ├── next.config.ts
│       └── tsconfig.json
│
└── docs/
```

Do **not** copy or commit generated/dependency directories such as:

```text
venv/
node_modules/
.next/
__pycache__/
```

These are recreated locally.

---

# 3. Required Accounts and Services

| Service | Required | Purpose |
|---|---|---|
| Git repository | Yes | Source code |
| PostgreSQL | Yes | Application database |
| OpenAI | If used | AI functionality |
| Google Gemini | If used | AI functionality |
| Cloudinary | Yes | Media storage |
| Meta Developer | Yes | Facebook/Instagram integration |
| Facebook account/Page | Yes for OAuth testing | Facebook testing |
| Instagram account | Yes for OAuth testing | Instagram testing |
| ngrok | Local OAuth only | Public HTTPS callback |
| Render | Production only | Deployment |

---

# 4. Access and Permissions

The developer responsible for setup should have:

### Repository

- Clone/read access.
- Pull access.
- Push access if development is required.
- Deployment access if the repository is connected to Render.

### PostgreSQL

The developer needs:

```text
Host
Port
Database
Username
Password
```

### External services

The responsible developer needs access to the project's:

- OpenAI/Gemini account.
- Cloudinary account.
- Meta Developer application.
- Facebook test Page/account.
- Instagram test account.
- Render account for deployment.

Do not share passwords through source code. Use environment variables.

---

# 5. Clone the Repository

From the desired parent directory:

```powershell
git clone <REPOSITORY_URL>
cd social-media-ai-platform
```

---

# 6. Backend Setup

## 6.1 Enter Backend

```powershell
cd backend
```

## 6.2 Create Virtual Environment

```powershell
python -m venv venv
```

Activate it:

```powershell
.\venv\Scripts\Activate.ps1
```

Verify:

```powershell
python --version
```

Expected:

```text
Python 3.11.x
```

## 6.3 Install Dependencies

```powershell
pip install -r requirements.txt
```

Verify:

```powershell
pip --version
```

Backend dependencies are defined in:

```text
backend/requirements.txt
```

---

# 7. Backend Environment Variables

Create:

```text
backend/app/.env
```

Use the following template:

```env
# ============================================================
# APPLICATION
# ============================================================

PROJECT_NAME=AI Social Media Automation Platform
API_V1_STR=/api/v1
ENVIRONMENT=development


# ============================================================
# DATABASE
# ============================================================

DATABASE_URL=postgresql://USERNAME:PASSWORD@HOST:PORT/DATABASE_NAME


# ============================================================
# AUTHENTICATION
# ============================================================

JWT_SECRET=GENERATE_A_LONG_RANDOM_SECRET
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30


# ============================================================
# AI
# ============================================================

OPENAI_API_KEY=
GEMINI_API_KEY=


# ============================================================
# CLOUDINARY
# ============================================================

CLOUDINARY_NAME=
CLOUDINARY_API_KEY=
CLOUDINARY_API_SECRET=


# ============================================================
# AYRSHARE
# ============================================================

AYRSHARE_API_KEY=


# ============================================================
# META / FACEBOOK
# ============================================================

META_APP_ID=
META_APP_SECRET=
META_REDIRECT_URI=


# ============================================================
# INSTAGRAM
# ============================================================

INSTAGRAM_APP_ID=
INSTAGRAM_APP_SECRET=
INSTAGRAM_REDIRECT_URI=


# ============================================================
# DEVELOPMENT TEST PUBLISHING
# ============================================================

TEST_PUBLISH_CAPTION=Unified AI Social Media Platform Test
TEST_PUBLISH_IMAGE_URL=
FACEBOOK_TEST_PAGE_ID=
```

### Security

Never commit the real `.env` file.

Generate a JWT secret with:

```powershell
python -c "import secrets; print(secrets.token_urlsafe(64))"
```

---

# 8. PostgreSQL Setup

PostgreSQL is the application's primary database.

The database stores:

- Users
- Organizations
- Organization memberships
- Facebook connections
- Instagram connections
- Posts
- Scheduling information
- Publishing information

Create a PostgreSQL database for local development.

Example:

```text
Database: platform
Host: localhost
Port: 5433
User: postgres
```

Example connection string:

```env
DATABASE_URL=postgresql://postgres:YOUR_PASSWORD@localhost:5433/platform
```

Use the actual credentials configured on the machine.

Do not use local development credentials in production.

---

# 9. Database Migrations

The project uses **Alembic** to manage database schema changes.

The migration flow is:

```text
SQLAlchemy Models
       ↓
Alembic Migration
       ↓
PostgreSQL
```

## 9.1 Check Current Migration

From `backend/`:

```powershell
alembic current
```

The current verified migration head is:

```text
62f43b53c412 (head)
```

## 9.2 Check Migration State

```powershell
alembic check
```

Expected:

```text
No new upgrade operations detected.
```

## 9.3 Apply Migrations

For a new database:

```powershell
alembic upgrade head
```

Then verify:

```powershell
alembic current
```

Expected:

```text
62f43b53c412 (head)
```

## 9.4 Creating New Migrations

Do not create a migration during normal setup.

Only create one after intentionally changing the database models:

```powershell
alembic revision --autogenerate -m "describe change"
alembic upgrade head
```

For normal setup/deployment, use:

```powershell
alembic upgrade head
```

---

# 10. Start the Backend

Ensure:

```text
PostgreSQL       ✓
.env             ✓
Virtual env      ✓
Dependencies     ✓
Migrations       ✓
```

From `backend/`:

```powershell
uvicorn main:app --reload
```

Backend:

```text
http://127.0.0.1:8000
```

Swagger API documentation:

```text
http://127.0.0.1:8000/docs
```

Health endpoint:

```text
http://127.0.0.1:8000/api/v1/health
```

Expected:

```json
{
  "status": "ok"
}
```

Always verify the health endpoint before debugging frontend or third-party integrations.

---

# 11. Frontend Setup

Open a second terminal.

```powershell
cd frontend\frontend
```

Install dependencies:

```powershell
npm install
```

## 11.1 Frontend Environment

Create:

```text
frontend/frontend/.env.local
```

Add:

```env
NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1
```

This value is used by:

```text
frontend/frontend/src/lib/api.ts
```

## 11.2 Start Frontend

```powershell
npm run dev
```

Frontend:

```text
http://localhost:3000
```

---

# 12. Local System Startup

Two terminals are required for normal local development.

### Terminal 1 — Backend

```powershell
cd backend
.\venv\Scripts\Activate.ps1
uvicorn main:app --reload
```

### Terminal 2 — Frontend

```powershell
cd frontend\frontend
npm run dev
```

Open:

```text
http://localhost:3000
```

---

# 13. Initial Verification

Before continuing to external integrations, verify:

```text
[ ] PostgreSQL is running
[ ] alembic upgrade head completed
[ ] Backend starts successfully
[ ] /api/v1/health returns 200
[ ] Frontend starts successfully
[ ] Frontend loads
[ ] Registration page loads
[ ] New user can register
[ ] User can log in
[ ] Dashboard loads
```

---

# 14. Recommended Setup Order

Follow this order:

```text
1. Clone repository
2. Install prerequisites
3. Create PostgreSQL database
4. Create backend/app/.env
5. Create Python virtual environment
6. Install backend dependencies
7. Run Alembic migrations
8. Start backend
9. Verify health endpoint
10. Create frontend/.env.local
11. Install frontend dependencies
12. Start frontend
13. Register a fresh user
14. Login and verify dashboard
15. Test database/user isolation
16. Configure AI services
17. Configure Cloudinary
18. Configure Facebook/Meta
19. Configure Instagram
20. Configure ngrok for local OAuth
21. Test publishing and scheduling
22. Deploy to production
23. Configure production OAuth
24. Run final production QA
```

For Facebook/Instagram OAuth, end-to-end testing, and deployment instructions, continue with:

**`docs/DEPLOYMENT_AND_TESTING.md`**

---

## Notes

- The backend environment file is located at `backend/app/.env`.
- The frontend environment file is located at `frontend/frontend/.env.local`.
- Do not commit either file if it contains real secrets.
- If the JWT expiration setting is changed for deployment, update `ACCESS_TOKEN_EXPIRE_MINUTES` in the environment template accordingly.
