# Supply Chain Analytics with Python

## 📌 Project Overview
This repository explores the impact of **supply chain efficiency** on customer behavior and sales performance in the e-commerce sector using the **DataCo Global Supply Chain dataset**.  

Two Python workflows are included:  

1. **Customer Behavior Analysis** → Calculates **Churn Rate**, **Customer Retention Rate (CRR)**, and **Repeat Purchase Rate (RPR)**, along with visualizations to evaluate how delivery performance affects customer loyalty.  
2. **Optimized Regression Analysis** → Performs a **Multiple Linear Regression (MLR)** to quantify the effect of supply chain variables (e.g., shipping days, discount rate, delivery risk) on **sales per customer**.  

---

## 🛠️ Tools & Libraries Used
- **Python 3**
- **Pandas** → Data cleaning, transformation, aggregation  
- **NumPy** → Numerical computations  
- **Matplotlib & Seaborn** → Data visualizations  
- **Datetime** → Time-based calculations  
- **Statsmodels** → Regression analysis (OLS)  
- **OpenPyXL** → Export results to Excel  

---

## 📂 Dataset
The project uses the **DataCo Global Supply Chain Dataset**, which includes:  
- Customer IDs and Segments  
- Order & Shipping Dates  
- Delivery Status and Risks  
- Product Pricing, Discounts, and Quantities  
- Regional and Market Segments  
- Sales per Customer  

---

## 📊 Analysis & Metrics

### 🔹 Part 1: Customer Behavior Analysis
- **Churn Rate** → % of customers lost due to poor delivery performance (Late/Cancelled orders).  
- **Customer Retention Rate (CRR)** → % of customers retained month-over-month.  
- **Repeat Purchase Rate (RPR)** → % of customers making more than one purchase.  

**Visualizations:**
- Churn by Delivery Status (bar chart)  
- Retention Rate Over Time (line chart)  
- Repeat Purchases Distribution (histogram)  
- Retention by Delivery Status (bar chart)  

---

### 🔹 Part 2: Regression Analysis
- **Variables Considered**: Sales, Quantity, Product Price, Discount Rate, Days for Shipping, Delivery Risk, Customer Segment, Market, Category.  
- **Steps**:  
  1. Aggregate data by customer.  
  2. Encode categorical variables.  
  3. Run **OLS regression** using statsmodels.  
  4. Export results to Excel.  

**Outputs:**
- Regression coefficients, t-stats, p-values  
- Model metrics: R², Adjusted R², F-statistic, Significance F  
- List of **significant predictors (p < 0.05)**  

---

## 🚀 How to Run

1. Clone this repository:
   ```bash
   git clone https://github.com/your-username/supply-chain-analytics.git
