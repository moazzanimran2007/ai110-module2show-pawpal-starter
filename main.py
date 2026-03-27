"""Temporary terminal script to exercise pawpal_system scheduling logic."""

from __future__ import annotations

from datetime import date

from pawpal_system import ConstraintSet, Owner, PawPalAppController, Pet, TaskRepository


def _build_controller(owner: Owner, pet: Pet) -> PawPalAppController:
    return PawPalAppController(owner=owner, pet=pet, task_repo=TaskRepository())


def main() -> None:
    owner = Owner(
        owner_id="o-demo",
        name="Alex Rivera",
        available_minutes_per_day=240,
        preferences={"preferred_categories": ["walk", "feeding"]},
    )

    pet_dog = Pet(pet_id="p-dog", name="Mochi", species="dog", age_years=3.0)
    pet_cat = Pet(pet_id="p-cat", name="Nimbus", species="cat", age_years=2.0)

    # Dog: two tasks with different durations
    dog_ctrl = _build_controller(owner, pet_dog)
    dog_ctrl.task_repo.add_task(
        PawPalAppController.new_task(
            "Morning walk", duration_minutes=35, priority="high", category="walk", is_required=True
        )
    )
    dog_ctrl.task_repo.add_task(
        PawPalAppController.new_task(
            "Training session", duration_minutes=20, priority="medium", category="enrichment"
        )
    )

    # Cat: two more tasks — total four tasks, all distinct durations across pets
    cat_ctrl = _build_controller(owner, pet_cat)
    cat_ctrl.task_repo.add_task(
        PawPalAppController.new_task(
            "Feed breakfast", duration_minutes=15, priority="high", category="feeding", is_required=True
        )
    )
    cat_ctrl.task_repo.add_task(
        PawPalAppController.new_task(
            "Brush coat", duration_minutes=25, priority="low", category="grooming"
        )
    )

    constraints = ConstraintSet(
        max_daily_minutes=owner.available_minutes_per_day,
        must_include_categories=["feeding"],
        preferred_categories=list(owner.preferences.get("preferred_categories", [])),
    )

    today = date.today().isoformat()

    print("Today's Schedule")
    print("================")

    for label, ctrl in (("Mochi (dog)", dog_ctrl), ("Nimbus (cat)", cat_ctrl)):
        plan = ctrl.create_daily_plan(constraints, target_date=today)
        print(f"\n{label} — {plan.date}")
        if not plan.items:
            print("  (no tasks scheduled)")
            continue
        for item in plan.items:
            print(
                f"  {item.start_time}–{item.end_time}  {item.task.title}  "
                f"({item.task.duration_minutes} min, {item.task.priority}) — {item.reason}"
            )
        print(f"  Total: {plan.total_minutes} min planned, {plan.leftover_minutes} min free")


if __name__ == "__main__":
    main()
