# FastAPI MVC Task Application

## Features

- Follows MVC design pattern
- Signup/Login with JWT Auth
- Add/Get/Delete in-memory posts
- SQLAlchemy with MySQL
- Caching with 5-minute expiry
- Full field validation using Pydantic
- Configured via `.env`

## Setup

```bash
# 1. Clone the repo
$ git clone https://github.com/yourname/fastapi-mvc-task.git
$ cd fastapi-mvc-task

# 2. Create .env
$ cp .env.example .env  # or manually add DB and JWT configs

# 3. Install dependencies
$ pip install -r requirements.txt

# 4. Run app
$ uvicorn main:app --reload
```

## .env Example

```
DATABASE_URL=mysql+pymysql://user:password@localhost:3306/mvc_app
SECRET_KEY=your_super_secret
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

## API Endpoints

### Auth

- `POST /auth/signup` — Register user
- `POST /auth/login` — Login and get token

### Posts (Requires Token)

- `POST /posts/add` — Add post (max 1MB)
- `GET /posts/` — Get user posts (cached 5 min)
- `DELETE /posts/{post_id}` — Delete post

## Testing

Use Postman or curl to test endpoints. Include the JWT token in the `Authorization` header: `Bearer <token>`
