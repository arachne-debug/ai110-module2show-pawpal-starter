import streamlit as st

from pawpal_system import Owner, Pet, Scheduler, Task

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

if "owner" not in st.session_state:
    st.session_state.owner = Owner(id="owner-1", name="Jordan")

owner = st.session_state.owner

st.title("🐾 PawPal+")

st.markdown(
    """
Welcome to PawPal+. This app keeps your pet-care data in the browser session so your owner and pet records persist while you use the app.
"""
)

with st.expander("Scenario", expanded=True):
    st.markdown(
        """
**PawPal+** is a pet care planning assistant. It helps a pet owner plan care tasks
for their pet(s) based on constraints like time, priority, and preferences.
"""
    )

st.divider()

st.subheader("Owner")
owner_name = st.text_input("Owner name", value=owner.name)
if owner_name != owner.name:
    owner.name = owner_name
    st.session_state.owner = owner

st.subheader("Add a Pet")
with st.form("add_pet_form"):
    pet_name = st.text_input("Pet name", value="")
    species = st.selectbox("Species", ["dog", "cat", "other"])
    submitted_pet = st.form_submit_button("Add pet")

if submitted_pet and pet_name.strip():
    pet = Pet(id=f"pet-{len(owner.pets) + 1}", name=pet_name.strip(), species=species)
    owner.add_pet(pet)
    st.session_state.owner = owner
    st.success(f"Added {pet.name} to {owner.name}'s pets.")

if owner.pets:
    st.subheader("Your Pets")
    for pet in owner.pets:
        st.write(f"- {pet.name} ({pet.species})")
else:
    st.info("No pets yet. Add one above.")

st.divider()

st.subheader("Add a Task")
if owner.pets:
    with st.form("add_task_form"):
        pet_choice = st.selectbox("Select pet", [pet.name for pet in owner.pets])
        task_title = st.text_input("Task title", value="Morning walk")
        task_time = st.text_input("Time", value="08:00")
        frequency = st.selectbox("Frequency", ["daily", "weekly", "as needed"])
        submitted_task = st.form_submit_button("Add task")

    if submitted_task:
        selected_pet = next(pet for pet in owner.pets if pet.name == pet_choice)
        task = Task(description=task_title.strip(), time=task_time.strip(), frequency=frequency)
        selected_pet.add_task(task)
        st.session_state.owner = owner
        st.success(f"Added '{task.description}' for {selected_pet.name}.")
else:
    st.info("Add a pet before creating tasks.")

st.divider()

st.subheader("Today's Schedule")
scheduler = Scheduler(owner=owner)
if owner.pets:
    schedule = scheduler.get_today_schedule()
    if schedule:
        for task in schedule:
            pet = next((pet for pet in owner.pets if task in pet.tasks), None)
            pet_name = pet.name if pet else "Unknown pet"
            st.write(f"- {task.time} | {pet_name} | {task.description} | {'Done' if task.completed else 'Pending'}")
    else:
        st.info("No tasks scheduled yet.")
else:
    st.info("No pets available to schedule.")

st.divider()

st.subheader("Quick Demo Inputs")
if st.button("Generate schedule"):
    st.write(scheduler.print_schedule())
