from scrapers import (
    Dota2Scraper,
    HeroesOfTheStormScraper,
    LolScraper,
    SmiteScraper,
)


def main():
    scrapers = [
        # (
        #     Dota2Scraper('https://www.dota2.com/', scrape_directly=True),
        #     '../data/dota2'
        # ),
        # (
        #     HeroesOfTheStormScraper('https://heroesofthestorm.com/', '../misc/hots_heroes.txt'),
        #     '../data/hots'
        # ),
        (
            LolScraper('https://www.leagueoflegends.com/en-us/champions/'),
            '../data/lol'
        ),
        # (
        #     SmiteScraper('https://www.smitegame.com/gods/'),
        #     '../data/smite'
        # )
    ]

    for scraper, dest_folder in scrapers:
        print(f'{scraper}:')
        print('----------------------------------------------------------')
        scraper.scrape(dest_folder)
        print()


if __name__ == '__main__':
    main()
