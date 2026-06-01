import pandas as pd

METRIC_DIRECTIONS = {
    # True means higher values are better
    
    "eFG%": True,
    "eFG% Def": False,

    "FTR": True,
    "FTR Def": False,

    "OR%": True,
    "DR%": True,

    "TO%": False,
    "TO% Def.": True,

    "3P%": True,
    "3P% Def": False,

    "3P Rate": True,
    "3P Rate Def": False,
}

def add_percentile_columns(df: pd.DataFrame) -> pd.DataFrame:
    """
    Add percentile columns for each Four Factors metric

    Each percentile is scaled from 0-100, where higher is always better

    Returns a copy of original dataframe with new percentile columns
    """
    result = df.copy()

    for metric, higher_is_better in METRIC_DIRECTIONS.items():
        if metric not in result.columns:
            raise KeyError(f"Missing expected metric column: {metric}")
        
        numeric_values = pd.to_numeric(result[metric], errors="coerce")

        percentile_col = f"{metric} Percentile"

        result[percentile_col] = (
            numeric_values.rank(
                pct=True,
                ascending=higher_is_better
            ) * 100
        ).round(1)

    return result

def get_percentile_column(metric: str) -> str:
    """
    Return the percentile column name for a given metric
    """
    return f"{metric} Percentile"

def get_metric_percentile(team_row: pd.Series, metric: str) -> float:
    """
    Return a team's percentile for a single metric
    """
    percentile_col = get_percentile_column(metric)
    return float(team_row[percentile_col])