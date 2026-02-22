# Bond YTM calculator

---

## Project Overview

This application allows for the calculation of the yield-to-maturity of bonds. The user is sequentially prompted to provide the current bond price, maturity date, coupon yield, and annual coupon frequency. This information allows for the internal rate of return (yield-to-maturity) according to:

$$ f(r)=\sum_{i=1}^{n}\frac{C_i}{\left( 1+r \right)^{t_{i}}}-P=0 $$

The application then uses the Newton-Raphson Method to find the roots of the corresponding net present value polynomial.

$$ r_{n+1} = r_{n} - \frac{f\left( r_{n} \right)}{f'\left( r_{n} \right)} $$