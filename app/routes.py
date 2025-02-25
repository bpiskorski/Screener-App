from flask import Blueprint, jsonify
from app.models import StockPrice
from app.utils.csv_importer import import_all_stocks
from app import db


main_routes = Blueprint('main', __name__)

@main_routes.route('/')
def home():
    return "Stock Data API!"

@main_routes.route('/test-db')
def test_db():
    try:
        db.engine.execute("SELECT 1")
        return "Database connection successful!"
    except Exception as e:
        return f"Database connection failed: {str(e)}", 500
    
    
@main_routes.route('/stocks', methods=['GET'])
def get_stocks():
    stock_data = StockPrice.query.all()
    return jsonify([data.to_dict() for data in stock_data])

@main_routes.route('/stocks/<ticker>', methods=['GET'])
def get_stock_data(ticker):
    stock_data = StockPrice.query.filter_by(ticker=ticker).all()
    return jsonify([data.to_dict() for data in stock_data])

@main_routes.route('/import', methods=['POST'])
def import_stocks():
    import_all_stocks('app/data')
    return "Data imported successfully!"
    
