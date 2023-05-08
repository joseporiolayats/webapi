
# API Documentation

This document describes the API endpoints for the FastAPI application, including authentication, user registration, login, and accessing policy data.

## Table of Contents

- [Authentication](#authentication)
- [User Registration](#user-registration)
- [User Login](#user-login)
- [Get User Data](#get-user-data)
- [Get Policy Data](#get-policy-data)

## Authentication

The application uses JWT (JSON Web Tokens) for authentication. After registering or logging in, a JWT token is returned. This token must be included in the `Authorization` header for all requests to restricted endpoints.

## User Registration

**Endpoint:** `/register`

**Method:** `POST`

**Request Body:**

- `username` (string): The desired username.
- `email` (string): The user's email address.
- `password` (string): The user's password.

**Response:**

A JSON object containing the newly created user's data.

**Example Request:**

```bash
http POST http://localhost:8000/register username="newuser" email="newuser@example.com" password="mypassword"
```


## **User Login**

Endpoint: `/login`

Method: `POST`

Request Body:



* `email` (string): The user's email address.
* `password` (string): The user's password.

Response:

A JSON object containing the JWT token.

Example Request:

bash


```
http POST http://localhost:8000/login email="britneyblankenship@quotezart.com" password="mypassword"
```



## **Get User Data**

Endpoint: `/me`

Method: `GET`

Headers:



* `Authorization`: Bearer {your_jwt_token}

Response:

A JSON object containing the logged-in user's data.

Example Request:

bash


```
http GET http://localhost:8000/me "Authorization: Bearer {your_jwt_token}"
```



## **Get Policy Data**


### **List all policies**

Endpoint: `/policies`

Method: `GET`

Headers:



* `Authorization`: Bearer {your_jwt_token}

Response:

A JSON array containing all the policy data.

Example Request:

bash


```
http GET http://localhost:8000/policies "Authorization: Bearer {your_jwt_token}"
```



### **Get policy by ID**

Endpoint: `/policies/{policy_id}`

Method: `GET`

Path Parameters:



* `policy_id` (string): The ID of the policy.

Headers:



* `Authorization`: Bearer {your_jwt_token}

Response:

A JSON object containing the policy data for the specified ID.

Example Request:

bash


```
http GET http://localhost:8000/policies/64cceef9-3a01-49ae-a23b-3761b604800b "Authorization: Bearer {your_jwt_token}"
```



### **Get policies by user ID**

Endpoint: `/policies/user/{user_id}`

Method: `GET`

Path Parameters:



* `user_id` (string): The ID of the user.

Headers:



* `Authorization`: Bearer {your_jwt_token}

Response:

A JSON array containing the policy data for the specified user ID.

Example Request:

bash


```
http GET http://localhost:8000/policies/user/a0ece5db-cd14-4f21-812f-966633e
