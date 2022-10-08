from dataclasses import dataclass
from datetime import datetime, date
from websocket import create_connection
from dateutil.relativedelta import relativedelta
import json
import graphing


@dataclass
class Petition:
    id: int
    signatures: int
    response: bool
    updates: bool
    charged: bool
    timestamp: date
    expires: date
    title: str
    author: str
    tags: list


# From web browser
headers = json.dumps({
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'en-US,en;q=0.9',
    'Cache-Control': 'no-cache',
    'Connection': 'Upgrade',
    'Host': 'pawprints.rit.edu',
    'Origin': 'https://pawprints.rit.edu',
    'Pragma': 'no-cache',
    'Sec-WebSocket-Extensions': 'permessage-deflate; client_max_window_bits',
    'Sec-WebSocket-Key': 'https://github.com/Carter4242/Pawprints-Webscraper',
    'Sec-WebSocket-Version': '13',
    'Upgrade': 'websocket',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
})

def mostFrequentAuthor(List):
    authors = []
    for i in List:
        authors.append(i.author)
    
    counter = 0
    num = authors[0]
    for i in authors:
        curr_frequency = authors.count(i)
        if(curr_frequency > counter):
            counter = curr_frequency
            num = i
    return num

# Launch the connection to the server.
# Perform the handshake.
# ws.send(json.dumps({"command": "get", "id": 7}))
print("\nCreating Connection")
ws = create_connection('wss://pawprints.rit.edu/ws/', headers=headers)
#ws.send(json.dumps({"command":"paginate","sort":"most recent","filter":"all","page":1}))
ws.send(json.dumps({"command":"all"}))

print("\nReceiving paginate")
result = ws.recv()
print("Receiving all")
result = ws.recv()

print("\nRemoving header")
result = result[14:result.find(', \"map\": {')]
print("Loading json")
data = json.loads(result)
print ("Length of data: " + str(len(data)))

print("\nLoading Petitions List")
petitions = []
for i in data:
    made = datetime.date(datetime.strptime(i['timestamp'],'%B %d, %Y'))
    expired = datetime.date(datetime.strptime(i['expires'],'%B %d, %Y'))
    updated = False
    responded = bool(i['response'])
    if i['updates'] != []:
        updated = True
        responded = True
    petitions.append(Petition(
        id=int(i['id']),
        signatures=int(i['signatures']),
        response=responded,
        updates=updated,
        charged=bool(i['in_progress']),
        timestamp= made,
        expires= expired,
        title=i["title"],
        author=i['author'],
        tags=i['tags'],
        ))

print("Finished Loading Petitions List")
print("Length of petitions: " + str(len(petitions)))

print("\nSorting...")
petitions.sort(key = lambda x: x.signatures, reverse = True)
petitions.sort(key = lambda x: x.response, reverse = True)
# print("Most frequent author:", mostFrequentAuthor(petitions))
petitions.sort(key = lambda x: x.timestamp)

sixMonthsAgo = date.today() - relativedelta(months=+6)
for i in petitions:
    if i.response == False:
            if i.signatures >= 200 and i.timestamp < sixMonthsAgo:
                # print(i)
                pass


# graphing.buildTimeGraph(petitions)


filename = "Output/" + str(datetime.now()) + " - Length: " + str(len(petitions)) + ".txt"
print("\nOpening "+filename)
with open(filename, 'a') as f:
    print("Writing to " + filename)
    for i in petitions:
        f.write(str(i))
        f.write("\n")
print(filename +" written\n")

lastLine = ""

with open('DailySignatures/signatureTotals.txt') as f:
    for line in f:
        lastLine = line

lastLine = lastLine.split()

if lastLine[0] != str(date.today()):
    print("Printing Today's Total Sigs\n")
    totalSigs = 0
    for p in petitions:
        totalSigs += p.signatures
    
    with open('DailySignatures/signatureTotals.txt', 'a') as f:
        f.write('\n')
        f.write(str(date.today()) + ' ' + str(totalSigs))

