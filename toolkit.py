from typing import Callable
import requests
from bs4 import BeautifulSoup
import json
import html
import pandas as pd

class InvalidUrlExeption(Exception):
    def __init__(self) -> None:
        super().__init__('유효하지 않은 URL 입니다.')

def get_reviews_url(url: str):
    result: Callable[[int], str]
    if "shopping.naver.com/market/necessity/" in url:
        bs = BeautifulSoup(requests.get(url).text, "html5lib")
        script_nodes = bs.select("script")
        preloaded_state = list(filter(lambda node: node.text.startswith("window.__PRELOADED_STATE__="), script_nodes))[0]
        preloaded_state = json.loads(preloaded_state.text[(len("window.__PRELOADED_STATE__=")):])
        merchantNo = preloaded_state['product']['A']['channel']['naverPaySellerNo']
        originProductNo = preloaded_state['photoVideoReviewIds']['A']['originProductNo']
        result = lambda page: f"https://shopping.naver.com/v1/reviews/paged-reviews?page={page}&pageSize=30&merchantNo={merchantNo}&originProductNo={originProductNo}&sortType=REVIEW_RANKING"
        return result
    if "search.shopping.naver.com/catalog/" in url:
        nv_mid = url.split("?")[0].split("/")[-1]
        result = lambda page: f"https://search.shopping.naver.com/api/review?nvMid={nv_mid}&reviewType=ALL&page={page}"
        return result
    raise InvalidUrlExeption()

def get_reviews(review_url: str):
    dataset: pd.DataFrame
    if review_url.startswith("https://shopping.naver.com/v1/reviews/paged-reviews?"):
        dataset = pd.DataFrame(json.loads(requests.get(review_url).text)['contents'])[["reviewScore", "reviewContent"]]
        dataset.reviewContent = dataset.reviewContent.apply(html.unescape)
        dataset = dataset.rename(columns={'reviewScore':'ratings', 'reviewContent': 'reviews'})
        return dataset
    if review_url.startswith("https://search.shopping.naver.com/api/review?nvMid="):
        dataset = pd.DataFrame(json.loads(requests.get(review_url).text)['reviews'])[["starScore", "content"]]
        dataset = dataset.rename(columns={'starScore':'ratings', 'content': 'reviews'})
        return dataset
    raise InvalidUrlExeption()
