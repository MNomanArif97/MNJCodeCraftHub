CodeCraftHub is a beginner-friendly REST API project for managing courses.

The application allows users to create, view, update, and delete courses. It is built with Python and Flask and uses JSON for communication between the client and the server.

This project is useful for learning:

- REST API concepts
- HTTP methods
- JSON request and response data
- Flask routing
- CRUD operations
- API testing with `curl.exe`
- Error handling and HTTP status codes

---

## Features

CodeCraftHub provides the following features:

- Create a new course
- View all courses
- View one course by its ID
- Update an existing course
- Delete a course
- Validate required course fields
- Validate course status values
- Validate target dates
- Return JSON responses
- Return suitable HTTP status codes
- Handle invalid JSON requests
- Handle requests for courses that do not exist

---

## Technologies Used

- Python
- Flask
- Flask-SQLAlchemy or SQLite database, depending on the project configuration
- REST API
- JSON
- `curl.exe`
- PowerShell or VS Code terminal

---

## Project Requirements

Before installing the project, make sure you have:

- Python installed
- Visual Studio Code installed
- Git installed, if cloning the project from a repository
- A terminal such as PowerShell
- A web browser or API testing tool

To check whether Python is installed, run:

```powershell
python --version
Example output:

Python 3.14.3
The exact version on your computer may be different.

Installation
1. Open the project folder
Open the CodeCraftHub project in Visual Studio Code.

Alternatively, navigate to the project folder in PowerShell:

cd "D:\Study\Generative AI Elevate your Software Development Career\Final Project\Final Project Code\CodeCraftHub"
Replace the path with the location of your project if necessary.

Check your current folder:

Get-Location
2. Create a virtual environment
A virtual environment keeps the project's Python packages separate from other Python projects.

Run:

python -m venv venv
This creates a folder named
venv
.

3. Activate the virtual environment
For PowerShell, run:

.\venv\Scripts\Activate.ps1
After activation, the terminal usually shows
(venv)
at the beginning of the command line.

Example:

(venv) PS D:\Study\...\CodeCraftHub>
If PowerShell blocks activation
You may receive an execution policy error. Open PowerShell as an administrator and run:

Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
Enter:

Y
Then return to the project terminal and run:

.\venv\Scripts\Activate.ps1
4. Install the dependencies
If the project contains a
requirements.txt
file, run:

pip install -r requirements.txt
If there is no
requirements.txt
file, install Flask:

pip install Flask
If the project uses SQLAlchemy, also install:

pip install Flask-SQLAlchemy
To see the installed packages, run:

pip list
Running the Application
1. Activate the virtual environment
If it is not already active, run:

.\venv\Scripts\Activate.ps1
2. Start the Flask application
Depending on the project entry file, use one of the following commands.

If the main file is called
app.py
:

python app.py
If the project uses Flask's command-line interface:

flask --app app run
The application should start at:

http://127.0.0.1:5000
Keep this terminal open while testing the API.

3. Check that the server is running
Open another VS Code terminal and run:

curl.exe -i -X GET "http://127.0.0.1:5000/api/courses"
A successful response should begin with:

HTTP/1.1 200 OK
The response may be:

[]
if there are no courses yet.

Understanding the API
The base URL for the API is:

http://127.0.0.1:5000
The course endpoints use this path:

/api/courses
The API uses the following HTTP methods:

Method	Purpose
GET
Read data
POST
Create data
PUT
Update data
DELETE
Delete data
Course Data Format
A course uses the following JSON structure:

{
  "name": "Flask REST APIs",
  "description": "Learn how to build REST APIs with Flask.",
  "target_date": "2026-12-31",
  "status": "Not Started"
}
Course fields
Field	Description
name
The name of the course
description
A description of the course
target_date
The planned completion date
status
The current progress status
The date should normally use this format:

YYYY-MM-DD
Example:

2026-12-31
Possible status values may include:

Not Started
In Progress
Completed
Use the values supported by your application.

API Endpoints
1. Get all courses
Endpoint
GET /api/courses
curl command
Run this in PowerShell:

curl.exe -i -X GET "http://127.0.0.1:5000/api/courses"
Successful response
HTTP/1.1 200 OK
Example response:

[
  {
    "id": 1,
    "name": "Flask REST APIs",
    "description": "Learn how to build REST APIs with Flask.",
    "target_date": "2026-12-31",
    "status": "Not Started"
  }
]
If no courses exist, the response may be:

[]
2. Get one course
Endpoint
GET /api/courses/<id>
Replace
<id>
with the course ID.

curl command
curl.exe -i -X GET "http://127.0.0.1:5000/api/courses/1"
Successful response
HTTP/1.1 200 OK
Example:

{
  "id": 1,
  "name": "Flask REST APIs",
  "description": "Learn how to build REST APIs with Flask.",
  "target_date": "2026-12-31",
  "status": "Not Started"
}
3. Create a course
Endpoint
POST /api/courses
The request must contain JSON data.

Recommended PowerShell method
PowerShell quotation marks can cause problems when JSON is written directly in a command. The safest method is to create a JSON file.

Step 1: Create
course-post.json
Run this command:

@'
{
  "name": "Flask REST APIs",
  "description": "Learn how to build REST APIs with Flask.",
  "target_date": "2026-12-31",
  "status": "Not Started"
}
'@ | Set-Content -Path ".\course-post.json" -Encoding utf8
Step 2: Check the file
Get-Content ".\course-post.json"
The file should contain:

{
  "name": "Flask REST APIs",
  "description": "Learn how to build REST APIs with Flask.",
  "target_date": "2026-12-31",
  "status": "Not Started"
}
Step 3: Send the POST request
curl.exe -i -X POST "http://127.0.0.1:5000/api/courses" -H "Content-Type: application/json" --data-binary "@.\course-post.json"
The important part is:

--data-binary "@.\course-post.json"
This tells
curl.exe
to read the JSON request body from the file.

Successful response
HTTP/1.1 201 CREATED
Example:

{
  "id": 1,
  "name": "Flask REST APIs",
  "description": "Learn how to build REST APIs with Flask.",
  "target_date": "2026-12-31",
  "status": "Not Started"
}
The returned
id
should be recorded for later requests.

Important JSON rule
Valid JSON must begin with
{
and end with
}
.

Correct:

{
  "name": "Flask REST APIs"
}
Incorrect:

"name": "Flask REST APIs"
Also, do not use this:

--data-raw json
That sends the literal word
json
, not a JSON object.

4. Update a course
Endpoint
PUT /api/courses/<id>
Replace
<id>
with the course ID.

Step 1: Create
course-put.json
@'
{
  "name": "Advanced Flask REST APIs",
  "description": "Build and test production-ready REST APIs with Flask.",
  "target_date": "2027-01-15",
  "status": "In Progress"
}
'@ | Set-Content -Path ".\course-put.json" -Encoding utf8
Step 2: Send the PUT request
For a course with ID
1
, run:

curl.exe -i -X PUT "http://127.0.0.1:5000/api/courses/1" -H "Content-Type: application/json" --data-binary "@.\course-put.json"
Replace
1
with the actual course ID.

Successful response
HTTP/1.1 200 OK
Example:

{
  "id": 1,
  "name": "Advanced Flask REST APIs",
  "description": "Build and test production-ready REST APIs with Flask.",
  "target_date": "2027-01-15",
  "status": "In Progress"
}
5. Delete a course
Endpoint
DELETE /api/courses/<id>
curl command
curl.exe -i -X DELETE "http://127.0.0.1:5000/api/courses/1"
Replace
1
with the ID of the course to delete.

Successful response
The application may return:

HTTP/1.1 200 OK
with a response such as:

{
  "message": "Course deleted successfully."
}
Some APIs return:

HTTP/1.1 204 NO CONTENT
A
204
response normally does not include a response body.

HTTP Status Codes
Status code	Meaning
200 OK
The request succeeded
201 CREATED
A new resource was created
204 NO CONTENT
The request succeeded without a response body
400 BAD REQUEST
The request contains invalid data
404 NOT FOUND
The requested course or endpoint does not exist
500 INTERNAL SERVER ERROR
An unexpected server error occurred
Testing the API
Test 1: Create a course
curl.exe -i -X POST "http://127.0.0.1:5000/api/courses" -H "Content-Type: application/json" --data-binary "@.\course-post.json"
Expected result:

HTTP/1.1 201 CREATED
Test 2: Get all courses
curl.exe -i -X GET "http://127.0.0.1:5000/api/courses"
Expected result:

HTTP/1.1 200 OK
Test 3: Get a specific course
curl.exe -i -X GET "http://127.0.0.1:5000/api/courses/1"
Expected result:

HTTP/1.1 200 OK
Test 4: Update a course
curl.exe -i -X PUT "http://127.0.0.1:5000/api/courses/1" -H "Content-Type: application/json" --data-binary "@.\course-put.json"
Expected result:

HTTP/1.1 200 OK
Test 5: Delete a course
curl.exe -i -X DELETE "http://127.0.0.1:5000/api/courses/1"
Expected result:

HTTP/1.1 200 OK
or:

HTTP/1.1 204 NO CONTENT
Error Testing
Invalid JSON
Create a file containing invalid JSON:

@'
{
  "name": "Invalid JSON"
'@ | Set-Content -Path ".\invalid-json.json" -Encoding utf8
Send it:

curl.exe -i -X POST "http://127.0.0.1:5000/api/courses" -H "Content-Type: application/json" --data-binary "@.\invalid-json.json"
Expected result:

HTTP/1.1 400 BAD REQUEST
Possible response:

{
  "error": "Request body must contain valid JSON."
}
Missing required fields
Create an empty JSON object:

'{}' | Set-Content -Path ".\missing-fields.json" -Encoding utf8
Send it:

curl.exe -i -X POST "http://127.0.0.1:5000/api/courses" -H "Content-Type: application/json" --data-binary "@.\missing-fields.json"
Expected result:

HTTP/1.1 400 BAD REQUEST
Invalid status
@'
{
  "name": "Flask REST APIs",
  "description": "Learn REST APIs.",
  "target_date": "2026-12-31",
  "status": "Unknown"
}
'@ | Set-Content -Path ".\invalid-status.json" -Encoding utf8
curl.exe -i -X POST "http://127.0.0.1:5000/api/courses" -H "Content-Type: application/json" --data-binary "@.\invalid-status.json"
Expected result:

HTTP/1.1 400 BAD REQUEST
Course not found
Use a course ID that does not exist:

curl.exe -i -X GET "http://127.0.0.1:5000/api/courses/9999"
Expected result:

HTTP/1.1 404 NOT FOUND
The same test can be performed for
PUT
:

curl.exe -i -X PUT "http://127.0.0.1:5000/api/courses/9999" -H "Content-Type: application/json" --data-binary "@.\course-put.json"
And
DELETE
:

curl.exe -i -X DELETE "http://127.0.0.1:5000/api/courses/9999"
Troubleshooting
Problem:
Request body must contain valid JSON
This usually means the request body is not valid JSON.

Make sure the JSON has:

An opening
{
A closing
}
Double quotes around property names
Double quotes around text values
Commas between properties
Correct:

{
  "name": "Flask REST APIs",
  "description": "Learn REST APIs.",
  "target_date": "2026-12-31",
  "status": "Not Started"
}
Incorrect:

"name":"Flask REST APIs"
The safest command is:

curl.exe -i -X POST "http://127.0.0.1:5000/api/courses" -H "Content-Type: application/json" --data-binary "@.\course-post.json"
Problem:
curl: Could not resolve host
This usually happens when JSON is not enclosed correctly and
curl.exe
treats words such as
REST
or
APIs
as separate command-line arguments.

Avoid placing complicated JSON directly into the command. Use a JSON file:

--data-binary "@.\course-post.json"
Problem:
curl: URL rejected: Malformed input
This is also commonly caused by incorrect quotation marks or braces in an inline JSON command.

Use the file-based method:

curl.exe -i -X POST "http://127.0.0.1:5000/api/courses" -H "Content-Type: application/json" --data-binary "@.\course-post.json"
Problem:
File not found
or the file cannot be read
Check whether the file exists:

Test-Path ".\course-post.json"
Expected result:

True
If the result is
False
, create the file again or use the full file path:

curl.exe -i -X POST "http://127.0.0.1:5000/api/courses" -H "Content-Type: application/json" --data-binary "@D:\path\to\course-post.json"
Problem:
404 NOT FOUND
when calling the API
Check the following:

The Flask application is running.
The URL is correct.
The endpoint is correct.
The port is correct.
The route includes
/api/courses
.
Correct:

http://127.0.0.1:5000/api/courses
Incorrect:

http://127.0.0.1:5000/courses
Problem:
Connection refused
This usually means that the Flask server is not running.

Start the application:

python app.py
Then try the request again.

Problem:
400 BAD REQUEST
Check:

The
Content-Type
header is present.
The JSON is valid.
Required fields are included.
The date uses
YYYY-MM-DD
.
The status value is supported.
The JSON file is the file you intended to send.
You can validate the JSON file with:

Get-Content ".\course-post.json" -Raw | ConvertFrom-Json
If this command finishes without an error, the JSON is valid.

Problem: PowerShell does not activate the virtual environment
Run:

Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
Then activate the environment again:

.\venv\Scripts\Activate.ps1
Project Structure
A typical CodeCraftHub project may have a structure similar to this:

CodeCraftHub/
│
├── app.py
├── requirements.txt
├── README.md
├── course-post.json
├── course-put.json
│
├── instance/
│   └── database.db
│
├── static/
│   ├── css/
│   └── js/
│
├── templates/
│   └── index.html
│
├── tests/
│   ├── test_courses.py
│   └── test_api.py
│
└── venv/
The exact structure may be different depending on the project implementation.

Important files and folders
app.py
This is usually the main Flask application file. It may contain:

Flask application setup
API routes
Database configuration
Request handling
Error handling
requirements.txt
This file lists the Python packages required by the project.

Install all dependencies with:

pip install -r requirements.txt
README.md
This documentation file explains how to install, run, and test the project.

instance/
This folder may contain the local SQLite database.

Do not manually edit the database unless you understand the database structure.

templates/
This folder contains HTML templates if the project includes a web interface.

static/
This folder contains static files such as:

CSS
JavaScript
Images
tests/
This folder contains automated tests for the application.

venv/
This is the Python virtual environment. It should generally not be committed to Git.

Basic REST API Concepts
Resource
A resource is an object managed by the API.

In CodeCraftHub, a course is a resource.

Example course URL:

/api/courses/1
Endpoint
An endpoint is a URL where the API can be accessed.

Example:

/api/courses
Request
A request is sent from a client to the server.

For example, a
POST
request sends a new course to the API.

Response
A response is sent from the server back to the client.

It usually includes:

An HTTP status code
A response body
JSON data
JSON
JSON is a common format for sending data between applications.

Example:

{
  "name": "Flask REST APIs",
  "status": "Not Started"
}
Typical Test Workflow
Use the following order when testing CodeCraftHub:

Start the Flask application.
Create a course with
POST
.
Copy the returned course ID.
Get all courses with
GET
.
Get the individual course with
GET /api/courses/<id>
.
Update the course with
PUT
.
Test invalid data.
Delete the course with
DELETE
.
Request the deleted course.
Confirm that the API returns
404 NOT FOUND
.
Stopping the Application
To stop the Flask server, click the terminal where it is running and press:

Ctrl + C
Summary
CodeCraftHub is a Flask REST API for managing courses.

The main endpoints are:

GET     /api/courses
POST    /api/courses
GET     /api/courses/<id>
PUT     /api/courses/<id>
DELETE  /api/courses/<id>
For PowerShell testing, use
curl.exe
and send JSON files with:

--data-binary "@.\filename.json"
This avoids common quotation and JSON formatting problems when working in the VS Code terminal.

undefined