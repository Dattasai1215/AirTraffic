def get_alert(prob):
    """
    Classifies conflict probability into standard Air Traffic Control (ATC) alert levels.
    """
    if prob > 0.75:
        return {
            "level": "CRITICAL",
            "icon": "🚨",
            "msg": "CONFLICT RESOLUTION ADVISORY (RA)",
            "color": "red"
        }
    elif prob > 0.40:
        return {
            "level": "WARNING",
            "icon": "⚠️",
            "msg": "TRAFFIC ADVISORY (TA)",
            "color": "orange"
        }
    elif prob > 0.15:
        return {
            "level": "MONITOR",
            "icon": "🔍",
            "msg": "PROXIMITY ALERT",
            "color": "yellow"
        }
    return {
        "level": "SAFE",
        "icon": "✅",
        "msg": "NORMAL SEPARATION",
        "color": "green"
    }
