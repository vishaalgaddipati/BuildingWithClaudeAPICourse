def greeting():
    print("Hi there")


def calculate_pi():
    """
    Calculate pi to the 5th decimal place using the Machin formula.
    π/4 = 4*arctan(1/5) - arctan(1/239)
    
    Returns:
        float: Pi rounded to 5 decimal places (3.14159)
    """
    from decimal import Decimal, getcontext
    
    # Set precision high enough to get accurate 5 decimal places
    getcontext().prec = 50
    
    def arctan(x, num_terms=100):
        """Calculate arctan using Taylor series."""
        x = Decimal(x)
        result = Decimal(0)
        for n in range(num_terms):
            term = ((-1) ** n) * (x ** (2 * n + 1)) / (2 * n + 1)
            result += term
        return result
    
    # Machin formula: π/4 = 4*arctan(1/5) - arctan(1/239)
    pi = 4 * (4 * arctan(Decimal(1) / Decimal(5)) - arctan(Decimal(1) / Decimal(239)))
    
    # Round to 5 decimal places
    pi_5_digits = round(float(pi), 5)
    return pi_5_digits