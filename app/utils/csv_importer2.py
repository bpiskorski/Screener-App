from sqlalchemy.orm import sessionmaker
from app import db
import os 
import pandas as pd
from app.models import StockPrice


def process_stock_data(file_path):
    try:
        ticker = os.path.basename(file_path).replace(".csv", "").upper()
        df = pd.read_csv(file_path, skiprows=3, header=None, names=['Date', 'Close', 'High', 'Low', 'Open', 'Volume'])
        df['Date'] = pd.to_datetime(df['Date'])

        # Create a session using sessionmaker
        Session = sessionmaker(bind=db.engine)
        session = Session()

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
            session.add(stock_entry)

        session.commit()
        print(f"Processed {len(df)} records for {ticker}")
    except Exception as e:
        print(f"Error processing {file_path}: {str(e)}")
        session.rollback()
    finally:
        session.close()
def import_all_stocks2(folder_path):
    # Iterate over all CSV files in the folder
    for filename in os.listdir(folder_path):
        if filename.endswith(".csv"):
            file_path = os.path.join(folder_path, filename)
            process_stock_data(file_path)
