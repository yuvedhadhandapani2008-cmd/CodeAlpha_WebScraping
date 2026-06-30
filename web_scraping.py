import requests
from bs4 import BeautifulSoup
import pandas as pd
import matplotlib.pyplot as plt

url = "http://books.toscrape.com/"

response = requests.get(url)

if response.status_code == 200:
    print("Website downloaded successfully!\n")
else:
    print("Failed to access website.")
    exit()

soup = BeautifulSoup(response.text, "html.parser")

books = soup.find_all("article", class_="product_pod")

print("Total Books Found:", len(books))
print("-" * 60)

book_data = []

for book in books:

    title = book.find("h3").find("a")["title"]

    price = book.find("p", class_="price_color").text

    rating = book.find("p", class_="star-rating")["class"][1]

    availability = book.find(
        "p",
        class_="instock availability"
    ).text.strip()

    print("Title        :", title)
    print("Price        :", price)
    print("Rating       :", rating)
    print("Availability :", availability)
    print("-" * 60)

    book_data.append([
        title,
        price,
        rating,
        availability
    ])

df = pd.DataFrame(
    book_data,
    columns=[
        "Title",
        "Price",
        "Rating",
        "Availability"
    ]
)

print("\n========= DATA CLEANING =========\n")

df["Price"] = df["Price"].str.replace(r"[^\d.]", "", regex=True)

df["Price"] = df["Price"].astype(float)

print("\nData Types:\n")
print(df.dtypes)


print("\n========== DATA ANALYSIS ==========\n")

print("Total Number of Books :", len(df))

print("Average Price :", round(df["Price"].mean(), 2))

print("Highest Price :", df["Price"].max())

print("Lowest Price :", df["Price"].min())

print("\nMost Expensive Book\n")
print(df[df["Price"] == df["Price"].max()])

print("\nCheapest Book\n")
print(df[df["Price"] == df["Price"].min()])

print("\nBooks by Rating\n")
print(df["Rating"].value_counts())

print("\nAvailability Status\n")
print(df["Availability"].value_counts())

print("\nStatistical Summary\n")
print(df.describe())

df.to_csv("books.csv", index=False)

print("\nDataset saved successfully as books.csv")

# -----------------------------
# VISUALIZATION 1
# Rating Distribution
# -----------------------------

rating_counts = df["Rating"].value_counts()

plt.figure(figsize=(7,5))

rating_counts.plot(kind="bar")

plt.title("Book Rating Distribution")

plt.xlabel("Rating")

plt.ylabel("Number of Books")

plt.tight_layout()

plt.savefig("rating_distribution.png")

plt.show()

# -----------------------------
# VISUALIZATION 2
# Price Distribution
# -----------------------------

plt.figure(figsize=(7,5))

plt.hist(df["Price"], bins=8)

plt.title("Price Distribution")

plt.xlabel("Price (£)")

plt.ylabel("Frequency")

plt.tight_layout()

plt.savefig("price_distribution.png", dpi=300)

plt.show()

# -----------------------------
# VISUALIZATION 3
# Top 10 Most Expensive Books
# -----------------------------

top_books = df.sort_values(by="Price", ascending=False).head(10)

top_books["Short Title"] = top_books["Title"].str[:20] + "..."

plt.figure(figsize=(14, 7))

plt.bar(top_books["Short Title"], top_books["Price"])

plt.title("Top 10 Most Expensive Books")
plt.xlabel("Book Title")
plt.ylabel("Price (£)")

plt.xticks(rotation=45, ha="right", fontsize=9)

plt.tight_layout()

plt.savefig("top10_expensive_books.png", dpi=300)

plt.show()