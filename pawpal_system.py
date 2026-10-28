from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional


@dataclass
class Task:
    """Represents a single pet-care activity."""

    description: str
    time: str
    frequency: str = "once"
    completed: bool = False

    def mark_complete(self) -> None:
        """Mark the task as complete."""
        self.completed = True

    def mark_incomplete(self) -> None:
        """Mark the task as incomplete."""
        self.completed = False

    def __str__(self) -> str:
        """Return a readable terminal string for the task."""
        status = "Done" if self.completed else "Pending"
        return f"{self.time} - {self.description} ({self.frequency}) [{status}]"

@dataclass
class Pet:
    """Stores pet details and the tasks assigned to that pet."""

    id: str
    name: str
    species: str
    tasks: List[Task] = field(default_factory=list)
    notes: Optional[str] = None
    owner_id: Optional[str] = None

    def add_task(self, task: Task) -> None:
        """Add a task to this pet."""
        self.tasks.append(task)

    def get_tasks(self) -> List[Task]:
        """Return all tasks assigned to this pet."""
        return self.tasks

    def complete_task(self, description: str) -> bool:
        """Mark the matching task complete and return whether it was found."""
        for task in self.tasks:
            if task.description.lower() == description.lower():
                task.mark_complete()
                return True
        return False

    def __str__(self) -> str:
        """Return a readable summary of the pet."""
        return f"{self.name} ({self.species})"

@dataclass
class Owner:
    """Manages multiple pets and provides access to all their tasks."""

    id: str
    name: str
    pets: List[Pet] = field(default_factory=list)

    def add_pet(self, pet: Pet) -> None:
        """Add a pet to the owner and link it to the owner."""
        pet.owner_id = self.id
        if pet not in self.pets:
            self.pets.append(pet)

    def remove_pet(self, pet_id: str) -> None:
        """Remove a pet by ID from the owner's collection."""
        self.pets = [pet for pet in self.pets if pet.id != pet_id]

    def get_all_tasks(self) -> List[Task]:
        """Collect every task across all pets owned by this owner."""
        all_tasks: List[Task] = []
        for pet in self.pets:
            all_tasks.extend(pet.tasks)
        return all_tasks

    def __str__(self) -> str:
        """Return a readable owner summary."""
        return f"{self.name} ({len(self.pets)} pets)"

@dataclass
class ServiceRequest:
    id: str
    owner_id: str
    pet_id: str
    service_type: str
    preferred_window: str
    duration_minutes: int
    is_emergency: bool = False
    priority: int = 0
    assigned_slot: Optional[str] = None
    status: str = "pending"

    def validate(self) -> bool:
        return bool(self.owner_id and self.pet_id and self.service_type and self.preferred_window)

    def mark_scheduled(self) -> None:
        self.status = "scheduled"

    def cancel(self) -> None:
        self.status = "cancelled"

@dataclass
class Scheduler:
    """Retrieves, organizes, and manages tasks across the owner's pets."""

    owner: Optional[Owner] = None
    requests: List[ServiceRequest] = field(default_factory=list)
    business_hours: List[str] = field(default_factory=list)
    scheduled_slots: List[str] = field(default_factory=list)

    def set_owner(self, owner: Owner) -> None:
        """Set the owner whose pets should be scheduled."""
        self.owner = owner

    def get_all_tasks(self) -> List[Task]:
        """Return all scheduled tasks from the owner’s pets."""
        if self.owner is None:
            return []
        return self.owner.get_all_tasks()

    def organize_tasks(self) -> List[Task]:
        """Sort tasks by time so they can be displayed in a plan."""
        tasks = self.get_all_tasks()
        return sorted(tasks, key=lambda task: task.time)

    def get_today_schedule(self) -> List[Task]:
        """Return the ordered schedule for the day."""
        return self.organize_tasks()

    def print_schedule(self) -> str:
        """Return a readable schedule string for the terminal."""
        if self.owner is None:
            return "No owner assigned."

        lines = ["Today's Schedule:"]
        tasks = self.get_today_schedule()
        if not tasks:
            lines.append("- No tasks scheduled.")
            return "\n".join(lines)

        for task in tasks:
            pet = next((pet for pet in self.owner.pets if task in pet.tasks), None)
            pet_label = pet.name if pet else "Unknown pet"
            status = "Done" if task.completed else "Pending"
            lines.append(f"- {task.time} | {pet_label} | {task.description} | {status}")
        return "\n".join(lines)

    def check_conflict(self, slot: str) -> bool:
        return slot in self.scheduled_slots

    def schedule(self, requests: Optional[List[ServiceRequest]] = None) -> List[ServiceRequest]:
        if requests is not None:
            self.requests = requests

        ordered = sorted(
            self.requests,
            key=lambda r: (0 if r.is_emergency else 1, -r.priority, r.preferred_window),
        )

        for request in ordered:
            if request.status == "pending":
                if self.check_conflict(request.preferred_window):
                    request.status = "waiting"
                    continue
                request.assigned_slot = request.preferred_window
                request.mark_scheduled()
                self.scheduled_slots.append(request.preferred_window)

        return self.requests

    def find_feasible_slots(self, request: ServiceRequest) -> List[str]:
        return self.business_hours if self.business_hours else [request.preferred_window]

    def assign(self, request: ServiceRequest, slot: str) -> bool:
        if slot not in self.find_feasible_slots(request) or self.check_conflict(slot):
            return False
        request.status = "scheduled"
        request.assigned_slot = slot
        request.preferred_window = slot
        self.scheduled_slots.append(slot)
        return True

    def notify_owner(self, owner_id: str, message: str) -> str:
        return f"Owner {owner_id}: {message}"
