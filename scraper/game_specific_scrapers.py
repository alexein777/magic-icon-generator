from typing import Union
import json
import os
import re
import requests

from bs4 import BeautifulSoup

from scraper.base_scraper import BaseScraper
from utils.image_process import get_img_ext


class Dota2Scraper(BaseScraper):
    def __init__(self, url: Union[os.PathLike, str], scrape_directly: bool, log_progress=True):
        super().__init__(url, scrape_directly, log_progress)

    def __str__(self):
        return 'Dota 2 scraper'

    def get_endpoints(self) -> list:
        endpoints = []
        hero_urls = [self._url + f'/datafeed/herodata?language=english&hero_id={hero_id}'
                     for hero_id in range(1, 138)]

        for hero_url in hero_urls:
            cdn_base_url = 'https://cdn.cloudflare.steamstatic.com/apps/dota2/images/dota_react/abilities/'
            json_text = requests.get(hero_url).text
            json_data = json.loads(json_text)

            try:
                heroes = json_data['result']['data']['heroes']
                for hero in heroes:
                    ability_names = [ability['name'] for ability in hero['abilities']]
                    for ability_name in ability_names:
                        ability_endpoint = cdn_base_url + ability_name + '.png'
                        if self.img_url_fulfills_conditions(ability_endpoint):
                            ability_endpoint = self.preprocess_img_url(ability_endpoint)
                            endpoints.append(ability_endpoint)
            except KeyError:
                print(f'Skipping {hero_url} due to missing json fields required for scraping abilities...')

        return endpoints

    def img_url_fulfills_conditions(self, img_url: str) -> bool:
        return get_img_ext(img_url) is not None

    def preprocess_img_url(self, img_url: str) -> str:
        return img_url

    def endpoint_fulfills_conditions(self, url: str) -> bool:
        return True

    def preprocess_endpoint(self, endpoint: str) -> str:
        return endpoint


class HeroesOfTheStormScraper(BaseScraper):
    def __init__(
        self,
        url: Union[os.PathLike, str],
        heroes_file: Union[os.PathLike, str],
        scrape_directly=False,
        log_progress=True
    ):
        self._heroes_file = heroes_file
        super().__init__(url, scrape_directly=scrape_directly, log_progress=log_progress)

    def __str__(self):
        return 'Heroes of the Storm scraper'

    def get_endpoints(self):
        endpoints = []
        with open(self._heroes_file, 'r') as f:
            lines = f.readlines()
            for line in lines:
                line_clean = line.strip()
                if line_clean != '':
                    endpoint = '/en-us/heroes/' + line_clean + '/'
                    endpoints.append(endpoint)

        return endpoints

    def img_url_fulfills_conditions(self, img_url):
        return 'abilities' in img_url

    def preprocess_img_url(self, img_url):
        return img_url.replace('hexagon', 'square')

    def endpoint_fulfills_conditions(self, url):
        return url

    def preprocess_endpoint(self, endpoint):
        return endpoint


class LeagueOfLegendsScraper(BaseScraper):
    def __init__(
        self,
        url: Union[os.PathLike, str],
        scrape_directly=False,
        log_progress=True
    ):
        super().__init__(url, scrape_directly=scrape_directly, log_progress=log_progress)

    def __str__(self):
        return 'League of Legends scraper'

    def get_endpoints(self) -> list:
        return []

    def img_url_fulfills_conditions(self, img_url):
        # Spell names DONT have 'ability' in their name (illustrations of how abilities work have, hence the filter)
        no_ability = 'ability' not in img_url
        no_assets = 'assets' not in img_url
        no_hero_imgs = '/champion/splash' not in img_url

        return no_ability and no_assets and no_hero_imgs

    def preprocess_img_url(self, img_url):
        return img_url

    def endpoint_fulfills_conditions(self, url):
        return 'champions' in url

    def preprocess_endpoint(self, endpoint):
        return endpoint.replace('/en-us/champions', '')


class SmiteScraper(BaseScraper):
    def __init__(
        self,
        url: Union[os.PathLike, str],
        scrape_directly=False,
        log_progress=True
    ):
        super().__init__(url, scrape_directly=scrape_directly, log_progress=log_progress)

    def __str__(self):
        return 'Smite scraper'

    def get_endpoints(self) -> list:
        gods_src_url = 'https://cms.smitegame.com/wp-json/smite-api/all-gods/1'
        res = requests.get(gods_src_url)
        if res.status_code != 200:
            raise ValueError(f'Invalid response from "{gods_src_url}" (status code != 200)')

        soup = BeautifulSoup(res.text, 'html.parser')

        gods = re.findall(r'"name":"([-_\'a-zA-Z]+)"', soup.text)
        endpoints = [god.replace('"name":', '').replace('"', '') for god in gods]

        return endpoints

    def img_url_fulfills_conditions(self, img_url):
        return 'god-abilities' in img_url

    def preprocess_img_url(self, img_url):
        return img_url

    def endpoint_fulfills_conditions(self, url):
        return 'gods' in url

    def preprocess_endpoint(self, endpoint):
        return endpoint


class HeroesOfNewerthScraper(BaseScraper):
    def __init__(
        self,
        url: Union[os.PathLike, str],
        scrape_directly=False,
        log_progress=True
    ):
        super().__init__(url, scrape_directly=scrape_directly, log_progress=log_progress)

    def __str__(self):
        return 'Heroes of Newerth scraper'

    def get_endpoints(self) -> list:
        endpoints = []
        # HoN hero ids are weird: some ids are missing between 20-50 but there are valid ids over 200
        hero_urls = [self._url + f'/images/heroes/{hero_id}' for hero_id in range(2, 300)]
        for hero_url in hero_urls:
            ability_endpoints = [hero_url + f'/ability{a_id}_128.jpg' for a_id in range(1, 8)]
            for ability_endpoint in ability_endpoints:
                ability_endpoint = self.preprocess_endpoint(ability_endpoint)
                if self.img_url_fulfills_conditions(ability_endpoint):
                    ability_endpoint = self.preprocess_img_url(ability_endpoint)
                    endpoints.append(ability_endpoint)

        return endpoints

    def img_url_fulfills_conditions(self, img_url):
        return get_img_ext(img_url) is not None

    def preprocess_img_url(self, img_url):
        return img_url

    def endpoint_fulfills_conditions(self, url):
        return True

    def preprocess_endpoint(self, endpoint):
        return endpoint
