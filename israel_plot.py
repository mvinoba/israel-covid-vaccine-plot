import matplotlib.pyplot as plt
import pandas as pd

# get covid severe data
df_covid_severe = pd.read_csv(
    "https://raw.githubusercontent.com/dancarmoz/israel_moh_covid_dashboard_data/master/severe_ages_dists.csv",
    skiprows=1)

df_covid_severe['Update Time'] = pd.to_datetime(df_covid_severe['Update Time'])
df_covid_severe.set_index('Update Time', inplace=True)

df_covid_severe = df_covid_severe[
    ['0-9', '10-19', '20-29', '30-39', '40-49', '50-59', '60-69', '70-79', '80-89', '90+']]
df_covid_severe['elderly_over_total'] = df_covid_severe[['60-69', '70-79', '80-89', '90+']].sum(
    axis=1) / df_covid_severe.sum(axis=1)
    
df_covid_severe['elderly_severe'] = df_covid_severe[['60-69', '70-79', '80-89', '90+']].sum(axis=1)

# get vaccine data
df_vaccine = pd.read_csv(
    'https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/vaccinations/country_data/Israel.csv')
total_pop = 9_227_700
df_vaccine['perc'] = df_vaccine['total_vaccinations'] / total_pop
df_vaccine['date'] = pd.to_datetime(df_vaccine['date'], utc=True)

df_plot = pd.merge(df_covid_severe.resample('D')['elderly_over_total'].mean(), df_vaccine, right_on='date',
                   left_index=True)

# handling plot stuff
plt.plot(df_plot['date'].dt.date, df_plot['perc'], 'o-', label='Percentual Vacinado da População')
plt.plot(df_plot['date'].dt.date, df_plot['elderly_over_total'], 'o-',
         label='Idosos/Total dos Pacientes em Situação Crítica')

plt.legend(loc="lower right")
plt.title("Israel COVID-19 - Vacina e Hospitalização")


def annotate_data(x_data, y_data):
    for x, y in zip(x_data, y_data):
        label = "{:.1f}%".format(y * 100)

        plt.annotate(label,  # this is the text
                     (x, y),  # this is the point to label
                     textcoords="offset points",  # how to position the text
                     xytext=(0, 10),  # distance from text to points (x,y)
                     ha='center')  # horizontal alignment can be left, right or center


annotate_data(df_plot['date'].dt.date, df_plot['perc'])
annotate_data(df_plot['date'].dt.date, df_plot['elderly_over_total'])

plt.gca().set_yticklabels(['{:.0f}%'.format(x * 100) for x in plt.gca().get_yticks()])

plt.show()


df_plot = pd.merge(df_covid_severe.resample('D')['elderly_severe'].mean(), df_vaccine, right_on='date',
                   left_index=True)
                   
plt.plot(df_plot['date'].dt.date, df_plot['elderly_severe'], 'o-',
         label='Total de Idosos em Situação Crítica')

plt.legend(loc="lower right")
plt.title("Israel COVID-19 - Vacina e Hospitalização")  

plt.show()


df_covid_hospitalizations = pd.read_csv(
    "https://raw.githubusercontent.com/dancarmoz/israel_moh_covid_dashboard_data/master/hospitalized_and_infected.csv")


df_covid_hospitalizations['Date'] = pd.to_datetime(df_covid_hospitalizations['Date'], utc=True)
df_covid_hospitalizations.set_index('Date', inplace=True)
df_plot = pd.merge(df_covid_hospitalizations, df_vaccine, right_on='date',
                   left_index=True)
 
fig, ax1 = plt.subplots()
ax2 = ax1.twinx()
ax1.plot(df_plot['date'].dt.date, df_plot['Hospitalized'], 'bo-')
ax1.set_ylabel('Hospitalizados', color='b')
         
ax2.plot(df_plot['date'].dt.date, df_plot['perc'], 'go-')
ax2.set_ylabel('Percentual Vacinado da População', color='g')

plt.legend(loc="lower right")
plt.title("Israel COVID-19 - Vacina e Hospitalização")  

plt.show()