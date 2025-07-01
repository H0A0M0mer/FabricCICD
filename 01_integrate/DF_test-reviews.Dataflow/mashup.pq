[DefaultOutputDestinationSettings = [DestinationDefinition = [Kind = "Reference", QueryName = "DefaultDestination", IsNewTarget = true], UpdateMethod = [Kind = "Replace"], DestinationTypeSettings = [Kind = "Table"]], StagingDefinition = [Kind = "FastCopy"]]
section Section1;
[BindToDefaultDestination = true]
shared test_reviews = let
  Source = AzureStorage.DataLake("https://hammeradlsg2.dfs.core.windows.net/"),
  #"Filtered rows" = Table.SelectRows(Source, each ([Folder Path] = "https://hammeradlsg2.dfs.core.windows.net/review-texts/")),
  Navigation = #"Filtered rows"{[#"Folder Path" = "https://hammeradlsg2.dfs.core.windows.net/review-texts/", Name = "TestReviews.csv"]}[Content],
  #"Imported CSV" = Csv.Document(Navigation, [Delimiter = ",", Columns = 2, QuoteStyle = QuoteStyle.Csv]),
  #"Promoted headers" = Table.PromoteHeaders(#"Imported CSV", [PromoteAllScalars = true]),
  #"Changed column type" = Table.TransformColumnTypes(#"Promoted headers", {{"review", type text}, {"class", Int64.Type}})
in
  #"Changed column type";
shared DefaultDestination = Lakehouse.Contents([EnableFolding = false]){[workspaceId = "3a4b7256-9761-4633-ae8e-a679bc1b4264"]}[Data]{[lakehouseId = "5e9fcace-872d-4b15-9732-1bb8f400c877"]}[Data];
