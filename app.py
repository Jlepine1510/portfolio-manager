# app.py
import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.express as px

# Initialize portfolio
if 'portfolio' not in st.session_state:
    st.session_state.portfolio = pd.DataFrame(columns=['Ticker', 'Weight'])

# Basic functions
def get_prices(tickers):
    try:
        data = yf.download(tickers, period="1d")['Adj Close']
        return data.iloc[-1] if not data.empty else None
    except:
        return None

# Main interface
st.title("💰 Simple Portfolio Manager")
st.write("Add stocks to see your portfolio breakdown")

# Input section
col1, col2 = st.columns(2)
with col1:
    ticker = st.text_input("Stock Symbol (e.g. AAPL)").upper().strip()
with col2:
    weight = st.number_input("Weight %", min_value=0.0, max_value=100.0, step=1.0)

if st.button("Add Stock") and ticker:
    new_entry = pd.DataFrame([[ticker, weight]], columns=['Ticker', 'Weight'])
    st.session_state.portfolio = pd.concat([st.session_state.portfolio, new_entry])

# Display section
if not st.session_state.portfolio.empty:
    st.subheader("Your Portfolio")
    
    # Get prices
    prices = get_prices(st.session_state.portfolio['Ticker'].tolist())
    
    if prices is not None:
        # Calculate values
        portfolio = st.session_state.portfolio.copy()
        portfolio['Price'] = portfolio['Ticker'].map(prices)
        portfolio['Value'] = portfolio['Weight'] * portfolio['Price']
        
        # Show table
        st.dataframe(portfolio.style.format({'Price': '${:.2f}', 'Value': '${:.2f}'}))
        
        # Show pie chart
        fig = px.pie(portfolio, values='Weight', names='Ticker', 
                    title="Portfolio Allocation", hole=0.3)
        st.plotly_chart(fig)
    else:
        st.warning("⚠️ Couldn't fetch prices. Check internet connection!")