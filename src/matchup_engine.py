from metrics import get_metric_percentile

MATCHUP_AREAS = [
    {
        "name": "Defensive glass pressure",
        "opponent_metric": "OR%",
        "base_metric": "DR%",
    },
    {
        "name": "Opponent three-point volume pressure",
        "opponent_metric": "3P Rate",
        "base_metric": "3P Rate Def",
    },
    {
        "name": "Opponent shooting efficiency pressure",
        "opponent_metric": "eFG%",
        "base_metric": "eFG% Def",
    },
    {
        "name": "Opponent turnover pressure",
        "opponent_metric": "TO% Def.",
        "base_metric": "TO%",
    },
    {
        "name": "Opponent free throw pressure",
        "opponent_metric": "FTR",
        "base_metric": "FTR Def",
    },
]

BASE_EDGE_AREAS = [
    {
        "name": "Offensive glass edge",
        "base_metric": "OR%",
        "opponent_metric": "DR%",
    },
    {
        "name": "Three-point volume edge",
        "base_metric": "3P Rate",
        "opponent_metric": "3P Rate Def",
    },
    {
        "name": "Shooting efficiency edge",
        "base_metric": "eFG%",
        "opponent_metric": "eFG% Def",
    },
    {
        "name": "Ball security edge",
        "base_metric": "TO%",
        "opponent_metric": "TO% Def.",
    },
    {
        "name": "Free throw pressure edge",
        "base_metric": "FTR",
        "opponent_metric": "FTR Def",
    },
]

METRIC_DISPLAY_NAMES = {
    "eFG%": "shooting efficiency",
    "eFG% Def": "shot defense",
    "FTR": "free throw pressure",
    "FTR Def": "foul avoidance",
    "OR%": "offensive rebounding",
    "DR%": "defensive rebounding",
    "TO%": "ball security",
    "TO% Def.": "turnover creation",
    "3P Rate": "three-point volume",
    "3P Rate Def": "three-point volume allowed",
}

def calculate_pressure_score(opponent_strength: float, base_resistance: float) -> float:
    """
    Calculate how much pressure an opponent puts on the base team in one matchup area

    opponent_strength:
        Opponent percentile in the attacking stat

    base_resistance:
        Base team's percentile in the corresponding resistance stat

    Returns:
        A 0-100 pressure score
    """
    base_vulnerability = 100 - base_resistance

    pressure_score = (opponent_strength + base_vulnerability) / 2

    return round(pressure_score, 1)

def score_matchup_area(base_team, opponent, area: dict) -> dict:
    """
    Score one matchup area between an opponent strength and a base team's resistance
    """
    opponent_strength = get_metric_percentile(
        opponent,
        area["opponent_metric"],
    )

    base_resistance = get_metric_percentile(
        base_team,
        area["base_metric"],
    )

    pressure_score = calculate_pressure_score(
        opponent_strength,
        base_resistance,
    )

    return {
        "name": area["name"],
        "base_team": base_team["TeamName"],
        "opponent": opponent["TeamName"],
        "opponent_metric": area["opponent_metric"],
        "base_metric": area["base_metric"],
        "opponent_strength": opponent_strength,
        "base_resistance": base_resistance,
        "pressure_score": pressure_score,
    }

def score_opponent_pressures(base_team, opponent) -> list[dict]:
    """
    Score all ways the opponent can put pressure on the base team
    """
    scores = []

    for area in MATCHUP_AREAS:
        score = score_matchup_area(base_team, opponent, area)
        scores.append(score)

    scores = sorted(
        scores,
        key=lambda score: score["pressure_score"],
        reverse=True,
    )

    return scores

def get_top_opponent_pressures(base_team, opponent, limit: int = 3) -> list[dict]:
    """
    Return the highest-pressure opponent matchup areas
    """
    scores = score_opponent_pressures(base_team, opponent)

    return scores[:limit]

def format_pressure_score(score: dict) -> str:
    """
    Format one opponent pressure score as readable text
    """
    opponent_metric_name = METRIC_DISPLAY_NAMES[score["opponent_metric"]]
    base_metric_name = METRIC_DISPLAY_NAMES[score["base_metric"]]

    return (
        f"{score['name']}: {score['pressure_score']}/100 ({get_score_confidence(score['pressure_score'])}) — "
        f"{score['opponent']}'s {opponent_metric_name} attacks "
        f"{score['base_team']}'s {base_metric_name} profile. "
        f"{score['opponent']} {score['opponent_metric']} percentile: {score['opponent_strength']}; "
        f"{score['base_team']} {score['base_metric']} percentile: {score['base_resistance']}."
    )

def format_top_opponent_pressures(base_team, opponent, limit: int = 3) -> list[str]:
    """
    Format the highest-pressure opponent matchup areas
    """
    top_scores = get_top_opponent_pressures(base_team, opponent, limit)

    formatted_scores = []

    for score in top_scores:
        formatted_scores.append(format_pressure_score(score))

    return formatted_scores

def score_base_edge_area(base_team, opponent, area: dict) -> dict:
    """
    Score one matchup area where the base team may have an edge
    """
    base_strength = get_metric_percentile(
        base_team,
        area["base_metric"],
    )

    opponent_resistance = get_metric_percentile(
        opponent,
        area["opponent_metric"],
    )

    edge_score = calculate_pressure_score(
        base_strength,
        opponent_resistance,
    )

    return {
        "name": area["name"],
        "base_team": base_team["TeamName"],
        "opponent": opponent["TeamName"],
        "base_metric": area["base_metric"],
        "opponent_metric": area["opponent_metric"],
        "base_strength": base_strength,
        "opponent_resistance": opponent_resistance,
        "edge_score": edge_score,
    }


def score_base_team_edges(base_team, opponent) -> list[dict]:
    """
    Score all ways the base team can put pressure on the opponent
    """
    scores = []

    for area in BASE_EDGE_AREAS:
        score = score_base_edge_area(base_team, opponent, area)
        scores.append(score)

    scores = sorted(
        scores,
        key=lambda score: score["edge_score"],
        reverse=True,
    )

    return scores


def get_top_base_team_edges(base_team, opponent, limit: int = 3) -> list[dict]:
    """
    Return the highest-edge base team matchup areas
    """
    scores = score_base_team_edges(base_team, opponent)

    return scores[:limit]


def format_edge_score(score: dict) -> str:
    """
    Format one base team edge score as readable text
    """
    base_metric_name = METRIC_DISPLAY_NAMES[score["base_metric"]]
    opponent_metric_name = METRIC_DISPLAY_NAMES[score["opponent_metric"]]

    return (
        f"{score['name']}: {score['edge_score']}/100 ({get_score_confidence(score['edge_score'])}) — "
        f"{score['base_team']}'s {base_metric_name} attacks "
        f"{score['opponent']}'s {opponent_metric_name} profile. "
        f"{score['base_team']} {score['base_metric']} percentile: {score['base_strength']}; "
        f"{score['opponent']} {score['opponent_metric']} percentile: {score['opponent_resistance']}."
    )


def format_top_base_team_edges(base_team, opponent, limit: int = 3) -> list[str]:
    """
    Format the highest-edge base team matchup areas
    """
    top_scores = get_top_base_team_edges(base_team, opponent, limit)

    formatted_scores = []

    for score in top_scores:
        formatted_scores.append(format_edge_score(score))

    return formatted_scores

def get_score_confidence(score: float) -> str:
    """
    Return a confidence label for a matchup score
    """
    if score >= 75:
        return "High confidence"
    if score >= 50:
        return "Medium confidence"
    return "Low confidence"