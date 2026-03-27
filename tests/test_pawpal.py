"""Pet and task behavior tests."""

from pawpal_system import CareTask, Pet


def test_task_mark_complete_updates_status() -> None:
    task = CareTask(
        task_id="t-1",
        title="Morning walk",
        category="walk",
        duration_minutes=20,
        priority="high",
        is_complete=False,
    )

    assert task.is_complete is False

    task.mark_complete()

    assert task.is_complete is True


def test_adding_task_to_pet_increases_task_count() -> None:
    pet = Pet(pet_id="p-1", name="Mochi", species="dog")
    assert pet.task_count == 0

    task = CareTask(
        task_id="t-walk",
        title="Walk",
        category="walk",
        duration_minutes=30,
        priority="medium",
    )

    pet.add_task(task)

    assert pet.task_count == 1
    assert pet.tasks[0] is task
