# Fabric notebook source

# METADATA ********************

# META {
# META   "kernel_info": {
# META     "name": "synapse_pyspark"
# META   },
# META   "dependencies": {
# META     "lakehouse": {
# META       "default_lakehouse": "ebee1193-64fe-4a28-a3db-61479ec0f59e",
# META       "default_lakehouse_name": "LH_store_transformed",
# META       "default_lakehouse_workspace_id": "3a4b7256-9761-4633-ae8e-a679bc1b4264",
# META       "known_lakehouses": [
# META         {
# META           "id": "ebee1193-64fe-4a28-a3db-61479ec0f59e"
# META         }
# META       ]
# META     }
# META   }
# META }

# MARKDOWN ********************

# ### Install Fabric Semantic Link

# CELL ********************

%pip install semantic-link
%load_ext sempy

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# ### Import Libraries

# CELL ********************

# Basic Imports
import pandas as pd
import numpy as np

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# Fabric Imports
import sempy.fabric as fabric
import pyspark.sql.functions as F

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# Machine Learning Libraries
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn import preprocessing
from sklearn.model_selection import train_test_split
from sklearn.model_selection import GridSearchCV
from sklearn.linear_model import LinearRegression
from sklearn.metrics import roc_curve, roc_auc_score, \
classification_report, accuracy_score, confusion_matrix 
import mlflow

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# ### Get Reference to Power BI Data

# CELL ********************

df_datasets = fabric.list_datasets()
df_datasets

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

dataset = "SM_Sales_DL"
EXPERIMENT_NAME = "retail-total-sales-prediction"

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# ### Examine What's Available in Power BI Data Model

# CELL ********************

from sempy.relationships import plot_relationship_metadata
relationships = fabric.list_relationships(dataset)
plot_relationship_metadata(relationships)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

fabric.list_measures(dataset)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# ### Query for Data to use as source for Machine Learning Model

# CELL ********************

df = fabric.evaluate_measure(dataset, \
measure=["_Total Sales", "_Total Profits"], \
groupby_columns=["customers[customer_names]", \
                 "products[product_name]", \
                "regions[city]"])

df.head()

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

df.shape

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

df.describe()

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

display(df["customer_names"].unique())
display(df["product_name"].unique())

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# ### Build a regression model to predict Total Sales column

# CELL ********************

Y = df['_Total Profits'].to_numpy()

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

df_with_dummies = pd.get_dummies(df, columns=['customer_names', 'product_name', 'city'])

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

df_with_dummies.head()

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

df_with_dummies.columns

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

X = df_with_dummies.drop(columns=['_TotalSales'])

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

X

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

mlflow.set_experiment(EXPERIMENT_NAME)
mlflow.autolog()
mlflow.sklearn.autolog(registered_model_name='retail_regression')

model = LinearRegression()
model.fit(X, Y)
Y_hat = model.predict(X)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

r2_score = model.score(X, Y)
print('The R-square is: ', r2_score)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# Write your code below and press Shift+Enter to execute
ax1 = sns.distplot(df['TotalSales'], hist=False, color="r", label="Actual Value")
sns.distplot(Y_hat, hist=False, color="b", label="Fitted Values" , ax=ax1)

plt.title('Actual vs Fitted Values for TotalSales')
plt.xlabel('Total Sales')
plt.ylabel('Proportion of Stores')

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }
