from pydantic import BaseModel
from typing import List

class User(BaseModel):
    id: int
    firstname: str
    lastname: str
    email: str
    phone: str

    class Config:
        from_attributes = True

class paginated_user_response(BaseModel):  
    total_count: int
    filtered_count: int
    page_size: int
    page_number: int
    users: List[User]

    class Config:
        from_attributes = True
