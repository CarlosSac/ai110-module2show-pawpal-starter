import streamlit as st
from pawpal_system import Owner, Pet, Task, Scheduler

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

st.divider()

# --- Owner & Pet setup ---
st.subheader("Owner & Pet Info")
owner_name = st.text_input("Owner name", value="Jordan")
available_minutes = st.number_input("Time available today (minutes)", min_value=10, max_value=480, value=90)
pet_name = st.text_input("Pet name", value="Mochi")
species = st.selectbox("Species", ["dog", "cat", "other"])

# Rebuild owner/pet whenever inputs change
if (
    "owner" not in st.session_state
    or st.session_state.owner.name != owner_name
    or st.session_state.owner.available_minutes != available_minutes
    or st.session_state.pet.name != pet_name
):
    tasks = st.session_state.pet.tasks if "pet" in st.session_state else []
    st.session_state.owner = Owner(owner_name, available_minutes)
    st.session_state.pet = Pet(pet_name, species)
    for t in tasks:
        st.session_state.pet.add_task(t)
    st.session_state.owner.add_pet(st.session_state.pet)

if "pet" not in st.session_state:
    st.session_state.pet = Pet(pet_name, species)
    st.session_state.owner.add_pet(st.session_state.pet)

st.divider()

# --- Add task ---
st.subheader("Add a Task")
col1, col2, col3, col4 = st.columns(4)
with col1:
    task_description = st.text_input("Description", value="Morning walk")
with col2:
    duration = st.number_input("Duration (min)", min_value=1, max_value=240, value=20)
with col3:
    priority = st.selectbox("Priority", ["low", "medium", "high"], index=2)
with col4:
    start_time = st.text_input("Start time (HH:MM)", value="08:00")

frequency = st.selectbox("Frequency", ["daily", "weekly", "once"])

if st.button("Add task"):
    task = Task(task_description, int(duration), priority, frequency, start_time)
    st.session_state.pet.add_task(task)
    st.success(f"Task added: {task_description} at {start_time} ({priority} priority, {frequency})")

st.divider()

# --- Pending tasks sorted by time ---
st.subheader("Pending Tasks")
scheduler = Scheduler(st.session_state.owner)
sorted_tasks = scheduler.sort_by_time()

if sorted_tasks:
    st.table([
        {
            "Start": t.start_time,
            "Description": t.description,
            "Duration (min)": t.duration_minutes,
            "Priority": t.priority,
            "Frequency": t.frequency,
            "Due": t.due_date,
        }
        for t in sorted_tasks
    ])
else:
    st.info("No pending tasks. Add one above.")

# --- Conflict warnings ---
conflicts = scheduler.detect_conflicts()
if conflicts:
    st.subheader("Scheduling Conflicts")
    for w in conflicts:
        st.warning(w)

st.divider()

# --- Build schedule ---
st.subheader("Build Schedule")
if st.button("Generate schedule"):
    schedule = scheduler.build_schedule()
    if schedule:
        st.success(f"Schedule generated — {sum(t.duration_minutes for t in schedule)} of {available_minutes} min used")
        st.table([
            {
                "Start": t.start_time,
                "Description": t.description,
                "Duration (min)": t.duration_minutes,
                "Priority": t.priority,
                "Due": t.due_date,
            }
            for t in schedule
        ])
    else:
        st.warning("No tasks could be scheduled. Add tasks or increase available time.")

st.divider()

# --- Mark task complete ---
st.subheader("Mark Task Complete")
pending = st.session_state.pet.get_pending_tasks()
if pending:
    task_labels = [f"{t.start_time} — {t.description} ({t.priority})" for t in pending]
    selected_label = st.selectbox("Select a completed task", task_labels)
    if st.button("Mark complete"):
        selected_task = pending[task_labels.index(selected_label)]
        st.session_state.pet.complete_task(selected_task)
        if selected_task.frequency in ("daily", "weekly"):
            st.success(f"'{selected_task.description}' marked done. Next occurrence scheduled.")
        else:
            st.success(f"'{selected_task.description}' marked done.")
else:
    st.info("No pending tasks to complete.")
