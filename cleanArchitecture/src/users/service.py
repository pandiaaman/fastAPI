from uuid import UUID
from sqlalchemy.orm import Session
from fastapi import HTTPException
from . import model
from src.entities.user import User
from src.exceptions import UserNotFoundError
from src.auth.service import verify_password, get_password_hash
import logging

def get_user_by_id(db:Session, user_id:UUID|None) -> model.UserResponse:
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        logging.warning(f"User not found with ID: {user_id}")
        raise UserNotFoundError(user_id)
    logging.info(f"Successfully retrieved the user with ID: {user_id}")
    return user

# WE can implement change password feature later on. 
# def change_password(db:Session, user_id:UUID, password_change:model.PasswordChange) -> None:
#     try:
#         user = get_user_by_id(db, user_id)
#         # verify current password
#         if not verify_password(password_change.current_password, user.password_hash)
#         logging.warning(f"Invalid current password provided for user id : {user_id}")
#         raise InvalidPasswordError()
    
