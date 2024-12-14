# save the upper text analysis into a jsonl file
# keep the structure of dictionary
import os
import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pygal
from pygal.style import *
from IPython.display import display, HTML
import plotly.express as px

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

# filter the data#
class Analysis:
    def __init__(self, data):
        self.data = data

    def analyze_segment(self):
        segment_distribution = self.data['Segment'].value_counts().to_dict()
        segment_distribution = {k: (v, round(v / len(self.data), 2)) for k, v in segment_distribution.items()}
        segment_quantity = self.data.groupby('Segment')['Quantity'].mean().round(2).to_dict()
        segment_unit_price = (self.data.groupby('Segment')['Sales'].sum() / self.data.groupby('Segment')['Quantity'].sum()).round(2).to_dict()
        segment_profit = (self.data.groupby('Segment')['Profit'].sum() / self.data.groupby('Segment')['Quantity'].sum()).round(2).to_dict()
        segment_discount = self.data.groupby('Segment')['Discount'].mean().round(2).to_dict()
        return {
            'segment_distribution': segment_distribution,
            'segment_quantity': segment_quantity,
            'segment_unit_price': segment_unit_price,
            'segment_profit': segment_profit,
            'segment_discount': segment_discount
        }

    def analyze_region(self):
        region_distribution = self.data['Region'].value_counts().to_dict()
        region_distribution = {k: (v, round(v / len(self.data), 2)) for k, v in region_distribution.items()}
        region_quantity = self.data.groupby('Region')['Quantity'].mean().round(2).to_dict()
        region_sales = self.data.groupby('Region')['Sales'].mean().round(2).to_dict()
        region_unit_price = (self.data.groupby('Region')['Sales'].sum() / self.data.groupby('Region')['Quantity'].sum()).round(2).to_dict()
        region_discount = self.data.groupby('Region')['Discount'].mean().round(2).to_dict()
        region_profit = (self.data.groupby('Region')['Profit'].sum() / self.data.groupby('Region')['Quantity'].sum()).round(2).to_dict()
        region_profit_margin = (self.data.groupby('Region')['Profit'].sum() / self.data.groupby('Region')['Sales'].sum()).round(2).to_dict()
        return {
            'region_distribution': region_distribution,
            'region_quantity': region_quantity,
            'region_sales': region_sales,
            'region_unit_price': region_unit_price,
            'region_discount': region_discount,
            'region_profit': region_profit,
            'region_profit_margin': region_profit_margin
        }

    def analyze_country(self):
        country_distribution = self.data['Country'].value_counts().to_dict()
        country_distribution = {k: (v, round(v / len(self.data), 2)) for k, v in country_distribution.items()}
        country_quantity = self.data.groupby('Country')['Quantity'].mean().round(2).to_dict()
        country_sales = self.data.groupby('Country')['Sales'].mean().round(2).to_dict()
        country_unit_price = (self.data.groupby('Country')['Sales'].sum() / self.data.groupby('Country')['Quantity'].sum()).round(2).to_dict()
        country_profit = (self.data.groupby('Country')['Profit'].sum() / self.data.groupby('Country')['Quantity'].sum()).round(2).to_dict()
        country_profit_margin = (self.data.groupby('Country')['Profit'].sum() / self.data.groupby('Country')['Sales'].sum()).round(2).to_dict()
        return {
            'country_distribution': country_distribution,
            'country_quantity': country_quantity,
            'country_sales': country_sales,
            'country_unit_price': country_unit_price,
            'country_profit': country_profit,
            'country_profit_margin': country_profit_margin
        }

    def analyze_discount(self):
        self.data['Discount_Group'] = self.data['Discount'].apply(discount_group)
        discount_distribution = self.data['Discount_Group'].value_counts().to_dict()
        discount_distribution = {k: (v, round(v / len(self.data), 2)) for k, v in discount_distribution.items()}
        discount_quantity = self.data.groupby('Discount_Group')['Quantity'].mean().round(2).to_dict()
        discount_sales = self.data.groupby('Discount_Group')['Sales'].mean().round(2).to_dict()
        discount_profit = self.data.groupby('Discount_Group')['Profit'].mean().round(2).to_dict()
        discount_unit_price = (self.data.groupby('Discount_Group')['Sales'].sum() / self.data.groupby('Discount_Group')['Quantity'].sum()).round(2).to_dict()
        discount_profit_margin = (self.data.groupby('Discount_Group')['Profit'].sum() / self.data.groupby('Discount_Group')['Sales'].sum()).round(2).to_dict()
        return {
            'discount_distribution': discount_distribution,
            'discount_quantity': discount_quantity,
            'discount_sales': discount_sales,
            'discount_profit': discount_profit,
            'discount_unit_price': discount_unit_price,
            'discount_profit_margin': discount_profit_margin
        }

    def analyze_time(self):
        self.data['Order Date'] = pd.to_datetime(self.data['Order Date'])
        self.data['Quarter'] = self.data['Order Date'].dt.quarter
        quarter_map = {1: 'Spring', 2: 'Summer', 3: 'Autumn', 4: 'Winter'}
        seasonal_quantity = self.data.groupby('Quarter')['Quantity'].sum().round(2).to_dict()
        seasonal_quantity = {quarter_map[k]: v for k, v in seasonal_quantity.items()}
        seasonal_sales = self.data.groupby('Quarter')['Sales'].sum().round(2).to_dict()
        seasonal_sales = {quarter_map[k]: v for k, v in seasonal_sales.items()}
        seasonal_profit = self.data.groupby('Quarter')['Profit'].sum().round(2).to_dict()
        seasonal_profit = {quarter_map[k]: v for k, v in seasonal_profit.items()}
        self.data['Sales_Ratio'] = self.data['Sales'] / self.data['Quantity']
        sales_ratio_by_quarter = self.data.groupby('Quarter')['Sales_Ratio'].mean().round(2).to_dict()
        sales_ratio_by_quarter = {quarter_map[k]: v for k, v in sales_ratio_by_quarter.items()}
        self.data['profit_ratio_by_sales'] = self.data['Profit'] / self.data['Sales']
        seasonal_profit_ratio_by_sales = self.data.groupby('Quarter')['profit_ratio_by_sales'].sum().round(2).to_dict()
        seasonal_profit_ratio_by_sales = {quarter_map[k]: v for k, v in seasonal_profit_ratio_by_sales.items()}
        self.data['Year'] = self.data['Order Date'].dt.year
        year_seasonal_quantity = self.data.groupby(['Year', 'Quarter'])['Quantity'].sum()
        year_seasonal_quantity = year_seasonal_quantity.to_dict()
        year_seasonal_quantity = {f"{k[0]}{quarter_map[k[1]]}": round(v, 2) for k, v in year_seasonal_quantity.items()}
        year_seasonal_sales = self.data.groupby(['Year', 'Quarter'])['Sales'].sum()
        year_seasonal_sales = year_seasonal_sales.to_dict()
        year_seasonal_sales = {f"{k[0]}{quarter_map[k[1]]}": round(v, 2) for k, v in year_seasonal_sales.items()}
        return {
            'seasonal_quantity': seasonal_quantity,
            'seasonal_sales': seasonal_sales,
            'seasonal_profit': seasonal_profit,
            'sales_ratio_by_quarter': sales_ratio_by_quarter,
            'seasonal_profit_ratio_by_sales': seasonal_profit_ratio_by_sales,
            'year_seasonal_quantity': year_seasonal_quantity,
            'year_seasonal_sales': year_seasonal_sales
        }

    def analyze_state_city(self):
        state_distribution = self.data['State'].value_counts().to_dict()
        state_distribution = {k: (v, round(v / len(self.data), 2)) for k, v in state_distribution.items()}
        top_10_states = dict(list(state_distribution.items())[:10])
        top_10_states_values = [v[0] for v in top_10_states.values()]
        city_distribution = self.data['City'].value_counts().to_dict()
        city_distribution = {k: (v, round(v / len(self.data), 2)) for k, v in city_distribution.items()}
        top_10_cities = dict(list(city_distribution.items())[:10])
        top_10_cities_values = [v[0] for v in top_10_cities.values()]
        return {
            'top_10_states': top_10_states,
            'top_10_states_values': top_10_states_values,
            'top_10_cities': top_10_cities,
            'top_10_cities_values': top_10_cities_values
        }

    def analyze_ship_mode(self):
        ship_mode_distribution = self.data['Ship Mode'].value_counts().to_dict()
        ship_mode_distribution = {k: (v, round(v / len(self.data), 2)) for k, v in ship_mode_distribution.items()}
        self.data['Ship Date'] = pd.to_datetime(self.data['Ship Date'])
        self.data['Order Date'] = pd.to_datetime(self.data['Order Date'])
        self.data['Ship Speed'] = (self.data['Ship Date'] - self.data['Order Date']).dt.days
        ship_speed_distribution = self.data['Ship Speed'].value_counts().to_dict()
        ship_speed_distribution = {k: (v, round(v / len(self.data), 2)) for k, v in ship_speed_distribution.items()}
        return {
            'ship_mode_distribution': ship_mode_distribution,
            'ship_speed_distribution': ship_speed_distribution
        }

    def analyze_all(self):
        return {
            **self.analyze_segment(),
            **self.analyze_region(),
            **self.analyze_country(),
            **self.analyze_discount(),
            **self.analyze_time(),
            **self.analyze_state_city(),
            **self.analyze_ship_mode()
        }

