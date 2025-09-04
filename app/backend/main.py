from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import uvicorn
import json

app = FastAPI(title="Kitaverse Backend")

# Add CORS middleware to allow browser connections
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Data models
class Space(BaseModel):
    id: int
    name: str
    type: str  # meeting, market, festival
    description: str
    capacity: int = 50
    current_users: int = 0

class User(BaseModel):
    id: int
    name: str
    position: dict = {"x": 0, "y": 0, "z": 0}
    space_id: Optional[int] = None

# In-memory storage (in production, use a database)
spaces = [
    Space(
        id=1,
        name="Community Center",
        type="meeting",
        description="A place for village meetings and discussions",
        capacity=30
    ),
    Space(
        id=2,
        name="Village Market",
        type="market",
        description="Buy and sell goods with other villagers",
        capacity=100
    ),
    Space(
        id=3,
        name="Festival Grounds",
        type="festival",
        description="Celebrate festivals and cultural events",
        capacity=200
    )
]

users = []

@app.get("/")
async def root():
    return {"message": "Welcome to Kitaverse Backend", "version": "1.0.0"}

@app.get("/spaces")
async def get_spaces():
    """Return available virtual public spaces"""
    return {"spaces": spaces}

@app.get("/spaces/{space_id}")
async def get_space(space_id: int):
    """Return details about a specific space"""
    for space in spaces:
        if space.id == space_id:
            return space
    raise HTTPException(status_code=404, detail="Space not found")

@app.post("/spaces/{space_id}/enter")
async def enter_space(space_id: int, user: User):
    """Allow a user to enter a space"""
    # Check if space exists
    space = None
    for s in spaces:
        if s.id == space_id:
            space = s
            break
    
    if not space:
        raise HTTPException(status_code=404, detail="Space not found")
    
    # Check if space is full
    if space.current_users >= space.capacity:
        raise HTTPException(status_code=400, detail="Space is full")
    
    # Add user to space
    user.space_id = space_id
    space.current_users += 1
    
    # Add user to users list if not already there
    existing_user = next((u for u in users if u.id == user.id), None)
    if not existing_user:
        users.append(user)
    else:
        existing_user.space_id = space_id
        existing_user.position = user.position
    
    return {"message": f"User {user.name} entered {space.name}", "space": space}

@app.post("/spaces/{space_id}/leave")
async def leave_space(space_id: int, user_id: int):
    """Allow a user to leave a space"""
    # Find the space
    space = None
    for s in spaces:
        if s.id == space_id:
            space = s
            break
    
    if not space:
        raise HTTPException(status_code=404, detail="Space not found")
    
    # Find the user
    user = None
    for u in users:
        if u.id == user_id:
            user = u
            break
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Remove user from space
    if user.space_id == space_id:
        user.space_id = None
        space.current_users -= 1
        return {"message": f"User {user.name} left {space.name}", "space": space}
    else:
        raise HTTPException(status_code=400, detail="User is not in this space")

@app.get("/spaces/{space_id}/users")
async def get_space_users(space_id: int):
    """Get all users in a specific space"""
    # Check if space exists
    space_exists = any(s.id == space_id for s in spaces)
    if not space_exists:
        raise HTTPException(status_code=404, detail="Space not found")
    
    # Get users in this space
    space_users = [u for u in users if u.space_id == space_id]
    return {"users": space_users}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)