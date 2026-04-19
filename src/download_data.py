from pathlib import Path
import yfinance as yf
import pandas as pd
from pathlib import Path


DEFAULT_TICKERS = [
    "^GSPC",    # 米国（代表）
    "^IXIC",    # 米国（ハイテク）
    "^DJI",     # 米国（大型株）

    "^N225",    # 日本

    "^FTSE",    # 英国
    "^GDAXI",   # ドイツ

    "^HSI",     # 香港（中国 proxy）

    "^AXJO",    # オーストラリア

    "^BVSP"     # ブラジル（新興国）
]

def download_index_data(
    tickers=None,
    start_date='2007-01-01',
    end_date='2010-12-31',
    save_dir="data/raw",
    file_prefix="indices" 
):
    if tickers is None:
        tickers = DEFAULT_TICKERS
    
    BASE_DIR = Path.cwd().parent
    save_dir = BASE_DIR / "data/raw"
    save_dir.mkdir(parents=True, exist_ok=True)

    df = yf.download(tickers, start=start_date, end=end_date)["Close"]

    file_name = f"{file_prefix}_{start_date}_{end_date}.csv"
    save_path = save_dir / file_name

    df.to_csv(save_path)
    print(f"Data downloaded and saved to {save_path}")
    return df

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Download stock index data")
    parser.add_argument("--start", default="2007-01-01", help="Start date for data download (YYYY-MM-DD)")
    parser.add_argument("--end", default="2010-12-31", help="End date for data download (YYYY-MM-DD)")

    args = parser.parse_args()
    download_index_data(start_date=args.start, end_date=args.end)