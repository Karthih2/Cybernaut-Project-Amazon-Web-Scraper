import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import pandas as pd
import os
from concurrent.futures import ThreadPoolExecutor
import time
import re
from datetime import datetime
import matplotlib.pyplot as plt
from wordcloud import WordCloud

# Setup
load_dotenv()
api_key = os.getenv("apikey")
if not api_key:
    raise SystemExit("Missing API key in .env (apikey=...)")

#User Inputs
search_item = input("Enter product to search on Amazon: ").strip()
if not search_item:
    raise SystemExit("Please enter a product.")

search_item_for_url = search_item.replace(" ", "+")
base_url = f"https://www.amazon.in/s?k={search_item_for_url}"

max_pages = int(input("Max pages to scrape (default 5): ").strip() or "5")
max_workers = 5
price_limit_input = input("Filter max price (INR) or press Enter to skip: ").strip()
rating_min_input = input("Filter min rating (e.g. 4.0) or press Enter to skip: ").strip()

#Helpers
def get_page_soup(url, retries=2, delay=1.0):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36"
    }
    params = {'apikey': api_key, 'url': url, 'premium_proxy': 'true'}
    for attempt in range(retries + 1):
        try:
            resp = requests.get("https://api.zenrows.com/v1/", params=params, headers=headers, timeout=20)
            if resp.status_code != 200:
                raise Exception(f"Status code: {resp.status_code}")
            return BeautifulSoup(resp.text, "html.parser")
        except Exception as e:
            print(f"Attempt {attempt+1} failed: {e}")
            if attempt < retries:
                time.sleep(delay)
            else:
                raise

def clean_description_inline(description, max_len=300):
    if not description or description == "N/A":
        return "N/A"
    description = re.sub(r"[【】✅🌐\[\]•●▪◆★✦]", "|", description)
    description = re.sub(r"\|+", "|", description)
    description = re.sub(r"\s+", " ", description)
    description = description.strip(" |")
    if len(description) > max_len:
        description = description[:max_len].rstrip() + "..."
    return description

def get_product_details(product):
    try:
        title_tag = product.h2
        title = title_tag.get_text(strip=True) if title_tag else "N/A"
        title = " ".join(title.split())
        title = title[:80] + "..." if len(title) > 80 else title

        price_tag = product.find("span", class_="a-offscreen")
        price = price_tag.get_text(strip=True) if price_tag else "N/A"

        img_tag = product.find("img", class_="s-image")
        img_url = img_tag['src'] if img_tag and img_tag.has_attr('src') else "N/A"

        rating_tag = product.find("span", class_="a-icon-alt")
        rating = rating_tag.get_text(strip=True) if rating_tag else "N/A"

        asin = product.get("data-asin")
        product_link = f"https://www.amazon.in/dp/{asin}" if asin else "N/A"

        description = "N/A"
        if product_link != "N/A":
            prod_soup = get_page_soup(product_link)
            desc_tag = prod_soup.find("div", {"id": "productDescription"})
            if desc_tag:
                description = desc_tag.get_text(separator=" ").strip()
            else:
                bullet_tags = prod_soup.select("#feature-bullets li span")
                bullets = [b.get_text(separator=" ").strip() for b in bullet_tags if b.get_text(strip=True)]
                if bullets:
                    description = " | ".join(bullets)
            description = clean_description_inline(description, max_len=300)
            time.sleep(0.25)

        scraped_at = datetime.utcnow().isoformat() + "Z"

        return {
            "Title": title,
            "Price": price,
            "Image Url": img_url,
            "Rating": rating,
            "Product Link": product_link,
            "Description": description,
            "ScrapedAt": scraped_at
        }
    except Exception as e:
        print("Error in get_product_details:", e)
        return {
            "Title": "N/A",
            "Price": "N/A",
            "Image Url": "N/A",
            "Rating": "N/A",
            "Product Link": "N/A",
            "Description": "N/A",
            "ScrapedAt": datetime.utcnow().isoformat() + "Z"
        }

