USE [$database$]
GO

/****** Object:  User [rudin_user]    Script Date: 07/23/2013 03:48:51 ******/
CREATE USER [rudin_user] FOR LOGIN [rudin_user] WITH DEFAULT_SCHEMA=[dbo]
GO
/****** Object:  User [tpo]    Script Date: 07/23/2013 03:48:51 ******/
CREATE USER [tpo] FOR LOGIN [tpo] WITH DEFAULT_SCHEMA=[dbo]
GO
/****** Object:  User [TPOWEB_USER]    Script Date: 07/23/2013 03:48:51 ******/
CREATE USER [TPOWEB_USER] FOR LOGIN [TPOWEB_USER] WITH DEFAULT_SCHEMA=[dbo]
GO
/****** Object:  Table [dbo].[weather_hourly_forecast_sendid_tracker_status]    Script Date: 07/23/2013 03:48:51 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[weather_hourly_forecast_sendid_tracker_status](
	[SENTID] [int] NULL
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[weather_hourly_forecast_sendid_tracker]    Script Date: 07/23/2013 03:48:51 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[weather_hourly_forecast_sendid_tracker](
	[SENTID] [int] NULL
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[observations_history_sendid_tracker_status]    Script Date: 07/23/2013 03:48:51 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[observations_history_sendid_tracker_status](
	[SENTID] [int] NULL
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[observations_history_sendid_tracker]    Script Date: 07/23/2013 03:48:51 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[observations_history_sendid_tracker](
	[SENTID] [int] NULL
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[560lex_str_sendid_tracker]    Script Date: 07/23/2013 03:48:51 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[560lex_str_sendid_tracker](
	[SENTID] [int] NULL
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[560lex_stp_sendid_tracker]    Script Date: 07/23/2013 03:48:51 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[560lex_stp_sendid_tracker](
	[SENTID] [int] NULL
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[560lex_rdr_sendid_tracker]    Script Date: 07/23/2013 03:48:51 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[560lex_rdr_sendid_tracker](
	[SENTID] [int] NULL
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[560lex_elp_sendid_tracker]    Script Date: 07/23/2013 03:48:51 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[560lex_elp_sendid_tracker](
	[SENTID] [int] NULL
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[560alarm_sendid_tracker]    Script Date: 07/23/2013 03:48:51 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[560alarm_sendid_tracker](
	[SENTID] [int] NULL
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[345park_str_sendid_tracker]    Script Date: 07/23/2013 03:48:51 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[345park_str_sendid_tracker](
	[SENTID] [int] NULL
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[345park_stp_sendid_tracker]    Script Date: 07/23/2013 03:48:51 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[345park_stp_sendid_tracker](
	[SENTID] [int] NULL
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[345park_sdp_sendid_tracker]    Script Date: 07/23/2013 03:48:51 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[345park_sdp_sendid_tracker](
	[SENTID] [int] NULL
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[345park_rdr_sendid_tracker]    Script Date: 07/23/2013 03:48:51 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[345park_rdr_sendid_tracker](
	[SENTID] [int] NULL
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[345park_elp_sendid_tracker]    Script Date: 07/23/2013 03:48:51 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[345park_elp_sendid_tracker](
	[SENTID] [int] NULL
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[345alarm_sendid_tracker]    Script Date: 07/23/2013 03:48:51 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[345alarm_sendid_tracker](
	[SENTID] [int] NULL
) ON [PRIMARY]
GO
