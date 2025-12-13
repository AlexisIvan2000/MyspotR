from collections import Counter, defaultdict
from datetime import datetime

def analyze_mood_from_recent(recent):
    if not recent:
        return {
            "label": "Unknown",
            "score": 0,
            "timeline": []
        }

    energy = 0
    calm = 0
    timeline = []

    for item in recent:
        track = item["track"]
        popularity = track.get("popularity", 50)
        explicit = track.get("explicit", False)

        played_at = item.get("played_at")
        hour = datetime.fromisoformat(played_at.replace("Z", "")).hour if played_at else None

       
        score = 0
        if popularity > 70:
            score += 2
        elif popularity > 50:
            score += 1
        else:
            score -= 1

        if explicit:
            score += 1

        if hour is not None:
            if hour >= 22 or hour <= 6:
                score -= 1  
            elif 10 <= hour <= 18:
                score += 1 

        if score >= 2:
            energy += 1
            label = "Energetic"
        else:
            calm += 1
            label = "Chill"

        timeline.append({
            "label": label,
            "score": score,
            "hour": hour
        })

    final_label = "Energetic" if energy > calm else "Chill"

    return {
        "label": final_label,
        "energy": energy,
        "calm": calm,
        "timeline": timeline[-20:]  
    }


def aggregate_by_day(timeline):
    days = defaultdict(list)

    for item in timeline:
        hour = item.get("hour")
        label = item.get("label")

        if hour is None:
            continue

        day = "day" if 8 <= hour <= 20 else "night"
        days[day].append(label)

    result = {}
    for day, moods in days.items():
        energetic = moods.count("Energetic")
        chill = moods.count("Chill")
        result[day] = "Energetic" if energetic > chill else "Chill"

    return result