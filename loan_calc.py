
def calculate_loan_payment(interest: float, term: float, present_value: float) -> float:
    """
    Calculates the monthly payment for a loan.

    Args:
        interest (float): The annual interest rate as a percentage (e.g., 5 for 5%).
        term (float): The loan term in years.
        present_value (float): The principal loan amount (present value).

    Returns:
        float: The monthly loan payment.
    """
    if interest < 0:
        raise ValueError("Interest rate cannot be negative.")
    if term <= 0:
        raise ValueError("Loan term must be greater than zero.")
    if present_value <= 0:
        raise ValueError("Present value must be greater than zero.")

    # Convert annual interest rate (percentage) to monthly decimal rate
    # Example: 5% annual -> 0.05 / 12 monthly
    monthly_interest_rate = (interest / 100) / 12

    # Convert loan term from years to months
    number_of_payments = term * 12

    if monthly_interest_rate == 0:
        # If the interest rate is 0, the payment is simply principal divided by the number of payments.
        monthly_payment = present_value / number_of_payments
    else:
        # Formula for loan payment (annuity payment formula):
        # M = P [ i(1 + i)^n ] / [ (1 + i)^n � 1]
        # Where:
        # M = Monthly payment
        # P = Principal loan amount (present_value)
        # i = Monthly interest rate (monthly_interest_rate)
        # n = Number of payments (number_of_payments)
        
        # This can also be written as:
        # M = P * (i * (1 + i)**n) / (((1 + i)**n) - 1)
        
        factor = (1 + monthly_interest_rate)**number_of_payments
        monthly_payment = present_value * (monthly_interest_rate * factor) / (factor - 1)

    return monthly_payment