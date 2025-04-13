from flask import Flask, render_template, request
import pandas as pd
import os
import math

app = Flask(__name__)

DEFAULT_FILE = "online database.csv"
BET_RETURN_FILE = "online database w bet return.csv"

@app.route('/', methods=['GET', 'POST'])
def index():
    file_choice = request.form.get('bet_return', 'no') if request.method == 'POST' else 'no'
    selected_file = BET_RETURN_FILE if file_choice == 'yes' else DEFAULT_FILE

    df = pd.read_csv(selected_file)

    sports = sorted(df['Sport'].dropna().unique())
    types = sorted(df['Type'].dropna().unique())
    platforms = sorted(df['Platform'].dropna().unique())
    wide_ranges = sorted(df['Wide Odd Range'].dropna().unique())
    narrow_ranges = sorted(df['Narrow Odd Range'].dropna().unique())
    odds_list = sorted(df['Odd'].dropna().unique())
    stakes = sorted(df['Stake'].dropna().unique())

    if request.method == 'POST':
        sport = request.form.get('sport', '').strip()
        bet_type = request.form.get('type', '').strip()
        platform = request.form.get('platform', '').strip()
        odds = request.form.get('odds', '').strip()
        wide_range = request.form.get('wide_range', '').strip()
        narrow_range = request.form.get('narrow_range', '').strip()
        stake = request.form.get('stake', '').strip()

        filters_applied = [f"Bet Return: {'Yes' if file_choice == 'yes' else 'No'}"]

        if sport:
            df = df[df['Sport'].astype(str).str.lower() == sport.lower()]
            filters_applied.append(f"Sport: {sport}")
        if bet_type:
            df = df[df['Type'].astype(str).str.lower() == bet_type.lower()]
            filters_applied.append(f"Type: {bet_type}")
        if platform:
            df = df[df['Platform'].astype(str).str.lower() == platform.lower()]
            filters_applied.append(f"Platform: {platform}")
        if odds:
            try:
                df = df[df['Odd'].astype(float) == float(odds)]
                filters_applied.append(f"Odds: {odds}")
            except:
                pass
        if wide_range:
            df = df[df['Wide Odd Range'].astype(str).str.lower() == wide_range.lower()]
            filters_applied.append(f"Wide Range: {wide_range}")
        if narrow_range:
            df = df[df['Narrow Odd Range'].astype(str).str.lower() == narrow_range.lower()]
            filters_applied.append(f"Narrow Range: {narrow_range}")
        if stake:
            try:
                df = df[df['Stake'].astype(float) == float(stake)]
                filters_applied.append(f"Stake: {stake}")
            except:
                pass

        try:
            total_profit = round(df['Profit/Loss'].sum(), 2)
        except:
            total_profit = 0.0

        total_wins = len(df[df['Result'].astype(str).str.upper() == 'W'])
        total_losses = len(df[df['Result'].astype(str).str.upper() == 'L'])
        total_pushes = len(df[df['Result'].astype(str).str.upper() == 'P'])
        total_bets = len(df)

        win_rate = round((total_wins / (total_wins + total_losses)) * 100, 2) if (total_wins + total_losses) > 0 else 0
        profit_per_bet = round(total_profit / total_bets, 2) if total_bets > 0 else 0.0

        if total_bets <= 50:
            confidence = "Low"
            confidence_percent = 33
        elif total_bets <= 200:
            confidence = "Medium"
            confidence_percent = 66
        else:
            confidence = "High"
            confidence_percent = 100

        return render_template(
            'results.html',
            profit=total_profit,
            win_rate=win_rate,
            total_bets=total_bets,
            profit_per_bet=profit_per_bet,
            confidence_level=confidence,
            confidence_percent=confidence_percent,
            wins=total_wins,
            losses=total_losses,
            pushes=total_pushes,
            filters_applied=filters_applied
        )

    return render_template(
        'index.html',
        sports=sports,
        types=types,
        platforms=platforms,
        wide_ranges=wide_ranges,
        narrow_ranges=narrow_ranges,
        odds=odds_list,
        stakes=stakes
    )

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))
