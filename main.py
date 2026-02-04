from datetime import date

current_date = date.today()
face_value = 1000

while True:
    while True:
        try:
            price_input = input("Enter today's Market Price: ")
            price = float(price_input) * 10

            if price <= 0:
                print("Error: Market Price must be larger than 0")
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

    delta_time = maturity_date - current_date
    delta_days = delta_time.days

    print(f"The difference is {delta_days} days.")

    coupon_period_days = 365 / frequency

    days = delta_days
    cash_flow_dates = []

    while days > 0:
        cash_flow_dates.append(days)
        days = days - coupon_period_days

    cash_flow_dates.reverse()

    print(cash_flow_dates)

    cash_flow_count = len(cash_flow_dates)

    cash_flow_amounts = []
    i = 0

    while i < cash_flow_count:
        if i == 0:
            cash_flow_one = (coupon_rate * face_value * cash_flow_dates[0]) / (frequency * 365)
            cash_flow_amounts.append(cash_flow_one)
        elif i < (cash_flow_count - 1):
            cash_flow_other = (coupon_rate * face_value) / frequency
            cash_flow_amounts.append(cash_flow_other)
        else: 
            cash_flow_other = ((1 + coupon_rate) * face_value) / frequency
            cash_flow_amounts.append(cash_flow_other)
        i = i + 1

    print(cash_flow_amounts)

    def net_present_value(days_list, cashflow_list, rate, price):
        npv = -price
        for day, cashflow in zip(days_list, cashflow_list):
            npv = npv + (cashflow / ((1 + rate)**(day / 365)))
        return npv

    def get_derivative(days_list, cashflow_list, rate):
        derivative = 0
        for day, cashflow in zip(days_list, cashflow_list):
            derivative = derivative + -(day / 365) * (cashflow / ((1 + rate)**(day / 365 + 1)))
        return derivative

    rate = 0.02
    tolerance = 1e-7 
    max_iterations = 100

    iteration = 0
    while iteration < max_iterations:
        npv_value = net_present_value(cash_flow_dates, cash_flow_amounts, rate, price)
        derivative_value = get_derivative(cash_flow_dates, cash_flow_amounts, rate)
        
        new_rate = rate - (npv_value / derivative_value)
        
        if abs(new_rate - rate) < tolerance:
            break
            
        rate = new_rate
        iteration += 1

    print(f"Converged after {iteration} iterations.")
    print(f"IRR = {rate * 100:.2f}%")

    print("-" * 30)
    choice = input("Type 'Q' to quit or press any button to restart: ").lower()
    if choice == 'q':
        break
    print("-" * 30)