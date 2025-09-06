# TODO API in FastAPI

> ## How to run
First, open a terminal in the root directory of the project and run the following commands:
```bash
pip install fastapi[standard]

pip install -r requirements.txt
```

After, run the following command from the opened terminal:

```bash
fastapi dev src/main.py
```

> ## How to test
Run the following command in your terminal from the root directory of the project
 - `Linux`
```bash
python3 test.py
```
 - `Windows`
```shell
python test.py
```

> ## How to use
For a more detailed information, run the app and open the <a href="http://localhost:8000/docs">documentation</a>. (***this will work only in your local machine if the app is running***)
### Users endpoints

> `POST` /api/v1/register:
```shell
curl http://localhost:8000/api/v1/register \
  --request POST \
  --header 'Content-Type: application/json' \
  --data '{
  "username": "name",
  "email": "email@example.com",
  "password": "password"
}'
```
- `RESPONSE`:
```shell
{
  "username": "name",
  "email": "email@example.com",
  "id": "password"
}
```

> `POST` /api/v1/token:
```shell
curl http://localhost:8000/api/v1/token \
  --request POST \
  --header 'Content-Type: application/x-www-form-urlencoded' \
  --data-urlencode 'grant_type=password' \
  --data-urlencode 'username=name' \
  --data-urlencode 'password=user_password' \
  --data-urlencode 'scope=' \
  --data-urlencode 'client_id=client_id' \
  --data-urlencode 'client_secret=client_secret'
```

 - `RESPONSE`:
```shell
{
  "access_token": "string",
  "token_type": "string"
}
```

### Tasks endpoints

> `POST` /api/v1/tasks
```shell
curl http://localhost:8000/api/v1/tasks \
  --request POST \
  --header 'Content-Type: application/json' \
  --header 'Authorization: Bearer YOUR_SECRET_TOKEN' \
  --data '{
  "title": "title",
  "description": "description",
  "status": false
}'
```

 - `RESPONSE`:
```shell
{
  "title": "title",
  "description": "description",
  "status": false,
  "id": "string",
  "created_at": "2025-09-06T07:11:34.762Z",
  "user_id": "string"
}
```

> `GET` /api/v1/tasks:
```shell
curl 'http://localhost:8000/api/v1/tasks?skip=0&limit=100&status=true' \
  --header 'Authorization: Bearer YOUR_SECRET_TOKEN'
```

 - `RESPONSE`:
```shell
[
  {
    "title": "string",
    "description": "string",
    "status": false,
    "id": "string",
    "created_at": "2025-09-06T07:11:34.762Z",
    "user_id": "string"
  }
]
```

> `GET` /api/v1/tasks/{task_id}:
```shell
curl 'http://localhost:8000/api/v1/tasks/{task_id}' \
  --header 'Authorization: Bearer YOUR_SECRET_TOKEN'
```
 - `RESPONSE`:
```shell
{
  "title": "string",
  "description": "string",
  "status": false,
  "id": "string",
  "created_at": "2025-09-06T07:11:34.762Z",
  "user_id": "string"
}
```

> `PUT` /api/v1/tasks/{task_id}:
```shell
curl 'http://localhost:8000/api/v1/tasks/{task_id}' \
  --request PUT \
  --header 'Content-Type: application/json' \
  --header 'Authorization: Bearer YOUR_SECRET_TOKEN' \
  --data '{
  "title": "new title",
  "description": "new description",
  "status": false
}'
```
 - `RESPONSE`:
```shell
{
  "title": "new title",
  "description": "new description",
  "status": false,
  "id": "string",
  "created_at": "2025-09-06T07:11:34.762Z",
  "user_id": "string"
}
```

> `DELETE` /api/v1/tasks/{task_id}:
```shell
curl 'http://localhost:8000/api/v1/tasks/{task_id}' \
  --request DELETE \
  --header 'Authorization: Bearer YOUR_SECRET_TOKEN'
```
 - `RESPONSE`:
```shell
null
```
