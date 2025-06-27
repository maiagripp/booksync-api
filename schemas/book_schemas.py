from pydantic import BaseModel

class ReviewInput(BaseModel):
    rating: int
    comment: str
    status: str

class StatusInput(BaseModel):
    status: str
