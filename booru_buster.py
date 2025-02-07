import os
import requests
from bs4 import BeautifulSoup
import time

SYNC_FOLDER = "sync"

def get_existing_images():
    """Récupère la liste des fichiers déjà présents dans le dossier sync."""
    if not os.path.exists(SYNC_FOLDER):
        os.makedirs(SYNC_FOLDER)
    return set(os.listdir(SYNC_FOLDER))

def get_image_links(username):
    """Récupère la liste des posts favoris de l'utilisateur."""
    base_url = f"https://danbooru.donmai.us/posts?page=1&tags=ordfav%3A{username}"
    image_links = []

    while base_url:
        print(f"Scraping page: {base_url}")
        response = requests.get(base_url)
        if response.status_code != 200:
            print(f"Failed to fetch {base_url}")
            break

        soup = BeautifulSoup(response.text, "html.parser")

        posts_container = soup.find("div", class_="posts-container")
        if not posts_container:
            print("No posts found.")
            break
        
        articles = posts_container.find_all("article")
        for article in articles:
            post_link = article.find("a", class_="post-preview-link")
            if post_link and 'href' in post_link.attrs:
                full_post_url = f"https://danbooru.donmai.us{post_link['href'].split('?')[0]}"
                image_links.append(full_post_url)

        paginator = soup.find("a", class_="paginator-next")
        base_url = f"https://danbooru.donmai.us{paginator['href']}" if paginator else None

        time.sleep(1)  

    return image_links

def get_original_image_url(post_url):
    """Récupère le lien de l'image originale à partir de la page du post."""
    response = requests.get(post_url)
    if response.status_code != 200:
        print(f"Failed to fetch post page: {post_url}")
        return None

    soup = BeautifulSoup(response.text, "html.parser")

    resize_notice = soup.find("div", class_="post-notice-resized")
    if resize_notice:
        original_link = resize_notice.find("a", class_="image-view-original-link")
        if original_link and 'href' in original_link.attrs:
            return original_link["href"]

    content_section = soup.find("section", id="content")
    if content_section:
        img_tag = content_section.find("img", class_="fit-width")
        if img_tag and 'src' in img_tag.attrs:
            return img_tag["src"]

    print(f"No original image found for: {post_url}")
    return None

def download_image(image_url):
    """Télécharge l'image si elle n'est pas déjà présente."""
    filename = image_url.split("/")[-1]
    file_path = os.path.join(SYNC_FOLDER, filename)

    if filename in get_existing_images():
        print(f"Skipping (already exists): {filename}")
        return filename

    response = requests.get(image_url, stream=True)
    if response.status_code == 200:
        with open(file_path, "wb") as file:
            for chunk in response.iter_content(1024):
                file.write(chunk)
        print(f"Downloaded: {filename}")
        return filename
    else:
        print(f"Failed to download: {image_url}")
        return None

def remove_unfavorited_images(saved_filenames, fetched_filenames):
    """Supprime les images qui ne sont plus dans les favoris."""
    files_to_delete = saved_filenames - fetched_filenames
    for filename in files_to_delete:
        file_path = os.path.join(SYNC_FOLDER, filename)
        try:
            os.remove(file_path)
            print(f"Removed: {filename} (no longer in favorites)")
        except Exception as e:
            print(f"Error deleting {filename}: {e}")

def main(username):
    print(f"Fetching images for user: {username}")

    saved_images = get_existing_images()
    fetched_images = set() 

    post_links = get_image_links(username)

    if not post_links:
        print("No images found.")
        return
    
    for post_link in post_links:
        image_url = get_original_image_url(post_link)
        if image_url:
            downloaded_filename = download_image(image_url)
            if downloaded_filename:
                fetched_images.add(downloaded_filename)

    remove_unfavorited_images(saved_images, fetched_images)

    print("[DONE]")

if __name__ == "__main__":
    username = input("Enter Danbooru username: ")
    main(username)

