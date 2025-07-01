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

# MARKDOWN ********************

# ## Handling incorrect schema on read

# MARKDOWN ********************

# **Upload the CSV files, schematize and read into data frame**
# 
# File schema:
# 1. **Jan-Feb**: Date,Country,Units,Revenue
# 2. **March**: Date,Country,Units
# 3. **April**: Date,Country,Units,**Sales**
# 4. **May**: c1,c2,c3,c4
# 
# 


# MARKDOWN ********************

# ##### How Default Schema enforcement works?

# CELL ********************

csv_schema='SalesDate STRING,Country STRING,Units STRING,Revenue STRING'
df = spark.read.format("csv").schema(csv_schema).option('header',True)\
 .load("Files/CSV/SchemaEnforcement")\

display(df)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# **Use case 1- missing column**

# CELL ********************

display(df.filter("SalesDate between '2019-03-01' and '2019-03-31'" ))

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# **Use case 2:single irregular column**

# CELL ********************

display(df.filter("SalesDate between '2019-04-01' and '2019-04-30'" ))

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# **Use case 3: all column names are irregular**

# CELL ********************

display(df.filter("SalesDate between '2019-05-01' and '2019-05-31'" ))

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# **Disabling schema enforcement option**

# CELL ********************

csv_schema='SalesDate STRING,Country STRING,Units STRING,Revenue STRING'
df = spark.read.format("csv")\
 .schema(csv_schema)\
 .option('header',True)\
 .option('enforceSchema',False)\
 .load("Files/CSV/SchemaEnforcement")\

display(df)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# #### Handling Corrupt values 

# MARKDOWN ********************

# **Reading corrupt rows, default behaviour**

# CELL ********************

csv_schema='SalesDate Date,Country STRING,Units INTEGER,Revenue STRING'
df = spark.read.format("csv")\
 .schema(csv_schema)\
 .option('header',True)\
 .load("Files/CSV/SchemaEnforcement/June 2019.csv")

display(df)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# **Using Permissive mode and _columnNameOfCorruptRecord_ option**

# CELL ********************

csv_schema='SalesDate Date,Country STRING,Units INTEGER,Revenue STRING,CorruptRecord STRING'
df = spark.read.format("csv")\
 .schema(csv_schema)\
 .option('header',True)\
 .option('mode','PERMISSIVE')\
 .option('columnNameOfCorruptRecord','CorruptRecord')\
 .load("Files/CSV/SchemaEvolution/June 2019.csv")

display(df)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# **Using DROPMALFORMED mode**

# CELL ********************

csv_schema='SalesDate Date,Country STRING,Units INTEGER,Revenue STRING'
df = spark.read.format("csv")\
 .schema(csv_schema)\
 .option('header',True)\
 .option('mode','DROPMALFORMED')\
 .load("Files/CSV/SchemaEvolution/June 2019.csv")

display(df)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# **Using FAILFAST mode**

# CELL ********************

csv_schema='SalesDate Date,Country STRING,Units INTEGER,Revenue STRING'
df = spark.read.format("csv")\
 .schema(csv_schema)\
 .option('header',True)\
 .option('mode','FAILFAST')\
 .load("Files/CSV/SchemaEvolution/June 2019.csv")

display(df)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# ## Schema handling while writing to Delta tables

# CELL ********************

csv_schema='SalesDate STRING,Country STRING,Units STRING,Revenue STRING'
df = spark.read.format("csv")\
 .schema(csv_schema)\
 .option('header',True)\
 .load("Files/CSV/SchemaEnforcement/January 2019.csv")


# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# **Creating target table with 2 columns**

# CELL ********************

df.select('SalesDate','Country')\
.write.format('delta')\
.mode('append')\
.saveAsTable('Sales_SE')

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# **Writing less columns than in the target**

# CELL ********************

df.select('SalesDate').write.format('delta').mode('append').saveAsTable('Sales_SE')

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# MAGIC %%sql
# MAGIC select * from Sales_SE

# METADATA ********************

# META {
# META   "language": "sparksql",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# **Writing more columns than in the target**

# CELL ********************

df.select('SalesDate','Country','Units').write.format('delta').mode('append').saveAsTable('Sales_SE')

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# **Using autoMerge on a single table**

# CELL ********************

df.select('SalesDate','Country','Units')\
 .write.format('delta')\
 .mode('append')\
 .option("mergeSchema", "true")\
 .saveAsTable('Sales_SE')

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# MAGIC %%sql
# MAGIC select * from Sales_SE

# METADATA ********************

# META {
# META   "language": "sparksql",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# **Setting AutoMerge for all tables**

# CELL ********************

spark.conf.get("spark.databricks.delta.schema.autoMerge.enabled")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

spark.conf.set("spark.databricks.delta.schema.autoMerge.enabled", "true")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# **Now the write command succeeds with extra columns**

# CELL ********************

df.select('SalesDate','Country','Units','Revenue')\
.write.format('delta')\
.mode('append')\
.saveAsTable('Sales_SE')

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# MAGIC %%sql
# MAGIC drop TABLE Sales_SE;

# METADATA ********************

# META {
# META   "language": "sparksql",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************


# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }
