-- Fabric notebook source

-- METADATA ********************

-- META {
-- META   "kernel_info": {
-- META     "name": "sqldatawarehouse"
-- META   },
-- META   "dependencies": {
-- META     "warehouse": {
-- META       "default_warehouse": "358ef085-ece7-b097-43b0-40431256ae20",
-- META       "known_warehouses": [
-- META         {
-- META           "id": "358ef085-ece7-b097-43b0-40431256ae20",
-- META           "type": "Datawarehouse"
-- META         }
-- META       ]
-- META     }
-- META   }
-- META }

-- CELL ********************

SELECT TOP (100) [DateID],
			[GeographyID],
			[PrecipitationInches],
			[AvgTemperatureFahrenheit]
FROM [WH_engineer_demo].[dbo].[Weather]

-- METADATA ********************

-- META {
-- META   "language": "sql",
-- META   "language_group": "sqldatawarehouse"
-- META }

-- CELL ********************

SELECT TOP (100) [PaymentType],
			[PaymentsCount],
			[TotalAmountProcessed]
FROM [WH_engineer_demo].[dbo].[vw_PaymentAnalysis]

-- METADATA ********************

-- META {
-- META   "language": "sql",
-- META   "language_group": "sqldatawarehouse"
-- META }
