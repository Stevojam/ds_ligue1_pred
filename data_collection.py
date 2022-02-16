import TransferMarkt_scraper as tms
import pandas as pd

df_squadValues = tms.get_squadValues(2011, 2022)
df_transferDetails = tms.get_transferDetails(2011, 2022)
df_standings = tms.get_seasonTable(2011, 2022)

df_squadValues.to_csv('squad_values.csv', index = False)
df_transferDetails.to_csv('transfer_details.csv', index = False)
df_standings.to_csv('standings.csv', index = False)


