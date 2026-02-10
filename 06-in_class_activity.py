from datetime import date, timedelta
import pandas as pd
import plotly.express as px
import streamlit as st
import yfinance as yf

# CONSTANTS
END = date.today()
START = END - timedelta(365)

# data handling
@st.cache_data
def get_stock_data(ticker, start, end):
    try:
        data = yf.download(ticker, start, end, auto_adjust=False)
        if data.empty:
            return None, f"No data found for {ticker}"
        if isinstance(data.columns, pd.MultiIndex):
            data.columns = data.columns.get_level_values(0)
        return data, f"Successfully loaded data for {ticker}"
    except Exception as e:
        return None, f"Error {e}"

#add title
st.title('Stock Analysis')
#set main ticker to apple
ticker = st.sidebar.text_input('Main Ticker', 'AAPL').upper().strip()
#set comparison ticker to SPY
comparison_ticker = st.sidebar.text_input('Comparison Ticker', 'SPY').upper().strip()
#create run button
run_button = st.sidebar.button('Run')

if run_button:
    #load stock data and start/end message for main ticker
    df, msg = get_stock_data(ticker, START, END)
    #load SPY data and start/end message for comparison ticker
    comparison_df, comp_msg = get_stock_data(comparison_ticker, START, END)
    #display messages
    st.sidebar.write(msg)
    st.sidebar.write(comp_msg)
    #If no data in main ticker or comparison data frame: error
    if df is None or comparison_df is None:
        st.error('Could not load tickers')
        st.stop()

    #make sure dates of the stock data are the same, so find a common one and stick with that
    common = df.index.intersection(comparison_df.index)
    df = df.loc[common].copy()
    comparison_df = comparison_df.loc[common].copy()
    #normalize stock prices for better comparison
    df['Normalized_Close'] = (df['Close'] / df['Close'].iloc[0]) * 100
    comparison_df['Normalized_Close'] = (comparison_df['Close'] / comparison_df['Close'].iloc[0]) * 100

    #create tabs for price, data, info and comparison
    tab1, tab2, tab3, tab4 = st.tabs(['Price', 'Data', 'Info', '📈Comparison'])

    #edit comparison tab
    with tab4:
        #create a plot to compare the data set current date pull main ticker & comparison ticker values
        comp_plot = pd.DataFrame({
            'Date': df.index,
            ticker: df['Normalized_Close'].values,
            comparison_ticker: comparison_df['Normalized_Close'].values
        }).melt(id_vars = 'Date', var_name="Ticker", value_name="Normalized Close")
        #Create line plot using the stock comparison data, set x to date and y to normalized close price of the two stocks, and add a title
        fig = px.line(
            comp_plot,
            x='Date',
            y='Normalized Close',
            color='Ticker',
            title=f"{ticker} vs {comparison_ticker} Performance (Base 100)"
        )
        st.plotly_chart(fig, use_container_width=True)
        #create table below to compare the stats, data from main and comparison ticker, the minimum close for both, max close for both and final close for both compared
        stats = pd.DataFrame({
            'Ticker': [ticker, comparison_ticker],
            'Min': [df['Normalized_Close'].min(), comparison_df['Normalized_Close'].min()],
            'Max': [df['Normalized_Close'].max(), comparison_df['Normalized_Close'].max()],
            'Final': [df['Normalized_Close'].iloc[-1], comparison_df['Normalized_Close'].iloc[-1]],
        })
        st.dataframe(stats, use_container_width=True)



