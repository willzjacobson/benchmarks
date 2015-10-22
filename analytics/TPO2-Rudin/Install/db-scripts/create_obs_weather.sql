USE [Weather]
GO

/****** Object:  Table [dbo].[Obs_Weather]    Script Date: 3/21/2013 3:04:03 PM ******/
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
) ON [PRIMARY] TEXTIMAGE_ON [PRIMARY]

GO

SET ANSI_PADDING OFF
GO
