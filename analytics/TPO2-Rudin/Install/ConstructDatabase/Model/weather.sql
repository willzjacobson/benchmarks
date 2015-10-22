USE [$database$]
GO

/****** Object:  User [rudin_db_reader]    Script Date: 07/23/2013 04:33:26 ******/
CREATE USER [rudin_db_reader] FOR LOGIN [rudin_db_reader] WITH DEFAULT_SCHEMA=[dbo]
GO
/****** Object:  User [rudin_user]    Script Date: 07/23/2013 04:33:26 ******/
CREATE USER [rudin_user] FOR LOGIN [rudin_user] WITH DEFAULT_SCHEMA=[dbo]
GO
/****** Object:  User [tpo]    Script Date: 07/23/2013 04:33:26 ******/
CREATE USER [tpo] FOR LOGIN [tpo] WITH DEFAULT_SCHEMA=[dbo]
GO
/****** Object:  User [TPOWEB_USER]    Script Date: 07/23/2013 04:33:26 ******/
CREATE USER [TPOWEB_USER] FOR LOGIN [TPOWEB_USER] WITH DEFAULT_SCHEMA=[dbo]
GO
/****** Object:  Table [dbo].[Observations_History]    Script Date: 07/23/2013 04:33:26 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
SET ANSI_PADDING ON
GO
CREATE TABLE [dbo].[Observations_History](
	[Run_DateTime] [datetime2](7) NOT NULL,
	[Date] [datetime2](7) NOT NULL,
	[UTC_Date] [datetime2](7) NOT NULL,
	[TempA] [float] NULL,
	[TempM] [float] NULL,
	[DewPointA] [float] NULL,
	[DewPointM] [float] NULL,
	[Humidity] [tinyint] NULL,
	[WindSpeedA] [float] NULL,
	[WindSpeedM] [float] NULL,
	[WindGustA] [float] NULL,
	[WindGustM] [float] NULL,
	[WindDir] [float] NULL,
	[VisibilityA] [float] NULL,
	[VisibilityM] [float] NULL,
	[PressureA] [float] NULL,
	[PressureM] [float] NULL,
	[WindChillA] [float] NULL,
	[WindChillM] [float] NULL,
	[HeatIndexA] [float] NULL,
	[HeatIndexM] [float] NULL,
	[PrecipA] [float] NULL,
	[PrecipM] [float] NULL,
	[Condition] [varchar](max) NULL,
	[Fog] [bit] NULL,
	[Rain] [bit] NULL,
	[Snow] [bit] NULL,
	[Hail] [bit] NULL,
	[Thunder] [bit] NULL,
	[Tornado] [bit] NULL,
	[ID] [int] IDENTITY(1,1) NOT NULL
) ON [PRIMARY]
GO
SET ANSI_PADDING OFF
GO
/****** Object:  UserDefinedFunction [dbo].[HUMIDEX]    Script Date: 07/23/2013 04:33:26 ******/
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
/****** Object:  Table [dbo].[Hourly_Forecast]    Script Date: 07/23/2013 04:33:26 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
SET ANSI_PADDING ON
GO
CREATE TABLE [dbo].[Hourly_Forecast](
	[Fcst_date] [datetime2](7) NOT NULL,
	[Fcst_UTC_Date] [datetime2](7) NOT NULL,
	[Date] [datetime2](7) NOT NULL,
	[UTC_Date] [datetime2](7) NOT NULL,
	[TempA] [smallint] NULL,
	[TempM] [smallint] NULL,
	[DewA] [smallint] NULL,
	[DewM] [smallint] NULL,
	[Condition] [varchar](max) NULL,
	[Sky] [tinyint] NULL,
	[WSpeedA] [tinyint] NULL,
	[WSpeedM] [tinyint] NULL,
	[WDir] [smallint] NULL,
	[WX] [varchar](max) NULL,
	[UVI] [smallint] NULL,
	[Humidity] [smallint] NULL,
	[WindChillA] [smallint] NULL,
	[WindChillM] [smallint] NULL,
	[HeatIndexA] [smallint] NULL,
	[HeatIndexM] [smallint] NULL,
	[FeelsLikeA] [smallint] NULL,
	[FeelsLikeM] [smallint] NULL,
	[QPFA] [float] NULL,
	[QPFM] [float] NULL,
	[SnowA] [float] NULL,
	[SnowM] [float] NULL,
	[POP] [tinyint] NULL,
	[MSLPA] [float] NULL,
	[MSLPM] [smallint] NULL,
	[ID] [int] IDENTITY(1,1) NOT NULL
) ON [PRIMARY]
GO
SET ANSI_PADDING OFF
GO
/****** Object:  View [dbo].[Date_TempA]    Script Date: 07/23/2013 04:33:26 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE VIEW [dbo].[Date_TempA]
AS
SELECT     Date, TempA
FROM         dbo.Observations_History
GO

