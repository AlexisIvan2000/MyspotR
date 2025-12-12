def mood_from_features(audio_features):
    valid = [f for f in audio_features if f]
    if not valid:
        return None
    timeline = []
    for f in valid:
        mood = (
            f['valence'] * 0.6 +
            f['energy'] * 0.3 +
            f['danceability'] * 0.2
        )
        timeline.append(round(mood, 2))
        avg = round(sum(timeline) / len(timeline), 2)
        if avg < 0.3:
            label = 'sad'
        elif avg < 0.6:
            label = 'chill'
        else:
            label = 'happy'
    return {
        "average":avg,
        "label":label,
        "timeline":timeline
    }