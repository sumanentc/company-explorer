from typing import Type

import requests
from langchain_community.tools.ddg_search import DuckDuckGoSearchRun
from langchain_core.tools import BaseTool
from pydantic import BaseModel, Field
import yfinance as yf
import requests_cache

from dataframe_helper import extract_income_statement_data, extract_earnings_data, extract_balance_sheet_data, \
    extract_cash_flow_data


def get_data_as_string(data):
    temp_data = []
    for map in data:
        for key, value in map.items():
            data_str = f'{key} : {value}'
            temp_data.append(data_str)

    return ', '.join(temp_data)


def get_company_income_statement(year):
    print(f'Inside get_income_statement {year}')
    import streamlit as st
    comp_ticker = st.session_state.selected_ticker
    print(f'{comp_ticker}')
    if comp_ticker:
        api_key = st.secrets["alpha_vantage_api_key"]
        url = f'https://www.alphavantage.co/query?function=INCOME_STATEMENT&symbol={comp_ticker}&apikey={api_key}'
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
        r = requests.get(url, headers=headers)
        annual_data_string = None
        quarterly_data_string = None
        if response := r.json():
            for k, v in response.items():
                if k == 'annualReports':
                    # Filter python objects with list comprehensions
                    annual_data = [x for x in v if year in x['fiscalDateEnding']]
                    if annual_data:
                        annual_data_pivot_table = extract_income_statement_data(annual_data)
                        st.session_state.annual_income_statement = annual_data_pivot_table
                        annual_data_string = get_data_as_string(annual_data)
                elif k == 'quarterlyReports':
                    quarterly_data = [x for x in v if year in x['fiscalDateEnding']]
                    # print(f'quarterly_data {quarterly_data}')
                    if quarterly_data:
                        quarterly_data_pivot_table = extract_income_statement_data(quarterly_data)
                        st.session_state.quarterly_income_statement = quarterly_data_pivot_table
                        quarterly_data_string = get_data_as_string(quarterly_data)
            return (f"Annual Income Statement Data = {annual_data_string} \n\n "
                    f"Quarterly Income Statement Data = {quarterly_data_string}")
    return None


def get_balance_sheet_data(year):
    print(f'Inside get_balance_sheet_data {year}')
    import streamlit as st
    comp_ticker = st.session_state.selected_ticker
    print(f'{comp_ticker}')
    if comp_ticker:
        api_key = st.secrets["alpha_vantage_api_key"]
        url = f'https://www.alphavantage.co/query?function=BALANCE_SHEET&symbol={comp_ticker}&apikey={api_key}'
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
        r = requests.get(url, headers=headers)
        annual_data_string = None
        quarterly_data_string = None
        if response := r.json():
            for k, v in response.items():
                if k == 'annualReports':
                    # Filter python objects with list comprehensions
                    annual_data = [x for x in v if year in x['fiscalDateEnding']]
                    if annual_data:
                        annual_balance_sheet_data_pivot_table = extract_balance_sheet_data(annual_data)
                        st.session_state.annual_balance_sheet = annual_balance_sheet_data_pivot_table
                        annual_data_string = get_data_as_string(annual_data)
                elif k == 'quarterlyReports':
                    quarterly_data = [x for x in v if year in x['fiscalDateEnding']]
                    if quarterly_data:
                        quarterly_balance_sheet_data_pivot_table = extract_balance_sheet_data(quarterly_data)
                        st.session_state.quarterly_balance_sheet = quarterly_balance_sheet_data_pivot_table
                        quarterly_data_string = get_data_as_string(quarterly_data)
            return (f"Annual Balance Sheet Data = {annual_data_string} \n\n "
                    f"Quarterly Balance Sheet Data = {quarterly_data_string}")
    return None


def get_cash_flow(year):
    print(f'Inside get_cash_flow {year}')
    import streamlit as st
    comp_ticker = st.session_state.selected_ticker
    print(f'{comp_ticker}')
    if comp_ticker:
        api_key = st.secrets["alpha_vantage_api_key"]
        url = f'https://www.alphavantage.co/query?function=CASH_FLOW&symbol={comp_ticker}&apikey={api_key}'
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
        r = requests.get(url, headers=headers)
        if response := r.json():
            annual_data_string = None
            quarterly_data_string = None
            for k, v in response.items():
                if k == 'annualReports':
                    if annual_data := [
                        x for x in v if year in x['fiscalDateEnding']
                    ]:
                        annual_cash_flow_data_pivot_table = extract_cash_flow_data(annual_data)
                        st.session_state.annual_cash_flow = annual_cash_flow_data_pivot_table
                        annual_data_string = get_data_as_string(annual_data)
                elif k == 'quarterlyReports':
                    if quarterly_data := [
                        x for x in v if year in x['fiscalDateEnding']
                    ]:
                        quarterly_cash_flow_data_pivot_table = extract_cash_flow_data(quarterly_data)
                        st.session_state.quarterly_cash_flow = quarterly_cash_flow_data_pivot_table
                        quarterly_data_string = get_data_as_string(quarterly_data)
            return (f"Annual Cash Flow Data = {annual_data_string} \n\n "
                    f"Quarterly Cash Flow Data = {quarterly_data_string}")

    return None


