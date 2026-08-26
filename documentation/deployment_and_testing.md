# AI Social Media Automation Platform

# Deployment & End-to-End Testing Guide

This is the second and final operational document.

Use it after completing `SETUP.md`.

The goal is to take the project from:

```text

Local setup

   ↓

Third-party accounts

   ↓

OAuth

   ↓

End-to-end testing

   ↓

Production deployment

   ↓

Final verification

```

---

# 1. Required Accounts and Permissions

The following access is required for the person responsible for setup, testing, and deployment.

> **IMPORTANT:** Complete this checklist before starting end-to-end testing or production deployment.

---

## 1.1 GitHub / Git Repository

**Required:** Yes

The developer must have:

- [ ] Repository URL
- [ ] Permission to clone the repository
- [ ] Read access to the complete repository
- [ ] Permission to pull the latest code
- [ ] Push access if development changes are required
- [ ] Permission to connect the repository to Render if responsible for deployment

**Used for:**

```text
Source code
Version control
Pulling updates
Pushing changes
Render deployment
```

---

## 1.2 PostgreSQL

**Required:** Yes

The developer must have access to a PostgreSQL database.

Required information:

```text
Host:
Port:
Database:
Username:
Password:
```

The developer must have:

- [ ] Permission to connect to the database
- [ ] Permission to use/create the project database
- [ ] Permission to run database migrations
- [ ] Permission to read/write application data

**Used for:**

```text
Users
Organizations
Organization memberships
Social connections
Posts
Scheduling
Publishing information
```

---

## 1.3 OpenAI

**Required:** Only if OpenAI features are enabled.

The developer must have:

- [ ] OpenAI account/project accesss
- [ ] Permission to create or use an API key
- [ ] API key available for backend configuration

Environment variable:

```env
OPENAI_API_KEY=
```

**Used for:**

```text
AI functionality
```

---

## 1.4 Google AI Studio / Gemini

**Required:** Only if Gemini features are enabled.

The developer must have:

- [ ] Google AI Studio/Gemini access
- [ ] Access to the required API/project configuration
- [ ] Permission to create or use an API key
- [ ] API key available for backend configuration

Environment variable:

```env
GEMINI_API_KEY=
```

**Used for:**

```text
AI functionality
```

---

## 1.5 Cloudinary

**Required:** Yes

The developer must have access to the project's Cloudinary account.

Required information:

```text
Cloud Name:
API Key:
API Secret:
```

The developer must have:

- [ ] Cloudinary account access
- [ ] Cloud Name
- [ ] API Key
- [ ] API Secret
- [ ] Permission to upload media
- [ ] Permission to use the project's media storage

Environment variables:

```env
CLOUDINARY_NAME=
CLOUDINARY_API_KEY=
CLOUDINARY_API_SECRET=
```

**Used for:**

```text
Image upload
Media storage
Public image URLs
```

---

## 1.6 Meta Developer Application

**Required:** Yes for Facebook/Instagram integration.

The developer must have access to the project's Meta Developer application.

Required:

- [ ] Meta Developer account
- [ ] Access to the correct Meta application
- [ ] Permission to view application settings
- [ ] Permission to modify application settings
- [ ] Permission to configure OAuth
- [ ] Permission to configure OAuth redirect URLs
- [ ] Permission to configure required products/permissions
- [ ] Access to App ID
- [ ] Access to App Secret
- [ ] Permission to manage application testers/users where required

Environment variables:

```env
META_APP_ID=
META_APP_SECRET=
META_REDIRECT_URI=
```

**Used for:**

```text
Facebook OAuth
Instagram OAuth
Facebook Page access
Instagram account access
Social publishing
```

> **Security:** The Meta App Secret must never be committed to Git or exposed in frontend code.

---

## 1.7 Facebook Account and Page

**Required:** Yes for Facebook testing.

The testing account must have access to the Facebook Page used for testing.

Required:

- [ ] Facebook account available
- [ ] Developer/tester can log in to the account
- [ ] Facebook Page available
- [ ] Developer/tester has the required Page permissions
- [ ] Page can be accessed through the Meta application
- [ ] Page can be selected by the application
- [ ] Facebook publishing can be tested

Development test variable:

