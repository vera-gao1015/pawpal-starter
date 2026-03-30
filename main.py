from pawpal_system import Owner, Pet, Scheduler, Task


def main() -> None:
    owner = Owner(name="Vera", available_time=60)

    maomao = Pet(name="Maomao", type="cat", age=3)
    luna = Pet(name="Luna", type="cat", age=5)

    maomao.add_task(Task(description="Morning walk", duration=20, frequency="daily", priority=3))
    maomao.add_task(Task(description="Breakfast", duration=10, frequency="daily", priority=2))
    luna.add_task(Task(description="Litter cleaning", duration=15, frequency="daily", priority=2))
    luna.add_task(Task(description="Play time", duration=25, frequency="daily", priority=1))

    owner.add_pet(maomao)
    owner.add_pet(luna)

    scheduler = Scheduler(owner)
    plan = scheduler.generate_plan()

    print("Today's Schedule")
    print("================")
    print(scheduler.display_plan())
    print()
    print("Explanation:")
    print(plan["explanation"])


if __name__ == "__main__":
    main()
