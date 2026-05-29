import sys
import pandas as pd

from load_data import load_torvik_four_factors, get_team


def classify_rank(rank: int) -> str:
    """
    Convert a national rank into a scouting label

    Lower ranks are better
    """
    if rank <= 25:
        return "Elite"
    elif rank <= 75:
        return "Strong"
    elif rank <= 150:
        return "Average"
    elif rank <= 205:
        return "Weak"
    else:
        return "Major weakness"
    

def describe_metric(metric_name: str, value: float, rank: int) -> str:
    """
    Create a short description for a single metric
    """
    label = classify_rank(rank)

    return f"{metric_name}: {value:.1f} ({label}, rank {rank})"


def get_team_strengths(team_ff: pd.Series) -> list[str]:
    """
    Identify major team strengths from Four Factors rankings.
    """
    strengths = []

    if team_ff["eFG% Rank"] <= 75:
        strengths.append(f"{strength_prefix(team_ff['eFG% Rank'])} shooting efficiency")

    if team_ff["OR% Rank"] <= 75:
        strengths.append(f"{strength_prefix(team_ff['OR% Rank'])} offensive rebounding")

    if team_ff["TO% Rank"] <= 75:
        strengths.append(f"{strength_prefix(team_ff['TO% Rank'])} ball security")

    if team_ff["FTR Rank"] <= 75:
        strengths.append(f"{strength_prefix(team_ff['FTR Rank'])} free throw generation")

    if team_ff["eFG% Def Rank"] <= 75:
        strengths.append(f"{strength_prefix(team_ff['eFG% Def Rank'])} shot defense")

    if team_ff["FTR Def Rank"] <= 75:
        strengths.append(f"{strength_prefix(team_ff['FTR Def Rank'])} foul avoidance")

    if team_ff["TO% Def. Rank"] <= 75:
        strengths.append(f"{strength_prefix(team_ff['TO% Def. Rank'])} defensive turnover creation")

    if team_ff["3P Rate Rank"] <= 75:
        strengths.append(f"{strength_prefix(team_ff['3P Rate Rank'])} three-point volume")

    return strengths

def get_team_weaknesses(team_ff: pd.Series) -> list[str]:
    """
    Identify major team weaknesses from Four Factors rankings.
    """
    weaknesses = []

    if team_ff["eFG% Rank"] > 250:
        weaknesses.append(f"{weakness_prefix(team_ff['eFG% Rank'])}: inefficient shooting offense")

    if team_ff["OR% Rank"] > 250:
        weaknesses.append(f"{weakness_prefix(team_ff['OR% Rank'])}: weak offensive rebounding")

    if team_ff["TO% Rank"] > 250:
        weaknesses.append(f"{weakness_prefix(team_ff['TO% Rank'])}: turnover-prone offense")

    if team_ff["FTR Rank"] > 250:
        weaknesses.append(f"{weakness_prefix(team_ff['FTR Rank'])}: does not get to the free throw line often")

    if team_ff["eFG% Def Rank"] > 250:
        weaknesses.append(f"{weakness_prefix(team_ff['eFG% Def Rank'])}: allows efficient opponent shooting")

    if team_ff["FTR Def Rank"] > 250:
        weaknesses.append(f"{weakness_prefix(team_ff['FTR Def Rank'])}: fouls too often defensively")

    if team_ff["TO% Def. Rank"] > 250:
        weaknesses.append(f"{weakness_prefix(team_ff['TO% Def. Rank'])}: does not force many turnovers")

    if team_ff["3P Rate Def Rank"] > 250:
        weaknesses.append(f"{weakness_prefix(team_ff['3P Rate Def Rank'])}: allows a high volume of opponent three-point attempts")

    return weaknesses


def explain_strength(strength: str) -> str:
    """
    Add basketball context to a strength label
    """
    if "shooting efficiency" in strength:
        return f"{strength} — converts possessions efficiently, especially when able to generate clean looks."
    if "offensive rebounding" in strength:
        return f"{strength} — creates extra possessions and punishes opponents that fail to finish defensive possessions."

    if "ball security" in strength:
        return f"{strength} — limits turnovers and reduces transition chances for opponents."

    if "free throw generation" in strength:
        return f"{strength} — puts pressure on defenses and can create foul trouble."

    if "shot defense" in strength:
        return f"{strength} — holds opponents to difficult or inefficient looks."

    if "foul avoidance" in strength:
        return f"{strength} — keeps opponents off the free throw line and avoids cheap points."

    if "defensive turnover creation" in strength:
        return f"{strength} — creates extra possessions through pressure and disruption."

    if "three-point volume" in strength:
        return f"{strength} — stretches defenses and can create scoring runs."

    return strength

def explain_weakness(weakness: str) -> str:
    """
    Add basketball context to a weakness label
    """
    if "inefficient shooting offense" in weakness:
        return f"{weakness} — may struggle to score if forced into half-court possessions or contested shots."

    if "weak offensive rebounding" in weakness:
        return f"{weakness} — misses are more likely to end possessions."

    if "turnover-prone offense" in weakness:
        return f"{weakness} — pressure can create extra possessions and transition opportunities."

    if "does not get to the free throw line often" in weakness:
        return f"{weakness} — relies more heavily on made field goals rather than foul pressure."

    if "allows efficient opponent shooting" in weakness:
        return f"{weakness} — opponents can generate or convert quality looks."

    if "fouls too often defensively" in weakness:
        return f"{weakness} — opponents can create cheap points and put key defenders in foul trouble."

    if "does not force many turnovers" in weakness:
        return f"{weakness} — opponents can usually initiate offense without heavy disruption."

    if "allows a high volume of opponent three-point attempts" in weakness:
        return f"{weakness} — closeout discipline and help rotations are important."

    return weakness


def generate_team_report(team_ff: pd.Series) -> dict:
    """
    Generate a scouting report dictionary for a single team
    """
    strengths = get_team_strengths(team_ff)
    weaknesses = get_team_weaknesses(team_ff)

    explained_strengths = []
    for strength in strengths:
        explained_strengths.append(explain_strength(strength))

    explained_weaknesses = []
    for weakness in weaknesses:
        explained_weaknesses.append(explain_weakness(weakness))
    
    report = {
        "team": team_ff["TeamName"],
        "strengths": explained_strengths,
        "weaknesses": explained_weaknesses,
    }

    return report

def strength_prefix(rank: int) -> str:
    """
    Return a stronger word for higher ranks
    """
    if rank <= 25:
        return "Elite"
    else:
        return "Strong"
    
def weakness_prefix(rank: int) -> str:
    """
    Return a more severe word for very low ranks
    """
    if rank > 325:
        return "Severe concern"
    else:
        return "Concern"


if __name__ == "__main__":
    four_factors = load_torvik_four_factors(2026)

    if len(sys.argv) > 1:
        team_name = " ".join(sys.argv[1:])
    else:
        team_name = "Illinois"

    team = get_team(four_factors, team_name, "TeamName")

    report = generate_team_report(team)

    print("Loaded scouting data.")
    print("Team:", report["team"])

    print("\nStrengths:")
    for strength in report["strengths"]:
        print("-", strength)

    print("\nWeaknesses:")
    for weakness in report["weaknesses"]:
        print("-", weakness)