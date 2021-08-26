import pandas as pd
import seaborn as sns
import plotly.express as px
import matplotlib.pyplot as plt


def vacc_rate_to_pop(data):
    '''
    Takes in a dataframe from the owid database, and creates a plot of
    Rate of Vaccination poer 1 million people in Developed Countries
    and returns the max vaccination rate per 1 million people. Lastly,
    makes an interactive plot of the bar plot.
    '''
    df = data[['location',
               'date',
               'new_vaccinations_smoothed_per_million',
               'population', 'human_development_index']].dropna()
    df_new = df.merge(df.groupby('location')['date'].max().reset_index(),
                      on=['location', 'date'], how='inner')
    df_developed = df_new[(df_new['human_development_index'] > 0.930) &
                          (df_new['human_development_index'] < 1.000)]
    g = sns.barplot(data=df_developed,
                    x='location',
                    y='new_vaccinations_smoothed_per_million',
                    hue='location')
    g.set_xticklabels(g.get_xticklabels(), rotation=45)
    plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
    plt.title('Rate of Vaccination per 1 million people in Developed Countries')
    plt.xlabel('Developed Countries (HDI > 0.930)')
    plt.ylabel('Total Vaccinations administered per 1 million people')
    plt.savefig('figures/vaccination_rate.png', bbox_inches='tight')
    # Interactive Plot
    fig = px.bar(df_developed,
                 x='location',
                 y='new_vaccinations_smoothed_per_million',
                 color='location',
                 title='Rate of Vaccination per 1 million people in Developed Countries')
    fig.show()
    # print(df_developed)
    return df['new_vaccinations_smoothed_per_million'].max()


def pop_density_coid_growth_rate(data):
    '''
    Takes in a dataframe from the owid database, and creates plots of
    Growth Rate of COVID-19 against Population Density for Developed Countries,
    Growth Rate of COVID-19 against Population Density for Underdeveloped
    Countries, and Growth Rate of COVID-19 against Population Density for
    All Countries. At the very end returns a Series of the calculated average
    growth rate of COVID 19 for each country. Also makes an interactive plot
    of the last chart.
    '''
    df = data[['location',
               'date',
               'total_cases',
               'population_density',
               'human_development_index']]
    df = df.dropna()
    # Change String dates to someting we could process numerically
    df['date'] = pd.to_datetime(df['date'], format='%Y-%m-%d')
    avg_growth_rates = df.groupby('location')['date', 'total_cases'].apply(
        lambda x: (max(x['total_cases']) - min(x['total_cases'])) /
                  ((max(x['date']) - min(x['date'])).days)
        )
    df_unique_countries = df.drop_duplicates(subset=['location'])
    df_unique_countries = df_unique_countries[['location',
                                               'population_density',
                                               'human_development_index']]
    hdi_unique = df_unique_countries['human_development_index']
    pop_dense = df_unique_countries['population_density']
    df_final = pd.DataFrame({'location': df_unique_countries['location'],
                             'population_density': pop_dense,
                             'average_growth_rate': avg_growth_rates.values,
                             'HDI': hdi_unique})
    df_final = df_final[(df_final['location'] != 'Singapore') &
                        (df_final['location'] != 'United States') &
                        (df_final['location'] != 'World') &
                        (df_final['average_growth_rate'] < 10000) &
                        (df_final['population_density'] < 400)]
    df_final_developed = df_final[(df_final['HDI'] > 0.930) &
                                  (df_final['HDI'] < 1.000)]
    df_final_undeveloped = df_final[(df_final['HDI'] < 0.600)]
    fig1, axs1 = plt.subplots(1)
    sns.regplot(data=df_final_developed,
                ax=axs1,
                x='population_density',
                y='average_growth_rate')
    plt.title('Growth Rate of COVID-19 against Population Density for Developed Countries')
    fig1.savefig('figures/growth_rate_vs_pop_density_developed.png',
                 bbox_inches='tight')
    fig2, axs2 = plt.subplots(1)
    sns.regplot(data=df_final_undeveloped,
                ax=axs2,
                x='population_density',
                y='average_growth_rate')
    plt.title('Growth Rate of COVID-19 against Population Density for Underdeveloped Countries')
    fig2.savefig('figures/growth_rate_vs_pop_density_underdeveloped.png',
                 bbox_inches='tight')
    fig3, axs3 = plt.subplots(1)
    sns.scatterplot(data=df_final,
                    ax=axs3,
                    x='population_density',
                    y='average_growth_rate',
                    hue='location')
    plt.title('Growth Rate of COVID-19 against Population Density for All Countries')
    plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
    fig3.savefig('figures/growth_rate_vs_pop_density_both.png',
                 bbox_inches='tight')
    # Interactive Plot
    fig = px.scatter(df_final,
                     x='population_density',
                     y='average_growth_rate',
                     color='location',
                     title='Growth Rate of COVID-19 against Population Density for All Countries')
    fig.show()
    # print(avg_growth_rates)
    # print(df_final)
    return df_final_developed['average_growth_rate']


