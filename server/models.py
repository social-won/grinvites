from typing import List, Literal

from pydantic import BaseModel


class User(BaseModel):
      id: str                          # Supabase UUID
      email: str
      display_name: str | None = None
      invite_times: dict[str, str] = {}  # {"Mon": "08:00", "Tues": "12:00"}


class Interest(BaseModel):
    id: int
    name: str
    type: str                        # "academic" | "athletics" | "club" | "department"

class Event(BaseModel):
    id: int
    title: str
    org_name: str | None = None
    description: str | None = None
    start_time: str                  # ISO datetime
    end_time: str | None = None
    location: str | None = None
    frequency: str | None = None

class Interests(BaseModel):
    id: int
    name: str
    type: str

class UserInterestsUpdate(BaseModel):
    interest_ids: List[int]