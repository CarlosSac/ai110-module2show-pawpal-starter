import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from pawpal_system import Task, Pet


def test_mark_complete_changes_status():
    task = Task("Morning walk", 30, "daily", "high")
    assert task.completed == False
    task.mark_complete()
    assert task.completed == True


def test_add_task_increases_pet_task_count():
    pet = Pet("Mochi", "dog")
    assert len(pet.tasks) == 0
    pet.add_task(Task("Feeding", 10, "daily", "high"))
    assert len(pet.tasks) == 1
