import requests
from bs4 import BeautifulSoup
import sqlite3
import re

headers = {
"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 \ (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
}


links = [
    "https://www.morele.net/karta-graficzna-gigabyte-radeon-rx-7600-xt-gaming-oc-16gb-gddr6-gv-r76xtgaming-oc-16gd-13168875/",
    "https://www.morele.net/karta-graficzna-gigabyte-geforce-rtx-5060-windforce-oc-8gb-gddr7-dlss4-gv-n5060wf2oc-8gd-15234816/",
    "https://www.morele.net/karta-graficzna-pny-geforce-rtx-4060-ti-verto-dual-fan-8gb-gddr6-vcg4060t8dfxpb1-12923011/",
    "https://www.morele.net/karta-graficzna-palit-geforce-rtx-5060-dual-8gb-gddr7-dlss4-ne75060019p1-gb2063d-15068906/"
]

def init_db():
        conn = sqlite3.connect("links.db")
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS links (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                url TEXT UNIQUE NOT NULL
            )
        """)
        conn.commit()
        conn.close()

init_db()

def save_links_to_db(url):
    if not is_valid_url(url):
        raise ValueError("Invalid URL format")
    conn = sqlite3.connect("links.db")
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO links (url) VALUES (?)", (url,))
        conn.commit()
    finally:
        conn.close()

def get_product_info(url):
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    
    # name
    title_element = soup.find("h1", class_="prod-name")
    title = title_element.get_text(strip=True) if title_element else "Unknown title"
    
    # price
    
    price_element = soup.find("div", class_="product-price")
    price = price_element.get_text(strip=True) if price_element else "Unknown price"
    
    return {"title": title, "price": price}
    
    
    

def refresh_all(tree):
    conn = sqlite3.connect("links.db")
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT url FROM links")
        rows = cursor.fetchall()
    finally:
        conn.close()
    
    print(rows)
    tree.delete(*tree.get_children())
    for row in rows:
        info = get_product_info(row[0])
        tree.insert("", "end", iid=row[0], values=(info["title"], info["price"]))
    
def delete_from_db(url_to_delete):
    conn = sqlite3.connect("links.db")
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM links WHERE url = ?", (url_to_delete,))
        conn.commit()
    finally:
        conn.close()
        

def is_valid_url(url):
    pattern = re.compile(
        r'^https?://'  # http:// lub https:// na początku
        r'([a-z0-9\-]+\.)+[a-z]{2,6}'  # domena
        r'(/[a-z0-9\-._~:/?#\[\]@!$&\'()*+,;=]*)?$',  # ścieżka i parametry (opcjonalne)
        re.IGNORECASE
    )
    return bool(pattern.match(url))
    