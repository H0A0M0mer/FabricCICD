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

# Import Synapse Machine Learning services
import synapse.ml.core
from synapse.ml.services import *
from pyspark.sql.functions import col, udf
from pyspark.sql import Row
from pyspark.sql.types import StringType, StructType, StructField

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# Classify visit reports regarding sentiment using Generative AI
# Create a prompt template
def prompt_template(x):
    return f'''You are an AI that classifies customer reviews regarding sentiment. Classify the following reviews into 1 of the following categories:
    
        Positive sentiment
        Neutral sentiment
        Negative sentiment

    Here is the text to classify:
    
    {x}

    Now, return the classified category.'''

# Turn that template into a UDF with output type of string
process_column_udf = udf(prompt_template, StringType())

# Create a new column for the prompt
test_reviews_sen = test_reviews\
    .withColumn("prompt", process_column_udf(test_reviews["review"]))\
    .cache()

# Call the LLM to make the classification based on the provided prompt
completion = (
    OpenAICompletion()
    .setDeploymentName("gpt-35-turbo-instruct")
    .setMaxTokens(200)
    .setPromptCol("prompt")
    .setErrorCol("errors")
    .setOutputCol("classifications")
)
test_reviews_sen_c = completion.transform(test_reviews_sen)\
                .withColumn("classifications", col("classifications.choices.text")[0])\
                .cache()

# Display table with insights
display(test_reviews_sen_c)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark",
# META   "frozen": false,
# META   "editable": true
# META }

# CELL ********************

# Remove errors column
test_reviews_sen_cc = test_reviews_sen_c.drop("errors")
display(test_reviews_sen_cc)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# Write table with insights to enriched lakehouse
test_reviews_ins = "test_reviews_sen_cc"
test_reviews_sen_cc.write.mode("overwrite").option("overwriteSchema", "true").format("delta").saveAsTable(test_reviews_ins)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }
