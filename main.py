from pawpal_system import Owner, Pet, Task, Scheduler

# Create owner
jordan = Owner("Jordan", available_minutes=90)

# Create pets
mochi = Pet("Mochi", "dog")
luna = Pet("Luna", "cat")

# Add tasks OUT OF ORDER (start_times intentionally scrambled)
mochi.add_task(Task("Evening walk",   20, "high",   "daily",  "18:00"))
mochi.add_task(Task("Morning walk",   30, "high",   "daily",  "07:00"))
mochi.add_task(Task("Grooming",       20, "low",    "weekly", "14:00"))
mochi.add_task(Task("Feeding",        10, "high",   "daily",  "08:00"))

luna.add_task(Task("Playtime",        15, "low",    "daily",  "16:00"))
luna.add_task(Task("Litter cleaning", 10, "medium", "daily",  "09:00"))
luna.add_task(Task("Vet meds",         5, "high",   "daily",  "07:30"))

# Intentional conflicts: both overlap with Mochi's Morning walk (07:00, 30 min → ends 07:30)
mochi.add_task(Task("Brush teeth",    10, "medium", "daily",  "07:15"))  # same pet, overlaps 07:00 walk
luna.add_task( Task("Breakfast",      15, "high",   "daily",  "07:10"))  # different pet, overlaps 07:00 walk

# Mark tasks complete via Pet.complete_task() — triggers next occurrence for recurring tasks
mochi.complete_task(mochi.tasks[3])   # Feeding (daily)  → spawns tomorrow's Feeding
luna.complete_task(luna.tasks[1])     # Litter cleaning (daily) → spawns tomorrow's Litter cleaning
mochi.complete_task(mochi.tasks[2])   # Grooming (weekly) → spawns next week's Grooming

# Register pets with owner
jordan.add_pet(mochi)
jordan.add_pet(luna)

scheduler = Scheduler(jordan)

# --- sort_by_time() ---
print("=" * 40)
print("  TASKS SORTED BY START TIME (HH:MM)")
print("=" * 40)
for task in scheduler.sort_by_time():
    print(f"  {task.start_time}  {task}")

# --- filter_tasks: pending only ---
print("\n" + "=" * 40)
print("  PENDING TASKS (all pets)")
print("=" * 40)
for task in scheduler.filter_tasks(completed=False):
    print(f"  {task}")

# --- filter_tasks: completed only ---
print("\n" + "=" * 40)
print("  COMPLETED TASKS (all pets)")
print("=" * 40)
for task in scheduler.filter_tasks(completed=True):
    print(f"  {task}")

# --- filter_tasks: by pet name ---
print("\n" + "=" * 40)
print("  ALL TASKS FOR MOCHI")
print("=" * 40)
for task in scheduler.filter_tasks(pet_name="Mochi"):
    print(f"  {task}")

# --- detect_conflicts ---
print("\n" + "=" * 40)
print("  CONFLICT DETECTION")
print("=" * 40)
conflicts = scheduler.detect_conflicts()
if conflicts:
    for w in conflicts:
        print(f"  {w}")
else:
    print("  No conflicts found.")

# --- build_schedule ---
print("\n" + "=" * 40)
print("       TODAY'S SCHEDULE")
print("=" * 40)
print(scheduler.explain_schedule(scheduler.build_schedule()))
