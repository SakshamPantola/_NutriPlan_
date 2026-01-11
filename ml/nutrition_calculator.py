def calculate_bmr(weight, height, age, gender, activity, goal):
  
    if gender.lower() == "male":
        bmr = 10*weight + 6.25*height - 5*age + 5
    else:
        bmr = 10*weight + 6.25*height - 5*age - 161

    activity_map = {
        "low": 1.2,
        "medium": 1.55,
        "high": 1.75
    }

    calories = bmr * activity_map.get(activity.lower(), 1.2)

    if goal == "loss":
        calories -= 400
    elif goal == "gain":
        calories += 300

    return round(calories, 2)


def macro_targets(calories):
    return {
        "calories": calories,
        "protein": round((calories * 0.30) / 4, 1),
        "carbs": round((calories * 0.45) / 4, 1),
        "fat": round((calories * 0.25) / 9, 1)
    }
