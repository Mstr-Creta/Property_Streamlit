import pandas as pd
import streamlit as st
import math


st.title('Complaints Rgarding Consumer Financial Protection Bureau')
st.subheader("Check your eligibility before planning to buy properties for your personal or business needs, both residential and commercial properties can be mortgaged for availing a loan against property.", divider=True)
st.image("https://img.freepik.com/free-vector/finance-department-employees-are-calculating-expenses-company-s-business_1150-41782.jpg?t=st=1735309876~exp=1735313476~hmac=cb374b2aa6865b6166904b608eb95587680e1f70e2425e388f621fa488c9a5ac&w=1060") 

st.write("## Enter the details of your loan")
col1, col2 = st.columns(2)
home_value = col1.number_input("Home Value", value=100000)
deposit = col2.number_input("Deposit", value=10000)
interest_rate = st.slider("Interest Rate", min_value=0.0, max_value=10.0, value=5.0, step=0.1)
loan_term = st.slider("Loan Term", min_value=1, max_value=30, value=15, step=1)

st.title('Calculation')
# Calculate the repayments.
loan_amount = home_value - deposit
monthly_interest_rate = (interest_rate / 100) / 12
number_of_payments = loan_term * 12
monthly_payment = (
    loan_amount
    * (monthly_interest_rate * (1 + monthly_interest_rate) ** number_of_payments)
    / ((1 + monthly_interest_rate) ** number_of_payments - 1)
)

# Display the repayments.
total_payments = monthly_payment * number_of_payments
total_interest = total_payments - loan_amount

st.write("### Repayments")
col1, col2, col3 = st.columns(3)
col1.metric(label="Monthly Repayments", value=f"${monthly_payment:,.2f}")
col2.metric(label="Total Repayments", value=f"${total_payments:,.0f}")
col3.metric(label="Total Interest", value=f"${total_interest:,.0f}")


# Create a data-frame with the payment schedule.
schedule = []
remaining_balance = loan_amount

for i in range(1, number_of_payments + 1):
    interest_payment = remaining_balance * monthly_interest_rate
    principal_payment = monthly_payment - interest_payment
    remaining_balance -= principal_payment
    year = math.ceil(i / 12)  # Calculate the year into the loan
    schedule.append(
        [
            i,
            monthly_payment,
            principal_payment,
            interest_payment,
            remaining_balance,
            year,
        ]
    )

df = pd.DataFrame(
    schedule,
    columns=["Month", "Payment", "Principal", "Interest", "Remaining Balance", "Year"],
)

# Display the data-frame as a chart.
st.write("### Payment Schedule")
payments_df = df[["Year", "Remaining Balance"]].groupby("Year").min()
st.line_chart(payments_df)