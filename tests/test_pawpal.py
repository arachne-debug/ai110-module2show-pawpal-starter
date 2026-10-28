from pawpal_system import Owner, Pet, Scheduler, Task


def test_task_completion_marks_complete():
    task = Task(description="Walk the dog", time="08:00")
    assert task.completed is False

    task.mark_complete()

    assert task.completed is True


def test_adding_task_increases_task_count():
    pet = Pet(id="pet-1", name="Biscuit", species="Dog")
    initial_count = len(pet.tasks)

    pet.add_task(Task(description="Feed breakfast", time="09:00"))

    assert len(pet.tasks) == initial_count + 1


def test_tasks_are_returned_in_chronological_order():
    owner = Owner(id="owner-1", name="Sam")
    pet = Pet(id="pet-2", name="Mochi", species="Cat")
    owner.add_pet(pet)

    late_task = Task(description="Evening play", time="18:00")
    early_task = Task(description="Morning walk", time="08:00")
    pet.add_task(late_task)
    pet.add_task(early_task)

    scheduler = Scheduler(owner=owner)
    ordered = scheduler.organize_tasks()

    assert [task.time for task in ordered] == ["08:00", "18:00"]


def test_daily_task_completes_and_creates_next_day_task():
    pet = Pet(id="pet-3", name="Luna", species="Dog")
    task = Task(description="Morning walk", time="08:00", frequency="daily")
    pet.add_task(task)

    pet.complete_task("Morning walk")

    assert task.completed is True
    assert len(pet.tasks) == 2
    assert pet.tasks[-1].time == "08:00"
    assert pet.tasks[-1].completed is False
    assert pet.tasks[-1].frequency == "daily"


def test_scheduler_flags_duplicate_times_as_conflicts():
    owner = Owner(id="owner-1", name="Sam")
    pet = Pet(id="pet-4", name="Biscuit", species="Dog")
    owner.add_pet(pet)
    pet.add_task(Task(description="Walk", time="08:00"))
    pet.add_task(Task(description="Feed", time="08:00"))

    scheduler = Scheduler(owner=owner)
    conflicts = scheduler.find_conflicts()

    assert "08:00" in conflicts
