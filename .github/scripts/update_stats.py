import json
import re
import urllib.request
from pathlib import Path

USERNAME = "auzungol"

def fetch_followers():
    req = urllib.request.Request(
        f"https://api.github.com/users/{USERNAME}",
        headers={"User-Agent": "profile-stats-bot", "Accept": "application/vnd.github+json"},
    )
    with urllib.request.urlopen(req, timeout=15) as resp:
        data = json.load(resp)
    return int(data.get("followers", 0))

def fetch_views():
    req = urllib.request.Request(
        f"https://komarev.com/ghpvc/?username={USERNAME}",
        headers={"User-Agent": "profile-stats-bot"},
    )
    with urllib.request.urlopen(req, timeout=15) as resp:
        svg_text = resp.read().decode("utf-8", errors="ignore")
    numbers = re.findall(r">(\d[\d,]*)<", svg_text)
    if not numbers:
        raise RuntimeError("Could not find view count in komarev response")
    return int(numbers[-1].replace(",", ""))

def format_tr(n):
    return f"{n:,}".replace(",", ".")

TEMPLATE = """<svg xmlns="http://www.w3.org/2000/svg" width="420" height="100" viewBox="0 0 420 100">
  <style>
    .num {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Ubuntu, Helvetica, Arial, sans-serif; font-size: 32px; font-weight: 700; fill: #ffffff; }}
    .lbl {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Ubuntu, Helvetica, Arial, sans-serif; font-size: 13px; fill: #8b949e; }}
  </style>
  <line x1="210" y1="18" x2="210" y2="82" stroke="#30363d" stroke-width="1" opacity="0.7"/>
  <text x="105" y="46" text-anchor="middle" class="num">{views}</text>
  <text x="105" y="70" text-anchor="middle" class="lbl">Profil G&#246;r&#252;nt&#252;lenme</text>
  <text x="315" y="46" text-anchor="middle" class="num">{followers}</text>
  <text x="315" y="70" text-anchor="middle" class="lbl">Takip&#231;i</text>
</svg>
"""

def main():
    followers = fetch_followers()
    views = fetch_views()
    svg = TEMPLATE.format(views=format_tr(views), followers=format_tr(followers))
    out_path = Path(__file__).resolve().parents[2] / "extra-stats.svg"
    out_path.write_text(svg, encoding="utf-8")
    print(f"Updated extra-stats.svg: views={views}, followers={followers}")

if __name__ == "__main__":
    main()
