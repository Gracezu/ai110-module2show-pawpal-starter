from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, List, Optional


@dataclass
class Task:
    task_id: str
    title: str
    description: Optional[str] = None
    due_date: Optional[datetime] = None
    completed: bool = False

    def mark_complete(self) -> None:
        pass

    def postpone(self, new_due_date: datetime) -> None:
        pass


@dataclass
class User:
    user_id: str
    email: str
    password: str
    caregiver_role: str
    pets: List[Pet] = field(default_factory=list)

    def add_pet(self, pet: Pet) -> None:
        pass

    def invite_caregiver(self, caregiver_email: str) -> None:
        pass


@dataclass
class Pet:
    pet_id: str
    name: str
    breed: str
    weight: float
    age: int
    feedings: List[Feeding] = field(default_factory=list)
    walks: List[Walk] = field(default_factory=list)
    medications: List[Medication] = field(default_factory=list)
    appointments: List[Appointment] = field(default_factory=list)

    def update_profile(self) -> None:
        pass

    def generate_health_report(self) -> None:
        pass


@dataclass
class Feeding:
    feeding_id: str
    food_type: str
    portion_size: str
    scheduled_time: datetime
    is_completed: bool = False
    completed_by: Optional[str] = None

    def schedule_feeding(self) -> None:
        pass

    def mark_as_fed(self) -> None:
        pass

    def send_reminder(self) -> None:
        pass

    def update_portion(self, portion_size: str) -> None:
        pass

    def log_skipped_meal(self) -> None:
        pass


@dataclass
class Walk:
    walk_id: str
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    distance: float = 0.0
    gps_route: List[Any] = field(default_factory=list)
    potty_breaks: int = 0

    def start_walk(self) -> None:
        pass

    def end_walk(self) -> None:
        pass

    def log_potty(self) -> None:
        pass

    def calculate_duration(self) -> None:
        pass

    def share_walk_report(self) -> None:
        pass


@dataclass
class Medication:
    medication_id: str
    med_name: str
    dosage: str
    frequency: str
    instructions: str
    inventory_count: int

    def administer_dose(self) -> None:
        pass

    def schedule_next_dose(self) -> None:
        pass

    def check_refill_status(self) -> None:
        pass

    def trigger_refill_alert(self) -> None:
        pass

    def skip_dose(self) -> None:
        pass


@dataclass
class Appointment:
    appointment_id: str
    provider_name: str
    date_time: datetime
    location: str
    reason: str
    notes: Optional[str] = None

    def create_appointment(self) -> None:
        pass

    def reschedule(self, new_date_time: datetime) -> None:
        pass

    def cancel_appointment(self) -> None:
        pass

    def send_reminder(self) -> None:
        pass

    def attach_document(self, document: Any) -> None:
        pass
