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

# # This workbook imports W2 Data from Scanned W2 Documents
# 
# Note: this notebook is for demonstration/proof-of-concept usage and isn't built for production scale. 
# 
# - Submissions to Azure AI Document Intelligence service wait for each completion (polling). In production a production solution, submissions should be submitted and results read in a separate process.
# - Little to no error checking or validation is done to keep the code more clear and easy to follow.
# 
# The source of the input W2 forms is a set of Fake W2 documents [available on Kaggle](https://www.kaggle.com/datasets/mcvishnu1/fake-w2-us-tax-form-dataset)


# CELL ********************

%pip install azure-ai-documentintelligence


# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# ### Get Key for Azure AI Services from Key Vault

# CELL ********************

# Get Azure AI Services Keys
# from trident_token_library_wrapper \
# import PyTridentTokenLibrary as tl

# key_vault_name = 'hammer-kv'
# key_name = "adDNA-AI"
ai_services_endpoint = "https://ai-fabric-addna.cognitiveservices.azure.com/"

# Get access token to key vault for current session ID
# access_token = mssparkutils.credentials.getToken("keyvault")

# Get secret value from Key Vault using the access token
# ai_services_key = tl.get_secret_with_token( \
#   f"https://{key_vault_name}.vault.azure.net/", \
#   key_name, \
#   access_token)
# ai_services_region = "westeurope"

ai_services_key = "5qjVVb87xihtZw1kguFcLgqd40LIwgGO0xXbS2FIC774HgKpblAhJQQJ99BFAC5RqLJXJ3w3AAAEACOG9mEC"

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark",
# META   "frozen": false,
# META   "editable": true
# META }

# CELL ********************

print(ai_services_key)
print(ai_services_endpoint)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# Source read for new scanned forms W2 in JPG format
source_folder = "Files/W2_Scanned_Images/New_Files"
source_folder_file_api = "/lakehouse/default/Files/W2_Scanned_Images/New_Files"

# Processed files are moved to an Archive folder for reference
archive_folder = "/lakehouse/default/Files/W2_Scanned_Images/Loaded_Archive"

# The output Delta table where extracted data is appended
delta_table_name = "Forms_W2"


# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# ### Define the structure of the output Delta Table

# CELL ********************

from pyspark.sql.types import StructType,StructField, StringType, BooleanType, DecimalType

schema = StructType([ 
    StructField("scanned_filename",StringType(), True),
    StructField("form_variant",StringType(),True), 
    StructField("tax_year",StringType(),True),    
    StructField("w2_copy", StringType(), True),
    StructField("control_number", StringType(), True), 
    StructField("employee_name",StringType(),True),   
    StructField("employee_ssn", StringType(), True),
    StructField("employee_street", StringType(), True),
    StructField("employee_city", StringType(), True), 
    StructField("employee_state", StringType(), True), 
    StructField("employee_postal_code", StringType(), True), 
    StructField("employer_name", StringType(), True),
    StructField("employer_id", StringType(), True),
    StructField("employer_street", StringType(), True),
    StructField("employer_city", StringType(), True), 
    StructField("employer_state", StringType(), True), 
    StructField("employer_postal_code", StringType(), True), 
    StructField("wages_tips", DecimalType(10,2), True),
    StructField("fed_income_tax_withheld", DecimalType(10,2), True),
    StructField("social_security_wages", DecimalType(10,2), True),
    StructField("social_security_tax_withheld", DecimalType(10,2), True),
    StructField("medicare_wages_tips", DecimalType(10,2), True),
    StructField("medicare_tax_withheld", DecimalType(10,2), True),
    StructField("social_security_tips", DecimalType(10,2), True),
    StructField("allocated_tips", DecimalType(10,2), True),
    StructField("non_qualified_plans", DecimalType(10,2), True),
    StructField("dependent_care_benefits", DecimalType(10,2), True),
    StructField("is_statutory_employee", BooleanType(), True),
    StructField("is_retirement_plan", BooleanType(), True),
    StructField("is_third_party_sick_pay", BooleanType(), True)
  ])

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# ### Use Azure AI Document Intelligence to Extract Information from a scanned W2 image

# CELL ********************

