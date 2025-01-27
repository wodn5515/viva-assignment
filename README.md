# 기술과제
비바이노베이션 서버파트 사전과제입니다.

# 프로젝트 소개
## ⚙️ 개발 환경
- **Language**: Python 3.11.4
- **Database**:
  - MySQL 5.7
  - MongoDB 6.0.20
- **Framework**: Django 3.1.12
- Docker 20.10.12

## ▶️ Installation

    $ git clone https://github.com/wodn5515/viva-assignment.git

### 환경변수 설정

    DJANGO_SECRET_KEY="" # django 시크릿 키
    DJANGO_SETTINGS_MODULE="config.settings.development"
    # MONGO DB
    MONGO_DB_NAME="" # mongo db databse 명
    MONGO_DB_HOST="mongodb://mongo"
    MONGO_DB_USERNAME="" # mongo db에서 사용할 username
    MONGO_DB_PASSWORD="" # mongo db에서 사용할 password
    MONGO_DB_PORT="27017"
    MONGO_DB_URL="mongodb://{MONGO_DB_USER_NAME}:{MONGO_DB_PASSWORD}@mongo:27017/" # 위에 작성된 환경변수값 그대로 적용 
    ME_CONFIG_BASICAUTH="true"
    # MYSQL DB
    MYSQL_DB_HOST="mysql"
    MYSQL_DB_NAME="" # mysql에서 사용할 db name
    MYSQL_DB_USERNAME="" # mysql에서 사용할 username
    MYSQL_DB_PASSWORD="" # mysql에서 사용할 password
    MYSQL_DB_PORT="3306"
    MYSQL_ROOT_PASSWORD="" # mysql에서 사용할 root 계정 password
    MYSQL_ROOT_USERNAME="" # mysql에서 사용할 root 계정 username

### 도커 실행

    $ docker compose -f docker-compose.yml up --build

# 📒 API 명세

