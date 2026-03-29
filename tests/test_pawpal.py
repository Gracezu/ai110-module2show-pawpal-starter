from datetime import datetime, timedelta, timezone

from pawpal_system import Pet, Task


def test_task_completion() -> None:
    task = Task(
        task_id="task_001",
        title="Feed Milo",
        due_date=datetime.now(timezone.utc) + timedelta(hours=1),
    )

    assert task.completed is False
    task.mark_complete()
    assert task.completed is True


def test_pet_task_addition() -> None:
    pet = Pet(
        pet_id="pet_001",
        name="Milo",
        breed="Beagle",
        weight=18.2,
        age=4,
    )

    assert len(pet.tasks) == 0

    task = Task(
        task_id="task_002",
        title="Morning walk",
        due_date=datetime.now(timezone.utc) + timedelta(hours=2),
    )

    pet.add_task(task)
    assert len(pet.tasks) == 1
    assert pet.tasks[0] is task
