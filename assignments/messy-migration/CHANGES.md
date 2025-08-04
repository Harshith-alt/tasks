**Major Issues in Original Code:**

When I first looked at codebase, I noticed few issues:

- Everything was inside one file app.py file, mixing routes and database access including logic.
- SQL queries were written directly inserting user input into string.
- There was no input validation or checking.
- No proper error handling or status codes.Response has been returned as raw strings, Not JSON.

**What I have changed:**

# Structure and readability

I have restructured the entire app.py file to multiple clean files:

app.py - entry point
routes/ - split into users.py and auth.py
db.py - handles the database connection

# Security fixes

Replaced all SQL queries with parameterized queries to prevent SQL injection.
Added basic validation.(checking name,email and password).

# Error Handling & Status codes

Appropriate HTTP codes : 201 for created,
404 for not found, 400 for bad request.
Returns errors in JSON format , so the structured response is given.

**Trade offs and assumptions**

Continued using SQLite for simplicity.
Chose 'bcrypt' for the passwords hashing.

**AI Usage Acknowledgement**

Tools used: ChatGPT.
It is used for:

- Guidance on Flask best practices and bcrypt integration.
- Writing code and cleaning error handling.

Name: M Harshith Kumar
Task1 User Management API
