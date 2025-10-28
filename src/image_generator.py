import os
from PIL import Image, ImageDraw, ImageFont
from src.app import get_countries, get_status

def generate_summary_image():
    if not os.path.exists("cache"):
        os.makedirs("cache")

    # Get data
    status = get_status()
    total_countries = status["total_countries"]
    last_refreshed = status["last_refreshed_at"]
    top_countries = get_countries(sort="gdp_desc")[:5]

    # Create image
    img = Image.new("RGB", (600, 400), color=(255, 255, 255))
    d = ImageDraw.Draw(img)
    font_path = "arial.ttf"  # Make sure you have this font or use default
    font = ImageFont.load_default()

    d.text((20, 20), f"Total Countries: {total_countries}", fill=(0, 0, 0), font=font)
    d.text((20, 50), f"Last Refreshed: {last_refreshed}", fill=(0, 0, 0), font=font)
    d.text((20, 80), "Top 5 Countries by Estimated GDP:", fill=(0, 0, 0), font=font)

    y = 110
    for country in top_countries:
        d.text((40, y), f"{country['name']}: {country['estimated_gdp']:.2f}", fill=(0, 0, 0), font=font)
        y += 30

    img.save("cache/summary.png")
