import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

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