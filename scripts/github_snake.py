import requests
import json
from datetime import datetime, timedelta
import xml.etree.ElementTree as ET
import os

def fetch_github_contributions(username):
    url = f"https://github.com/users/{username}/contributions"
    response = requests.get(url)
    return response.text

def parse_contributions(html_content):
    # This is a simplified parser and might need adjustment based on GitHub's HTML structure
    contributions = []
    for line in html_content.split('\n'):
        if 'data-count' in line and 'data-date' in line:
            count = line.split('data-count="')[1].split('"')[0]
            date = line.split('data-date="')[1].split('"')[0]
            contributions.append((date, int(count)))
    return contributions

def generate_svg(contributions):
    svg = ET.Element('svg', width="800", height="200", xmlns="http://www.w3.org/2000/svg")
    
    # Define the grid
    for i, (date, count) in enumerate(contributions):
        x = i * 14
        y = 0
        color = get_color(count)
        rect = ET.SubElement(svg, 'rect', x=str(x), y=str(y), width="10", height="10", fill=color)
    
    # Define the snake
    snake = ET.SubElement(svg, 'rect', id="snake", width="10", height="10", fill="green")
    
    # Add CSS animation
    style = ET.SubElement(svg, 'style')
    style.text = """
        @keyframes snake-move {
            0% { transform: translate(0, 0); }
            100% { transform: translate(784px, 0); }
        }
        #snake {
            animation: snake-move 60s linear infinite;
        }
    """
    
    return ET.tostring(svg, encoding='unicode')

def get_color(count):
    if count == 0:
        return "#ebedf0"
    elif count < 5:
        return "#c6e48b"
    elif count < 10:
        return "#7bc96f"
    else:
        return "#196127"

def main():
    # Get the username from the environment variable
    username = os.environ.get('GITHUB_USERNAME')
    if not username:
        raise ValueError("GITHUB_USERNAME environment variable is not set")
    
    html_content = fetch_github_contributions(username)
    contributions = parse_contributions(html_content)
    svg_content = generate_svg(contributions)
    
    with open('github-snake.svg', 'w') as f:
        f.write(svg_content)

if __name__ == "__main__":
    main()