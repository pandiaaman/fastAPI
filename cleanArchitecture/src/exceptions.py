from fastapi import HTTPException, status

class AuthenticationError(HTTPException):
    def __init__(self, detail: str = "Invalid credentials"):
        super().__init__(status_code=status.HTTP_401_UNAUTHORIZED, detail=detail)

class UserNotFoundError(HTTPException):
    def __init__(self, user_id):
        detail = f"User with ID '{user_id}' not found"
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=detail)