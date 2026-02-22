from datetime import date
from dateutil.relativedelta import relativedelta

# 1. Bond Parameter Input

face_value = 100

while True:
    while True:
        try:
            price_input = input("(1/6) Enter Settlement Price (incl. accr. interest): ")
            price = float(price_input)

            if price <= 0:
                print("Error: Market Price must be larger than 0")
                continue
            break

        except ValueError:
            print("Error: Invalid input")

    while True:
        try:
            settlement_input = input("(2/6) Enter Settlement Date (YYYY-MM-DD): ")
            settlement_date = date.fromisoformat(settlement_input)

            break

        except ValueError:
            print("Error: Invalid input")

    while True:
        try:
            issue_input = input("(3/6) Enter Issue Date (YYYY-MM-DD): ")
            issue_date = date.fromisoformat(issue_input)

            if issue_date > settlement_date:
                print("Error: Issue date must be in the past")
                continue
            break

        except ValueError:
            print("Error: Invalid input")

    while True:
        try:
            maturity_input = input("(4/6) Enter Maturity Date (YYYY-MM-DD): ")
            maturity_date = date.fromisoformat(maturity_input)

            if maturity_date < settlement_date:
                print("Error: Maturity date must be in the future")
                continue
            break

        except ValueError:
            print("Error: Invalid input")

    while True:
        try:
            coupon_input = input("(5/6) Enter Coupon Rate (%): ")
            coupon_rate = float(coupon_input) / 100

            if coupon_rate < 0:
                print("Error: Coupon Rate cannot be negative")
                continue
            break

        except ValueError:
            print("Error: Invalid input")

    while True:
        try:
            frequency_input = input("(6/6) Enter Annual Coupon Frequency (1, 2, 4, or 12): ")
            frequency = int(frequency_input)

            if frequency not in [1, 2, 4, 12]:
                 print("Error: Frequency must be 1, 2, 4, or 12")
                 continue
            break

        except ValueError:
            print("Error: Invalid input")


# 2. Cash Flow Reconstruction (Dates and Amounts)

    # Calculate exactly how many months make up one coupon period
    months_per_period = int(12 / frequency)
    
    cash_flow_dates = []
    settlement_date_iter = maturity_date
    
    # Walk backward from maturity to find exact calendar dates of all coupons
    while settlement_date_iter > issue_date:
        cash_flow_dates.append(settlement_date_iter)
        settlement_date_iter -= relativedelta(months=months_per_period)
    
    # Reverse the list so the dates go from oldest to newest
    cash_flow_dates.reverse()
    cash_flow_count = len(cash_flow_dates)

    # Pre-calculate the regular coupon amount
    regular_coupon = (face_value * coupon_rate) / frequency

    # Determine the first coupon amount (checking for a true stub)
    exact_previous_period = cash_flow_dates[0] - relativedelta(months=months_per_period)
    
    if issue_date == exact_previous_period:
        # The issue date aligns perfectly with a standard coupon cycle (No stub)
        stub_coupon = regular_coupon
    else:
        # It is a true stub period (short or long)
        stub_days = (cash_flow_dates[0] - issue_date).days
        stub_coupon = face_value * coupon_rate * (stub_days / 365.0)

    # Build the full array of cash flow amounts cleanly
    all_amounts = [stub_coupon] + [regular_coupon] * (cash_flow_count - 1)
    
    # Add the principal to the final payment
    all_amounts[-1] = all_amounts[-1] + face_value


# 3. Future Cash Flows and Exact Time Periods

    future_w_periods = []
    future_amounts = []

    # Zip pairs the full history of dates and amounts together perfectly
    for cf_date, amount in zip(cash_flow_dates, all_amounts):
        
        # Filter: We only care about cash flows happening after today
        if cf_date > settlement_date:
            
            # Exact days from today until the cash flow hits
            days_from_today = (cf_date - settlement_date).days
            
            # Convert days into exact fractional coupon periods (Actual/365 convention)
            w_period = (days_from_today / 365.0) * frequency
            
            future_w_periods.append(w_period)
            future_amounts.append(amount)

    # Safety Check for Matured Bonds
    if not future_w_periods:
        print("Error: This bond has already matured\n")
        continue

    # Display Expected Cash Flows
    print("\n" + "=" * 45)
    print(" EXPECTED FUTURE CASH FLOWS")
    print("=" * 45)
    print(f"{'Days from Settlement':<22} | {'Amount':<20}")
    print("-" * 45)

    for w, amount in zip(future_w_periods, future_amounts):
        # Reverse the w math to get approximate days back, rounded to nearest integer
        display_days = round((w / frequency) * 365)
        
        # Format the amount to 2 decimal places
        display_amount = f"{amount:.2f}"
        
        print(f"{display_days:<22} | {display_amount:<20}")

    print("=" * 45 + "\n")


# 4. Find YTM using Newton_Raphson Method

    def net_present_value(w_periods, cashflows, rate, price):
        npv = -price
        for w, cf in zip(w_periods, cashflows):
            npv = npv + cf / ((1 + rate / frequency)**w)
        return npv

    def get_derivative(w_periods, cashflows, rate):
        derivative = 0
        for w, cf in zip(w_periods, cashflows):
            derivative = derivative - (w * cf / frequency) / ((1 + rate / frequency)**(w + 1))
        return derivative

    rate = 0.02
    tolerance = 1e-7 
    max_iterations = 1000

    iteration = 0
    while iteration < max_iterations:
        npv_value = net_present_value(future_w_periods, future_amounts, rate, price)
        derivative_value = get_derivative(future_w_periods, future_amounts, rate)
        
        new_rate = rate - (npv_value / derivative_value)
        
        if abs(new_rate - rate) < tolerance:
            break
            
        rate = new_rate
        iteration = iteration + 1

    print(f"YTM = {rate * 100:.2f}%")

    print("-" * 30)
    choice = input("Type 'Q' to quit or press any button to restart: ").lower()
    if choice == 'q':
        break
    print("-" * 30)