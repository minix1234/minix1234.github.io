print("Covid-19 Province Based Graphs")
print("-------------------------------")
print("For Canada")

import pandas as pd
import numpy as np
import plotly.express as px

url = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv'  #time_series_19-covid-Confirmed.csv'#
dfcases = pd.read_csv(url,index_col=0,parse_dates=[0])

threshold = 5000  #used to remove countries in earlier infections from plots
dfcases = dfcases[dfcases['Country/Region'] == 'Canada']
dfcases = dfcases.drop(columns=['Lat','Long','Country/Region'])

df = dfcases.groupby('Province/State').sum()
df = df.reset_index()
df = df.rename(columns={'Province/State ': 'date'})
df = df.T
df.columns = df.iloc[0]
df = df.drop(df.index[0])
df = df.reset_index()
df = df.rename(columns={'index': 'dates'})
df['dates'] = df['dates'].astype('datetime64')
df = df.set_index('dates')
df = df.apply(pd.to_numeric) # convert all columns of DataFrame
df = df[df.index >= '2020-02-23']
df.at['2020-04-04','Quebec'] = 6997

dfmelt = df.reset_index()
dfmelt = dfmelt.melt(id_vars=['dates'])

dfmelt = dfmelt.rename(columns={'Province/State': 'Province'})
dfmelt = dfmelt.rename(columns={'value': 'cases'})
#dfmelt = dfmelt.drop(columns=['dates'])
dfmelt = dfmelt.set_index('dates')
dfmelt['Province'] = dfmelt['Province'].astype('category')

fig = px.line(dfmelt, x=dfmelt.index, y="cases",color='Province')#,log_y=True)
fig.update_layout(
    title="Aligned Covid-19 Active Cases Data",
    xaxis_title="Dates",
    yaxis_title="Number of Active Cases",
    font=dict(
        family="Courier New, monospace",
        size=16,
        color="#7f7f7f"
    ),
    legend=dict(
        font=dict(
            family="sans-serif",
            size=12,
            color="black"
        )
    )
)
#fig.show()
print("Writing figure file")
fig.write_html("province.html")
