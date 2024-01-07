# tests/test_package_interaction.py

from f1_racing_reports.report import RacerData

from src.package_interaction import reformat_racers_to_dict, get_report, get_driver_list


def test_reformat_racers_to_dict():
    # Assuming some test data
    racers = [
        RacerData(name="Driver1", team="Team1", lap_time="1:30.000", driver_id="ID1"),
        RacerData(name="Driver2", team="Team2", lap_time="1:35.000", driver_id="ID2"),
    ]

    expected_result = [
        {
            "name": "Driver1",
            "team": "Team1",
            "lap_time": "1:30.000",
            "driver_id": "ID1",
        },
        {
            "name": "Driver2",
            "team": "Team2",
            "lap_time": "1:35.000",
            "driver_id": "ID2",
        },
    ]

    assert reformat_racers_to_dict(racers) == expected_result


def test_get_report():
    # Assuming some test data
    top_racers = [
        RacerData(name="Driver1", team="Team1", lap_time="1:30.000", driver_id="ID1")
    ]
    remaining_racers = [
        RacerData(name="Driver2", team="Team2", lap_time="1:35.000", driver_id="ID2")
    ]

    expected_result = [
        {
            "name": "Driver1",
            "team": "Team1",
            "lap_time": "1:30.000",
            "driver_id": "ID1",
        },
        {
            "name": "Driver2",
            "team": "Team2",
            "lap_time": "1:35.000",
            "driver_id": "ID2",
        },
    ]

    assert get_report("asc", top_racers, remaining_racers) == expected_result
    assert get_report("desc", top_racers, remaining_racers) == expected_result[::-1]


def test_get_driver_list():
    # Assuming some test data
    abbreviations = [["ID1", "Driver1", "Team1"], ["ID2", "Driver2", "Team2"]]

    expected_result_asc = [
        {"driver_id": "ID1", "name": "Driver1", "team": "Team1"},
        {"driver_id": "ID2", "name": "Driver2", "team": "Team2"},
    ]

    expected_result_desc = [
        {"driver_id": "ID2", "name": "Driver2", "team": "Team2"},
        {"driver_id": "ID1", "name": "Driver1", "team": "Team1"},
    ]

    assert get_driver_list("asc", abbreviations) == expected_result_asc
    assert get_driver_list("desc", abbreviations) == expected_result_desc
