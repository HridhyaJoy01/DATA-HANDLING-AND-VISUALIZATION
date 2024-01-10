
import csv
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from matplotlib.gridspec import GridSpec as gsp
from matplotlib.gridspec import GridSpec

def read_data(file_path):
    # Read data from CSV file
    with open(file_path, 'r') as csvfile:
        csv_reader = csv.DictReader(csvfile)
        # Return the entire data
        return list(csv_reader)

def line_plot(data, indicator_to_plot, start_year, end_year, countries_to_plot, ax=None):
    # If ax is not provided, create a new plot
    if ax is None:
        fig, ax = plt.subplots()

    # Create a dictionary to store data for each country
    country_data = {country: {'years': [], 'data': []} for country in countries_to_plot}

    # Extract years and data for the chosen indicator within the specified range
    for i, row in enumerate(data):
        if row['Indicator Name'] == indicator_to_plot and start_year <= int(row['Year']) <= end_year:
            for j, country in enumerate(countries_to_plot):
                country_data[country]['years'].append(int(row['Year']))
                # Assuming the column for the country is the same as the country name
                country_data[country]['data'].append(float(row[country]))
                
    # Plot the data for each country without specifying line styles, markers, or colors
    for j, country in enumerate(countries_to_plot):
        ax.plot(country_data[country]['years'], country_data[country]['data'], label=f'{country}')

    # Add labels and title
    ax.set_xlabel('Year')
    ax.set_ylabel('Value')
    ax.set_title('Line Plot for {}'.format(indicator_to_plot))

    # Add legend to the right side
    ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))

    # If ax was not provided, show the plot
    if not ax:
        plt.show()

    # Return the axis for potential further customization
    return ax

def bar_plot(data, indicator_to_plot, selected_years, countries_to_plot, ax=None):
    # If ax is not provided, create a new plot
    if ax is None:
        fig, ax = plt.subplots(figsize=(12, 8))

    # Create a dictionary to store data for each country and year
    country_year_data = {country: {year: [] for year in selected_years} for country in countries_to_plot}

    # Extract data for the chosen indicator and years
    for row in data:
        if row['Indicator Name'] == indicator_to_plot and int(row['Year']) in selected_years:
            year = int(row['Year'])
            for country in countries_to_plot:
                country_year_data[country][year].append(float(row[country]))


    # Plot the data as a grouped bar chart with new light colors
    bar_width = 0.2  # Adjust the width of the bars

    # Define the positions for each group of bars
    positions = np.arange(len(countries_to_plot)) + 0.5 * (len(selected_years) - 1) * bar_width

    # Define new light colors
    new_colors = ['#7FFFD4', '#FF6347', '#20B2AA', '#BA55D3', '#00FA9A']

    for i, year in enumerate(selected_years):
        # Adjust the positions for each year
        year_positions = positions - 0.5 * (len(selected_years) - 1 - i) * bar_width
        values = np.array([country_year_data[country][year] for country in countries_to_plot])

        ax.bar(year_positions, np.sum(values, axis=1), width=bar_width, label=str(year), color=new_colors[i])

    # Add labels and title
    ax.set_xlabel('Country')
    ax.set_ylabel('Value')
    ax.set_title('Grouped Bar Plot for {} (from 1995 to 2015)'.format(indicator_to_plot))

    # Set x-axis ticks and labels
    ax.set_xticks(positions)
    ax.set_xticklabels(countries_to_plot)

    # Add legend
    ax.legend(title='Year')

    # If ax was not provided, show the plot
    if not ax:
        plt.show()

    # Return the axis for potential further customization
    return ax


