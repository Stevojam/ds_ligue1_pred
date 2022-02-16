
import requests
from bs4 import BeautifulSoup
import pandas as pd

### Function to get the squad values from TransferMarkt
def get_squadValues(year, year_end=None):
    
    headers={"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36"}

    if year_end == None:
        page="https://www.transfermarkt.com/ligue-1/startseite/wettbewerb/FR1/plus/?saison_id=2020"
        pageTree = requests.get(page, headers=headers)
        pageSoup = BeautifulSoup(pageTree.content, 'html.parser')

        teams = pageSoup.find_all("td", {"class": "hauptlink no-border-links"})
        squad = pageSoup.find_all("td", {"class": "zentriert"})
        average_age = pageSoup.find_all("td", {"class": "zentriert"})
        market_value = pageSoup.find_all("td", {"class": "rechts"})

        teamsList, squadList, average_age_list, market_value_list = [], [], [], []

        for i in range(len(teams)):
            teamsList.append(teams[i].text)
            squadList.append(squad[4 + 4*i].text)
            average_age_list.append(average_age[1+i].text)
            market_value_list.append(market_value[3+2*i].text)

        df = pd.DataFrame({"Team": teamsList, "Squad": squadList, "Average_age": average_age_list, "Market_value": market_value_list})
        
    else:
        seasons = list(range(year, year_end,1))
        teamsList, squadList, average_age_list, market_value_list, seasonsList = [], [], [], [], []
        for i in seasons:
            page="https://www.transfermarkt.com/ligue-1/startseite/wettbewerb/FR1/plus/?saison_id=" + str(i)
            pageTree = requests.get(page, headers=headers)
            pageSoup = BeautifulSoup(pageTree.content, 'html.parser')

            teams = pageSoup.find_all("td", {"class": "hauptlink no-border-links"})
            squad = pageSoup.find_all("td", {"class": "zentriert"})
            average_age = pageSoup.find_all("td", {"class": "zentriert"})
            market_value = pageSoup.find_all("td", {"class": "rechts"})
            for j in range(len(teams)):
                teamsList.append(teams[j].text)
                squadList.append(squad[4 + 4*j].text)
                average_age_list.append(average_age[5+4*j].text)
                market_value_list.append(market_value[3+2*j].text)
                seasonsList.append(i)

        df = pd.DataFrame({"Year": seasonsList, "Team": teamsList, "Squad": squadList, "Average_age": average_age_list, "Market_value": market_value_list})
    
    return df



### Function to get the transfer expenditure from TransferMarkt

def get_transferDetails(year, year_end=None):
    """
    Get transfer detail for one or multiple year from TransferMarkt
    """
    headers={"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36"}

    if year_end == None:
        page= f"https://www.transfermarkt.com/ligue-1/einnahmenausgaben/wettbewerb/FR1/plus/0?ids=a&sa=&saison_id={year}&saison_id_bis={year}&nat=&pos=&altersklasse=&w_s=s&leihe=&intern=0"
        pageTree = requests.get(page, headers=headers)
        pageSoup = BeautifulSoup(pageTree.content, 'html.parser')

        teams = pageSoup.find_all("td", {"class": "hauptlink no-border-links"})
        nb_players = pageSoup.find_all("td", {"class": "zentriert"})
        expenditure = pageSoup.find_all("td", {"class": "rechts hauptlink redtext"})
        income = pageSoup.find_all("td", {"class": "rechts hauptlink greentext"})
        balance = pageSoup.find_all("td", {"class": "rechts hauptlink"})

        teamsList, arrivalsList, departuresList, expenditureList, incomeList, balanceList = [], [], [], [], [], []

        for i in range(len(teams)):
            teamsList.append(teams[i].text)
            arrivalsList.append(nb_players[2+i*4].text)
            departuresList.append(nb_players[3+i*4].text)
            expenditureList.append(expenditure[i].text)
            incomeList.append(income[i].text)
            balanceList.append(balance[i].text)

        df = pd.DataFrame({"Team": teamsList, "Arrivals": arrivalsList, "Expenditure": expenditureList, 
                    "Departures": departuresList, "Income": incomeList, "Balance": balanceList})

    else:
        seasons = list(range(year, year_end, 1))
        teamsList, arrivalsList, departuresList, expenditureList, incomeList, balanceList, seasonList = [], [], [], [], [], [], []

        for i in seasons:
            page= f"https://www.transfermarkt.com/ligue-1/einnahmenausgaben/wettbewerb/FR1/plus/0?ids=a&sa=&saison_id={str(i)}&saison_id_bis={str(i)}&nat=&pos=&altersklasse=&w_s=s&leihe=&intern=0"
            pageTree = requests.get(page, headers=headers)
            pageSoup = BeautifulSoup(pageTree.content, 'html.parser')

            teams = pageSoup.find_all("td", {"class": "hauptlink no-border-links"})
            nb_players = pageSoup.find_all("td", {"class": "zentriert"})
            expenditure = pageSoup.find_all("td", {"class": "rechts hauptlink redtext"})
            income = pageSoup.find_all("td", {"class": "rechts hauptlink greentext"})
            balance = pageSoup.find_all("td", {"class": "rechts hauptlink"})

            for j in range(len(teams)):
                teamsList.append(teams[j].text)
                arrivalsList.append(nb_players[2+j*4].text)
                departuresList.append(nb_players[3+j*4].text)
                expenditureList.append(expenditure[j].text)
                incomeList.append(income[j].text)
                balanceList.append(balance[j].text)
                seasonList.append(i)

        df = pd.DataFrame({"Season": seasonList, "Team": teamsList, "Arrivals": arrivalsList, "Expenditure": expenditureList, 
                    "Departures": departuresList, "Income": incomeList, "Balance": balanceList})

    return df


