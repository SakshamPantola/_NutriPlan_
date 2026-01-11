def score_dish(dish, target):
    protein_score = dish["protein"] / target["protein"]
    calorie_score = 1 - abs(dish["calories"] - target["calories"]/3) / 250
    fat_penalty = dish["fat"] / 30

    score = (protein_score * 0.5) + (calorie_score * 0.3) - (fat_penalty * 0.2)
    return round(score, 2)


def explain_dish(dish):
    reasons = []
    if dish["protein"] >= 15:
        reasons.append("High protein")
    if dish["fat"] <= 10:
        reasons.append("Low fat")
    if dish["calories"] <= 250:
        reasons.append("Light meal")

    return reasons


def recommend_meals(dishes, target):
    scored = []

    for dish in dishes:
        s = score_dish(dish, target)
        scored.append((s, dish))

    scored.sort(reverse=True, key=lambda x: x[0])

    selected = scored[:3]

    meals = []
    for score, dish in selected:
        meals.append({
            "dish": dish,
            "score": score,
            "reason": explain_dish(dish)
        })

    return meals
