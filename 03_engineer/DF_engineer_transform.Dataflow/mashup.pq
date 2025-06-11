[DefaultOutputDestinationSettings = [DestinationDefinition = [Kind = "Reference", QueryName = "DefaultDestination", IsNewTarget = true], UpdateMethod = [Kind = "Replace"]], StagingDefinition = [Kind = "FastCopy"]]
section Section1;
[BindToDefaultDestination = true]
shared customers = let
  Source = Lakehouse.Contents(null),
  Navigation = Source{[workspaceId = "3a4b7256-9761-4633-ae8e-a679bc1b4264"]}[Data],
  #"Navigation 1" = Navigation{[lakehouseId = "5e9fcace-872d-4b15-9732-1bb8f400c877"]}[Data],
  #"Navigation 2" = #"Navigation 1"{[Id = "customers", ItemKind = "Table"]}[Data]
in
  #"Navigation 2";
[BindToDefaultDestination = true]
shared date = let
  Source = Lakehouse.Contents(null),
  Navigation = Source{[workspaceId = "3a4b7256-9761-4633-ae8e-a679bc1b4264"]}[Data],
  #"Navigation 1" = Navigation{[lakehouseId = "5e9fcace-872d-4b15-9732-1bb8f400c877"]}[Data],
  #"Navigation 2" = #"Navigation 1"{[Id = "date", ItemKind = "Table"]}[Data],
  #"Changed column type" = Table.TransformColumnTypes(#"Navigation 2", {{"date", type date}, {"week_ending", type date}}, "de-DE")
in
  #"Changed column type";
[BindToDefaultDestination = true]
shared products = let
  Source = Lakehouse.Contents(null),
  Navigation = Source{[workspaceId = "3a4b7256-9761-4633-ae8e-a679bc1b4264"]}[Data],
  #"Navigation 1" = Navigation{[lakehouseId = "5e9fcace-872d-4b15-9732-1bb8f400c877"]}[Data],
  #"Navigation 2" = #"Navigation 1"{[Id = "products", ItemKind = "Table"]}[Data]
in
  #"Navigation 2";
[BindToDefaultDestination = true]
shared regions = let
  Source = Lakehouse.Contents(null),
  Navigation = Source{[workspaceId = "3a4b7256-9761-4633-ae8e-a679bc1b4264"]}[Data],
  #"Navigation 1" = Navigation{[lakehouseId = "5e9fcace-872d-4b15-9732-1bb8f400c877"]}[Data],
  #"Navigation 2" = #"Navigation 1"{[Id = "regions", ItemKind = "Table"]}[Data]
in
  #"Navigation 2";
[BindToDefaultDestination = true]
shared sales_orders = let
  Source = Lakehouse.Contents(null),
  Navigation = Source{[workspaceId = "3a4b7256-9761-4633-ae8e-a679bc1b4264"]}[Data],
  #"Navigation 1" = Navigation{[lakehouseId = "5e9fcace-872d-4b15-9732-1bb8f400c877"]}[Data],
  #"Navigation 2" = #"Navigation 1"{[Id = "sales_orders", ItemKind = "Table"]}[Data],
  #"Changed column type" = Table.TransformColumnTypes(#"Navigation 2", {{"order_date", type date}, {"ship_date", type date}, {"unit_price", type number}, {"total_unit_cost", type number}, {"total_revenue", type number}}, "de-DE")
in
  #"Changed column type";
shared DefaultDestination = Lakehouse.Contents([EnableFolding = false]){[workspaceId = "3a4b7256-9761-4633-ae8e-a679bc1b4264"]}[Data]{[lakehouseId = "ebee1193-64fe-4a28-a3db-61479ec0f59e"]}[Data];
