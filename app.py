import streamlit as st
from datetime import time
from pawpal_system import Owner, Pet, Task, DailySchedule

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="wide")

st.title("🐾 PawPal+ Pet Care Scheduler")

# Initialize session state
if "schedule" not in st.session_state:
    st.session_state.schedule = DailySchedule()
if "tasks" not in st.session_state:
    st.session_state.tasks = []
if "owner" not in st.session_state:
    st.session_state.owner = None
if "pet" not in st.session_state:
    st.session_state.pet = None

# Owner & Pet Setup
st.subheader("📋 Owner & Pet Information")
col1, col2, col3 = st.columns(3)

with col1:
    owner_name = st.text_input("Owner name", value="Jordan", key="owner_name")
    available_hours = st.number_input("Available hours per day", min_value=0.5, max_value=24.0, value=4.0, key="avail_hours")
    owner_email = st.text_input("Email", value="owner@email.com", key="owner_email")

with col2:
    pet_name = st.text_input("Pet name", value="Mochi", key="pet_name")
    pet_age = st.number_input("Pet age (years)", min_value=0, max_value=50, value=3, key="pet_age")

with col3:
    breed = st.text_input("Breed", value="Golden Retriever", key="breed")
    st.write("")

if st.button("✅ Create Owner & Pet", use_container_width=True):
    st.session_state.owner = Owner(owner_name, owner_email, int(available_hours))
    st.session_state.pet = Pet(pet_name, pet_age, breed, st.session_state.owner)
    st.success(f"✓ Owner '{owner_name}' and pet '{pet_name}' created!")

st.divider()

# Task Management
st.subheader("📝 Add Tasks")
col1, col2, col3, col4 = st.columns(4)

with col1:
    task_title = st.text_input("Task title", value="Morning walk", key="task_title")
with col2:
    task_type = st.selectbox("Task type",
        ["walk", "feeding", "medication", "training", "play", "grooming", "checkup"],
        key="task_type")
with col3:
    duration = st.number_input("Duration (min)", min_value=1, max_value=240, value=30, key="duration")
with col4:
    priority = st.selectbox("Priority", [1, 2, 3, 4, 5], format_func=lambda x: f"{x} - {'Critical' if x==1 else 'High' if x==2 else 'Medium' if x==3 else 'Low' if x==4 else 'Optional'}", key="priority")

col1, col2, col3 = st.columns(3)
with col1:
    frequency = st.selectbox("Frequency", ["daily", "twice_daily", "weekly", "once"], key="frequency")
with col2:
    task_time = st.time_input("Preferred time (optional)", value=None, key="task_time")
with col3:
    st.write("")

if st.button("➕ Add Task", use_container_width=True):
    if st.session_state.pet is None:
        st.error("Please create owner & pet first!")
    else:
        new_task = Task(
            title=task_title,
            task_type=task_type,
            frequency=frequency,
            duration=duration,
            priority=priority,
            time=task_time,
            pet=st.session_state.pet
        )
        st.session_state.schedule.add_task(new_task)
        st.session_state.tasks.append(new_task)
        st.success(f"✓ Task '{task_title}' added!")

# Display current tasks
if st.session_state.tasks:
    st.markdown("### Current Tasks")
    task_data = []
    for task in st.session_state.tasks:
        task_data.append({
            "Title": task.title,
            "Type": task.task_type,
            "Duration (min)": task.duration,
            "Priority": f"P{task.priority}",
            "Frequency": task.frequency,
            "Time": task.time.strftime("%H:%M") if task.time else "—",
            "Status": "✓" if task.is_completed else "○"
        })
    st.table(task_data)
else:
    st.info("No tasks yet. Add one above.")

st.divider()

# Schedule Generation & Display
st.subheader("📅 Generate & View Schedule")

