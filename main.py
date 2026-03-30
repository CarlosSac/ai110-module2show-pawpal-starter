from pawpal_system import Owner, Pet, Task, Scheduler

# Create owner
jordan = Owner("Jordan", available_minutes=90)

# Create pets
mochi = Pet("Mochi", "dog")
luna = Pet("Luna", "cat")

# Add tasks to Mochi
mochi.add_task(Task("Morning walk", 30, "daily", "high"))
mochi.add_task(Task("Feeding", 10, "daily", "high"))
mochi.add_task(Task("Grooming", 20, "weekly", "low"))

# Add tasks to Luna
luna.add_task(Task("Litter cleaning", 10, "daily", "medium"))
luna.add_task(Task("Playtime", 15, "daily", "low"))

# Register pets with owner
jordan.add_pet(mochi)
jordan.add_pet(luna)

# Build and display schedule
scheduler = Scheduler(jordan)
schedule = scheduler.build_schedule()

print("=" * 40)
print("       TODAY'S SCHEDULE")
print("=" * 40)
print(scheduler.explain_schedule(schedule))
