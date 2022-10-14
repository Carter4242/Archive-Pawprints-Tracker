"""
PAWPRINTS-WEBSCRAPER

This project scrapes all petition data using the websocket all command from the RIT SG Pawprints Website.
It then formats and then preforms various queries, as well as graphing the data.

Author: Carter4242
https://github.com/Carter4242
"""


import format
import graphing
import info
import load
import write
import sys
import os
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
    latestPetitions = format.latestPetitions(petitions)

    # print("Most frequent author:", scraping_info.mostFrequentAuthor(petitions))
    # scraping_info.noResponseSixMonths(petitions)  # No response within six months > 200 sigs

    graphing.buildBarGraphs(petitions)  # Bar Graphs

    write.writeToFile(petitions)  # Write full list to file
    write.petitionsWrite(latestPetitions)

    if exitCode != 42:
        #write.petitionsWrite(latestPetitions)  # If new day write every petition to there file
        write.totalSigsWrite(petitions)  # If new day write totalSigs to file
    else:
        print("")
        for i in range(8):
            print("ERROR: WILL NOT WRITE - RUNNING ON LOCAL")
        print("\n")

    #graphing.buildPetitionsGraphs
    graphing.buildLineGraphs()  # Graph by line

    sys.exit(exitCode)




if __name__ == '__main__':
    main()
