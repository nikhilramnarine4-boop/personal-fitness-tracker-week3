# Author: Nikhil Ramnarine
# Date: November 16, 2026
# Program: Personal Fitness Tracker
# Description: Logs workouts, calculates calorie-burning intensity, displays
#              workout statistics, checks a calorie goal, and analyzes trends.
# Tier attempted: Advanced (includes Base and Intermediate requirements)
#
# TEST RESULTS (verified using the functions in this file):
#   180 calories / 45 minutes -> 4.0 cal/min, Low
#   300 calories / 40 minutes -> 7.5 cal/min, Moderate
#   320 calories / 30 minutes -> 10.7 cal/min, High
#   250 calories / 50 minutes -> 5.0 cal/min, Moderate
#   200 calories / 20 minutes -> 10.0 cal/min, High
#   0 workouts -> "No workouts were logged."
#   1 workout -> "Not enough data" trend
#   [200, 250, 300] -> Improving
#   [400, 300, 200] -> Declining
#   [300, 200, 350] -> Mixed
#   Tied highest calories -> first logged workout wins
#   800 total vs. 1000 goal -> 200 calories short
#   800 total vs. 800 goal -> Goal reached


def calories_per_minute(calories, duration):
    """Return calories burned per minute, rounded to one decimal place."""
    return round(calories / duration, 1)


def get_intensity(rate):
    """Return the intensity level for a calories-per-minute rate."""
    if rate < 5.0:
        return "Low"
    elif rate < 10.0:
        return "Moderate"
    else:
        return "High"


def calculate_total(values):
    """Add the values using a loop instead of the built-in sum function."""
    total = 0
    for value in values:
        total += value
    return total


def calculate_average(values):
    """Return the average of the values, rounded to one decimal place."""
    if len(values) == 0:
        return 0.0
    return round(calculate_total(values) / len(values), 1)


def find_best_workout(names, calories_list):
    """Return the first workout name with the highest calorie burn."""
    if len(names) == 0:
        return "None"
    best_index = 0
    for index in range(1, len(calories_list)):
        if calories_list[index] > calories_list[best_index]:
            best_index = index
    return names[best_index]


def check_goal(total_calories, goal):
    """Return a message indicating whether the calorie goal was reached."""
    if total_calories >= goal:
        return f"Goal reached! You burned {total_calories} calories."
    else:
        return f"{goal - total_calories} calories short of your {goal}-calorie goal."


def format_workout_row(name, duration, calories, width=20):
    """Build one aligned table row using the two base-level functions."""
    rate = calories_per_minute(calories, duration)
    intensity = get_intensity(rate)
    return (f"{name:<{width}} {duration:>8} {calories:>10} "
            f"{rate:>8.1f} c/m   {intensity}")


def print_workout_table(names, durations, calories_list):
    """Print a readable table, adjusting its name column to fit long names."""
    # A nested loop examines the characters of each name to find the width.
    name_width = 20
    for name in names:
        character_count = 0
        for character in name:
            character_count += 1
        if character_count > name_width:
            name_width = character_count

    print("\n===== Workout Table =====")
    print(f"{'Workout':<{name_width}} {'Duration':>8} {'Calories':>10} {'Rate':>12}   Intensity")
    print("-" * (name_width + 45))
    for index in range(len(names)):
        print(format_workout_row(names[index], durations[index],
                                 calories_list[index], name_width))


def analyze_trend(calories_list):
    """Compare consecutive calorie totals to classify the workout trend."""
    if len(calories_list) < 2:
        return "Not enough data"

    increases = 0
    decreases = 0
    for index in range(1, len(calories_list)):
        if calories_list[index] > calories_list[index - 1]:
            increases += 1
        elif calories_list[index] < calories_list[index - 1]:
            decreases += 1

    if increases > 0 and decreases > 0:
        return "Mixed"
    elif decreases == 0:
        return "Improving"
    else:
        return "Declining"


def get_nonnegative_integer(prompt, allow_zero=True):
    """Read a whole number, re-prompting on invalid input."""
    while True:
        response = input(prompt).strip()
        if response.isdigit():
            number = int(response)
            if number > 0 or (allow_zero and number == 0):
                return number
        if allow_zero:
            print("Please enter a non-negative whole number.")
        else:
            print("Please enter a whole number greater than zero.")


def print_session_summary(names, durations, calories_list, goal):
    """Display the workout table and all calculated session statistics."""
    print_workout_table(names, durations, calories_list)
    total_calories = calculate_total(calories_list)
    print("\n===== Session Summary =====")
    print(f"Workouts logged : {len(names)}")
    print(f"Total calories  : {total_calories}")
    print(f"Avg calories    : {calculate_average(calories_list):.1f}")
    print(f"Avg duration    : {calculate_average(durations):.1f} min")
    print(f"Best workout    : {find_best_workout(names, calories_list)}")
    print(f"Effort trend    : {analyze_trend(calories_list)}")
    print(f"Goal check      : {check_goal(total_calories, goal)}")
    print("===========================")


def main():
    """Ask for a goal, log workouts until done, and show the summary."""
    print("Welcome to the Personal Fitness Tracker!")
    print("Log workouts and type 'done' when finished.\n")
    goal = get_nonnegative_integer("Daily calorie burn goal: ")

    workout_names = []
    workout_durations = []
    workout_calories = []

    while True:
        print(f"\n--- Workout {len(workout_names) + 1} ---")
        name = input("Workout name (or 'done'): ").strip()
        if name.lower() == "done":
            break
        if name == "":
            print("Please enter a workout name.")
            continue

        duration = get_nonnegative_integer("Duration (minutes): ", False)
        calories = get_nonnegative_integer("Calories burned: ")
        workout_names.append(name)
        workout_durations.append(duration)
        workout_calories.append(calories)

        rate = calories_per_minute(calories, duration)
        intensity = get_intensity(rate)
        print(f"Result: {name} | {duration} min | {calories} cal | "
              f"{rate:.1f} cal/min | Intensity: {intensity}")

    if len(workout_names) == 0:
        print("\nNo workouts were logged.")
    else:
        print_session_summary(workout_names, workout_durations,
                              workout_calories, goal)
        print("\nAll workouts logged. Great job staying active!")


if __name__ == "__main__":
    main()
