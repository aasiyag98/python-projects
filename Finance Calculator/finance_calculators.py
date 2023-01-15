# This is a calculator that allows the user to either calculate their interest
# on an investment or calculate the amount that should be repaid on a home 
# loan each month.

import math

# User has to select which calculator they would like to use.
# Regardless of how the user enters their option, it is converted to a lower-
# case format using '.lower()'
calculator = input('''Choose 'investment' or 'bond' from the menu below: 

investment - to calculate the amount of interest earned on your investment
bond       - to calculate the amount you'll have to pay on a home loan
''')
calculator = calculator.lower()

# Investment calculator prompts user to enter information that will be needed
# for carrying out the calculation.
if calculator == "investment":
    deposit = float(input("How much money are you depositing?: "))
    interest_rate = float(input("Enter the interest rate (number only): "))
    investment_years = int(input("How many years do you plan on investing?: "))
    interest_type = input("Choose either 'simple' or 'compound' interest: ")
    if interest_type == "simple":
        total_amount = round(deposit * (1 + 
                                   (investment_years * (interest_rate/100))),2)
    elif interest_type == "compound":
        total_amount = round(deposit * 
                             ((1 + (interest_rate/100)) ** investment_years),2)
    
    print(f"Total when {interest_type} interest is applied: £{total_amount}")

# Bond calculator prompts user to enter information that will be needed for
# carrying out the calculation.
elif calculator == "bond":
    present_value = float(input("Enter the present value of the house: "))
    interest_rate = float(input("Enter the interest rate (number only): "))
    repayment_months = int(input('''Enter the number of months you plan on 
    taking to repay the bond: '''))

    P = present_value
    i = interest_rate/1200
    n = repayment_months

    repayment = round((i * P)/(1-((1+i)**(-n))),2)

    print(f"You will have to repay £{repayment} each month.")

# If user enters something other than 'investment' or 'bond' calculator, an
# error message appears.
else:
    print("ERROR: You have not entered a correct option.")
