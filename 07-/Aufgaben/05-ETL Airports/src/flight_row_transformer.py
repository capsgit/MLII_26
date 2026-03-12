from datetime import datetime
from models import FlightRecord


def validate_raw_flight(flight: dict) -> tuple[bool, str | None]:
    origin_country = flight.get("departure", {}).get("airport", {}).get("countryCode")
    origin_iata_airport = flight.get("departure", {}).get("airport", {}).get("iata")
    flight_number = flight.get("number")
    airline_name = flight.get("airline", {}).get("name")
    arrival_info = flight.get("arrival", {}).get("scheduledTime", {}).get("local")

    if not origin_country:
        return False, "missing origin_country"
    if not origin_iata_airport:
        return False, "missing origin_iata_airport"
    if not flight_number:
        return False, "missing flight_number"
    if not airline_name:
        return False, "missing airline_name"
    if not arrival_info:
        return False, "missing arrival_info"

    return True, None

def transform_flights(raw_flights: list[dict], destination_airport: str) -> tuple[list[FlightRecord], dict]:
    records = []
    report = {
        "raw_total": len(raw_flights),
        "valid_total": 0,
        "skipped_total": 0,
        "skip_reasons": {}
    }

    for flight in raw_flights:
        is_valid, reason = validate_raw_flight(flight)

        if not is_valid:
            report["skipped_total"] += 1
            report["skip_reasons"][reason] = report["skip_reasons"].get(reason, 0) + 1
            continue

        arrival_info = flight["arrival"]["scheduledTime"]["local"]
        arrival_dt = datetime.fromisoformat(arrival_info)

        record = FlightRecord(
            origin_country=flight["departure"]["airport"]["countryCode"],
            origin_iata_airport=flight["departure"]["airport"]["iata"],
            destination_airport=destination_airport,
            flight_number=flight["number"],
            airline_name=flight["airline"]["name"],
            year=arrival_dt.year,
            month=arrival_dt.month,
            day=arrival_dt.day,
            hour=arrival_dt.hour,
            minute=arrival_dt.minute,
            second=arrival_dt.second,
        )
        records.append(record)
        report["valid_total"] += 1

    return records, report