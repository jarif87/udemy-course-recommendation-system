import pandas as pd
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('dashboard.log'),
        logging.StreamHandler()
    ]
)

def getvaluecounts(df):
    try:
        if 'subject' not in df.columns:
            logging.error("Column 'subject' not found in DataFrame")
            return {}
        result = df['subject'].value_counts().to_dict()
        logging.info(f"getvaluecounts result: {result}")
        return result
    except Exception as e:
        logging.error(f"Error in getvaluecounts: {e}")
        return {}

def getlevelcount(df):
    try:
        if 'level' not in df.columns or 'num_subscribers' not in df.columns:
            logging.error("Column 'level' or 'num_subscribers' not found in DataFrame")
            return {}
        result = df.groupby('level')['num_subscribers'].count().to_dict()
        logging.info(f"getlevelcount result: {result}")
        return result
    except Exception as e:
        logging.error(f"Error in getlevelcount: {e}")
        return {}

def getsubjectsperlevel(df):
    try:
        if 'subject' not in df.columns or 'level' not in df.columns:
            logging.error("Column 'subject' or 'level' not found in DataFrame")
            return {}
        grouped = df.groupby(['subject', 'level']).size().to_dict()
        result = {f"{sub}_{lvl}": count for (sub, lvl), count in grouped.items()}
        logging.info(f"getsubjectsperlevel result: {result}")
        return result
    except Exception as e:
        logging.error(f"Error in getsubjectsperlevel: {e}")
        return {}

def yearwiseprofit(df):
    try:
        df = df.copy()
        required_columns = ['price', 'num_subscribers', 'published_timestamp']
        missing_columns = [col for col in required_columns if col not in df.columns]
        if missing_columns:
            logging.error(f"Missing columns: {missing_columns}")
            return {}, {}, {}, {}

        # Convert price to numeric, handle all non-numeric values
        df['price'] = pd.to_numeric(df['price'], errors='coerce').fillna(0.0)
        invalid_prices = df['price'].isna().sum()
        if invalid_prices > 0:
            logging.warning(f"{invalid_prices} invalid prices set to 0.0")

        df['profit'] = df['price'] * df['num_subscribers']

        # Handle timestamps
        df['published_date'] = pd.to_datetime(
            df['published_timestamp'].str.split('T').str[0],
            format="%Y-%m-%d",
            errors='coerce'
        )
        invalid_dates = df['published_date'].isna().sum()
        if invalid_dates > 0:
            logging.warning(f"Dropped {invalid_dates} rows with invalid timestamps")
            logging.debug(f"Invalid timestamps sample: {df[df['published_date'].isna()][['published_timestamp']].head().to_dict()}")
        df = df.dropna(subset=['published_date'])

        if df.empty:
            logging.error("No valid data after timestamp processing")
            return {}, {}, {}, {}

        # Extract datetime components
        df['Year'] = df['published_date'].dt.year
        df['Month_name'] = df['published_date'].dt.month_name()

        # Aggregations
        profitmap = df.groupby('Year')['profit'].sum().to_dict()
        subscribersmap = df.groupby('Year')['num_subscribers'].sum().to_dict()
        profitmonthwise = df.groupby('Month_name')['profit'].sum().to_dict()
        monthwisesub = df.groupby('Month_name')['num_subscribers'].sum().to_dict()

        logging.info(f"yearwiseprofit results: profitmap={profitmap}, subscribersmap={subscribersmap}, "
                     f"profitmonthwise={profitmonthwise}, monthwisesub={monthwisesub}")
        return profitmap, subscribersmap, profitmonthwise, monthwisesub
    except Exception as e:
        logging.error(f"Error in yearwiseprofit: {e}")
        return {}, {}, {}, {}