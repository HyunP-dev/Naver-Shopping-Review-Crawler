# Naver Shopping Review Crawler
네이버 쇼핑에서 상품평을 가져오는 웹 스크래퍼

## Functions

### `(function) get_reviews_url: (url: str) -> (page: int) -> str`

get_reviews 의 매개변수인 review_url를 내보내는 함수를 반환합니다.


### `(function) get_reviews: (review_url: str) -> DataFrame`

get_reviews_url로부터 얻은 url를 통해 DataFrame을 만들어 반환합니다.

## Example

```py
from toolkit import *
from tqdm import tqdm

url = "https://shopping.naver.com/market/necessity/products/2038109297"
reviews_url_generator = get_reviews_url(url)
dataset = get_reviews(reviews_url_generator(1))
for page in tqdm(range(2, 1000)):
    dataset = pd.concat([dataset, get_reviews(reviews_url_generator(page))], ignore_index=True)
dataset.to_csv(url.split("/")[-1]+".csv", encoding="utf-8-sig", index=False)
```
