"""
PawPal+ System - Backend Logic Layer
This module contains all the core classes for the pet care scheduling system.
"""

from dataclasses import dataclass, field
from typing import List, Dict


@dataclass
class Pet:
    """Represents a pet that needs care."""
    name: str
    type: str
    age: int

    def get_info(self) -> str:
        """Returns pet information as a formatted string."""
        pass


@dataclass
class Owner:
    """Represents the pet owner with time constraints and preferences."""
    name: str
    available_time: int
    preferences: Dict = field(default_factory=dict)

    def get_available_time(self) -> int:
        """Returns total available minutes for pet care."""
        pass

    def get_info(self) -> str:
        """Returns owner information as a formatted string."""
        pass


@dataclass
class Task:
    """Represents a pet care task with duration and priority."""
    name: str
    duration: int
    priority: int
    task_type: str
    description: str = ""

    def get_duration(self) -> int:
        """Returns task duration in minutes."""
        pass

    def get_priority(self) -> int:
        """Returns priority level."""
        pass


class Scheduler:
    """Handles scheduling logic to generate daily plans."""

    def __init__(self, owner: Owner):
        """Initialize a Scheduler with owner constraints."""
        self.tasks: List[Task] = []
        self.owner = owner

    def add_task(self, task: Task) -> None:
        """Adds a new task to the list."""
        pass

    def remove_task(self, task_name: str) -> bool:
        """Removes a task by name. Returns True if successful."""
        pass

    def generate_plan(self) -> 'DailyPlan':
        """Creates an optimized daily plan based on constraints and priorities."""
        pass


@dataclass
class DailyPlan:
    """Represents a generated daily schedule with tasks and explanations."""
    scheduled_tasks: List[Task] = field(default_factory=list)
    total_duration: int = 0
    explanation: str = ""
    unscheduled_tasks: List[Task] = field(default_factory=list)

    def get_schedule(self) -> List[Task]:
        """Returns ordered list of scheduled tasks."""
        pass

    def display_plan(self) -> str:
        """Formats and displays the plan clearly."""
        pass

    def get_explanation(self) -> str:
        """Returns reasoning for the schedule."""
        pass
