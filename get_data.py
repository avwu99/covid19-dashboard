import requests
import time

URL = "http://coronavirusapi.com/getTimeSeriesJson/"


def getData(state):
    r = requests.get(URL+ state)
    data = r.json()

    return data

def filterIntoList(state):
    json_data = getData(state)
    date = []
    dates = listTime(json_data)
    tested = listTested(json_data)
    positive = listPositive(json_data)
    deaths = listDeaths(json_data)

    return dates[-15:], tested[-15:], positive[-15:], deaths[-15:]


def listTime(data):
    dates = []
    for i in range(len(data)):
        curr_epoch = data[i]['seconds_since_epoch']
        day = time.strftime('%m/%d/%y', time.gmtime(curr_epoch))
        dates.append(day)

    return dates

def listTested(data):
    tested = []
    for i in range(len(data)):
        curr_tested = data[i]['tested']

        tested.append(curr_tested)

    return tested

def listPositive(data):
    positive = []
    for i in range(len(data)):
        curr_pos = data[i]['positive']
        if curr_pos == "None":
            positive.append(0)
        else:
            positive.append(curr_pos)

    return positive

def listDeaths(data):
    deaths = []
    for i in range(len(data)):
        curr_death = data[i]['deaths']
        if isinstance(curr_death, int):
            deaths.append(curr_death)
        else:
            deaths.append(0)

    return deaths

# if __name__ == "__main__":
#     filterIntoList("il")
