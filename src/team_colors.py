DEFAULT_TEAM_COLORS = {
    "primary": "#1F2937",
    "secondary": "#E5E7EB",
}


TEAM_COLORS = {
    "Illinois": {
        "primary": "#13294B",
        "secondary": "#FF5F05",
    },
    "Houston": {
        "primary": "#C8102E",
        "secondary": "#FFFFFF",
    },
    "Florida": {
        "primary": "#0021A5",
        "secondary": "#FA4616",
    },
    "Chicago St.": {
        "primary": "#006747",
        "secondary": "#FFFFFF",
    },
    "Purdue": {
        "primary": "#CEB888",
        "secondary": "#000000",
    },
    "Indiana": {
        "primary": "#990000",
        "secondary": "#EEEDEB",
    },
    "Michigan St.": {
        "primary": "#18453B",
        "secondary": "#FFFFFF",
    },
    "Michigan": {
        "primary": "#00274C",
        "secondary": "#FFCB05",
    },
    "Ohio St.": {
        "primary": "#BB0000",
        "secondary": "#666666",
    },
    "Wisconsin": {
        "primary": "#C5050C",
        "secondary": "#FFFFFF",
    },
    "Maryland": {
        "primary": "#E03A3E",
        "secondary": "#FFD520",
    },
    "Iowa": {
        "primary": "#000000",
        "secondary": "#FFCD00",
    },
    "Northwestern": {
        "primary": "#4E2A84",
        "secondary": "#FFFFFF",
    },
    "Nebraska": {
        "primary": "#E41C38",
        "secondary": "#FFFFFF",
    },
    "Minnesota": {
        "primary": "#7A0019",
        "secondary": "#FFCC33",
    },
    "UCLA": {
        "primary": "#2D68C4",
        "secondary": "#FFD100",
    },
    "USC": {
        "primary": "#990000",
        "secondary": "#FFC72C",
    },
    "Oregon": {
        "primary": "#154733",
        "secondary": "#FEE123",
    },
    "Washington": {
        "primary": "#4B2E83",
        "secondary": "#B7A57A",
    },
    "North Carolina": {
        "primary": "#4B9CD3",
        "secondary": "#13294B",
    },
    "Duke": {
        "primary": "#00539B",
        "secondary": "#FFFFFF",
    },
    "Kansas": {
        "primary": "#0051BA",
        "secondary": "#E8000D",
    },
    "Kentucky": {
        "primary": "#0033A0",
        "secondary": "#FFFFFF",
    },
    "Arizona": {
        "primary": "#CC0033",
        "secondary": "#003366",
    },
    "Gonzaga": {
        "primary": "#041E42",
        "secondary": "#C8102E",
    },
    "Alabama": {
        "primary": "#9E1B32",
        "secondary": "#FFFFFF",
    },
    "Auburn": {
        "primary": "#0C2340",
        "secondary": "#F26522",
    },
    "Tennessee": {
        "primary": "#FF8200",
        "secondary": "#FFFFFF",
    },
    "Arkansas": {
        "primary": "#9D2235",
        "secondary": "#FFFFFF",
    },
    "Texas": {
        "primary": "#BF5700",
        "secondary": "#FFFFFF",
    },
    "Texas A&M": {
        "primary": "#500000",
        "secondary": "#FFFFFF",
    },
    "Baylor": {
        "primary": "#154734",
        "secondary": "#FFB81C",
    },
    "Iowa St.": {
        "primary": "#C8102E",
        "secondary": "#F1BE48",
    },
    "Marquette": {
        "primary": "#003366",
        "secondary": "#FFCC00",
    },
    "Creighton": {
        "primary": "#005CA9",
        "secondary": "#FFFFFF",
    },
    "Villanova": {
        "primary": "#00205B",
        "secondary": "#13B5EA",
    },
    "UConn": {
        "primary": "#000E2F",
        "secondary": "#FFFFFF",
    },
    "St. John's": {
        "primary": "#BA0C2F",
        "secondary": "#FFFFFF",
    },
}


def get_team_colors(team_name: str) -> dict:
    """
    Return team colors for app branding
    """
    return TEAM_COLORS.get(team_name, DEFAULT_TEAM_COLORS)