from typing import Optional
import re

from pydantic import BaseModel, EmailStr
from enum import Enum


class UserTypeEnum(str, Enum):
    employee = "employee"
    employer = "employer"


class UserLoginFormData(BaseModel):
    email: EmailStr
    password: str


class UserRegisterFormData(BaseModel):
    email: EmailStr
    password: str
    user_type: UserTypeEnum
    

class RefreshTokenFormData(BaseModel):
    refresh_token: str


class UserChangePasswordFormData(BaseModel):
    current_password: str
    new_password: str
