import streamlit as st

from llm_agent import get_company_name, get_ticker, execute_user_query, get_company_information

# with st.sidebar:
#     openai_api_key = st.text_input("OpenAI API Key", key="chatbot_api_key", type="password")
#     "[Get an OpenAI API key](https://platform.openai.com/account/api-keys)"
#     "[View the source code](https://github.com/streamlit/llm-examples/blob/main/Chatbot.py)"
#     "[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/streamlit/llm-examples?quickstart=1)"


st.title("👲Company Explorer")
st.write("Company Explorer, is a versatile tool for in-depth research on publicly traded companies."
         " Whether you're seeking information or considering an investment, it offers features like company analysis, income statement and balance sheet access, and simplification of financial terminology."
         " This app aims to improve your understanding of the company you're interested in.")


def get_selected_ticker():
    session_tickers = st.session_state.tickers
    if session_tickers and len(session_tickers) > 1:
        values = []
        for key, val in session_tickers.items():
            values.append(key)
        selected_ticker = st.radio(
            "We found multiple companies with similar ticker symbol or name. Please change below 👇 options to use a different company.",
            options=values, format_func=lambda x: session_tickers[x] if x != '' else '',
            key="company_selected", captions=values)
        return selected_ticker, session_tickers[selected_ticker]
    else:
        return list(session_tickers.items())[0]


company_name = None
follow_up_question = False
with st.form("my_form"):
    query = st.text_input("Enter your Query:", "Analyse the income of Infosys for this year")
    submitted = st.form_submit_button("Submit")
    openai_api_key = api_key = st.secrets["openai_api_key"]
    if not openai_api_key:
        st.info("Please add your OpenAI API key to continue.")
    elif submitted:
        st.empty()
        st.session_state.openai_api_key = openai_api_key
        company_name_resp = get_company_name(query, openai_api_key)
        print(company_name_resp)
        if company_name_resp and company_name_resp['company_present']:
            if 'tickers' in st.session_state:
                del st.session_state['tickers']
            if 'selected_ticker' in st.session_state:
                del st.session_state['selected_ticker']
            if 'company_name' in st.session_state:
                del st.session_state['company_name']
            if 'matched_token' in st.session_state:
                del st.session_state['matched_token']

            api_key = st.secrets["alpha_vantage_api_key"]
            matched_token = company_name_resp['name']
            tickers = get_ticker(matched_token, api_key)
            if not tickers:
                st.error("I'm sorry, I couldn't find any information for the above company")
                st.stop()
            st.session_state.tickers = tickers
            st.session_state.matched_token = matched_token
        if not company_name_resp or not company_name_resp['company_present']:
            if 'company_name' in st.session_state:
                follow_up_question = True
            else:
                st.error("I'm sorry, I didn't quite understand your input."
                         " I can only help you with Company related queries.")
                st.stop()

