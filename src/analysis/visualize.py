import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd

def plot_rolling_volatility(rolling_vol, title="Rolling Volatility"):
    plt.figure(figsize=(12, 6))
    for col in rolling_vol.columns:
        plt.plot(rolling_vol.index, rolling_vol[col], label=col)
    plt.legend()
    plt.title(title)
    plt.show()

def plot_volatility_heatmap(rolling_vol, title="Normalized Volatility Heatmap", step=100):
    normalized_vol = (rolling_vol - rolling_vol.mean()) / rolling_vol.std() #標準化
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.heatmap(
        normalized_vol.T,
        cmap="YlGnBu",
        xticklabels=False,
        ax=ax)
    xticks = np.arange(0, len(rolling_vol.index), step)
    xticklabels = rolling_vol.index[::step].strftime('%Y-%m-%d')

    ax.set_xticks(xticks)
    ax.set_xticklabels(xticklabels, rotation=45)

    ax.set_title(title)
    plt.show()

def plot_hist_comparison(data_dict, bins=50, title=""):
    plt.figure(figsize=(12, 6))

    for label, series in data_dict.items():
        plt.hist(series.dropna(), bins=bins, alpha=0.5, label=label,density=True)

    plt.legend()
    plt.title(title)
    plt.xlabel("Value")
    plt.ylabel("Frequency")
    plt.show()

def plot_kde_comparison(data_dict, title="", log_scale=False):
    plt.figure(figsize=(12, 6))

    for label, series in data_dict.items():
        series.dropna().plot(kind="kde", label=label)

    if log_scale:
        plt.yscale("log")

    plt.legend()
    plt.title(title)
    plt.xlabel("Value")
    plt.ylabel("Frequency")
    plt.show()

def plot_returns_vol_scatter(returns, rolling_vol, title=""):
    df = pd.concat([returns, rolling_vol], axis=1)
    df = df.dropna()
    df.columns = ["returns", "rolling_vol"]
    plt.scatter(df["returns"].abs(), df["rolling_vol"], alpha=0.5)
    plt.xlabel("Absolute Log Returns")
    plt.ylabel("Rolling Volatility")
    plt.title(title)
    plt.show()
