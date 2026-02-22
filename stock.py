import datetime as dt #computes default start/end dates
import matplotlib.pyplot as plt #import plotting library
import matplotlib.ticker as mtick #format for axis ticks (e.g. percent signs)
import numpy as np #numerical operations (e.g. log, exp)
import pandas as pd #data frames and time series operations
import seaborn as sb #plot styling
import yfinance as yf  # Assuming yfinance for data API, download stock prices

sb.set_theme()

"""
STUDENT CHANGE LOG & AI DISCLOSURE:
----------------------------------
1. Did you use an LLM (ChatGPT/Claude/etc.)? [Yes/No]
Yes, Chat GPT
2. If yes, what was your primary prompt?
"I want to create an python object named 'stock'. I want it to be able to use yfinance 
to download stock price data, pandas for the date format, matplotlib for plotting, datetime, and seaborn for plot styling. 
I want to be able to 1. get data by pulling free stock data from yfinance and storing it in pandas data frame 2. I want to 
find the change between stock close prices from day to day and the daily instantaneous rate of return 3. I want to calculate 
moving averages and plot them, 4. i want to plot a histogram of the instantaneous returns and 5. I want to plot a line graphs 
of the stocks performance over the range of data collected and stored in the pandas data frame as a percent gain/loss. 
How should I begin creating my first method, get_data in my object stock.py"
----------------------------------
"""
#pull last year of data
#default_start = today's date - 365 days
DEFAULT_START = dt.date.isoformat(dt.date.today() - dt.timedelta(365))
#default_end = today's date
DEFAULT_END = dt.date.isoformat(dt.date.today())

#Create Stock object
class Stock:
    def __init__(self, symbol, start=DEFAULT_START, end=DEFAULT_END):
        #store symbol, start date, end date in stock object
        self.symbol = symbol
        self.start = start
        self.end = end
        #download and prepare data when object has been defined
        self.data = self.get_data()

    def get_data(self):
        """Downloads data from yfinance and triggers return calculation."""
        # TODO: Use yf.download(self.symbol, start=self.start, end=self.end)
        #yf.download pulls daily open, high, low, close, volume data
        #set auto_adjust to False so 'Close' and 'Adj Close' are presented seperately
        data = yf.download(self.symbol, start=self.start, end=self.end, progress=False, auto_adjust=False)

        #error if invalid date range or if no data found for symbol
        if data is None or data.empty:
            raise ValueError(f'No data found for {self.symbol}')

        #convert df to index in pandas datetime format so time-series tool works
        data.index = pd.to_datetime(data.index)
        #name the index for future plots and so its easily identifiable
        data.index.name = 'Date'

        #Keep only OHLCV columns
        columns = [c for c in ["Open", "High", "Low", "Close", "Adj Close", "Volume"] if c in data.columns]
        data = data[columns]

        #add computed columns to the data frame
        self.calc_returns(data)
        return data


    def calc_returns(self, df):
        # Requirement: Use vectorized pandas operations, not loops.
        #make sure df has close price data
        if "Close" not in df.columns:
            raise KeyError("DataFrame must have a 'Close' column.")

        #df['close'].diff() = today's close - yesterday's close for each row
        df["Change"] = df["Close"].diff()
        #compute instant return using natural log of close prices, then subtract rows, and round to nearest 4th decimal
        df["InstantReturn"] = np.log(df["Close"]).diff().round(4)


    
    def add_technical_indicators(self, windows=[20, 50]):
        """
        Add Simple Moving Averages (SMA) for the given windows
        to the internal DataFrame. Produce a plot showing the closing price and SMAs.
        """
        #make sure data is loaded
        if self.data is None or self.data.empty:
            raise ValueError("No data available for {self.data}")
        #make sure you have close price to compute moving averages
        if "Close" not in self.data.columns:
            raise KeyError("'Close' column needed to calculate simple moving averages.")

        #for each time period/'window' create a new column with a rolling mean
        for w in windows:
            # include window in column name so it's possible to have multiple SMA's
            col = f'Simple Moving Average ({w})'
            #compute the mean of the last 'w' number of rows
            self.data[col] = self.data["Close"].rolling(window=w).mean()

        #plot stock close price data
        ax = self.data['Close'].plot(figsize=(12, 6), linewidth=2, title=f'{self.symbol} Close & SMAs')

       #Plot each SMA on the same axes (ax)
        #wasnt sure if just adding moving averages to the object and plots so I also plotted SMA's and close prices
        for w in windows:
            self.data[f'Simple Moving Average ({w})'].plot(ax=ax, linewidth=1.5)

        #create labels
        ax.set_xlabel("Date")
        ax.set_ylabel("Price ($)")
        #make the plot readable with grid adjustments
        ax.grid(True, alpha=0.3)
        #add legend labels for each row
        ax.legend(["Close"] + [f'Simple Moving Average ({w})' for w in windows])
        #make sure labels don't get cut off
        plt.tight_layout()
        #display plot window
        plt.show()



    def plotreturndist(self, bins=50):
        '''
        plot a histogram of InstantReturn Values
        shows how daily returns are distributed
        bins control how many bars the histogram has
        '''

        #dropna() removes missing values
        series = self.data["InstantReturn"].dropna()
        #create figure and axes
        fig, ax = plt.subplots(figsize=(10, 5))
        #create histogram to count how many returns fall in each bins range
        ax.hist(series, bins=bins)

        #add labels and make plot readable
        ax.set_title(f'{self.symbol} Instant Return Distribution')
        ax.set_xlabel('Instant Returns')
        ax.set_ylabel('Frequency')
        ax.grid(True, alpha=0.3)
        #more layout adjustments and show plot
        plt.tight_layout()
        plt.show()

    def plot_performance(self):
        """Plots cumulative growth of $1 investment."""
        #find growth/multiplier by adding log returns over time and converting them into a multiplier
        growth = np.exp(self.data["InstantReturn"].fillna(0).cumsum())
        #convert multiplier into percent change
        percent = (growth - 1.0) * 100.0

        #create figure and axes
        fig, ax = plt.subplots(figsize=(12, 6))
        #create plot to show percent change
        ax.plot(percent.index, percent.values)

        #create labels
        ax.set_title(f'{self.symbol} Performance (Percent Gain/Loss)')
        ax.set_xlabel("Date")
        ax.set_ylabel("Return (%)")
        # us set_major_formatter to define range of values 1-100 by default
        ax.yaxis.set_major_formatter(mtick.PercentFormatter())

        #more style adjustments
        ax.grid(True, alpha=0.3)
        plt.tight_layout()
        #show plot
        plt.show()

        pass


def main():
    #test
   test = Stock("GOOGL")

   print(test.data.head())

   test.plotreturndist()
   test.plot_performance()
   test.add_technical_indicators()


if __name__ == "__main__":
    main()