if st.button("🔄 Generate Schedule", use_container_width=True, type="primary"):
    if st.session_state.owner is None:
        st.error("Please create owner & pet first!")
    elif not st.session_state.tasks:
        st.error("Please add at least one task!")
    else:
        # Generate schedule using scheduler logic
        scheduled = st.session_state.schedule.schedule(st.session_state.owner, [st.session_state.pet])

        # Check for conflicts
        conflicts = st.session_state.schedule.detect_scheduling_conflicts()

        # Display validation status
        if st.session_state.schedule.validate():
            st.success("✓ Schedule is valid! All critical tasks included.")
        else:
            errors = st.session_state.schedule.get_validation_errors()
            for error in errors:
                st.warning(f"⚠ {error}")

        # Display conflicts if any
        if conflicts:
            st.warning("⚠ **Scheduling Conflicts Detected:**")
            for conflict in conflicts:
                st.warning(conflict)
        else:
            st.success("✓ No time conflicts detected.")

        # Display schedule as table
        if scheduled:
            st.markdown("### 📍 Your Daily Schedule")
            schedule_data = []
            for task, hour in sorted(scheduled.items(), key=lambda x: x[1]):
                hour_int = int(hour)
                minutes = int((hour % 1) * 60)
                time_str = f"{hour_int:02d}:{minutes:02d}"

                schedule_data.append({
                    "Time": time_str,
                    "Task": task.title,
                    "Type": task.task_type,
                    "Duration": f"{task.duration}m",
                    "Priority": f"P{task.priority}",
                    "Pet": task.pet.name if task.pet else "—"
                })
            st.table(schedule_data)

            # Display schedule explanation
            st.markdown("### 📝 Schedule Explanation")
            explanation = st.session_state.schedule.explain()
            st.code(explanation)
        else:
            st.info("No tasks could be scheduled with available hours.")

st.divider()

# Task Filtering
st.subheader("🔍 Filter & Manage Tasks")
col1, col2 = st.columns(2)

with col1:
    filter_status = st.selectbox("Filter by status", ["All", "Completed", "Incomplete"], key="filter_status")
with col2:
    filter_pet = st.selectbox("Filter by pet", ["All pets"] + [pet.name for pet in [st.session_state.pet] if st.session_state.pet], key="filter_pet")

# Apply filters
is_completed = None if filter_status == "All" else (True if filter_status == "Completed" else False)
pet_name = None if filter_pet == "All pets" else filter_pet

filtered_tasks = st.session_state.schedule.filter_tasks(is_completed=is_completed, pet_name=pet_name)

if filtered_tasks:
    st.markdown("### Filtered Tasks")
    filtered_data = []
    for task in filtered_tasks:
        filtered_data.append({
            "Title": task.title,
            "Type": task.task_type,
            "Duration (min)": task.duration,
            "Priority": f"P{task.priority}",
            "Status": "✓ Completed" if task.is_completed else "○ Incomplete"
        })
    st.table(filtered_data)

    # Mark tasks as complete
    if filter_status != "Completed":
        st.markdown("### ✅ Mark Tasks Complete")
        for idx, task in enumerate(filtered_tasks):
            col1, col2 = st.columns([4, 1])
            with col1:
                st.write(f"{task.title} ({task.task_type})")
            with col2:
                if st.button("Done", key=f"complete_{idx}"):
                    next_task = st.session_state.schedule.mark_task_complete(task)
                    if next_task:
                        st.session_state.tasks.append(next_task)
                        st.success(f"✓ Marked complete! Next occurrence created.")
                    else:
                        st.success(f"✓ Marked complete!")
                    st.rerun()
else:
    st.info("No tasks match the selected filters.")

st.divider()

# System Info
with st.expander("ℹ️ About PawPal+"):
    st.markdown(
        """
**PawPal+** is an intelligent pet care scheduler that:
- **Sorts** tasks by preferred time, frequency, and priority
- **Detects** scheduling conflicts (same-pet or same-time tasks)
- **Validates** that critical tasks fit within available hours
- **Recurs** daily/weekly tasks automatically when marked complete
- **Filters** tasks by completion status and pet name
        """
    )
