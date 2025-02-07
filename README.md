# Booru Buster

Booru Buster is a Python script that scrapes and downloads images from **Danbooru** based on a user's favorites. It ensures that only currently favorited images are kept, avoiding unnecessary downloads and automatically removing images that are no longer favorited.

## Features 🚀
- **Scrape all favorite images** from a given Danbooru username.
- **Download only original images** to ensure maximum quality.
- **Avoid duplicate downloads** by checking existing files.
- **Automatically clean up** images that are no longer favorited.
- **Handles pagination** to scrape all pages of favorites.

## Requirements 📦
Make sure you have the following dependencies installed before running the script:

```sh
pip install requests beautifulsoup4
```
## Usage ⚡

1. Clone the repository:
```sh
git clone https://github.com/your-repo/booru-buster.git
cd booru-buster
```
2. Run the script:
```sh
    python booru_buster.py
```
3. Enter the Danbooru username when prompted.
The script will:
- Scrape all pages of the user's favorite posts.
- Download only original images.
- Skip already downloaded images.
- Remove images that are no longer in the user's favorites.

## Folder Structure 📂
```
booru-buster/
│── booru_buster.py   # The main script
│── sync/             # Folder where downloaded images are stored
│── README.md         # Documentation
```
## Customization 🎨
You can change the sync folder name in the script (SYNC_FOLDER = "sync") if you want a different download directory.
If you experience rate limits, consider adding longer delays in time.sleep(1).

## License 📜

This project is licensed under the MIT License. Feel free to modify and distribute it!

Made with ❤️ by Sayuri
