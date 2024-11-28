import os

# Determine the base path dynamically (where the script is located)
base_path = os.path.dirname(os.path.abspath(__file__))
race_files_path = os.path.join(base_path, "Race_Files")


def read_integer_between_numbers(prompt, mini, maximum):
    while True:
        try:
            users_input = int(input(prompt))
            if mini <= users_input <= maximum:
                return users_input
            else:
                print(f"Numbers from {mini} to {maximum} only.")
        except ValueError:
            print("Sorry - numbers only please.")


def read_nonempty_string(prompt):
    while True:
        users_input = input(prompt)
        if len(users_input) > 0 and users_input.isalpha():
            return users_input
        else:
            print("Please enter a valid string containing only letters.")


def read_integer(prompt):
    while True:
        try:
            users_input = int(input(prompt))
            if users_input >= 0:
                return users_input
            else:
                print("Please enter a non-negative number.")
        except ValueError:
            print("Sorry - numbers only please.")


def runners_data():
    runners_file = os.path.join(base_path, "Runners.txt")
    with open(runners_file) as input_file:
        lines = input_file.readlines()
    runners_name = []
    runners_id = []
    for line in lines:
        line = line.strip()
        if line:
            split_line = line.split(",")
            if len(split_line) == 2:
                runners_name.append(split_line[0].strip())
                runners_id.append(split_line[1].strip())
    return runners_name, runners_id


def race_venues():
    races_file = os.path.join(base_path, "Races.txt")
    with open(races_file) as input_file:
        lines = input_file.readlines()
    races_location = [line.split(",")[0].strip() for line in lines if line.strip()]
    return races_location


def reading_race_results(location):
    file_path = os.path.join(race_files_path, f"{location}.txt")
    with open(file_path) as input_file:
        lines = input_file.readlines()
    ids = []
    time_taken = []
    for line in lines:
        split_line = line.strip().split(",")
        if len(split_line) == 2:
            ids.append(split_line[0].strip())
            time_taken.append(int(split_line[1].strip()))
    return ids, time_taken


def winner_of_race(ids, time_taken):
    quickest_time = min(time_taken)
    for i in range(len(ids)):
        if quickest_time == time_taken[i]:
            return ids[i]
    return None


def podium_places(ids, time_taken):
    sorted_times = sorted((time, id_) for time, id_ in zip(time_taken, ids))
    return [sorted_times[i][1] for i in range(min(3, len(sorted_times)))]


def display_races(ids, time_taken, venue):
    MINUTE = 60
    print(f"Results for {venue}")
    print("=" * 37)
    for i in range(len(ids)):
        minutes = time_taken[i] // MINUTE
        seconds = time_taken[i] % MINUTE
        print(f"{ids[i]:<10s} {minutes} minutes and {seconds} seconds")
    print("\nPodium Places:")
    podium = podium_places(ids, time_taken)
    for idx, id_ in enumerate(podium, 1):
        print(f"{idx}. {id_}")


def add_results_for_race(races_location, runners_id):
    new_race = read_nonempty_string("Enter the venue for the new race: ").capitalize()
    if new_race in races_location:
        print("Race already exists.")
        return

    races_location.append(new_race)
    with open(os.path.join(race_files_path, f"{new_race}.txt"), "w") as race_file:
        print("Enter race times for each runner. (Enter 0 if the runner did not participate)")
        for runner_id in runners_id:
            time = read_integer(f"Time for {runner_id} (in seconds): ")
            if time > 0:
                race_file.write(f"{runner_id},{time}\n")

    with open(os.path.join(base_path, "Races.txt"), "w") as races_file:
        for race in races_location:
            races_file.write(race + "\n")
    print("Race results added successfully.")


