"""
PAWPRINTS-WEBSCRAPER

This project scrapes all petition data using the websocket all command from the RIT SG Pawprints Website.
It then formats and then preforms various queries, as well as graphing the data.

Author: Carter4242
https://github.com/Carter4242
"""


import write
import graphing
import load
import info
import sys
from sys import platform


def main() -> None:
    """
    Loads all scraping data into petitions list, then sorts in by a variety of methods.
    Calls several info functions and graphs data.
    Finally writes the formatted list and total sigs all time to a two separate files.

    :rtype: None
    """

    exitCode = 0
    print("Platform is: " + platform)
    if platform == "darwin":
        exitCode = 42
    

    petitions = load.scrapeAll()  # Load all data

    print("\nSorting...")
    petitions = info.sortPetitions(petitions, 'signatures')
    petitions = info.sortPetitions(petitions, 'response')
    petitions = info.sortPetitions(petitions, 'timestamp')
    # print("Most frequent author:", scraping_info.mostFrequentAuthor(petitions))
    # scraping_info.noResponseSixMonths(petitions)  # No response within six months > 200 sigs

    graphing.buildBarGraphs(petitions)  # Bar Graphs

    write.writeToFile(petitions)  # Write full list to file
    if exitCode != 42:
        write.totalSigsWrite(petitions)  # If new day write totalSigs to file
    else:
        print("")
        for i in range(8):
            print("ERROR: WILL NOT WRITE - RUNNING ON LOCAL")
        print("")

    graphing.buildLineGraphs()  # Graph by line

    sys.exit(exitCode)




if __name__ == '__main__':
    main()
