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


st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="wide")

st.title("🐾 PawPal+")

st.markdown(
    """
PawPal+ is a pet care planning assistant that stores pets, tasks, and a daily schedule.
Use the forms below to add pets, assign tasks, and generate a plan.
"""
)

owner = get_owner()
scheduler = get_scheduler()


def get_pet_name_for_task(task: Task) -> str:
    """Return the pet name associated with a task instance."""
    for pet in owner.pets:
        if task in pet.tasks:
            return pet.name
    return "Unknown pet"


def format_task_records(task_records: list[dict]) -> list[dict]:
    """Format scheduler task records for display."""
    formatted_rows = []
    for task in task_records:
        due_label = task["due_date"] or "today"
        formatted_rows.append(
            {
                "pet": task["pet_name"],
                "description": task["description"],
                "time": task["scheduled_time"] or "flexible",
                "due": due_label,
                "duration": task["duration"],
                "frequency": task["frequency"],
                "priority": task["priority"],
                "completed": "Yes" if task["completed"] else "No",
            }
        )
    return formatted_rows


def render_task_actions(task_records: list[dict], empty_message: str, key_prefix: str) -> None:
    """Render task rows with complete and remove actions."""
    if not task_records:
        st.warning(empty_message)
        return

    for task in task_records:
        time_label = task["scheduled_time"] or "flexible"
        due_label = task["due_date"] or "today"
        details_col, complete_col, remove_col = st.columns([7, 1.5, 1.5])

        with details_col:
            st.write(
                f'**{task["pet_name"]}** | {task["description"]} | '
                f'{task["duration"]} min | {task["frequency"]} | '
                f'priority {task["priority"]} | {time_label} | due {due_label}'
            )

        with complete_col:
            if not task["completed"] and st.button(
                "Complete",
                key=f'{key_prefix}_complete_{task["task_id"]}',
                use_container_width=True,
            ):
                task_completed = scheduler.mark_task_complete(task["task_id"], task["pet_name"])
                if task_completed:
                    if task["frequency"] in {"daily", "weekly"}:
                        st.success(
                            f'Completed "{task["description"]}" for {task["pet_name"]}. '
                            f'A new {task["frequency"]} task was created for the next occurrence.'
                        )
                    else:
                        st.success(f'Completed "{task["description"]}" for {task["pet_name"]}.')
                    st.rerun()
                st.error("Unable to complete that task.")

        with remove_col:
            if st.button(
                "Remove",
                key=f'{key_prefix}_remove_{task["task_id"]}',
                use_container_width=True,
            ):
                task_removed = scheduler.remove_task(task["task_id"], task["pet_name"])
                if task_removed:
                    st.success(f'Removed "{task["description"]}" for {task["pet_name"]}.')
                    st.rerun()
                st.error("Unable to remove that task.")

st.divider()

# Add custom CSS for column separator
st.markdown(
    """
    <style>
    [data-testid="column"]:first-child {
        border-right: 2px solid #e0e0e0;
        padding-right: 2rem;
    }
    [data-testid="column"]:last-child {
        padding-left: 2rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Create two-column layout for better space utilization
left_col, right_col = st.columns([1, 1])

# LEFT COLUMN: Owner and Pet Management
with left_col:
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
            pet_added = owner.add_pet(Pet(name=pet_name.strip(), type=species, age=int(pet_age)))
            if pet_added:
                st.success(f"Added {pet_name.strip()}.")
            else:
                st.error("A pet with that name already exists. Please enter a different name.")
        else:
            st.error("Enter a pet name before adding a pet.")

    if owner.pets:
        st.write("Current pets:")
        for index, pet in enumerate(owner.pets):
            details_col, remove_col = st.columns([7, 1.5])
            with details_col:
                st.write(f'**{pet.name}** | {pet.type} | age {pet.age} | {len(pet.tasks)} task(s)')
            with remove_col:
                if st.button("Remove", key=f"remove_pet_{index}_{pet.name}", use_container_width=True):
                    pet_removed = owner.remove_pet(pet.name)
                    if pet_removed:
                        st.success(f"Removed {pet.name}.")
                        st.rerun()
                    st.error("Unable to remove that pet.")
    else:
        st.info("No pets yet. Add one above.")

# RIGHT COLUMN: Task Management
with right_col:
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

    st.divider()

    all_tasks = scheduler.get_all_tasks()
    if all_tasks:
        st.write("Task overview")
        pending_tasks = scheduler.filter_tasks(completed=False)
        completed_tasks = scheduler.filter_tasks(completed=True)
        st.caption("Recurring daily and weekly tasks create the next occurrence when completed.")

        if pending_tasks:
            st.success(f"{len(pending_tasks)} pending task(s) ready to schedule.")
        else:
            st.warning("No pending tasks are available to schedule.")

        if completed_tasks:
            st.info(f"{len(completed_tasks)} completed task(s) recorded.")

        all_tab, pending_tab, completed_tab = st.tabs(["Sorted tasks", "Pending", "Completed"])

        with all_tab:
            render_task_actions(
                [
                    {
                        "task_id": task.task_id,
                        "pet_name": get_pet_name_for_task(task),
                        "description": task.description,
                        "duration": task.duration,
                        "frequency": task.frequency,
                        "priority": task.priority,
                        "scheduled_time": task.scheduled_time,
                        "due_date": task.due_date.isoformat() if task.due_date else "",
                        "completed": task.completed,
                    }
                    for task in scheduler.sort_by_time(all_tasks)
                ],
                "No tasks to display.",
                "sorted",
            )

        with pending_tab:
            render_task_actions(pending_tasks, "No pending tasks to display.", "pending")

        with completed_tab:
            if completed_tasks:
                st.table(format_task_records(completed_tasks))
            else:
                st.warning("No completed tasks to display yet.")

        for warning in scheduler.detect_conflicts():
            st.warning(warning)
    else:
        st.info("No tasks yet. Add one above.")

st.divider()

st.subheader("Current Plan")
plan = scheduler.generate_plan()
if plan["warnings"]:
    for warning in plan["warnings"]:
        st.warning(warning)

if plan["scheduled_tasks"]:
    st.text(scheduler.display_plan())
    st.caption(plan["explanation"])
    if plan["unscheduled_tasks"]:
        st.write("Unscheduled tasks:")
        st.table(
            [
                {
                    "pet_name": task["pet_name"],
                    "description": task["description"],
                    "duration": task["duration"],
                    "frequency": task["frequency"],
                    "priority": task["priority"],
                    "scheduled_time": task["scheduled_time"] or "flexible",
                    "due": task["due_date"] or "today",
                }
                for task in plan["unscheduled_tasks"]
            ]
        )
else:
    st.warning("No tasks were scheduled.")
