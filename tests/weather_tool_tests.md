import os
from tools.weather import get_weather

os.makedirs("tests", exist_ok=True)

test_cases = [
    ("Mumbai", "2026-05-15"),
    ("Pune", "2026-05-16"),
    ("Hyderabad", "2026-04-01"),
    ("Kolkata", "2026-05-15"),
    ("Pune", "2026-05-32"),
    ("Bengaluru", "2026-06-10")
]

markdown_lines = ["# Weather Tool Test Cases & Outputs\n"]

for city, date in test_cases:
    res = get_weather(city, date)
    markdown_lines.append(f"### Input: city='{city}', date='{date}'")
    markdown_lines.append(f"```json\n{res}\n```\n")

with open("tests/weather_tool_tests.md", "w") as f:
    f.write("\n".join(markdown_lines))

print("tests/weather_tool_tests.md successfully generated!")
