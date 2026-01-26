def calculate_loan_payment(interest, term, present_value):
    """
    Calculates the monthly loan payment.

    Args:
        interest (float): Annual interest rate (e.g., 5 for 5%).
        term (int): Loan term in years.
        present_value (float): The principal loan amount (present value).

    Returns:
        float: The monthly loan payment amount.
    """
    monthly_interest_rate = interest / 12 / 100  # Convert annual percentage to monthly decimal
    num_payments = term * 12

    if monthly_interest_rate == 0:
        if num_payments == 0:
            return 0.0  # Or raise an error for an invalid term
        payment = present_value / num_payments
    else:
        # PMT = (P * r) / (1 - (1 + r)^-n)
        payment = (present_value * monthly_interest_rate) / (1 - (1 + monthly_interest_rate)**(-num_payments))
    
    return payment