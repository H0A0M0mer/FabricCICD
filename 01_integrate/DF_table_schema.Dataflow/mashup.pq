[StagingDefinition = [Kind = "FastCopy"]]
section Section1;
[DataDestinations = {[Definition = [Kind = "Reference", QueryName = "Forms_W2_DataDestination", IsNewTarget = true], Settings = [Kind = "Automatic", TypeSettings = [Kind = "Table"]]]}]
shared Forms_W2 = let
  Source = AzureStorage.DataLake("https://hammeradlsg2.dfs.core.windows.net/"),
  #"Filtered rows" = Table.SelectRows(Source, each ([Folder Path] = "https://hammeradlsg2.dfs.core.windows.net/table-schema/")),
  Navigation = #"Filtered rows"{[#"Folder Path" = "https://hammeradlsg2.dfs.core.windows.net/table-schema/", Name = "Forms_W2.csv"]}[Content],
  #"Imported CSV" = Csv.Document(Navigation, [Delimiter = ";", Columns = 30, Encoding = 65001, QuoteStyle = QuoteStyle.None]),
  #"Promoted headers" = Table.PromoteHeaders(#"Imported CSV", [PromoteAllScalars = true]),
  #"Changed column type" = Table.TransformColumnTypes(#"Promoted headers", {{"wages_tips", type number}, {"dependent_care_benefits", type number}, {"non_qualified_plans", type number}, {"allocated_tips", type number}, {"social_security_tips", type number}, {"medicare_tax_withheld", type number}, {"medicare_wages_tips", type number}, {"social_security_tax_withheld", type number}, {"social_security_wages", type number}, {"fed_income_tax_withheld", type number}, {"is_third_party_sick_pay", type logical}, {"is_retirement_plan", type logical}, {"is_statutory_employee", type logical}})
in
  #"Changed column type";
shared Forms_W2_DataDestination = let
  Pattern = Lakehouse.Contents([CreateNavigationProperties = false, EnableFolding = false]),
  Navigation_1 = Pattern{[workspaceId = "3a4b7256-9761-4633-ae8e-a679bc1b4264"]}[Data],
  Navigation_2 = Navigation_1{[lakehouseId = "ebee1193-64fe-4a28-a3db-61479ec0f59e"]}[Data],
  TableNavigation = Navigation_2{[Id = "Forms_W2", ItemKind = "Table"]}?[Data]?
in
  TableNavigation;