- [User API](#user)
  - [회원가입](#signup)
  - [로그인](#login)
  - [토큰 재발급](#refresh)
  - [로그아웃](#logout)
- [게시글 API](#board)
  - [게시글 작성](#create_post)
  - [게시글 목록 조회](#list_post)
  - [게시글 조회](#retrieve_post)
  - [게시글 수정](#update_post)
  - [게시글 삭제](#delete_post)

<a name="user"></a>
## 📌유저 API
<a name="signup"></a>
### 📍회원가입

    POST /users/signup

**Request**
- Body
```json
{
  "email": "로그인에 사용할 email (unique)",
  "name": "이름",
  "password": "비밀번호",
  "password_check": "비밀번호 확인용 재입력"
}
```
**Response**
- Success<br>
  STATUS_CODE: 201
  ```json
  {
    "id": 0,
    "name": "string",
    "email": "example@email.com",
    "is_active": true,
    "is_staff": false,
    "is_superuser": false
  }
  ```
- Error
  - 이미 가입한 이메일
  ```json
  {
      "status": 400,
      "code": "ALREADY_SIGNED_UP_EMAIL",
      "detail": "이미 가입된 이메일입니다."
  }
  ```
  - 비밀번호와 비밀번호검사 값이 다른경우
  ```json
  {
      "status": 400,
      "code": "PASSWORD_NOT_MATCHED",
      "detail": "비밀번호가 서로 다릅니다"
  }
  ```
  - 입력값 validation 실패시
  ```json
  {
    "status": 400,
    "code": "INPUT_VALIDATION_ERROR",
    "detail": "유효하지않은 입력입니다."
  }
  ```
---
<a name="login"></a>
### 📍로그인

    POST /users/login

**Request**
- Body
```json
{
    "email": "회원가입시 입력했던 email",
    "password": "회원가입시 입력했던 password"
}
```
**Response**
- Success<br>
  STATUS_CODE: 200
  ```json
  {
    "user": {
        "id": 0,
        "name": "string",
        "email": "example@email.com",
        "is_active": true,
        "is_staff": false,
        "is_superuser": false
    },
    "token": {
        "refresh": "string(refresh_token)",
        "access": "string(access_token)"
    }
  }
  ```
- Error
  - 입력값 validation 실패시
  ```json
  {
    "status": 400,
    "code": "INPUT_VALIDATION_ERROR",
    "detail": "유효하지않은 입력입니다."
  }
  ```
  - 입력된 데이터로 가입된 회원이 없는경우
  ```json
  {
    "status": 401,
    "code": "AUTHENTICATED_FAILED",
    "detail": "이메일 또는 비밀번호가 올바르지 않습니다."
  }
  ```
---
<a name="refresh"></a>
### 📍토큰 재발급

    POST /users/refresh

**Request**
- Body
```json
{
    "refresh": "string(refresh_token)"
}
```
**Response**
- Success<br>
  STATUS_CODE: 200
  ```json
  {
    "access": "string(access_token)"
  }
  ```
- Error
  - 입력값 validation 실패시
  ```json
  {
    "status": 400,
    "code": "INPUT_VALIDATION_ERROR",
    "detail": "유효하지않은 입력입니다."
  }
  ```
  - refresh_token이 유효하지 않은 경우
  ```json
  {
    "status": 401,
    "code": "TOKEN_IS_INVALID_OR_EXPIRED",
    "detail": "인증정보가 유효하지 않습니다. 새롭게 로그인 해주세요."
  }
  ```
---
<a name="logout"></a>
### 📍로그아웃

    POST /users/login

**Request**
- Header
```json
{
  "Authorization": "string(Bearer access_token)"
}
```
- Body
```json
{
  "refresh": "string(refresh_token)"
}
```
**Response**
- Success<br>
  STATUS_CODE: 204
  ```
  ```
- Error
  - 입력값 validation 실패시
  ```json
  {
    "status": 400,
    "code": "INPUT_VALIDATION_ERROR",
    "detail": "유효하지않은 입력입니다."
  }
  ```
  - refresh_token이 유효하지 않은 경우
  ```json
  {
    "status": 401,
    "code": "TOKEN_IS_INVALID_OR_EXPIRED",
    "detail": "인증정보가 유효하지 않습니다. 새롭게 로그인 해주세요."
  }
  ```
  - access token 로그인 실패시
  ```json
  {
    "status": 401,
    "code": "NOT_AUTHENTICATED",
    "detail": "로그인이 필요합니다."
  }
  ```
---
<a name="board"></a>
## 📌게시글 API
<a name="create_post"></a>
### 📍게시글 작성

    POST /posts

**Request**
- Header
```json
{
  "Authorization": "string(Bearer access_token)"
}
```
- Body
```json
{
  "title": "string",
  "content": "string"
}
```
**Response**
- Success<br>
  STATUS_CODE: 201
  ```json
  {
    "id": 0,
    "title": "string",
    "content": "string",
    "author_id": 0,
    "created_at": "string(datetime)",
    "updated_at": "string(datetime)"
  }
  ```
- Error
  - access token 로그인 실패시
  ```
  - access token 로그인 실패시
  ```json
  {
    "status": 401,
    "code": "NOT_AUTHENTICATED",
    "detail": "로그인이 필요합니다."
  }
  ```
  - 입력값 validation 실패시
  ```json
  {
    "status": 400,
    "code": "INPUT_VALIDATION_ERROR",
    "detail": "유효하지않은 입력입니다."
  }
  ```
  - 게시글의 제목이 너무 긴 경우
  ```json
  {
    "status": 400,
    "code": "TITLE_TOO_LONG",
    "detail": "게시글의 제목이 너무 깁니다."
  }
  ```
---
<a name="list_post"></a>
### 📍게시글 목록 조회

    GET /posts

**Request**
- Params
```
page: int
page-size: int # 페이지당 데이터 개수
order-by: strEnum["newest", "oldest"] # 최신순/오래된순 정렬
author-id: int # 작성자 user_id로 검색
```
**Response**
- Success<br>
  STATUS_CODE: 200
  ```json
  {
    "results": [
        {
            "id": 0,
            "title": "string",
            "content": "string",
            "author_id": 0,
            "created_at": "string(datetime)",
            "updated_at": "string(datetime)"
        }
    ]
  }
  ```
- Error
  - 입력값 validation 실패시
  ```json
  {
    "status": 400,
    "code": "INPUT_VALIDATION_ERROR",
    "detail": "유효하지않은 입력입니다."
  }
  ```
---
<a name="retrieve_post"></a>
### 📍게시글 조회

    POST /posts/{post_id}

**Request**
- PathVariable
```
  "post_id": int
```
**Response**
- Success<br>
  STATUS_CODE: 200
  ```json
  {
    "id": 0,
    "title": "string",
    "content": "string",
    "author_id": 0,
    "created_at": "string(datetime)",
    "updated_at": "string(datetime)"
  }
  ```
- Error
  - 게시글이 존재하지 않는 경우
  ```json
  {
    "status": 404,
    "code": "POST_NOT_FOUND",
    "detail": "게시글을 찾을 수 없습니다."
  }
  ```
---
<a name="update_post"></a>
### 📍게시글 수정

    PATCH /posts{post_id}

**Request**
- PathVariable
```
  "post_id": int
```
- Header
```json
{
  "Authorization": "string(Bearer access_token)"
}
```
- Body
```json
{
  "title": "string(optional)",
  "content": "string(optional)"
}
```
**Response**
- Success<br>
  STATUS_CODE: 200
  ```json
  {
    "id": 0,
    "title": "string",
    "content": "string",
    "author_id": 0,
    "created_at": "string(datetime)",
    "updated_at": "string(datetime)"
  }
  ```
- Error
  - access token 로그인 실패시
  ```
  - access token 로그인 실패시
  ```json
  {
    "status": 401,
    "code": "NOT_AUTHENTICATED",
    "detail": "로그인이 필요합니다."
  }
  ```
  - 수정 권한이 없는 경우
  ```json
  {
    "status": 403,
    "code": "PERMISSION_DENIED",
    "detail": "권한이 없습니다."
  }
  ```
  - 입력값 validation 실패시
  ```json
  {
    "status": 400,
    "code": "INPUT_VALIDATION_ERROR",
    "detail": "유효하지않은 입력입니다."
  }
  ```
  - 게시글의 제목이 너무 긴 경우
  ```json
  {
    "status": 400,
    "code": "TITLE_TOO_LONG",
    "detail": "게시글의 제목이 너무 깁니다."
  }
  ```
  - 게시글이 존재하지 않는 경우
  ```json
  {
    "status": 404,
    "code": "POST_NOT_FOUND",
    "detail": "게시글을 찾을 수 없습니다."
  }
  ```
---
<a name="delete_post"></a>
### 📍게시글 삭제

    DELETE /posts/{post_id}

**Request**
- PathVariable
```
  "post_id": int
```
- Header
```json
{
  "Authorization": "string(Bearer access_token)"
}
```
**Response**
- Success<br>
  STATUS_CODE: 204
  ```json
  {
    "id": 0,
    "title": "string",
    "content": "string",
    "author_id": 0,
    "created_at": "string(datetime)",
    "updated_at": "string(datetime)"
  }
  ```
- Error
  - access token 로그인 실패시
  ```
  - access token 로그인 실패시
  ```json
  {
    "status": 401,
    "code": "NOT_AUTHENTICATED",
    "detail": "로그인이 필요합니다."
  }
  ```
  - 삭제 권한이 없는 경우
  ```json
  {
    "status": 403,
    "code": "PERMISSION_DENIED",
    "detail": "권한이 없습니다."
  }
  ```
  - 입력값 validation 실패시
  ```json
  {
    "status": 400,
    "code": "INPUT_VALIDATION_ERROR",
    "detail": "유효하지않은 입력입니다."
  }
  ```
  - 게시글이 존재하지 않는 경우
  ```json
  {
    "status": 404,
    "code": "POST_NOT_FOUND",
    "detail": "게시글을 찾을 수 없습니다."
  }
  ```
---



