"""
PawPal+ System - Backend Logic Layer
This module contains all the core classes for the pet care scheduling system.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List


@dataclass
class Task:
    """Represents a single pet care activity."""
    description: str
    duration: int
    frequency: str
    completed: bool = False
    priority: int = 1

    def get_duration(self) -> int:
        """Return the task duration in minutes."""
        return self.duration

    def get_priority(self) -> int:
        """Return the task priority."""
        return self.priority

    def mark_complete(self) -> None:
        """Mark the task as completed."""
        self.completed = True


@dataclass
class Pet:
    """Represents a pet that needs care."""
    name: str
    type: str
    age: int
    tasks: List[Task] = field(default_factory=list)

    def get_info(self) -> str:
        """Return a formatted summary of the pet."""
        return f"{self.name} is a {self.age}-year-old {self.type}."

    def add_task(self, task: Task) -> None:
        """Add a care task to this pet."""
        self.tasks.append(task)

    def get_tasks(self) -> List[Task]:
        """Return all tasks assigned to this pet."""
        return self.tasks


@dataclass
class Owner:
    """Represents the pet owner with time constraints and preferences."""
    name: str
    available_time: int
    preferences: Dict = field(default_factory=dict)
    pets: List[Pet] = field(default_factory=list)

    def get_available_time(self) -> int:
        """Return the owner's available pet-care time."""
        return self.available_time

    def get_info(self) -> str:
        """Return a formatted summary of the owner."""
        pet_names = ", ".join(pet.name for pet in self.pets) or "no pets added"
        return (
            f"{self.name} has {self.available_time} minutes available and cares for "
            f"{pet_names}."
        )

    def add_pet(self, pet: Pet) -> None:
        """Add a pet to this owner."""
        self.pets.append(pet)

    def get_all_tasks(self) -> List[Task]:
        """Return tasks from all of the owner's pets."""
        all_tasks: List[Task] = []
        for pet in self.pets:
            all_tasks.extend(pet.get_tasks())
        return all_tasks


class Scheduler:
    """Handles scheduling logic to generate daily plans."""

    def __init__(self, owner: Owner):
        """Initialize the scheduler for an owner."""
        self.owner = owner

    def get_all_tasks(self) -> List[Task]:
        """Return all tasks from the owner's pets."""
        return self.owner.get_all_tasks()

    def remove_task(self, description: str, pet_name: str) -> bool:
        """Remove a task from a specific pet."""
        for pet in self.owner.pets:
            if pet.name != pet_name:
                continue
            for index, task in enumerate(pet.tasks):
                if task.description == description:
                    del pet.tasks[index]
                    return True
        return False

    def mark_task_complete(self, description: str, pet_name: str) -> bool:
        """Mark a task complete for a specific pet."""
        for pet in self.owner.pets:
            if pet.name != pet_name:
                continue
            for task in pet.tasks:
                if task.description == description:
                    task.mark_complete()
                    return True
        return False

    def generate_plan(self) -> Dict:
        """Generate a daily schedule from the owner's tasks."""
        tasks = [task for task in self.get_all_tasks() if not task.completed]
        sorted_tasks = sorted(tasks, key=lambda task: (-task.priority, task.duration))
        scheduled_tasks: List[Dict] = []
        unscheduled_tasks: List[Dict] = []
        used_time = 0

        for task in sorted_tasks:
            pet_name = self._find_pet_for_task(task)
            task_data = {
                "pet_name": pet_name,
                "description": task.description,
                "duration": task.duration,
                "frequency": task.frequency,
                "priority": task.priority,
            }
            if used_time + task.duration <= self.owner.available_time:
                scheduled_tasks.append(task_data)
                used_time += task.duration
            else:
                unscheduled_tasks.append(task_data)

        covered_pets = sorted({task["pet_name"] for task in scheduled_tasks if task["pet_name"]})
        pet_summary = ", ".join(covered_pets) if covered_pets else "no pets"
        explanation = (
            f"Scheduled {len(scheduled_tasks)} tasks for {pet_summary} within "
            f"{self.owner.available_time} available minutes, prioritizing higher-priority "
            f"tasks first."
        )

        return {
            "owner_name": self.owner.name,
            "pet_names": [pet.name for pet in self.owner.pets],
            "scheduled_tasks": scheduled_tasks,
            "total_duration": used_time,
            "explanation": explanation,
            "unscheduled_tasks": unscheduled_tasks,
        }

    def _find_pet_for_task(self, target_task: Task) -> str:
        """Return the pet name associated with a task."""
        for pet in self.owner.pets:
            if target_task in pet.tasks:
                return pet.name
        return "Unknown pet"

    def display_plan(self) -> str:
        """Return the generated plan as formatted text."""
        plan = self.generate_plan()

        if not plan["scheduled_tasks"]:
            return "No tasks were scheduled."

        lines = [
            f"Daily plan for {plan['owner_name']}",
            f"Pets: {', '.join(plan['pet_names']) if plan['pet_names'] else 'none'}",
        ]
        for task in plan["scheduled_tasks"]:
            lines.append(
                f"- {task['description']} for {task['pet_name']} "
                f"({task['duration']} min, priority {task['priority']})"
            )
        lines.append(f"Total scheduled time: {plan['total_duration']} minutes")
        return "\n".join(lines)

    def get_explanation(self) -> str:
        """Return the scheduling explanation."""
        return self.generate_plan()["explanation"]
