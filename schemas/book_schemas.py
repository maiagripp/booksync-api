from pydantic import BaseModel, Field

class ReviewInput(BaseModel):
    rating: int
    comment: str
    status: str = "lendo"

class StatusInput(BaseModel):
    status: str
    
class SearchQuery(BaseModel):
    query: str
    
class PathGoogleID(BaseModel):
    google_id: str = Field(..., description="ID do livro no Google Books")