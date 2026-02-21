# Bond YTM calculator

---

## Project Overview

This application allows for the calculation of the yield-to-maturity of bonds. The user is sequentially prompted to provide the current bond price, maturity date, coupon yield, and annual coupon frequency. The application then uses the Newton-Raphson method to solve the corresponding net present value polynomial. 

$$ r_{n+1} = r_{n} - \frac{f\left( r_{n} \right)}{f\left( r_{n} \right)} $$