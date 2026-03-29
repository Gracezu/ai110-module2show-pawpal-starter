from datetime import datetime, timedelta

from pawpal_system import Owner, Pet, Task, Scheduler


def main() -> None:
    owner = Owner(
        owner_id="owner_001",
        email="alex@example.com",
        password="supersecret",
        caregiver_role="primary",
    )

    pet_milo = Pet(pet_id="pet_001", name="Milo", breed="Beagle", weight=18.2, age=4)
    pet_zoe = Pet(pet_id="pet_002", name="Zoe", breed="Siamese", weight=10.1, age=2)

    owner.add_pet(pet_milo)
    owner.add_pet(pet_zoe)

    now = datetime.utcnow()

    task1 = Task(
        task_id="task_001",
        title="Morning walk",
        description="Walk Milo around the neighborhood",
        due_date=now + timedelta(hours=1),
        frequency="daily",
    )

    task2 = Task(
        task_id="task_002",
        title="Medication for Zoe",
        description="Administer daily medication before lunch",
        due_date=now + timedelta(hours=3),
        frequency="daily",
    )

    task3 = Task(
        task_id="task_003",
        title="Grooming check",
        description="Inspect pet nails and ears",
        due_date=now + timedelta(hours=5),
        frequency="weekly",
    )

    pet_milo.add_task(task1)
    pet_zoe.add_task(task2)
    pet_milo.add_task(task3)

    scheduler = Scheduler([owner])
    tasks = scheduler.organize_tasks_by_due_date(owner.get_all_tasks())

    print("Today's Schedule")
    print("----------------")
    for task in tasks:
        due = task.due_date.strftime("%Y-%m-%d %H:%M UTC") if task.due_date else "No due date"
        print(f"- {task.title} ({due}) - Completed: {task.completed}")


if __name__ == "__main__":
    main()