def competitors_by_county(runners_name, runners_id):
    county_runners = {}
    for name, id_ in zip(runners_name, runners_id):
        county = id_.split("-")[0]
        if county not in county_runners:
            county_runners[county] = []
        county_runners[county].append(f"{name} ({id_})")

    for county in sorted(county_runners.keys()):
        print(f"{county} Runners:")
        print("=" * 20)
        for runner in sorted(county_runners[county]):
            print(runner)


def displaying_winners_of_each_race(races_location):
    print("Venue             Podium Places")
    print("=" * 35)
    for race in races_location:
        ids, time_taken = reading_race_results(race)
        podium = podium_places(ids, time_taken)
        print(f"{race:<18s}{', '.join(podium)}")


def show_race_times_and_positions(races_location, runners_name, runners_id):
    runner_name, runner_id = relevant_runner_info(runners_name, runners_id)
    print(f"\nRace times and positions for {runner_name} ({runner_id}):")
    print("=" * 50)

    found_races = False
    for race in races_location:
        ids, times = reading_race_results(race)
        if runner_id in ids:
            found_races = True
            time = times[ids.index(runner_id)]
            position = sorted(times).index(time) + 1
            minutes, seconds = divmod(time, 60)
            print(f"{race:<15} {minutes} minutes {seconds} seconds (Position: {position})")

    if not found_races:
        print("This runner has not participated in any races.")


def show_winners(races_location, runners_name, runners_id):
    winners = set()
    for race in races_location:
        ids, times = reading_race_results(race)
        if ids and times:
            fastest_runner = winner_of_race(ids, times)
            winners.add(fastest_runner)

    print("\nCompetitors who have won at least one race:")
    print("=" * 50)
    for runner_id in winners:
        if runner_id in runners_id:
            index = runners_id.index(runner_id)
            print(f"{runners_name[index]} ({runner_id})")


def relevant_runner_info(runners_name, runners_id):
    print("Select a runner:")
    for idx, name in enumerate(runners_name, 1):
        print(f"{idx}: {name}")
    user_choice = read_integer_between_numbers("Choice: ", 1, len(runners_name))
    return runners_name[user_choice - 1], runners_id[user_choice - 1]


def non_podium_finishers(races_location, runners_id):
    podium_ids = set()
    for race in races_location:
        ids, time_taken = reading_race_results(race)
        podium_ids.update(podium_places(ids, time_taken))

    non_podium_runners = [id_ for id_ in runners_id if id_ not in podium_ids]
    return non_podium_runners


def main():
    races_location = race_venues()
    runners_name, runners_id = runners_data()
    MENU = (
        "1. Show the results for a race\n"
        "2. Add results for a race\n"
        "3. Show all competitors by county\n"
        "4. Show the podium-places for each race\n"
        "5. Show all the race times and positions for a competitor\n"
        "6. Show all competitors who have won a race\n"
        "7. Show all competitors who have not taken a podium position\n"
        "8. Quit\n>>> "
    )

    while True:
        choice = read_integer_between_numbers(MENU, 1, 8)

        if choice == 1:
            for idx, race in enumerate(races_location, 1):
                print(f"{idx}: {race}")
            selected_race_idx = read_integer_between_numbers(
                "Select a race: ", 1, len(races_location)
            )
            race = races_location[selected_race_idx - 1]
            ids, time_taken = reading_race_results(race)
            display_races(ids, time_taken, race)
        elif choice == 2:
            add_results_for_race(races_location, runners_id)
        elif choice == 3:
            competitors_by_county(runners_name, runners_id)
        elif choice == 4:
            displaying_winners_of_each_race(races_location)
        elif choice == 5:
            show_race_times_and_positions(races_location, runners_name, runners_id)
        elif choice == 6:
            show_winners(races_location, runners_name, runners_id)
        elif choice == 7:
            non_podium = non_podium_finishers(races_location, runners_id)
            print("Non-podium Finishers:")
            for runner in non_podium:
                print(runner)
        elif choice == 8:
            print("Goodbye!")
            break


if __name__ == "__main__":
    main()
