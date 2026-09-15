import json
import os
from datetime import date, timedelta

DATA_FILE = "habits.json"


# -----------------------------
# Load and save data
# -----------------------------
def load_data():
    if not os.path.exists(DATA_FILE):
        return []

    try:
        with open(DATA_FILE, "r") as file:
            return json.load(file)
    except (json.JSONDecodeError, FileNotFoundError):
        return []


def save_data(habits):
    with open(DATA_FILE, "w") as file:
        json.dump(habits, file, indent=4)


# -----------------------------
# Calculate streak
# -----------------------------
def calculate_streak(completed_dates):
    if not completed_dates:
        return 0

    completed = sorted(
        [date.fromisoformat(d) for d in completed_dates],
        reverse=True
    )

    today = date.today()

    # Streak can continue from today or yesterday
    if completed[0] == today:
        current_date = today
    elif completed[0] == today - timedelta(days=1):
        current_date = today - timedelta(days=1)
    else:
        return 0

    streak = 0

    completed_set = set(completed)

    while current_date in completed_set:
        streak += 1
        current_date -= timedelta(days=1)

    return streak


# -----------------------------
# Add habit
# -----------------------------
def add_habit(habits):
    print("\n--- Add New Habit ---")

    name = input("Enter habit name: ").strip()

    if not name:
        print("Habit name cannot be empty.")
        return

    description = input("Enter habit description: ").strip()

    habit = {
        "name": name,
        "description": description,
        "completed_dates": []
    }

    habits.append(habit)

    save_data(habits)

    print(f"\nHabit '{name}' added successfully!")


# -----------------------------
# Daily check-in
# -----------------------------
def check_in(habits):
    if not habits:
        print("\nNo habits available. Add a habit first.")
        return

    print("\n--- Daily Check-In ---")

    for index, habit in enumerate(habits, start=1):
        print(f"{index}. {habit['name']}")

    try:
        choice = int(input("\nSelect habit number: "))

        if choice < 1 or choice > len(habits):
            print("Invalid choice.")
            return

    except ValueError:
        print("Please enter a valid number.")
        return

    selected_habit = habits[choice - 1]

    today = date.today().isoformat()

    if today in selected_habit["completed_dates"]:
        print(
            f"\n'{selected_habit['name']}' is already completed today!"
        )
        return

    selected_habit["completed_dates"].append(today)

    save_data(habits)

    streak = calculate_streak(selected_habit["completed_dates"])

    print(
        f"\nGreat! '{selected_habit['name']}' completed for today."
    )

    print(f"Current streak: {streak} day(s) 🔥")


# -----------------------------
# View progress
# -----------------------------
def view_progress(habits):
    print("\n--- Habit Progress ---")

    if not habits:
        print("No habits found.")
        return

    print("-" * 60)

    for index, habit in enumerate(habits, start=1):

        streak = calculate_streak(
            habit["completed_dates"]
        )

        print(f"Habit {index}")
        print(f"Name        : {habit['name']}")
        print(f"Description : {habit['description']}")
        print(f"Streak      : {streak} day(s)")
        print(
            f"Total Days  : {len(habit['completed_dates'])}"
        )

        print("-" * 60)


# -----------------------------
# Main application
# -----------------------------
def main():

    habits = load_data()

    while True:

        print("\n==============================")
        print("      DAILY HABIT TRACKER")
        print("==============================")

        print("1. Add Habit")
        print("2. Daily Check-In")
        print("3. View Progress")
        print("4. Exit")

        choice = input("\nChoose an option (1-4): ").strip()

        if choice == "1":
            add_habit(habits)

        elif choice == "2":
            check_in(habits)

        elif choice == "3":
            view_progress(habits)

        elif choice == "4":
            print("\nThanks for using Habit Tracker!")
            print("Keep building good habits! 👋")
            break

        else:
            print("\nInvalid option. Please choose 1-4.")


if __name__ == "__main__":
    main()