def hdi_vs_mortality_testing_rate(data):
    '''
    Takes in a dataframe from the owid database, and creates plots of
    Max Mortality Rate of Each Country against HDI and Max Death Rate
    of Each Country against HDI. At the very end returns a Series for
    the Max Mortality Rate of each country.
    '''
    df_death_rates = data[['location',
                           'date',
                           'total_deaths_per_million',
                           'human_development_index']].dropna()
    df_test_rates = data[['location',
                          'date',
                          'total_tests_per_thousand',
                          'human_development_index']].dropna()
    max_death_rates = df_death_rates.groupby('location')[
                                           'total_deaths_per_million'].max()
    max_test_rates = df_test_rates.groupby('location')[
                                           'total_tests_per_thousand'].max()
    df_unique_countries_dr = df_death_rates.drop_duplicates(
                                                        subset=['location'])
    df_unique_countries_tr = df_test_rates.drop_duplicates(subset=['location'])
    df_unique_countries_dr = df_unique_countries_dr[[
                                'location',
                                'total_deaths_per_million',
                                'human_development_index'
                                ]]
    df_unique_countries_tr = df_unique_countries_tr[[
                                'location',
                                'total_tests_per_thousand',
                                'human_development_index'
                                ]]
    hdi_dr = df_unique_countries_dr['human_development_index']
    df_final_dr = pd.DataFrame({
                            'location': df_unique_countries_dr['location'],
                            'total_deaths_per_million': max_death_rates.values,
                            'HDI': hdi_dr})
    hdi_tr = df_unique_countries_tr['human_development_index']
    df_final_tr = pd.DataFrame({
                            'location': df_unique_countries_tr['location'],
                            'total_tests_per_thousand': max_test_rates.values,
                            'HDI': hdi_tr
                            })
    fig1, axs1 = plt.subplots(1)
    sns.regplot(data=df_final_dr,
                ax=axs1,
                x='HDI',
                y='total_deaths_per_million',
                order=3)
    plt.title('Max Mortality Rate of Each Country against HDI')
    fig1.savefig('figures/mortality_rate_vs_hdi.png', bbox_inches='tight')
    fig2, axs2 = plt.subplots(1)
    sns.regplot(data=df_final_tr,
                ax=axs2,
                x='HDI',
                y='total_tests_per_thousand',
                order=3)
    plt.title('Max Death Rate of Each Country against HDI')
    fig2.savefig('figures/test_rate_vs_hdi.png', bbox_inches='tight')
    # print(max_death_rates)
    # print(max_test_rates)
    return df_final_dr['total_deaths_per_million']


def main():
    covid_data = pd.read_csv('owid-covid-data.csv')
    vacc_rate_to_pop(covid_data)
    pop_density_coid_growth_rate(covid_data)
    hdi_vs_mortality_testing_rate(covid_data)


if __name__ == '__main__':
    main()
