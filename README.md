# Bug Tracker API
Welcome to the Bug Tracker API documentation! This API provides endpoints for managing users, projects, and bugs, allowing you to efficiently track and manage software bugs. 

## Technology Used: 
1. FastAPI (Framework)
2. MongoDB (Database)
3. Beanie (ODM)

## Authentication
Routes /dashboard, /projects, and /bugs are protected by JWT token authentication. Include a valid JWT token in the headers of your request to access these routes.

## Routes 
### Users
**prefix: /users**
| HTTP Method	| Route     | Details   |
|  :---         | :---      | :---      | 
| POST          | /signup   | create a new user account
| POST          | /access-token   | Obtain an access token
| GET          | /dashboard   | Retriever user dashboard information

### Projects
**prefix: /projects**
| HTTP Method	| Route     | Details   |
|  :---         | :---      | :---      | 
| POST          | /create   | create a new project
| GET          | /   | Retrieve a list of projects
| GET          | /{project_id}   | Retrieve project details
| DELETE          | /{project_id}   | Delete a project
| PUT          | /{project_id}   | Update project details

### Bugs
**prefix: /bugs**
| HTTP Method	| Route     | Details   |
|  :---         | :---      | :---      | 
| POST          | /create   | create a new bug
| GET          | /projects/{bug_id}   | Retrieve a list of bugs for given project id
| GET          | /{bug_id}   | Retrieve bug details
| DELETE          | /{bug_id}   | Delete a bug
| PUT          | /{project_id}   | Update bug details

