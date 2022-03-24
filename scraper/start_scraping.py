from game_specific_scrapers import (
    Dota2Scraper,
    HeroesOfNewerthScraper,
    HeroesOfTheStormScraper,
    LeagueOfLegendsScraper,
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
        # (
        #     LeagueOfLegendsScraper('https://www.leagueoflegends.com/en-us/champions/'),
        #     '../data/lol'
        # ),
        # (
        #     SmiteScraper('https://www.smitegame.com/gods/'),
        #     '../data/smite'
        # ),
        (
            HeroesOfNewerthScraper('https://www.heroesofnewerth.com', scrape_directly=True),
            '../data/hon'
        )
    ]

    for scraper, dest_folder in scrapers:
        print(f'{scraper}:')
        print('----------------------------------------------------------')
        scraper.scrape(dest_folder)
        print()


if __name__ == '__main__':
    main()
