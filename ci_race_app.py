def read_integer_between_numbers(prompt, mini, maximum):
    while True:
        try:
            users_input = int(input(prompt))
            if mini <= users_input <= maximum:
                return users_input
            else:
                print(f"Numbers from {mini} to {maximum} only.")
        except ValueError:
            print("Sorry - numbers only please")

def read_nonempty_string(prompt):
    while True:
        users_input = input(prompt)
        if len(users_input) > 0 and users_input.isalpha():
            return users_input
        print("Please enter a valid string.")

def read_integer(prompt):
    while True:
        try:
            users_input = int(input(prompt))
            if users_input >= 0:
                return users_input
        except ValueError:
            print("Sorry - numbers only please")

def runners_data():
    with open("Runners.txt") as input:
        lines = input.readlines()
    runners_name = []
    runners_id = []
    for line in lines:
        split_line = line.strip().split(",")
        runners_name.append(split_line[0])
        runners_id.append(split_line[1])
    return runners_name, runners_id

def race_venues():
    with open("Races.txt") as input:
        lines = input.readlines()
    races_location = []
    for line in lines:
        races_location.append(line.strip().split(",")[0])
    return races_location

def reading_race_results(location):
    with open(f"{location}.txt") as input_type:
        lines = input_type.readlines()
    id = []
    time_taken = []
    for line in lines:
        split_line = line.strip().split(",")
        id.append(split_line[0])
        time_taken.append(int(split_line[1]))
    return id, time_taken

def winner_of_race(id, time_taken):
    quickest_time = min(time_taken)
    for i in range(len(id)):
        if quickest_time == time_taken[i]:
            return id[i]

def display_races(id, time_taken, venue, fastest_runner):
    print(f"\nResults for {venue}")
    print("=" * 30)
    for i in range(len(id)):
        minutes, seconds = divmod(time_taken[i], 60)
        print(f"{id[i]}: {minutes} minutes and {seconds} seconds")
    print(f"\n{fastest_runner} won the race!")

def main():
    races_location = race_venues()
    runners_name, runners_id = runners_data()
    MENU = (
        "1. Show the results for a race\n"
        "2. Quit\n>>> "
    )
    
    while True:
        input_menu = read_integer_between_numbers(MENU, 1, 2)
        if input_menu == 1:
            venue = race_venues()[read_integer_between_numbers("Select race (1-5): ", 1, 5) - 1]
            id, time_taken = reading_race_results(venue)
            fastest_runner = winner_of_race(id, time_taken)
            display_races(id, time_taken, venue, fastest_runner)
        elif input_menu == 2:
            print("Goodbye!")
            break

main()
