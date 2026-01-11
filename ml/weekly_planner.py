from .meal_optimizer import recommend_meals


def generate_week_plan(dishes, target):
    week = {}
    usage = {}

    for day in range(1, 8):
        meals = recommend_meals(dishes, target)
        filtered = []

        for m in meals:
            name = m["dish"]["name"]
            if usage.get(name, 0) < 2:
                filtered.append(m)
                usage[name] = usage.get(name, 0) + 1

        week[f"Day {day}"] = filtered

    return week
