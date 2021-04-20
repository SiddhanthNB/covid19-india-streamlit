import streamlit as st
import numpy as np
import pandas as pd
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import matplotlib.pyplot as plt

table =pd.read_csv('https://api.covid19india.org/csv/latest/states.csv')
state_list= ['West Bengal', 'Uttarakhand', 'Uttar Pradesh', 'Tripura', 'Telangana',
            'Tamil Nadu', 'Sikkim', 'Rajasthan', 'Punjab', 'Puducherry', 'Odisha', 
            'Nagaland', 'Mizoram', 'Meghalaya', 'Manipur','Maharashtra', 'Madhya Pradesh',
            'Lakshadweep', 'Ladakh', 'Kerala', 'Karnataka', 'Jharkhand', 'Jammu and Kashmir', 
            'Himachal Pradesh', 'Haryana', 'Gujarat', 'Goa', 'Delhi', 
            'Dadra and Nagar Haveli and Daman and Diu', 'Chhattisgarh', 'Chandigarh', 'Bihar', 
            'Assam', 'Arunachal Pradesh', 'Andhra Pradesh', 'Andaman and Nicobar Islands' ]

temp_list =[]
for i in state_list:
    tmpo = table[table["State"]== i]
    tmpo = tmpo.iloc[-1:,1:5]
    tmpo["Active"]=tmpo['Confirmed']-tmpo["Recovered"]-tmpo['Deceased']
    lis = tmpo.values.tolist()
    temp_list.append(lis[0])

state = []
active = []
confirmed = []
recovered =[]
deaths = []
for i in range(len(temp_list)):
    state.append(temp_list[i][0])
    confirmed.append(temp_list[i][1])
    recovered.append(temp_list[i][2])
    deaths.append(temp_list[i][3])
    active.append(temp_list[i][4])

data_list = [state,confirmed,active,recovered,deaths]  

covid_data = pd.DataFrame(data_list)
covid_data = covid_data.transpose()
covid_data.columns = ["State/UT","Total Cases","Active","Recovered","Deaths"]
covid_data = covid_data.sort_values('Total Cases', ascending=False )
#covid_data.to_csv("covid-19-statewise.csv")

