# Amazon Product Scraper and Analyzer

A Python-based tool to **scrape, analyze, and visualize Amazon product data**.

**Author:** H2 Karthick S
**Team:** Team 1 (Team Lead)
**Internship:** Cybernaut

---

## Overview

The **Amazon Product Scraper and Analyzer** allows users to:

* Scrape Amazon India product listings across multiple pages.
* Extract product details including:

  * Title
  * Price
  * Image URL
  * Rating
  * Product link
  * Description
  * Scrape timestamp
* Filter products by **maximum price** and **minimum rating**.
* Save data in **CSV, Excel, and JSON** formats.
* Generate visualizations like **rating distributions** and **word clouds** of product descriptions.

The tool uses **Python**, **BeautifulSoup**, **ZenRows API**, and **multi-threading** for efficient scraping.

---

## Features

* Multi-page scraping
* Concurrent product page fetching
* Data cleaning and formatting
* Optional price and rating filters
* CSV, Excel, JSON export
* Rating histogram and word cloud generation

---

## Requirements

* Python 3.10+
* Libraries:

  ```bash
  pip install requests beautifulsoup4 pandas matplotlib wordcloud python-dotenv
  ```
* ZenRows API key stored in `.env` file:

  ```
  apikey=YOUR_ZENROWS_API_KEY
  ```

---

## Usage

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/amazon-product-scraper.git
   cd amazon-product-scraper
   ```

2. Install dependencies.

3. Create a `.env` file and add your ZenRows API key.

4. Run the script:

   ```bash
   python amazon_scraper.py
   ```

5. Enter:

   * Product name
   * Maximum pages to scrape
   * Optional price and rating filters

6. Outputs will be saved in the project folder and `visuals/` for charts.

---

## Sample Output

| Title                                                                                  | Price   | Image Url                                                              | Rating             | Product Link                                | Description                         | ScrapedAt                   | Price\_Numeric              | Rating\_Numeric |   |
| -------------------------------------------------------------------------------------- | ------- | ---------------------------------------------------------------------- | ------------------ | ------------------------------------------- | ----------------------------------- | --------------------------- | --------------------------- | --------------- | - |
| Lenovo Smartchoice Ideapad Slim 3 13Th Gen Intel Core I7-13620H 15.3 Inch(...)         | ₹57,990 | ![Img](https://m.media-amazon.com/images/I/71IjxF4prWL._AC_UY218_.jpg) | 4.0 out of 5 stars | [Link](https://www.amazon.in/dp/B0F2162VGQ) | Processor: Intel Core i7-13620H ... | 2025-09-22T09:51:26.770674Z | 57990                       | 4               |   |
| Dell Inspiron 3535, AMD Ryzen 5-7530U, 16GB RAM, 512GB SSD, FHD WVA IPS 15.6"/39(...)  | ₹40,990 | ![Img](https://m.media-amazon.com/images/I/61diqHMquqL._AC_UY218_.jpg) | 4.0 out of 5 stars | [Link](https://www.amazon.in/dp/B0DSFRQTGB) | R5-7530U                            | 16GB DDR4 ...               | 2025-09-22T09:51:24.814608Z | 40990           | 4 |
| HP Pavilion x360, 13th Gen Intel Core i5-1335U (16GB DDR4, 512GB SSD) Touchscreen(...) | ₹64,990 | ![Img](https://m.media-amazon.com/images/I/618zAXbM4uL._AC_UY218_.jpg) | 3.7 out of 5 stars | [Link](https://www.amazon.in/dp/B0CJ2KWNNQ) | Processor - Intel Core i5-1335U ... | 2025-09-22T09:51:23.153871Z | 64990                       | 3.7             |   |


---

## Visualizations

1. **Rating Distribution**: `visuals/<product>_rating_distribution.png`
2. **Word Cloud**: `visuals/<product>_wordcloud.png`

---

## Future Enhancements

* GUI interface using **Tkinter**, **PyQt**, or **Flask**
* Real-time dashboard with **Plotly Dash** or **Power BI**
* Scraping across multiple marketplaces (Flipkart, Snapdeal)
* Automated alerts for price drops or product ratings
* Database storage (SQL/NoSQL) for large-scale historical analysis
* Predictive analytics using machine learning

---

Do you want me to do that?
