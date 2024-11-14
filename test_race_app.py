from ci_race_app import races, runners

def test_races_exist():
    assert len(races) > 0

def test_runners_exist():
    assert len(runners) > 0
