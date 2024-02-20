Note-taking application is a RESTful API built using Django Rest Framework. This API allows user to perform CRUD operations on notes along with note sharing functionality and tracking version history. It utilizes SQLite as database for storing data. 

## Installation

1. Clone the repository:

git clone "https://github.com/muskan484/notes_application_drf",

2. Commands to run the project
    - python3 -m venv <ENV_NAME>
    - source <ENV_NAME>/bin/activate
    - pip3 install -r requirements.txt
    - Migrations for database 
        python3 manage.py makemigrations
        python3 manage.py migrate  
    - Start the development server:
        python3 manage.py runserver

## Models

### User Model

- username: CharField, stores the unique username of the user.
- email: EmailField, unique email address of the user.
- password: CharField, stores the password of the user.

### Note Model

- content: TextField (required) - Stores the textual content of the note.
- owner: ForeignKey to User model (required) - Represents the user who owns the note.
- shared_users: ManyToManyField to User model - Represents users with whom the note is shared.

### NoteHistory Model

- note: ForeignKey to Note model (required) - Represents the note to which the history entry belongs.
- user: ForeignKey to User model (required) - Represents the user who made the change.
- created_at: DateTimeField (auto-generated) - Represents the date and time when the history entry was created.
- updated_at: DateTimeField (auto-generated) - Represents the date and time when the history entry was last updated.
- timestamp: DateTimeField (auto-generated) - Represents the timestamp of the change.
- change: TextField - Stores the details of the change made to the note.


## API endpoints

1. /signup

    This endpoint is used to create new user
    Methods: POST
    Request Body : 
    ```
    {
        'username' : '',
        'email_id' : '',
        'password' : ''
    }
    ```

2. /login

    This endpoint is used to login to the user account
    Methods: POST
    Request Body:
        ```
        {
            "username": '',
            "password": ''
        }
        ```

    
3. /notes/create
    This endpoint is used to create note
    Methods: POST
    Request Body:
        ```
        {
            "content": ""
        }
        ```

4. /notes/{id}
    This endpoint is used to get, update, delete the specific note
    Methods: GET, PUT, DELETE
    Request Body:
    ```
    {
        "content":""
    }
    ```

5. /notes/share
    This endpoint is used to share the notes with other user
    Method: POST
    Request Body:
    ```
    {
        "note_id":""
        "shared_users":["",""]
    }
    ```

6. /notes/version-history/{id}
    This endpoint is used to get the version history of note
    Method: GET

## Authentication

- Authentication in the project is implemented using JSON Web Tokens (JWT). JWT provides secure access to users' accounts and resources by generating a token upon successful authentication. This token is then used to authorize and authenticate subsequent requests made by the user on any notes endpoint.