for y1 in list(set(data_og['Combined_Category'])):
    print(y1)
    if not os.path.exists('./analysis_result_{}'.format(y1)):
        os.makedirs('./analysis_result_{}'.format(y1))
    data = data_og[data_og['Combined_Category'] == y1]
    analysis = Analysis(data)
    analysis_result = analysis.analyze_all()
    with open('./analysis_result_{}/analysis_result_{}.json'.format(y1, y1), 'w') as f:
        json.dump(analysis_result, f, indent=4)

class Visualization:
    def __init__(self, data, analysis_result, category):
        self.data = data
        self.analysis_result = analysis_result
        self.category = category

    def plot_top_10_states(self):
        top_10_states = self.analysis_result['top_10_states']
        top_10_states_values = self.analysis_result['top_10_states_values']
        plt.figure(figsize=(12, 6))
        plt.bar(top_10_states.keys(), top_10_states_values)
        plt.xlabel('State')
        plt.ylabel('Number of Purchase')
        plt.title('Top 10 state distribution of item {}'.format(self.category))
        for i, v in enumerate(top_10_states_values):
            plt.text(i, v, str(v), ha='center', va='bottom')
        plt.xticks(rotation=45)
        plt.savefig('./analysis_result_{}/top_10_states_distribution_{}.png'.format(self.category, self.category))

    def plot_top_10_cities(self):
        top_10_cities = self.analysis_result['top_10_cities']
        top_10_cities_values = self.analysis_result['top_10_cities_values']
        plt.figure(figsize=(12, 6))
        plt.bar(top_10_cities.keys(), top_10_cities_values)
        plt.xlabel('City')
        plt.ylabel('Number of Purchase')
        plt.title('Top 10 city distribution of item {}'.format(self.category))
        for i, v in enumerate(top_10_cities_values):
            plt.text(i, v, str(v), ha='center', va='bottom')
        plt.xticks(rotation=45)
        plt.savefig('./analysis_result_{}/top_10_cities_distribution_{}.png'.format(self.category, self.category))

    def plot_us_state_profit_map(self):
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
        us_state_profit = self.data[self.data['State'].isin(us_states_full)].groupby('State')['Profit'].sum().reset_index()
        us_state_profit['State'] = us_state_profit['State'].map(state_abbreviations)
        fig = px.choropleth(
            us_state_profit,
            locations='State',
            locationmode='USA-states',
            color='Profit',
            color_continuous_scale='Blues',
            scope='usa',
            title=f'Profit by US State for item {self.category}',
            labels={'Profit': 'Total Profit'}
        )
        fig.update_traces(
            hovertemplate="<b>%{location}</b><br>Total Profit: %{z:$,.2f}<extra></extra>"
        )
        fig.show()
        output_file = './analysis_result_{}/US_state_profit_map.html'.format(self.category, self.category)
        fig.write_html(output_file, include_plotlyjs='cdn')
        print(f"US_State profit map saved to: {output_file}")

    def plot_sales_over_time(self):
        style1 = Style(
            background='white',
            plot_background='white',
            foreground='#000000',
            foreground_strong='#0F52BA',
            foreground_subtle='#4682B4',
            colors=('#0F52BA', '#4682B4', '#5F9EA0', '#87CEFA')
        )
        self.data['YearMonth'] = self.data['Order Date'].dt.to_period('M')
        sales_by_month = self.data.groupby('YearMonth')['Sales'].sum()
        months = sales_by_month.index.astype(str).tolist()
        sales = sales_by_month.values.tolist()
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
        line_chart.title = 'Sales Amount Over Time for Item {}'.format(self.category)
        line_chart.x_labels = months
        line_chart.add('Monthly Sales', sales)
        output_file = './analysis_result_{}/sales_over_time_{}.svg'.format(self.category, self.category)
        line_chart.render_to_file(output_file)

    def plot_seasonal_analysis(self):
        seasonal_sales = self.analysis_result['seasonal_sales']
        seasonal_quantity = self.analysis_result['seasonal_quantity']
        seasonal_profit = self.analysis_result['seasonal_profit']
        sales_ratio_by_quarter = self.analysis_result['sales_ratio_by_quarter']
        seasonal_profit_ratio_by_sales = self.analysis_result['seasonal_profit_ratio_by_sales']
        seasons = list(seasonal_sales.keys())
        sales = list(seasonal_sales.values())
        quantity = list(seasonal_quantity.values())
        profit = list(seasonal_profit.values())
        sales_ratio = list(sales_ratio_by_quarter.values())
        profit_ratio_by_sales = list(seasonal_profit_ratio_by_sales.values())
        fig, axes = plt.subplots(2, 3, figsize=(20, 12))
        fig.suptitle('Sales Amount Over Time for Item {}'.format(self.category), fontsize=20, color='#4682B4', weight='bold')
        axes[0, 0].bar(seasons, sales, color='#4682B4', alpha=0.8, edgecolor='black')
        axes[0, 0].set_title('Seasonal Sales', fontsize=16, color='#4682B4')
        axes[0, 0].set_xlabel('Season', fontsize=12)
        axes[0, 0].set_ylabel('Sales', fontsize=12)
        axes[0, 0].grid(axis='y', linestyle='--', alpha=0.7)
        for i, value in enumerate(sales):
            y_position = min(value + 5000, axes[0, 0].get_ylim()[1] - 5000)
            axes[0, 0].text(i, y_position, f'{value:,.0f}', ha='center', fontsize=10, color='black')
        axes[0, 1].bar(seasons, quantity, color='#5F9EA0', alpha=0.8, edgecolor='black')
        axes[0, 1].set_title('Seasonal Quantity', fontsize=16, color='#5F9EA0')
        axes[0, 1].set_xlabel('Season', fontsize=12)
        axes[0, 1].set_ylabel('Quantity', fontsize=12)
        axes[0, 1].grid(axis='y', linestyle='--', alpha=0.7)
        for i, value in enumerate(quantity):
            y_position = min(value + 100, axes[0, 1].get_ylim()[1] - 100)
            axes[0, 1].text(i, y_position, f'{value:,.0f}', ha='center', fontsize=10, color='black')
        axes[0, 2].bar(seasons, profit, color='#87CEFA', alpha=0.8, edgecolor='black')
        axes[0, 2].set_title('Seasonal Profit', fontsize=16, color='#87CEFA')
        axes[0, 2].set_xlabel('Season', fontsize=12)
        axes[0, 2].set_ylabel('Profit', fontsize=12)
        axes[0, 2].grid(axis='y', linestyle='--', alpha=0.7)
        for i, value in enumerate(profit):
            y_position = min(value + 1500, axes[0, 2].get_ylim()[1] - 1500)
            axes[0, 2].text(i, y_position, f'{value:,.0f}', ha='center', fontsize=10, color='black')
        axes[1, 0].plot(seasons, sales_ratio, marker='o', color='#4682B4', linewidth=2)
        axes[1, 0].set_title('Sales-to-Quantity Ratio', fontsize=16, color='#4682B4')
        axes[1, 0].set_xlabel('Season', fontsize=12)
        axes[1, 0].set_ylabel('Ratio', fontsize=12)
        axes[1, 0].grid(axis='both', linestyle='--', alpha=0.7)
        for i, value in enumerate(sales_ratio):
            y_position = max(value - 1, axes[1, 0].get_ylim()[0] + 1)
            axes[1, 0].text(i, y_position, f'{value:.1f}', ha='center', fontsize=10, color='black')
        axes[1, 1].plot(seasons, profit_ratio_by_sales, marker='o', color='#5F9EA0', linewidth=2)
        axes[1, 1].set_title('Profit-to-Sales Ratio', fontsize=16, color='#5F9EA0')
        axes[1, 1].set_xlabel('Season', fontsize=12)
        axes[1, 1].set_ylabel('Ratio', fontsize=12)
        axes[1, 1].grid(axis='both', linestyle='--', alpha=0.7)
        for i, value in enumerate(profit_ratio_by_sales):
            y_position = min(value + 2, axes[1, 1].get_ylim()[1] - 2)
            axes[1, 1].text(i, y_position, f'{value:.1f}', ha='center', fontsize=10, color='black')
        axes[1, 2].axis('off')
        plt.subplots_adjust(hspace=0.5, wspace=0.3)
        plt.savefig('./analysis_result_{}/Seasonal_Analysis_{}.png'.format(self.category, self.category))
        plt.show()

    def plot_discount_vs_sales_and_profit(self):
        discount_quantity = self.analysis_result['discount_quantity']
        discount_profit = self.analysis_result['discount_profit']
        discount_profit_margin = self.analysis_result['discount_profit_margin']
        style2 = Style(
            background='white',
            plot_background='white',
            foreground='black',
            foreground_strong='black',
            foreground_subtle='#630C0D',
            colors=('#0F52BA', '#B22222')
        )
        discount_levels = list(discount_quantity.keys())
        avg_sales_volumes = list(discount_quantity.values())
        avg_profit = list(discount_profit.values())
        profit_margin = list(discount_profit_margin.values())
        discounts = [str(d) for d in discount_levels]
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
        dual_axis_chart.title = 'Discount vs Average Sales Volume and Average Profit for item {}'.format(self.category)
        dual_axis_chart.x_labels = discounts
        dual_axis_chart.add('Average Sales Volume', avg_sales_volumes)
        dual_axis_chart.add('Average Profit', avg_profit, secondary=True)
        dual_axis_chart.add('Average Profit Margin', profit_margin, secondary=True)
        output_file = './analysis_result_{}/discount_vs_avg_sales_volumes_and_profit_{}.svg'.format(self.category, self.category)
        dual_axis_chart.render_to_file(output_file)
        print("Chart saved to: {}".format(output_file))

    def plot_segment_analysis(self):
        segment_unit_price = self.analysis_result['segment_unit_price']
        segment_profit = self.analysis_result['segment_profit']
        segment_discount = self.analysis_result['segment_discount']
        style3 = Style(
            background='white',
            plot_background='white',
            foreground='black',
            foreground_strong='black',
            foreground_subtle='#630C0D',
            colors=('#4682B4', '#8B0000', '#32CD32')
        )
        labels = list(segment_unit_price.keys())
        unit_price_values = list(segment_unit_price.values())
        profit_values = list(segment_profit.values())
        discount_values = [v * 100 for v in segment_discount.values()]
        print("Note: Discount values scaled by 100 for better visualization.")
        max_value = max(max(unit_price_values), max(profit_values), max(discount_values))
        min_value = min(min(profit_values), min(discount_values))
        y_range_padding = (max_value - min_value) * 0.2
        y_range_max = max_value + y_range_padding
        y_range_min = min_value - y_range_padding
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
        grouped_bar_chart.title = 'Average Unit Price, Profit, and Discount by Segment for item {}'.format(self.category)
        grouped_bar_chart.x_labels = labels
        grouped_bar_chart.add('Unit Price', unit_price_values)
        grouped_bar_chart.add('Profit', profit_values)
        grouped_bar_chart.add('Discount (scaled x100)', discount_values)
        output_file = './analysis_result_{}/unit_price_profit_discount_by_segment_{}.svg'.format(self.category, self.category)
        grouped_bar_chart.render_to_file(output_file)
        print("Chart saved to: {}".format(output_file))

    def plot_ship_mode_distribution(self):
        ship_mode_distribution = self.analysis_result['ship_mode_distribution']
        ship_mode_style = Style(
            background='white',
            plot_background='white',
            foreground='black',
            foreground_strong='black',
            foreground_subtle='#333333',
            colors=('#B22222', '#6B8E23', '#4682B4', '#FFD700')
        )
        ship_mode_labels = list(ship_mode_distribution.keys())
        ship_mode_values = [v[0] for v in ship_mode_distribution.values()]
        ship_mode_percentages = [v[1] * 100 for v in ship_mode_distribution.values()]
        pie_chart = pygal.Pie(
            style=ship_mode_style,
            title_font_size=20,
            legend_at_bottom=True,
            inner_radius=0.3
        )
        pie_chart.title = 'Ship Mode Distribution of item {}'.format(self.category)
        for label, value, percentage in zip(ship_mode_labels, ship_mode_values, ship_mode_percentages):
            pie_chart.add(f"{label} ({percentage:.1f}%)", value)
        output_file = './analysis_result_{}/ship_mode_distribution_{}.svg'.format(self.category, self.category)
        pie_chart.render_to_file(output_file)
        print("Chart saved to: {}".format(output_file))

for y1 in list(set(data_og['Combined_Category'])):
    print(y1)
    if not os.path.exists('./analysis_result_{}'.format(y1)):
        os.makedirs('./analysis_result_{}'.format(y1))
    data = data_og[data_og['Combined_Category'] == y1]
    analysis = Analysis(data)
    analysis_result = analysis.analyze_all()
    with open('./analysis_result_{}/analysis_result_{}.json'.format(y1, y1), 'w') as f:
        json.dump(analysis_result, f, indent=4)
    visualization = Visualization(data, analysis_result, y1)
    visualization.plot_top_10_states()
    visualization.plot_top_10_cities()
    visualization.plot_us_state_profit_map()
    visualization.plot_sales_over_time()
    visualization.plot_seasonal_analysis()
    visualization.plot_discount_vs_sales_and_profit()
    visualization.plot_segment_analysis()
    visualization.plot_ship_mode_distribution()