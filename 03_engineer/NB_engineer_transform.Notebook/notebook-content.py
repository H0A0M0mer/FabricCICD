# Fabric notebook source

# METADATA ********************

# META {
# META   "kernel_info": {
# META     "name": "synapse_pyspark"
# META   },
# META   "dependencies": {
# META     "lakehouse": {
# META       "default_lakehouse": "5e9fcace-872d-4b15-9732-1bb8f400c877",
# META       "default_lakehouse_name": "LH_store_raw",
# META       "default_lakehouse_workspace_id": "3a4b7256-9761-4633-ae8e-a679bc1b4264",
# META       "known_lakehouses": [
# META         {
# META           "id": "5e9fcace-872d-4b15-9732-1bb8f400c877"
# META         }
# META       ]
# META     }
# META   }
# META }

# CELL ********************

# read table from raw lakehouse
df = spark.sql("SELECT * FROM LH_store_raw.dbo.sales_orders LIMIT 1000")
display(df)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# write table to transformed lakehouse
sales_orders = "sales_orders"
df.write.mode("overwrite").option("overwriteSchema", "true").format("delta").saveAsTable(sales_orders)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }
