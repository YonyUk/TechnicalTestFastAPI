from pydantic import BaseModel, EmailStr

# User schema
class UserBase(BaseModel):
    username: str
    email: EmailStr

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: str
    
    class Config:
        orm_mode = True