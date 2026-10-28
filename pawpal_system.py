from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional


@dataclass
class Pet:
    id: str
    name: str
    species: str
    age: int
    needs: List[str] = field(default_factory=list)
    notes: Optional[str] = None

    def get_needs(self) -> List[str]:
        return self.needs

    def add_need(self, need: str) -> None:
        if need not in self.needs:
            self.needs.append(need)


@dataclass
class Owner:
    id: str
    name: str
    contact_info: str
    preferred_time_windows: List[str] = field(default_factory=list)
    priority: int = 0
    pets: List[Pet] = field(default_factory=list)

    def add_pet(self, pet: Pet) -> None:
        if pet not in self.pets:
            self.pets.append(pet)

    def remove_pet(self, pet_id: str) -> None:
        self.pets = [pet for pet in self.pets if pet.id != pet_id]

    def create_request(self, service_type: str, pet_id: str, preferred_window: str) -> "ServiceRequest":
        return ServiceRequest(
            id=f"req-{datetime.utcnow().strftime('%Y%m%d%H%M%S')}",
            owner_id=self.id,
            pet_id=pet_id,
            service_type=service_type,
            preferred_window=preferred_window,
            duration_minutes=60,
            is_emergency=False,
            status="pending",
        )


@dataclass
class ServiceRequest:
    id: str
    owner_id: str
    pet_id: str
    service_type: str
    preferred_window: str
    duration_minutes: int
    is_emergency: bool = False
    status: str = "pending"

    def validate(self) -> bool:
        return bool(self.owner_id and self.pet_id and self.service_type and self.preferred_window)

    def mark_scheduled(self) -> None:
        self.status = "scheduled"

    def cancel(self) -> None:
        self.status = "cancelled"


@dataclass
class Scheduler:
    requests: List[ServiceRequest] = field(default_factory=list)
    business_hours: List[str] = field(default_factory=list)

    def schedule(self, requests: Optional[List[ServiceRequest]] = None) -> List[ServiceRequest]:
        if requests is not None:
            self.requests = requests

        for request in self.requests:
            if request.status == "pending":
                request.mark_scheduled()

        return self.requests

    def find_feasible_slots(self, request: ServiceRequest) -> List[str]:
        return self.business_hours if self.business_hours else [request.preferred_window]

    def assign(self, request: ServiceRequest, slot: str) -> bool:
        if slot not in self.find_feasible_slots(request):
            return False
        request.status = "scheduled"
        request.preferred_window = slot
        return True

    def notify_owner(self, owner_id: str, message: str) -> str:
        return f"Owner {owner_id}: {message}"
