import pandas as pd
import numpy as np
import plotly.express as px

url = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv'  #time_series_19-covid-Confirmed.csv'#
dfcases = pd.read_csv(url,index_col=0,parse_dates=[0])
dfcases = dfcases.drop(columns=['Lat','Long'])
threshold = 10000  #used to remove countries in earlier infections from plots

dfcases.at['Quebec','4/4/20'] = 6997 # fixes an issue with the numbers from WHO

df = dfcases.groupby('Country/Region').sum()
#df = df.T
df = df.reset_index()
#df = df.drop([0, 1])
#df['index'] = df['index'].astype('datetime64')
#df = df.set_index('index')


df = df.rename(columns={'Country/Region': 'date'})
df = df.T
df.columns = df.iloc[0]
df = df.drop(df.index[0])
df = df.reset_index()
df = df.rename(columns={'index': 'dates'})
df['dates'] = df['dates'].astype('datetime64')
df = df.set_index('dates')
df = df.apply(pd.to_numeric)

dfmax = pd.DataFrame(df.max(),columns=['max'] )
dfmax = dfmax.reset_index()
dfmax = dfmax.rename(columns={'date': 'country'})

dfmax = dfmax[dfmax['max'] > threshold]
llist = dfmax['country'].values.tolist()
#llist = llist + ['Japan']
df1 = df[llist]

dfgt = pd.DataFrame()
dflt = pd.DataFrame()
shift = {}

for country in llist:
    #Check country data for if the value is greater than 100
    dfgt[country] = df1[country]>=100
    # Determine the number of days to shift backwards to day zero.
    sh = pd.to_datetime('2020-01-22') - dfgt[country].idxmax() #idxmax() -> find the first instance of True in the above Boolean list
    df1[country] = df1[country].shift(sh.days)
    
    #if country in poplist:
    #    try:
    #        num = pop['Population'].loc[pop['Country'] == country].values
    #        df[country] = df[country]/num[0]*100
    #    except:
    #        pass


df1['China'] = df1['China'].shift(4)


df1.index = pd.to_timedelta(df.index - pd.to_datetime('2020-01-22')).days

dfmelt = df1.reset_index()
dfmelt = dfmelt.melt(id_vars=['dates'])
dfmelt = dfmelt.rename(columns={'date': 'country'})
dfmelt = dfmelt.rename(columns={'value': 'cases'})
#dfmelt = dfmelt.drop(columns=['dates'])
dfmelt = dfmelt.set_index('dates')
dfmelt['country'] = dfmelt['country'].astype('category')
#dfmelt['cases'] = dfmelt['cases'].astype('int32') # fails due to nan
gbt = dfmelt.groupby(dfmelt.index).sum()

fig = px.line(dfmelt, x=dfmelt.index, y="cases",color='country')#,log_y=True)
fig.update_layout(
    title="Aligned Covid-19 Active Cases Data",
    xaxis_title="Days Since 100th Active Case",
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
fig.write_html("infections_aligned.html")

figlog = px.line(dfmelt, x=dfmelt.index, y="cases",color='country',log_y=True)
figlog.update_layout(
    title="Aligned Covid-19 Active Cases Data",
    xaxis_title="Days Since 100th Active Case",
    yaxis_title="Number of Active Cases [Log Scale]",
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
#figlog.show()
figlog.write_html("infections_logscal.html")

df2 = df1.diff()
dfmelt2 = df2.reset_index()
dfmelt2 = dfmelt2.melt(id_vars=['dates'])
dfmelt2 = dfmelt2.rename(columns={'date': 'country'})
dfmelt2 = dfmelt2.rename(columns={'value': 'cases'})
#dfmelt = dfmelt.drop(columns=['dates'])
dfmelt2 = dfmelt2.set_index('dates')
dfmelt2['country'] = dfmelt2['country'].astype('category')
#dfmelt['cases'] = dfmelt['cases'].astype('int32') # fails due to nan
#dfmelt2.tail()

figdif = px.line(dfmelt2, x=dfmelt2.index, y="cases", color='country')
figdif.update_layout(
    title="New Daily Cases",
    xaxis_title="Days Since 100th Active Case",
    yaxis_title="Daily Cases",
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
#figdif.show()
figdif.write_html("differences.html")

""" pop = pd.read_csv('population.csv')
poplist = pop['Country'].to_list()

dfpop = pd.DataFrame()

for country in llist:
    # Check is country name from Github is also in the population CSV
    if country in poplist:
        try:
            num = pop['Population'].loc[pop['Country'] == country].values #find the population data, comes out as array
            dfpop[country] = df1[country]/num[0]*100 #convert the df cases values from absolute to percetnage of country population
        except:
            pass """

""" dfpctmelt = dfpop.reset_index()
dfpctmelt = dfpctmelt.melt(id_vars=['dates'])

dfpctmelt = dfpctmelt.rename(columns={'variable': 'country'})
dfpctmelt = dfpctmelt.rename(columns={'value': 'percent'})
dfpctmelt = dfpctmelt.set_index('dates')
dfpctmelt['country'] = dfpctmelt['country'].astype('category')

popfig = px.line(dfpctmelt, x=dfpctmelt.index, y="percent",color='country',log_y=True)
popfig.update_layout(
    title="Aligned Covid-19 Active Cases Data",
    xaxis_title="Days Since 100th Active Case",
    yaxis_title="Percent of Country Infected",
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
#popfig.show()
popfig.write_html("percentage_aligned.html") """