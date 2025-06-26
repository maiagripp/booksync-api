from pydantic import BaseModel, EmailStr, Field

class UserInput(BaseModel):
    email: EmailStr = Field(..., example="usuario@exemplo.com")
    password: str = Field(..., example="senha123")