#Pagination
all_products = []
page_number = 1
print("Starting search:", search_item)

while page_number <= max_pages:
    page_url = f"{base_url}&page={page_number}"
    print(f"Fetching page {page_number}...")
    soup = get_page_soup(page_url)
    products = soup.find_all("div", {"data-component-type": "s-search-result"})
    if not products:
        print(f"No products found on page {page_number}.")
        break
    all_products.extend(products)
    page_number += 1
    time.sleep(0.5)

if not all_products:
    print("No products scraped. Exiting.")
    exit()

print(f"Total search-result items collected: {len(all_products)}")

#Multi-thread fetch product pages
with ThreadPoolExecutor(max_workers=max_workers) as executor:
    product_dicts = list(executor.map(get_product_details, all_products))

#DataFrame
df = pd.DataFrame(product_dicts)

# Parse numeric price
df["Price_Numeric"] = df["Price"].astype(str).str.replace(r"[^\d]", "", regex=True)
df["Price_Numeric"] = pd.to_numeric(df["Price_Numeric"], errors="coerce")

# Parse numeric rating
df["Rating_Numeric"] = df["Rating"].astype(str).str.extract(r"([\d\.]+)").astype(float, errors='ignore')

#Apply filters
filtered_df = df.copy()
if price_limit_input:
    try:
        max_price_val = float(re.sub(r"[^\d\.]", "", price_limit_input))
        filtered_df = filtered_df[filtered_df["Price_Numeric"].notna() & (filtered_df["Price_Numeric"] <= max_price_val)]
    except:
        print("Invalid price limit input; skipping price filter.")

if rating_min_input:
    try:
        min_rating_val = float(rating_min_input)
        filtered_df = filtered_df[filtered_df["Rating_Numeric"].notna() & (filtered_df["Rating_Numeric"] >= min_rating_val)]
    except:
        print("Invalid rating input; skipping rating filter.")

#Save outputs
safe_name = re.sub(r"\s+", "_", search_item.strip())

all_excel = f"{safe_name}_products_all.xlsx"
all_csv = f"{safe_name}_products_all.csv"
json_file = f"{safe_name}_products_all.json"

df.to_excel(all_excel, index=False)
df.to_csv(all_csv, index=False)
df.to_json(json_file, orient="records", force_ascii=False, indent=2)

print(f"Saved ALL results to: {all_excel}, {all_csv}, {json_file}")

if len(filtered_df) != len(df):
    f_excel = f"{safe_name}_products_filtered.xlsx"
    f_csv = f"{safe_name}_products_filtered.csv"
    filtered_df.to_excel(f_excel, index=False)
    filtered_df.to_csv(f_csv, index=False)
    print(f"Saved FILTERED results to: {f_excel}, {f_csv} (rows: {len(filtered_df)})")
else:
    print("No filters applied or filters did not reduce results.")

#Visualization
os.makedirs("visuals", exist_ok=True)

# 1. Rating Distribution
df_rating = df["Rating_Numeric"].dropna()
if not df_rating.empty:
    plt.figure(figsize=(8, 5))
    df_rating.hist(bins=10)
    plt.title("Product Ratings Distribution")
    plt.xlabel("Rating")
    plt.ylabel("Count")
    rating_img = os.path.join("visuals", f"{safe_name}_rating_distribution.png")
    plt.savefig(rating_img)
    plt.close()

# 2. Word Cloud (Descriptions)
text = " ".join(str(desc) for desc in df["Description"].dropna())
text = re.sub(r"[^a-zA-Z\s]", " ", text)
if text.strip():
    wc = WordCloud(width=800, height=400, background_color="white").generate(text)
    plt.figure(figsize=(10, 6))
    plt.imshow(wc, interpolation="bilinear")
    plt.axis("off")
    plt.title("Most Common Keywords in Product Descriptions", fontsize=16)
    wordcloud_img = os.path.join("visuals", f"{safe_name}_wordcloud.png")
    plt.savefig(wordcloud_img)
    plt.close()

print("Visualizations saved in 'visuals/' folder.")
print("Done.")
