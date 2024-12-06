from flask import Flask, jsonify, request, render_template
import pandas as pd

app = Flask(__name__)

# Load data from Excel file
FILE_PATH = 'sampledatafoodsales_analysis.xlsx'
SHEET_NAME = 'FoodSales'
data = pd.read_excel(FILE_PATH, sheet_name=SHEET_NAME)
data['Date'] = data['Date'].astype(str)  # Convert Date column to string for easy filtering

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_data', methods=['GET'])
def get_data():
    return jsonify(data.to_dict(orient='records'))

@app.route('/filter_data', methods=['GET'])
def filter_data():
    start_date = request.args.get('startDate')
    end_date = request.args.get('endDate')
    city = request.args.get('city')
    category = request.args.get('category')

    filtered_data = data.copy()

    if start_date:
        filtered_data = filtered_data[filtered_data['Date'] >= start_date]
    if end_date:
        filtered_data = filtered_data[filtered_data['Date'] <= end_date]
    if city:
        filtered_data = filtered_data[filtered_data['City'] == city]
    if category:
        filtered_data = filtered_data[filtered_data['Category'] == category]

    return jsonify(filtered_data.to_dict(orient='records'))

if __name__ == '__main__':
    app.run()
