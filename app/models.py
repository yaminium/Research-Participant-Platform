import reflex as rx
from typing import TypedDict, Optional


class User(TypedDict):
    id: str
    email: str
    password_hash: str
    name: str
    role: str
    bookmarks: list[str]
    created_at: str


class Study(TypedDict):
    id: str
    researcher_id: str
    title: str
    description: str
    study_image: str
    experiment_type: str
    sample_size: int
    compensation: str
    participant_criteria: str
    psychological_health_type: str
    age_range_min: int
    age_range_max: int
    gender_requirement: str
    custom_criteria: str
    procedure_description: str
    location_type: str
    physical_location: str
    duration: str
    contact_info: str
    status: str
    created_at: str


class Application(TypedDict):
    id: str
    study_id: str
    participant_id: str
    participant_name: str
    age: int
    gender: str
    email: str
    phone: str
    motivation_message: str
    status: str
    created_at: str