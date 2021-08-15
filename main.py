import requests
from bs4 import BeautifulSoup
import pandas as pd

x = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:89.0) Gecko/20100101 Firefox/89.0",
}

url = "https://www.openrice.com/en/hongkong/restaurants?landmarkId=1010"

response = requests.get(
    url,
    headers=x
)

soup = BeautifulSoup(response.text, "html.parser")

ul = soup.select_one("ul.sr1-listing-content-cells")

lis = ul.select("li.sr1-listing-content-cell")

restaurants = []
reviews = []

for li in lis:
    id = li.select(".content-cell-wrapper .content-wrapper .js-openrice-bookmark")[0]["data-poi-id"]
    title_name = li.select(".title-name")[0].text.strip()
    restaurant_url = "https://www.openrice.com" + li.select(".title-name > a")[0]["href"]
    restaurants.append([id, title_name, restaurant_url])

    page_num = 1
    review_count = 0
    while review_count < 11:
        response_review = requests.get(restaurant_url + f'/reviews?page={page_num}', headers=x)
        soup_review = BeautifulSoup(response_review.text, "html.parser")
        for i in range(15):
            while review_count < 11:
                review_title = soup_review.select(".sr2-review-list-container .review-title a")[i].text.strip()
                review_content = soup_review.select(".sr2-review-list-container section.review-container")[i]
                for review_content_a_tag in review_content.select("a"):
                    review_content_a_tag.decompose()
                review_content = review_content.text.replace("\n", "").replace("\r", "").strip()
                reviewer_id = soup_review.select(".sr2-review-list2-profile-section div.js-follow-btn")[i]["data-user-id"]
                if review_title == '':
                    break
                reviews.append([id, review_title, review_content, reviewer_id])
                review_count += 1
                print(review_count)
        page_num += 1
        print(page_num)

pd.DataFrame(data=restaurants, columns=["rest_id", "rest_name", "rest_url"]).to_csv("restaurants.csv")
pd.DataFrame(data=reviews, columns=["review_id", "review_title", "review_content", "reviewer_id"]).to_csv("reviews.csv")
