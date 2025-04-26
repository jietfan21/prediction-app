from flask import Flask, render_template, request
import pandas as pd
import os
import math
import statistics
import scipy.stats as stats

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
        sports_selected = request.form.getlist('sport[]')
        types_selected = request.form.getlist('type[]')
        platforms_selected = request.form.getlist('platform[]')
        odds = request.form.get('odds', '').strip()
        wide_ranges_selected = request.form.getlist('wide_range[]')
        narrow_ranges_selected = request.form.getlist('narrow_range[]')
        stakes_selected = request.form.getlist('stake[]')

        filters_applied = [f"Bet Return: {'Yes' if file_choice == 'yes' else 'No'}"]

        if sports_selected:
            df = df[df['Sport'].astype(str).str.lower().isin([s.lower() for s in sports_selected])]
            filters_applied.append(f"Sports: {', '.join(sports_selected)}")
        if types_selected:
            df = df[df['Type'].astype(str).str.lower().isin([t.lower() for t in types_selected])]
            filters_applied.append(f"Types: {', '.join(types_selected)}")
        if platforms_selected:
            df = df[df['Platform'].astype(str).str.lower().isin([p.lower() for p in platforms_selected])]
            filters_applied.append(f"Platforms: {', '.join(platforms_selected)}")
        if odds:
            try:
                df = df[df['Odd'].astype(float) == float(odds)]
                filters_applied.append(f"Odds: {odds}")
            except:
                pass
        if wide_ranges_selected:
            df = df[df['Wide Odd Range'].astype(str).str.lower().isin([w.lower() for w in wide_ranges_selected])]
            filters_applied.append(f"Wide Range: {', '.join(wide_ranges_selected)}")
        if narrow_ranges_selected:
            df = df[df['Narrow Odd Range'].astype(str).str.lower().isin([n.lower() for n in narrow_ranges_selected])]
            filters_applied.append(f"Narrow Range: {', '.join(narrow_ranges_selected)}")
        if stakes_selected:
            try:
                df = df[df['Stake'].astype(float).isin([float(s) for s in stakes_selected])]
                filters_applied.append(f"Stake: {', '.join(stakes_selected)}")
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

        # One-Tailed Confidence
        margin_of_error = 0.1
        filtered_profits = df['Profit/Loss'].dropna().tolist()
        n = len(filtered_profits)

        if n >= 2:
            sd = statistics.stdev(filtered_profits)
            z_score = (margin_of_error * math.sqrt(n)) / sd if sd > 0 else 0
            confidence_percent = round(stats.norm.cdf(z_score) * 100, 2)
        else:
            sd = 0
            z_score = 0
            confidence_percent = 0

        if confidence_percent < 50:
            confidence_level = "Low"
        elif confidence_percent < 75:
            confidence_level = "Medium"
        else:
            confidence_level = "High"

        return render_template(
            'results.html',
            profit=total_profit,
            win_rate=win_rate,
            total_bets=total_bets,
            profit_per_bet=profit_per_bet,
            confidence_level=confidence_level,
            confidence_percent=confidence_percent,
            z_score=round(z_score, 2),
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
