COLLEGE_DAYS_PER_MONTH = 22
SHARED_MODES = {"Auto Rickshaw", "Cab"}

MODES = {
    "Walking": {"base": 0.0, "per_km": 0.0, "speed_kmph": 5.0, "co2_g_per_km": 0},
    "Local Bus": {"base": 10.0, "per_km": 1.5, "speed_kmph": 18.0, "co2_g_per_km": 65},
    "Metro": {"base": 10.0, "per_km": 2.5, "speed_kmph": 32.0, "co2_g_per_km": 30},
    "Auto Rickshaw": {"base": 25.0, "per_km": 17.0, "speed_kmph": 22.0, "co2_g_per_km": 110},
    "Cab": {"base": 50.0, "per_km": 20.0, "speed_kmph": 26.0, "co2_g_per_km": 170},
}


def estimate_trip(distance_km, round_trip=False, riders=1):
    multiplier = 2 if round_trip else 1
    total_km = distance_km * multiplier
    results = []

    for mode, spec in MODES.items():
        total_fare = (spec["base"] + spec["per_km"] * distance_km) * multiplier
        fare = total_fare / riders if mode in SHARED_MODES else total_fare
        monthly_fare = fare * COLLEGE_DAYS_PER_MONTH
        mins = (total_km / spec["speed_kmph"]) * 60
        co2_g = total_km * spec["co2_g_per_km"]
        results.append((mode, fare, monthly_fare, mins, co2_g))

    return total_km, results


def main():
    print("=== Smart Commute & Fare Estimator ===")
    while True:
        try:
            dist = float(input("\nOne-way distance in km (0 to exit): "))
            if dist == 0:
                print("Goodbye!")
                break
            if dist < 0:
                print("Distance cannot be negative.")
                continue
        except ValueError:
            print("Enter a valid number.")
            continue

        rt = input("Round trip? (y/n): ").strip().lower() == "y"

        try:
            riders = int(input("Number of friends sharing auto/cab (1 for solo): "))
            if riders < 1:
                print("Number of people must be at least 1.")
                continue
        except ValueError:
            print("Enter a whole number for people sharing.")
            continue

        total_km, results = estimate_trip(dist, rt, riders)

        cheapest = min(results, key=lambda r: r[1])
        fastest = min(results, key=lambda r: r[3])

        print(
            f"\nTotal Distance: {total_km:.1f} km | Monthly: {COLLEGE_DAYS_PER_MONTH} days | Split: {riders}"
        )
        print(f"{'Mode':<15} {'Trip Fare':<11} {'22-Day Cost':<13} {'Time':<10} {'CO2 (g)'}")
        print("-" * 62)
        for mode, fare, monthly_fare, mins, co2_g in results:
            print(
                f"{mode:<15} ₹{fare:<10.2f} ₹{monthly_fare:<12.2f} {mins:<6.0f} min {co2_g:.0f}"
            )

        print("-" * 62)
        print(f"Cheapest : {cheapest[0]} (₹{cheapest[1]:.2f}/trip, ₹{cheapest[2]:.2f}/mo)")
        print(f"Fastest  : {fastest[0]} ({fastest[3]:.0f} min)")


if __name__ == "__main__":
    main()