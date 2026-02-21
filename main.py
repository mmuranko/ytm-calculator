from datetime import date

current_date = date.today()

# 1. Bond Parameter Input

face_value = 100

while True:
    while True:
        try:
            price_input = input("Enter today's Market Price: ")
            price = float(price_input)

            if price <= 0:
                print("Error: Market Price must be larger than 0")
                continue
            break

        except ValueError:
            print("Error: Invalid input")

    while True:
        try:
            issue_input = input("Enter Issue Date (YYYY-MM-DD): ")
            issue_date = date.fromisoformat(issue_input)

            if issue_date > current_date:
                print("Error: Issue date must be in the past")
                continue
            break

        except ValueError:
            print("Error: Invalid input")

    while True:
        try:
            maturity_input = input("Enter Maturity Date (YYYY-MM-DD): ")
            maturity_date = date.fromisoformat(maturity_input)

            if maturity_date < current_date:
                print("Error: Maturity date must be in the future")
                continue
            break

        except ValueError:
            print("Error: Invalid input")

    while True:
        try:
            coupon_input = input("Enter Coupon Rate (%): ")
            coupon_rate = float(coupon_input) / 100

            if coupon_rate < 0:
                print("Error: Coupon Rate cannot be negative")
                continue
            break

        except ValueError:
            print("Error: Invalid input")

    while True:
        try:
            frequency_input = input("Enter Annual Coupon Frequency (1, 2, 4, or 12): ")
            frequency = int(frequency_input)

            if frequency not in [1, 2, 4, 12]:
                 print("Error: Frequency must be 1, 2, 4, or 12")
                 continue
            break

        except ValueError:
            print("Error: Invalid input")


# 2. Cash Flow Reconstruction

    # Find the number of days from issuance until maturity
    maturity_days = (maturity_date - issue_date).days

    # Find the number of days between coupon payments
    coupon_period_days = 365 / frequency

    # Calculate exact number of periods by rounding off the leap-year remainder
    total_periods = round(maturity_days / coupon_period_days)

    # Create a list of all coupon payment dates, expressed as "days since issuance".
    cash_flow_days = []
    for i in range(total_periods):
        cash_flow_days.append(maturity_days - (i * coupon_period_days))

    # Reverse the list, such that the first entry refers to the first cash flow
    cash_flow_days.reverse()

    # Find the total number of cash flows
    cash_flow_count = len(cash_flow_days)

    cash_flow_amounts = []
    i = 0

    while i < cash_flow_count:
        if i == 0:
            cash_flow_stub = (face_value * coupon_rate * cash_flow_days[0]) / 365

            # Edge case: check if the first cash flow is also the last
            # If so, add the face value as well
            if cash_flow_count == 1:
                cash_flow_stub = cash_flow_stub + face_value

            cash_flow_amounts.append(cash_flow_stub)

        elif i < (cash_flow_count - 1):
            cash_flow_other = (face_value * coupon_rate) / frequency
            cash_flow_amounts.append(cash_flow_other)

        else: 
            cash_flow_final = face_value + ((face_value * coupon_rate) / frequency)
            cash_flow_amounts.append(cash_flow_final)

        i = i + 1

# 3. Future Cash Flows from Today

    # Find the number of days from issuance until today
    today_days = (current_date - issue_date).days

    # Create new lists to hold only the future cash flows
    future_days = []
    future_amounts = []

    # Loop through both original lists simultaneously
    for day, amount in zip(cash_flow_days, cash_flow_amounts):

        # Only look at days strictly in the future
        # Adjust day count to: days from today
        if day > today_days:
            days_from_today = day - today_days

            future_days.append(days_from_today)
            future_amounts.append(amount)

    # Safety Check for Matured Bonds
    if len(future_days) == 0:
        print("Error: This bond has already matured\n")
        continue

# 4. Find YTM using Newton_Raphson Method

    def net_present_value(days_list, cashflow_list, rate, price):
        npv = -price
        for day, cashflow in zip(days_list, cashflow_list):
            npv = npv + (cashflow / ((1 + rate / frequency)**(frequency * (day / 365))))
        return npv

    def get_derivative(days_list, cashflow_list, rate):
        derivative = 0
        for day, cashflow in zip(days_list, cashflow_list):
            derivative = derivative + -(frequency * (day / 365)) * (cashflow / frequency) / ((1 + rate / frequency)**(frequency * (day / 365) + 1))
        return derivative

    rate = 0.02
    tolerance = 1e-7 
    max_iterations = 1000

    iteration = 0
    while iteration < max_iterations:
        npv_value = net_present_value(future_days, future_amounts, rate, price)
        derivative_value = get_derivative(future_days, future_amounts, rate)
        
        new_rate = rate - (npv_value / derivative_value)
        
        if abs(new_rate - rate) < tolerance:
            break
            
        rate = new_rate
        iteration += 1

    print(f"Converged after {iteration} iterations.")
    print(f"YTM = {rate * 100:.2f}%")

    print("-" * 30)
    choice = input("Type 'Q' to quit or press any button to restart: ").lower()
    if choice == 'q':
        break
    print("-" * 30)