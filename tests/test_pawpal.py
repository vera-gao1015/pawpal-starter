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


def test_remove_pet_removes_matching_pet_from_owner() -> None:
    owner = Owner(name="Jordan", available_time=60)
    mochi = Pet(name="Mochi", type="dog", age=3)
    luna = Pet(name="Luna", type="cat", age=5)
    owner.add_pet(mochi)
    owner.add_pet(luna)

    result = owner.remove_pet("Mochi")

    assert result is True
    assert [pet.name for pet in owner.pets] == ["Luna"]


def test_add_pet_rejects_duplicate_names() -> None:
    owner = Owner(name="Jordan", available_time=60)

    first_result = owner.add_pet(Pet(name="Mochi", type="dog", age=3))
    second_result = owner.add_pet(Pet(name="Mochi", type="cat", age=5))

    assert first_result is True
    assert second_result is False
    assert [pet.name for pet in owner.pets] == ["Mochi"]


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

    assert len(filtered_tasks) == 1
    assert filtered_tasks[0]["task_id"] == completed_task.task_id
    assert filtered_tasks[0]["pet_name"] == "Mochi"
    assert filtered_tasks[0]["description"] == "Breakfast"
    assert filtered_tasks[0]["duration"] == 10
    assert filtered_tasks[0]["frequency"] == "daily"
    assert filtered_tasks[0]["priority"] == 1
    assert filtered_tasks[0]["scheduled_time"] == ""
    assert filtered_tasks[0]["completed"] is True


def test_mark_task_complete_creates_next_daily_occurrence() -> None:
    owner = Owner(name="Jordan", available_time=60)
    pet = Pet(name="Mochi", type="dog", age=3)
    task = Task(description="Breakfast", duration=10, frequency="daily", scheduled_time="08:00")
    pet.add_task(task)
    owner.add_pet(pet)

    scheduler = Scheduler(owner)
    result = scheduler.mark_task_complete(task.task_id, "Mochi")

    assert result is True
    assert len(pet.tasks) == 2
    assert pet.tasks[0].completed is True
    assert pet.tasks[1].completed is False
    assert pet.tasks[1].task_id != pet.tasks[0].task_id
    assert pet.tasks[1].description == "Breakfast"
    assert pet.tasks[1].frequency == "daily"
    assert pet.tasks[1].scheduled_time == "08:00"
    assert pet.tasks[1].due_date == date.today() + timedelta(days=1)


def test_mark_task_complete_creates_next_weekly_occurrence_only_for_recurring_tasks() -> None:
    owner = Owner(name="Jordan", available_time=60)
    pet = Pet(name="Luna", type="cat", age=5)
    brush_task = Task(description="Brush", duration=5, frequency="weekly")
    vet_task = Task(description="Vet visit", duration=30, frequency="as needed")
    pet.add_task(brush_task)
    pet.add_task(vet_task)
    owner.add_pet(pet)

    scheduler = Scheduler(owner)

    weekly_result = scheduler.mark_task_complete(brush_task.task_id, "Luna")
    as_needed_result = scheduler.mark_task_complete(vet_task.task_id, "Luna")

    brush_tasks = [task for task in pet.tasks if task.description == "Brush"]
    vet_tasks = [task for task in pet.tasks if task.description == "Vet visit"]

    assert weekly_result is True
    assert as_needed_result is True
    assert len(brush_tasks) == 2
    assert brush_tasks[0].completed is True
    assert brush_tasks[1].completed is False
    assert brush_tasks[1].task_id != brush_tasks[0].task_id
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


def test_generate_plan_respects_available_time_and_tracks_unscheduled_tasks() -> None:
    owner = Owner(name="Jordan", available_time=30)
    pet = Pet(name="Mochi", type="dog", age=3)
    pet.add_task(Task(description="Walk", duration=20, frequency="daily", priority=3))
    pet.add_task(Task(description="Breakfast", duration=10, frequency="daily", priority=2))
    pet.add_task(Task(description="Brush", duration=5, frequency="weekly", priority=1))
    owner.add_pet(pet)

    scheduler = Scheduler(owner)
    plan = scheduler.generate_plan()

    assert [task["description"] for task in plan["scheduled_tasks"]] == ["Walk", "Breakfast"]
    assert [task["description"] for task in plan["unscheduled_tasks"]] == ["Brush"]
    assert plan["total_duration"] == 30


def test_sort_by_time_places_blank_scheduled_times_last() -> None:
    owner = Owner(name="Jordan", available_time=60)
    scheduler = Scheduler(owner)
    tasks = [
        Task(description="Flexible check-in", duration=5, frequency="daily"),
        Task(description="Breakfast", duration=10, frequency="daily", scheduled_time="08:00"),
        Task(description="Walk", duration=20, frequency="daily", scheduled_time="07:15"),
    ]

    sorted_tasks = scheduler.sort_by_time(tasks)

    assert [task.description for task in sorted_tasks] == ["Walk", "Breakfast", "Flexible check-in"]


def test_detect_conflicts_ignores_invalid_times_and_back_to_back_tasks() -> None:
    owner = Owner(name="Jordan", available_time=60)
    pet = Pet(name="Mochi", type="dog", age=3)
    pet.add_task(Task(description="Breakfast", duration=30, frequency="daily", scheduled_time="08:00"))
    pet.add_task(Task(description="Medication", duration=10, frequency="daily", scheduled_time="08:30"))
    pet.add_task(Task(description="Bad time entry", duration=15, frequency="daily", scheduled_time="not-a-time"))
    owner.add_pet(pet)

    scheduler = Scheduler(owner)

    assert scheduler.detect_conflicts() == []


def test_mark_task_complete_only_affects_matching_pet_when_descriptions_repeat() -> None:
    owner = Owner(name="Jordan", available_time=60)
    mochi = Pet(name="Mochi", type="dog", age=3)
    luna = Pet(name="Luna", type="cat", age=5)
    mochi.add_task(Task(description="Feed", duration=10, frequency="daily"))
    luna.add_task(Task(description="Feed", duration=10, frequency="daily"))
    owner.add_pet(mochi)
    owner.add_pet(luna)

    scheduler = Scheduler(owner)
    result = scheduler.mark_task_complete(mochi.tasks[0].task_id, "Mochi")

    assert result is True
    assert mochi.tasks[0].completed is True
    assert luna.tasks[0].completed is False


def test_mark_task_complete_does_not_create_duplicate_recurring_tasks_when_repeated() -> None:
    owner = Owner(name="Jordan", available_time=60)
    pet = Pet(name="Mochi", type="dog", age=3)
    task = Task(description="Breakfast", duration=10, frequency="daily", scheduled_time="08:00")
    pet.add_task(task)
    owner.add_pet(pet)

    scheduler = Scheduler(owner)

    first_result = scheduler.mark_task_complete(task.task_id, "Mochi")
    second_result = scheduler.mark_task_complete(pet.tasks[1].task_id, "Mochi")

    breakfast_tasks = [task for task in pet.tasks if task.description == "Breakfast"]

    assert first_result is True
    assert second_result is True
    assert len(breakfast_tasks) == 3
    assert [task.completed for task in breakfast_tasks] == [True, True, False]


def test_task_ids_are_unique_for_separate_tasks() -> None:
    first_task = Task(description="Breakfast", duration=10, frequency="daily")
    second_task = Task(description="Breakfast", duration=10, frequency="daily")

    assert first_task.task_id != second_task.task_id
