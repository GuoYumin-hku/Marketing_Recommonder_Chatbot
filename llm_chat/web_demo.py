# now the gradio

import gradio as gr
import torch
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

# Function to classify commodity and generate sales suggestions
def chatbot(commodity_name):
    # Step 1: Classify the commodity's category using BERT
    inputs = tokenizer(commodity_name, return_tensors="pt").to(device)
    outputs = model(**inputs)
    preds = outputs.logits.argmax(-1).item()
    category = label_num_to_text[preds][0]+"-"+label_num_to_text[preds][1]

    # Step 2: Load the preprocessed analysis data for the category
    analysis_file = f'../data_analysis/analysis_result_{category}/analysis_result_{category}.json'
    with open(analysis_file, 'r') as f:
        analysis_result = json.load(f)

    # Extract known facts/features
    known_facts = {
        "product": category,
        "most_segment_customers": analysis_result["segment_distribution"],
        "most_quantity_customers": analysis_result["segment_quantity"],
        "highest_unit_price_analysis": analysis_result["segment_unit_price"],
        "highest_profit_analysis": analysis_result["segment_profit"],
        "highest_discount_analysis": analysis_result["segment_discount"],
        "most_region_customers": analysis_result["region_distribution"],
        "most_shipping_mode_counts": analysis_result["ship_mode_distribution"],
        "most_common_shipping_time_cost_counts": analysis_result["ship_days_distribution"]
    }

    # Step 3: Generate sales suggestions using ZhipuAI
    response = client.chat.completions.create(
        model="glm-4-plus",
        messages=[
            {"role": "user", "content": f"As a Sales Assistant to help the company, please analyze and generate sales suggestions and advice for the product {category}, with less than 300 words."},
            {"role": "assistant", "content": "Of course, I can help you with that. Could you provide me with some information about the product?"},
            {"role": "user", "content": f"Here are the facts: {known_facts}"}
        ],
    )
    sales_suggestions = response.choices[0].message.content

    return f"The commodity '{commodity_name}' belongs to category '{category}'.\n\nSales Suggestions:\n{sales_suggestions}"

# Create Gradio interface
iface = gr.Interface(
    fn=chatbot,
    inputs="text",
    outputs="text",
    title="Sales Assistant Chatbot",
    description="Ask the chatbot about a commodity and get sales suggestions."
)

# Launch the Gradio interface
iface.launch(share=True)