def donut_chart(data, indicator_to_plot, year, ax=None, hole_size=0.4, explode=None):
    # If ax is not provided, create a new plot
    if ax is None:
        fig, ax = plt.subplots()

    # Create a dictionary to store data for each country
    country_data = {}

    # Extract data for the chosen indicator and year
    for row in data:
        if row['Indicator Name'] == indicator_to_plot and int(row['Year']) == year:
            for country in row.keys():
                if country != 'Year' and country != 'Indicator Name' and row[country] != '':
                    country_data[country] = float(row[country])

    lighter_colors = ['#7FFFD4', '#FF6347', '#20B2AA', '#BA55D3', '#00FA9A']

    # Extract values and labels from the dictionary
    labels = list(country_data.keys())
    values = list(country_data.values())

    # Explode slices if specified
    if explode:
        explode = [0.1 if country in explode else 0 for country in labels]

    # Plot the data as a pie chart with additional styles
    ax.pie(values, labels=labels, colors=lighter_colors, autopct='%1.1f%%', startangle=90,
           shadow=True, explode=explode, textprops={'fontsize': 10, 'fontweight': 'bold'})

    # Use facecolor instead of color for the circle
    centre_circle = plt.Circle((0, 0), hole_size, facecolor='white', edgecolor='black', linewidth=0.8)
    ax.add_artist(centre_circle)

    # Equal aspect ratio ensures that the pie chart is circular
    ax.axis('equal')

    # Add title
    ax.set_title('Enhanced Donut Chart for {} in {}'.format(indicator_to_plot, year))

    # If ax was not provided, show the plot
    if not ax:
        plt.show()

    # Return the axis for potential further customization
    return ax


def area_plot_visualization(data, indicator_to_plot, start_year, end_year, countries_to_plot, ax=None):
    # If ax is not provided, create a new plot
    if ax is None:
        fig, ax = plt.subplots(figsize=(12, 8))

    # Filter data for the chosen indicator and years
    filtered_data = [row for row in data if row['Indicator Name'] == indicator_to_plot and start_year <= int(row['Year']) <= end_year]


    # Create a dictionary to store data for each source
    sources_data = {source: {'years': [], 'data': []} for source in data[0].keys() if source not in ['Year', 'Indicator Name'] and source in countries_to_plot}

    # Extract years and data for each source
    for row in filtered_data:
        for source in sources_data.keys():
            sources_data[source]['years'].append(int(row['Year']))
            sources_data[source]['data'].append(float(row[source]))

    # Create a list of years
    years = list(set(year for source_data in sources_data.values() for year in source_data['years']))

    # Plot the data as a stacked area plot
    ax.stackplot(years,
                 *[sources_data[c]['data'] for c in countries_to_plot],
                 labels=countries_to_plot)

    # Add labels and title
    ax.set_xlabel('Year')
    ax.set_ylabel('Percentage of Total')
    ax.set_title(f'Stacked Area Plot for {indicator_to_plot} ({start_year} to {end_year})')

    # Add legend
    ax.legend(loc='upper left', bbox_to_anchor=(1, 1))

    # If ax was not provided, show the plot
    if not ax:
        plt.show()

    # Return the axis for potential further customization
    return ax