```env
FACEBOOK_TEST_PAGE_ID=
```

**Used for:**

```text
Facebook OAuth
Facebook Page connection
Facebook publishing
Facebook publishing verification
```

> **Important:** Do not use another person's Facebook Page or account without explicit authorization.

---

## 1.8 Instagram Account

**Required:** Yes for Instagram testing.

The Instagram account must satisfy the requirements of the Instagram API flow configured for the project.

Required:

- [ ] Instagram account available
- [ ] Account is eligible for the configured Instagram API flow
- [ ] Instagram account is connected to the required Meta/Facebook setup
- [ ] Developer/tester has access to the account
- [ ] Required Instagram permissions are configured
- [ ] Instagram OAuth can be tested
- [ ] Instagram publishing can be tested

Environment variables:

```env
INSTAGRAM_APP_ID=
INSTAGRAM_APP_SECRET=
INSTAGRAM_REDIRECT_URI=
```

**Used for:**

```text
Instagram OAuth
Instagram account connection
Instagram media access
Instagram publishing
```

---

## 1.9 ngrok

**Required:** Only for local Facebook/Instagram OAuth testing.

The developer must have:

- [ ] ngrok account
- [ ] ngrok installed
- [ ] ngrok authentication token configured
- [ ] Permission to create HTTPS tunnels
- [ ] Ability to expose local port `8000`

Example:

```powershell
ngrok http 8000
```

The resulting public HTTPS URL is used for local OAuth callbacks.

Example:

```text
https://YOUR-NGROK-DOMAIN
```

**Used for:**

```text
Meta
  ↓
Public HTTPS URL
  ↓
ngrok
  ↓
Local FastAPI
  ↓
localhost:8000
```

> **Important:** ngrok is for local development/testing. Do not use an ngrok URL for production OAuth.

---

## 1.10 Render

**Required:** Yes for production deployment.

The deployment developer must have:

- [ ] Render account
- [ ] Access to the correct Render workspace
- [ ] Permission to create services
- [ ] Permission to manage services
- [ ] Permission to connect the Git repository
- [ ] Permission to configure environment variables
- [ ] Permission to deploy/redeploy services
- [ ] Permission to view deployment logs
- [ ] Access to the production PostgreSQL database

**Used for:**

```text
Production backend
Production frontend
Production PostgreSQL
Environment variables
Deployment
Application logs
```

---

## 1.11 Credential Security

Never commit the following to Git:

- [ ] Passwords
- [ ] API keys
- [ ] API secrets
- [ ] JWT secrets
- [ ] OAuth client secrets
- [ ] Database passwords
- [ ] Access tokens
- [ ] Refresh tokens
- [ ] ngrok authentication tokens
- [ ] Private keys

Local secrets must be stored in:

```text
backend/app/.env
frontend/frontend/.env.local
```

Production secrets must be configured through the production hosting provider.

---

## 1.12 Access Verification Before Testing

Before starting end-to-end testing, confirm:

```text
[ ] Git repository access
[ ] PostgreSQL access
[ ] Backend environment configured
[ ] Frontend environment configured
[ ] OpenAI configured if required
[ ] Gemini configured if required
[ ] Cloudinary configured
[ ] Meta Developer access
[ ] Facebook test account/Page
[ ] Instagram test account
[ ] ngrok configured for local OAuth
[ ] Render access if deploying
```

> **STOP CONDITION:** If a required account, permission, credential, or service is missing, stop at that step and obtain the required access before continuing.

---

## 1.13 Important Ownership Rule

Use **project-owned accounts and resources** wherever possible.

Do not depend on:

```text
A developer's personal Facebook Page
A developer's personal Instagram account
A developer's personal API key
A developer's personal Cloudinary account
A developer's personal database
A developer's personal Render workspace
A developer's personal ngrok credentials
```

The project should remain operational even when the original developer leaves the project.

---

# 2. OpenAI / Gemini

Only configure the providers actually used by the application.

Backend environment:

```env

OPENAI_API_KEY=

GEMINI_API_KEY=

```

Required:

```text

[ ] API account created

[ ] API key generated

[ ] Key added to backend/app/.env

[ ] AI feature tested from the frontend

```

Do not expose these keys through frontend code.

---

# 3. Cloudinary Setup

Cloudinary is used for media/image storage.

Create or obtain:

```text

CLOUDINARY_NAME

CLOUDINARY_API_KEY

CLOUDINARY_API_SECRET

```

Add them to:

```text

backend/app/.env

```

```env

CLOUDINARY_NAME=

CLOUDINARY_API_KEY=

CLOUDINARY_API_SECRET=

```

Verify:

```text

[ ] Cloudinary account accessible

[ ] Credentials added

[ ] Image upload works

[ ] Uploaded image receives a valid URL

[ ] Post creation can use the uploaded image URL

```

---

# 4. Meta / Facebook Setup

Facebook and Instagram OAuth are handled through the Meta developer application.

## 4.1 Meta Developer Access

The developer needs permission to manage the Meta application.

At minimum, the person responsible for configuration should be able to:

- Open the Meta developer application.

- View/edit application settings.

- Configure Facebook Login/OAuth.

- Configure valid OAuth redirect URLs.

- Manage application users/testers where required.

- View application credentials.

- Configure products and permissions.

- Test the application with the designated Facebook account/Page.

Keep the App ID and App Secret private.

Backend variables:

```env

META_APP_ID=

META_APP_SECRET=

META_REDIRECT_URI=

```

---

# 5. Facebook Account / Page Requirements

For Facebook publishing tests, the testing Facebook account must have access to the Page being used.

Required:

```text

[ ] Facebook account available

[ ] Facebook Page available

[ ] Tester has sufficient Page permissions

[ ] Meta app can authenticate the tester

[ ] Page can be selected by the application

[ ] Page publishing can be tested

```

The Page ID used for development test publishing is:

```env

FACEBOOK_TEST_PAGE_ID=

```

Do not use another user's Page without authorization.

---

# 6. Meta Permissions

The exact permissions available to the application depend on the Meta products, login flow, app mode, and account type.

For a Page publishing flow, the application commonly requires permissions corresponding to:

```text

pages_show_list

pages_read_engagement

pages_manage_posts

```

Depending on the implementation and Meta API version, additional permissions may be required.

For Instagram publishing, permissions may include:

```text

instagram_basic

instagram_content_publish

```

and Facebook/Page-related permissions required to discover and access the connected Instagram professional account.

Important:

**\*\*Do not blindly add every permission.\*\***

Only request permissions that are actually required by the routes implemented in this project and approved/configured in the Meta application.

If Meta rejects a permission:

1. Check the Meta application's configured products.

2. Check the OAuth scopes requested by the backend.

3. Check whether the test user has the required Page/account role.

4. Check whether the Instagram account is eligible for the selected API flow.

5. Check the Meta API response in the backend logs.

---

# 7. Instagram Requirements

The Instagram account used for publishing must satisfy the requirements of the Meta API flow configured by the project.

Before testing:

```text

[ ] Instagram account is available

[ ] Account is eligible for the selected Instagram API flow

[ ] Instagram account is connected to the required Meta/Facebook setup

[ ] Tester has access to the connected account/Page

[ ] Instagram app credentials are configured

```

Backend variables:

```env

INSTAGRAM_APP_ID=

INSTAGRAM_APP_SECRET=

INSTAGRAM_REDIRECT_URI=

```

The project also provides endpoints for:

```text

Instagram OAuth

Instagram account lookup

Instagram media lookup

Instagram publishing

```

---

# 8. OAuth Redirect URLs

OAuth redirect URLs must exactly match the URLs configured in the Meta application.

For local development, the callback cannot normally use:

```text

http://localhost

```

when the provider requires a public HTTPS callback.

Use ngrok.

Example:

```text

https://YOUR-NGROK-DOMAIN/\<YOUR-CALLBACK-PATH>

```

The exact callback path must match the route implemented by the backend.

Do not guess the callback path.

Check the backend OAuth routes before configuring Meta.

---

# 9. ngrok Local OAuth

ngrok exposes the local backend through a public HTTPS URL.

Purpose:

```text

Meta

  ↓

Public HTTPS ngrok URL

  ↓

Local FastAPI backend

  ↓

localhost:8000

```

## 9.1 Install and Authenticate ngrok

Create an ngrok account and configure the ngrok authentication token.

The ngrok account/token is required for the local tunnel.

## 9.2 Start Backend First

Terminal 1:

```powershell

cd backend

.\venv\Scripts\Activate.ps1

uvicorn main:app --reload

```

Verify:

```powershell

curl.exe http://127.0.0.1:8000/api/v1/health

```

Expected:

```json

{"status":"ok"}

```

## 9.3 Start ngrok

Terminal 3:

```powershell

ngrok http 8000

```

ngrok will display a forwarding URL similar to:

```text

https://example.ngrok-free.dev

```

ngrok's HTTP tunnel forwards traffic to the local service on port 8000. citeturn1search0

## 9.4 Verify the Tunnel

```powershell

curl.exe -i https://YOUR-NGROK-DOMAIN/api/v1/health

```

Expected:

```text

HTTP/1.1 200 OK

```

and:

```json

{"status":"ok"}

```

If this works, the public tunnel can reach FastAPI.

## 9.5 Configure OAuth

Set the Meta redirect URI to the exact public callback URL.

Update:

```env

META_REDIRECT_URI=

INSTAGRAM_REDIRECT_URI=

```

Restart the backend after changing environment variables.

---

# 10. Local End-to-End Testing

At this stage you should have:

```text

Terminal 1

Backend

http://127.0.0.1:8000

Terminal 2

Frontend

http://localhost:3000

Terminal 3

ngrok

https://YOUR-NGROK-DOMAIN

```

Do not close any of these terminals while testing local OAuth.

---

# 11. Fresh User Registration Test

Start with a completely new user.

Open:

```text

http://localhost:3000

```

Test:

```text

[ ] Registration page opens

[ ] New organization can be created

[ ] New user can be registered

[ ] Duplicate email is rejected

[ ] Invalid email is rejected

[ ] Weak/short password is rejected

[ ] User can log in

[ ] Dashboard opens

[ ] User receives a valid authenticated session

```

Record the test account separately.

Never document real passwords.

---

# 12. Authentication Test

Test:

```text

[ ] Valid login succeeds

[ ] Invalid password fails

[ ] Invalid email fails

[ ] Protected page cannot be accessed without authentication

[ ] /auth/me returns the logged-in user

[ ] Logout/clear authentication works

[ ] Expired/invalid token is rejected

```

The application uses JWT authentication.

The frontend stores authentication state using Zustand persistence.

---

# 13. User Isolation Test

This is a mandatory production-readiness test.

Create:

```text

User A

User B

```

Use different email addresses.

## User A

Create posts and connect the social accounts belonging to User A.

Verify User A can see:

```text

[ ] Own posts

[ ] Own connected accounts

[ ] Own organization data

```

## User B

Log in as User B.

Verify:

```text

[ ] User B cannot see User A's posts

[ ] User B cannot delete User A's posts

[ ] User B cannot access User A's post by ID

[ ] User B cannot use User A's social connection

[ ] User B sees only their own data

```

This test is critical because social publishing uses user-specific credentials.

---

# 14. Database Isolation Test

After registering two users, verify the PostgreSQL database contains separate records.

Important relationships include:

```text

users

organizations

organization_members

posts

meta_connections

facebook_pages

instagram_accounts

```

The application must always filter user-owned data by the authenticated user.

Example:

```text

User A → Post A

User B → Post B

User A requests Post B

        ↓

404 / access denied

```

Never solve isolation by hiding data only in the frontend.

Authorization must be enforced by the backend.

---

# 15. AI Feature Test

Test every AI feature exposed by the frontend.

```text

[ ] Caption generation works

[ ] Image generation works, if enabled

[ ] Invalid AI request returns a controlled error

[ ] API key failure produces a useful backend error

[ ] Frontend displays the error correctly

```

Check backend logs if an AI request fails.

---

# 16. Media Upload Test

From the create-post flow:

```text

[ ] Select image

[ ] Upload image

[ ] Cloudinary upload succeeds

[ ] Returned URL is valid

[ ] Image preview works

[ ] Post can use the returned image URL

```

If upload fails, check:

```text

CLOUDINARY_NAME

CLOUDINARY_API_KEY

CLOUDINARY_API_SECRET

```

---

# 17. Facebook Connection Test

Use the fresh test user.

From the Accounts page:

```text

[ ] Connect Facebook

[ ] OAuth page opens

[ ] Correct Meta application is displayed

[ ] Correct Facebook account is selected

[ ] Required permissions are accepted

[ ] OAuth callback succeeds

[ ] Facebook Page is returned

[ ] Connected Page is shown in the frontend

```

Do not test with the original developer account only.

The purpose is to prove that a completely new authorized user can connect their own account.

---

# 18. Instagram Connection Test

Using the fresh test user:

```text

[ ] Connect Instagram

[ ] OAuth page opens

[ ] Correct Meta application is displayed

[ ] Correct Instagram account is selected

[ ] Required permissions are accepted

[ ] OAuth callback succeeds

[ ] Instagram account is returned

[ ] Connected Instagram account is displayed

```

---

# 19. Publishing Test

Test Facebook and Instagram separately first.

## Facebook

```text

[ ] Create post

[ ] Select Facebook

[ ] Publish

[ ] Backend returns success

[ ] Post ID is stored

[ ] Post appears on the correct Page

```

## Instagram

```text

[ ] Create post

[ ] Select Instagram

[ ] Publish

[ ] Backend returns success

[ ] Instagram media ID is stored

[ ] Content appears on the correct Instagram account

```

## Combined

Finally:

```text

[ ] Select Facebook + Instagram

[ ] Publish

[ ] Both platforms succeed

[ ] Correct IDs are stored

[ ] No account belonging to another user is used

```

---

# 20. Scheduling Test

Create a post with a future time.

Verify:

```text

[ ] Post can be scheduled

[ ] scheduled_at is stored correctly

[ ] Post appears in Calendar

[ ] Scheduler processes the post

[ ] Post changes to the expected status

[ ] published_at is populated after successful publishing

[ ] error_message is populated if publishing fails

```

Do not schedule a production test to an unknown user's account.

---

# 21. Delete Post Test

Create a test post.

Verify:

```text

[ ] User can delete own post

[ ] Deleted post disappears from the frontend

[ ] Database record is removed

[ ] Another user cannot delete the post

```

---

# 22. API Route Smoke Test

The backend currently exposes routes in these groups:

```text

/auth

/facebook

/media

/posts

/ai

/health

```

Open:

```text

http://127.0.0.1:8000/docs

```

Use Swagger for a quick smoke test.

Minimum checks:

```text

GET  /health

POST /auth/register

POST /auth/login

GET  /auth/me

GET  /auth/meta

GET  /auth/meta/pages

GET  /auth/instagram

GET  /auth/instagram/account

POST /media/upload

POST /posts/publish

POST /posts/schedule

POST /posts/test-publish

GET  /posts

GET  /posts/{post_id}

DELETE /posts/{post_id}

POST /ai/...

```

The exact AI endpoint paths and request schemas should always be taken from the generated Swagger documentation because they may change with the implementation.

---

# 23. Logs and Error Investigation

When something fails, follow this order:

```text

1. Browser error

       ↓

2. Frontend Network tab

       ↓

3. HTTP status + response body

       ↓

4. Backend terminal logs

       ↓

5. Database state

       ↓

6. Third-party provider logs

```

Do not immediately change code.

First determine:

```text

What request was sent?

What status code was returned?

What response body was returned?

What did FastAPI log?

Was the database changed?

Did Meta/Instagram/Cloudinary/OpenAI reject the request?

```

---

# 24. Production Environment

Production must not use:

```text

localhost

127.0.0.1

development credentials

local PostgreSQL

temporary ngrok URL

```

Production should use:

```text

Production frontend URL

Production backend URL

Production PostgreSQL

Production OAuth redirect URLs

Production secrets

```

---

# 25. Render Deployment

Render can deploy web services directly from a connected Git repository. A Render Web Service receives a public `onrender.com` URL and can also use a custom domain. citeturn0search2turn0search4

The deployment owner needs:

```text

[ ] Render account

[ ] Access to the correct Render workspace

[ ] Permission to create/manage services

[ ] Permission to connect the Git repository

[ ] Access to the production database

[ ] Access to production environment variables

```

---

# 26. Production Database

Create a Render PostgreSQL database.

The backend needs:

```text

DATABASE_URL

```

Where possible, use Render's internal database connection when the application and database are in the same Render account and region. Render documents internal connections as the preferred option when available. citeturn0search8

After creating the production database:

```text

[ ] Database exists

[ ] DATABASE_URL obtained

[ ] Backend can connect

[ ] Alembic migrations applied

```

---

# 27. Deploy Backend to Render

Create a Render Web Service from the repository.

Use:

```text

Root Directory:

backend

```

Build command:

```bash

pip install -r requirements.txt

```

Start command:

```bash

uvicorn main:app --host 0.0.0.0 --port $PORT

```

Render requires web services to listen on `0.0.0.0`; the default Render port is `10000`, exposed through the `PORT` environment variable. citeturn0search2turn0search6

Do not use:

```bash

uvicorn main:app --reload

```

in production.

---

# 28. Production Backend Environment Variables

Add these in the Render service's Environment section.

```env

PROJECT_NAME=AI Social Media Automation Platform

API_V1_STR=/api/v1

ENVIRONMENT=production

DATABASE_URL=\<RENDER_POSTGRES_URL>

JWT_SECRET=\<STRONG_PRODUCTION_SECRET>

JWT_ALGORITHM=HS256

ACCESS_TOKEN_EXPIRE_MINUTES=\<APPROVED_VALUE>

OPENAI_API_KEY=\<SECRET>

GEMINI_API_KEY=\<SECRET>

CLOUDINARY_NAME=\<VALUE>

CLOUDINARY_API_KEY=\<SECRET>

CLOUDINARY_API_SECRET=\<SECRET>

AYRSHARE_API_KEY=\<SECRET>

META_APP_ID=\<VALUE>

META_APP_SECRET=\<SECRET>

META_REDIRECT_URI=\<PRODUCTION_CALLBACK_URL>

INSTAGRAM_APP_ID=\<VALUE>

INSTAGRAM_APP_SECRET=\<SECRET>

INSTAGRAM_REDIRECT_URI=\<PRODUCTION_CALLBACK_URL>

TEST_PUBLISH_CAPTION=\<TEST_CAPTION>

TEST_PUBLISH_IMAGE_URL=\<TEST_IMAGE_URL>

FACEBOOK_TEST_PAGE_ID=\<TEST_PAGE_ID>

```

Render supports adding environment variables through the dashboard and redeploying after changes. It also warns not to commit secret credentials to repository configuration. citeturn0search0

---

# 29. Production Frontend

Create a Render service for the Next.js frontend.

Use the repository's:

```text

frontend/frontend

```

as the application root.

The frontend must use:

```env

NEXT_PUBLIC_API_URL=\<PRODUCTION_BACKEND_URL>/api/v1

```

Build:

```bash

npm install

npm run build

```

Start:

```bash

npm start

```

The exact Render service type/configuration should match the Next.js deployment strategy selected for this project.

---

# 30. Production CORS

The backend currently allows local development origins:

```text

http://localhost:3000

http://127.0.0.1:3000

```

Before production release, update CORS to allow the actual production frontend domain.

Example:

```text

https://your-frontend-domain.com

```

Do not leave production dependent on localhost.

---

# 31. Production OAuth

After the frontend and backend have stable production URLs:

### Meta

Replace the local callback URL with the production callback URL.

Update:

```env

META_REDIRECT_URI=\<PRODUCTION_META_CALLBACK>

INSTAGRAM_REDIRECT_URI=\<PRODUCTION_INSTAGRAM_CALLBACK>

```

Also update the corresponding URLs in the Meta Developer application.

### Important

Do not use:

```text

ngrok

localhost

127.0.0.1

```

for production OAuth.

ngrok is a local-development tunnel.

---

# 32. Production Final Test

Run the complete test using a **\*\*new user\*\***, not the original developer account.

```text

[ ] Register new user

[ ] Login

[ ] Dashboard loads

[ ] /auth/me works

[ ] Generate AI caption

[ ] Generate AI image, if enabled

[ ] Upload image

[ ] Connect Facebook

[ ] Connect Instagram

[ ] Create Facebook post

[ ] Create Instagram post

[ ] Create combined post

[ ] Schedule post

[ ] Verify Calendar

[ ] Verify published status

[ ] Verify failed status handling

[ ] Delete post

[ ] Verify user isolation

[ ] Verify another user cannot access the first user's data

```

---

# 33. Deployment Checklist

Before handing over the project:

```text

REPOSITORY

[ ] Code pushed

[ ] No secrets committed

[ ] .env files ignored

[ ] README/docs updated

BACKEND

[ ] Production environment variables configured

[ ] Backend deploy successful

[ ] Health endpoint returns 200

[ ] Swagger accessible if intentionally exposed

[ ] Logs clean

DATABASE

[ ] Production PostgreSQL created

[ ] DATABASE_URL configured

[ ] alembic upgrade head completed

[ ] alembic current verified

FRONTEND

[ ] Production build succeeds

[ ] Production API URL configured

[ ] Frontend can reach backend

[ ] Login works

AUTH

[ ] Registration works

[ ] Login works

[ ] Protected routes work

[ ] User isolation verified

AI

[ ] OpenAI/Gemini configured

[ ] AI features tested

MEDIA

[ ] Cloudinary configured

[ ] Upload tested

FACEBOOK

[ ] Meta app configured

[ ] Required permissions configured

[ ] Production callback configured

[ ] Facebook connection tested

[ ] Facebook publishing tested

INSTAGRAM

[ ] Instagram integration configured

[ ] Required permissions configured

[ ] Production callback configured

[ ] Instagram connection tested

[ ] Instagram publishing tested

SCHEDULER

[ ] Scheduling works

[ ] Scheduler starts correctly

[ ] Scheduled post is processed

SECURITY

[ ] Production secrets are not in Git

[ ] Production CORS configured

[ ] JWT secret is production-specific

[ ] Test accounts/pages are not accidentally used for real customers

```

---

# 34. Troubleshooting Quick Reference

## Backend does not start

Check:

```text

Python version

Virtual environment

requirements.txt

backend/app/.env

DATABASE_URL

```

Then:

```powershell

uvicorn main:app --reload

```

---

## Database error

Run:

```powershell

alembic current

alembic check

```

For a new database:

```powershell

alembic upgrade head

```

Verify PostgreSQL is running and `DATABASE_URL` is correct.

---

## Frontend cannot reach backend

Check:

```env

NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1

```

Then restart Next.js:

```powershell

npm run dev

```

For production, verify the variable points to the production backend.

---

## OAuth fails

Check:

```text

[ ] Backend is running

[ ] ngrok is running

[ ] Public ngrok URL works

[ ] Redirect URL exactly matches Meta

[ ] App ID is correct

[ ] App Secret is correct

[ ] Required permissions are configured

[ ] Test user has required access

```

---

## Facebook publishes to the wrong Page

Stop testing immediately.

Verify:

```text

Authenticated user

       ↓

Meta connection

       ↓

Facebook Page

       ↓

Page ID

       ↓

Publisher

```

Never assume the selected Page belongs to the current user.

---

## Instagram publishes to the wrong account

Verify:

```text

Authenticated user

       ↓

Instagram connection

       ↓

Instagram account ID

       ↓

Publisher

```

Test using a completely fresh user/account before release.

---

## Render deployment fails

Check the Render deployment logs.

Verify:

```text

[ ] Correct root directory

[ ] Correct build command

[ ] Correct start command

[ ] Python/Node runtime

[ ] Environment variables

[ ] DATABASE_URL

[ ] Port binding

```

Render exposes deployment/build logs in the service dashboard. citeturn0search2

---

# 35. Final Handover

A deployment is considered ready only when:

```text

Local setup

       ✓

Database

       ✓

Migrations

       ✓

Backend

       ✓

Frontend

       ✓

Authentication

       ✓

User isolation

       ✓

AI

       ✓

Cloudinary

       ✓

Facebook

       ✓

Instagram

       ✓

Scheduling

       ✓

Production deployment

       ✓

Production OAuth

       ✓

Final fresh-user test

       ✓

```

The person receiving the project should be able to follow:

```text

SETUP.md

     ↓

DEPLOYMENT_AND_TESTING.md

     ↓

Working local environment

     ↓

Working production environment

```

No secret credentials should be stored in either documentation file.