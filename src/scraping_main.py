"""
PAWPRINTS-WEBSCRAPER

This project scrapes all petition data using the websocket all command from the RIT SG Pawprints Website.
It then formats and then preforms various queries, as well as graphing the data.

Author: Carter4242
https://github.com/Carter4242
"""


import scraping_write
import scraping_graphing
import scraping_load
import scraping_info


def main() -> None:
    """
    Loads all scraping data into petitions list, then sorts in by a variety of methods.
    Calls several info functions and graphs data.
    Finally writes the formatted list and total sigs all time to a two separate files.

    :rtype: None
    """
    
    petitions = scraping_load.scrapeAll()  # Load all data

    print("\nSorting...")
    petitions = scraping_info.sortPetitions(petitions, 'signatures')
    petitions = scraping_info.sortPetitions(petitions, 'response')
    petitions = scraping_info.sortPetitions(petitions, 'timestamp')
    print("Most frequent author:", scraping_info.mostFrequentAuthor(petitions))
    scraping_info.noResponseSixMonths(petitions)  # No response within six months > 200 sigs

    scraping_graphing.buildTimeGraph(petitions)  # Graph by time

    scraping_write.writeToFile(petitions)  # Write full list to file
    scraping_write.totalSigsWrite(petitions)  # If new day write totalSigs to file


if __name__ == '__main__':
    main()
