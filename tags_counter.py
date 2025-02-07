import os
import requests
from bs4 import BeautifulSoup
import time
from collections import Counter

def get_image_links(username):
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

def get_tags(post_url):
    response = requests.get(post_url)
    if response.status_code != 200:
        print(f"Failed to fetch post page: {post_url}")
        return []

    soup = BeautifulSoup(response.text, "html.parser")
    tag_list = soup.find("ul", class_="general-tag-list")

    if not tag_list:
        print(f"No tags found for: {post_url}")
        return []

    tags = [li["data-tag-name"] for li in tag_list.find_all("li", {"data-tag-name": True})]
    return tags

def main(username):
    print(f"Fetching tags for user: {username}")

    post_links = get_image_links(username)
    if not post_links:
        print("No images found.")
        return

    total_posts = len(post_links)
    tag_counter = Counter()

    for i, post_link in enumerate(post_links, start=1):
        tags = get_tags(post_link)
        tag_counter.update(tags)
        print(f"[ Image : {i} / {total_posts} ] Processed {len(tags)} tags.")

    print("\nMost common tags:")
    for tag, count in tag_counter.most_common(40):
        print(f"{tag}: {count}")

    print("[DONE]")

if __name__ == "__main__":
    username = input("Enter Danbooru username: ")
    main(username)