def analyze_tax_us_w2(filename, blob):

    from azure.core.credentials import AzureKeyCredential
    from azure.ai.documentintelligence import DocumentIntelligenceClient 
    from decimal import Decimal

    document_intelligence_client = DocumentIntelligenceClient(endpoint=ai_services_endpoint, credential=AzureKeyCredential(ai_services_key))

    print("Polling for Azure AI response...")
    poller = document_intelligence_client.begin_analyze_document("prebuilt-tax.us.w2", blob)
    w2s = poller.result()
    print("...have AI response!")

    output = []

    for idx, w2 in enumerate(w2s.documents):
        
        json = {}
        json["scanned_filename"] = filename

        # add field to JSON object if it exists
        def get_field(container, docField, jsonField, dataType):
            # Note: obj.get('valueString') fetches value; obj.confidence fetches 0-1 confidence 
            if type(container) is dict:
                obj = container.get(docField)
                if obj:
                    json[jsonField] = obj.get(dataType)
            else:
                obj = container.fields.get(docField)
                if obj:
                    if dataType == "valueNumber":
                        json[jsonField] = Decimal(obj.get(dataType))
                    else:
                        strVal = obj.get(dataType)
                        match strVal:
                            case "true":
                                json[jsonField] = True
                            case "false":
                                json[jsonField] = False
                            case _:
                                json[jsonField] = strVal
                        
        # extract employee address info
        def get_address(container, prefix):
            address = container.get("Address")
            if address:
                valueAddress = address.get("valueAddress")
                json[f'{prefix}_street'] = f"{valueAddress.house_number} {valueAddress.road}"
                json[f'{prefix}_city'] = valueAddress.city
                json[f'{prefix}_state'] = valueAddress.state
                json[f'{prefix}_postal_code'] = valueAddress.get("postalCode")
        
        get_field(w2, "W2FormVariant", "form_variant", 'valueString')
        get_field(w2, "TaxYear", "tax_year", 'valueString')
        get_field(w2, "W2Copy", "w2_copy", 'valueString')
        get_field(w2, "ControlNumber", "control_number", 'valueString')

        employee = w2.fields.get("Employee")
        if employee:
            obj = employee.get("valueObject")
            get_field(obj, "Name", "employee_name", "valueString")
            get_field(obj, "SocialSecurityNumber", "employee_ssn", "valueString")
            get_address(obj, "employee")
                
        employer = w2.fields.get("Employer")
        if employer:
            obj = employer.get("valueObject")
            get_field(obj, "Name", "employer_name", "valueString")
            get_field(obj, "IdNumber", "employer_id", "valueString")
            get_address(obj, "employer")

        get_field(w2, "WagesTipsAndOtherCompensation", "wages_tips", "valueNumber")
        get_field(w2, "FederalIncomeTaxWithheld", "fed_income_tax_withheld", "valueNumber")
        get_field(w2, "SocialSecurityWages", "social_security_wages", "valueNumber")
        get_field(w2, "SocialSecurityTaxWithheld", "social_security_tax_withheld", "valueNumber")
        get_field(w2, "MedicareWagesAndTips", "medicare_wages_tips", "valueNumber")
        get_field(w2, "MedicareTaxWithheld", "medicare_tax_withheld", "valueNumber")
        get_field(w2, "SocialSecurityTips", "social_security_tips", "valueNumber")
        get_field(w2, "AllocatedTips", "allocated_tips", "valueNumber")
        get_field(w2, "VerificationCode", "verification_code", "valueNumber")
        get_field(w2, "DependentCareBenefits", "dependent_care_benefits", "valueNumber")
        get_field(w2, "NonQualifiedPlans", "non_qualified_plans", "valueNumber")
        get_field(w2, "IsStatutoryEmployee", "is_statutory_employee", "valueString")
        get_field(w2, "IsRetirementPlan", "is_retirement_plan", "valueString")
        get_field(w2, "IsThirdPartySickPay", "is_third_party_sick_pay", "valueString")
        get_field(w2, "Other", "other_info", "valueString")

        output.append(json)

    return output

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# ### Save a batch of W2 Forms to a Delta Table

# CELL ********************

# Transform array of JSON objects to array of Tuples expected by PySpark


def save_batch_to_table(json_objects):
    print(f"Writing {len(json_objects)} rows to Delta table.")
    rows = []

    for obj in json_objects:
        rows.append((obj["scanned_filename"],
            obj["form_variant"], obj["tax_year"], \
            obj["w2_copy"], obj["control_number"], \
            obj["employee_name"], obj["employee_ssn"], \
            obj["employee_street"], obj["employee_city"], \
            obj["employee_state"], obj["employee_postal_code"], \
            obj["employer_name"], obj["employer_id"], \
            obj["employer_street"], obj["employer_city"], \
            obj["employer_state"], obj["employer_postal_code"], \
            obj["wages_tips"], obj["fed_income_tax_withheld"], \
            obj["social_security_wages"], obj["social_security_tax_withheld"], \
            obj["medicare_wages_tips"], obj["medicare_tax_withheld"], \
            obj["social_security_tips"], obj["allocated_tips"], \
            obj["non_qualified_plans"], obj["dependent_care_benefits"], \
            obj["is_statutory_employee"], obj["is_retirement_plan"], \
            obj["is_third_party_sick_pay"]
        ))

    df = spark.createDataFrame(data=rows, schema=schema)
    df.write.mode("append").format("delta").saveAsTable(delta_table_name)



# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

import os
import base64
# Step 1 - Read input JPG files
df = spark.read.format("binaryFile").load(source_folder)

# for each JPG, read data field using Azure AI Services
for row in df.rdd.collect():
    path = row.path
    blob = row.content
    filename = os.path.basename(path).split('/')[-1]
    print(f"Processing: {filename}")

    # Encode JPG as Base64 String for submission to Azure AI Service
    encoded = base64.b64encode(blob).decode('ascii')
    jsonInput = {
        "base64Source": encoded
    }

    # Call Azure AI to extract data from .jpg file, return as Spark DataFrame
    output = analyze_tax_us_w2(filename, jsonInput)

    # Append data to data frame and write to Lakehouse Table
    save_batch_to_table(output)

    # save completed file to archive folder
    if not os.path.exists(archive_folder):
        os.makedirs(archive_folder)

    archive_file_path = os.path.join(archive_folder, filename)
    archive_file = open(archive_file_path,"wb") 
    archive_file.write(blob) 
    archive_file.close()

    # Delete original file from source_folder
    new_file_path = os.path.join(source_folder_file_api, filename)
    os.remove(new_file_path)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

df = spark.sql("SELECT * FROM AI_Demo_LH.forms_w2 order by scanned_filename LIMIT 1000")
display(df)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }
