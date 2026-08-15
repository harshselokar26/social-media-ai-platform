---

#  `META_SETUP.md`


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
--

#3. Configure Application Settings

Configure the application's OAuth settings using the redirect URL provided
by the backend.

The redirect URL must exactly match the URL configured in the Meta application.

Example:

https://your-domain.com/api/v1/meta/callback

For local development, use the project's configured localhost callback URL.

Do not copy the example above unless it matches the actual backend route.
--------------------------------------------------------------------------------------------------------------------------------
4. Required Permissions

The current Facebook integration has been tested with permissions including:

pages_show_list
business_management
pages_read_engagement
pages_manage_metadata
pages_read_user_content
pages_manage_posts
pages_manage_engagement
public_profile

These permissions allow the application to perform the currently implemented
Facebook operations.

Permissions may require Meta review depending on the application mode,
account configuration and intended production usage.
--------------------------------------------------------------------------------------------------------------------------------
5. Authorization Flow

The application does not directly ask the customer to manually enter a
Facebook Page access token.

Instead, the application uses Meta authorization.

The flow is:

Customer
   |
   v
Our Application
   |
   v
Meta Login / Authorization
   |
   v
Customer grants permissions
   |
   v
Meta Authorization Response
   |
   v
Backend receives access information
   |
   v
Retrieve available Facebook Pages
   |
   v
Retrieve Page Access Token
   |
   v
Store connection

--------------------------------------------------------------------------------------------------------------------------------
6. User Token vs Page Access Token

This distinction is important.

The Meta user access token is not always the token used for Page operations.

For Page-level operations, the application obtains the Page access token after
retrieving the user's available Pages.

The backend stores the Page access token associated with the connected Page.

The Facebook service then uses this Page access token when calling the Graph API.
----------------------------------------------------------------------------------------------------------------------------------
7. Security

Meta credentials must never be exposed to frontend users or committed to the
repository.

Sensitive credentials must be stored securely.

At minimum:

META_APP_ID
META_APP_SECRET
META access tokens
Page access tokens

must be protected.
---------------------------------------------------------------------------------------------------------------------------
8. Development vs Production

During development, the Meta application can be configured for testing.

Before production deployment, verify:

OAuth redirect URL
Application mode
Required permissions
Meta review requirements
Page permissions
Production domain
HTTPS configuration
Token handling
--------------------------------------------------------------------------------------------------------------------------------


---

# 4. `FACEBOOK.md`

This should explain the **actual functionality we have already completed**.

```md
# Facebook Integration

## Overview

The Facebook integration allows an authenticated application user to connect
a Facebook Page and perform supported Page operations through the Meta Graph
API.

## Current Features

The current implementation supports:

- Retrieve Facebook Page information
- Retrieve Page posts
- Retrieve post comments
- Retrieve Page insights
- Create a Facebook Page post
- Delete a Facebook Page post

---

# 1. Facebook Connection

After Meta authorization, the backend retrieves the Facebook Pages available
to the user.

The selected Page is stored in the database.

The application associates the Page with the authenticated application user.

---

# 2. Page Information

Endpoint:

```text
GET /api/v1/facebook/pages/{page_id}
----------------------------------------------------------------------------------------------------------------------------------
3. Get Posts

Endpoint:

GET /api/v1/facebook/pages/{page_id}/posts

Returns Page posts including information such as:

id
message
created_time


4. Get Comments

Endpoint:

GET /api/v1/facebook/posts/{post_id}/comments

Returns comments associated with the post.



5. Page Insights

Endpoint:

GET /api/v1/facebook/pages/{page_id}/insights

The endpoint is read-only.

The metric can be provided as a query parameter.

Example:

?metric=page_views_total


6. Create Post

Endpoint:

POST /api/v1/facebook/pages/{page_id}/posts

The endpoint creates a text post on the connected Facebook Page.

Example message:

This is a test post from our Social Media Automation Platform.

The returned response contains the Meta post ID.



7. Delete Post

Endpoint:

DELETE /api/v1/facebook/posts/{post_id}

The endpoint deletes a Facebook post using the connected Page access token.

This functionality has been tested successfully.

Expected successful response:

{
    "success": true
}




8. Security

Before performing an operation, the backend verifies that the requested
Facebook Page belongs to the authenticated application user.

The backend checks:

Facebook Page
       ↓
Meta Connection
       ↓
Authenticated User

This prevents a user from directly using another user's connected Page.





9. Facebook API Flow
Application User
       ↓
JWT Authentication
       ↓
Find Connected Facebook Page
       ↓
Retrieve Page Access Token
       ↓
FacebookPageService
       ↓
Meta Graph API
       ↓
Facebook Page

---

# 5. `API_REFERENCE.md`

This should be extremely simple.

```md
# API Reference

Base URL:

```text
http://127.0.0.1:8000/api/v1

Production URL will depend on deployment configuration.

Facebook
Get Page
GET /facebook/pages/{page_id}

Purpose:

Retrieve Facebook Page information.

Get Posts
GET /facebook/pages/{page_id}/posts

Purpose:

Retrieve posts from a Facebook Page.

Get Comments
GET /facebook/posts/{post_id}/comments

Purpose:

Retrieve comments for a Facebook post.

Get Insights
GET /facebook/pages/{page_id}/insights

Purpose:

Retrieve Page insights.

Query parameter:

metric

Example:

GET /facebook/pages/123456/insights?metric=page_views_total
Create Post
POST /facebook/pages/{page_id}/posts

Purpose:

Create a text post.

Delete Post
DELETE /facebook/posts/{post_id}

Purpose:

Delete a Facebook post.

Authentication

Protected endpoints require:

Authorization: Bearer <JWT_TOKEN>

The JWT token belongs to the application authentication system.

It is different from the Meta access token.


---


# 6. `ARCHITECTURE.md`

```md
# System Architecture

## Overview

The platform uses a backend service architecture where the FastAPI
application manages authentication, database access and communication with
social media APIs.

## Architecture

```text
                    Client
                      |
                      v
                FastAPI Backend
                      |
          +-----------+-----------+
          |           |           |
          v           v           v
       Auth       Database    Social Services
          |           |           |
          |           |           v
          |           |      Meta Graph API
          |           |           |
          |           |      +----+----+
          |           |      |         |
          |           |   Facebook  Instagram
          |           |
          +-----------+
Main Components
Authentication

Responsible for authenticating application users.

Database

Stores:

Users
Meta connections
Facebook Pages
Page access tokens
Application configuration
Meta Authentication Service

Responsible for Meta authorization and retrieving available Pages.

Facebook Page Service

Responsible for communication with the Facebook Graph API.

Current operations:

Get Page
Get Posts
Get Comments
Get Insights
Create Post
Delete Post
API Router

Exposes the backend functionality through REST endpoints.

Facebook Request Flow
HTTP Request
     |
     v
Facebook Router
     |
     v
Authenticate User
     |
     v
Find User's Facebook Page
     |
     v
FacebookPageService
     |
     v
Meta Graph API
     |
     v
Return Response

---



# 7. `TESTING.md`

This is based heavily on what we just went through.

```md
# Testing Guide

## Objective

Verify that the Facebook integration can communicate with Meta and perform
basic read/write operations successfully.

---

# 1. Start Backend

```bash
uvicorn app.main:app --reload

Open:

http://127.0.0.1:8000/docs



2. Authenticate

Authenticate through the application and obtain a JWT token.

Authorize Swagger with:

Bearer <JWT_TOKEN>



3. Verify Facebook Page

Call:

GET /api/v1/facebook/pages/{page_id}

Expected:

{
    "id": "...",
    "name": "..."
}
4. Verify Posts

Call:

GET /api/v1/facebook/pages/{page_id}/posts

Verify that existing Page posts are returned.




5. Create Test Post

Call:

POST /api/v1/facebook/pages/{page_id}/posts

Use a clearly identifiable test message.

Example:

TEST POST - Social Media Automation Platform

Save the returned post ID.

6. Verify Test Post

Call:

GET /api/v1/facebook/pages/{page_id}/posts

Confirm that the test post appears.

7. Delete Test Post

Call:

DELETE /api/v1/facebook/posts/{post_id}

Expected:

{
    "success": true
}
8. Verify Deletion

Request the Page posts again and confirm that the test post is no longer
present.

Successful Test Flow
Connect Meta
     ↓
Get Page
     ↓
Get Posts
     ↓
Create Test Post
     ↓
Get Posts
     ↓
Find Test Post
     ↓
Delete Test Post
     ↓
Success

---

# 8. `TROUBLESHOOTING.md`

And this one is **gold** because we've already solved these problems ourselves.

```md
# Troubleshooting

## 1. Invalid OAuth Access Token

Example:

```text
Invalid OAuth 2.0 Access Token
Possible Cause

The wrong type of Meta token is being used.

For Page operations, the application should use the Page access token obtained
for the connected Page.

Check

Verify:

Meta connection exists
Correct Page is connected
Page access token exists
Token has required permissions
2. Unsupported Delete Request

Example:

Unsupported delete request.
Object with ID '...' does not exist,
cannot be loaded due to missing permissions,
or does not support this operation.
Check
Verify the post ID.
Verify the post belongs to the connected Page.
Verify the Page access token.
Verify required permissions.
Confirm the post has not already been deleted.
3. Facebook Requires Page Access Token

If Facebook returns an error indicating that a Page access token is required,
verify that the backend is not accidentally using the application user's
access token.

The correct flow is:

User Access Token
       ↓
Get Pages
       ↓
Page Access Token
       ↓
Page API Request
4. HTTPX ReadTimeout

Example:

httpx.ReadTimeout
Cause

Facebook did not return a response within the HTTP client's configured
timeout.

Handling

The Facebook service uses an explicit HTTP timeout and catches timeout
exceptions.

The API returns a gateway/timeout error instead of exposing the raw exception
to the client.

5. 404 Not Found

If Swagger returns:

{
    "detail": "Not Found"
}

Check:

Backend is running the latest code.
Correct URL is being used.
Router is included in the FastAPI application.
Server has been restarted after route changes.

Example expected route:

DELETE /api/v1/facebook/posts/{post_id}
6. Facebook Permission Error

If Meta returns a permission error:

Check the permissions granted to the Meta application.

Current Facebook integration requires permissions appropriate for the
operations being performed.

Also verify that the user has appropriate access to the Facebook Page

