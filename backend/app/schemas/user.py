from pydantic import BaseModel, ConfigDict, EmailStr, Field


class UserBase(BaseModel):
    email: EmailStr
    username: str = Field(min_length=3, max_length=40)


class UserCreate(UserBase):
    """Self-registration. There is deliberately no is_admin field: nobody can make themselves an admin."""

    password: str = Field(min_length=8, max_length=128)


class AdminUserCreate(UserCreate):
    """Used only by the admin-protected endpoint."""

    is_admin: bool = False


class UserResponse(UserBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    is_admin: bool
