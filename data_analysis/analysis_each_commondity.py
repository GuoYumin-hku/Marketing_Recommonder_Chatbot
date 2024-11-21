
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import json

# data loading and preprocessing
data = pd.read_csv('../data/Sample_Superstore.csv', on_bad_lines='skip')
data = data.dropna()
data['Combined_Category'] = data['Category'].astype(str) + '-' + data['Sub-Category'].astype(str)
data.head()

print(set(data['Ship Mode']))
print(set(data['Segment']))
print(set(data['Region']))
print("States:",len(set(data['State'])))
print("Cities:",len(set(data['City'])))
# print(set(data['Category']))
# print(set(data['Sub-Category']))
print(set(data['Combined_Category']))
# data.columns


def analysis_data(data, y1):
    if not os.path.exists('./analysis_result_{}'.format(y1)):
        os.makedirs('./analysis_result_{}'.format(y1))
    data = data[data['Combined_Category'] == y1]

    # analyze the segment distribution and save in dictionary in both number and percentage
    segment_distribution = data['Segment'].value_counts().to_dict()
    segment_distribution = {k: (v, round(v / len(data), 2)) for k, v in segment_distribution.items()}
    print("The segment distribution of item '{}' is: {}".format(y1, segment_distribution))

    # analyze the difference of average quantity between the segment, round to 2 decimal
    segment_quantity = data.groupby('Segment')['Quantity'].mean().to_dict()
    segment_quantity = {k: round(v, 2) for k, v in segment_quantity.items()}
    print("The average quantity of item bought by each segment is: {}".format(segment_quantity))

    # analyze the average unit price; profit; discount of each segment, round to 2 decimal
    # unit price = sales / quantity
    segment_unit_price = data.groupby('Segment')['Sales'].sum() / data.groupby('Segment')['Quantity'].sum()
    segment_unit_price = segment_unit_price.to_dict()
    segment_unit_price = {k: round(v, 2) for k, v in segment_unit_price.items()}
    print("The average unit price of item bought by each segment is: {}".format(segment_unit_price))
    # also draw the curve plot by pyplot of unit price along the order-date
    # data['Order Date'] = pd.to_datetime(data['Order Date'])
    # data_sort_by_date = data.sort_values(by='Order Date')
    # plt.plot(data_sort_by_date['Order Date'], data_sort_by_date['Sales'] / data_sort_by_date['Quantity'])
    # plt.xlabel('Order Date')
    # plt.ylabel('Unit Price')
    # plt.title('Unit Price of item {} along the order date'.format(y1))
    # plt.show()

    # mean profit = profit / quantity
    segment_profit = data.groupby('Segment')['Profit'].sum() / data.groupby('Segment')['Quantity'].sum()
    segment_profit = segment_profit.to_dict()
    segment_profit = {k: round(v, 2) for k, v in segment_profit.items()}
    print("The average profit of item bought by each segment is: {}".format(segment_profit))

    # discount
    segment_discount = data.groupby('Segment')['Discount'].mean()
    segment_discount = segment_discount.to_dict()
    segment_discount = {k: round(v, 2) for k, v in segment_discount.items()}
    print("The average discount of item bought by each segment is: {}".format(segment_discount))

    # analyze the region distribution and save in dictionary in both number and percentage
    region_distribution = data['Region'].value_counts().to_dict()
    region_distribution = {k: (v, round(v / len(data), 2)) for k, v in region_distribution.items()}
    print("The region distribution of item '{}' is: {}".format(y1, region_distribution))


    data[data['Combined_Category'] == y1].head()

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
    print(top_10_cities)

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

    # save the upper text analysis into a jsonl file
    # keep the structure of dictionary

    with open('./analysis_result_{}/analysis_result_{}.json'.format(y1, y1), 'w') as f:
        json.dump({
            'segment_distribution': segment_distribution,
            'segment_quantity': segment_quantity,
            'segment_unit_price': segment_unit_price,
            'segment_profit': segment_profit,
            'segment_discount': segment_discount,
            'region_distribution': region_distribution,
            # 'state_distribution': state_distribution,
            # 'city_distribution': city_distribution,
            'top_10_states': top_10_states,
            'top_10_cities': top_10_cities
        }, f, indent=4)

    with open('./analysis_result_{}/analysis_result_{}_oneline.json'.format(y1, y1), 'w') as f:
        json.dump({
            'segment_distribution': segment_distribution,
            'segment_quantity': segment_quantity,
            'segment_unit_price': segment_unit_price,
            'segment_profit': segment_profit,
            'segment_discount': segment_discount,
            'region_distribution': region_distribution,
            # 'state_distribution': state_distribution,
            # 'city_distribution': city_distribution,
            'top_10_states': top_10_states,
            'top_10_cities': top_10_cities
        }, f)

for y1 in set(data['Combined_Category']):
    analysis_data(data, y1)
    print("Analysis of item '{}' is done.".format(y1))