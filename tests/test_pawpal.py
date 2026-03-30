from pathlib import Path
import sys
from datetime import date, timedelta

sys.path.append(str(Path(__file__).resolve().parents[1]))

from pawpal_system import Owner, Pet, Scheduler, Task


def test_mark_complete_updates_task_status() -> None:
    task = Task(description="Morning walk", duration=20, frequency="daily")

    task.mark_complete()

    assert task.completed is True


def test_add_task_increases_pet_task_count() -> None:
    pet = Pet(name="Mochi", type="dog", age=3)
    task = Task(description="Breakfast", duration=10, frequency="daily")

    pet.add_task(task)

    assert len(pet.tasks) == 1


def test_sort_by_time_orders_tasks_by_hhmm_string() -> None:
    owner = Owner(name="Jordan", available_time=60)
    scheduler = Scheduler(owner)
    tasks = [
        Task(description="Lunch", duration=10, frequency="daily", scheduled_time="12:30"),
        Task(description="Breakfast", duration=10, frequency="daily", scheduled_time="08:00"),
        Task(description="Walk", duration=20, frequency="daily", scheduled_time="07:15"),
    ]

    sorted_tasks = scheduler.sort_by_time(tasks)

    assert [task.description for task in sorted_tasks] == ["Walk", "Breakfast", "Lunch"]


def test_filter_tasks_by_completion_status_and_pet_name() -> None:
    owner = Owner(name="Jordan", available_time=60)
    mochi = Pet(name="Mochi", type="dog", age=3)
    luna = Pet(name="Luna", type="cat", age=5)

    completed_task = Task(description="Breakfast", duration=10, frequency="daily")
    completed_task.mark_complete()
    pending_task = Task(description="Walk", duration=20, frequency="daily")
    other_pet_task = Task(description="Brush", duration=5, frequency="weekly")

    mochi.add_task(completed_task)
    mochi.add_task(pending_task)
    luna.add_task(other_pet_task)
    owner.add_pet(mochi)
    owner.add_pet(luna)

    scheduler = Scheduler(owner)
    filtered_tasks = scheduler.filter_tasks(completed=True, pet_name="Mochi")

    assert filtered_tasks == [
        {
            "pet_name": "Mochi",
            "description": "Breakfast",
            "duration": 10,
            "frequency": "daily",
            "priority": 1,
            "scheduled_time": "",
            "completed": True,
        }
    ]


def test_mark_task_complete_creates_next_daily_occurrence() -> None:
    owner = Owner(name="Jordan", available_time=60)
    pet = Pet(name="Mochi", type="dog", age=3)
    pet.add_task(Task(description="Breakfast", duration=10, frequency="daily", scheduled_time="08:00"))
    owner.add_pet(pet)

    scheduler = Scheduler(owner)
    result = scheduler.mark_task_complete("Breakfast", "Mochi")

    assert result is True
    assert len(pet.tasks) == 2
    assert pet.tasks[0].completed is True
    assert pet.tasks[1].completed is False
    assert pet.tasks[1].description == "Breakfast"
    assert pet.tasks[1].frequency == "daily"
    assert pet.tasks[1].scheduled_time == "08:00"
    assert pet.tasks[1].due_date == date.today() + timedelta(days=1)


def test_mark_task_complete_creates_next_weekly_occurrence_only_for_recurring_tasks() -> None:
    owner = Owner(name="Jordan", available_time=60)
    pet = Pet(name="Luna", type="cat", age=5)
    pet.add_task(Task(description="Brush", duration=5, frequency="weekly"))
    pet.add_task(Task(description="Vet visit", duration=30, frequency="as needed"))
    owner.add_pet(pet)

    scheduler = Scheduler(owner)

    weekly_result = scheduler.mark_task_complete("Brush", "Luna")
    as_needed_result = scheduler.mark_task_complete("Vet visit", "Luna")

    brush_tasks = [task for task in pet.tasks if task.description == "Brush"]
    vet_tasks = [task for task in pet.tasks if task.description == "Vet visit"]

    assert weekly_result is True
    assert as_needed_result is True
    assert len(brush_tasks) == 2
    assert brush_tasks[0].completed is True
    assert brush_tasks[1].completed is False
    assert brush_tasks[1].due_date == date.today() + timedelta(days=7)
    assert len(vet_tasks) == 1
    assert vet_tasks[0].completed is True


def test_detect_conflicts_for_same_pet_tasks_at_same_time() -> None:
    owner = Owner(name="Jordan", available_time=60)
    pet = Pet(name="Mochi", type="dog", age=3)
    pet.add_task(Task(description="Breakfast", duration=20, frequency="daily", scheduled_time="08:00"))
    pet.add_task(Task(description="Walk", duration=15, frequency="daily", scheduled_time="08:00"))
    owner.add_pet(pet)

    scheduler = Scheduler(owner)
    warnings = scheduler.detect_conflicts()

    assert warnings == [
        "Warning: Breakfast for Mochi overlaps with Walk for Mochi at 08:00."
    ]


def test_detect_conflicts_for_different_pets_with_overlapping_times() -> None:
    owner = Owner(name="Jordan", available_time=60)
    mochi = Pet(name="Mochi", type="dog", age=3)
    luna = Pet(name="Luna", type="cat", age=5)
    mochi.add_task(Task(description="Breakfast", duration=30, frequency="daily", scheduled_time="08:00"))
    luna.add_task(Task(description="Medication", duration=10, frequency="daily", scheduled_time="08:15"))
    owner.add_pet(mochi)
    owner.add_pet(luna)

    scheduler = Scheduler(owner)
    warnings = scheduler.detect_conflicts()

    assert warnings == [
        "Warning: Breakfast for Mochi overlaps with Medication for Luna at 08:15."
    ]
