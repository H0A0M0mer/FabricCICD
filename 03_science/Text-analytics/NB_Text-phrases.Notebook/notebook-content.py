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

# CELL ********************

# Load visit reports data from enriched lakehouse
test_reviews = spark.sql("SELECT * FROM LH_store_transformed.dbo_sc.test_reviews LIMIT 10")
display(test_reviews)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# import Synapse Machine Learning services
import synapse.ml.core
from synapse.ml.services import *
from pyspark.sql.functions import col, udf
from pyspark.sql import Row
from pyspark.sql.types import StringType, StructType, StructField
import json

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# translate all reviews into German
translate = (Translate()
    .setTextCol("review")
    .setToLanguage("de")
    .setOutputCol("translation")
    .setConcurrency(5)
    .setErrorCol("errors"))

# get just the detected language and translation result
test_reviews_de = translate.transform(test_reviews)\
    .withColumn("DetectedLanguage", col("translation.detectedLanguage.language").getItem(0))\
    .withColumn("TranslationResult", col("translation.translations").getItem(0).getField("text").getItem(0))\
    .cache()

# remove the translation and Errors columns
test_reviews_de = test_reviews_de.drop("translation", "errors")

display(test_reviews_de)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# extract key phrases from the translated reviews
model = (AnalyzeText()
        .setTextCol("review")
        .setKind("KeyPhraseExtraction")
        .setOutputCol("response")
        .setErrorCol("errors"))

test_reviews_key = model.transform(test_reviews_de)\
        .withColumn("KeyPhrases", col("response.documents").getItem("keyPhrases"))\
        .cache()

# remove the translation and Errors columns
test_reviews_key = test_reviews_key.drop("response", "errors")

display(test_reviews_key)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# Write table with insights to enriched lakehouse
test_reviews_ins = "test_reviews_key"
test_reviews_key.write.mode("overwrite").option("overwriteSchema", "true").format("delta").saveAsTable(test_reviews_ins)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }
