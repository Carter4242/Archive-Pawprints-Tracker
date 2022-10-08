"""
PAWPRINTS-WEBSCRAPER

This module handles the writing to files of the full petitions list and the daily total signatures.

Author: Carter4242
https://github.com/Carter4242
"""


from datetime import datetime, date


def writeToFile(petitions: list) -> None:
    """
    Writes the full list of petitions into a newly created file, each petition on a new line.
    Filename is - YYYY-MM-DD HR:MM:SS:DECMAL

    :param petitions: Full list of petitions
    :type petitions: list
    :rtype: None
    """

    # YYYY-MM-DD HR:MM:SS:DECMAL
    filename = "Output/" + str(datetime.now()) + " - Length: " + str(len(petitions)) + ".txt"

    print("\nOpening "+filename)
    with open(filename, 'a') as f:  # Appending
        print("Writing to " + filename)
        for i in petitions:
            f.write(str(i))
            f.write("\n")  # There will be one extra line at end of file.

    print(filename +" written\n")


def totalSigsWrite(petitions: list) -> None:
    """
    Gets the last line of signatureTotals.txt
    Splits it into date [(YYYY-MM-DD), totalSigs)] then checks if the day isn't today.
    If so finds the totalSigs for all time by reading entire petitions list.
    Writes total sigs to the end of the file in the form - YYYY-MM-DD totalSigs) - Including the space.

    :param petitions: Full list of petitions
    :type petitions: list
    :rtype: None
    """
    lastLine = ""
    with open('DailySignatures/signatureTotals.txt', 'r') as f:  # Reading contents
        for line in f:
            lastLine = line  # Will end with this as the actual last line.

    lastLine = lastLine.split()  # Split by the one space character.

    if lastLine[0] != str(date.today()):  # Is the day today?
        print("Printing Today's Total Sigs\n")
        totalSigs = 0
        for p in petitions:
            totalSigs += p.signatures
        
        with open('DailySignatures/signatureTotals.txt', 'a') as f:  # Appending
            f.write('\n')
            f.write(str(date.today()) + ' ' + str(totalSigs))
