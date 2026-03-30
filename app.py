import streamlit as st

from pawpal_system import Owner, Pet, Scheduler, Task


def get_owner() -> Owner:
    """Return the owner stored in session state."""
    if "owner" not in st.session_state:
        st.session_state.owner = Owner(name="Jordan", available_time=60)
    return st.session_state.owner


def get_scheduler() -> Scheduler:
    """Return the scheduler stored in session state."""
    if "scheduler" not in st.session_state:
        st.session_state.scheduler = Scheduler(get_owner())
    return st.session_state.scheduler


st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

st.markdown(
    """
PawPal+ is a pet care planning assistant that stores pets, tasks, and a daily schedule.
Use the forms below to add pets, assign tasks, and generate a plan.
"""
)

owner = get_owner()
scheduler = get_scheduler()

st.divider()

st.subheader("Owner Setup")
owner_name = st.text_input("Owner name", value=owner.name)
available_time = st.number_input(
    "Available time (minutes)", min_value=1, max_value=480, value=owner.available_time
)

owner.name = owner_name
owner.available_time = int(available_time)

st.divider()

st.subheader("Add a Pet")
with st.form("add_pet_form"):
    pet_name = st.text_input("Pet name")
    species = st.selectbox("Species", ["dog", "cat", "other"])
    pet_age = st.number_input("Pet age", min_value=0, max_value=40, value=1)
    add_pet_submitted = st.form_submit_button("Add pet")

if add_pet_submitted:
    if pet_name.strip():
        owner.add_pet(Pet(name=pet_name.strip(), type=species, age=int(pet_age)))
        st.success(f"Added {pet_name.strip()}.")
    else:
        st.error("Enter a pet name before adding a pet.")

if owner.pets:
    st.write("Current pets:")
    st.table(
        [{"name": pet.name, "type": pet.type, "age": pet.age, "tasks": len(pet.tasks)} for pet in owner.pets]
    )
else:
    st.info("No pets yet. Add one above.")

st.divider()

st.subheader("Schedule a Task")
if owner.pets:
    with st.form("add_task_form"):
        pet_options = [pet.name for pet in owner.pets]
        selected_pet_name = st.selectbox("Choose a pet", pet_options)
        task_description = st.text_input("Task description", value="Morning walk")
        duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
        frequency = st.selectbox("Frequency", ["daily", "weekly", "as needed"])
        priority_label = st.selectbox("Priority", ["low", "medium", "high"], index=2)
        scheduled_time = st.text_input("Task time (HH:MM)", value="")
        add_task_submitted = st.form_submit_button("Add task")

    if add_task_submitted:
        priority_map = {"low": 1, "medium": 2, "high": 3}
        selected_pet = next((pet for pet in owner.pets if pet.name == selected_pet_name), None)
        if selected_pet is None:
            st.error("Select a valid pet before adding a task.")
        elif task_description.strip():
            selected_pet.add_task(
                Task(
                    description=task_description.strip(),
                    duration=int(duration),
                    frequency=frequency,
                    priority=priority_map[priority_label],
                    scheduled_time=scheduled_time.strip(),
                )
            )
            st.success(f"Added task for {selected_pet.name}.")
        else:
            st.error("Enter a task description before adding a task.")
else:
    st.info("Add a pet before scheduling tasks.")

all_tasks = owner.get_all_tasks()
if all_tasks:
    st.write("Current tasks:")
    task_rows = []
    for pet in owner.pets:
        for task in pet.tasks:
            task_rows.append(
                {
                    "pet": pet.name,
                    "description": task.description,
                    "time": task.scheduled_time or "flexible",
                    "duration": task.duration,
                    "frequency": task.frequency,
                    "priority": task.priority,
                    "completed": task.completed,
                }
            )
    st.table(task_rows)
else:
    st.info("No tasks yet. Add one above.")

st.divider()

st.subheader("Build Schedule")
if st.button("Generate schedule"):
    plan = scheduler.generate_plan()
    for warning in plan["warnings"]:
        st.warning(warning)
    if plan["scheduled_tasks"]:
        st.text(scheduler.display_plan())
        st.caption(plan["explanation"])
        if plan["unscheduled_tasks"]:
            st.write("Unscheduled tasks:")
            st.table(plan["unscheduled_tasks"])
    else:
        st.warning("No tasks were scheduled.")
