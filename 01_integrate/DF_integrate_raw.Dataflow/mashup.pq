[DefaultOutputDestinationSettings = [DestinationDefinition = [Kind = "Reference", QueryName = "DefaultDestination", IsNewTarget = true], UpdateMethod = [Kind = "Replace"]], StagingDefinition = [Kind = "FastCopy"]]
section Section1;
[BindToDefaultDestination = true]
shared customers = let
  Source = AzureStorage.DataLake("https://hammeradlsg2.dfs.core.windows.net/"),
  #"Filtered rows" = Table.SelectRows(Source, each ([Folder Path] = "https://hammeradlsg2.dfs.core.windows.net/powerbi-data/")),
  Navigation = #"Filtered rows"{[#"Folder Path" = "https://hammeradlsg2.dfs.core.windows.net/powerbi-data/", Name = "customers.csv"]}[Content],
  #"Imported CSV" = Csv.Document(Navigation, [Delimiter = ";", Columns = 2, QuoteStyle = QuoteStyle.None]),
  #"Promoted headers" = Table.PromoteHeaders(#"Imported CSV", [PromoteAllScalars = true]),
  #"Changed column type" = Table.TransformColumnTypes(#"Promoted headers", {{"customer_index", Int64.Type}, {"customer_names", type text}})
in
  #"Changed column type";
[BindToDefaultDestination = true]
shared date = let
  Source = AzureStorage.DataLake("https://hammeradlsg2.dfs.core.windows.net/"),
  #"Filtered rows" = Table.SelectRows(Source, each ([Folder Path] = "https://hammeradlsg2.dfs.core.windows.net/powerbi-data/")),
  Navigation = #"Filtered rows"{[#"Folder Path" = "https://hammeradlsg2.dfs.core.windows.net/powerbi-data/", Name = "date.csv"]}[Content],
  #"Imported CSV" = Csv.Document(Navigation, [Delimiter = ";", Columns = 17, Encoding = 65001, QuoteStyle = QuoteStyle.None]),
  #"Promoted headers" = Table.PromoteHeaders(#"Imported CSV", [PromoteAllScalars = true]),
  #"Changed column type" = Table.TransformColumnTypes(#"Promoted headers", {{"date", type text}, {"year", Int64.Type}, {"quarter_of_year", Int64.Type}, {"month_of_year", Int64.Type}, {"day_of_month", Int64.Type}, {"date_key", Int64.Type}, {"month_name", type text}, {"month_year", type date}, {"quarter_year", type text}, {"day_in_week", Int64.Type}, {"day_of_week_name", type text}, {"week_ending", type text}, {"week_number", Int64.Type}, {"month_n_year", Int64.Type}, {"quarter_n_year", Int64.Type}, {"short_year", Int64.Type}, {"fy", type text}})
in
  #"Changed column type";
[BindToDefaultDestination = true]
shared products = let
  Source = AzureStorage.DataLake("https://hammeradlsg2.dfs.core.windows.net/"),
  #"Filtered rows" = Table.SelectRows(Source, each ([Folder Path] = "https://hammeradlsg2.dfs.core.windows.net/powerbi-data/")),
  Navigation = #"Filtered rows"{[#"Folder Path" = "https://hammeradlsg2.dfs.core.windows.net/powerbi-data/", Name = "products.csv"]}[Content],
  #"Imported CSV" = Csv.Document(Navigation, [Delimiter = ";", Columns = 2, QuoteStyle = QuoteStyle.None]),
  #"Promoted headers" = Table.PromoteHeaders(#"Imported CSV", [PromoteAllScalars = true]),
  #"Changed column type" = Table.TransformColumnTypes(#"Promoted headers", {{"product_index", Int64.Type}, {"product_name", type text}})
in
  #"Changed column type";
[BindToDefaultDestination = true]
shared regions = let
  Source = AzureStorage.DataLake("https://hammeradlsg2.dfs.core.windows.net/"),
  #"Filtered rows" = Table.SelectRows(Source, each ([Folder Path] = "https://hammeradlsg2.dfs.core.windows.net/powerbi-data/")),
  Navigation = #"Filtered rows"{[#"Folder Path" = "https://hammeradlsg2.dfs.core.windows.net/powerbi-data/", Name = "regions.csv"]}[Content],
  #"Imported CSV" = Csv.Document(Navigation, [Delimiter = ";", Columns = 7, QuoteStyle = QuoteStyle.None]),
  #"Promoted headers" = Table.PromoteHeaders(#"Imported CSV", [PromoteAllScalars = true]),
  #"Changed column type" = Table.TransformColumnTypes(#"Promoted headers", {{"index", Int64.Type}, {"suburb", type text}, {"city", type text}, {"postcode", Int64.Type}, {"longitude", Int64.Type}, {"latitude", Int64.Type}, {"address", type text}})
in
  #"Changed column type";
[BindToDefaultDestination = true]
shared sales_orders_01 = let
  Source = AzureStorage.DataLake("https://hammeradlsg2.dfs.core.windows.net/"),
  #"Filtered rows" = Table.SelectRows(Source, each ([Folder Path] = "https://hammeradlsg2.dfs.core.windows.net/powerbi-data/")),
  Navigation = #"Filtered rows"{[#"Folder Path" = "https://hammeradlsg2.dfs.core.windows.net/powerbi-data/", Name = "sales_orders.csv"]}[Content],
  #"Imported CSV" = Csv.Document(Navigation, [Delimiter = ";", Columns = 13, QuoteStyle = QuoteStyle.None]),
  #"Promoted headers" = Table.PromoteHeaders(#"Imported CSV", [PromoteAllScalars = true]),
  #"Changed column type" = Table.TransformColumnTypes(#"Promoted headers", {{"order_number", type text}, {"order_date", type text}, {"ship_date", type text}, {"customer_name_index", Int64.Type}, {"channel", type text}, {"currency_code", type text}, {"warehouse_code", type text}, {"delivery_region_index", Int64.Type}, {"product_description_index", Int64.Type}, {"order_quantity", Int64.Type}, {"unit_price", type text}, {"total_unit_cost", type text}, {"total_revenue", type text}})
in
  #"Changed column type";
shared DefaultDestination = Lakehouse.Contents([EnableFolding = false]){[workspaceId = "3a4b7256-9761-4633-ae8e-a679bc1b4264"]}[Data]{[lakehouseId = "5e9fcace-872d-4b15-9732-1bb8f400c877"]}[Data];
