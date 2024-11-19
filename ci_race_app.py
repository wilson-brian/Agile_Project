races = {
    "Kinsale": [("CK-24", 3040), ("KY-43", 2915)],
    "Castletownbere": [("CK-11", 3245), ("CK-23", 2900)]
}

runners = {
    "CK-24": "Anna Fox",
    "KY-43": "Ann Cahill",
    "CK-11": "Joe Flynn",
    "CK-23": "Des Kelly"
}

def show_race_results():
    print("\nAvailable Races:")
    for idx, race in enumerate(races, 1):
        print(f"{idx}. {race}")
    
    choice = int(input("Select a race by number: "))
    race_name = list(races.keys())[choice - 1]
    
    print(f"\nResults for {race_name}:")
    for runner_id, time in races[race_name]:
        minutes, seconds = divmod(time, 60)
        print(f"{runners[runner_id]} ({runner_id}): {minutes}m {seconds}s")


