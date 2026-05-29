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
    if illinois["TO% Rank"] <= 75 and opponent["TO% Def. Rank"] > 250:
        advantages.append(
            f"Illinois's ball security matches up well against a {opponent['TeamName']} defense that does not force many turnovers."
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

def get_matchup_swing_factors(illinois, opponent) -> list[str]:
    """
    Identify relative matchup themes that may matter even when there is no obvious national-level weakness.
    """
    factors = []

    if illinois["OR% Rank"] <= 75 and opponent["DR% Rank"] <= 150:
        factors.append(
            f"Possession battle: Illinois is strong on the offensive glass, but {opponent['TeamName']} is not a clear defensive rebounding liability. Second-chance points may depend on effort, lineup choices, and physicality."
        )
    elif illinois["OR% Rank"] <= 75 and opponent["DR% Rank"] > 150:
        factors.append(
            f"Possession battle: Illinois has a likely offensive rebounding edge against {opponent['TeamName']}. Extra possessions could be a major swing factor."
        )

    if opponent["OR% Rank"] <= 75:
        factors.append(
            f"Defensive glass: {opponent['TeamName']} is strong on the offensive boards, so Illinois must prevent second-chance possessions."
        )

    if illinois["FTR Def Rank"] <= 75 and opponent["FTR Rank"] <= 75:
        factors.append(
            f"Foul game: {opponent['TeamName']} generates free throws well, but Illinois is strong at defending without fouling. Whichever side wins that tension could shape the game."
        )
    elif illinois["FTR Def Rank"] <= 75 and opponent["FTR Rank"] > 250:
        factors.append(
            f"Foul game: Illinois defends without fouling, and {opponent['TeamName']} already struggles to get to the line. This could limit easy points for the opponent."
        )

    if illinois["3P Rate Rank"] <= 75:
        factors.append(
            "Shot profile: Illinois takes a high volume of threes, so shot quality and three-point variance could heavily influence the matchup."
        )

    if opponent["3P Rate Rank"] <= 75:
        factors.append(
            f"Perimeter defense: {opponent['TeamName']} takes a high volume of threes, so Illinois must stay disciplined on closeouts and rotations."
        )

    if opponent["eFG% Def Rank"] <= 75:
        factors.append(
            f"Shot creation test: {opponent['TeamName']} has strong shot defense, so Illinois may need pace, spacing, and offensive rebounding to avoid stagnant half-court possessions."
        )

    if opponent["TO% Def. Rank"] <= 75 and illinois["TO% Rank"] <= 75:
        factors.append(
            f"Pressure vs. poise: {opponent['TeamName']} creates turnovers, but Illinois is strong at protecting the ball. This is a key matchup strength-on-strength."
        )

    return factors

def generate_keys_to_victory(illinois, opponent) -> list[str]:
    """
    Generate concise keys to victory for Illinois
    """
    keys = []

    if opponent["OR% Rank"] <= 75:
        keys.append("Finish defensive possessions with physical box-outs and team rebounding.")

    if opponent["TO% Def. Rank"] <= 75:
        keys.append("Value the ball and avoid live-ball turnovers against defensive pressure.")
    
    if opponent["TO% Def. Rank"] > 250 and illinois["TO% Rank"] <= 75:
        keys.append("Run organized offense and avoid self-inflicted turnovers against a defense that does not create many turnovers.")

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
        "matchup_swing_factors": get_matchup_swing_factors(illinois, opponent),
        "keys_to_victory": generate_keys_to_victory(illinois, opponent),
    }

    return report

def print_section(title: str, items: list[str], empty_message: str) -> None:
    """
    Print a report section. If the section has no items, print a fallback message.
    """
    print(f"\n{title}")

    if len(items) == 0:
        print("-", empty_message)
        return

    for item in items:
        print("-", item)

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

    print_section(
    "Illinois strengths:",
    report["illinois_strengths"],
    "No major Illinois strengths flagged by the current thresholds.",
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
        "Illinois matchup advantages:",
        report["illinois_advantages"],
        "No clear Illinois-specific matchup advantages flagged by the current rule set.",
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