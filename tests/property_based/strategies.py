from decimal import Decimal

from hypothesis import strategies as st


# Monetary values use two decimal places to match the Django model.
money = st.decimals(
    min_value=Decimal("0.00"),
    max_value=Decimal("1000000.00"),
    places=2,
    allow_nan=False,
    allow_infinity=False,
)


positive_money = st.decimals(
    min_value=Decimal("0.01"),
    max_value=Decimal("1000000.00"),
    places=2,
    allow_nan=False,
    allow_infinity=False,
)


valid_deposit_amounts = st.decimals(
    min_value=Decimal("10.00"),
    max_value=Decimal("1000000.00"),
    places=2,
    allow_nan=False,
    allow_infinity=False,
)


invalid_deposit_amounts = st.decimals(
    min_value=Decimal("0.00"),
    max_value=Decimal("9.99"),
    places=2,
    allow_nan=False,
    allow_infinity=False,
)


valid_interest_rates = st.decimals(
    min_value=Decimal("0.00"),
    max_value=Decimal("100.00"),
    places=2,
    allow_nan=False,
    allow_infinity=False,
)


positive_interest_rates = st.decimals(
    min_value=Decimal("0.01"),
    max_value=Decimal("100.00"),
    places=2,
    allow_nan=False,
    allow_infinity=False,
)


interest_frequencies = st.integers(
    min_value=1,
    max_value=12,
)