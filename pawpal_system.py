class Owner:
    def __init__(self, name: str, available_minutes: int, preferences: list = None):
        self.name = name
        self.available_minutes = available_minutes
        self.preferences = preferences or []
        self.pets = []

    def add_pet(self, pet):
        pass

    def __str__(self):
        pass


class Pet:
    def __init__(self, name: str, species: str, age: int, special_needs: list = None):
        self.name = name
        self.species = species
        self.age = age
        self.special_needs = special_needs or []

    def get_default_tasks(self):
        pass

    def __str__(self):
        pass


class Task:
    def __init__(self, title: str, duration_minutes: int, priority: str, required: bool = False, preferred_time: str = "any"):
        self.title = title
        self.duration_minutes = duration_minutes
        self.priority = priority
        self.required = required
        self.preferred_time = preferred_time

    def priority_value(self):
        pass

    def __str__(self):
        pass


class Scheduler:
    def __init__(self, owner: Owner, pet: Pet, tasks: list):
        self.owner = owner
        self.pet = pet
        self.tasks = tasks

    def build_schedule(self):
        pass

    def _sort_by_priority(self, tasks: list):
        pass

    def _fit_within_time(self, tasks: list, available_minutes: int):
        pass

    def _assign_times(self, tasks: list):
        pass

    def _generate_explanation(self, task: Task, reason: str):
        pass
