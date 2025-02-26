from flask import Blueprint, jsonify
from app.models import StockPrice
from app.utils.csv_importer import import_all_stocks
from app import db
from sqlalchemy import text
from app.utils.csv_importer2 import import_all_stocks2
import os
main_routes = Blueprint('main', __name__)
folder_path = os.path.abspath('data/stocks')
@main_routes.route('/')
def home():
    return "Stock Data API!"

@main_routes.route('/check-db', methods=['GET'])
def check_db():
    try:
        db.session.execute(text('SELECT 1'))
        return "Database connection is successful!"
    except Exception as e:
        return f"Database connection failed: {str(e)}", 500

@main_routes.route('/stocks', methods=['GET'])
def get_stocks():
    stock_data = StockPrice.query.all()
    return jsonify([data.to_dict() for data in stock_data])

@main_routes.route('/stocks/<ticker>', methods=['GET'])
def get_stock_data(ticker):
    stock_data = StockPrice.query.filter_by(ticker=ticker).all()
    print(f"Stock data found for {ticker}: {stock_data}") 
    return jsonify([data.to_dict() for data in stock_data])

@main_routes.route('/import', methods=['POST'])
def import_stocks():
    import_all_stocks2('data/stocks')
    return "Data imported successfully!"

#@main_routes.route('/importtest', methods=['POST'])
#def import_stocks():
#    try:
#        import_all_stocks2(folder_path)
#        return "Data import completed!"
 #   except Exception as e:
#        return f"Error during import: {str(e)}", 500
    
@main_routes.route('/health')
def health():
    return "OK", 200    

#@main_routes.route('/stockstest/<ticker>', methods=['GET'])
#def get_stock_data(ticker):
 #   print(f"Fetching data for ticker: {ticker}")
  #  stock_data = StockPrice.query.filter_by(ticker=ticker).all()
   # if not stock_data:
    #    return jsonify({"message": "No data found for ticker"}), 404
    #return jsonify([data.to_dict() for data in stock_data])