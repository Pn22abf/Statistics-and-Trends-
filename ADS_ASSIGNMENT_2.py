
"""the python modules which help in data analysis for 
   ploting required comparing graphs along with the heatmap 
 
 """

# necessary imports
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


# initial data for analysis

# Countries and years for analysis

countries = ["Canada",'Belgium','Algeria','Japan','France',"Kuwait"]

years = ["1991","1996","2001", "2006", "2011", "2016"]

# read the csv file
main_dataframe = pd.read_csv("World_bank_data.csv")

"""defining the function to read the CSV file in the mata data format and 
   then Transpose the CSV file to get the required rows and cloumns to 
   access the datato plot countries and years with the required indicators
""" 

def countries_years(file_name):
    """This function takes a filename as argument, reads a dataframe in World bank format
    and returns two dataframes:one with years as columns and one with countries as columns."""

    # read the csv file
    read_data = pd.read_csv(file_name)


    country_columns = read_data.set_index("Country Name").transpose()

    # get the columns data from index 3
    columns_data = read_data.columns[3:]

    # set the index as Country Name and filter the dataframe with given columns data
    years_columns = read_data.set_index("Country Name")
    years_columns = years_columns.loc[:, columns_data]

    return country_columns, years_columns


country_as_columns, years__as_columns = countries_years(
    file_name="World_bank_data.csv"
)
print(country_as_columns, years__as_columns)



def plotting_data(indicator_name):
    """This function takes indicator name as argument, It plots the bar graph for the dataframe and
    returns the filtered dataframe for the indicator with given countries and years"""

    if indicator_name == "Total greenhouse gas emissions (kt of CO2 equivalent)":
        label = "kt of CO2 equivalent"
    elif indicator_name == "Agricultural land (% of land area)":
        label = "% of land area"
    elif indicator_name == "Electricity production from natural gas sources (% of total)":
        label = "% of total"

    # filter the dataframe with given countries and indicator name and set the index as Country Name.
    selected_data = main_dataframe[
        (main_dataframe["Country Name"].isin(countries))
        & (main_dataframe["Indicator Name"] == indicator_name)
    ].set_index("Country Name")

    # filter the dataframe with given years and reset the index
    refined_df = selected_data.loc[:, years].reset_index()
    # plt.legend(bbox_to_anchor=(1.0, 1.0))
    refined_df.set_index("Country Name").plot.bar(
        rot=0, xlabel="Countries", ylabel=label, title=indicator_name
    )

    return refined_df


#
plotting_data("Total greenhouse gas emissions (kt of CO2 equivalent)")
plotting_data("Agricultural land (% of land area)")
plotting_data("Electricity production from natural gas sources (% of total)")

# driver code for plotting_data function
collected_data = plotting_data(indicator_name="Agricultural land (% of land area)")
plotting_data(indicator_name="Electricity production from natural gas sources (% of total)")


def mean_stats():
    """This function plots the graph for Electricity production from oil
    source with hydroelectric dependency with the help ofpandas statistical
    function mean()"""

    # mean of the population growth
    mean_series = collected_data.max(numeric_only=True)
    mean_data = pd.DataFrame({"Years": years, "yeild rate (agric)": mean_series})
    mean_data.set_index("Years").plot(
        rot=0, title="Impact of Natural Gas-Based power Generation on Agricultural Land Usage",color="green"
    )


# driver code for mean_stats function
mean_stats()



def plot_corr(country_name):
    """This function takes the Country Name as argument and cross compare
    the correlations between different indicators of the Country and plot the heatmap"""

    # filter the dataframe with given country name
    country_data = main_dataframe[main_dataframe["Country Name"] == country_name]

    # list of indicators for the country
    indicator_names = [
        "Total greenhouse gas emissions (kt of CO2 equivalent)",
        "Population, total",
        "CO2 emissions (kt)",
        "Electric power consumption (kWh per capita)",
        "Agricultural land (sq. km)",
        "Electricity production from natural gas sources (% of total)",
    ]

    # set the index as Indicator Name and filter the dataframe with given indicator names and years
    country_data_indicator = country_data.set_index("Indicator Name")

    # extract the data for the given years and indicator names and transpose the dataframe
    extracted_data_t = country_data_indicator.loc[indicator_names, years].transpose()
    

    # plot the heatmap for the correlation between different indicators
    plt.title(country_name, fontsize=20)
    sns.heatmap(extracted_data_t.corr(), linecolor='white',
                linewidths=0.1, annot=True, cmap="Accent",)
    return extracted_data_t

#calling function for corelation
plot_corr("Algeria")
plot_corr("Kuwait")

