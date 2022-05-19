# Set-as-a-Service REST API sample application

This is a bare-bones example of a REST API that implements the
'set' datatructure without using built-in hashmaps or sets.

The entire application is contained within the `main.py` file,
and the only requirement is Python 3.

## Run the app

    python3 main.py

## Run the tests

    python3 main.py test

# REST API

The REST API to the example app is described below.

## Get objects in the set

### Request

`GET /status/`

    curl -i http://localhost:8080/status/

### Response

    HTTP/1.0 200 OK
    Server: BaseHTTP/0.6 Python/3.10.4
    Date: Fri, 20 May 2022 00:00:00 GMT
    Content-Type: application/json
    Content-Length: 13

    {"result":[]}

## Add a new element

### Request

`GET /add/:id`

    curl -i http://localhost:8080/add/

### Response

    HTTP/1.0 201 Created
    Server: BaseHTTP/0.6 Python/3.10.4
    Date: Fri, 20 May 2022 00:00:00 GMT
    Content-Type: application/json
    Content-Length: 15

    {"result":"ok"}

## Remove an element

### Request

`GET /remove/:id`

    curl -i http://localhost:8080/remove/1

### Response

    HTTP/1.0 200 OK
    Server: BaseHTTP/0.6 Python/3.10.4
    Date: Fri, 20 May 2022 00:00:00 GMT
    Content-Type: application/json
    Content-Length: 15

    {"result":"ok"}

## Check if an element is present

### Request

`GET /has/:id`

    curl -i http://localhost:8080/has/1

### Response

    HTTP/1.0 200 OK
    Server: BaseHTTP/0.6 Python/3.10.4
    Date: Fri, 20 May 2022 00:00:00 GMT
    Content-Type: application/json
    Content-Length: 17

    {"result":"True"}

## Add an element that already exists

### Request

`GET /add/:id`

    curl -i http://localhost:8080/add/1

### Response

    HTTP/1.0 200 OK
    Server: BaseHTTP/0.6 Python/3.10.4
    Date: Fri, 20 May 2022 00:00:00 GMT
    Content-Type: application/json
    Content-Length: 15

    {"result":"ok"}

## Remove a non-existent element

### Request

`GET /remove/:id`

    curl -i http://localhost:8080/remove/999

### Response

    HTTP/1.0 400 Bad Request
    Server: BaseHTTP/0.6 Python/3.10.4
    Date: Fri, 20 May 2022 00:00:00 GMT
    Content-Type: application/json
    Content-Length: 24

    {"result":"nonexistent"}

## Check if an element is present (negative case)

### Request

`GET /has/:id`

    curl -i http://localhost:8080/has/999

### Response

    HTTP/1.0 200 OK
    Server: BaseHTTP/0.6 Python/3.10.4
    Date: Fri, 20 May 2022 00:00:00 GMT
    Content-Type: application/json
    Content-Length: 18

    {"result":"False"}

## Attempting to make a request with missing or invalid data

### Request

`GET /add/:id`

    curl -i http://localhost:8080/add/
    curl -i http://localhost:8080/add/nope

### Response

    HTTP/1.0 406 Not Acceptable
    Server: BaseHTTP/0.6 Python/3.10.4
    Date: Fri, 20 May 2022 00:00:00 GMT

## Attempting to make a request with an unsupported method

### Request

`PUT /add/:id`

    curl -i -X PUT http://localhost:8080/add/1

### Response

    HTTP/1.0 501 Unsupported method ('PUT')
    Server: BaseHTTP/0.6 Python/3.10.4
    Date: Fri, 20 May 2022 00:00:00 GMT
    Connection: close
    Content-Type: text/html;charset=utf-8
    Content-Length: 496

    <!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN"
            "http://www.w3.org/TR/html4/strict.dtd">
    <html>
        <head>
            <meta http-equiv="Content-Type" content="text/html;charset=utf-8">
            <title>Error response</title>
        </head>
        <body>
            <h1>Error response</h1>
            <p>Error code: 501</p>
            <p>Message: Unsupported method ('PUT').</p>
            <p>Error code explanation: HTTPStatus.NOT_IMPLEMENTED - Server does not support this operation.</p>
        </body>
    </html>
