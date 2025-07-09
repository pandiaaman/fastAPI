from fastapi import HTTPException, status

class AuthenticationError(HTTPException):
    def __init__(self, detail: str = "Invalid credentials"):
        super().__init__(status_code=status.HTTP_401_UNAUTHORIZED, detail=detail)

class UserNotFoundError(HTTPException):
    def __init__(self, user_id):
        detail = f"User with ID '{user_id}' not found"
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=detail)

class TodoCreationError(HTTPException):
    def __init__(self, detail: str = "Failed to create todo"):
        super().__init__(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=detail)

class TodoNotFoundError(HTTPException):
    def __init__(self, todo_id):
        detail = f"Todo with ID '{todo_id}' not found"
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=detail)