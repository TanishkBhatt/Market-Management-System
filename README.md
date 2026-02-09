# Market Management System - Python

A `Python-Based Backend Only Market Management System` is designed to simulate a real-world retail store workflow. The system covers inventory handling, customer management, sales processing, billing, payment support, database storage, and business analytics.

The Project also includes a dedicated data analysis notebook for evaluating financial performance, inventory health, customer influence, and sales trends.

---

## Table of Contents

- [Features](#features)
  - [Inventory Management](#inventory-management)
  - [Customer Management](#customer-management)
  - [Cart and Order System](#cart-and-order-system)
  - [Billing and Payments](#billing-and-payments)
  - [Database Storage](#database-storage)
  - [Feedback System](#feedback-system)
  - [Business Analytics](#business-analytics)
- [Project Structure](#project-structure)
- [Technical Stack Used](#technical-stack-used)
- [How to Run the Project](#how-to-run-the-project)
- [Future Improvements](#future-improvements)
- [Author](#author)

---

## Features

### Inventory Management
- JSON-based inventory system
- Tracks product unit, cost price, selling price, discounts, available stocks, and category
- Automatic stock updates after each successful sale
- Supports global or seasonal discount configuration

---

### Customer Management
- Auto-generated unique customer IDs
- Validation for customer details such as name, age, and gender
- Persistent storage of customer data using CSV files

---

### Cart and Order System
- Add products to cart
- Update quantities or remove items from cart
- Real-time bill calculation
- Per-item discount handling
- Unique order ID generation based on timestamp

---

### Billing and Payments
- Final bill generation with discount application
- Demo QR code generation for UPI-based payments
- Automatic bill text file creation
- Bills stored locally for future reference

---

### Database Storage
All transactional data is stored using CSV-based databases:

- `custumerDB.csv` – Customer information
- `salesDB.csv` – Sales transactions
- `feedbackDB.csv` – Customer ratings and feedback

---

### Feedback System
- Customer rating input on a scale of 0 to 10
- Optional textual feedback
- Persistent storage for analytical use

---

### Business Analytics
The `analysis.ipynb` notebook provides analytical insights using Pandas and Matplotlib, including:

1. Financial performance analysis
2. Inventory health visualization
3. Customer influence metrics :
    - Most frequent product
    - Most demanding category
    - Age wise distribution of custumers
    - Gender wise distribution of custumers
4. Daily sales and income trend analysis

---

## Project Structure

    Market-Management-System/
    │
    ├── main.py
    ├── analysis.ipynb
    │
    ├── src/
    │ ├── inventory.json
    │ ├── methods.py
    |
    ├── DataBase/
    │ ├── custumerDB.csv
    │ ├── salesDB.csv
    │ └── feedbackDB.csv
    │
    ├── QRCodes/
    ├── Payment Bills/
    │
    ├── README.md
    ├── requirements.txt

---

## Technical Stack Used

- Programming Langusge: `Python`
- Standard Libraries: 
    - `json`
    - `csv`
    - `datetime`
    - `random`
- Third-party Libraries:
    - `pandas`
    - `matplotlib`
    - `qrcode`
- For Analysis: `Jupyter Notebook`

---

## How to Run the Project

1. Clone the repository:
   ```bash
   git clone https://github.com/TanishkBhatt/Market-Management-System.git

2. Install required dependencies:
    ```bash
    pip install -r requirements.txt

3. Run the main application:
    ```bash
    python main.py

4. Open the analysis notebook:
    ```bash
    jupyter notebook analysis.ipynb

---

## Future Improvements
- Use of a proper SQL based database
- Integrating a UI along the project
- Use of Machine Learning models for deeper analysis
- Authorisation via Google, etc.

---

## Author

Developed by `Tanishk Bhatt`, a Student and a Programmer of India, as a real-world practice project focused on building production-oriented Python systems and data analysis workflows.

---

## Links

- Portfolio : https://tanishkbhatt.github.io/Portfolio/
- GitHub : https://github.com/TanishkBhatt/
- YouTube : https://www.youtube.com/@TanishkBhatt-x6w/

---
