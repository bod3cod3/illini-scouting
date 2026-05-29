import pandas as pd

def load_torvik_team_results(year: int = 2026) -> pd.DataFrame:
    """
    Load team-level BartTorvik data for a given college basketball season

    Params:
        year: the season year (2026 means 2025-2026)

    Returns: 
        Pandas Dataframe with team results
    
    """
    url = f"https://barttorvik.com/{year}_team_results.csv"

    df = pd.read_csv(url)

    return df

def get_team(df: pd.DataFrame, team_name: str, team_column: str) -> pd.Series:
    """
    Return one team's row from a DataFrame

    Params: 
        df: Full DataFrame
        team_name: Exact name of team
        team_column: Column containing team names

    Returns: 
        Pandas Series corresponding to a single team
    """
    clean_team_names = df[team_column].astype(str).str.strip().str.lower()
    clean_search_name = team_name.strip().lower()

    matches = df[clean_team_names == clean_search_name]

    if matches.empty:
        raise ValueError(f"Could not find team: {team_name}")
    
    return matches.iloc[0]

def load_torvik_four_factors(year: int = 2026) -> pd.DataFrame:
    """
    Load and clean BartTorvik Four Factors data for a given college basketball season.

    Params:
        year: The season year (2026 means 2025-2026)

    Returns:
        A cleaned pandas DataFrame with team names and Four Factors data
    """
    url = f"https://barttorvik.com/{year}_fffinal.csv"

    raw = pd.read_csv(url)
    raw = raw.reset_index()

    clean = pd.DataFrame()

    clean["TeamName"] = raw["level_0"]

    clean["eFG%"] = raw["level_1"]
    clean["eFG% Rank"] = raw["level_2"]
    clean["eFG% Def"] = raw["level_3"]
    clean["eFG% Def Rank"] = raw["TeamName"]

    clean["FTR"] = raw["eFG%"]
    clean["FTR Rank"] = raw["Rk"]
    clean["FTR Def"] = raw["eFG% Def"]
    clean["FTR Def Rank"] = raw["Rk.1"]

    clean["OR%"] = raw["FTR"]
    clean["OR% Rank"] = raw["Rk.2"]
    clean["DR%"] = raw["FTR Def"]
    clean["DR% Rank"] = raw["Rk.3"]

    clean["TO%"] = raw["OR%"]
    clean["TO% Rank"] = raw["Rk.4"]
    clean["TO% Def."] = raw["DR%"]
    clean["TO% Def. Rank"] = raw["Rk.5"]

    clean["3P%"] = raw["TO%"]
    clean["3P% Rank"] = raw["Rk.6"]
    clean["3P% Def"] = raw["TO% Def."]
    clean["3P% Def Rank"] = raw["Rk.7"]

    clean["3P Rate"] = raw["ft%"]
    clean["3P Rate Rank"] = raw["rk.4"]
    clean["3P Rate Def"] = raw["ft%D"]
    clean["3P Rate Def Rank"] = raw["rk.5"]

    return clean

if __name__ == "__main__":
    teams = load_torvik_team_results(2026)
    team_name = "Illinois"

    print("Data loaded successfully.")
    print("Shape:", teams.shape)

    print(f"\n{team_name} scouting basics:")
    team = get_team(teams, team_name, "team")

    print("Team:", team["team"])
    print("Conference:", team["conf"])
    print("Record:", team["record"])
    print("Rank:", team["rank"])
    print("Adjusted Offensive Efficiency:", f"{team['adjoe']:.1f}")
    print("Adjusted Defensive Efficiency:", f"{team['adjde']:.1f}")
    print("Overall Rating:", f"{team['barthag']:.3f}")
    print("Adjusted Tempo:", f"{team['adjt']:.1f}")

    four_factors = load_torvik_four_factors(2026)

    print("\nFour Factors data loaded successfully.")
    print("Shape:", four_factors.shape)

    team_ff = get_team(four_factors, team_name, "TeamName")
    
    print(f"\n{team_name} Four Factors:")
    print("Team:", team_ff["TeamName"])
    print("Offensive eFG%:", f"{team_ff['eFG%']:.1f}")
    print("Defensive eFG% Allowed:", f"{team_ff['eFG% Def']:.1f}")
    print("Free Throw Rate:", f"{team_ff['FTR']:.1f}")
    print("Free Throw Rate Allowed:", f"{team_ff['FTR Def']:.1f}")
    print("Offensive Rebounding %:", f"{team_ff['OR%']:.1f}")
    print("Defensive Rebounding %:", f"{team_ff['DR%']:.1f}")
    print("Turnover %:", f"{team_ff['TO%']:.1f}")
    print("Turnover % Forced:", f"{team_ff['TO% Def.']:.1f}")
    print("3P%:", f"{team_ff['3P%']:.1f}")
    print("3P% Allowed:", f"{team_ff['3P% Def']:.1f}")
    print("3P Rate:", f"{team_ff['3P Rate']:.1f}")
    print("3P Rate Allowed:", f"{team_ff['3P Rate Def']:.1f}")
    
    
