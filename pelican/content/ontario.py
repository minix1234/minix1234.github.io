url = 'https://data.ontario.ca/dataset/f4112442-bdc8-45d2-be3c-12efae72fb27/resource/455fd63b-603d-4608-8216-7d8647f43350/download/conposcovidloc.csv'
urlstatus = 'https://data.ontario.ca/dataset/f4f86e54-872d-43f8-8a86-3892fd3cb5e6/resource/ed270bb8-340b-41f9-a7c6-e8ef587e6d11/download/covidtesting.csv'
vaccinestatus = "https://data.ontario.ca/dataset/752ce2b7-c15a-4965-a3dc-397bf405e7cc/resource/8a89caa9-511c-4568-af89-7f2174b4378c/download/vaccine_doses.csv"

import pandas as pd
import numpy as np
import plotly.express as px

dfcases = pd.read_csv(url,index_col=1,parse_dates=[1])
dfcases = dfcases.drop(columns=['Reporting_PHU_Website','Reporting_PHU_Latitude','Reporting_PHU_Longitude','Reporting_PHU_Address','Reporting_PHU_Postal_Code'])
dfcases = dfcases[dfcases.index <= '2021-06-01']


df2 = dfcases.groupby(['Age_Group','Outcome1']).count()
df2 = df2.drop(columns=['Client_Gender','Case_AcquisitionInfo','Reporting_PHU','Reporting_PHU_City'])
df2 = df2.reset_index()#.to_csv('ontario.csv')
df2 = df2.rename(columns={'Outcome1': 'Outcome'})
df2 = df2.rename(columns={'Row_ID': 'Cases'})

