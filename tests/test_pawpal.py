import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from datetime import date, timedelta
from pawpal_system import Task, Pet, Owner, Scheduler


def test_mark_complete_changes_status():
    task = Task("Morning walk", 30, "high", "daily")
    assert task.completed == False
    task.mark_complete()
    assert task.completed == True


def test_add_task_increases_pet_task_count():
    pet = Pet("Mochi", "dog")
    assert len(pet.tasks) == 0
    pet.add_task(Task("Feeding", 10, "high", "daily"))
    assert len(pet.tasks) == 1


# --- Sorting correctness ---

def test_sort_by_time_returns_chronological_order():
    owner = Owner("Jordan", 120)
    pet = Pet("Mochi", "dog")
    pet.add_task(Task("Evening walk",  20, "high", "daily", "18:00"))
    pet.add_task(Task("Morning walk",  30, "high", "daily", "07:00"))
    pet.add_task(Task("Midday feed",   10, "high", "daily", "12:00"))
    owner.add_pet(pet)
    scheduler = Scheduler(owner)

    sorted_tasks = scheduler.sort_by_time()
    times = [t.start_time for t in sorted_tasks]
    assert times == sorted(times)


def test_sort_by_time_excludes_completed_tasks():
    owner = Owner("Jordan", 120)
    pet = Pet("Mochi", "dog")
    task_done = Task("Grooming", 20, "low", "weekly", "06:00")
    task_done.mark_complete()
    pet.add_task(task_done)
    pet.add_task(Task("Feeding", 10, "high", "daily", "08:00"))
    owner.add_pet(pet)
    scheduler = Scheduler(owner)

    sorted_tasks = scheduler.sort_by_time()
    assert all(not t.completed for t in sorted_tasks)


# --- Recurrence logic ---

def test_daily_task_creates_next_occurrence_after_complete():
    pet = Pet("Mochi", "dog")
    task = Task("Feeding", 10, "high", "daily", "08:00")
    pet.add_task(task)
    pet.complete_task(task)

    tomorrow = (date.today() + timedelta(days=1)).isoformat()
    new_tasks = [t for t in pet.tasks if not t.completed]
    assert len(new_tasks) == 1
    assert new_tasks[0].due_date == tomorrow


def test_weekly_task_creates_next_occurrence_seven_days_out():
    pet = Pet("Mochi", "dog")
    task = Task("Grooming", 20, "low", "weekly", "14:00")
    pet.add_task(task)
    pet.complete_task(task)

    next_week = (date.today() + timedelta(weeks=1)).isoformat()
    new_tasks = [t for t in pet.tasks if not t.completed]
    assert len(new_tasks) == 1
    assert new_tasks[0].due_date == next_week


def test_non_recurring_task_does_not_spawn_next_occurrence():
    pet = Pet("Mochi", "dog")
    task = Task("Vet visit", 60, "high", "once", "10:00")
    pet.add_task(task)
    pet.complete_task(task)

    assert len(pet.tasks) == 1  # only the original, no new task appended


def test_recurred_task_preserves_description_and_duration():
    pet = Pet("Mochi", "dog")
    task = Task("Morning walk", 30, "high", "daily", "07:00")
    pet.add_task(task)
    pet.complete_task(task)

    new_task = next(t for t in pet.tasks if not t.completed)
    assert new_task.description == "Morning walk"
    assert new_task.duration_minutes == 30


# --- Conflict detection ---

def test_detect_conflicts_flags_same_start_time():
    owner = Owner("Jordan", 120)
    pet = Pet("Mochi", "dog")
    pet.add_task(Task("Feeding",      10, "high",   "daily", "08:00"))
    pet.add_task(Task("Morning walk", 30, "high",   "daily", "08:00"))
    owner.add_pet(pet)
    scheduler = Scheduler(owner)

    warnings = scheduler.detect_conflicts()
    assert len(warnings) >= 1


def test_detect_conflicts_flags_partial_overlap():
    owner = Owner("Jordan", 120)
    pet = Pet("Mochi", "dog")
    pet.add_task(Task("Morning walk", 30, "high", "daily", "07:00"))  # ends 07:30
    pet.add_task(Task("Brush teeth",  10, "medium", "daily", "07:15"))  # starts inside walk
    owner.add_pet(pet)
    scheduler = Scheduler(owner)

    warnings = scheduler.detect_conflicts()
    assert len(warnings) == 1
    assert "Morning walk" in warnings[0]
    assert "Brush teeth" in warnings[0]


def test_detect_conflicts_flags_cross_pet_overlap():
    owner = Owner("Jordan", 120)
    mochi = Pet("Mochi", "dog")
    luna  = Pet("Luna", "cat")
    mochi.add_task(Task("Morning walk", 30, "high", "daily", "07:00"))
    luna.add_task( Task("Breakfast",    15, "high", "daily", "07:10"))
    owner.add_pet(mochi)
    owner.add_pet(luna)
    scheduler = Scheduler(owner)

    warnings = scheduler.detect_conflicts()
    assert len(warnings) >= 1


def test_detect_conflicts_returns_empty_when_no_overlap():
    owner = Owner("Jordan", 120)
    pet = Pet("Mochi", "dog")
    pet.add_task(Task("Feeding",      10, "high", "daily", "08:00"))  # ends 08:10
    pet.add_task(Task("Morning walk", 30, "high", "daily", "09:00"))  # starts after
    owner.add_pet(pet)
    scheduler = Scheduler(owner)

    assert scheduler.detect_conflicts() == []


# --- Edge cases ---

def test_empty_pet_does_not_crash_scheduler():
    owner = Owner("Jordan", 60)
    owner.add_pet(Pet("Ghost", "cat"))
    scheduler = Scheduler(owner)

    assert scheduler.build_schedule() == []
    assert scheduler.sort_by_time() == []
    assert scheduler.detect_conflicts() == []


def test_task_fitting_budget_exactly_is_scheduled():
    owner = Owner("Jordan", 30)
    pet = Pet("Mochi", "dog")
    pet.add_task(Task("Morning walk", 30, "high", "daily", "07:00"))
    owner.add_pet(pet)

    schedule = Scheduler(owner).build_schedule()
    assert len(schedule) == 1


def test_task_exceeding_budget_by_one_minute_is_excluded():
    owner = Owner("Jordan", 29)
    pet = Pet("Mochi", "dog")
    pet.add_task(Task("Morning walk", 30, "high", "daily", "07:00"))
    owner.add_pet(pet)

    schedule = Scheduler(owner).build_schedule()
    assert len(schedule) == 0
