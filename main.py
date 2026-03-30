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
        title="Afternoon play",
        description="Play fetch with Milo",
        due_date=now + timedelta(hours=3),
        frequency="daily",
    )

    task2 = Task(
        task_id="task_002",
        title="Morning meds",
        description="Give Zoe her morning medication",
        due_date=now + timedelta(hours=1),
        frequency="daily",
    )

    task3 = Task(
        task_id="task_003",
        title="Evening grooming",
        description="Brush Milo and check nails",
        due_date=now + timedelta(hours=5),
        frequency="weekly",
    )

    task4 = Task(
        task_id="task_004",
        title="Midday feeding",
        description="Feed Zoe her lunch portion",
        due_date=now + timedelta(hours=2),
        frequency="daily",
    )

    # Injecting a scheduling conflict for Step 4 testing
    task5 = Task(
        task_id="task_005",
        title="Zoe's Vet Appointment",
        description="Annual checkup",
        due_date=now + timedelta(hours=3), # Intentionally matches task1
        frequency="once",
    )

    pet_milo.add_task(task1)
    pet_milo.add_task(task3)
    pet_zoe.add_task(task2)
    pet_zoe.add_task(task4)
    pet_zoe.add_task(task5)

    scheduler = Scheduler([owner])

    # Check for Schedule Conflicts (Step 4)
    conflicts = scheduler.check_conflicts()
    if conflicts:
        print("\n=== SYSTEM ALERTS ===")
        for warning in conflicts:
            print(warning)
        print("=====================\n")

    # Complete task using the Scheduler to trigger Recurring Tasks (Step 3)
    # This will mark 'task_002' as true, and create a NEW task for tomorrow!
    scheduler.complete_task("task_002")

    sorted_tasks = scheduler.sort_by_time(owner.get_all_tasks())
    incomplete_tasks = scheduler.filter_tasks(completed=False)
    zoe_tasks = scheduler.filter_tasks(pet_name="Zoe")

    print("Today's Schedule (sorted by time)")
    print("----------------------------------")
    for task in sorted_tasks:
        due = task.due_date.strftime("%Y-%m-%d %H:%M UTC") if task.due_date else "No due date"
        print(f"- {task.title} ({due}) - Completed: {task.completed}")

    print("\nZoe's Tasks (Showing Automated Recurring Task)")
    print("-------------")
    for task in zoe_tasks:
        due = task.due_date.strftime("%Y-%m-%d %H:%M UTC") if task.due_date else "No due date"
        print(f"- {task.title} at {due} - Completed: {task.completed}")

if __name__ == "__main__":
    main()