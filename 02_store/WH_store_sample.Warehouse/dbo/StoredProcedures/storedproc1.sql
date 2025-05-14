CREATE PROC [dbo].[storedproc1]
@param1 int,
@param2 int
AS
BEGIN
SELECT @param1, @param2
END