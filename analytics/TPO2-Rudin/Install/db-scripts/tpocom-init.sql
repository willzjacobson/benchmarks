USE [master]
GO
/****** Object:  Database [TPOCOM]    Script Date: 7/23/2013 2:50:13 AM ******/
CREATE DATABASE [TPOCOM] ON  PRIMARY 
( NAME = N'TPOCOM', FILENAME = N'F:\SQL\TPOCOM.mdf' , SIZE = 3072KB , MAXSIZE = UNLIMITED, FILEGROWTH = 1024KB )
 LOG ON 
( NAME = N'TPOCOM_log', FILENAME = N'F:\SQL\TPOCOM_log.ldf' , SIZE = 3840KB , MAXSIZE = 2048GB , FILEGROWTH = 10%)
GO
ALTER DATABASE [TPOCOM] SET COMPATIBILITY_LEVEL = 100
GO
IF (1 = FULLTEXTSERVICEPROPERTY('IsFullTextInstalled'))
begin
EXEC [TPOCOM].[dbo].[sp_fulltext_database] @action = 'enable'
end
GO
ALTER DATABASE [TPOCOM] SET ANSI_NULL_DEFAULT OFF 
GO
ALTER DATABASE [TPOCOM] SET ANSI_NULLS OFF 
GO
ALTER DATABASE [TPOCOM] SET ANSI_PADDING OFF 
GO
ALTER DATABASE [TPOCOM] SET ANSI_WARNINGS OFF 
GO
ALTER DATABASE [TPOCOM] SET ARITHABORT OFF 
GO
ALTER DATABASE [TPOCOM] SET AUTO_CLOSE OFF 
GO
ALTER DATABASE [TPOCOM] SET AUTO_CREATE_STATISTICS ON 
GO
ALTER DATABASE [TPOCOM] SET AUTO_SHRINK OFF 
GO
ALTER DATABASE [TPOCOM] SET AUTO_UPDATE_STATISTICS ON 
GO
ALTER DATABASE [TPOCOM] SET CURSOR_CLOSE_ON_COMMIT OFF 
GO
ALTER DATABASE [TPOCOM] SET CURSOR_DEFAULT  GLOBAL 
GO
ALTER DATABASE [TPOCOM] SET CONCAT_NULL_YIELDS_NULL OFF 
GO
ALTER DATABASE [TPOCOM] SET NUMERIC_ROUNDABORT OFF 
GO
ALTER DATABASE [TPOCOM] SET QUOTED_IDENTIFIER OFF 
GO
ALTER DATABASE [TPOCOM] SET RECURSIVE_TRIGGERS OFF 
GO
ALTER DATABASE [TPOCOM] SET  DISABLE_BROKER 
GO
ALTER DATABASE [TPOCOM] SET AUTO_UPDATE_STATISTICS_ASYNC OFF 
GO
ALTER DATABASE [TPOCOM] SET DATE_CORRELATION_OPTIMIZATION OFF 
GO
ALTER DATABASE [TPOCOM] SET TRUSTWORTHY OFF 
GO
ALTER DATABASE [TPOCOM] SET ALLOW_SNAPSHOT_ISOLATION OFF 
GO
ALTER DATABASE [TPOCOM] SET PARAMETERIZATION SIMPLE 
GO
ALTER DATABASE [TPOCOM] SET READ_COMMITTED_SNAPSHOT OFF 
GO
ALTER DATABASE [TPOCOM] SET HONOR_BROKER_PRIORITY OFF 
GO
ALTER DATABASE [TPOCOM] SET RECOVERY FULL 
GO
ALTER DATABASE [TPOCOM] SET  MULTI_USER 
GO
ALTER DATABASE [TPOCOM] SET PAGE_VERIFY CHECKSUM  
GO
ALTER DATABASE [TPOCOM] SET DB_CHAINING OFF 
GO
USE [TPOCOM]
GO
/****** Object:  User [TPOWEB_USER]    Script Date: 7/23/2013 2:50:14 AM ******/
CREATE USER [TPOWEB_USER] FOR LOGIN [TPOWEB_USER] WITH DEFAULT_SCHEMA=[dbo]
GO
/****** Object:  User [tpo]    Script Date: 7/23/2013 2:50:14 AM ******/
CREATE USER [tpo] FOR LOGIN [tpo] WITH DEFAULT_SCHEMA=[dbo]
GO
/****** Object:  User [rudin_user]    Script Date: 7/23/2013 2:50:14 AM ******/
CREATE USER [rudin_user] FOR LOGIN [rudin_user] WITH DEFAULT_SCHEMA=[dbo]
GO
/****** Object:  User [ANDERSON\ashwath]    Script Date: 7/23/2013 2:50:14 AM ******/
CREATE USER [ANDERSON\ashwath] FOR LOGIN [ANDERSON\ashwath] WITH DEFAULT_SCHEMA=[dbo]
GO
/****** Object:  User [ANDERSON\agagneja]    Script Date: 7/23/2013 2:50:14 AM ******/
CREATE USER [ANDERSON\agagneja] FOR LOGIN [ANDERSON\agagneja] WITH DEFAULT_SCHEMA=[dbo]
GO
ALTER ROLE [db_datareader] ADD MEMBER [TPOWEB_USER]
GO
ALTER ROLE [db_datareader] ADD MEMBER [tpo]
GO
ALTER ROLE [db_datawriter] ADD MEMBER [tpo]
GO
ALTER ROLE [db_owner] ADD MEMBER [rudin_user]
GO
ALTER ROLE [db_owner] ADD MEMBER [ANDERSON\ashwath]
GO
ALTER ROLE [db_owner] ADD MEMBER [ANDERSON\agagneja]
GO
/****** Object:  Table [dbo].[345alarm_sendid_tracker]    Script Date: 7/23/2013 2:50:14 AM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[345alarm_sendid_tracker](
	[SENTID] [int] NULL
) ON [PRIMARY]

GO
/****** Object:  Table [dbo].[345park_elp_sendid_tracker]    Script Date: 7/23/2013 2:50:14 AM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[345park_elp_sendid_tracker](
	[SENTID] [int] NULL
) ON [PRIMARY]

GO
/****** Object:  Table [dbo].[345park_rdr_sendid_tracker]    Script Date: 7/23/2013 2:50:14 AM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[345park_rdr_sendid_tracker](
	[SENTID] [int] NULL
) ON [PRIMARY]

GO
/****** Object:  Table [dbo].[345park_sdp_sendid_tracker]    Script Date: 7/23/2013 2:50:14 AM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[345park_sdp_sendid_tracker](
	[SENTID] [int] NULL
) ON [PRIMARY]

GO
/****** Object:  Table [dbo].[345park_stp_sendid_tracker]    Script Date: 7/23/2013 2:50:14 AM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[345park_stp_sendid_tracker](
	[SENTID] [int] NULL
) ON [PRIMARY]

GO
/****** Object:  Table [dbo].[345park_str_sendid_tracker]    Script Date: 7/23/2013 2:50:14 AM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[345park_str_sendid_tracker](
	[SENTID] [int] NULL
) ON [PRIMARY]

GO
/****** Object:  Table [dbo].[560alarm_sendid_tracker]    Script Date: 7/23/2013 2:50:14 AM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[560alarm_sendid_tracker](
	[SENTID] [int] NULL
) ON [PRIMARY]

GO
/****** Object:  Table [dbo].[560lex_elp_sendid_tracker]    Script Date: 7/23/2013 2:50:14 AM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[560lex_elp_sendid_tracker](
	[SENTID] [int] NULL
) ON [PRIMARY]

GO
/****** Object:  Table [dbo].[560lex_rdr_sendid_tracker]    Script Date: 7/23/2013 2:50:14 AM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[560lex_rdr_sendid_tracker](
	[SENTID] [int] NULL
) ON [PRIMARY]

GO
/****** Object:  Table [dbo].[560lex_stp_sendid_tracker]    Script Date: 7/23/2013 2:50:14 AM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[560lex_stp_sendid_tracker](
	[SENTID] [int] NULL
) ON [PRIMARY]

GO
/****** Object:  Table [dbo].[560lex_str_sendid_tracker]    Script Date: 7/23/2013 2:50:14 AM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[560lex_str_sendid_tracker](
	[SENTID] [int] NULL
) ON [PRIMARY]

GO
/****** Object:  Table [dbo].[observations_history_sendid_tracker]    Script Date: 7/23/2013 2:50:14 AM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[observations_history_sendid_tracker](
	[SENTID] [int] NULL
) ON [PRIMARY]

GO
/****** Object:  Table [dbo].[observations_history_sendid_tracker_status]    Script Date: 7/23/2013 2:50:14 AM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[observations_history_sendid_tracker_status](
	[SENTID] [int] NULL
) ON [PRIMARY]

GO
/****** Object:  Table [dbo].[weather_hourly_forecast_sendid_tracker]    Script Date: 7/23/2013 2:50:14 AM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[weather_hourly_forecast_sendid_tracker](
	[SENTID] [int] NULL
) ON [PRIMARY]

GO
/****** Object:  Table [dbo].[weather_hourly_forecast_sendid_tracker_status]    Script Date: 7/23/2013 2:50:14 AM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[weather_hourly_forecast_sendid_tracker_status](
	[SENTID] [int] NULL
) ON [PRIMARY]

GO
USE [master]
GO
ALTER DATABASE [TPOCOM] SET  READ_WRITE 
GO
