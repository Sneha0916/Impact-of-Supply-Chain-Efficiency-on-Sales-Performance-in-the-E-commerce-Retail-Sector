# -*- coding: utf-8 -*-
"""
Created on Mon Apr 14 19:32:52 2025

@author: Sneha B
"""

# -*- coding: utf-8 -*-
"""
Optimized Supply Chain Analysis - Key Variables Only
"""

import pandas as pd
import statsmodels.api as sm

# Step 1: Load the dataset
file_path = r"C:\Users\sneha\OneDrive\Desktop\DataCoSupplyChainDataset 567.csv"
df = pd.read_csv(file_path, encoding='ISO-8859-1')

# Step 2: Select only essential columns
columns_to_keep = [
    'Customer Id', 
    'Sales per customer', 
    'Order Item Quantity',
    'Order Item Product Price',
    'Order Item Discount Rate',
    'Days for shipping (real)',
    'Late_delivery_risk',
    'Delivery Status',
    'Customer Segment',
    'Market',
    'Category Name'
]
df = df[columns_to_keep]

# Step 3: Group by Customer Id with focused aggregation
df_grouped = df.groupby('Customer Id').agg({
    'Sales per customer': 'sum',
    'Order Item Quantity': 'mean',
    'Order Item Product Price': 'mean',
    'Order Item Discount Rate': 'mean',
    'Days for shipping (real)': 'mean',
    'Late_delivery_risk': 'mean',
    'Delivery Status': lambda x: x.mode()[0],
    'Customer Segment': lambda x: x.mode()[0],
    'Market': lambda x: x.mode()[0],
    'Category Name': lambda x: x.mode()[0]
}).reset_index()

# Step 4: One-hot encode categorical variables
categorical_cols = [
    'Delivery Status',
    'Customer Segment',
    'Market',
    'Category Name'
]
df_final = pd.get_dummies(df_grouped, columns=categorical_cols, drop_first=True, dtype=int)

# Step 5: Define X and y
X = df_final.drop(['Customer Id', 'Sales per customer'], axis=1)
y = df_final['Sales per customer']

# Step 6: Convert to numeric and drop NA
X = X.apply(pd.to_numeric, errors='coerce')
y = pd.to_numeric(y, errors='coerce')
df_clean = pd.concat([X, y], axis=1).dropna()
X_clean = df_clean[X.columns]
y_clean = df_clean[y.name]

# Step 7: Add constant and fit model
X_sm = sm.add_constant(X_clean)
model = sm.OLS(y_clean, X_sm).fit()

# Step 8: Create DataFrames for output
summary_df = pd.DataFrame({
    'Coefficient': model.params.round(4),
    'T-Statistic': model.tvalues.round(4),
    'P-Value': model.pvalues.round(4)
})

model_metrics_df = pd.DataFrame({
    'Metric': ['R-squared', 'Adjusted R-squared', 'F-statistic', 'Significance F'],
    'Value': [
        round(model.rsquared, 4),
        round(model.rsquared_adj, 4),
        round(model.fvalue, 4),
        round(model.f_pvalue, 4)
    ]
})

# Step 9: Export to Excel
output_file = r"C:\Users\sneha\OneDrive\Desktop\regression_output_optimized.xlsx"

with pd.ExcelWriter(output_file) as writer:
    summary_df.to_excel(writer, sheet_name='Regression Coefficients')
    model_metrics_df.to_excel(writer, sheet_name='Model Metrics', index=False)

print("✅ Optimized regression output saved to:", output_file)

# Print model metrics
print("\n📊 Optimized Model Summary:")
print(f"R-squared: {model.rsquared:.4f}")
print(f"Adjusted R-squared: {model.rsquared_adj:.4f}")
print(f"F-statistic: {model.fvalue:.4f}")
print(f"Significance F (p-value): {model.f_pvalue:.4f}")

# Print significant variables
print("\n✨ Key Significant Variables (p < 0.05):")
significant_vars = summary_df[summary_df['P-Value'] < 0.05]
print(significant_vars[['Coefficient', 'P-Value']])
