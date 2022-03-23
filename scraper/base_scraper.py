from abc import ABC, abstractmethod
from collections import deque
from typing import Union, Any
import datetime
import os
import re
import requests

from bs4 import BeautifulSoup
from utils.image_process import (
    get_img_ext,
    save_image_from_url,
)


class BaseScraper(ABC):
    """
    Abstract scraper that will serve as a base for game-specific web scraper.
    Each game-specific web scraper will be responsible to download images from a specific url/game.
    """

    def __init__(self, url: str, scrape_directly: bool, overwrite: bool, log_progress: bool):
        self._url = url
        self._scrape_directly = scrape_directly
        self._overwrite = overwrite
        self._log_progress = log_progress
        self._endpoints = self.get_endpoints()

    @property
    def url(self):
        return self._url

    @property
    def scrape_directly(self):
        return self._scrape_directly

    @url.setter
    def url(self, value):
        self._url = value

    @property
    def log_progress(self):
        return self._log_progress

    @property
    def overwrite(self):
        return self.overwrite

    @property
    def endpoints(self):
        return self._endpoints

    def __str__(self):
        pass

    def scrape_images(self, dest_folder: Union[os.PathLike, str], recursive=True):
        """
        Scrape all images from url and endpoints provided in the scraper constructor.

        :param dest_folder: Where to save images.
        :param recursive: Whether to scrape recursively.
        :return: None
        """
        endpoints_full = list(
            map(
                lambda ep: self._url + ep if self._url.endswith('/') else self._url + '/' + ep,
                self._endpoints
            )
        )

        if not os.path.exists(dest_folder):
            os.mkdir(dest_folder)

        visited_urls = set([])
        visited_endpoints = set([])
        url_queue = deque([self._url] + endpoints_full)
        n_downloaded = 0

        while len(url_queue) > 0:
            curr_url = url_queue.popleft()
            if curr_url not in visited_urls:
                visited_urls.add(curr_url)

                if self.log_progress:
                    print(f'Scraping "{curr_url}"...')

                res = requests.get(curr_url)
                if res.status_code != 200:
                    continue

                soup = BeautifulSoup(res.text, 'html.parser')

                img_tags = soup.find_all('img')
                for img_tag in img_tags:
                    src = img_tag.attrs.get('src', img_tag.attrs.get('data-src', None))
                    if src is None:
                        continue

                    if not self.img_url_fulfills_conditions(src):
                        continue

                    img_url = self.preprocess_img_url(src)
                    save_image_from_url(img_url, dest_folder, overwrite=self._overwrite)

                curr_url_hrefs_visited = set([])
                aas = soup.find_all('a')

                for a in aas:
                    endpoint = a.attrs.get('href', None)
                    if endpoint is None:
                        continue

                    if not self.endpoint_fulfills_conditions(endpoint):
                        continue

                    # endpoint not in curr_url_hrefs_visited
                    if recursive and endpoint.startswith('/') and endpoint not in visited_endpoints:
                        endpoint_prep = self.preprocess_endpoint(endpoint)
                        visited_endpoints.add(endpoint_prep)

                        next_url = curr_url + endpoint_prep if not curr_url.endswith('/') \
                            else curr_url + endpoint_prep[1:]
                        url_queue.append(next_url)

        if self.log_progress:
            print('\nDone.')

    def scrape_images_directly(self, dest_folder: Union[os.PathLike, str]):
        """
        Using endpoints when constructing scraper, download images directly from those endpoints
        instead of scraping web and searching for images.

        :param dest_folder: Where to save images.
        :return: None
        """

        if not os.path.exists(dest_folder):
            os.mkdir(dest_folder)

        for endpoint in self._endpoints:
            endpoint_processed = self.preprocess_endpoint(endpoint)
            img_ext = get_img_ext(endpoint_processed) if endpoint_processed is not None else None
            if img_ext is not None:
                if self._log_progress:
                    print(f'Downloading image from {endpoint_processed}...')

                save_image_from_url(endpoint_processed, dest_folder, overwrite=self._overwrite)

        if self.log_progress:
            print('\nDone.')

    def scrape(self, dest_folder: Union[os.PathLike, str], recursive=True):
        if self._scrape_directly:
            self.scrape_images_directly(dest_folder)
        else:
            self.scrape_images(dest_folder, recursive=recursive)

    @abstractmethod
    def get_endpoints(self) -> list:
        """
        Additional endpoints to scrape, beside base url.

        :return: List of endpoints to scrape.
        """
        pass

    @abstractmethod
    def img_url_fulfills_conditions(self, img_url: str) -> bool:
        """
        Defines conditions based upon which image will be downloaded from an url, and skipped otherwise.

        :param img_url: Image url.
        :return: True if image url fulfills conditions.
        """
        pass

    @abstractmethod
    def preprocess_img_url(self, img_url: str) -> str:
        """
        Modifies img_url before downloading the image.

        :param img_url:
        :return:
        """
        pass

    @abstractmethod
    def endpoint_fulfills_conditions(self, url: str) -> bool:
        """
        Defines conditions based upon which endpoint will be scraped.

        :param url: URL (can be literally anything when scraping)
        :return: True if endpoint fulfills conditions.
        """
        pass

    @abstractmethod
    def preprocess_endpoint(self, endpoint: str) -> str:
        """
        Modifies endpoint before scraping it.

        :param endpoint: Specific endpoint that scraper will analyze when scraping a website.
        :return: Modified endpoint.
        """
        pass


