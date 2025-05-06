from sqlalchemy.orm import Session
from .models import User

def get_users(db: Session, of: int = 0, limit: int = 10, name: str = None):
    base_query = db.query(User)
    
    if name:
        base_query = base_query.filter(User.firstname.ilike(f"%{name}%"))

    total_count = base_query.count() #count
    filtered_count = base_query.count()  # total rows after filter

    users = base_query.offset(of).limit(limit).all()

    return {
        "total_count": total_count,
        "filtered_count": filtered_count,
        "page_size": limit,
        "page_number": (of // limit) + 1,
        "users": users
    }
