import os
import gradio as gr
from gradio.components import HTML
import torch
from PIL.ImageOps import scale
from PIL import Image
from transformers import BertTokenizer, BertForSequenceClassification
import json
from zhipuai import ZhipuAI

label_num_to_text = {0: ('Furniture', 'Bookcases'), 1: ('Furniture', 'Chairs'), 2: ('Furniture', 'Furnishings'), 3: ('Furniture', 'Tables'), 4: ('Office Supplies', 'Appliances'), 5: ('Office Supplies', 'Art'), 6: ('Office Supplies', 'Binders'), 7: ('Office Supplies', 'Envelopes'), 8: ('Office Supplies', 'Fasteners'), 9: ('Office Supplies', 'Labels'), 10: ('Office Supplies', 'Paper'), 11: ('Office Supplies', 'Storage'), 12: ('Office Supplies', 'Supplies'), 13: ('Technology', 'Accessories'), 14: ('Technology', 'Copiers'), 15: ('Technology', 'Machines'), 16: ('Technology', 'Phones')}

# Load the BERT model and tokenizer
model_path = '../Classification/results/checkpoint-1299'
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
model = BertForSequenceClassification.from_pretrained(model_path)
device = torch.device('cuda') if torch.cuda.is_available() else torch.device('cpu')
model.to(device)

# Initialize ZhipuAI client
client = ZhipuAI(api_key="06f59aab3f61a4e8ba0ef45b663fc204.ipiw6sxXKMQNoBY6")

# Function to classify commodity
def classify_commodity(commodity_name):
    inputs = tokenizer(commodity_name, return_tensors="pt").to(device)
    outputs = model(**inputs)
    preds = outputs.logits.argmax(-1).item()
    category = label_num_to_text[preds][0] + "-" + label_num_to_text[preds][1]
    print(category)
    return category

# Function to generate sales suggestions
def generate_suggestions(messages, commodity_name, category):

    analysis_file = f'../data_analysis/analysis_result_{category}/analysis_result_{category}.json'
    with open(analysis_file, 'r') as f:
        analysis_result = json.load(f)

    known_facts = {
        "product": category,
        "most_segment_customers": analysis_result["segment_distribution"],
        "most_quantity_customers": analysis_result["segment_quantity"],
        "highest_unit_price_analysis": analysis_result["segment_unit_price"],
        "highest_profit_analysis": analysis_result["segment_profit"],
        "highest_discount_analysis": analysis_result["segment_discount"],
        "most_region_customers": analysis_result["region_distribution"],
        "most_shipping_mode_counts": analysis_result["ship_mode_distribution"],
        "most_common_shipping_time_cost_counts": analysis_result["ship_speed_distribution"],
        "most_country_customers": analysis_result["country_distribution"],
        "most_discount_customers": analysis_result["discount_distribution"],
        "most_segment_discount_customers": analysis_result["segment_discount"],
        "most_quantity_discount": analysis_result["discount_quantity"],
        "highest_discount_sales_analysis": analysis_result["discount_sales"],
        "highest_discount_profit_analysis": analysis_result["discount_profit"],
        "highest_discount_unit_price_analysis": analysis_result["discount_unit_price"],
        "highest_discount_profit_margin_analysis": analysis_result["discount_profit_margin"],
        "most_quantity_seasons": analysis_result["seasonal_quantity"],
        "most_quantity_year_seasons": analysis_result["year_seasonal_quantity"],
        "highest_season_sales_analysis": analysis_result["seasonal_sales"],
        "highest_year_season_sales_analysis": analysis_result["year_seasonal_sales"],
    }
    top_10_cities_image = Image.open(f'../data_analysis/analysis_result_{category}/top_10_cities_distribution_{category}.png')
    top_10_states_image = Image.open(f'../data_analysis/analysis_result_{category}/top_10_states_distribution_{category}.png')
    seasonal_analysis_image = Image.open(f'../data_analysis/analysis_result_{category}/Seasonal_Analysis_{category}.png')


    response = client.chat.completions.create(
        model="glm-4-plus",
        messages=[
            {"role": "user", "content": f"As a Sales Assistant to help the company, please analyze and generate sales suggestions and advice for the product {category}, with less than 300 words."},
            {"role": "assistant", "content": "Of course, I can help you with that. Could you provide me with some information about the product?"},
            {"role": "user", "content": f"Here are the facts: {known_facts}"}
        ],
    )
    sales_suggestions = response.choices[0].message.content

    messages.append((commodity_name, f"The commodity '{commodity_name}' belongs to category '{category}'.\n\nSales Suggestions:\n{sales_suggestions}"))
    return messages, known_facts, top_10_states_image, top_10_cities_image, seasonal_analysis_image

