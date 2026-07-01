import pandas as pd
import numpy as np
import yfinance as yf
from pathlib import Path
from scipy.optimize import minimize

class PortfolioOptimizer:
    def __init__(self, tickers):
        self.tickers = tickers
        self.prices = None
        self.returns = None
    
    def download_data(self, start_date, end_date):
        self.start_date = start_date
        self.end_date = end_date

        
        self.prices = yf.download(self.tickers, start=start_date, end=end_date)["Close"]
        if isinstance(self.prices, pd.Series):
            self.prices = self.prices.to_frame()
        self.prices = self.prices.dropna()

    def calculate_returns(self):
        if self.prices is None:
            raise ValueError("価格データがありません。download_dataを先に実行してください。")
        self.returns = self.prices.pct_change().dropna()
        return self.returns
    
    def portfolio_returns(self, weights):
        if self.returns is None:
            raise ValueError("リターンデータがありません。calculate_returnsを先に実行してください。")
        portfolio_returns = self.returns @ weights
        return portfolio_returns
    
    def mean_returns(self):
        if self.returns is None:
            raise ValueError("リターンデータがありません。calculate_returnsを先に実行してください。")
        mean_returns =  self.returns.mean()
        return mean_returns

    def covariance_matrix(self):
        if self.returns is None:
            raise ValueError("リターンデータがありません。calculate_returnsを先に実行してください。")
        covariance_matrix = self.returns.cov()
        return covariance_matrix
    
    def optimize_portfolio(self):
        if self.returns is None:
            raise ValueError("リターンデータがありません。calculate_returnsを先に実行してください。")
        mu = self.mean_returns().values * 252
        cov = self.covariance_matrix().values * 252

        n = len(mu)
        weights = np.ones(n) / n

        def portfolio_variance(weights):
            return weights.T @ cov @ weights * 252
        
        def negative_sharpe(weights):
            portfolio_return = weights @ mu
            portfolio_risk = np.sqrt(weights @ cov @ weights)

            return - portfolio_return / portfolio_risk

        constraints = {
            "type": "eq",
            "fun": lambda weights: np.sum(weights) - 1
        }

        bounds = [(0, 1) for _ in range(n)]

        result = minimize(
            negative_sharpe,
            weights,
            method="SLSQP",
            bounds=bounds,
            constraints=constraints            
        )
        if not result.success:
            raise ValueError("最適化に失敗しました: " + result.message)

        return result.x
    
    def portfolio_performance(self, weights):

        mu = self.mean_returns().values * 252
        cov = self.covariance_matrix().values * 252

        portfolio_return = weights @ mu
        portfolio_risk = np.sqrt(weights @ cov @ weights)
        sharpe = portfolio_return / portfolio_risk

        return portfolio_return, portfolio_risk, sharpe

    
if __name__ == "__main__":
    import numpy as np
    import pandas as pd
    import yfinance as yf
    from scipy.optimize import minimize

    tickers = ["AAPL", "MSFT", "GOOG", "META"]

    pf = PortfolioOptimizer(tickers)

    pf.download_data(start_date="2020-01-01", end_date="2024-01-01")
    pf.calculate_returns()

    weights = pf.optimize_portfolio()

    print("最適ウェイト:")
    for t, w in zip(tickers, weights):
        print(f"{t}: {w:.4f}")

    print(pf.returns.std() * np.sqrt(252))
    print(pf.covariance_matrix() * 252)

    ret, risk, sharpe = pf.portfolio_performance(weights)




    print(f"期待リターン: {ret:.4f}")
    print(f"リスク: {risk:.4f}")
    print(f"シャープレシオ: {sharpe:.4f}")



