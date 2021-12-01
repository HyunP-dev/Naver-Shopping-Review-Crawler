from typing import Callable
import requests
from bs4 import BeautifulSoup
import json
import html
import pandas as pd

def get_reviews_url(url: str):
    bs = BeautifulSoup(requests.get(url).text, "html5lib")
    script_nodes = bs.select("script")
    preloaded_state = list(filter(lambda node: node.text.startswith("window.__PRELOADED_STATE__="), script_nodes))[0]
    preloaded_state = json.loads(preloaded_state.text[(len("window.__PRELOADED_STATE__=")):])
    merchantNo = preloaded_state['product']['A']['channel']['naverPaySellerNo']
    originProductNo = preloaded_state['photoVideoReviewIds']['A']['originProductNo']
    result: Callable[[int], str] = lambda page: f"https://shopping.naver.com/v1/reviews/paged-reviews?page={page}&pageSize=30&merchantNo={merchantNo}&originProductNo={originProductNo}&sortType=REVIEW_RANKING"
    return result

def get_reviews(review_url: str) -> pd.DataFrame:
    dataset = pd.DataFrame(json.loads(requests.get(review_url).text)['contents'])[["reviewScore", "reviewContent"]]
    dataset.reviewContent = dataset.reviewContent.apply(html.unescape)
    dataset = dataset.rename(columns={'reviewScore':'ratings', 'reviewContent': 'reviews'})
    return dataset