### Function to get the table data from Transfermarkt
def get_seasonTable(year, year_end=None):
    """
    Get the league standings of one or multiple year from TransferMarkt
    """
    headers={"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36"}

    if year_end == None:
        page="https://www.transfermarkt.com/ligue-1/tabelle/wettbewerb/FR1?saison_id=" + str(year)
        pageTree = requests.get(page, headers=headers)
        pageSoup = BeautifulSoup(pageTree.content, 'html.parser')

        position = pageSoup.find_all("td", {"class": "rechts hauptlink"})
        teams = pageSoup.find_all("td", {"class": "no-border-links hauptlink"})
        table_values = pageSoup.find_all("td", {"class": "zentriert"})

        positionList, teamsList, matchesList, winList, drawList, lossList, goalsList, pointsList = [], [], [], [], [], [], [], []

        for j in range(20):
            positionList.append(position[j].text)
            teamsList.append(teams[j].a["title"])
            matchesList.append(table_values[1+8*j].text)
            winList.append(table_values[2+8*j].text)
            drawList.append(table_values[3+8*j].text)
            lossList.append(table_values[4+8*j].text)
            goalsList.append(table_values[5+8*j].text)
            pointsList.append(table_values[7+8*j].text)
    

        df = pd.DataFrame({"Position": positionList, "Team": teamsList, "Matches": matchesList, "Wins": winList, 
                    "Draws": drawList, "Losses": lossList, "Goals": goalsList, "Points": pointsList})

    else:
        seasons = list(range(year,year_end,1))
        positionList, teamsList, matchesList, winList, drawList, lossList, goalsList, pointsList, seasonList = [], [], [], [], [], [], [], [], []

        for i in seasons:
            page= "https://www.transfermarkt.com/ligue-1/tabelle/wettbewerb/FR1?saison_id=" + str(i)
            pageTree = requests.get(page, headers=headers)
            pageSoup = BeautifulSoup(pageTree.content, 'html.parser')

            position = pageSoup.find_all("td", {"class": "rechts hauptlink"})
            teams = pageSoup.find_all("td", {"class": "no-border-links hauptlink"})
            table_values = pageSoup.find_all("td", {"class": "zentriert"})

            for j in range(20):
                positionList.append(position[j].text)
                teamsList.append(teams[j].a["title"])
                matchesList.append(table_values[1+8*j].text)
                winList.append(table_values[2+8*j].text)
                drawList.append(table_values[3+8*j].text)
                lossList.append(table_values[4+8*j].text)
                goalsList.append(table_values[5+8*j].text)
                pointsList.append(table_values[7+8*j].text)
                seasonList.append(i)
    
        df = pd.DataFrame({"Season": seasonList, "Position": positionList, "Team": teamsList, "Matches": matchesList, "Wins": winList, 
                    "Draws": drawList, "Losses": lossList, "Goals": goalsList, "Points": pointsList})

    return df