def get_earnings(year):
    print(f'Inside get_earnings {year}')
    import streamlit as st
    comp_ticker = st.session_state.selected_ticker
    print(f'{comp_ticker}')
    if comp_ticker:
        api_key = st.secrets["alpha_vantage_api_key"]
        url = f'https://www.alphavantage.co/query?function=EARNINGS&symbol={comp_ticker}&apikey={api_key}'
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
        r = requests.get(url, headers=headers)
        if response := r.json():
            annual_data_string = None
            quarterly_data_string = None
            for k, v in response.items():
                if k == 'annualEarnings':
                    if annual_data := [
                        x for x in v if year in x['fiscalDateEnding']
                    ]:
                        # print(annual_data)
                        annual_earnings_data_pivot_table = extract_earnings_data(annual_data)
                        st.session_state.annual_earnings_data = annual_earnings_data_pivot_table
                        annual_data_string = get_data_as_string(annual_data)
                elif k == 'quarterlyEarnings':
                    if quarterly_data := [
                        x for x in v if year in x['fiscalDateEnding']
                    ]:
                        # print(quarterly_data)
                        quarterly_earnings_data_pivot_table = extract_earnings_data(quarterly_data)
                        st.session_state.quarterly_earnings_data = quarterly_earnings_data_pivot_table
                        quarterly_data_string = get_data_as_string(quarterly_data)
            return (f"Annual Earnings Data = {annual_data_string} \n\n "
                    f"Quarterly Earnings Data = {quarterly_data_string}")
    return None


def get_company_overview(query) -> str:
    """Search the company overview
    Args:
        query: The input query which we want to search.
    """
    print(f'Inside get_company_overview ')
    import streamlit as st
    comp_ticker = st.session_state.selected_ticker
    print(f'{comp_ticker}')
    session = requests_cache.CachedSession('yfinance.cache')
    session.headers[
        'User-agent'] = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'
    ticker_data = yf.Ticker(comp_ticker, session)
    if ticker_data:
        return ticker_data.info.get('longBusinessSummary')
    return None


def search_general(query) -> str:
    """Search the internet. useful for when you need to search some information that is missing or you are not able to understand
    Args:
        query: The input query which we want to search.
    """
    return DuckDuckGoSearchRun().run(f"{query}")


def search_news(query):
    print(f'Inside get_news {query}')
    import streamlit as st
    comp_ticker = st.session_state.selected_ticker
    print(f'{comp_ticker}')
    if comp_ticker:
        api_key = st.secrets["alpha_vantage_api_key"]
        url = f'https://www.alphavantage.co/query?function=NEWS_SENTIMENT&tickers={comp_ticker}&apikey={api_key}&limit=10&sort=RELEVANCE'
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
        selected_news = []
        selected_news_list = []
        try:
            r = requests.get(url, headers=headers)
            news = r.json()
            if news and news.get('feed'):
                for curr_news in news.get('feed'):
                    selected_comp_news = None
                    for tick in curr_news.get('ticker_sentiment'):
                        if tick.get('ticker') == comp_ticker:
                            selected_comp_news = True
                            break
                    if selected_comp_news:
                        selected_news.append(f"{curr_news.get('summary')} , "
                                             f"Sentiment: {curr_news.get('overall_sentiment_label')})")
                        selected_news_list.append(f"[{curr_news.get('title')}]({curr_news.get('url')})")
                        if len(selected_news) >= 5:
                            break
        except Exception as e:
            print(f'Exception occurred {e}')
        if not selected_news:
            return search_general(query)
        else:
            st.session_state.selected_news = selected_news_list
            return '\n'.join(selected_news)


class CustomYearInput(BaseModel):
    """Inputs for get_company_income_statement"""
    year: str = Field(description="Year e.g. 2023")