def create_dashboard(data, countries):
    fig = plt.figure(figsize=(20, 20), facecolor='white')
    fig.text(0.5, 0.92,"Name:Hridhya Joy        StudentId: 22074909",
             ha="center", fontweight='bold', fontsize=15)

    gs = GridSpec(2, 2, hspace=0.4, wspace=0.4)

    # Plot Line Plot in the first subplot (ax1)
    ax1 = plt.subplot(gs[0, 0])
    line_plot(data, 'Urban population (% of total population)', 1995, 2000, countries, ax=ax1)
    ax1.text(0.5, -0.15, """ 1. Urban Population Trend (1995-2000)
    Categorical data details are succinctly conveyed, noting the lowest recorded value
    in India during 1995 (26.607) and the highest in Australia for the same year (84.898), 
    providing concise insights into dataset variability
    """, transform=ax1.transAxes, fontsize=12, ha='center', va='top')
    ax1.set_title('Urban population (% of total population) - 1995 to 2000')

    # Plot Bar Plot in the second subplot (ax2)
    ax2 = plt.subplot(gs[0, 1])
    bar_plot(data, 'Population growth (annual %)', [1995, 2000, 2005, 2010, 2015], countries, ax=ax2)
    ax2.text(0.5, -0.15, """2. Population Growth (1995-2015)
        Italy's gradual ascent from its minimal value in 1995 (0.0016) to Australia's peak 
        in 2010 (1.56) highlights a significant and consistent upward trend observed over the 15-year period.
        """, transform=ax2.transAxes, fontsize=12, ha='center', va='top')

    # Plot Donut Chart in the third subplot (ax3)
    ax3 = plt.subplot(gs[1, 0])
    donut_chart(data, 'Urban population growth (annual %)', 2005, ax=ax3)
    ax3.text(0.5, -0.15, """4. Urban Population Growth (2005)
    In 2005, urban population growth rates varied across countries: 
    China experienced the highest at 3.88%, India showed substantial growth at 2.75%, 
    while Italy had a modest increase at 0.67%. Australia and the United Kingdom demonstrated steady 
    rates of 1.36% and 1.05%, respectively""",
              ha='center', va='center', transform=ax3.transAxes, fontsize=12, color='black')

    # Plot Area Plot in the fourth subplot (ax4)
    ax4 = plt.subplot(gs[1, 1])
    area_plot_visualization(data, 'Cereal yield (kg per hectare)', 1995, 2000, countries, ax=ax4)
    ax4.text(0.5, -0.15, """ 3. Cereal yield (kg per hectare) (1995-2015)
    The Area Plot illustrates Cereal yield from (1995-2015).  India saw rising Cereal yield (2111.7 to 2676.4) 
    hina exhibited significant growth in value of metrics. Italy maintained stable yield.
    Australia showed variable yield decrease. The UK witnessed fluctuating yield in 1995 to 2000 """
        , transform=ax4.transAxes, fontsize=12, ha='center', va='top')
    
    conclusion_text = """ Description: The dashboard encompasses diverse insights into socio-economic facets. 
    The "Urban Population Trend (1995-2000)" highlights categorical variability, ranging from India's 1995 low (26.607)
    to Australia's peak (84.898). The "Population Growth (1995-2015)" plot observes Italy's gradual 
    ascent (0.0016 to 1.56) over 15 years. The "Agriculture (1995-2015)" 
    area Plot reveals nuanced dynamics, including India's rising cereal yield and slight forest expansion,
    China's significant growth, Italy's stability, Australia's variability, and the UK's fluctuations.
    The "Urban Population Growth (2005)" zooms into urbanization, showcasing varied rates across countries. 
    Collectively, these plots unveil comprehensive socio-economic trends with rich insights across countries and time spans."""
    fig.text(0.5, -0.03, conclusion_text, ha='center', fontsize=14, va='center')
    
    fig.suptitle('Global Trends Dashboard: Urbanization, Population Growth, Agricultural Productivity, and Urban Population Growth',
             fontweight='bold', fontsize=20)
        
    plt.tight_layout()
    plt.show()



def main():
    file_path = r"population_df.csv" 
    indicator_to_plot_line = 'Urban population (% of total population)'
    start_year = 1995
    end_year = 2000
    countries = ['India', 'China', 'Italy', 'Australia', 'United Kingdom']

    # Read data from CSV file
    data = read_data(file_path)
    
    indicator_to_plot_bar = 'Population growth (annual %)'
    years_bar = [1995,2000,2005,2010,2015]
    indicator_to_plot_donut= 'Urban population growth (annual %)'
    indicator_to_areaplot= 'Cereal yield (kg per hectare)'
    year_donut = 2005

    # Create individual plots
    line_plot(data, indicator_to_plot_line, start_year, end_year, countries)
    bar_plot(data, indicator_to_plot_bar, years_bar, countries)
    donut_chart(data, indicator_to_plot_donut, year_donut)
    area_plot_visualization(data, indicator_to_areaplot, start_year, end_year, countries)

    create_dashboard(data, countries)

if __name__ == '__main__':
    main()
