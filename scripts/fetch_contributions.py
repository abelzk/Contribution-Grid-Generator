import requests
import json
from datetime import datetime, timedelta
import math

def fetch_contributions(username):
    # GitHub API endpoint for user contributions
    url = f"https://api.github.com/users/{username}/contributions"
    
    # Fetch data from GitHub API
    response = requests.get(url)
    data = response.json()
    
    # Process and return contribution data
    contributions = []
    for day in data:
        date = datetime.strptime(day['date'], "%Y-%m-%d")
        count = day['count']
        contributions.append({'date': date, 'count': count})
    
    return contributions

def generate_svg_grid(contributions):
    svg = f'''
    <svg width="720" height="112" viewBox="0 0 720 112" xmlns="http://www.w3.org/2000/svg">
        <style>
            .contribution {{ fill: #ebedf0; }}
            .contribution-1 {{ fill: #9be9a8; }}
            .contribution-2 {{ fill: #40c463; }}
            .contribution-3 {{ fill: #30a14e; }}
            .contribution-4 {{ fill: #216e39; }}
            .snake {{ fill: none; stroke: #30a14e; stroke-width: 2; stroke-dasharray: 1000; stroke-dashoffset: 1000; animation: snake-animation 5s linear infinite; }}
            @keyframes snake-animation {{
                0% {{ stroke-dashoffset: 1000; }}
                100% {{ stroke-dashoffset: 0; }}
            }}
        </style>
        <g transform="translate(10, 20)">
    '''
    
    max_contrib = max(c['count'] for c in contributions)
    
    for i, contrib in enumerate(contributions):
        x = i % 52 * 14
        y = i // 52 * 14
        level = min(4, math.ceil(4 * contrib['count'] / max_contrib)) if max_contrib > 0 else 0
        svg += f'<rect class="contribution contribution-{level}" x="{x}" y="{y}" width="10" height="10" />'
    
    # Generate snake path
    path = "M"
    for i in range(52):
        x = i * 14 + 5
        y = 5 if i % 2 == 0 else 91
        path += f"{x},{y} "
    
    svg += f'<path class="snake" d="{path}" />'
    svg += '''
        </g>
    </svg>
    '''
    
    return svg

if __name__ == "__main__":
    username = "your_github_username"
    contributions = fetch_contributions(username)
    svg_grid = generate_svg_grid(contributions)
    
    # Save SVG to file
    with open("contribution_snake.svg", "w") as f:
        f.write(svg_grid) 