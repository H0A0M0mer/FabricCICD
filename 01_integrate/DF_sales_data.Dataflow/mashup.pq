[DefaultOutputDestinationSettings = [DestinationDefinition = [Kind = "Reference", QueryName = "DefaultDestination", IsNewTarget = true], UpdateMethod = [Kind = "Replace"]], StagingDefinition = [Kind = "FastCopy"]]
section Section1;
[BindToDefaultDestination = true]
shared #"January 2019" = let
  Source = AzureStorage.DataLake("https://hammeradlsg2.dfs.core.windows.net/"),
  #"Filtered rows" = Table.SelectRows(Source, each ([Folder Path] = "https://hammeradlsg2.dfs.core.windows.net/sales-data/")),
  Navigation = #"Filtered rows"{[#"Folder Path" = "https://hammeradlsg2.dfs.core.windows.net/sales-data/", Name = "January 2019.csv"]}[Content],
  #"Imported CSV" = Csv.Document(Navigation, [Delimiter = ",", Columns = 4, QuoteStyle = QuoteStyle.None]),
  #"Promoted headers" = Table.PromoteHeaders(#"Imported CSV", [PromoteAllScalars = true]),
  #"Changed column type" = Table.TransformColumnTypes(#"Promoted headers", {{"Date", type date}, {"Country", type text}, {"Units", Int64.Type}, {"Revenue", type number}})
in
  #"Changed column type";
[BindToDefaultDestination = true]
shared #"February 2019" = let
  Source = AzureStorage.DataLake("https://hammeradlsg2.dfs.core.windows.net/"),
  #"Filtered rows" = Table.SelectRows(Source, each ([Folder Path] = "https://hammeradlsg2.dfs.core.windows.net/sales-data/")),
  Navigation = #"Filtered rows"{[#"Folder Path" = "https://hammeradlsg2.dfs.core.windows.net/sales-data/", Name = "February 2019.csv"]}[Content],
  #"Imported CSV" = Csv.Document(Navigation, [Delimiter = ",", Columns = 4, QuoteStyle = QuoteStyle.None]),
  #"Promoted headers" = Table.PromoteHeaders(#"Imported CSV", [PromoteAllScalars = true]),
  #"Changed column type" = Table.TransformColumnTypes(#"Promoted headers", {{"Date", type date}, {"Country", type text}, {"Units", Int64.Type}, {"Revenue", type number}})
in
  #"Changed column type";
[BindToDefaultDestination = true]
shared #"March 2019" = let
  Source = AzureStorage.DataLake("https://hammeradlsg2.dfs.core.windows.net/"),
  #"Filtered rows" = Table.SelectRows(Source, each ([Folder Path] = "https://hammeradlsg2.dfs.core.windows.net/sales-data/")),
  Navigation = #"Filtered rows"{[#"Folder Path" = "https://hammeradlsg2.dfs.core.windows.net/sales-data/", Name = "March 2019.csv"]}[Content],
  #"Imported CSV" = Csv.Document(Navigation, [Delimiter = ",", Columns = 3, QuoteStyle = QuoteStyle.None]),
  #"Promoted headers" = Table.PromoteHeaders(#"Imported CSV", [PromoteAllScalars = true]),
  #"Changed column type" = Table.TransformColumnTypes(#"Promoted headers", {{"Date", type date}, {"Country", type text}, {"Units", Int64.Type}})
in
  #"Changed column type";
[BindToDefaultDestination = true]
shared #"April 2019" = let
  Source = AzureStorage.DataLake("https://hammeradlsg2.dfs.core.windows.net/"),
  #"Filtered rows" = Table.SelectRows(Source, each ([Folder Path] = "https://hammeradlsg2.dfs.core.windows.net/sales-data/")),
  Navigation = #"Filtered rows"{[#"Folder Path" = "https://hammeradlsg2.dfs.core.windows.net/sales-data/", Name = "April 2019.csv"]}[Content],
  #"Imported CSV" = Csv.Document(Navigation, [Delimiter = ",", Columns = 4, QuoteStyle = QuoteStyle.None]),
  #"Promoted headers" = Table.PromoteHeaders(#"Imported CSV", [PromoteAllScalars = true]),
  #"Changed column type" = Table.TransformColumnTypes(#"Promoted headers", {{"Date", type date}, {"Country", type text}, {"Units", Int64.Type}, {"Sales", type number}})
in
  #"Changed column type";
[BindToDefaultDestination = true]
shared #"May 2019" = let
  Source = AzureStorage.DataLake("https://hammeradlsg2.dfs.core.windows.net/"),
  #"Filtered rows" = Table.SelectRows(Source, each ([Folder Path] = "https://hammeradlsg2.dfs.core.windows.net/sales-data/")),
  Navigation = #"Filtered rows"{[#"Folder Path" = "https://hammeradlsg2.dfs.core.windows.net/sales-data/", Name = "May 2019.csv"]}[Content],
  #"Imported CSV" = Csv.Document(Navigation, [Delimiter = ",", Columns = 4, QuoteStyle = QuoteStyle.None]),
  #"Promoted headers" = Table.PromoteHeaders(#"Imported CSV", [PromoteAllScalars = true]),
  #"Changed column type" = Table.TransformColumnTypes(#"Promoted headers", {{"c1", type date}, {"c2", type text}, {"c3", Int64.Type}, {"c4", type number}})
in
  #"Changed column type";
[BindToDefaultDestination = true]
shared #"June 2019" = let
  Source = AzureStorage.DataLake("https://hammeradlsg2.dfs.core.windows.net/"),
  #"Filtered rows" = Table.SelectRows(Source, each ([Folder Path] = "https://hammeradlsg2.dfs.core.windows.net/sales-data/")),
  Navigation = #"Filtered rows"{[#"Folder Path" = "https://hammeradlsg2.dfs.core.windows.net/sales-data/", Name = "June 2019.csv"]}[Content],
  #"Imported CSV" = Csv.Document(Navigation, [Delimiter = ",", Columns = 4, QuoteStyle = QuoteStyle.None]),
  #"Promoted headers" = Table.PromoteHeaders(#"Imported CSV", [PromoteAllScalars = true]),
  #"Changed column type" = Table.TransformColumnTypes(#"Promoted headers", {{"SalesDate", type text}, {"Country", type text}, {"Units", type text}, {"Revenue", type number}})
in
  #"Changed column type";
shared DefaultDestination = Lakehouse.Contents([EnableFolding = false]){[workspaceId = "3a4b7256-9761-4633-ae8e-a679bc1b4264"]}[Data]{[lakehouseId = "5e9fcace-872d-4b15-9732-1bb8f400c877"]}[Data];
