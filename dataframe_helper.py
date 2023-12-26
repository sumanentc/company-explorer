import numpy as np
import pandas as pd


def extract_income_statement_data(data):
    df = pd.DataFrame.from_records(data)
    # print(f'data -> {df}')
    df = df.apply(pd.to_numeric, errors='ignore')
    df = df.astype({'reportedCurrency': 'str'})
    df["fiscalDateEnding"] = pd.to_datetime(df["fiscalDateEnding"], format="%Y-%m-%d")
    df.rename(columns={'fiscalDateEnding': 'Fiscal-Date', 'reportedCurrency': 'Currency',
                       'grossProfit': 'GrossProfit', 'totalRevenue': 'TotalRevenue',
                       'costOfRevenue': 'CostOfRevenue',
                       'costofGoodsAndServicesSold': 'CostofGoodsAndServicesSold',
                       'operatingIncome': 'OperatingIncome',
                       'sellingGeneralAndAdministrative': 'SellingGeneralAndAdministrative',
                       'researchAndDevelopment': 'ResearchAndDevelopment',
                       'operatingExpenses': 'OperatingExpenses',
                       'investmentIncomeNet': 'InvestmentIncomeNet',
                       'netInterestIncome': 'NetInterestIncome',
                       'interestIncome': 'InterestIncome',
                       'interestExpense': 'InterestExpense',
                       'nonInterestIncome': 'NonInterestIncome',
                       'otherNonOperatingIncome': 'OtherNonOperatingIncome',
                       'depreciation': 'Depreciation',
                       'depreciationAndAmortization': 'DepreciationAndAmortization',
                       'incomeBeforeTax': 'IncomeBeforeTax',
                       'incomeTaxExpense': 'IncomeTaxExpense',
                       'interestAndDebtExpense': 'InterestAndDebtExpense',
                       'netIncomeFromContinuingOperations': 'NetIncomeFromContinuingOperations',
                       'comprehensiveIncomeNetOfTax': 'ComprehensiveIncomeNetOfTax',
                       'ebit': 'Ebit',
                       'ebitda': 'Ebitda', 'netIncome': 'NetIncome', }, inplace=True)
    df = df.replace(to_replace='None', value=np.nan)
    df.dropna(axis=1, inplace=True)
    df.sort_values(by='Fiscal-Date', ascending=False)
    return pd.pivot_table(data=df, index=['Currency', 'Fiscal-Date'], sort=False)


def extract_earnings_data(data):
    df = pd.DataFrame.from_records(data)
    # print(f'data -> {df}')
    df = df.drop(['reportedDate'], axis=1, errors='ignore')
    df = df.apply(pd.to_numeric, errors='ignore')
    df["fiscalDateEnding"] = pd.to_datetime(df["fiscalDateEnding"], format="%Y-%m-%d")
    df.rename(columns={'fiscalDateEnding': 'Fiscal-Date', 'reportedEPS': 'EPS'}, inplace=True)
    df = df.replace(to_replace='None', value=np.nan)
    df.dropna(axis=1, inplace=True)
    df.sort_values(by='Fiscal-Date', ascending=False)
    return pd.pivot_table(data=df, index=['Fiscal-Date'], sort=False)


def extract_balance_sheet_data(data):
    df = pd.DataFrame.from_records(data)
    df = df.apply(pd.to_numeric, errors='ignore')
    df = df.astype({'reportedCurrency': 'str'})
    df["fiscalDateEnding"] = pd.to_datetime(df["fiscalDateEnding"], format="%Y-%m-%d")
    df.rename(columns={'fiscalDateEnding': 'Fiscal-Date', 'reportedCurrency': 'Currency',
                       'totalAssets': 'TotalAssets', 'totalCurrentAssets': 'TotalCurrentAssets',
                       'inventory': 'Inventory',
                       'currentNetReceivables': 'CurrentNetReceivables',
                       'totalLiabilities': 'TotalLiabilities',
                       'totalCurrentLiabilities': 'TotalCurrentLiabilities',
                       'currentAccountsPayable': 'CurrentAccountsPayable',
                       'currentDebt': 'CurrentDebt',
                       'shortTermDebt': 'ShortTermDebt',
                       'longTermDebt': 'LongTermDebt',
                       'totalShareholderEquity': 'TotalShareholderEquity',
                       'shortLongTermDebtTotal': 'ShortLongTermDebtTotal',
                       'commonStockSharesOutstanding': 'CommonStockSharesOutstanding'}, inplace=True)
    df = df.replace(to_replace='None', value=np.nan)
    df.dropna(axis=1, inplace=True)
    df.sort_values(by='Fiscal-Date', ascending=False)
    return pd.pivot_table(data=df, index=['Currency', 'Fiscal-Date'], sort=False)


def extract_cash_flow_data(data):
    df = pd.DataFrame.from_records(data)
    df = df.apply(pd.to_numeric, errors='ignore')
    df = df.astype({'reportedCurrency': 'str'})
    df["fiscalDateEnding"] = pd.to_datetime(df["fiscalDateEnding"], format="%Y-%m-%d")
    df.rename(columns={'fiscalDateEnding': 'Fiscal-Date', 'reportedCurrency': 'Currency',
                       'operatingCashflow': 'OperatingCashflow', 'netIncome': 'NetIncome',
                       'profitLoss': 'ProfitLoss',
                       'paymentsForOperatingActivities': 'PaymentsForOperatingActivities',
                       'proceedsFromOperatingActivities': 'ProceedsFromOperatingActivities',
                       'changeInOperatingLiabilities': 'ChangeInOperatingLiabilities',
                       'changeInOperatingAssets': 'ChangeInOperatingAssets',
                       'depreciationDepletionAndAmortization': 'DepreciationDepletionAndAmortization',
                       'capitalExpenditures': 'CapitalExpenditures',
                       'changeInReceivables': 'ChangeInReceivables',
                       'changeInInventory': 'ChangeInInventory',
                       'cashflowFromInvestment': 'CashflowFromInvestment',
                       'cashflowFromFinancing': 'CashflowFromFinancing',
                       'dividendPayout': 'DividendPayout',
                       'dividendPayoutCommonStock': 'DividendPayoutCommonStock',
                       'dividendPayoutPreferredStock': 'DividendPayoutPreferredStock', }, inplace=True)
    df = df.replace(to_replace='None', value=np.nan)
    df.dropna(axis=1, inplace=True)
    df.sort_values(by='Fiscal-Date', ascending=False)
    return pd.pivot_table(data=df, index=['Currency', 'Fiscal-Date'], sort=False)
