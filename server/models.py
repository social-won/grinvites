from pydantic import BaseModel


class User(BaseModel):
      id: str                          # Supabase UUID
      email: str
      display_name: str
      invite_times: dict[str, str] = {}  # {"Mon": "08:00", "Tues": "12:00"}
      theme: str | None = None         # "light" | "dark" | "system"
      events_emailed: str | None = None  # JSON string of list of event IDs that have been emailed to the user


class Interest(BaseModel):
    id: int
    name: str
    type: str                           # "organization"
    # "academic" | "athletics" | "club" | "department"
    groups: list[str]


class Organization(BaseModel):
    name: str
    original_name: str
    formatted_name: str
    groups: list[str]
    has_comma: bool


class Event(BaseModel):
    id: int
    event_id: str
    title: str
    creation_time_stamp: str
    start_time: str                  # ISO datetime
    end_time: str | None = None
    location: str | None = None
    summary: str | None = None
    categories: str | None = None
    tags: str | None = None
    org_name: str | None = None
    occurances: str | None = None
    frequency: str | None = None


class UserInterestsUpdate(BaseModel):
    interest_ids: list[int]

class UserUpdate(BaseModel):
    email: str | None = None
    display_name: str | None = None
    invite_times: dict[str, str] | None = None
    theme: str | None = None