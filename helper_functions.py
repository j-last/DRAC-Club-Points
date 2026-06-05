import time
import json
import pandas as pd
from datetime import time
from config import TIME_FORMAT
import requests
from bs4 import BeautifulSoup as bs

def get_total_race_timings_results(url:str) -> dict[str:time]:
    """Web scrapes all dereham runners AC results from a totalracetiming website.
    Returns a dictionary with entries in the form {runnerName : runnerTime}
    """
    race_runners = {}

    page = requests.get(url)
    soup = bs(page.content, "html.parser")
    runners = soup.find("tbody") # gets all 

    for runner in runners:
        runnerstring = runner.decode_contents()
        if "<td>Dereham Runners AC</td>" in runnerstring:
            runnerstring = runnerstring.split("<td")
            name = (runnerstring[2][1:-5] + " " + runnerstring[3][1:-5]).upper()
            raceTime = time.strptime(runnerstring[-2][2:-8], "%H:%M:%S")

            race_runners[name] = raceTime
    
    return race_runners