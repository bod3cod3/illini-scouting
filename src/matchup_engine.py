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

TEAM_STYLE_SIGNALS = [
    {
        "name": "Efficient scoring",
        "metric": "eFG%",
        "description": "converts possessions efficiently"
    },
    {
        "name": "Offensive glass pressure",
        "metric": "OR%",
        "description": "creates extra possessions through offensive rebounding"
    },
    {
        "name": "Ball security",
        "metric": "TO%",
        "description": "protects possessions and limits live-ball turnover risk"
    },
    {
        "name": "Free throw pressure",
        "metric": "FTR",
        "description": "puts pressure on the rim and gets to the free throw line"
    },
    {
        "name": "Shot defense",
        "metric": "eFG% Def",
        "description": "forces opponents into inefficient shooting"
    },
    {
        "name": "Foul avoidance",
        "metric": "FTR Def",
        "description": "defends without sending opponents to the free throw line"
    },
    {
        "name": "Defensive pressure",
        "metric": "TO% Def.",
        "description": "creates turnovers through pressure and disruption"
    },
    {
        "name": "Three-point volume",
        "metric": "3P Rate",
        "description": "takes a high share of attempts from three"
    },
]

IDENTITY_AXES = [
    {
        "name": "Offensive firepower",
        "metrics": ["eFG%", "OR%", "TO%", "3P Rate"],
        "description": "scores efficiently, protects possessions, creates second chances, and stretches defenses"
    },
    {
        "name": "Possession control",
        "metrics": ["OR%", "TO%", "TO% Def."],
        "description": "wins the possession battle through rebounding, ball security, and defensive disruption"
    },
    {
        "name": "Defensive disruption",
        "metrics": ["TO% Def.", "eFG% Def"],
        "description": "pressures opponents into turnovers and difficult shots"
    },
    {
        "name": "Defensive discipline",
        "metrics": ["eFG% Def", "FTR Def"],
        "description": "forces inefficient shots without fouling"
    },
    {
        "name": "Perimeter volume",
        "metrics": ["3P Rate", "3P%"],
        "description": "leans on three-point volume and perimeter shotmaking"
    },
    {
        "name": "Paint and free throw pressure",
        "metrics": ["FTR", "OR%"],
        "description": "puts pressure on the rim, free throw line, and offensive glass"
    },
]

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
        f"{score['name']}: {score['pressure_score']}/100 ({get_pressure_matchup_type(score)}). "
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
        f"{score['name']}: {score['edge_score']}/100 ({get_edge_matchup_type(score)}). "
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

def generate_matchup_summary(base_team, opponent) -> str:
    """
    Generate a compact matchup summary from archetypes and top matchup scores
    """
    base_team_name = base_team["TeamName"]
    opponent_name = opponent["TeamName"]

    base_archetype = identify_team_archetype(base_team)
    opponent_archetype = identify_team_archetype(opponent)

    top_pressure = get_top_opponent_pressures(base_team, opponent, limit=1)[0]
    top_edge = get_top_base_team_edges(base_team, opponent, limit=1)[0]

    pressure_metric_name = METRIC_DISPLAY_NAMES[top_pressure["opponent_metric"]]
    resistance_metric_name = METRIC_DISPLAY_NAMES[top_pressure["base_metric"]]

    edge_metric_name = METRIC_DISPLAY_NAMES[top_edge["base_metric"]]
    opponent_resistance_name = METRIC_DISPLAY_NAMES[top_edge["opponent_metric"]]

    pressure_type = get_pressure_matchup_type(top_pressure)
    edge_type = get_edge_matchup_type(top_edge)

    return (
        f"{base_team_name} enters as a {base_archetype.lower()}, while "
        f"{opponent_name} profiles as a {opponent_archetype.lower()}. "
        f"{opponent_name}'s clearest pressure area is {top_pressure['name'].lower()} "
        f"({top_pressure['pressure_score']}/100, {pressure_type.lower()}), where its "
        f"{pressure_metric_name} attacks {base_team_name}'s {resistance_metric_name} profile. "
        f"{base_team_name}'s cleanest counter is its {edge_metric_name} "
        f"({top_edge['edge_score']}/100, {edge_type.lower()}), which attacks "
        f"{opponent_name}'s {opponent_resistance_name} profile. "
        f"The matchup likely hinges on whether {base_team_name} can manage "
        f"{opponent_name}'s top pressure area while still leaning into its clearest offensive edge."
    )

def get_pressure_matchup_type(score: dict) -> str:
    """
    Describe what kind of opponent pressure matchup this is
    """
    opponent_strength = score["opponent_strength"]
    base_resistance = score["base_resistance"]

    if opponent_strength >= 75 and base_resistance <= 25:
        return "Clear pressure point"

    if opponent_strength >= 75 and base_resistance >= 75:
        return "Strength-on-strength"

    if opponent_strength >= 75:
        return "Opponent strength"

    if base_resistance <= 25:
        return "Vulnerability watch"

    return "Lower-leverage area"

def get_edge_matchup_type(score: dict) -> str:
    """
    Describe what kind of base team edge matchup this is
    """
    base_strength = score["base_strength"]
    opponent_resistance = score["opponent_resistance"]

    if base_strength >= 75 and opponent_resistance <= 25:
        return "Clear edge"

    if base_strength >= 75 and opponent_resistance >= 75:
        return "Strength-on-strength"

    if base_strength >= 75:
        return "Base team strength"

    if opponent_resistance <= 25:
        return "Opponent vulnerability watch"

    return "Lower-leverage edge"

def score_team_style_signals(team) -> list[dict]:
    """
    Score a team's strongest statistical style signals
    """
    signals = []

    for signal in TEAM_STYLE_SIGNALS:
        percentile = get_metric_percentile(
            team,
            signal["metric"],
        )

        signals.append(
            {
                "team": team["TeamName"],
                "name": signal["name"],
                "metric": signal["metric"],
                "description": signal["description"],
                "percentile": percentile,
            }
        )

    signals = sorted(
        signals,
        key=lambda signal: signal["percentile"],
        reverse=True,
    )

    return signals

def identify_team_archetype(team) -> str:
    """
    Identify a team's broad statistical archetype from composite identity scores
    """
    axes = score_identity_axes(team)

    top_axis = axes[0]
    second_axis = axes[1]

    top_name = top_axis["name"]
    second_name = second_axis["name"]

    top_score = top_axis["score"]
    second_score = second_axis["score"]

    top_two_names = {top_name, second_name}

    if top_score < 50:
        return "Low-signal statistical profile"

    if top_score >= 85 and second_score >= 80:
        if {"Offensive firepower", "Defensive discipline"}.issubset(top_two_names):
            return "Two-way efficiency team"

        if {"Defensive disruption", "Possession control"}.issubset(top_two_names):
            return "Possession-control pressure team"

        if {"Defensive discipline", "Paint and free throw pressure"}.issubset(top_two_names):
            return "Physical defensive discipline team"

        if {"Offensive firepower", "Perimeter volume"}.issubset(top_two_names):
            return "High-powered perimeter offense"

    if top_score >= 75:
        if top_name == "Offensive firepower":
            return "Offensive firepower team"

        if top_name == "Possession control":
            return "Possession-control team"

        if top_name == "Defensive disruption":
            return "Defensive disruption team"

        if top_name == "Defensive discipline":
            return "Defensive discipline team"

        if top_name == "Perimeter volume":
            return "Perimeter-volume offense"

        if top_name == "Paint and free throw pressure":
            return "Physical paint-pressure team"

    return "Mixed statistical profile"

def score_identity_axes(team) -> list[dict]:
    """
    Score a team's broader statistical identity areas
    """
    axes = []

    for axis in IDENTITY_AXES:
        percentiles = []

        for metric in axis["metrics"]:
            percentile = get_metric_percentile(team, metric)
            percentiles.append(percentile)

        axis_score = sum(percentiles) / len(percentiles)

        axes.append(
            {
                "team": team["TeamName"],
                "name": axis["name"],
                "description": axis["description"],
                "metrics": axis["metrics"],
                "score": round(axis_score, 1),
            }
        )

    axes = sorted(
        axes,
        key=lambda axis: axis["score"],
        reverse=True,
    )

    return axes

def get_key_from_opponent_pressure(score: dict) -> str:
    """
    Create one key to victory from an opponent pressure score
    """
    base_team = score["base_team"]
    opponent = score["opponent"]
    matchup_type = get_pressure_matchup_type(score).lower()

    if score["name"] == "Defensive glass pressure":
        return (
            f"Finish defensive possessions: {opponent}'s offensive rebounding is a "
            f"{matchup_type}, so {base_team} needs five-man box-outs before leaking out."
        )

    if score["name"] == "Opponent three-point volume pressure":
        return (
            f"Control the arc: {opponent}'s three-point volume is a {matchup_type}, "
            f"so {base_team} needs disciplined closeouts without overhelping."
        )

    if score["name"] == "Opponent shooting efficiency pressure":
        return (
            f"Make first shots difficult: {opponent}'s shooting efficiency is a "
            f"{matchup_type}, so {base_team} cannot give up clean early-clock looks."
        )

    if score["name"] == "Opponent turnover pressure":
        return (
            f"Protect possessions: {opponent}'s turnover creation is a {matchup_type}, "
            f"so {base_team} needs strong spacing, simple outlets, and limited live-ball mistakes."
        )

    if score["name"] == "Opponent free throw pressure":
        return (
            f"Defend without fouling: {opponent}'s free throw pressure is a "
            f"{matchup_type}, so {base_team} needs verticality and disciplined help rotations."
        )

    return (
        f"Manage {score['name'].lower()}: {base_team} needs to limit the matchup area "
        f"where {opponent} creates the most pressure."
    )


def get_key_from_base_team_edge(score: dict) -> str:
    """
    Create one key to victory from a base team edge score
    """
    base_team = score["base_team"]
    opponent = score["opponent"]
    matchup_type = get_edge_matchup_type(score).lower()

    if score["name"] == "Offensive glass edge":
        return (
            f"Attack the offensive glass: {base_team}'s offensive rebounding is a "
            f"{matchup_type}, so second-chance points can be a major source of value."
        )

    if score["name"] == "Three-point volume edge":
        return (
            f"Lean into quality threes: {base_team}'s three-point volume is a "
            f"{matchup_type}, so clean catch-and-shoot looks should be emphasized."
        )

    if score["name"] == "Shooting efficiency edge":
        return (
            f"Create efficient looks: {base_team}'s shooting efficiency is a "
            f"{matchup_type}, so pace, spacing, and ball movement should drive the offense."
        )

    if score["name"] == "Ball security edge":
        return (
            f"Make {opponent} defend full possessions: {base_team}'s ball security is a "
            f"{matchup_type}, so avoiding empty possessions can tilt the possession math."
        )

    if score["name"] == "Free throw pressure edge":
        return (
            f"Pressure the rim: {base_team}'s free throw pressure is a "
            f"{matchup_type}, so attacking closeouts and drawing contact can create efficient points."
        )

    return (
        f"Use {score['name'].lower()}: {base_team} should lean into the matchup area "
        f"where it creates the clearest edge."
    )


def generate_engine_keys_to_victory(base_team, opponent) -> list[str]:
    """
    Generate keys to victory from the top pressure and edge scores
    """
    keys = []

    top_pressures = get_top_opponent_pressures(base_team, opponent, limit=2)
    top_edges = get_top_base_team_edges(base_team, opponent, limit=2)

    for pressure in top_pressures:
        keys.append(get_key_from_opponent_pressure(pressure))

    for edge in top_edges:
        keys.append(get_key_from_base_team_edge(edge))

    return keys