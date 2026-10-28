from pawpal_system import Owner, Pet, Task, Scheduler


def build_demo_owner() -> Owner:
    owner = Owner(id="owner-1", name="Sam")

    dog = Pet(id="pet-1", name="Biscuit", species="Dog")
    cat = Pet(id="pet-2", name="Mochi", species="Cat")

    owner.add_pet(dog)
    owner.add_pet(cat)

    dog.add_task(Task(description="Morning walk", time="08:00", frequency="daily"))
    dog.add_task(Task(description="Feed breakfast", time="09:00", frequency="daily"))
    cat.add_task(Task(description="Litter cleaning", time="08:30", frequency="daily"))
    cat.add_task(Task(description="Play session", time="18:00", frequency="daily"))

    return owner


if __name__ == "__main__":
    owner = build_demo_owner()
    scheduler = Scheduler(owner=owner)
    print(scheduler.print_schedule())
