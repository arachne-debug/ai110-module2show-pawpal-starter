from pawpal_system import Pet, Task


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
