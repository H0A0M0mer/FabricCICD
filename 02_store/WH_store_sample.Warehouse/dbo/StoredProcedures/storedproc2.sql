CREATE PROC [dbo].[storedproc2]
@param1 int,
@param2 int
AS
BEGIN
SELECT @param1, @param2
END