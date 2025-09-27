import sqlite3
import requests
# import beautifulsoup4
import pandas
import sqlite_utils
from bs4 import BeautifulSoup


url = "https://books.toscrape.com/catalogue/page-1.html"
response = requests.get(url)
html = response.text
soup = BeautifulSoup(html, "html.parser")

books = []
for book in soup.select("article.product_pod"):
    title = book.h3.a["title"]
    price = book.select_one("p.price_color").text
    availability = book.select_one("p.instock.availability").text.strip()
    books.append({"title": title, "price": price, "availability": availability})

print(books)


conn=sqlite3.connect("books.db")
cursor=conn.cursor()
# cursor.execute("""
# CREATE TABLE IF NOT EXISTS books
# (
# id INTEGER PRIMARY KEY AUTOINCREMENT,
# title TEXT,
#  price TEXT,
#   availability TEXT)
# """
# )
# print("done")

for book in books:
    cursor.execute("""
    INSERT INTO books (title, price, availability)
    VALUES (?, ?, ?)
    """, (book["title"], book["price"], book["availability"]))

conn.commit()
conn.close()
print("done")