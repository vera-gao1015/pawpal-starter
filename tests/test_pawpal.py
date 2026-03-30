from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parents[1]))

from pawpal_system import Pet, Task


def test_mark_complete_updates_task_status() -> None:
    task = Task(description="Morning walk", duration=20, frequency="daily")

    task.mark_complete()

    assert task.completed is True


def test_add_task_increases_pet_task_count() -> None:
    pet = Pet(name="Mochi", type="dog", age=3)
    task = Task(description="Breakfast", duration=10, frequency="daily")

    pet.add_task(task)

    assert len(pet.tasks) == 1