if 'tickers' in st.session_state:
    ticker = get_selected_ticker()
    company_name = ticker[1]
    st.session_state.company_name = company_name
    session_tickers = st.session_state.tickers
    selected_ticker = ticker[0]
    print(f'selected ticker: {selected_ticker}')
    st.session_state.selected_ticker = selected_ticker

    st.write(f"""
            #### :orange[{company_name}]
            
            """)

    # Company Overview
    if not follow_up_question:
        with st.status("""###### Generating Company Information""", expanded=True) as status:
            company_info = get_company_information(f'Provide an Overview about {company_name}.', openai_api_key)
            st.write(company_info.get('output'))
            status.update(label="""###### Company Overview""", state="complete", expanded=True)

    with st.status("""###### Analyzing your Question""", expanded=True) as status:
        resp1 = execute_user_query(query, openai_api_key)
        if resp1.get('output'):
            st.write(f'''```{resp1.get('output')}\n```''')
        status.update(label="""###### Answer""", state="complete", expanded=True)

    # Company Income
    if 'annual_income_statement' in st.session_state:
        st.markdown(''' ###### :blue[Annual Income Statement]''')
        pivot_table = st.session_state.annual_income_statement
        st.dataframe(pivot_table, column_order=(
            "GrossProfit", "TotalRevenue", "NetIncome", "OperatingIncome", "NetInterestIncome", "CostOfRevenue",
            "InterestIncome", "InterestExpense", "IncomeBeforeTax", "InterestAndDebtExpense", "Ebit",
            "Ebitda"), column_config={
            "Fiscal-Date": st.column_config.DateColumn(
                "Date",
                format="YYYY-MM-DD",
            )
        }, use_container_width=True)
        del st.session_state['annual_income_statement']

    if 'quarterly_income_statement' in st.session_state:
        st.markdown(''' ###### :blue[Quarterly Income Statement]''')
        pivot_table = st.session_state.quarterly_income_statement
        st.dataframe(pivot_table, column_order=(
            "GrossProfit", "TotalRevenue", "OperatingIncome", "NetInterestIncome", "NetIncome", "CostOfRevenue",
            "InterestIncome", "InterestExpense", "IncomeBeforeTax", "InterestAndDebtExpense", "Ebit",
            "Ebitda"), column_config={
            "Fiscal-Date": st.column_config.DateColumn(
                "Date",
                format="YYYY-MM-DD",
            )
        }, use_container_width=True)
        del st.session_state['quarterly_income_statement']

    # Earnings
    if 'annual_earnings_data' in st.session_state:
        st.markdown(''' ###### :blue[Annual Earnings]''')
        pivot_table = st.session_state.annual_earnings_data
        st.dataframe(pivot_table, column_config={
            "Fiscal-Date": st.column_config.DateColumn(
                "Date",
                format="YYYY-MM-DD",
            )
        }, use_container_width=True)
        del st.session_state['annual_earnings_data']

    if 'quarterly_earnings_data' in st.session_state:
        st.markdown(''' ###### :blue[Quarterly Earnings]''')
        pivot_table = st.session_state.quarterly_earnings_data
        st.dataframe(pivot_table, column_config={
            "Fiscal-Date": st.column_config.DateColumn(
                "Date",
                format="YYYY-MM-DD",
            )
        }, use_container_width=True)
        del st.session_state['quarterly_earnings_data']

    # Balance Sheet
    if 'annual_balance_sheet' in st.session_state:
        st.markdown(''' ###### :blue[Annual Balance Sheet]''')
        pivot_table = st.session_state.annual_balance_sheet
        st.dataframe(pivot_table, column_config={
            "Fiscal-Date": st.column_config.DateColumn(
                "Date",
                format="YYYY-MM-DD",
            )
        }, use_container_width=True)
        del st.session_state['annual_balance_sheet']

    if 'quarterly_balance_sheet' in st.session_state:
        st.markdown(''' ###### :blue[Quarterly Balance Sheet]''')
        pivot_table = st.session_state.quarterly_balance_sheet
        st.dataframe(pivot_table, column_config={
            "Fiscal-Date": st.column_config.DateColumn(
                "Date",
                format="YYYY-MM-DD",
            )
        }, use_container_width=True)
        del st.session_state['quarterly_balance_sheet']

    # Cash Flow
    if 'annual_cash_flow' in st.session_state:
        st.markdown(''' ###### :blue[Annual Cash Flow]''')
        pivot_table = st.session_state.annual_cash_flow
        st.dataframe(pivot_table, column_config={
            "Fiscal-Date": st.column_config.DateColumn(
                "Date",
                format="YYYY-MM-DD",
            )
        }, use_container_width=True)
        del st.session_state['annual_cash_flow']

    if 'quarterly_cash_flow' in st.session_state:
        st.markdown(''' ###### :blue[Annual Cash Flow]''')
        pivot_table = st.session_state.quarterly_cash_flow
        st.dataframe(pivot_table, column_config={
            "Fiscal-Date": st.column_config.DateColumn(
                "Date",
                format="YYYY-MM-DD",
            )
        }, use_container_width=True)
        del st.session_state['quarterly_cash_flow']

    # News
    if 'selected_news' in st.session_state:
        st.markdown(''' ###### :orange[News]''')
        selected_news = st.session_state.selected_news
        for curr_news in selected_news[:6]:
            st.markdown(f'''{curr_news}\n''', unsafe_allow_html=True)
