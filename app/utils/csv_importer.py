import os
import pandas as pd


def process_stock_data(file_path):
    from app import db
    from app.models import StockPrice
    
    try:
        # Extract ticker from filename (e.g., NVDA.csv -> NVDA)
        ticker = os.path.basename(file_path).replace(".csv", "")

        # Load CSV data
        df = pd.read_csv(file_path, skiprows=3, header=None, names=['Date', 'Close', 'High', 'Low', 'Open', 'Volume'])
        df['Date'] = pd.to_datetime(df['Date'])
        
        print(f"Processing data for {ticker}:")
        print(df.head())  # print the first few rows
        # Prepare data for batch insertion
        stock_entries = []
        for _, row in df.iterrows():
            stock_entry = StockPrice(
                ticker=ticker,
                date=row['Date'],
                open=row['Open'],
                high=row['High'],
                low=row['Low'],
                close=row['Close'],
                volume=row['Volume']
            )
            stock_entries.append(stock_entry)

        # Batch insert into database
        db.session.bulk_save_objects(stock_entries)
        db.session.commit()
        print(f"Successfully inserted {len(stock_entries)}")
    except Exception as e:
        db.session.rollback()
        print(f"Error processing {file_path}: {e}")

def import_all_stocks(folder_path):
    # Iterate over all CSV files in the folder
    for filename in os.listdir(folder_path):
        if filename.endswith(".csv"):
            file_path = os.path.join(folder_path, filename)
            process_stock_data(file_path)