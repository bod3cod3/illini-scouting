def get_base_team_advantages(base_team, opponent) -> list[str]:
    """
    Identify legacy rank-rule areas where the base team may have an advantage
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
    Identify legacy rank-rule areas where the opponent may create problems for the base team
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
    Identify legacy rank-rule matchup themes that may matter
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