from pathlib import Path
import sys

import pandas as pd

ROOT_DIR = Path(__file__).resolve().parents[1]
SRC_DIR = ROOT_DIR / "src"
sys.path.append(str(SRC_DIR))

from matchup_engine import (
    calculate_base_favorability_score,
    calculate_pressure_score,
    get_edge_matchup_type,
    get_matchup_evidence_rows,
    get_pressure_matchup_type,
)


def make_team(name: str, percentiles: dict) -> pd.Series:
    """
    Build a fake team row for matchup engine tests
    """
    row = {"TeamName": name}

    for metric, percentile in percentiles.items():
        row[f"{metric} Percentile"] = percentile

    return pd.Series(row)


def test_pressure_score_combines_opponent_strength_and_base_vulnerability():
    score = calculate_pressure_score(
        opponent_strength=90,
        base_resistance=20,
    )

    assert score == 85.0


def test_base_favorability_score_is_higher_when_base_matchup_is_better():
    score = calculate_base_favorability_score(
        base_percentile=90,
        opponent_percentile=20,
    )

    assert score == 85.0

def test_pressure_matchup_type_identifies_clear_pressure_point():
    pressure = {
        "opponent_strength": 90,
        "base_resistance": 20,
    }

    assert get_pressure_matchup_type(pressure) == "Clear pressure point"


def test_edge_matchup_type_identifies_clear_edge():
    edge = {
        "base_strength": 90,
        "opponent_resistance": 20,
    }

    assert get_edge_matchup_type(edge) == "Clear edge"


def test_matchup_evidence_rows_include_pressure_and_edge_context():
    base_team = make_team(
        "Illinois",
        {
            "OR%": 85,
            "DR%": 20,
            "3P Rate": 90,
            "3P Rate Def": 30,
            "eFG%": 80,
            "eFG% Def": 70,
            "TO%": 75,
            "TO% Def.": 55,
            "FTR": 60,
            "FTR Def": 80,
        },
    )

    opponent = make_team(
        "Houston",
        {
            "OR%": 95,
            "DR%": 80,
            "3P Rate": 70,
            "3P Rate Def": 40,
            "eFG%": 85,
            "eFG% Def": 90,
            "TO%": 65,
            "TO% Def.": 85,
            "FTR": 75,
            "FTR Def": 70,
        },
    )

    rows = get_matchup_evidence_rows(base_team, opponent)

    assert len(rows) == 6

    required_keys = {
    "area",
    "direction",
    "matchup_type",
    "base_favorability_score",
    "base_team",
    "base_metric_display_name",
    "base_metric_abbreviation",
    "base_percentile",
    "opponent",
    "opponent_metric_display_name",
    "opponent_metric_abbreviation",
    "opponent_percentile",
    }

    for row in rows:
        assert required_keys.issubset(row.keys())

    directions = {row["direction"] for row in rows}

    assert "Opponent pressure" in directions
    assert "Base team edge" in directions

    for row in rows:
        assert row["base_team"] == "Illinois"
        assert row["opponent"] == "Houston"
        assert 0 <= row["base_favorability_score"] <= 100