def main(): 
	page = st.sidebar.selectbox("Choose a page", ["Homepage","Symptoms", "State-Wise Visualizations", "A Quick Note"])
	st.sidebar.info(
		"This Project is made possible by [covid19india.org](https://www.covid19india.org/) and also it's [API.](https://github.com/covid19india/api) \n\n"
		"This project is maintained by [Siddhanth](https://github.com/SiddhanthNB).")
    
	if page == "Homepage":
		df =covid_data.copy()
		st.title("Covid-19 in India")
		st.write("""
		### A State-wise Analysis.###
					  """)
		from datetime import date
		today = date.today()
		todays_date = today.strftime("%B %d,%Y")
		st.write('Updated:',todays_date)
	
		st.dataframe(df)
	
		total_cases = df['Total Cases'].sum()
		active_cases = df['Active'].sum()
		deaths = df['Deaths'].sum()
		cured_cases = df['Recovered'].sum()
		mortality_rate = round((deaths/total_cases)*100,2)
		recovery_rate = round((cured_cases/total_cases)*100,2)
		
		st.write("""
		## Lets look at the numbers in India:
		""")
		st.write('Total confirmed cases:', total_cases)
		st.write('Total active cases:', active_cases)
		st.write('Total COVID-19 deaths:', deaths)
		st.write('Total COVID-19 recoveries:', cured_cases)
		st.write('Mortality rate in India till',todays_date,':', mortality_rate,"%")
		st.write('Recovery rate in India till',todays_date,':', recovery_rate,"%")

	
 
	elif page == "State-Wise Visualizations":
		st.write("""
		## We Humans like colors and visuals rather than black and white text, Don't We? ##
		*Note: It is recommended to watch this webpage in fullscreen (i.e. Close the left-side pane)* 
		""")
		df =covid_data.copy()
		active = df['Active'].sum()
		labels = ['Active','Recovered','Deaths']
		values = [active, df['Recovered'].sum(), sum(df['Deaths'])]
		fig1 = go.Figure(data=[go.Pie(labels=labels, values=values)],layout=go.Layout(title='India Corona Virus Cases'))
		fig1.update_traces(hoverinfo='label+percent', textinfo='value', textfont_size=20,
                  marker=dict(colors=['#263fa3', '#2fcc41','#cc3c2f'], line=dict(color='#FFFFFF', width=2)))
		fig1.update_layout(title_text='Current Situation in India according to www.covid19india.org',plot_bgcolor='rgb(275, 270, 273)')
		st.write(fig1)
	
		df =covid_data.copy()
		fig2 = px.bar(df.sort_values('Total Cases', ascending=False).sort_values('Total Cases', ascending=True), 
             x="Total Cases", y="State/UT", 
             title='Statewise Total Cases till today', 
             text='Total Cases', 
             orientation='h', 
             width=1000, height=700, range_x = [0, max(df['Total Cases'])])
		fig2.update_traces(marker_color='#1B13E9', opacity=0.8, textposition='inside')

		fig2.update_layout(plot_bgcolor='rgb(250, 242, 242)')
		st.write(fig2)

		fig3 = px.bar(df.sort_values('Active', ascending=False).sort_values('Active', ascending=True), 
             x="Active", y="State/UT", 
             title='Statewise Total Active Cases till today', 
             text='Active', 
             orientation='h', 
             width=1000, height=700, range_x = [0, max(df['Active'])])
		fig3.update_traces(marker_color='#FF0000', opacity=0.8, textposition='inside')

		fig3.update_layout(plot_bgcolor='rgb(250, 242, 242)')
		st.write(fig3)
		
	elif page == "Symptoms":
		st.write(""" 
		## Symptoms observed in COVID-19 patients ##
		COVID-19 typically causes flu-like symptoms including a fever and cough.
		In some patients - particularly the elderly and others with other chronic health conditions - these symptoms can develop into pneumonia, with chest tightness, chest pain, and shortness of breath.
		It seems to start with a fever, followed by a dry cough.
		After a week, it can lead to shortness of breath, with about 20% of patients requiring hospital treatment.
		Notably, the COVID-19 infection rarely seems to cause a runny nose, sneezing, or sore throat (these symptoms have been observed in only about 5% of patients). Sore throat, sneezing, and stuffy nose are most often signs of a cold. [Source](https://www.worldometers.info/coronavirus/coronavirus-symptoms/)
		""")
		symptoms={'symptoms':['Fever','Tiredness','Dry-cough','Shortness of breath','aches and pains','Sore throat','Diarrhoea','Nausea','vomiting','abdominal pain'],'percentage':[98.6,69.9,82,16.6,14.8,13.9,10.1,10.1,3.6,2.2]}
		symptoms=pd.DataFrame(data=symptoms,index=range(10))
		st.dataframe(symptoms)
		
		labels1 = symptoms["symptoms"]
		values1 = symptoms["percentage"]
		fig6 = go.Figure(data=[go.Pie(labels=labels1, values=values1)],layout=go.Layout(title='Symptoms of Covid-19'))
		st.write(fig6)
		
	elif page == "A Quick Note":
		st.write("""
		## Quick Note on Mental health & COVID-19 ##
		Fear, worry, and stress are normal responses to perceived or real threats, and at times when we are faced with uncertainty or the unknown. So it is normal and understandable that people are experiencing fear in the context of the COVID-19 pandemic.
		Added to the fear of contracting the virus in a pandemic such as COVID-19 are the significant changes to our daily lives as our movements are restricted in support of efforts to contain and slow down the spread of the virus. Faced with new realities of working from home, temporary unemployment, home-schooling of children, and lack of physical contact with other family members, friends and colleagues, it is important that we look after our mental, as well as our physical, health.
		""")	
		st.write("""
		## Conclusions ##
		The best way to prevent and slow down transmission is be well informed about the COVID-19 virus, the disease it causes and how it spreads. Protect yourself and others from infection by washing your hands or using an alcohol based rub frequently and not touching your face. 
		The COVID-19 virus spreads primarily through droplets of saliva or discharge from the nose when an infected person coughs or sneezes, so it’s important that you also practice respiratory etiquette (for example, by coughing into a flexed elbow).
		""")
		st.title("Stay Home, Stay Safe!")
		

		

@st.cache
def load_data():
    df = data.covid_data()
    return df
		
if __name__ == "__main__":
    main()
