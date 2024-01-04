from f1_racing_reports.report import parse_logs, load_abbreviations, RacerData


start_log_file = "inputs/start.log"
end_log_file = "inputs/end.log"
abbreviations_file_path = "inputs/abbreviations.txt"

abbreviations = load_abbreviations(abbreviations_file_path)

top_racers, remaining_racers = parse_logs(start_log_file, end_log_file, abbreviations)


def reformat_racers_to_dict(racers: list[RacerData]) -> list[dict]:
    result = list()
    for racer in racers:
        new_racer = dict()
        new_racer["name"] = racer.name
        new_racer["team"] = racer.team
        new_racer["lap_time"] = racer.lap_time
        new_racer["driver_id"] = racer.driver_id
        result.append(new_racer)
    return result


def get_report(order: str = None) -> list | None:
    if order == "asc":
        return top_racers + remaining_racers
    elif order == "desc":
        return remaining_racers[::-1] + top_racers[::-1]


def get_driver_list(order: str = None) -> list | None:
    if order == "asc":
        return sorted(abbreviations, key=lambda x: x[1])
    elif order == "desc":
        return sorted(abbreviations, key=lambda x: x[1], reverse=True)