# Function to send a message to the chatbot to keep talking (remember using the history)
def send_message(chat_history, message):
    messages = []
    print(chat_history)
    for i in range(0, len(chat_history)):
        messages.append({
            "role": "user",
            "content": chat_history[i][0]
        })
        messages.append({
            "role": "assistant",
            "content": chat_history[i][1]
        })
    messages.append({
        "role": "user",
        "content": message
    })
    # using history to keep the conversation
    print(messages)
    response = client.chat.completions.create(
        model="glm-4-plus",
        messages=messages,
    )
    messages.append({
        "role": "assistant",
        "content": response.choices[0].message.content
    })
    chat_history.append([message,response.choices[0].message.content])
    return chat_history

# Function to read SVG files
def read_svgs(category, svg_file_name):
    svg_path = f"../data_analysis/analysis_result_{category}/{svg_file_name}_{category}.svg"
    with open(svg_path, 'r', encoding='utf-8') as file:
        svg_content = file.read()
    return f"<div style='width:100%; height:600px; overflow:auto;'>{svg_content}</div>"

# Function to open HTML file
def open_html(category):
    html_path = fr"..\data_analysis\analysis_result_{category}\US_state_profit_map.html"
    try:
        os.startfile(html_path)
        return "HTML file opened successfully."
    except Exception as e:
        return f"Failed to open HTML file. Error: {e}"


# Create Gradio Blocks interface
with gr.Blocks() as demo:
    title = "# Sales Assistant Chatbot"
    gr.Markdown(title)
    category = gr.State()

    with gr.Row():
        with gr.Column(scale=1):
            commodity_input = gr.Textbox(label="Input Commodity Name")
            classify_button = gr.Button("Step1.Classify")
            category_output = gr.Textbox(label="Category", interactive=False)
            suggestions_button = gr.Button("Step2.Generate Suggestions")
            known_facts_output = gr.Textbox(label="Known Facts", interactive=False)
        with gr.Column(scale=4):
            chatbot = gr.Chatbot(label="Sales Assistant Chatbot")
            chatbot_input = gr.Textbox(label="Your Message")
            send_button = gr.Button("Continue Chat")
            html_button = gr.Button("Open US State Profit Map")
            with gr.Row():
                # 2 images in a row
                image1 = gr.Image(value=None, label="Top 10 States Distribution")
                image2 = gr.Image(value=None, label="Top 10 Cities Distribution")
            with gr.Row():
                image3 = gr.Image(value=None, label="Seasonal Analysis")
            with gr.Row():
                image4 = gr.HTML(label="Discount VS Sales and Profit")
                image5 = gr.HTML(label="Sales Over Time")
            with gr.Row():
                image6 = gr.HTML(label="Ship Mode Distribution")
                image7 = gr.HTML(label="Unit Price Profit Discount By Segment")



    classify_button.click(fn=classify_commodity, inputs=commodity_input, outputs=category_output)
    # suggestions_button.click(fn=generate_suggestions, inputs=[chatbot, commodity_input, category_output], outputs=[chatbot, known_facts_output, image1, image2])
    suggestions_button.click(
        fn=lambda chatbot, commodity_name, category: (
            *generate_suggestions(chatbot, commodity_name, category),
            read_svgs(category, "discount_vs_avg_sales_volumes_and_profit"),
            read_svgs(category, "sales_over_time"),
            read_svgs(category, "ship_mode_distribution"),
            read_svgs(category, "unit_price_profit_discount_by_segment"),
            # read_html(category)
        ),
        inputs=[chatbot, commodity_input, category_output],
        outputs=[chatbot, known_facts_output, image1, image2, image3, image4, image5, image6, image7],
    )
    send_button.click(fn=send_message, inputs=[chatbot, chatbot_input], outputs=chatbot)
    html_button.click(fn=open_html, inputs=category_output)

demo.launch(share=True)