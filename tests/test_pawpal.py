from datetime import datetime, timedelta, timezone

from pawpal_system import Owner, Pet, Scheduler, Task


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


def test_sorting_correctness() -> None:
    owner = Owner(
        owner_id="owner_001",
        email="test@example.com",
        password="secret",
        caregiver_role="primary",
    )
    pet = Pet(pet_id="pet_001", name="Milo", breed="Beagle", weight=18.2, age=4)
    owner.add_pet(pet)

    now = datetime.now(timezone.utc)
    task_late = Task(task_id="task_001", title="Late task", due_date=now + timedelta(hours=4))
    task_early = Task(task_id="task_002", title="Early task", due_date=now + timedelta(hours=1))
    task_middle = Task(task_id="task_003", title="Middle task", due_date=now + timedelta(hours=2))

    pet.add_task(task_late)
    pet.add_task(task_early)
    pet.add_task(task_middle)

    scheduler = Scheduler([owner])
    sorted_tasks = scheduler.sort_by_time(owner.get_all_tasks())

    assert [task.task_id for task in sorted_tasks] == ["task_002", "task_003", "task_001"]


def test_recurrence_logic() -> None:
    owner = Owner(
        owner_id="owner_002",
        email="daily@example.com",
        password="secret",
        caregiver_role="primary",
    )
    pet = Pet(pet_id="pet_002", name="Zoe", breed="Siamese", weight=10.1, age=2)
    owner.add_pet(pet)

    now = datetime.now(timezone.utc).replace(hour=8, minute=0, second=0, microsecond=0)
    recurring_task = Task(
        task_id="task_004",
        title="Daily medication",
        due_date=now,
        frequency="daily",
    )
    pet.add_task(recurring_task)

    scheduler = Scheduler([owner])
    scheduler.complete_task("task_004")

    assert len(pet.tasks) == 2
    next_task = [task for task in pet.tasks if task.task_id != "task_004"]
    assert len(next_task) == 1
    assert next_task[0].due_date == now + timedelta(days=1)
    assert next_task[0].frequency == "daily"


def test_conflict_detection() -> None:
    owner = Owner(
        owner_id="owner_003",
        email="conflict@example.com",
        password="secret",
        caregiver_role="primary",
    )
    pet = Pet(pet_id="pet_003", name="Buddy", breed="Labrador", weight=25.0, age=5)
    owner.add_pet(pet)

    now = datetime.now(timezone.utc).replace(second=0, microsecond=0)
    task_a = Task(task_id="task_005", title="Walk", due_date=now)
    task_b = Task(task_id="task_006", title="Feed", due_date=now)

    pet.add_task(task_a)
    pet.add_task(task_b)

    scheduler = Scheduler([owner])
    conflicts = scheduler.check_conflicts()

    assert len(conflicts) == 1
    assert "Walk" in conflicts[0] and "Feed" in conflicts[0]
