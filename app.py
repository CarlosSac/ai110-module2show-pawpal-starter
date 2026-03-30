import streamlit as st
from pawpal_system import Owner, Pet, Task, Scheduler

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

st.divider()

st.subheader("Owner & Pet Info")
owner_name = st.text_input("Owner name", value="Jordan")
available_minutes = st.number_input("Time available today (minutes)", min_value=10, max_value=480, value=90)
pet_name = st.text_input("Pet name", value="Mochi")
species = st.selectbox("Species", ["dog", "cat", "other"])

# Initialize owner and pet in session state
if "owner" not in st.session_state:
    st.session_state.owner = Owner(owner_name, available_minutes)

if "pet" not in st.session_state:
    st.session_state.pet = Pet(pet_name, species)
    st.session_state.owner.add_pet(st.session_state.pet)

st.markdown("### Tasks")

col1, col2, col3 = st.columns(3)
with col1:
    task_description = st.text_input("Task description", value="Morning walk")
with col2:
    duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
with col3:
    priority = st.selectbox("Priority", ["low", "medium", "high"], index=2)

if st.button("Add task"):
    task = Task(task_description, int(duration), priority)
    st.session_state.pet.add_task(task)
    st.success(f"Added: {task}")

pending = st.session_state.pet.get_pending_tasks()
if pending:
    st.write("Current tasks:")
    st.table([{"description": t.description, "duration (min)": t.duration_minutes, "priority": t.priority} for t in pending])
else:
    st.info("No tasks yet. Add one above.")

st.divider()

st.subheader("Build Schedule")
if st.button("Generate schedule"):
    scheduler = Scheduler(st.session_state.owner)
    schedule = scheduler.build_schedule()
    if schedule:
        st.success("Schedule generated!")
        st.text(scheduler.explain_schedule(schedule))
    else:
        st.warning("No tasks could be scheduled. Add tasks or increase available time.")
