import sys

SEASON_YEAR = 2026

from load_data import load_torvik_four_factors, get_team
from metrics import add_percentile_columns
from matchup_engine import (
    format_top_opponent_pressures,
    format_top_base_team_edges,
    generate_engine_keys_to_victory,
    generate_matchup_summary,
    identify_team_archetype,
)
from scouting import generate_team_report

def get_base_team_advantages(base_team, opponent) -> list[str]:
    """
    Identify matchup areas where the base team may have an advantage
    """
    advantages = []

    if base_team["3P Rate Rank"] <= 75 and opponent["3P Rate Def Rank"] > 250:
        advantages.append(
            f"{base_team['TeamName']}'s high three-point volume matches up well against an opponent defense that allows a high volume of three-point attempts."
        )

    if base_team["OR% Rank"] <= 75 and opponent["DR% Rank"] > 250:
        advantages.append(
            f"{base_team['TeamName']}'s offensive rebounding may create extra possessions against an opponent that struggles to finish defensive possessions."
        )

    if base_team["TO% Rank"] <= 75 and opponent["TO% Def. Rank"] <= 75:
        advantages.append(
            f"{base_team['TeamName']}'s ball security can help reduce the impact of the opponent's defensive pressure."
        )
    if base_team["TO% Rank"] <= 75 and opponent["TO% Def. Rank"] > 250:
        advantages.append(
            f"{base_team['TeamName']}'s ball security matches up well against a {opponent['TeamName']} defense that does not force many turnovers."
        )

    if base_team["FTR Def Rank"] <= 75 and opponent["FTR Rank"] > 250:
        advantages.append(
            f"{base_team['TeamName']}'s ability to defend without fouling may compound the opponent's difficulty getting to the free throw line."
        )

    if base_team["eFG% Rank"] <= 75 and opponent["eFG% Def Rank"] > 250:
        advantages.append(
            f"{base_team['TeamName']}'s shooting efficiency could be especially valuable against an opponent that allows efficient shooting."
        )

    return advantages

def get_opponent_dangers(base_team, opponent) -> list[str]:
    """
    Identify matchup areas where the opponent may create problems for the base team
    """
    dangers = []

    if opponent["OR% Rank"] <= 75:
        dangers.append(
            f"{opponent['TeamName']}'s offensive rebounding can create extra-possession risk. {base_team['TeamName']} must finish defensive possessions with strong box-outs."
        )

    if opponent["3P Rate Rank"] <= 75 and base_team["3P Rate Def Rank"] > 250:
        dangers.append(
            f"{opponent['TeamName']}'s three-point volume could stress {base_team['TeamName']}'s perimeter defense if closeouts and rotations are late."
        )

    if opponent["eFG% Rank"] <= 75:
        dangers.append(
            f"{opponent['TeamName']} scores efficiently, so {base_team['TeamName']} cannot rely on empty possessions or low-quality offensive trips."
        )

    if opponent["TO% Def. Rank"] <= 75 and base_team["TO% Rank"] > 150:
        dangers.append(
            f"{opponent['TeamName']} forces turnovers well, which could create transition chances if {base_team['TeamName']} gets loose with the ball."
        )

    if opponent["FTR Rank"] <= 75 and base_team["FTR Def Rank"] > 150:
        dangers.append(
            f"{opponent['TeamName']} gets to the free throw line well, so {base_team['TeamName']} must defend without fouling."
        )

    return dangers

def get_matchup_swing_factors(base_team, opponent) -> list[str]:
    """
    Identify relative matchup themes that may matter even when there is no obvious national-level weakness
    """
    factors = []

    if base_team["OR% Rank"] <= 75 and opponent["DR% Rank"] <= 150:
        factors.append(
            f"Possession battle: {base_team['TeamName']} is strong on the offensive glass, but {opponent['TeamName']} is not a clear defensive rebounding liability. Second-chance points may depend on effort, lineup choices, and physicality."
        )
    elif base_team["OR% Rank"] <= 75 and opponent["DR% Rank"] > 150:
        factors.append(
            f"Possession battle: {base_team['TeamName']} has a likely offensive rebounding edge against {opponent['TeamName']}. Extra possessions could be a major swing factor."
        )

    if opponent["OR% Rank"] <= 75:
        factors.append(
            f"Defensive glass: {opponent['TeamName']} is strong on the offensive boards, so {base_team['TeamName']} must prevent second-chance possessions."
        )

    if base_team["FTR Def Rank"] <= 75 and opponent["FTR Rank"] <= 75:
        factors.append(
            f"Foul game: {opponent['TeamName']} generates free throws well, but {base_team['TeamName']} is strong at defending without fouling. Whichever side wins that tension could shape the game."
        )
    elif base_team["FTR Def Rank"] <= 75 and opponent["FTR Rank"] > 250:
        factors.append(
            f"Foul game: {base_team['TeamName']} defends without fouling, and {opponent['TeamName']} already struggles to get to the line. This could limit easy points for the opponent."
        )

    if base_team["3P Rate Rank"] <= 75:
        factors.append(
            f"Shot profile: {base_team['TeamName']} takes a high volume of threes, so shot quality and three-point variance could heavily influence the matchup."
        )

    if opponent["3P Rate Rank"] <= 75:
        factors.append(
            f"Perimeter defense: {opponent['TeamName']} takes a high volume of threes, so {base_team['TeamName']} must stay disciplined on closeouts and rotations."
        )

    if opponent["eFG% Def Rank"] <= 75:
        factors.append(
            f"Shot creation test: {opponent['TeamName']} has strong shot defense, so {base_team['TeamName']} may need pace, spacing, and offensive rebounding to avoid stagnant half-court possessions."
        )

    if opponent["TO% Def. Rank"] <= 75 and base_team["TO% Rank"] <= 75:
        factors.append(
            f"Pressure vs. poise: {opponent['TeamName']} creates turnovers, but {base_team['TeamName']} is strong at protecting the ball. This is a key matchup strength-on-strength."
        )

    return factors

def generate_keys_to_victory(base_team, opponent) -> list[str]:
    """
    Generate concise keys to victory for the base team
    """
    keys = []

    if opponent["OR% Rank"] <= 75:
        keys.append("Finish defensive possessions with physical box-outs and team rebounding.")

    if opponent["TO% Def. Rank"] <= 75:
        keys.append("Value the ball and avoid live-ball turnovers against defensive pressure.")
    
    if opponent["TO% Def. Rank"] > 250 and base_team["TO% Rank"] <= 75:
        keys.append("Run organized offense and avoid self-inflicted turnovers against a defense that does not create many turnovers.")

    if opponent["3P Rate Rank"] <= 75 or opponent["3P% Rank"] <= 75:
        keys.append("Maintain closeout discipline and limit rhythm three-point attempts.")

    if opponent["eFG% Rank"] <= 75:
        keys.append("Avoid empty offensive possessions because the opponent converts efficiently.")

    if opponent["FTR Rank"] <= 75:
        keys.append("Defend without fouling and keep the opponent away from the free throw line.")

    if opponent["eFG% Def Rank"] <= 75:
        keys.append("Create clean looks through pace, spacing, and ball movement against strong shot defense.")
    
    if base_team["OR% Rank"] <= 75:
        keys.append("Attack the offensive glass to create second-chance points.")

    if base_team["3P Rate Rank"] <= 75 and opponent["3P Rate Def Rank"] > 250:
        keys.append("Lean into three-point volume when quality catch-and-shoot looks are available.")

    return keys

def generate_matchup_report(base_team, opponent) -> dict:
    """
    Generate a matchup report comparing the base team to a single opponent
    """
    base_team_report = generate_team_report(base_team)
    opponent_report = generate_team_report(opponent)

    report = {
        "base_team": base_team_report["team"],
        "opponent": opponent_report["team"],
        "base_team_archetype": identify_team_archetype(base_team),
        "opponent_archetype": identify_team_archetype(opponent),
        "matchup_summary": generate_matchup_summary(base_team, opponent),
        "base_team_strengths": base_team_report["strengths"],
        "opponent_strengths": opponent_report["strengths"],
        "opponent_weaknesses": opponent_report["weaknesses"],
        "priority_opponent_pressures": format_top_opponent_pressures(base_team, opponent),
        "priority_base_team_edges": format_top_base_team_edges(base_team, opponent),
        "base_team_advantages": get_base_team_advantages(base_team, opponent),
        "opponent_dangers": get_opponent_dangers(base_team, opponent),
        "matchup_swing_factors": get_matchup_swing_factors(base_team, opponent),
        "keys_to_victory": generate_engine_keys_to_victory(base_team, opponent),
    }

    return report

def print_section(title: str, items: list[str], empty_message: str) -> None:
    """
    Print a report section if the section has no items, print a fallback message
    """
    print(f"\n{title}")

    if len(items) == 0:
        print("-", empty_message)
        return

    for item in items:
        print("-", item)

if __name__ == "__main__":
    four_factors = load_torvik_four_factors(SEASON_YEAR)
    four_factors = add_percentile_columns(four_factors)

    if len(sys.argv) > 2:
        base_team_name = sys.argv[1]
        opponent_name = " ".join(sys.argv[2:])
    elif len(sys.argv) > 1:
        base_team_name = "Illinois"
        opponent_name = " ".join(sys.argv[1:])
    else:
        base_team_name = "Illinois"
        opponent_name = "Houston"

    base_team = get_team(four_factors, base_team_name, "TeamName")
    opponent = get_team(four_factors, opponent_name, "TeamName")

    report = generate_matchup_report(base_team, opponent)

    print("Matchup loaded successfully.")
    print("Base team:", report["base_team"])
    print("Opponent:", report["opponent"])
    print("Base team identity:", report["base_team_archetype"])
    print("Opponent identity:", report["opponent_archetype"])
    print("\nScout summary:")
    print(report["matchup_summary"])

    print_section(
        f"{report['base_team']} strengths:",
        report["base_team_strengths"],
        "No major base team strengths flagged by the current thresholds.",
    )

    print_section(
        f"{report['opponent']} strengths:",
        report["opponent_strengths"],
        "No major opponent strengths flagged by the current thresholds.",
    )

    print_section(
        f"{report['opponent']} weaknesses:",
        report["opponent_weaknesses"],
        "No major opponent weaknesses flagged by the current national-threshold model.",
    )

    print_section(
        "Top opponent pressure areas:",
        report["priority_opponent_pressures"],
        "No major opponent pressure areas generated by the percentile matchup engine.",
    )

    print_section(
    f"Top {report['base_team']} edge areas:",
    report["priority_base_team_edges"],
    "No major base team edge areas generated by the percentile matchup engine.",
    )

    print_section(
        f"{report['base_team']} matchup advantages:",
        report["base_team_advantages"],
        "No clear base-team-specific matchup advantages flagged by the current rule set.",
    )

    print_section(
        "Opponent danger areas:",
        report["opponent_dangers"],
        "No major opponent danger areas flagged by the current rule set.",
    )

    print_section(
        "Matchup swing factors:",
        report["matchup_swing_factors"],
        "No major swing factors generated by the current rule set.",
    )

    print_section(
        "Keys to victory:",
        report["keys_to_victory"],
        "No keys generated by the current rule set.",
    )