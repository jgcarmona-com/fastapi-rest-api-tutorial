# constants.py

TITLE = "Custom FastAPI REST API"
DESCRIPTION = """
Welcome to the Custom FastAPI REST API documentation!

This API provides endpoints for managing questions, answers, and comments in a Q&A system. You can use this API to create, retrieve, update, and delete records. The main features include:

- **Questions Management**: Create a question, retrieve a list of questions, get details of a specific question by its ID, and delete questions.
- **Answers Management**: Post an answer to a specific question, retrieve all answers for a given question, get details of a specific answer, and delete answers.
- **Comments Management**: Add comments to answers, retrieve all comments for a given answer, and delete comments.

### Authentication
Currently, this API does not require authentication. In a production environment, you would typically secure these endpoints with authentication and authorization mechanisms.

### Error Handling
The API provides meaningful error messages and HTTP status codes to help you understand what went wrong. Common status codes include:
- **200 OK**: The request was successful.
- **201 Created**: A new resource was successfully created.
- **400 Bad Request**: The request was invalid or cannot be otherwise served.
- **404 Not Found**: The requested resource could not be found.
- **422 Unprocessable Entity**: The request was well-formed but was unable to be followed due to semantic errors, such as validation errors in the request body.
- **500 Internal Server Error**: An error occurred on the server.

Explore the endpoints below to see how you can integrate our API into your application. Happy coding!
"""
CONTACT = {
    "name": "Juan G Carmona",
    "url": "http://jgcarmona.com/contact",
    "email": "juan@jgcarmona.com",
}
LICENSE_INFO = {
    "name": "MIT",
    "url": "https://opensource.org/licenses/MIT",
}
SWAGGER_UI_PARAMETERS = {"syntaxHighlight.theme": "obsidian"}
SWAGGER_FAVICON_URL = "https://example.com/your-favicon.ico" 
