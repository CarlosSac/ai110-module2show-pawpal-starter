from datetime import date, timedelta


class Task:
    def __init__(self, description: str, duration_minutes: int, priority: str, frequency: str = "daily", start_time: str = "08:00", due_date: str = None):
        self.description = description
        self.duration_minutes = duration_minutes
        self.frequency = frequency  # "daily" or "weekly"
        self.priority = priority    # "low", "medium", "high"
        self.start_time = start_time  # "HH:MM" format
        self.due_date = due_date or date.today().isoformat()  # "YYYY-MM-DD"
        self.completed = False

    """Marks the task as completed."""
    def mark_complete(self):
        self.completed = True

    """Returns a new Task for the next occurrence based on frequency, or None if not recurring."""
    def next_occurrence(self):
        if self.frequency == "daily":
            next_date = date.today() + timedelta(days=1)
        elif self.frequency == "weekly":
            next_date = date.today() + timedelta(weeks=1)
        else:
            return None
        return Task(self.description, self.duration_minutes, self.priority, self.frequency, self.start_time, next_date.isoformat())

    """Returns a numeric value for priority to help with sorting."""
    def priority_value(self):
        return {"low": 1, "medium": 2, "high": 3}.get(self.priority, 0)

    """String representation of the task."""
    def __str__(self):
        status = "done" if self.completed else "pending"
        return f"[{status}] {self.description} ({self.duration_minutes} min, {self.priority} priority, {self.frequency}, due {self.due_date})"


class Pet:
    def __init__(self, name: str, species: str):
        self.name = name
        self.species = species
        self.tasks = []

    """Adds a task to the pet's task list."""
    def add_task(self, task: Task):
        self.tasks.append(task)

    """Marks a task complete and appends the next occurrence if the task is recurring."""
    def complete_task(self, task: Task):
        task.mark_complete()
        next_task = task.next_occurrence()
        if next_task:
            self.tasks.append(next_task)

    """Returns a list of pending tasks for the pet."""
    def get_pending_tasks(self):
        return [t for t in self.tasks if not t.completed]

    """String representation of the pet."""
    def __str__(self):
        return f"{self.name} ({self.species})"


class Owner:
    def __init__(self, name: str, available_minutes: int):
        self.name = name
        self.available_minutes = available_minutes
        self.pets = []

    """Adds a pet to the owner's list of pets."""
    def add_pet(self, pet: Pet):
        self.pets.append(pet)

    """Returns a list of all pending tasks across all pets."""  
    def get_all_tasks(self):
        all_tasks = []
        for pet in self.pets:
            all_tasks.extend(pet.get_pending_tasks())
        return all_tasks

    def __str__(self):
        return f"{self.name} ({len(self.pets)} pet(s), {self.available_minutes} min available)"


class Scheduler:
    def __init__(self, owner: Owner):
        self.owner = owner

    """Returns a list of tasks sorted by priority (high to low)."""
    def get_tasks_by_priority(self):
        tasks = self.owner.get_all_tasks()
        return sorted(tasks, key=lambda t: t.priority_value(), reverse=True)

    """Builds a schedule of tasks that can be completed within the owner's available time."""
    def build_schedule(self):
        scheduled = []
        remaining = self.owner.available_minutes
        for task in self.get_tasks_by_priority():
            if task.duration_minutes <= remaining:
                scheduled.append(task)
                remaining -= task.duration_minutes
        return scheduled

    """Filters tasks by completion status and/or pet name."""
    def filter_tasks(self, completed: bool = None, pet_name: str = None):
        results = []
        for pet in self.owner.pets:
            if pet_name is not None and pet.name.lower() != pet_name.lower():
                continue
            for task in pet.tasks:
                if completed is not None and task.completed != completed:
                    continue
                results.append(task)
        return results

    """Returns a list of tasks sorted by start_time ("HH:MM") ascending."""
    def sort_by_time(self):
        tasks = self.owner.get_all_tasks()
        return sorted(tasks, key=lambda t: t.start_time)

    """Detects scheduling conflicts where two pending tasks overlap in time. Returns a list of warning strings."""
    def detect_conflicts(self):
        warnings = []
        # Build a flat list of (pet_name, task) pairs for all pending tasks
        entries = []
        for pet in self.owner.pets:
            for task in pet.get_pending_tasks():
                h, m = map(int, task.start_time.split(":"))
                start = h * 60 + m
                end = start + task.duration_minutes
                entries.append((pet.name, task, start, end))

        for i in range(len(entries)):
            for j in range(i + 1, len(entries)):
                pet_a, task_a, start_a, end_a = entries[i]
                pet_b, task_b, start_b, end_b = entries[j]
                if start_a < end_b and start_b < end_a:
                    warnings.append(
                        f"WARNING: '{task_a.description}' ({pet_a}, {task_a.start_time}) "
                        f"overlaps with '{task_b.description}' ({pet_b}, {task_b.start_time})"
                    )
        return warnings

    """Provides a human-readable explanation of the schedule."""
    def explain_schedule(self, schedule: list):
        lines = [f"Schedule for {self.owner.name} ({self.owner.available_minutes} min available):\n"]
        for i, task in enumerate(schedule, 1):
            lines.append(f"{i}. {task}")
        lines.append(f"\nTotal time: {sum(t.duration_minutes for t in schedule)} min")
        return "\n".join(lines)