figage = px.bar(df2, x="Age_Group", y="Cases", color='Outcome')
figage.update_layout(
    title="Ontario Covid-19 Cases by Age Group and Case Outcome",
    xaxis_title="Age Grouping",
    yaxis_title="Number of Cases",
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
#figage.show()
figage.write_html("Ontariobarage.html")

df3 = dfcases.groupby(['Reporting_PHU_City','Outcome1','Age_Group']).count()
df3 = df3.drop(columns=['Client_Gender','Case_AcquisitionInfo','Reporting_PHU'])
df3 = df3.reset_index()#.to_csv('ontario.csv')
df3 = df3[df3['Outcome1'] == 'Not Resolved']
df3 = df3.rename(columns={'Outcome1': 'Outcome'})
df3 = df3.rename(columns={'Row_ID': 'Cases'})

figPHU = px.bar(df3, x="Reporting_PHU_City", y="Cases", color='Age_Group')
figPHU.update_layout(
    title="Ontario Covid-19 Active Cases by Reportin Public Health Unit and Age Group",
    xaxis_title="",
    yaxis_title="Number of Cases",
    font=dict(
        family="Courier New, monospace",
        size=12,
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
#figPHU.show()
figPHU.write_html("OntarioPHU.html")

dfstatus = pd.read_csv(urlstatus,index_col=0,parse_dates=[0])
dfstatus = dfstatus.astype(float)
dfstatus = dfstatus[dfstatus.columns[0:13]]
dfstatus.columns = ['Confirmed Negative','Presumptive Negative','Presumtive Positive','Confirmed Positive','Resolved','Deaths','Total Cases','Approved for Testing','Tests Completed','Under Investigation','Hospitalized','In ICU','On Venilator']

df1 = dfstatus
df1 = df1.apply(pd.to_numeric)
dfmelt = df1.reset_index()
dfmelt = dfmelt.drop(columns=["Approved for Testing"])
dfmelt = dfmelt.melt(id_vars=['Reported Date'])
dfmelt = dfmelt.set_index('Reported Date')
dfmelt['variable'] = dfmelt['variable'].astype('category')

fig = px.line(dfmelt, x=dfmelt.index, y="value",color='variable')#,log_y=True)
fig.update_layout(
    title="Ontario Covid-19 Data",
    xaxis_title="Dates",
    yaxis_title="Values",
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
fig.write_html("Ontario.html")



df3 = dfcases.reset_index()
df4 = pd.DataFrame()
df4['CASES'] = df3.groupby(['Accurate_Episode_Date','Outcome1'])['Row_ID'].count()
df4 = df4.reset_index()
df4['Outcome1'] = df4['Outcome1'].astype('category')



fig = px.bar(df4, x="Accurate_Episode_Date", y="CASES", color='Outcome1')
fig.update_layout(
    title="Ontario Covid-19 Data by Presentation Date",
    xaxis_title="Dates",
    yaxis_title="Number of Cases",
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
fig.write_html("Ontariobar.html")


dffatal = dfcases[dfcases['Outcome1'] == 'Fatal'].groupby(['Age_Group']).count()
dffatal = dffatal.rename(columns={'Row_ID': 'Number of Dead'})
dffatal = dffatal.reset_index()


figpie = px.pie(dffatal, values='Number of Dead', names='Age_Group', title='')
figpie.update_layout(
    title="Ontario Covid-19 Deaths",
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
#figpie.show()
figpie.write_html("Ontariopie.html")

df5 = df4
df5['Outcome1'] = df5['Outcome1'].astype('object')
df5 = df5.pivot(values='CASES', index='Accurate_Episode_Date', columns='Outcome1')
df5 = df5.fillna(0)
df5 = df5.cumsum(skipna=True)
df5 = df5.reset_index()
df5['Total_Cases'] = df5['Fatal']+df5['Not Resolved']+df5['Resolved']
#df5 = df5[df5['Accurate_Episode_Date'] > '2020-01-27']
df5 = pd.melt(df5,id_vars=['Accurate_Episode_Date'],value_vars=['Fatal','Not Resolved','Resolved','Total_Cases'])
#df5 = pd.melt(df5,id_vars=['Accurate_Episode_Date'],value_vars=['Total_Cases'])
df5 = df5.set_index('Accurate_Episode_Date')
#df5 = df5[df5.index <= '2021-06-01']

figpres = px.line(df5, x=df5.index, y="value",color='Outcome1')#,log_y=True)
figpres.update_layout(
    title="Ontario Covid-19 Data by Presentation Date",
    xaxis_title="Date",
    yaxis_title="Cases",
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
#figpres.show()
figpres.write_html("Ontariopresdate.html")


# Vaccination Data
# -------------------------------------
# Graph to plot the various vacination 
# data
# --------------------------------------

vaccinestatus = "https://data.ontario.ca/dataset/752ce2b7-c15a-4965-a3dc-397bf405e7cc/resource/8a89caa9-511c-4568-af89-7f2174b4378c/download/vaccine_doses.csv"

#dfVC = pd.read_csv(vaccinestatus,parse_dates=[1])
#dfVC = dfVC.set_index('report_date')
#dfVC.columns=["Daily Doses","Total Doses","Doses for Fully Vaccinated","Fully Vaccinated"]
#dfVC["Partially Vaccinated"] = dfVC['Total Doses']-dfVC["Doses for Fully Vaccinated"]
#dfVC["Population Vaccinated"] = dfVC["Partially Vaccinated"]+dfVC["Fully Vaccinated"]
#dfVC["Vaccinated Percentage"] = dfVC["Population Vaccinated"]/14750000*100

dfVC = pd.read_csv(vaccinestatus,parse_dates=[1])
dfVC = dfVC.set_index('report_date')
dfVC.columns=["Daily Daily","Daily First Dose","Daily Second Dose","Total Doses","Population Vaccinated","Doses for Fully Vaccinated","Fully Vaccinated"]
dfVC["Partially Vaccinated"] = dfVC['Total Doses']-dfVC["Doses for Fully Vaccinated"]
dfVC["Vaccinated Percentage"] = dfVC["Population Vaccinated"]/14750000*100
dfVC.to_csv('dfVC.csv')

dfmelt = dfVC.reset_index()
dfmelt = dfmelt.melt(id_vars=['report_date'])
dfmelt = dfmelt.set_index('report_date')
dfmelt['variable'] = dfmelt['variable'].astype('category')
dfmelt.to_csv('dfmelt.csv')

fig = px.line(dfmelt, x=dfmelt.index, y="value",color='variable')#,log_y=True)
fig.update_layout(
    title="Ontario Covid-19 Vaccination Data",
    xaxis_title="Date",
    yaxis_title="Cases",
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
fig.write_html("OntarioPPLVac.html")