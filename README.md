# EquilPy: Bioethanol Flash Drum Simulator ⚗️💻

EquilPy is a desktop-based Vapor-Liquid Equilibrium (VLE) simulator specifically designed to analyze the phase separation of bioethanol mixtures (Ethanol-Water). This project is built using Object-Oriented Programming (OOP) architecture in Python to model thermodynamic streams and solve mass balances numerically.

The application utilizes a modular approach by separating the graphical user interface (GUI), the thermodynamic calculation engine, and database integration for the physical properties of chemical components.

## 🚀 Key Features
* **Database-Driven Properties:** Pure component vapor pressure data (Antoine Constants) and binary interactions are fetched dynamically from an SQLite database using Pandas.
* **Numerical Convergence:** Implements the Rachford-Rice algorithm to iteratively solve the vapor-liquid phase mass balance (V/F) convergence.
* **Dual Thermodynamic Models:**
  * **Ideal Systems:** Calculations using Raoult's Law.
  * **Non-Ideal Systems:** Thermodynamic activity coefficient approach using the Van Laar model.
* **Interactive GUI:** A visual interface built with PyQt6, complete with error handling to prevent system crashes from invalid user inputs.

## 🧮 Thermodynamic Models & Mathematical Equations
EquilPy utilizes a series of fundamental chemical engineering equations to execute mass balance and phase equilibrium calculations.

**1. Pure Component Vapor Pressure (Antoine Equation)**
Calculates the pure component vapor pressure (\(P^{sat}_i\)) at operating temperature \(T\) using the natural logarithm (adjusted to the reference literature basis):

$$P^{sat}_i = \exp\left(A_i - \frac{B_i}{T + C_i}\right)$$

2. Activity Coefficient (Van Laar Model)
For non-ideal systems, intermolecular interactions ($\gamma$) are calculated using the binary interaction matrix from the Van Laar equation:

$$\gamma_1 = \exp\left(\frac{A_{12}}{\left(1 + \frac{A_{12} x_1}{A_{21} x_2}\right)^2}\right)$$

$$\gamma_2 = \exp\left(\frac{A_{21}}{\left(1 + \frac{A_{21} x_2}{A_{12} x_1}\right)^2}\right)$$

3. Equilibrium Ratio (K-Value)
Determines the relative volatility of each component using Modified Raoult's Law (for ideal systems, the value is $\gamma_i = 1$):

$$K_i = \frac{\gamma_i P^{sat}_i}{P_{total}}$$

4. Mass Balance Convergence (Rachford-Rice Equation)
Solved numerically using the Bisection method to find the vapor fraction ($V/F$) where the objective function equals zero:

$$f\left(\frac{V}{F}\right) = \sum_{i=1}^{n} \frac{z_i (K_i - 1)}{1 + \frac{V}{F} (K_i - 1)} = 0$$

5. Liquid ($x_i$) and Vapor ($y_i$) Phase Distribution
Once the vapor fraction $V/F$ converges, the mole fraction composition of each component in each phase is calculated using:

$$x_i = \frac{z_i}{1 + \frac{V}{F} (K_i - 1)}$$

$$y_i = K_i x_i$$

## 📂 Architecture Structure (MVC)
This project separates the calculation logic and user interface into several modules:
* `main_app.py` : Main execution module and PyQt6 interface (View/Controller).
* `units.py` : Unit operation calculator logic (Flash Drum) and numerical thermodynamic solver.
* `stream.py` : OOP object constructor for modeling the physical properties of mass streams (Temperature, Pressure, Flow Rate, Mole Fraction).
* `db_handler.py` : Connection script bridging the simulation engine with the SQLite database.
* `properties.db` : Local database storage.
* `EquilPy Notebook.ipynb` : Dedicated Jupyter Notebook for database administrator functions (adding new chemical components).

## 🛠️ Technologies Used
* **Primary Language:** Python 3
* **Numerical Computation:** NumPy
* **Data Manipulation:** Pandas
* **Database:** SQLite3
* **Graphic User Interface:** PyQt6

## ⚙️ How to Run the Application
1. Ensure Python 3 is installed on your device.
2. Clone this repository to your local machine.
3. Install the required libraries by running the following command in your terminal:
   ```bash
   pip install pandas numpy PyQt6
   ```
4. Run the application via the main execution file:
   ```bash
   python main_app.py
   ```

## 🗺️ Future Roadmap
This project is under active development. Upcoming features planned for the next release (v1.1+) include:
- [ ] Addition of a `Mixer` class for multi-stream mixing integration.
- [ ] Addition of a `Heater/Cooler` module with heat capacity (\(C_p\)) integration.
- [ ] Expansion to distillation column simulation (stage-wise separation).
- [ ] Development of a GUI "Database Manager" tab to allow users to add new components without using a Jupyter Notebook.
