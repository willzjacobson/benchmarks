USE [Weather]
GO

/****** Object:  UserDefinedFunction [dbo].[HUMIDEX]    Script Date: 7/22/2013 7:23:49 PM ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO




-- =============================================
-- Author:		<Gagneja, Ashish>
-- Create date: <04/09/2013>
-- Description:	Compute Humidex
-- =============================================
CREATE FUNCTION [dbo].[HUMIDEX] 
(
	@temp real, @dew_pt real
)
RETURNS real
AS
BEGIN
	-- Declare the return variable here
	DECLARE @dew_pt_klvn real, @e real

	SET @dew_pt_klvn = (@dew_pt - 32)*5/9 + 273.15
	SET @e = 6.112 * exp(5417.7530 * ((1/273.16) - (1/@dew_pt_klvn)))

	-- Return the result of the function
	RETURN (@temp -32)*5/9 + (0.5555 * (@e - 10.0))

END




GO


