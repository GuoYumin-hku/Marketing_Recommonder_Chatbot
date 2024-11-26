# save the upper text analysis into a jsonl file
# keep the structure of dictionary
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import json

# data loading and preprocessing
data_og = pd.read_csv('../data/Sample_Superstore.csv', on_bad_lines='skip')
data_og['Combined_Category'] = data_og['Category'].astype(str) + '-' + data_og['Sub-Category'].astype(str)


def discount_group(discount):
    if discount == 0:
        return '0'
    elif 0.1 <= discount < 0.2:
        return '10%-20%'
    elif 0.2 <= discount < 0.3:
        return '20%-30%'
    elif 0.3 <= discount < 0.4:
        return '30%-40%'
    elif 0.4 <= discount < 0.5:
        return '40%-50%'
    else:
        return '>=50%'


# Assume we are going to analysis the item which has 'combined_category' as 'Furniture-Bookcases'

# filter the data##################################
for y1 in list(set(data_og['Combined_Category'])):
    print(y1)
    if not os.path.exists('./analysis_result_{}'.format(y1)):
        os.makedirs('./analysis_result_{}'.format(y1))
    data = data_og[data_og['Combined_Category'] == y1]
    # analyze the segment distribution and save in dictionary in both number and percentage
    segment_distribution = data['Segment'].value_counts().to_dict()
    segment_distribution = {k: (v, round(v / len(data), 2)) for k, v in segment_distribution.items()}
    # print("The segment distribution of item '{}' is: {}".format(y1, segment_distribution))

    # analyze the difference of average quantity between the segment, round to 2 decimal
    segment_quantity = data.groupby('Segment')['Quantity'].mean().to_dict()
    segment_quantity = {k: round(v, 2) for k, v in segment_quantity.items()}
    # print("The average quantity of item bought by each segment is: {}".format(segment_quantity))

    # analyze the average unit price; profit; discount of each segment, round to 2 decimal
    # unit price = sales / quantity
    segment_unit_price = data.groupby('Segment')['Sales'].sum() / data.groupby('Segment')['Quantity'].sum()
    segment_unit_price = segment_unit_price.to_dict()
    segment_unit_price = {k: round(v, 2) for k, v in segment_unit_price.items()}
    # print("The average unit price of item bought by each segment is: {}".format(segment_unit_price))

    # mean profit = profit / quantity
    segment_profit = data.groupby('Segment')['Profit'].sum() / data.groupby('Segment')['Quantity'].sum()
    segment_profit = segment_profit.to_dict()
    segment_profit = {k: round(v, 2) for k, v in segment_profit.items()}
    # print("The average profit of item bought by each segment is: {}".format(segment_profit))

    # discount
    segment_discount = data.groupby('Segment')['Discount'].mean()
    segment_discount = segment_discount.to_dict()
    segment_discount = {k: round(v, 2) for k, v in segment_discount.items()}
    # print("The average discount of item bought by each segment is: {}".format(segment_discount))

    # analyze the region distribution and save in dictionary in both number and percentage
    region_distribution = data['Region'].value_counts().to_dict()
    region_distribution = {k: (v, round(v / len(data), 2)) for k, v in region_distribution.items()}
    # print("The region distribution of item '{}' is: {}".format(y1, region_distribution))

    # analyze the Ship Mode distribution and save in dictionary in both number and percentage
    ship_mode_distribution = data['Ship Mode'].value_counts().to_dict()
    ship_mode_distribution = {k: (v, round(v / len(data), 2)) for k, v in ship_mode_distribution.items()}
    # print("The Ship Mode distribution of item '{}' is: {}".format(y1, ship_mode_distribution))

    # analyze the Ship Speed distribution and save in dictionary in both number and percentage
    # ship speed = ship date - order date
    data['Ship Date'] = pd.to_datetime(data['Ship Date'])
    data['Order Date'] = pd.to_datetime(data['Order Date'])
    data['Ship Speed'] = data['Ship Date'] - data['Order Date']
    data['Ship Speed'] = data['Ship Speed'].dt.days
    ship_speed_distribution = data['Ship Speed'].value_counts().to_dict()
    ship_speed_distribution = {k: (v, round(v / len(data), 2)) for k, v in ship_speed_distribution.items()}

    # sort by keys
    ship_speed_distribution = dict(sorted(ship_speed_distribution.items()))
    # print("The Ship Days distribution of item '{}' is: {}".format(y1, ship_speed_distribution))

    ## Rgion level analysis
    # analyze the average quantity; sale; unit price; profit; discount; profit margin of each region, round to 2 decimal
    region_quantity = data.groupby('Region')['Quantity'].mean()
    region_quantity = region_quantity.to_dict()
    region_quantity = {k: round(v, 2) for k, v in region_quantity.items()}

    region_sales = data.groupby('Region')['Sales'].mean()
    region_sales = region_sales.to_dict()
    region_sales = {k: round(v, 2) for k, v in region_sales.items()}

    region_unit_price = data.groupby('Region')['Sales'].sum() / data.groupby('Region')['Quantity'].sum()
    region_unit_price = region_unit_price.to_dict()
    region_unit_price = {k: round(v, 2) for k, v in region_unit_price.items()}

    region_discount = data.groupby('Region')['Discount'].mean()
    region_discount = region_discount.to_dict()
    region_discount = {k: round(v, 2) for k, v in region_discount.items()}

    region_profit = data.groupby('Region')['Profit'].sum() / data.groupby('Region')['Quantity'].sum()
    region_profit = region_profit.to_dict()
    region_profit = {k: round(v, 2) for k, v in region_profit.items()}

    region_profit_margin = data.groupby('Region')['Profit'].sum() / data.groupby('Region')['Sales'].sum()
    region_profit_margin = region_profit_margin.to_dict()
    region_profit_margin = {k: round(v, 2) for k, v in region_profit_margin.items()}

    # print("The average quantity of item per order in each region is: {}".format(region_quantity))
    # print("The average sales of item per order in each region is: {}".format(region_sales))
    # print("The average unit price of item in each region is: {}".format(region_unit_price))
    # print("The average discount of item per order in each region is: {}".format(region_discount))
    # print("The average profit of item in each region is: {}".format(region_profit))
    # print("The average profit margin of item in each region is: {}".format(region_profit_margin))

    ## Country level analysis
    # analyze the country distribution and save in dictionary in both number and percentage
    country_distribution = data['Country'].value_counts().to_dict()
    country_distribution = {k: (v, round(v / len(data), 2)) for k, v in country_distribution.items()}
    print("The country distribution of item '{}' is: {}".format(y1, country_distribution))

    # analyze the average quantity; sale; unit price; profit; profit margin of each country, round to 2 decimal, list the top 10 countries 
    country_quantity = data.groupby('Country')['Quantity'].mean().to_dict()
    country_quantity = {k: round(v, 2) for k, v in country_quantity.items()}
    country_quantity = dict(sorted(country_quantity.items(), key=lambda x: x[1], reverse=True))
    country_quantity_top_10 = dict(list(country_quantity.items())[:10])

    country_sales = data.groupby('Country')['Sales'].mean().to_dict()
    country_sales = {k: round(v, 2) for k, v in country_sales.items()}
    country_sales = dict(sorted(country_sales.items(), key=lambda x: x[1], reverse=True))
    country_sales_top_10 = dict(list(country_sales.items())[:10])

    country_unit_price = data.groupby('Country')['Sales'].sum() / data.groupby('Country')['Quantity'].sum()
    country_unit_price = country_unit_price.to_dict()
    country_unit_price = {k: round(v, 2) for k, v in country_unit_price.items()}
    country_unit_price = dict(sorted(country_unit_price.items(), key=lambda x: x[1], reverse=True))
    country_unit_price_top_10 = dict(list(country_unit_price.items())[:10])

    country_profit = data.groupby('Country')['Profit'].sum() / data.groupby('Country')['Quantity'].sum()
    country_profit = country_profit.to_dict()
    country_profit = {k: round(v, 2) for k, v in country_profit.items()}
    country_profit = dict(sorted(country_profit.items(), key=lambda x: x[1], reverse=True))
    country_profit_top_10 = dict(list(country_profit.items())[:10])

    country_profit_margin = data.groupby('Country')['Profit'].sum() / data.groupby('Country')['Sales'].sum()
    country_profit_margin = country_profit_margin.to_dict()
    country_profit_margin = {k: round(v, 2) for k, v in country_profit_margin.items()}
    country_profit_margin = dict(sorted(country_profit_margin.items(), key=lambda x: x[1], reverse=True))
    country_profit_margin_top_10 = dict(list(country_profit_margin.items())[:10])

    # print("The top 10 countries with highest average quantity of item per order is: {}".format(country_quantity_top_10))
    # print("The top 10 countries with highest average sales of item per order is: {}".format(country_sales_top_10))
    # print("The top 10 countries with highest average unit price of item is: {}".format(country_unit_price_top_10))
    # print("The top 10 countries with highest average profit of item is: {}".format(country_profit_top_10))
    # print("The top 10 countries with highest average profit margin of item is: {}".format(country_profit_margin_top_10))

    ## discount analysis
    # divide the discount into 6 group based on the value: 0, 10%-20%, 20%-30%, 30%-40%, 40%-50%, >50%, match the label to the group

    data['Discount_Group'] = data['Discount'].apply(discount_group)

    # analyze the discount distribution and save in dictionary
    discount_distribution = data['Discount_Group'].value_counts().to_dict()
    discount_distribution = {k: (v, round(v / len(data), 2)) for k, v in discount_distribution.items()}
    print("The discount distribution of item '{}' is: {}".format(y1, discount_distribution))

    # analyze the percentage of discount group in each segement, save in dictionary in both number and percentage
    segment_discount_distribution = data.groupby('Segment')['Discount_Group'].value_counts().unstack().T
    segment_discount_distribution = segment_discount_distribution.fillna(0).astype(int).to_dict()
    segment_discount_distribution_percentage = {}
    for k, v in segment_discount_distribution.items():
        total = sum(v.values())
        v_percentage = {kk: (vv, round(vv / total, 2)) for kk, vv in v.items()}
        segment_discount_distribution_percentage[k] = v_percentage

    # print("The discount distribution of item '{}' in each segment is: {}".format(y1, segment_discount_distribution_percentage))

    # analyze the average quantity; sale; profit; unit price; profit margin of each discount group, round to 2 decimal
    discount_quantity = data.groupby('Discount_Group')['Quantity'].mean().to_dict()
    discount_quantity = {k: round(v, 2) for k, v in discount_quantity.items()}
    discount_sales = data.groupby('Discount_Group')['Sales'].mean().to_dict()
    discount_sales = {k: round(v, 2) for k, v in discount_sales.items()}
    discount_profit = data.groupby('Discount_Group')['Profit'].mean().to_dict()
    discount_profit = {k: round(v, 2) for k, v in discount_profit.items()}
    discount_unit_price = data.groupby('Discount_Group')['Sales'].sum() / data.groupby('Discount_Group')[
        'Quantity'].sum()
    discount_unit_price = discount_unit_price.to_dict()
    discount_unit_price = {k: round(v, 2) for k, v in discount_unit_price.items()}
    discount_profit_margin = data.groupby('Discount_Group')['Profit'].sum() / data.groupby('Discount_Group')[
        'Sales'].sum()
    discount_profit_margin = discount_profit_margin.to_dict()
    discount_profit_margin = {k: round(v, 2) for k, v in discount_profit_margin.items()}

    # print("The average quantity of item per order in each discount group is: {}".format(discount_quantity))
    # print("The average sales of item per order in each discount group is: {}".format(discount_sales))
    # print("The average profit of item in each discount group is: {}".format(discount_profit))
    # print("The average unit price of item in each discount group is: {}".format(discount_unit_price))
    # print("The average profit margin of item in each discount group is: {}".format(discount_profit_margin))

    ### Time
    # filter the data
    # Quantity
    # Extract quarterly information
    data['Quarter'] = data['Order Date'].dt.quarter
    # Quarterly sales statistics
    # Map quarter to season name
    quarter_map = {1: 'Spring', 2: 'Summer', 3: 'Autumn', 4: 'Winter'}

    seasonal_quantity = data.groupby(['Quarter'])['Quantity'].sum()
    seasonal_quantity = seasonal_quantity.to_dict()
    seasonal_quantity = {quarter_map[k]: round(v, 2) for k, v in seasonal_quantity.items()}
    # print("The sum quantity of each season by {} is: {}".format(y1,seasonal_quantity))

    # Extract year and quarter information
    data['Year'] = data['Order Date'].dt.year
    # Statistics of sales by year and quarter
    year_seasonal_quantity = data.groupby(['Year', 'Quarter'])['Quantity'].sum()
    year_seasonal_quantity = year_seasonal_quantity.to_dict()
    year_seasonal_quantity = {f"{k[0]}{quarter_map[k[1]]}": round(v, 2) for k, v in year_seasonal_quantity.items()}
    # print("The sum quantity of each season each year by {} is: {}".format(y1,year_seasonal_quantity))

    # Sales
    # Calculate the total sales revenue by quarter
    seasonal_sales = data.groupby(['Quarter'])['Sales'].sum()
    seasonal_sales = seasonal_sales.to_dict()
    seasonal_sales = {quarter_map[k]: round(v, 2) for k, v in seasonal_sales.items()}
    # print("The sum sales of each season by {} is: {}".format(y1,seasonal_sales))

    # Statistics of sales by year and quarter
    year_seasonal_sales = data.groupby(['Year', 'Quarter'])['Sales'].sum()
    year_seasonal_sales = year_seasonal_sales.to_dict()
    year_seasonal_sales = {f"{k[0]}{quarter_map[k[1]]}": round(v, 2) for k, v in year_seasonal_sales.items()}
    # print("The sum sales of each season each year by {} is: {}".format(y1,year_seasonal_sales))

    # Quarterly sales/sales ratio
    data['Sales_Ratio'] = data['Sales'] / data['Quantity']

    # View the ratio of sales volume to sales volume by quarter
    sales_ratio_by_quarter = data.groupby(['Quarter'])['Sales_Ratio'].mean()
    sales_ratio_by_quarter = sales_ratio_by_quarter.to_dict()
    sales_ratio_by_quarter = {quarter_map[k]: round(v, 2) for k, v in sales_ratio_by_quarter.items()}
    # print("The sales ratio by quarter season of {} is: {}".format(y1,sales_ratio_by_quarter))

    # profit
    seasonal_profit = data.groupby(['Quarter'])['Profit'].sum()
    seasonal_profit = seasonal_profit.to_dict()
    seasonal_profit = {quarter_map[k]: round(v, 2) for k, v in seasonal_profit.items()}
    # print("The sum profit of each season by {} is: {}".format(y1,seasonal_profit))

    year_seasonal_profit = data.groupby(['Year', 'Quarter'])['Profit'].sum()
    year_seasonal_profit = year_seasonal_profit.to_dict()
    year_seasonal_profit = {f"{k[0]}{quarter_map[k[1]]}": round(v, 2) for k, v in year_seasonal_profit.items()}
    # print("The sum profit of each season each year by {} is: {}".format(y1,year_seasonal_profit))

    # profit/sales
    data['profit_ratio_by_sales'] = data['Profit'] / data['Sales']
    seasonal_profit_ratio_by_sales = data.groupby(['Quarter'])['profit_ratio_by_sales'].sum()
    seasonal_profit_ratio_by_sales = seasonal_profit_ratio_by_sales.to_dict()
    seasonal_profit_ratio_by_sales = {quarter_map[k]: round(v, 2) for k, v in seasonal_profit_ratio_by_sales.items()}
    # print("The profit ratio by sales of each season by {} is: {}".format(y1,seasonal_profit_ratio_by_sales))

    # analyze the state distribution and save in dictionary in both number and percentage
    state_distribution = data['State'].value_counts().to_dict()
    state_distribution = {k: (v, round(v / len(data), 2)) for k, v in state_distribution.items()}
    # print("The state distribution of item '{}' is: {}".format(y1, state_distribution))
    # Extract the number of purchases for the top 10 states
    top_10_states = dict(list(state_distribution.items())[:10])
    top_10_states_values = [v[0] for v in top_10_states.values()]

    # Draw the top 10 states distribution in a bar plot
    plt.figure(figsize=(12, 6))
    plt.bar(top_10_states.keys(), top_10_states_values)
    plt.xlabel('State')
    plt.ylabel('Number of Purchase')
    plt.title('Top 10 state distribution of item {}'.format(y1))
    for i, v in enumerate(top_10_states_values):
        plt.text(i, v, str(v), ha='center', va='bottom')

    plt.xticks(rotation=45)
    # plt.show()
    # save plot
    plt.savefig('./analysis_result_{}/top_10_states_distribution_{}.png'.format(y1, y1))

    # analyze the city distribution and save in dictionary in both number and percentage
    city_distribution = data['City'].value_counts().to_dict()
    city_distribution = {k: (v, round(v / len(data), 2)) for k, v in city_distribution.items()}
    # print("The city distribution of item '{}' is: {}".format(y1, city_distribution))
    # Extract the number of purchases for the top 10 cities
    top_10_cities = dict(list(city_distribution.items())[:10])
    top_10_cities_values = [v[0] for v in top_10_cities.values()]
    # print(top_10_cities)

    # Draw the top 10 cities distribution in a bar plot with the value on the top of each bar
    plt.figure(figsize=(12, 6))
    plt.bar(top_10_cities.keys(), top_10_cities_values)
    plt.xlabel('City')
    plt.ylabel('Number of Purchase')
    plt.title('Top 10 city distribution of item {}'.format(y1))
    for i, v in enumerate(top_10_cities_values):
        plt.text(i, v, str(v), ha='center', va='bottom')
    plt.xticks(rotation=45)
    # plt.show()
    # save plot
    plt.savefig('./analysis_result_{}/top_10_cities_distribution_{}.png'.format(y1, y1))

    # Mapping U.S. State Profits
    # Mapping complete state names to two-letter abbreviations
    state_abbreviations = {
        'Alabama': 'AL', 'Alaska': 'AK', 'Arizona': 'AZ', 'Arkansas': 'AR', 'California': 'CA',
        'Colorado': 'CO', 'Connecticut': 'CT', 'Delaware': 'DE', 'Florida': 'FL', 'Georgia': 'GA',
        'Hawaii': 'HI', 'Idaho': 'ID', 'Illinois': 'IL', 'Indiana': 'IN', 'Iowa': 'IA',
        'Kansas': 'KS', 'Kentucky': 'KY', 'Louisiana': 'LA', 'Maine': 'ME', 'Maryland': 'MD',
        'Massachusetts': 'MA', 'Michigan': 'MI', 'Minnesota': 'MN', 'Mississippi': 'MS',
        'Missouri': 'MO', 'Montana': 'MT', 'Nebraska': 'NE', 'Nevada': 'NV', 'New Hampshire': 'NH',
        'New Jersey': 'NJ', 'New Mexico': 'NM', 'New York': 'NY', 'North Carolina': 'NC',
        'North Dakota': 'ND', 'Ohio': 'OH', 'Oklahoma': 'OK', 'Oregon': 'OR', 'Pennsylvania': 'PA',
        'Rhode Island': 'RI', 'South Carolina': 'SC', 'South Dakota': 'SD', 'Tennessee': 'TN',
        'Texas': 'TX', 'Utah': 'UT', 'Vermont': 'VT', 'Virginia': 'VA', 'Washington': 'WA',
        'West Virginia': 'WV', 'Wisconsin': 'WI', 'Wyoming': 'WY'
    }
    us_states_full = list(state_abbreviations.keys())
    us_state_profit = data[data['State'].isin(us_states_full)].groupby('State')['Profit'].sum().reset_index()
    us_state_profit['State'] = us_state_profit['State'].map(state_abbreviations)

    # Map
    fig = px.choropleth(
        us_state_profit,
        locations='State',
        locationmode='USA-states',
        color='Profit',
        color_continuous_scale='Blues',
        scope='usa',
        title=f'Profit by US State for item {y1}',
        labels={'Profit': 'Total Profit'}
    )
    # Customize Hover Content
    fig.update_traces(
        hovertemplate="<b>%{location}</b><br>Total Profit: %{z:$,.2f}<extra></extra>"
    )
    fig.show()

    # Save the HTML file
    output_file = './analysis_result_{}/US_state_profit_map.html'.format(y1, y1)
    fig.write_html(output_file, include_plotlyjs='cdn')
    print(f"US_State profit map saved to: {output_file}")

    # Analyze monthly sales by grouping data by year and month
    style1 = Style(
        background='white',
        plot_background='white',
        foreground='#000000',
        foreground_strong='#0F52BA',
        foreground_subtle='#4682B4',
        colors=('#0F52BA', '#4682B4', '#5F9EA0', '#87CEFA')
    )
    data['YearMonth'] = data['Order Date'].dt.to_period('M')
    sales_by_month = data.groupby('YearMonth')['Sales'].sum()

    # Prepare data for pygal visualization
    months = sales_by_month.index.astype(str).tolist()
    sales = sales_by_month.values.tolist()

    # Draw the monthly sales trend line chart using pygal
    line_chart = pygal.Line(
        style=style1,
        x_label_rotation=45,
        show_minor_x_labels=True,
        dots_size=6,
        title_font_size=20,
        label_font_size=14,
        major_label_font_size=14,
        legend_at_bottom=True
    )
    line_chart.title = 'Sales Amount Over Time for Item {}'.format(y1)
    line_chart.x_labels = months
    line_chart.add('Monthly Sales', sales)

    # Save and display the chart
    output_file = './analysis_result_{}/sales_over_time_{}.svg'.format(y1, y1)
    line_chart.render_to_file(output_file)

    # rendered_chart = line_chart.render(is_unicode=True)
    # html_output = base_html.format(rendered_chart=rendered_chart)
    # display(HTML(html_output))

    # Seasonal Analysis Portfolio Chart
    # Prepare seasonal data
    seasons = list(seasonal_sales.keys())  # Seasons: Spring, Summer, Autumn, Winter
    sales = list(seasonal_sales.values())
    quantity = list(seasonal_quantity.values())
    profit = list(seasonal_profit.values())
    sales_ratio = list(sales_ratio_by_quarter.values())
    profit_ratio_by_sales = list(seasonal_profit_ratio_by_sales.values())

    # Create grid layout 
    fig, axes = plt.subplots(2, 3, figsize=(20, 12))  # 2 rows, 3 columns
    fig.suptitle('Sales Amount Over Time for Item {}'.format(y1), fontsize=20, color='#4682B4', weight='bold')

    # Chart 1: Seasonal Sales
    axes[0, 0].bar(seasons, sales, color='#4682B4', alpha=0.8, edgecolor='black')
    axes[0, 0].set_title('Seasonal Sales', fontsize=16, color='#4682B4')
    axes[0, 0].set_xlabel('Season', fontsize=12)
    axes[0, 0].set_ylabel('Sales', fontsize=12)
    axes[0, 0].grid(axis='y', linestyle='--', alpha=0.7)
    for i, value in enumerate(sales):
        y_position = min(value + 5000, axes[0, 0].get_ylim()[1] - 5000)
        axes[0, 0].text(i, y_position, f'{value:,.0f}', ha='center', fontsize=10, color='black')

    # Chart 2: Seasonal Quantity
    axes[0, 1].bar(seasons, quantity, color='#5F9EA0', alpha=0.8, edgecolor='black')
    axes[0, 1].set_title('Seasonal Quantity', fontsize=16, color='#5F9EA0')
    axes[0, 1].set_xlabel('Season', fontsize=12)
    axes[0, 1].set_ylabel('Quantity', fontsize=12)
    axes[0, 1].grid(axis='y', linestyle='--', alpha=0.7)
    for i, value in enumerate(quantity):
        y_position = min(value + 100, axes[0, 1].get_ylim()[1] - 100)
        axes[0, 1].text(i, y_position, f'{value:,.0f}', ha='center', fontsize=10, color='black')

    # Chart 3: Seasonal Profit
    axes[0, 2].bar(seasons, profit, color='#87CEFA', alpha=0.8, edgecolor='black')
    axes[0, 2].set_title('Seasonal Profit', fontsize=16, color='#87CEFA')
    axes[0, 2].set_xlabel('Season', fontsize=12)
    axes[0, 2].set_ylabel('Profit', fontsize=12)
    axes[0, 2].grid(axis='y', linestyle='--', alpha=0.7)
    for i, value in enumerate(profit):
        y_position = min(value + 1500, axes[0, 2].get_ylim()[1] - 1500)
        axes[0, 2].text(i, y_position, f'{value:,.0f}', ha='center', fontsize=10, color='black')

    # Chart 4: Sales-to-Quantity Ratio
    axes[1, 0].plot(seasons, sales_ratio, marker='o', color='#4682B4', linewidth=2)
    axes[1, 0].set_title('Sales-to-Quantity Ratio', fontsize=16, color='#4682B4')
    axes[1, 0].set_xlabel('Season', fontsize=12)
    axes[1, 0].set_ylabel('Ratio', fontsize=12)
    axes[1, 0].grid(axis='both', linestyle='--', alpha=0.7)
    for i, value in enumerate(sales_ratio):
        y_position = max(value - 1, axes[1, 0].get_ylim()[0] + 1)
        axes[1, 0].text(i, y_position, f'{value:.1f}', ha='center', fontsize=10, color='black')

    # Chart 5: Profit-to-Sales Ratio
    axes[1, 1].plot(seasons, profit_ratio_by_sales, marker='o', color='#5F9EA0', linewidth=2)
    axes[1, 1].set_title('Profit-to-Sales Ratio', fontsize=16, color='#5F9EA0')
    axes[1, 1].set_xlabel('Season', fontsize=12)
    axes[1, 1].set_ylabel('Ratio', fontsize=12)
    axes[1, 1].grid(axis='both', linestyle='--', alpha=0.7)
    for i, value in enumerate(profit_ratio_by_sales):
        y_position = min(value + 2, axes[1, 1].get_ylim()[1] - 2)
        axes[1, 1].text(i, y_position, f'{value:.1f}', ha='center', fontsize=10, color='black')

    # Hide the last empty subplot
    axes[1, 2].axis('off')

    # Adjust layout to avoid overlap
    plt.subplots_adjust(hspace=0.5, wspace=0.3)
    plt.savefig('./analysis_result_{}/Seasonal_Analysis_{}.png'.format(y1, y1))
    plt.show()

    # Draw the combined Discount vs Average Sales Volume and Average Profit plot with dual Y-axes
    style2 = Style(
        background='white',
        plot_background='white',
        foreground='black',
        foreground_strong='black',
        foreground_subtle='#630C0D',
        colors=('#0F52BA', '#B22222')
    )
    discount_levels = list(discount_quantity.keys())  # Discount groups (0, 10%-20%, etc.)
    avg_sales_volumes = list(discount_quantity.values())  # Average quantity per discount group
    avg_profit = list(discount_profit.values())  # Average profit per discount group
    profit_margin = list(discount_profit_margin.values())  # Average profit margin per discount group

    # Prepare data for Pygal (convert discount groups to string for better labeling)
    discounts = [str(d) for d in discount_levels]  # Convert discount levels to strings for x-axis labels

    # Create a dual-axis chart using pygal
    dual_axis_chart = pygal.Line(
        style=style2,
        x_label_rotation=45,
        show_minor_x_labels=False,
        dots_size=6,
        title_font_size=20,
        label_font_size=14,
        major_label_font_size=14,
        legend_at_bottom=True
    )

    dual_axis_chart.title = 'Discount vs Average Sales Volume and Average Profit for item {}'.format(y1)
    dual_axis_chart.x_labels = discounts

    # Add the first Y-axis (Average Sales Volume)
    dual_axis_chart.add('Average Sales Volume', avg_sales_volumes)
    # Add the second Y-axis (Average Profit)
    dual_axis_chart.add('Average Profit', avg_profit, secondary=True)
    # Add the third Y-axis (Average Profit Margin)
    dual_axis_chart.add('Average Profit Margin', profit_margin, secondary=True)

    # Save the chart as an SVG file
    output_file = './analysis_result_{}/discount_vs_avg_sales_volumes_and_profit_{}.svg'.format(y1, y1)
    dual_axis_chart.render_to_file(output_file)
    print("Chart saved to: {}".format(output_file))

    # Display the chart dynamically in Jupyter Notebook
    # rendered_chart = dual_axis_chart.render(is_unicode=True)
    # html_output = base_html.format(rendered_chart=rendered_chart)
    # display(HTML(html_output))

    # Analyze average unit price, profit, and discount by segment
    style3 = Style(
        background='white',
        plot_background='white',
        foreground='black',
        foreground_strong='black',
        foreground_subtle='#630C0D',
        colors=('#4682B4', '#8B0000', '#32CD32')
    )

    # Prepare data for the grouped bar chart
    labels = list(segment_unit_price.keys())  # Segment labels
    unit_price_values = list(segment_unit_price.values())
    profit_values = list(segment_profit.values())
    discount_values = [v * 100 for v in segment_discount.values()]  # Scale discount values by 10 for better visibility

    # Add a note for scaled discount values
    print("Note: Discount values scaled by 100 for better visualization.")

    # Calculate dynamic y-axis range to ensure visibility of all data
    max_value = max(max(unit_price_values), max(profit_values), max(discount_values))
    min_value = min(min(profit_values), min(discount_values))
    y_range_padding = (max_value - min_value) * 0.2
    y_range_max = max_value + y_range_padding
    y_range_min = min_value - y_range_padding

    # Create a grouped bar chart using pygal
    grouped_bar_chart = pygal.Bar(
        style=style3,
        x_label_rotation=0,
        title_font_size=24,
        label_font_size=16,
        major_label_font_size=14,
        legend_at_bottom=True,
        range=(y_range_min, y_range_max),
        show_x_labels=True
    )

    # Set chart title and x-axis labels
    grouped_bar_chart.title = 'Average Unit Price, Profit, and Discount by Segment for item {}'.format(y1)
    grouped_bar_chart.x_labels = labels

    # Add data to the chart
    grouped_bar_chart.add('Unit Price', unit_price_values)
    grouped_bar_chart.add('Profit', profit_values)
    grouped_bar_chart.add('Discount (scaled x100)', discount_values)

    # Save the chart as an SVG file
    output_file = './analysis_result_{}/unit_price_profit_discount_by_segment_{}.svg'.format(y1, y1)
    grouped_bar_chart.render_to_file(output_file)
    print("Chart saved to: {}".format(output_file))

    # Dynamically display the chart in Jupyter Notebook
    # rendered_chart = grouped_bar_chart.render(is_unicode=True)
    # html_output = base_html.format(rendered_chart=rendered_chart)
    # display(HTML(html_output))

    # Analyze the Ship Mode distribution in both number and percentage
    ship_mode_style = Style(
        background='white',
        plot_background='white',
        foreground='black',
        foreground_strong='black',
        foreground_subtle='#333333',
        colors=('#B22222', '#6B8E23', '#4682B4', '#FFD700')  # Bright and distinguishable colors
    )

    ship_mode_distribution = data['Ship Mode'].value_counts().to_dict()
    ship_mode_distribution = {k: (v, round(v / len(data), 2)) for k, v in ship_mode_distribution.items()}
    print("The Ship Mode distribution of item '{}' is: {}".format(y1, ship_mode_distribution))

    # Prepare data for the pie chart
    ship_mode_labels = list(ship_mode_distribution.keys())
    ship_mode_values = [v[0] for v in ship_mode_distribution.values()]  # Number of orders
    ship_mode_percentages = [v[1] * 100 for v in ship_mode_distribution.values()]  # Percentages for labels

    # Use Pygal to create a pie chart
    pie_chart = pygal.Pie(
        style=ship_mode_style,
        title_font_size=20,
        legend_at_bottom=True,
        inner_radius=0.3  # Donut style for better visualization
    )

    # Add data to the pie chart
    pie_chart.title = 'Ship Mode Distribution of item {}'.format(y1)
    for label, value, percentage in zip(ship_mode_labels, ship_mode_values, ship_mode_percentages):
        pie_chart.add(f"{label} ({percentage:.1f}%)", value)

    # Save the chart as an SVG file
    output_file = './analysis_result_{}/ship_mode_distribution_{}.svg'.format(y1, y1)
    pie_chart.render_to_file(output_file)
    print("Chart saved to: {}".format(output_file))

    # Dynamically display the chart in Jupyter Notebook
    # rendered_chart = pie_chart.render(is_unicode=True)
    # html_output = base_html.format(rendered_chart=rendered_chart)
    # display(HTML(html_output))

    with open('./analysis_result_{}/analysis_result_{}.json'.format(y1, y1), 'w') as f:
        json.dump({
            'segment_distribution': segment_distribution,
            'segment_quantity': segment_quantity,
            'segment_unit_price': segment_unit_price,
            'segment_profit': segment_profit,
            'segment_discount': segment_discount,
            'region_distribution': region_distribution,
            'ship_mode_distribution': ship_mode_distribution,
            'ship_days_distribution': ship_speed_distribution,

            'region_quantity': region_quantity,
            'region_sales': region_sales,
            'region_unit_price': region_unit_price,
            'region_discount': region_discount,
            'region_profit': region_profit,
            'region_profit_margin': region_profit_margin,

            'country_distribution': country_distribution,
            'country_quantity_top_10': country_quantity_top_10,
            'country_sales_top_10': country_sales_top_10,
            'country_unit_price_top_10': country_unit_price_top_10,
            'country_profit_top_10': country_profit_top_10,
            'country_profit_margin_top_10': country_profit_margin_top_10,

            'discount_distribution': discount_distribution,
            'segment_discount_distribution_percentage': segment_discount_distribution_percentage,
            'discount_quantity': discount_quantity,
            'discount_sales': discount_sales,
            'discount_profit': discount_profit,
            'discount_unit_price': discount_unit_price,
            'discount_profit_margin': discount_profit_margin,

            'seasonal_quantity': seasonal_quantity,
            'year_seasonal_quantity': year_seasonal_quantity,
            'seasonal_sales': seasonal_sales,
            'year_seasonal_sales': year_seasonal_sales,
            'sales_ratio_by_quarter': sales_ratio_by_quarter,
            'seasonal_profit': seasonal_profit,
            'year_seasonal_profit': year_seasonal_profit,
            'seasonal_profit_ratio_by_sales': seasonal_profit_ratio_by_sales,

            'top_10_states': top_10_states,
            'top_10_cities': top_10_cities,
        }, f, indent=4)

    with open('./analysis_result_{}/analysis_result_{}_oneline.json'.format(y1, y1), 'w') as f:
        json.dump({
            'segment_distribution': segment_distribution,
            'segment_quantity': segment_quantity,
            'segment_unit_price': segment_unit_price,
            'segment_profit': segment_profit,
            'segment_discount': segment_discount,
            'region_distribution': region_distribution,
            'ship_mode_distribution': ship_mode_distribution,
            'ship_days_distribution': ship_speed_distribution,

            'region_quantity': region_quantity,
            'region_sales': region_sales,
            'region_unit_price': region_unit_price,
            'region_discount': region_discount,
            'region_profit': region_profit,
            'region_profit_margin': region_profit_margin,

            'country_distribution': country_distribution,
            'country_quantity_top_10': country_quantity_top_10,
            'country_sales_top_10': country_sales_top_10,
            'country_unit_price_top_10': country_unit_price_top_10,
            'country_profit_top_10': country_profit_top_10,
            'country_profit_margin_top_10': country_profit_margin_top_10,

            'discount_distribution': discount_distribution,
            'segment_discount_distribution_percentage': segment_discount_distribution_percentage,
            'discount_quantity': discount_quantity,
            'discount_sales': discount_sales,
            'discount_profit': discount_profit,
            'discount_unit_price': discount_unit_price,
            'discount_profit_margin': discount_profit_margin,

            'seasonal_quantity': seasonal_quantity,
            'year_seasonal_quantity': year_seasonal_quantity,
            'seasonal_sales': seasonal_sales,
            'year_seasonal_sales': year_seasonal_sales,
            'sales_ratio_by_quarter': sales_ratio_by_quarter,
            'seasonal_profit': seasonal_profit,
            'year_seasonal_profit': year_seasonal_profit,
            'seasonal_profit_ratio_by_sales': seasonal_profit_ratio_by_sales,

            'top_10_states': top_10_states,
            'top_10_cities': top_10_cities
        }, f)

