import sys

from load_data import load_torvik_four_factors, get_team
from scouting import generate_team_report

def get_illinois_advantages(illinois, opponent) -> list[str]:
    """
    Identify matchup areas where Illinois may have an advantage
    """
    advantages = []

    if illinois["3P Rate Rank"] <= 75 and opponent["3P Rate Def Rank"] > 250:
        advantages.append(
            "Illinois's high three-point volume matches up well against an opponent defense that allows a high volume of three-point attempts."
        )

    if illinois["OR% Rank"] <= 75 and opponent["DR% Rank"] > 250:
        advantages.append(
            "Illinois's offensive rebounding may create extra possessions against an opponent that struggles to finish defensive possessions."
        )

    if illinois["TO% Rank"] <= 75 and opponent["TO% Def. Rank"] <= 75:
        advantages.append(
            "Illinois's ball security can help reduce the impact of the opponent's defensive pressure."
        )

    if illinois["FTR Def Rank"] <= 75 and opponent["FTR Rank"] > 250:
        advantages.append(
            "Illinois's ability to defend without fouling may compound the opponent's difficulty getting to the free throw line."
        )

    if illinois["eFG% Rank"] <= 75 and opponent["eFG% Def Rank"] > 250:
        advantages.append(
            "Illinois's shooting efficiency could be especially valuable against an opponent that allows efficient shooting."
        )

    return advantages

def get_opponent_dangers(illinois, opponent) -> list[str]:
    """
    Identify matchup areas where the opponent may create problems for Illinois
    """
    dangers = []

    if opponent["OR% Rank"] <= 75:
        dangers.append(
            f"{opponent['TeamName']}'s offensive rebounding can create extra-possession risk. Illinois must finish defensive possessions with strong box-outs."
        )

    if opponent["3P Rate Rank"] <= 75 and illinois["3P Rate Def Rank"] > 250:
        dangers.append(
            f"{opponent['TeamName']}'s three-point volume could stress Illinois's perimeter defense if closeouts and rotations are late."
        )

    if opponent["eFG% Rank"] <= 75:
        dangers.append(
            f"{opponent['TeamName']} scores efficiently, so Illinois cannot rely on empty possessions or low-quality offensive trips."
        )

    if opponent["TO% Def. Rank"] <= 75 and illinois["TO% Rank"] > 150:
        dangers.append(
            f"{opponent['TeamName']} forces turnovers well, which could create transition chances if Illinois gets loose with the ball."
        )

    if opponent["FTR Rank"] <= 75 and illinois["FTR Def Rank"] > 150:
        dangers.append(
            f"{opponent['TeamName']} gets to the free throw line well, so Illinois must defend without fouling."
        )

    return dangers


def generate_keys_to_victory(illinois, opponent) -> list[str]:
    """
    Generate concise keys to victory for Illinois
    """
    keys = []

    if opponent["OR% Rank"] <= 75:
        keys.append("Finish defensive possessions with physical box-outs and team rebounding.")

    if opponent["TO% Def. Rank"] <= 75:
        keys.append("Value the ball and avoid live-ball turnovers against defensive pressure.")

    if opponent["3P Rate Rank"] <= 75 or opponent["3P% Rank"] <= 75:
        keys.append("Maintain closeout discipline and limit rhythm three-point attempts.")

    if opponent["eFG% Rank"] <= 75:
        keys.append("Avoid empty offensive possessions because the opponent converts efficiently.")

    if opponent["FTR Rank"] <= 75:
        keys.append("Defend without fouling and keep the opponent away from the free throw line.")

    if opponent["eFG% Def Rank"] <= 75:
        keys.append("Create clean looks through pace, spacing, and ball movement against strong shot defense.")

    if illinois["OR% Rank"] <= 75:
        keys.append("Attack the offensive glass to create second-chance points.")

    if illinois["3P Rate Rank"] <= 75 and opponent["3P Rate Def Rank"] > 250:
        keys.append("Lean into three-point volume when quality catch-and-shoot looks are available.")

    return keys

def generate_matchup_report(illinois, opponent) -> dict:
    """
    Generate a matchup report comparing Illinois to a single opponent
    """
    illinois_report = generate_team_report(illinois)
    opponent_report = generate_team_report(opponent)

    report = {
        "base_team": illinois_report["team"],
        "opponent": opponent_report["team"],
        "illinois_strengths": illinois_report["strengths"],
        "opponent_strengths": opponent_report["strengths"],
        "opponent_weaknesses": opponent_report["weaknesses"],
        "illinois_advantages": get_illinois_advantages(illinois, opponent),
        "opponent_dangers": get_opponent_dangers(illinois, opponent),
        "keys_to_victory": generate_keys_to_victory(illinois, opponent),
    }

    return report


if __name__ == "__main__":
    four_factors = load_torvik_four_factors(2026)

    illinois = get_team(four_factors, "Illinois", "TeamName")

    if len(sys.argv) > 1:
        opponent_name = " ".join(sys.argv[1:])
    else:
        opponent_name = "Houston"

    opponent = get_team(four_factors, opponent_name, "TeamName")

    report = generate_matchup_report(illinois, opponent)

    print("Matchup loaded successfully.")
    print("Base team:", report["base_team"])
    print("Opponent:", report["opponent"])

    print("\nIllinois strengths:")
    for strength in report["illinois_strengths"]:
        print("-", strength)

    print(f"\n{report['opponent']} strengths:")
    for strength in report["opponent_strengths"]:
        print("-", strength)

    print(f"\n{report['opponent']} weaknesses:")
    for weakness in report["opponent_weaknesses"]:
        print("-", weakness)

    print("\nIllinois matchup advantages:")
    for advantage in report["illinois_advantages"]:
        print("-", advantage)

    print("\nOpponent danger areas:")
    for danger in report["opponent_dangers"]:
        print("-", danger)

    print("\nKeys to victory:")
    for key in report["keys_to_victory"]:
        print("-", key)