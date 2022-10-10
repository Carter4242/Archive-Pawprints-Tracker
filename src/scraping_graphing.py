"""
PAWPRINTS-WEBSCRAPER

This module handles the creation of graphs using the petitions data.

Author: Carter4242
https://github.com/Carter4242
"""


import matplotlib.pyplot as plt


def buildGraphs(petitions: list) -> None:
    """
    Bit of a mess right now, will sort out later.

    :param petitions: Full list of petitions
    :type petitions: list
    :rtype: None
    """   

    yearMonthsList = []
    for p in petitions:
        dateStr = str(p.timestamp.month) + r"/" + str(p.timestamp.year)
        yearMonthsList.append(dateStr)

    xValues = []

    if (petitions[0].timestamp.year != petitions[-1].timestamp.year):
        for m in range(petitions[0].timestamp.month, 13):
            dateStr = str(m) + r"/" + str(petitions[0].timestamp.year)
            xValues.append(dateStr)

        if ((petitions[0].timestamp.year+1) != petitions[-1].timestamp.year):
            for y in range(petitions[0].timestamp.year+1,petitions[-1].timestamp.year):
                for m in range(1,13):
                    dateStr = str(m) + r"/" + str(y)
                    xValues.append(dateStr)

        for m in range(1, petitions[-1].timestamp.month+1):
            dateStr = str(m) + r"/" + str(petitions[-1].timestamp.year)
            xValues.append(dateStr)

    else:
        for m in range(petitions[0].timestamp.month, petitions[-1].timestamp.month+1):
                dateStr = str(m) + r"/" + str(petitions[-1].timestamp.year)
                xValues.append(dateStr)
    
    yValues = []
    yValuesIgnored = []
    yValuesResponded = []
    yValuesSigsOverCharged = []
    yValuesSigsOverNotCharged = []
    lIgnored = 0
    lResponded = 0
    lSigsOverCharged = 0
    lSigsNotOverCharged = 0
    lCountUp = -1
    lCountDown = 0
    for x in xValues:
        countPetitions = yearMonthsList.count(x)
        yValues.append(countPetitions)
        lCountDown = countPetitions
        lCountUp += countPetitions
        for i in range(lCountDown):
            if petitions[lCountUp-i].response == False:
                if petitions[lCountUp-i].signatures >= 200:
                    if petitions[lCountUp-i].charged:
                        lSigsOverCharged += 1
                    else:
                        lSigsNotOverCharged += 1
                else:
                    lIgnored += 1
            else:
                lResponded += 1
        yValuesIgnored.append(lIgnored)
        yValuesResponded.append(lResponded)
        yValuesSigsOverCharged.append(lSigsOverCharged)
        yValuesSigsOverNotCharged.append(lSigsNotOverCharged)
        lIgnored = 0
        lResponded = 0
        lSigsOverCharged = 0
        lSigsNotOverCharged = 0

    xAxis = []

    for i in range (1, len(xValues)+1):
        xAxis.append(i)
    
    xRespondedList = []
    for i in range(len(yValuesSigsOverCharged)):
        xRespondedList.append(yValuesSigsOverCharged[i] + yValuesSigsOverNotCharged[i])

    xIgnoreList = []
    for i in range(len(yValuesSigsOverCharged)):
        xIgnoreList.append(yValuesSigsOverCharged[i] + yValuesResponded[i] + yValuesSigsOverNotCharged[i])


    plt.figure(figsize=(12, 9), dpi=80)
    plt.bar(xValues, yValuesSigsOverNotCharged, 0.8, color = ['#FF0000'], label='Not Responded ≥ 200 Signatures + Not Charged')
    plt.bar(xValues, yValuesSigsOverCharged, 0.8, bottom=yValuesSigsOverNotCharged, color = ['#FF8000'], label='Not Responded ≥ 200 Signatures + Charged')
    plt.bar(xValues, yValuesResponded, 0.8, bottom=xRespondedList, color = ['#00E600'], label='Responded')
    plt.bar(xValues, yValuesIgnored, 0.8, bottom=xIgnoreList, color = ['#511717'], label='Not Responded < 200 Signatures')

    plt.ylabel("Signatures")
    plt.legend()

    plt.xticks(fontsize=8)
    plt.xticks(rotation = 90)

    plt.margins(0.005, tight=True)
    plt.tight_layout(pad=0.5)

    plt.savefig('graphs/petitionsBarGraphDetailed.svg')


    yValuesSigsOver = []
    for i in range(len(yValuesSigsOverCharged)):
        yValuesSigsOver.append(yValuesSigsOverCharged[i] + yValuesSigsOverNotCharged[i])


    plt.figure(figsize=(12, 9), dpi=80)
    plt.bar(xValues, yValuesSigsOver, 0.8, color = ['#FF0000'], label='Not Responded ≥ 200 Signatures')
    plt.bar(xValues, yValuesResponded, 0.8, bottom=yValuesSigsOver, color = ['#00E600'], label='Responded')
    plt.bar(xValues, yValuesIgnored, 0.8, bottom=xIgnoreList, color = ['#511717'], label='Not Responded < 200 Signatures')

    plt.ylabel("Signatures")
    plt.legend()

    plt.xticks(fontsize=8)
    plt.xticks(rotation = 90)

    plt.margins(0.005, tight=True)
    plt.tight_layout(pad=0.5)

    plt.savefig('graphs/petitionsBarGraph.svg')
    