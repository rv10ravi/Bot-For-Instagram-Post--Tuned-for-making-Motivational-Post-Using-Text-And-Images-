# Instagram Motivational Post Bot

This project automates the creation and posting of motivational content on Instagram. It fetches quotes from an API, overlays them on visually appealing images, and posts the resulting content to Instagram.

---

## Features

- **Automated Quote Fetching**: Retrieves motivational quotes from a quotes API.
- **Dynamic Image Fetching**: Downloads random images from Unsplash.
- **Image Editing**: Adds motivational quotes to images using customizable fonts and layouts.
- **Instagram Integration**: Logs in and posts the final images directly to your Instagram account.
- **Scheduled Posting**: (Optional) Can be extended to post at specified times.

---

## Prerequisites

### 1. Python Environment
Ensure you have Python 3.8+ installed. Required libraries:

- `requests`
- `Pillow`
- `apscheduler`
- `instagrapi`

Install dependencies:
pip install -r requirements.txt

2. API Keys

    Quotes API: Get a URL endpoint for fetching motivational quotes.
    Unsplash API: Sign up at Unsplash Developers to get an access key for fetching images.

3. Instagram Credentials

    Ensure you have a valid Instagram account.
    Enable "Allow login from third-party apps" in Instagram settings if applicable.

Configuration

Update the config.py file with the following:

# Quotes API Endpoint
QUOTES_API_URL  = "<your_quotes_api_url>"

# Unsplash API
UNSPLASH_API_URL = "https://api.unsplash.com/photos/random"
UNSPLASH_ACCESS_KEY = "<your_unsplash_access_key>"

# Instagram Credentials
INSTAGRAM_USERNAME = "<your_instagram_username>"
INSTAGRAM_PASSWORD = "<your_instagram_password>"
## How It Works

### Workflow

1. Fetches a random motivational quote.
2. Downloads a random image from Unsplash.
3. Overlays the quote on the image.
4. Posts the final image to Instagram.

### File Structure

project-directory/ ├── bot.py # Main script for bot logic ├── config.py # Configuration file ├── images/ # Directory for saving generated images └── requirements.txt # Python dependencies


### Running the Bot

Run the script:


python bot.py

Extending the Functionality
Scheduling Posts

Add scheduling logic to post multiple times per day using apscheduler. Example:

from apscheduler.schedulers.blocking import BlockingScheduler

scheduler = BlockingScheduler()
scheduler.add_job(main, 'cron', hour=8, minute=0)
scheduler.add_job(main, 'cron', hour=14, minute=0)
scheduler.add_job(main, 'cron', hour=20, minute=0)
scheduler.start()

Custom Fonts

Replace arial.ttf in the script with the path to your desired font.
Error Handling

Ensure robust error handling for API requests and Instagram login failures.
License

This project is licensed under the MIT License. Feel free to use and modify it as needed.
Contribution

Feel free to open an issue or submit a pull request if you would like to contribute or suggest improvements.
Acknowledgments

    Unsplash: For the high-quality free images.
    Quotes API: For the motivational quotes.
    Instagrapi: For Instagram API integration.

