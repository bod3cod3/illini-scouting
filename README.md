# Men's Basketball Opponent Prep Dashboard

## Overview

This project is a Python and Streamlit dashboard built to help coaching staff evaluate college basketball opponents before games. The app uses BartTorvik Four Factors data to compare a selected base team against an opponent and identify certain matchup areas that favor or threaten the base team.

Built with Python, Streamlit, pandas, and Plotly.

## Live App

Live dashboard: [https://illini-scouting-6555.streamlit.app/](https://illini-scouting-6555.streamlit.app/)

GitHub Repository: [https://github.com/bod3cod3/illini-scouting](https://github.com/bod3cod3/illini-scouting)

## Why This is Helpful

This project will allow coaching staff to efficiently analyze raw statistics, identifying where a team can create advantages in an upcoming matchup. The dashboard turns team stats into a structured scouting report, identifying potential pressure points, offensive edges, strength-on-strength matchups, and keys to victory for the base team.

The goal of this project is to help coaching staff or analysts quickly understand important statistics surrounding a matchup.

## Key Features

- Select any base team and opponent from the BartTorvik dataset
- Generate a one-paragraph matchup summary
- Identify top opponent pressure areas
- Identify top base-team edge areas
- Assign each area a base favorability score
- Display a matchup favorability chart
- Show supporting statistics in a table
- Generate keys to victory based on public data

## Matchup Engine Explained

The matchup engine compares the base team's and opponent's Four Factors data using percentile-based scores. Percentiles are consistent in that a higher percentile is always better, even for defensive metrics. 

The main score in the app is **base favorability**. This score, which ranges from 0 to 100, is always shown from the perspective of the base team, where:

- A score near 100 means the matchup strongly favors the base team.
- A score near 50 means the matchup is closer to neutral.
- A score near 0 means the matchup strongly favors the opponent. 

The app evaluates two types of matchup areas. **Opponent pressure areas** are areas where the opponent's offensive metrics match up against the base team's corresponding defensive metrics. **Base-team edge areas** are areas where the base team's offensive metrics match up against the opponent's corresponding defensive metrics.

The area label describes the direction of the matchup, while the base favorability score determines whether that area is actually good or bad for the base team.

## Data Source

This project uses public BartTorvik Four Factors data for the 2025-2026 men's college basketball season. 

Once loaded, the raw data is cleaned in `src/load_data.py` and converted to percentile-based metrics in `src/metrics.py`. 

The dashboard only uses public data and does not incorporate player tracking data or private scouting information. 

## How to Run Locally

While the easiest way to view the dashboard is through the live Streamlit link above, you can run this project locally by cloning the repository and installing the required dependencies.

Run the following in your CLI:

```bash
git clone https://github.com/bod3cod3/illini-scouting.git
cd illini-scouting
pip install -r requirements.txt
streamlit run app.py
```

## Example Matchup

**Illinois vs. Houston**

In this example matchup, Illinois is identified as a two-way efficiency team, while Houston is identified as a possession-control pressure team.

The engine identifies Houston's offensive rebounding as the top opponent pressure area, with Illinois' three-point volume as the top base-team edge area. 

The favorability chart confirms those takeaways, and the engine identifies that one of Illinois' keys to victory is to finish defensive possessions with five-man box-outs while still leaning into quality three-point opportunities. 