class CompanyIncomeStatementTool(BaseTool):
    name = "get_company_income_statement"
    description = """
        Get the annual and quarterly income statements for the company, with normalized fields mapped to GAAP and IFRS taxonomies of the SEC. 
        It contains company's yearly or quarterly earnings and financials. Useful to answer questions about company's performance, annual income,
         revenue growth, financial performance over a specific period, assessing profitability, growth.
         It has the following data points available. 
         ["GrossProfit", "TotalRevenue", "NetIncome", "OperatingIncome", "NetInterestIncome", "CostOfRevenue","InterestIncome",
         "InterestExpense", "IncomeBeforeTax", "InterestAndDebtExpense", "Ebit", "Ebitda"] for a fiscal date
        """
    args_schema: Type[BaseModel] = CustomYearInput

    def _run(self, year: str):
        return get_company_income_statement(year)

    def _arun(self, year: str):
        raise NotImplementedError("get_company_income_statement does not support async")


class CustomQueryInput(BaseModel):
    """Inputs for search_general"""
    query: str = Field(description="query to search e.g. how is the weather")


class CompanyInformationTool(BaseTool):
    name = "get_company_overview"
    description = """
        Company Overview. useful for when you need to answer questions about company overview or basic information 
        about the company
        """
    args_schema: Type[BaseModel] = CustomQueryInput

    def _run(self, query: str):
        return get_company_overview(query)

    def _arun(self, query: str):
        raise NotImplementedError("get_company_overview does not support async")


class CompanyBalanceSheetTool(BaseTool):
    name = "get_balance_sheet_data"
    description = """
        Get the annual and quarterly balance sheets for the company, with normalized fields mapped to GAAP and IFRS taxonomies of the SEC.
        useful to answer questions about company's annual prospects, financial stability, financial position, creditworthiness, balance sheet
        It has the following data points available.
        ["reportedCurrency", "totalAssets", "totalCurrentAssets", "inventory", "currentNetReceivables","totalLiabilities",
         "totalCurrentLiabilities", "currentAccountsPayable", "currentDebt", "shortTermDebt", "longTermDebt"] 
         for a fiscal date
        """
    args_schema: Type[BaseModel] = CustomYearInput

    def _run(self, year: str):
        return get_balance_sheet_data(year)

    def _arun(self, year: str):
        raise NotImplementedError("get_balance_sheet_data does not support async")


class CompanyCashFlowTool(BaseTool):
    name = "get_cash_flow"
    description = """
        Get the annual and quarterly cash flow for the company, with normalized fields mapped to GAAP and IFRS taxonomies of the SEC.
        useful for when you need to answer questions about company's annual cash generation, liquidity, and financial health, cash position.
        It has the following data points available.
        ["reportedCurrency", "operatingCashflow", "netIncome", "profitLoss", "capitalExpenditures","dividendPayout",
         "changeInOperatingLiabilities", "changeInOperatingAssets", "cashflowFromInvestment"] 
         for a fiscal date
        """
    args_schema: Type[BaseModel] = CustomYearInput

    def _run(self, year: str):
        return get_cash_flow(year)

    def _arun(self, year: str):
        raise NotImplementedError("get_cash_flow does not support async")


class CompanyEarningsTool(BaseTool):
    name = "get_earnings"
    description = """
        Get the annual and quarterly earnings (EPS) for the company. Quarterly data also includes analyst estimates and surprise metrics.
        useful for when you need to answer questions about long-term perspective on a company's financial health, strategic direction, and governance..
        It has the following data points available.
        ["fiscalDateEnding", "reportedEPS", "estimatedEPS", "reportedDate"] 
         for a fiscal date
        """
    args_schema: Type[BaseModel] = CustomYearInput

    def _run(self, year: str):
        return get_earnings(year)

    def _arun(self, year: str):
        raise NotImplementedError("get_earnings does not support async")


class SearchTool(BaseTool):
    name = "search_general"
    description = """
        Search the internet. useful for when you need to search some information that is missing or you are not able to understand
        """
    args_schema: Type[BaseModel] = CustomQueryInput

    def _run(self, query: str):
        return search_general(query)

    def _arun(self, query: str):
        raise NotImplementedError("search_general does not support async")


class SearchCompanyNewsTool(BaseTool):
    name = "search_news"
    description = """
        Search for recent news related to company.
        """
    args_schema: Type[BaseModel] = CustomQueryInput

    def _run(self, query: str):
        return search_news(query)

    def _arun(self, query: str):
        raise NotImplementedError("search_news does not support async")
