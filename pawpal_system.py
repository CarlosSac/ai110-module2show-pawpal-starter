class Task:
    def __init__(self, description: str, duration_minutes: int, frequency: str, priority: str):
        self.description = description
        self.duration_minutes = duration_minutes
        self.frequency = frequency  # "daily", "weekly", etc.
        self.priority = priority    # "low", "medium", "high"
        self.completed = False

    """Marks the task as completed."""
    def mark_complete(self):
        self.completed = True

    """Returns a numeric value for priority to help with sorting."""
    def priority_value(self):
        return {"low": 1, "medium": 2, "high": 3}.get(self.priority, 0)

    """String representation of the task."""
    def __str__(self):
        status = "done" if self.completed else "pending"
        return f"[{status}] {self.description} ({self.duration_minutes} min, {self.priority} priority)"


class Pet:
    def __init__(self, name: str, species: str):
        self.name = name
        self.species = species
        self.tasks = []

    """Adds a task to the pet's task list."""
    def add_task(self, task: Task):
        self.tasks.append(task)

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

    """Provides a human-readable explanation of the schedule."""
    def explain_schedule(self, schedule: list):
        lines = [f"Schedule for {self.owner.name} ({self.owner.available_minutes} min available):\n"]
        for i, task in enumerate(schedule, 1):
            lines.append(f"{i}. {task}")
        lines.append(f"\nTotal time: {sum(t.duration_minutes for t in schedule)} min")
        return "\n".join(lines)
