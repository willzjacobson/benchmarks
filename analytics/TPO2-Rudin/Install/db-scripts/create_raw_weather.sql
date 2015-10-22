USE [Weather]
GO

/****** Object:  Table [dbo].[Raw_Weather]    Script Date: 3/21/2013 3:07:55 PM ******/
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
) ON [PRIMARY] TEXTIMAGE_ON [PRIMARY]

GO

SET ANSI_PADDING OFF
GO


