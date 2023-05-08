# **API Documentation**

This documentation covers the API endpoints for the `clients`, `policies`, and `users` routes.


## **Clients**


### **List clients**

Endpoint: `/clients/`

Method: `GET`

Description: Lists all clients based on the given filters.

Query Parameters:



* `name` (optional, string): Filter clients by name.
* `id` (optional, string): Filter clients by ID.
* `role` (optional, string): Filter clients by role.
* `email` (optional, string): Filter clients by email.

Example:

```commandline
http GET 'http://localhost:8000/clients?name=John&id=1&role=admin&email=john@example.com' "Authorization: Bearer $TOKEN"
```


Success Response:



* Code: `200 OK`
* Content: List of filtered client objects.


### **List clients by name**

Endpoint: `/clients/name/{name}`

Method: `GET`

Description: Lists clients with the given name.

Path Parameters:



* `name` (required, string): Name to filter clients by.

Example:


```commandline
http GET 'http://localhost:8000/clients/name/John' "Authorization: Bearer $TOKEN"
```


Success Response:



* Code: `200 OK`
* Content: List of client objects with the given name.


### **List clients by filter**

Endpoint: `/clients/{filter}/{value}`

Method: `GET`

Description: Lists clients based on the given filter and value.

Path Parameters:



* `filter` (required, string): Key value for which to select the client.
* `value` (required, string): Value to filter clients by.

Example:

```commandline
http GET 'http://localhost:8000/clients/role/admin' "Authorization: Bearer $TOKEN"
```


Success Response:



* Code: `200 OK`
* Content: List of client objects with the given filter and value.


## **Policies**


### **List policies**

Endpoint: `/policies/`

Method: `GET`

Description: Lists all policies based on the given filters.

Query Parameters:



* `amountInsured` (optional, float): Filter policies by amount insured.
* `id` (optional, string): Filter policies by ID.
* `clientId` (optional, string): Filter policies by client ID.
* `inceptionDate` (optional, datetime): Filter policies by inception date.
* `installmentPayment` (optional, bool): Filter policies by installment payment.
* `email` (optional, string): Filter policies by email.

Example:
```commandline
http GET 'http://localhost:8000/policies?amountInsured=1000&id=1&clientId=1&inceptionDate=2023-05-01&installmentPayment=true&email=john@example.com' "Authorization: Bearer $TOKEN"
```


Success Response:



* Code: `200 OK`
* Content: List of filtered policy objects.


### **List policies by client name**

Endpoint: `/policies/by_client_name/{client_name}`

Method: `GET`

Description: Lists policies by the given client name.

Path Parameters:



* `client_name` (required, string): Client name to filter policies by.

Example:

```commandline
http GET 'http://localhost:8000/policies/by_client_name/John' "Authorization: Bearer $TOKEN"
```


Success Response:



* Code: `200 OK`
* Content: List of policy objects with the given client name or None if not found.


### **List client by policy**

**Endpoint: `/policies/by_policy/{policy_id}`

Method: `GET`

Description: Lists the client associated with the given policy ID.

Path Parameters:



* `policy_id` (required, string): Policy ID to find the associated client.

Example:

```commandline
http GET 'http://localhost:8000/policies/by_policy/{policy_id}' "Authorization: Bearer $TOKEN"
```


Success Response:



* Code: `200 OK`
* Content: List of client objects associated with the policy or None if not found.


## **Users**


### **Register user**

Endpoint: `/users/register`

Method: `POST`

Description: Registers a new user in the system.

Request Body:



* `newUser` (required, UserBase): New user object.

Example:

```commandline
http POST 'http://localhost:8000/users/register' newUser:='{"username": "newuser", "email": "newuser@example.com", "password": "mypassword", "role": "user"}'
```


Success Response:



* Code: `201 CREATED`
* Content: Created user data.


### **Login user**

Endpoint: `/users/login`

Method: `POST`

Description: Logs in a user and returns an access token.

Request Body:



* `username` (required, string): The user's username.
* `password` (required, string): The user's password.

Example:

```commandline
http POST 'http://localhost:8000/users/login' username='myusername' password='mypassword'
```


Success Response:



* Code: `200 OK`
* Content: Access token.

Note: Replace `localhost:8000` with the appropriate base URL of your API. Also, ensure that you have httpie installed and available on your system.
