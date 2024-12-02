import requests
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
from apscheduler.schedulers.blocking import BlockingScheduler
from instagrapi import Client
import os
import random
import config

def get_random_quote():
    response = requests.get(config.QUOTES_API_URL)
    if response.status_code == 200:
        quote_data = response.json()[0]
        return f"{quote_data['q']} - {quote_data['a']}"
    else:
        print("Error fetching quote")
        return None

def get_random_image():
    headers = {"Authorization": f"Client-ID {config.UNSPLASH_ACCESS_KEY}"}
    response = requests.get(config.UNSPLASH_API_URL, headers=headers)
    if response.status_code == 200:
        image_url = response.json()["urls"]["regular"]
        img_response = requests.get(image_url)
        return Image.open(BytesIO(img_response.content))
    else:
        print("Error fetching image")
        return None

def create_image_with_text(quote):
    image = get_random_image()
    if image is None or quote is None:
        return None

    # Set margins and maximum width/height for the text area
    margin = 20
    max_width = image.width - 2 * margin
    max_height = image.height - 2 * margin

    # Load font and adjust size to fit text within margins
    font_size = 50
    font = None
    draw = ImageDraw.Draw(image)  # Initialize draw object here

    while font_size > 10:
        try:
            font = ImageFont.truetype("arial.ttf", font_size)
        except IOError:
            font = ImageFont.load_default()

        # Wrap text within max width
        lines = []
        words = quote.split()
        line = ""
        
        for word in words:
            # Check if adding the word exceeds max width
            if draw.textlength(line + word + " ", font=font) <= max_width:
                line += word + " "
            else:
                lines.append(line.strip())
                line = word + " "
        lines.append(line.strip())

        # Calculate total text height
        text_height = sum(draw.textbbox((0, 0), line, font=font)[3] - draw.textbbox((0, 0), line, font=font)[1] for line in lines)

        if text_height <= max_height:
            break
        font_size -= 2  # Reduce font size if text exceeds the allowed height

    # Draw text centered with a 20dp margin and white color
    y = (image.height - text_height) / 2
    for line in lines:
        text_width = draw.textbbox((0, 0), line, font=font)[2]
        x = (image.width - text_width) / 2
        draw.text((x, y), line, font=font, fill="white")
        y += draw.textbbox((0, 0), line, font=font)[3] - draw.textbbox((0, 0), line, font=font)[1]  # Move y down by the height of the line

    # Resize image to meet Instagram's aspect ratio requirements (e.g., 4:5 for portrait)
    aspect_ratio = 4 / 5
    if image.width / image.height < aspect_ratio:
        new_width = int(image.height * aspect_ratio)
        image = image.resize((new_width, image.height), Image.LANCZOS)
    else:
        new_height = int(image.width / aspect_ratio)
        image = image.resize((image.width, new_height), Image.LANCZOS)

    # Save image locally
    os.makedirs("images", exist_ok=True)
    file_path = f"images/motivation_{random.randint(1000, 9999)}.png"
    image.save(file_path)
    return file_path

def post_to_instagram(image_path):
    # Initialize the client
    client = Client()

    # Login to Instagram
    client.login(config.INSTAGRAM_USERNAME, config.INSTAGRAM_PASSWORD)

    # Upload the photo with the caption
    media = client.photo_upload(image_path, caption="Your daily motivation!")

    # Extract media ID
    print(f"Photo uploaded successfully! Media ID: {media.id}")

def main():
    quote = get_random_quote()
    if quote:
        image_path = create_image_with_text(quote)
        if image_path:
            print(f"Image created successfully: {image_path}")
            post_to_instagram(image_path)
        else:
            print("Failed to create image.")
    else:
        print("Failed to fetch quote.")

if __name__ == "__main__":
    main()