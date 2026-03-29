from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List, Optional


@dataclass
class Task:
    task_id: str
    title: str
    description: Optional[str] = None
    due_date: Optional[datetime] = None
    frequency: Optional[str] = None
    completed: bool = False
    created_at: datetime = field(default_factory=datetime.utcnow)
    notes: Optional[str] = None

    def mark_complete(self) -> None:
        self.completed = True

    def postpone(self, new_due_date: datetime) -> None:
        if new_due_date <= datetime.utcnow():
            raise ValueError("new_due_date must be in the future")
        self.due_date = new_due_date

    def is_overdue(self) -> bool:
        return bool(self.due_date and not self.completed and self.due_date < datetime.utcnow())


@dataclass
class Pet:
    pet_id: str
    name: str
    breed: str
    weight: float
    age: int
    owner: Optional[Owner] = None
    tasks: List[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        self.tasks.append(task)

    def remove_task(self, task_id: str) -> None:
        self.tasks = [task for task in self.tasks if task.task_id != task_id]

    def get_tasks(self, completed: Optional[bool] = None) -> List[Task]:
        if completed is None:
            return list(self.tasks)
        return [task for task in self.tasks if task.completed == completed]

    def get_overdue_tasks(self) -> List[Task]:
        return [task for task in self.tasks if task.is_overdue()]

    def update_profile(
        self,
        name: Optional[str] = None,
        breed: Optional[str] = None,
        weight: Optional[float] = None,
        age: Optional[int] = None,
    ) -> None:
        if name is not None:
            self.name = name
        if breed is not None:
            self.breed = breed
        if weight is not None:
            self.weight = weight
        if age is not None:
            self.age = age

    def generate_health_report(self) -> Dict[str, Any]:
        return {
            "pet_id": self.pet_id,
            "name": self.name,
            "breed": self.breed,
            "weight": self.weight,
            "age": self.age,
            "task_count": len(self.tasks),
            "overdue_tasks": len(self.get_overdue_tasks()),
        }


@dataclass
class Owner:
    owner_id: str
    email: str
    password: str
    caregiver_role: str
    pets: List[Pet] = field(default_factory=list)

    def add_pet(self, pet: Pet) -> None:
        pet.owner = self
        self.pets.append(pet)

    def remove_pet(self, pet_id: str) -> None:
        self.pets = [pet for pet in self.pets if pet.pet_id != pet_id]

    def get_all_tasks(self, completed: Optional[bool] = None) -> List[Task]:
        all_tasks: List[Task] = []
        for pet in self.pets:
            all_tasks.extend(pet.get_tasks(completed=completed))
        return all_tasks

    def find_pet(self, pet_id: str) -> Optional[Pet]:
        for pet in self.pets:
            if pet.pet_id == pet_id:
                return pet
        return None

    def invite_caregiver(self, caregiver_email: str) -> None:
        # placeholder for invite workflow
        pass


class Scheduler:
    def __init__(self, owners: Optional[List[Owner]] = None) -> None:
        self.owners: List[Owner] = owners or []

    def register_owner(self, owner: Owner) -> None:
        self.owners.append(owner)

    def get_tasks_for_owner(self, owner_id: str, completed: Optional[bool] = None) -> List[Task]:
        owner = self._find_owner(owner_id)
        if not owner:
            return []
        return owner.get_all_tasks(completed=completed)

    def get_tasks_for_pet(self, pet_id: str, completed: Optional[bool] = None) -> List[Task]:
        for owner in self.owners:
            pet = owner.find_pet(pet_id)
            if pet:
                return pet.get_tasks(completed=completed)
        return []

    def organize_tasks_by_due_date(self, tasks: List[Task]) -> List[Task]:
        return sorted(tasks, key=lambda task: task.due_date or datetime.max)

    def get_overdue_tasks(self) -> List[Task]:
        overdue_tasks: List[Task] = []
        for owner in self.owners:
            overdue_tasks.extend(owner.get_all_tasks())
        return [task for task in overdue_tasks if task.is_overdue()]

    def schedule_task(self, pet_id: str, task: Task) -> None:
        for owner in self.owners:
            pet = owner.find_pet(pet_id)
            if pet:
                pet.add_task(task)
                return
        raise ValueError(f"No pet found with id {pet_id}")

    def reschedule_task(self, task_id: str, new_due_date: datetime) -> None:
        task = self._find_task_by_id(task_id)
        if task is None:
            raise ValueError(f"Task {task_id} not found")
        task.postpone(new_due_date)

    def cancel_task(self, task_id: str) -> None:
        for owner in self.owners:
            for pet in owner.pets:
                if any(task.task_id == task_id for task in pet.tasks):
                    pet.remove_task(task_id)
                    return
        raise ValueError(f"Task {task_id} not found")

    def _find_owner(self, owner_id: str) -> Optional[Owner]:
        for owner in self.owners:
            if owner.owner_id == owner_id:
                return owner
        return None

    def _find_task_by_id(self, task_id: str) -> Optional[Task]:
        for owner in self.owners:
            for pet in owner.pets:
                for task in pet.tasks:
                    if task.task_id == task_id:
                        return task
        return None
