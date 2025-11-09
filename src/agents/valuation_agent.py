import pandas as pd
import numpy as np
from datetime import datetime

# Import the API functions from tools.api module
from src.tools import api as hedge_api


def analyze_valuation(stock, end_date):
    """Run valuation analysis for a single stock."""
    try:
        # Fetch the financial metrics
        financial_metrics = hedge_api.get_financial_metrics(
            ticker=stock,
            end_date=end_date,
            period="ttm",
        )

        # Add safety check for financial metrics
        if not financial_metrics:
            return {"signal": "neutral", "confidence": 0}

        metrics = financial_metrics[0]

        # Fetch the specific line_items that we need for valuation purposes
        financial_line_items = hedge_api.search_line_items(
            ticker=stock,
            line_items=[
                "free_cash_flow",
                "net_income",
                "depreciation_and_amortization",
                "capital_expenditure",
                "working_capital",
            ],
            end_date=end_date,
            period="ttm",
            limit=2,
        )

        # Add safety check for financial line items
        if len(financial_line_items) < 2:
            return {"signal": "neutral", "confidence": 0}

        # Pull the current and previous financial line items
        current_financial_line_item = financial_line_items[0]
        previous_financial_line_item = financial_line_items[1]

        # Calculate working capital change
        working_capital_change = (
            current_financial_line_item.working_capital
            - previous_financial_line_item.working_capital
        )

        # Owner Earnings Valuation (Buffett Method)
        owner_earnings_value = calculate_owner_earnings_value(
            net_income=current_financial_line_item.net_income,
            depreciation=current_financial_line_item.depreciation_and_amortization,
            capex=current_financial_line_item.capital_expenditure,
            working_capital_change=working_capital_change,
            growth_rate=metrics.earnings_growth,
            required_return=0.15,
            margin_of_safety=0.25,
        )

        # DCF Valuation
        dcf_value = calculate_intrinsic_value(
            free_cash_flow=current_financial_line_item.free_cash_flow,
            growth_rate=metrics.earnings_growth,
            discount_rate=0.10,
            terminal_growth_rate=0.03,
            num_years=5,
        )

        # Get the market cap
        market_cap = hedge_api.get_market_cap(ticker=stock, end_date=end_date)

        # Calculate combined valuation gap (average of both methods)
        dcf_gap = (dcf_value - market_cap) / market_cap
        owner_earnings_gap = (owner_earnings_value - market_cap) / market_cap
        valuation_gap = (dcf_gap + owner_earnings_gap) / 2

        if valuation_gap > 0.15:  # More than 15% undervalued
            signal = "bullish"
        elif valuation_gap < -0.15:  # More than 15% overvalued
            signal = "bearish"
        else:
            signal = "neutral"

        # Create the reasoning
        reasoning = {}
        reasoning["dcf_analysis"] = {
            "signal": (
                "bullish"
                if dcf_gap > 0.15
                else "bearish"
                if dcf_gap < -0.15
                else "neutral"
            ),
            "details": f"Intrinsic Value: ${dcf_value:,.2f}, Market Cap: ${market_cap:,.2f}, Gap: {dcf_gap:.1%}",
        }

        reasoning["owner_earnings_analysis"] = {
            "signal": (
                "bullish"
                if owner_earnings_gap > 0.15
                else "bearish"
                if owner_earnings_gap < -0.15
                else "neutral"
            ),
            "details": f"Owner Earnings Value: ${owner_earnings_value:,.2f}, Market Cap: ${market_cap:,.2f}, Gap: {owner_earnings_gap:.1%}",
        }

        confidence = round(abs(valuation_gap), 2) * 100

        return {
            "signal": signal,
            "confidence": confidence,
            "reasoning": reasoning,
        }

    except Exception as e:
        print(f"Error in valuation analysis for {stock}: {e}")
        return {"signal": "neutral", "confidence": 0}


def calculate_owner_earnings_value(
    net_income: float,
    depreciation: float,
    capex: float,
    working_capital_change: float,
    growth_rate: float = 0.05,
    required_return: float = 0.15,
    margin_of_safety: float = 0.25,
    num_years: int = 5,
) -> float:
    """
    Calculates the intrinsic value using Buffett's Owner Earnings method.

    Owner Earnings = Net Income
                    + Depreciation/Amortization
                    - Capital Expenditures
                    - Working Capital Changes
    """
    if not all(
        [
            isinstance(x, (int, float))
            for x in [net_income, depreciation, capex, working_capital_change]
        ]
    ):
        return 0

    # Calculate initial owner earnings
    owner_earnings = net_income + depreciation - capex - working_capital_change

    if owner_earnings <= 0:
        return 0

    # Project future owner earnings
    future_values = []
    for year in range(1, num_years + 1):
        future_value = owner_earnings * (1 + growth_rate) ** year
        discounted_value = future_value / (1 + required_return) ** year
        future_values.append(discounted_value)

    # Calculate terminal value (using perpetuity growth formula)
    terminal_growth = min(growth_rate, 0.03)  # Cap terminal growth at 3%
    terminal_value = (future_values[-1] * (1 + terminal_growth)) / (
        required_return - terminal_growth
    )
    terminal_value_discounted = terminal_value / (1 + required_return) ** num_years

    # Sum all values and apply margin of safety
    intrinsic_value = sum(future_values) + terminal_value_discounted
    value_with_safety_margin = intrinsic_value * (1 - margin_of_safety)

    return value_with_safety_margin


def calculate_intrinsic_value(
    free_cash_flow: float,
    growth_rate: float = 0.05,
    discount_rate: float = 0.10,
    terminal_growth_rate: float = 0.02,
    num_years: int = 5,
) -> float:
    """
    Computes the discounted cash flow (DCF) for a given company based on the current free cash flow.
    """
    # Estimate the future cash flows based on the growth rate
    cash_flows = [free_cash_flow * (1 + growth_rate) ** i for i in range(num_years)]

    # Calculate the present value of projected cash flows
    present_values = []
    for i in range(num_years):
        present_value = cash_flows[i] / (1 + discount_rate) ** (i + 1)
        present_values.append(present_value)

    # Calculate the terminal value
    terminal_value = (
        cash_flows[-1]
        * (1 + terminal_growth_rate)
        / (discount_rate - terminal_growth_rate)
    )
    terminal_present_value = terminal_value / (1 + discount_rate) ** num_years

    # Sum up the present values and terminal value
    dcf_value = sum(present_values) + terminal_present_value

    return dcf_value
