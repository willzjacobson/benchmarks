USE [master]
GO
/****** Object:  Database [345]    Script Date: 7/22/2013 8:21:54 PM ******/
CREATE DATABASE [345] ON  PRIMARY 
( NAME = N'345', FILENAME = N'E:\Microsoft SQL Server\MSSQL10_50.MSSQLSERVER\MSSQL\DATA\345.mdf' , SIZE = 854016KB , MAXSIZE = UNLIMITED, FILEGROWTH = 1024KB )
 LOG ON 
( NAME = N'345_log', FILENAME = N'E:\Microsoft SQL Server\MSSQL10_50.MSSQLSERVER\MSSQL\DATA\345_log.ldf' , SIZE = 1623488KB , MAXSIZE = 2048GB , FILEGROWTH = 10%)
GO
ALTER DATABASE [345] SET COMPATIBILITY_LEVEL = 100
GO
IF (1 = FULLTEXTSERVICEPROPERTY('IsFullTextInstalled'))
begin
EXEC [345].[dbo].[sp_fulltext_database] @action = 'enable'
end
GO
ALTER DATABASE [345] SET ANSI_NULL_DEFAULT OFF 
GO
ALTER DATABASE [345] SET ANSI_NULLS OFF 
GO
ALTER DATABASE [345] SET ANSI_PADDING OFF 
GO
ALTER DATABASE [345] SET ANSI_WARNINGS OFF 
GO
ALTER DATABASE [345] SET ARITHABORT OFF 
GO
ALTER DATABASE [345] SET AUTO_CLOSE OFF 
GO
ALTER DATABASE [345] SET AUTO_CREATE_STATISTICS ON 
GO
ALTER DATABASE [345] SET AUTO_SHRINK OFF 
GO
ALTER DATABASE [345] SET AUTO_UPDATE_STATISTICS ON 
GO
ALTER DATABASE [345] SET CURSOR_CLOSE_ON_COMMIT OFF 
GO
ALTER DATABASE [345] SET CURSOR_DEFAULT  GLOBAL 
GO
ALTER DATABASE [345] SET CONCAT_NULL_YIELDS_NULL OFF 
GO
ALTER DATABASE [345] SET NUMERIC_ROUNDABORT OFF 
GO
ALTER DATABASE [345] SET QUOTED_IDENTIFIER OFF 
GO
ALTER DATABASE [345] SET RECURSIVE_TRIGGERS OFF 
GO
ALTER DATABASE [345] SET  DISABLE_BROKER 
GO
ALTER DATABASE [345] SET AUTO_UPDATE_STATISTICS_ASYNC OFF 
GO
ALTER DATABASE [345] SET DATE_CORRELATION_OPTIMIZATION OFF 
GO
ALTER DATABASE [345] SET TRUSTWORTHY OFF 
GO
ALTER DATABASE [345] SET ALLOW_SNAPSHOT_ISOLATION OFF 
GO
ALTER DATABASE [345] SET PARAMETERIZATION SIMPLE 
GO
ALTER DATABASE [345] SET READ_COMMITTED_SNAPSHOT OFF 
GO
ALTER DATABASE [345] SET HONOR_BROKER_PRIORITY OFF 
GO
ALTER DATABASE [345] SET RECOVERY FULL 
GO
ALTER DATABASE [345] SET  MULTI_USER 
GO
ALTER DATABASE [345] SET PAGE_VERIFY CHECKSUM  
GO
ALTER DATABASE [345] SET DB_CHAINING OFF 
GO
USE [345]
GO
/****** Object:  User [TPOWEB_USER]    Script Date: 7/22/2013 8:21:55 PM ******/
CREATE USER [TPOWEB_USER] FOR LOGIN [TPOWEB_USER] WITH DEFAULT_SCHEMA=[dbo]
GO
/****** Object:  User [tpo]    Script Date: 7/22/2013 8:21:55 PM ******/
CREATE USER [tpo] FOR LOGIN [tpo] WITH DEFAULT_SCHEMA=[dbo]
GO
/****** Object:  User [rudin_user2]    Script Date: 7/22/2013 8:21:55 PM ******/
CREATE USER [rudin_user2] FOR LOGIN [rudin_user2] WITH DEFAULT_SCHEMA=[dbo]
GO
/****** Object:  User [rudin_user]    Script Date: 7/22/2013 8:21:55 PM ******/
CREATE USER [rudin_user] FOR LOGIN [rudin_user] WITH DEFAULT_SCHEMA=[dbo]
GO
/****** Object:  User [rudin_db_user2]    Script Date: 7/22/2013 8:21:55 PM ******/
CREATE USER [rudin_db_user2] FOR LOGIN [rudin_db_user2] WITH DEFAULT_SCHEMA=[dbo]
GO
/****** Object:  User [ANDERSON\ashwath]    Script Date: 7/22/2013 8:21:55 PM ******/
CREATE USER [ANDERSON\ashwath] FOR LOGIN [ANDERSON\ashwath] WITH DEFAULT_SCHEMA=[dbo]
GO
/****** Object:  User [ANDERSON\agagneja]    Script Date: 7/22/2013 8:21:55 PM ******/
CREATE USER [ANDERSON\agagneja] FOR LOGIN [ANDERSON\agagneja] WITH DEFAULT_SCHEMA=[dbo]
GO
ALTER ROLE [db_datareader] ADD MEMBER [TPOWEB_USER]
GO
ALTER ROLE [db_accessadmin] ADD MEMBER [tpo]
GO
ALTER ROLE [db_datareader] ADD MEMBER [tpo]
GO
ALTER ROLE [db_datawriter] ADD MEMBER [tpo]
GO
ALTER ROLE [db_owner] ADD MEMBER [rudin_user2]
GO
ALTER ROLE [db_owner] ADD MEMBER [rudin_user]
GO
ALTER ROLE [db_datareader] ADD MEMBER [rudin_db_user2]
GO
ALTER ROLE [db_datawriter] ADD MEMBER [rudin_db_user2]
GO
ALTER ROLE [db_owner] ADD MEMBER [ANDERSON\ashwath]
GO
ALTER ROLE [db_owner] ADD MEMBER [ANDERSON\agagneja]
GO
/****** Object:  Table [dbo].[345_floor_zone_map]    Script Date: 7/22/2013 8:21:55 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[345_floor_zone_map](
	[FLOOR] [nvarchar](4) NOT NULL,
	[ZONE] [smallint] NOT NULL
) ON [PRIMARY]

GO
/****** Object:  Table [dbo].[345---------000ACS---TURINC---IN001]    Script Date: 7/22/2013 8:21:56 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[345---------000ACS---TURINC---IN001](
	[ID] [int] IDENTITY(1,1) NOT NULL,
	[ZONE] [nchar](3) NULL,
	[FLOOR] [nchar](3) NULL,
	[QUADRANT] [nchar](3) NULL,
	[EQUIPMENT_NO] [nchar](3) NULL,
	[TIMESTAMP] [datetime] NULL,
	[VALUE] [float] NULL,
PRIMARY KEY CLUSTERED 
(
	[ID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]

GO
/****** Object:  Table [dbo].[345---------000ACS---TUROUT---OUT001]    Script Date: 7/22/2013 8:21:56 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[345---------000ACS---TUROUT---OUT001](
	[ID] [int] IDENTITY(1,1) NOT NULL,
	[ZONE] [nchar](3) NULL,
	[FLOOR] [nchar](3) NULL,
	[QUADRANT] [nchar](3) NULL,
	[EQUIPMENT_NO] [nchar](3) NULL,
	[TIMESTAMP] [datetime] NULL,
	[VALUE] [float] NULL,
PRIMARY KEY CLUSTERED 
(
	[ID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]

GO
/****** Object:  Table [dbo].[345---------000SECCNTPEOBUI---INC001]    Script Date: 7/22/2013 8:21:56 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[345---------000SECCNTPEOBUI---INC001](
	[ID] [int] IDENTITY(1,1) NOT NULL,
	[ZONE] [nchar](3) NULL,
	[FLOOR] [nchar](3) NULL,
	[QUADRANT] [nchar](3) NULL,
	[EQUIPMENT_NO] [nchar](3) NULL,
	[TIMESTAMP] [datetime] NULL,
	[VALUE] [float] NULL,
PRIMARY KEY CLUSTERED 
(
	[ID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]

GO
/****** Object:  Table [dbo].[345---------000SECCNTPEOBUI---OUT001]    Script Date: 7/22/2013 8:21:56 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[345---------000SECCNTPEOBUI---OUT001](
	[ID] [int] IDENTITY(1,1) NOT NULL,
	[ZONE] [nchar](3) NULL,
	[FLOOR] [nchar](3) NULL,
	[QUADRANT] [nchar](3) NULL,
	[EQUIPMENT_NO] [nchar](3) NULL,
	[TIMESTAMP] [datetime] NULL,
	[VALUE] [float] NULL,
PRIMARY KEY CLUSTERED 
(
	[ID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]

GO
/****** Object:  Table [dbo].[345---------000SECCNTPEOBUI---VAL001]    Script Date: 7/22/2013 8:21:56 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[345---------000SECCNTPEOBUI---VAL001](
	[ID] [int] IDENTITY(1,1) NOT NULL,
	[ZONE] [nchar](3) NULL,
	[FLOOR] [nchar](3) NULL,
	[QUADRANT] [nchar](3) NULL,
	[EQUIPMENT_NO] [nchar](3) NULL,
	[TIMESTAMP] [datetime] NULL,
	[VALUE] [float] NULL,
PRIMARY KEY CLUSTERED 
(
	[ID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]

GO
/****** Object:  Table [dbo].[345---------000TPO---ALA---001]    Script Date: 7/22/2013 8:21:56 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
SET ANSI_PADDING ON
GO
CREATE TABLE [dbo].[345---------000TPO---ALA---001](
	[ID] [int] IDENTITY(1,1) NOT NULL,
	[STATE] [int] NULL,
	[PROPERTY_PRIO] [int] NULL,
	[INTERNAL] [int] NULL,
	[INITTS] [datetime] NULL,
	[NORMTS] [datetime] NULL,
	[PBS] [varchar](10) NULL,
	[SIGN] [varchar](100) NULL,
 CONSTRAINT [PK_345---------000TPO---ALA---001] PRIMARY KEY CLUSTERED 
(
	[ID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]

GO
SET ANSI_PADDING OFF
GO
/****** Object:  Table [dbo].[345---------000TPOFORELECON001---001]    Script Date: 7/22/2013 8:21:56 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[345---------000TPOFORELECON001---001](
	[Run_DateTime] [datetime] NOT NULL,
	[Prediction_DateTime] [datetime] NOT NULL,
	[Prediction_Value] [float] NULL,
	[Lower_Bound_95] [float] NULL,
	[Upper_Bound_95] [float] NULL,
	[Lower_Bound_68] [float] NULL,
	[Upper_Bound_68] [float] NULL,
	[ID] [int] IDENTITY(1,1) NOT NULL,
PRIMARY KEY CLUSTERED 
(
	[Run_DateTime] ASC,
	[Prediction_DateTime] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]

GO
/****** Object:  Table [dbo].[345---------000TPOFORELECON001---001_KPMG]    Script Date: 7/22/2013 8:21:56 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[345---------000TPOFORELECON001---001_KPMG](
	[Run_DateTime] [datetime] NOT NULL,
	[Prediction_DateTime] [datetime] NOT NULL,
	[Prediction_Value] [float] NULL,
	[Lower_Bound_95] [float] NULL,
	[Upper_Bound_95] [float] NULL,
	[Lower_Bound_68] [float] NULL,
	[Upper_Bound_68] [float] NULL,
	[ID] [int] IDENTITY(1,1) NOT NULL,
PRIMARY KEY CLUSTERED 
(
	[Run_DateTime] ASC,
	[Prediction_DateTime] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]

GO
/****** Object:  Table [dbo].[345---------000TPOFORELECON001---001_KPMG_RBF_Params]    Script Date: 7/22/2013 8:21:56 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[345---------000TPOFORELECON001---001_KPMG_RBF_Params](
	[Run_DateTime] [datetime] NOT NULL,
	[Hour] [smallint] NOT NULL,
	[c] [float] NOT NULL,
	[gamma] [float] NOT NULL,
	[avg_error] [float] NOT NULL,
PRIMARY KEY CLUSTERED 
(
	[Run_DateTime] ASC,
	[Hour] ASC,
	[c] ASC,
	[gamma] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]

GO
/****** Object:  Table [dbo].[345---------000TPOFORELECON001---001_KPMG_stats]    Script Date: 7/22/2013 8:21:56 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[345---------000TPOFORELECON001---001_KPMG_stats](
	[Prediction_Date] [datetime] NOT NULL,
	[RMSE] [float] NOT NULL,
	[MAE] [float] NOT NULL,
	[MAPE] [float] NOT NULL,
PRIMARY KEY CLUSTERED 
(
	[Prediction_Date] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]

GO
/****** Object:  Table [dbo].[345---------000TPOFORELECON001---001_NFL]    Script Date: 7/22/2013 8:21:56 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[345---------000TPOFORELECON001---001_NFL](
	[Run_DateTime] [datetime] NOT NULL,
	[Prediction_DateTime] [datetime] NOT NULL,
	[Prediction_Value] [float] NULL,
	[Lower_Bound_95] [float] NULL,
	[Upper_Bound_95] [float] NULL,
	[Lower_Bound_68] [float] NULL,
	[Upper_Bound_68] [float] NULL,
	[ID] [int] IDENTITY(1,1) NOT NULL,
PRIMARY KEY CLUSTERED 
(
	[Run_DateTime] ASC,
	[Prediction_DateTime] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]

GO
/****** Object:  Table [dbo].[345---------000TPOFORELECON001---001_NFL_RBF_Params]    Script Date: 7/22/2013 8:21:56 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[345---------000TPOFORELECON001---001_NFL_RBF_Params](
	[Run_DateTime] [datetime] NOT NULL,
	[Hour] [smallint] NOT NULL,
	[c] [float] NOT NULL,
	[gamma] [float] NOT NULL,
	[avg_error] [float] NOT NULL,
PRIMARY KEY CLUSTERED 
(
	[Run_DateTime] ASC,
	[Hour] ASC,
	[c] ASC,
	[gamma] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]

GO
/****** Object:  Table [dbo].[345---------000TPOFORELECON001---001_NFL_stats]    Script Date: 7/22/2013 8:21:56 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[345---------000TPOFORELECON001---001_NFL_stats](
	[Prediction_Date] [datetime] NOT NULL,
	[RMSE] [float] NOT NULL,
	[MAE] [float] NOT NULL,
	[MAPE] [float] NOT NULL,
PRIMARY KEY CLUSTERED 
(
	[Prediction_Date] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]

GO
/****** Object:  Table [dbo].[345---------000TPOFORELECON001---001_RBF_Params]    Script Date: 7/22/2013 8:21:56 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[345---------000TPOFORELECON001---001_RBF_Params](
	[Run_DateTime] [datetime] NOT NULL,
	[Hour] [smallint] NOT NULL,
	[c] [float] NOT NULL,
	[gamma] [float] NOT NULL,
	[avg_error] [float] NOT NULL,
PRIMARY KEY CLUSTERED 
(
	[Run_DateTime] ASC,
	[Hour] ASC,
	[c] ASC,
	[gamma] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]

GO
/****** Object:  Table [dbo].[345---------000TPOFORELECON001---001_stats]    Script Date: 7/22/2013 8:21:56 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[345---------000TPOFORELECON001---001_stats](
	[Prediction_Date] [datetime] NOT NULL,
	[RMSE] [float] NOT NULL,
	[MAE] [float] NOT NULL,
	[MAPE] [float] NOT NULL,
PRIMARY KEY CLUSTERED 
(
	[Prediction_Date] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]

GO
/****** Object:  Table [dbo].[345---------000TPOFORSTECON001---001]    Script Date: 7/22/2013 8:21:56 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[345---------000TPOFORSTECON001---001](
	[Run_DateTime] [datetime] NOT NULL,
	[Prediction_DateTime] [datetime] NOT NULL,
	[Prediction_Value] [float] NULL,
	[Lower_Bound_95] [float] NULL,
	[Upper_Bound_95] [float] NULL,
	[Lower_Bound_68] [float] NULL,
	[Upper_Bound_68] [float] NULL,
	[ID] [int] IDENTITY(1,1) NOT NULL,
PRIMARY KEY CLUSTERED 
(
	[Run_DateTime] ASC,
	[Prediction_DateTime] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]

GO
/****** Object:  Table [dbo].[345---------000TPOFORSTECON001---001_RBF_Params]    Script Date: 7/22/2013 8:21:56 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[345---------000TPOFORSTECON001---001_RBF_Params](
	[Run_DateTime] [datetime] NOT NULL,
	[Hour] [smallint] NOT NULL,
	[c] [float] NOT NULL,
	[gamma] [float] NOT NULL,
	[avg_error] [float] NOT NULL,
PRIMARY KEY CLUSTERED 
(
	[Run_DateTime] ASC,
	[Hour] ASC,
	[c] ASC,
	[gamma] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]

GO
/****** Object:  Table [dbo].[345---------000TPOFORSTECON001---001_Stats]    Script Date: 7/22/2013 8:21:56 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[345---------000TPOFORSTECON001---001_Stats](
	[Prediction_Date] [datetime] NOT NULL,
	[RMSE] [float] NOT NULL,
	[MAE] [float] NOT NULL,
	[MAPE] [float] NOT NULL,
PRIMARY KEY CLUSTERED 
(
	[Prediction_Date] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]

GO
/****** Object:  Table [dbo].[345---------000TPOFORTEMSPA001---001]    Script Date: 7/22/2013 8:21:56 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[345---------000TPOFORTEMSPA001---001](
	[Run_DateTime] [datetime] NOT NULL,
	[Prediction_DateTime] [datetime] NOT NULL,
	[Floor] [nvarchar](20) NOT NULL,
	[Quadrant] [nvarchar](20) NOT NULL,
	[Prediction_Value] [float] NULL,
	[Lower_Bound_95] [float] NULL,
	[Upper_Bound_95] [float] NULL,
	[Lower_Bound_68] [float] NULL,
	[Upper_Bound_68] [float] NULL,
	[ID] [int] IDENTITY(1,1) NOT NULL,
PRIMARY KEY CLUSTERED 
(
	[Run_DateTime] ASC,
	[Prediction_DateTime] ASC,
	[Floor] ASC,
	[Quadrant] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]

GO
/****** Object:  Table [dbo].[345---------000TPOFORTEMSPA001---001_Deltas]    Script Date: 7/22/2013 8:21:56 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[345---------000TPOFORTEMSPA001---001_Deltas](
	[Timestamp] [datetime] NOT NULL,
	[Floor] [nvarchar](20) NOT NULL,
	[Quadrant] [nvarchar](20) NOT NULL,
	[Predicted_Delta] [float] NULL,
	[Actual_Delta] [float] NULL,
PRIMARY KEY CLUSTERED 
(
	[Timestamp] ASC,
	[Floor] ASC,
	[Quadrant] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]

GO
/****** Object:  Table [dbo].[345---------000TPOFORTEMSPA001---001_Deltas_orig]    Script Date: 7/22/2013 8:21:56 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[345---------000TPOFORTEMSPA001---001_Deltas_orig](
	[Timestamp] [datetime] NOT NULL,
	[Floor] [smallint] NOT NULL,
	[Quadrant] [nvarchar](20) NOT NULL,
	[Predicted_Delta] [float] NULL,
	[Actual_Delta] [float] NULL,
PRIMARY KEY CLUSTERED 
(
	[Timestamp] ASC,
	[Floor] ASC,
	[Quadrant] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]

GO
/****** Object:  Table [dbo].[345---------000TPOFORTEMSPA001---001_Derivative]    Script Date: 7/22/2013 8:21:56 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[345---------000TPOFORTEMSPA001---001_Derivative](
	[Run_DateTime] [datetime] NOT NULL,
	[Prediction_DateTime] [datetime] NOT NULL,
	[Floor] [nvarchar](20) NOT NULL,
	[Quadrant] [nvarchar](20) NOT NULL,
	[Predicted_Slope] [float] NOT NULL,
PRIMARY KEY CLUSTERED 
(
	[Run_DateTime] ASC,
	[Prediction_DateTime] ASC,
	[Floor] ASC,
	[Quadrant] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]

GO
/****** Object:  Table [dbo].[345---------000TPOFORTEMSPA001---001_Derivative_orig]    Script Date: 7/22/2013 8:21:56 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[345---------000TPOFORTEMSPA001---001_Derivative_orig](
	[Run_DateTime] [datetime] NOT NULL,
	[Prediction_DateTime] [datetime] NOT NULL,
	[Floor] [smallint] NOT NULL,
	[Quadrant] [nvarchar](20) NOT NULL,
	[Predicted_Slope] [float] NOT NULL,
PRIMARY KEY CLUSTERED 
(
	[Run_DateTime] ASC,
	[Prediction_DateTime] ASC,
	[Floor] ASC,
	[Quadrant] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]

GO
/****** Object:  Table [dbo].[345---------000TPOFORTEMSPA001---001_orig]    Script Date: 7/22/2013 8:21:56 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[345---------000TPOFORTEMSPA001---001_orig](
	[Run_DateTime] [datetime] NOT NULL,
	[Prediction_DateTime] [datetime] NOT NULL,
	[Floor] [int] NOT NULL,
	[Quadrant] [nvarchar](2) NOT NULL,
	[Prediction_Value] [float] NULL,
	[Lower_Bound_95] [float] NULL,
	[Upper_Bound_95] [float] NULL,
	[Lower_Bound_68] [float] NULL,
	[Upper_Bound_68] [float] NULL,
	[ID] [int] IDENTITY(1,1) NOT NULL,
PRIMARY KEY CLUSTERED 
(
	[Run_DateTime] ASC,
	[Prediction_DateTime] ASC,
	[Floor] ASC,
	[Quadrant] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]

GO
/****** Object:  Table [dbo].[345---------000TPOFORTEMSPA001---001_RBF_Params]    Script Date: 7/22/2013 8:21:56 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[345---------000TPOFORTEMSPA001---001_RBF_Params](
	[Run_DateTime] [datetime] NOT NULL,
	[Floor] [nvarchar](20) NOT NULL,
	[Quadrant] [nvarchar](20) NOT NULL,
	[Hour] [smallint] NOT NULL,
	[c] [float] NOT NULL,
	[gamma] [float] NOT NULL,
	[avg_error] [float] NOT NULL,
PRIMARY KEY CLUSTERED 
(
	[Run_DateTime] ASC,
	[Hour] ASC,
	[Floor] ASC,
	[Quadrant] ASC,
	[c] ASC,
	[gamma] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]

GO
/****** Object:  Table [dbo].[345---------000TPOFORTEMSPA001---001_RBF_Params_orig]    Script Date: 7/22/2013 8:21:56 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[345---------000TPOFORTEMSPA001---001_RBF_Params_orig](
	[Run_DateTime] [datetime] NOT NULL,
	[Floor] [smallint] NOT NULL,
	[Quadrant] [nvarchar](2) NOT NULL,
	[Hour] [smallint] NOT NULL,
	[c] [float] NOT NULL,
	[gamma] [float] NOT NULL,
	[avg_error] [float] NOT NULL,
PRIMARY KEY CLUSTERED 
(
	[Run_DateTime] ASC,
	[Hour] ASC,
	[Floor] ASC,
	[Quadrant] ASC,
	[c] ASC,
	[gamma] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]

GO
/****** Object:  Table [dbo].[345---------000TPOFORTEMSPA001---001_Stats]    Script Date: 7/22/2013 8:21:56 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[345---------000TPOFORTEMSPA001---001_Stats](
	[Prediction_Date] [datetime] NOT NULL,
	[Floor] [nvarchar](20) NOT NULL,
	[Quadrant] [nvarchar](20) NOT NULL,
	[RMSE] [float] NOT NULL,
	[MAE] [float] NOT NULL,
	[MAPE] [float] NOT NULL
) ON [PRIMARY]

GO
/****** Object:  Table [dbo].[345---------000TPOFORTEMSPA001---001_Stats_orig]    Script Date: 7/22/2013 8:21:56 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[345---------000TPOFORTEMSPA001---001_Stats_orig](
	[Prediction_Date] [datetime] NOT NULL,
	[Floor] [smallint] NOT NULL,
	[Quadrant] [nvarchar](2) NOT NULL,
	[RMSE] [float] NOT NULL,
	[MAE] [float] NOT NULL,
	[MAPE] [float] NOT NULL
) ON [PRIMARY]

GO
/****** Object:  Table [dbo].[345---------000TPONOWTEMSPA001---001]    Script Date: 7/22/2013 8:21:56 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[345---------000TPONOWTEMSPA001---001](
	[Run_DateTime] [datetime] NULL,
	[Prediction_DateTime] [datetime] NULL,
	[Value] [real] NULL,
	[Floor] [nchar](3) NULL,
	[Quadrant] [nchar](3) NULL,
	[Prediction_Timestep] [datetime] NULL,
	[ID] [int] IDENTITY(1,1) NOT NULL,
	[Control_Setting] [float] NULL,
 CONSTRAINT [PK_spaceTemperature_trajectory] PRIMARY KEY CLUSTERED 
(
	[ID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]

GO
/****** Object:  Table [dbo].[345---------000TPOOPTTEMRDW001---001]    Script Date: 7/22/2013 8:21:56 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[345---------000TPOOPTTEMRDW001---001](
	[ID] [int] IDENTITY(1,1) NOT NULL,
	[Run_DateTime] [datetime] NULL,
	[Prediction_DateTime] [datetime] NULL,
 CONSTRAINT [PK_rampdown_time_rec] PRIMARY KEY CLUSTERED 
(
	[ID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]

GO
/****** Object:  Table [dbo].[345---------000TPOOPTTEMUPT001---001]    Script Date: 7/22/2013 8:21:56 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[345---------000TPOOPTTEMUPT001---001](
	[ID] [int] IDENTITY(1,1) NOT NULL,
	[Run_DateTime] [datetime] NULL,
	[Prediction_DateTime] [datetime] NULL,
 CONSTRAINT [PK_startup_time_rec] PRIMARY KEY CLUSTERED 
(
	[ID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]

GO
/****** Object:  Table [dbo].[345---------001BMSELEMET------VAL001]    Script Date: 7/22/2013 8:21:56 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[345---------001BMSELEMET------VAL001](
	[ID] [int] IDENTITY(1,1) NOT NULL,
	[ZONE] [nchar](3) NULL,
	[FLOOR] [nchar](3) NULL,
	[QUADRANT] [nchar](3) NULL,
	[EQUIPMENT_NO] [nchar](3) NULL,
	[TIMESTAMP] [datetime] NULL,
	[VALUE] [float] NULL,
PRIMARY KEY CLUSTERED 
(
	[ID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]

GO
/****** Object:  Table [dbo].[345---------001BMSHVAFANCWV---VAL001]    Script Date: 7/22/2013 8:21:56 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[345---------001BMSHVAFANCWV---VAL001](
	[ID] [int] IDENTITY(1,1) NOT NULL,
	[ZONE] [nchar](3) NULL,
	[FLOOR] [nchar](3) NULL,
	[QUADRANT] [nchar](3) NULL,
	[EQUIPMENT_NO] [nchar](3) NULL,
	[TIMESTAMP] [datetime] NULL,
	[VALUE] [float] NULL,
PRIMARY KEY CLUSTERED 
(
	[ID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]

GO
/****** Object:  Table [dbo].[345---------001BMSHVAFANLCP---VAL001]    Script Date: 7/22/2013 8:21:56 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[345---------001BMSHVAFANLCP---VAL001](
	[ID] [int] IDENTITY(1,1) NOT NULL,
	[ZONE] [nchar](3) NULL,
	[FLOOR] [nchar](3) NULL,
	[QUADRANT] [nchar](3) NULL,
	[EQUIPMENT_NO] [nchar](3) NULL,
	[TIMESTAMP] [datetime] NULL,
	[VALUE] [float] NULL,
PRIMARY KEY CLUSTERED 
(
	[ID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]

GO
/****** Object:  Table [dbo].[345---------001BMSHVAFANRAT---VAL001]    Script Date: 7/22/2013 8:21:56 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[345---------001BMSHVAFANRAT---VAL001](
	[ID] [int] IDENTITY(1,1) NOT NULL,
	[ZONE] [nchar](3) NULL,
	[FLOOR] [nchar](3) NULL,
	[QUADRANT] [nchar](3) NULL,
	[EQUIPMENT_NO] [nchar](3) NULL,
	[TIMESTAMP] [datetime] NULL,
	[VALUE] [float] NULL,
PRIMARY KEY CLUSTERED 
(
	[ID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]

GO
/****** Object:  Table [dbo].[345---------001BMSHVAFANRHC---SPV001]    Script Date: 7/22/2013 8:21:56 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[345---------001BMSHVAFANRHC---SPV001](
	[ID] [int] IDENTITY(1,1) NOT NULL,
	[ZONE] [nchar](3) NULL,
	[FLOOR] [nchar](3) NULL,
	[QUADRANT] [nchar](3) NULL,
	[EQUIPMENT_NO] [nchar](3) NULL,
	[TIMESTAMP] [datetime] NULL,
	[VALUE] [float] NULL,
PRIMARY KEY CLUSTERED 
(
	[ID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]

GO
/****** Object:  Table [dbo].[345---------001BMSHVAFANRHC---VAL001]    Script Date: 7/22/2013 8:21:56 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[345---------001BMSHVAFANRHC---VAL001](
	[ID] [int] IDENTITY(1,1) NOT NULL,
	[ZONE] [nchar](3) NULL,
	[FLOOR] [nchar](3) NULL,
	[QUADRANT] [nchar](3) NULL,
	[EQUIPMENT_NO] [nchar](3) NULL,
	[TIMESTAMP] [datetime] NULL,
	[VALUE] [float] NULL,
PRIMARY KEY CLUSTERED 
(
	[ID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]

GO
/****** Object:  Table [dbo].[345---------001BMSHVAFANSAT---SPV001]    Script Date: 7/22/2013 8:21:56 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[345---------001BMSHVAFANSAT---SPV001](
	[ID] [int] IDENTITY(1,1) NOT NULL,
	[ZONE] [nchar](3) NULL,
	[FLOOR] [nchar](3) NULL,
	[QUADRANT] [nchar](3) NULL,
	[EQUIPMENT_NO] [nchar](3) NULL,
	[TIMESTAMP] [datetime] NULL,
	[VALUE] [float] NULL,
PRIMARY KEY CLUSTERED 
(
	[ID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]

GO
/****** Object:  Table [dbo].[345---------001BMSHVAFANSAT---VAL001]    Script Date: 7/22/2013 8:21:56 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[345---------001BMSHVAFANSAT---VAL001](
	[ID] [int] IDENTITY(1,1) NOT NULL,
	[ZONE] [nchar](3) NULL,
	[FLOOR] [nchar](3) NULL,
	[QUADRANT] [nchar](3) NULL,
	[EQUIPMENT_NO] [nchar](3) NULL,
	[TIMESTAMP] [datetime] NULL,
	[VALUE] [float] NULL,
PRIMARY KEY CLUSTERED 
(
	[ID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]

GO
/****** Object:  Table [dbo].[345---------001BMSHVAMCT------ALA001]    Script Date: 7/22/2013 8:21:56 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[345---------001BMSHVAMCT------ALA001](
	[ID] [int] IDENTITY(1,1) NOT NULL,
	[ZONE] [nchar](3) NULL,
	[FLOOR] [nchar](3) NULL,
	[QUADRANT] [nchar](3) NULL,
	[EQUIPMENT_NO] [nchar](3) NULL,
	[TIMESTAMP] [datetime] NULL,
	[VALUE] [float] NULL,
PRIMARY KEY CLUSTERED 
(
	[ID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]

GO
/****** Object:  Table [dbo].[345---------001BMSHVAMCT------ALA002]    Script Date: 7/22/2013 8:21:56 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[345---------001BMSHVAMCT------ALA002](
	[ID] [int] IDENTITY(1,1) NOT NULL,
	[ZONE] [nchar](3) NULL,
	[FLOOR] [nchar](3) NULL,
	[QUADRANT] [nchar](3) NULL,
	[EQUIPMENT_NO] [nchar](3) NULL,
	[TIMESTAMP] [datetime] NULL,
	[VALUE] [float] NULL,
PRIMARY KEY CLUSTERED 
(
	[ID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]

GO
/****** Object:  Table [dbo].[345---------001BMSHVAMCT------ALA003]    Script Date: 7/22/2013 8:21:56 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[345---------001BMSHVAMCT------ALA003](
	[ID] [int] IDENTITY(1,1) NOT NULL,
	[ZONE] [nchar](3) NULL,
	[FLOOR] [nchar](3) NULL,
	[QUADRANT] [nchar](3) NULL,
	[EQUIPMENT_NO] [nchar](3) NULL,
	[TIMESTAMP] [datetime] NULL,
	[VALUE] [float] NULL,
PRIMARY KEY CLUSTERED 
(
	[ID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]

GO
/****** Object:  Table [dbo].[345---------001BMSHVAMCT------ALA004]    Script Date: 7/22/2013 8:21:56 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[345---------001BMSHVAMCT------ALA004](
	[ID] [int] IDENTITY(1,1) NOT NULL,
	[ZONE] [nchar](3) NULL,
	[FLOOR] [nchar](3) NULL,
	[QUADRANT] [nchar](3) NULL,
	[EQUIPMENT_NO] [nchar](3) NULL,
	[TIMESTAMP] [datetime] NULL,
	[VALUE] [float] NULL,
PRIMARY KEY CLUSTERED 
(
	[ID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]

GO
/****** Object:  Table [dbo].[345---------001BMSHVAMCT------ALA005]    Script Date: 7/22/2013 8:21:56 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[345---------001BMSHVAMCT------ALA005](
	[ID] [int] IDENTITY(1,1) NOT NULL,
	[ZONE] [nchar](3) NULL,
	[FLOOR] [nchar](3) NULL,
	[QUADRANT] [nchar](3) NULL,
	[EQUIPMENT_NO] [nchar](3) NULL,
	[TIMESTAMP] [datetime] NULL,
	[VALUE] [float] NULL,
PRIMARY KEY CLUSTERED 
(
	[ID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]

GO
/****** Object:  Table [dbo].[345---------001BMSHVAPFACWV---VAL001]    Script Date: 7/22/2013 8:21:56 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[345---------001BMSHVAPFACWV---VAL001](
	[ID] [int] IDENTITY(1,1) NOT NULL,
	[ZONE] [nchar](3) NULL,
	[FLOOR] [nchar](3) NULL,
	[QUADRANT] [nchar](3) NULL,
	[EQUIPMENT_NO] [nchar](3) NULL,
	[TIMESTAMP] [datetime] NULL,
	[VALUE] [float] NULL,
PRIMARY KEY CLUSTERED 
(
	[ID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]

GO
/****** Object:  Table [dbo].[345---------001BMSHVAPFALCP---VAL001]    Script Date: 7/22/2013 8:21:56 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[345---------001BMSHVAPFALCP---VAL001](
	[ID] [int] IDENTITY(1,1) NOT NULL,
	[ZONE] [nchar](3) NULL,
	[FLOOR] [nchar](3) NULL,
	[QUADRANT] [nchar](3) NULL,
	[EQUIPMENT_NO] [nchar](3) NULL,
	[TIMESTAMP] [datetime] NULL,
	[VALUE] [float] NULL,
PRIMARY KEY CLUSTERED 
(
	[ID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]

GO
/****** Object:  Table [dbo].[345---------001BMSHVAPFARAT---VAL001]    Script Date: 7/22/2013 8:21:56 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[345---------001BMSHVAPFARAT---VAL001](
	[ID] [int] IDENTITY(1,1) NOT NULL,
	[ZONE] [nchar](3) NULL,
	[FLOOR] [nchar](3) NULL,
	[QUADRANT] [nchar](3) NULL,
	[EQUIPMENT_NO] [nchar](3) NULL,
	[TIMESTAMP] [datetime] NULL,
	[VALUE] [float] NULL,
PRIMARY KEY CLUSTERED 
(
	[ID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]

GO
/****** Object:  Table [dbo].[345---------001BMSHVAPFARHC---VAL001]    Script Date: 7/22/2013 8:21:56 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[345---------001BMSHVAPFARHC---VAL001](
	[ID] [int] IDENTITY(1,1) NOT NULL,
	[ZONE] [nchar](3) NULL,
	[FLOOR] [nchar](3) NULL,
	[QUADRANT] [nchar](3) NULL,
	[EQUIPMENT_NO] [nchar](3) NULL,
	[TIMESTAMP] [datetime] NULL,
	[VALUE] [float] NULL,
PRIMARY KEY CLUSTERED 
(
	[ID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]

GO
/****** Object:  Table [dbo].[345---------001BMSHVAPFASAT---SPV001]    Script Date: 7/22/2013 8:21:56 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[345---------001BMSHVAPFASAT---SPV001](
	[ID] [int] IDENTITY(1,1) NOT NULL,
	[ZONE] [nchar](3) NULL,
	[FLOOR] [nchar](3) NULL,
	[QUADRANT] [nchar](3) NULL,
	[EQUIPMENT_NO] [nchar](3) NULL,
	[TIMESTAMP] [datetime] NULL,
	[VALUE] [float] NULL,
PRIMARY KEY CLUSTERED 
(
	[ID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]

GO
/****** Object:  Table [dbo].[345---------001BMSHVAPNE------ALA001]    Script Date: 7/22/2013 8:21:56 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[345---------001BMSHVAPNE------ALA001](
	[ID] [int] IDENTITY(1,1) NOT NULL,
	[ZONE] [nchar](3) NULL,
	[FLOOR] [nchar](3) NULL,
	[QUADRANT] [nchar](3) NULL,
	[EQUIPMENT_NO] [nchar](3) NULL,
	[TIMESTAMP] [datetime] NULL,
	[VALUE] [float] NULL,
PRIMARY KEY CLUSTERED 
(
	[ID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]

GO
/****** Object:  Table [dbo].[345---------001BMSHVATCT------ALA001]    Script Date: 7/22/2013 8:21:56 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[345---------001BMSHVATCT------ALA001](
	[ID] [int] IDENTITY(1,1) NOT NULL,
	[ZONE] [nchar](3) NULL,
	[FLOOR] [nchar](3) NULL,
	[QUADRANT] [nchar](3) NULL,
	[EQUIPMENT_NO] [nchar](3) NULL,
	[TIMESTAMP] [datetime] NULL,
	[VALUE] [float] NULL,
PRIMARY KEY CLUSTERED 
(
	[ID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]

GO
/****** Object:  Table [dbo].[345---------001BMSHVATCT------ALA002]    Script Date: 7/22/2013 8:21:56 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[345---------001BMSHVATCT------ALA002](
	[ID] [int] IDENTITY(1,1) NOT NULL,
	[ZONE] [nchar](3) NULL,
	[FLOOR] [nchar](3) NULL,
	[QUADRANT] [nchar](3) NULL,
	[EQUIPMENT_NO] [nchar](3) NULL,
	[TIMESTAMP] [datetime] NULL,
	[VALUE] [float] NULL,
PRIMARY KEY CLUSTERED 
(
	[ID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]

GO
/****** Object:  Table [dbo].[345---------001BMSHVATCT------ALA003]    Script Date: 7/22/2013 8:21:56 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[345---------001BMSHVATCT------ALA003](
	[ID] [int] IDENTITY(1,1) NOT NULL,
	[ZONE] [nchar](3) NULL,
	[FLOOR] [nchar](3) NULL,
	[QUADRANT] [nchar](3) NULL,
	[EQUIPMENT_NO] [nchar](3) NULL,
	[TIMESTAMP] [datetime] NULL,
	[VALUE] [float] NULL,
PRIMARY KEY CLUSTERED 
(
	[ID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]

GO
/****** Object:  Table [dbo].[345---------001BMSHVATEMPSP---VAL001]    Script Date: 7/22/2013 8:21:56 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[345---------001BMSHVATEMPSP---VAL001](
	[ID] [int] IDENTITY(1,1) NOT NULL,
	[ZONE] [nchar](3) NULL,
	[FLOOR] [nchar](3) NULL,
	[QUADRANT] [nchar](3) NULL,
	[EQUIPMENT_NO] [nchar](3) NULL,
	[TIMESTAMP] [datetime] NULL,
	[VALUE] [float] NULL,
PRIMARY KEY CLUSTERED 
(
	[ID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]

GO
/****** Object:  Table [dbo].[345---------001BMSHVATEMSPA---VAL001]    Script Date: 7/22/2013 8:21:56 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[345---------001BMSHVATEMSPA---VAL001](
	[ID] [int] IDENTITY(1,1) NOT NULL,
	[ZONE] [nchar](3) NULL,
	[FLOOR] [nchar](3) NULL,
	[QUADRANT] [nchar](3) NULL,
	[EQUIPMENT_NO] [nchar](3) NULL,
	[TIMESTAMP] [datetime] NULL,
	[VALUE] [float] NULL,
PRIMARY KEY CLUSTERED 
(
	[ID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]

GO
/****** Object:  Table [dbo].[345---------001BMSHVAWEAHUM---AVG001]    Script Date: 7/22/2013 8:21:56 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[345---------001BMSHVAWEAHUM---AVG001](
	[ID] [int] IDENTITY(1,1) NOT NULL,
	[ZONE] [nchar](3) NULL,
	[FLOOR] [nchar](3) NULL,
	[QUADRANT] [nchar](3) NULL,
	[EQUIPMENT_NO] [nchar](3) NULL,
	[TIMESTAMP] [datetime] NULL,
	[VALUE] [float] NULL,
PRIMARY KEY CLUSTERED 
(
	[ID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]

GO
/****** Object:  Table [dbo].[345---------001BMSHVAWEAHUM---VAL001]    Script Date: 7/22/2013 8:21:56 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[345---------001BMSHVAWEAHUM---VAL001](
	[ID] [int] IDENTITY(1,1) NOT NULL,
	[ZONE] [nchar](3) NULL,
	[FLOOR] [nchar](3) NULL,
	[QUADRANT] [nchar](3) NULL,
	[EQUIPMENT_NO] [nchar](3) NULL,
	[TIMESTAMP] [datetime] NULL,
	[VALUE] [float] NULL,
PRIMARY KEY CLUSTERED 
(
	[ID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]

GO
/****** Object:  Table [dbo].[345---------001BMSHVAWEATEM---AVG001]    Script Date: 7/22/2013 8:21:56 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[345---------001BMSHVAWEATEM---AVG001](
	[ID] [int] IDENTITY(1,1) NOT NULL,
	[ZONE] [nchar](3) NULL,
	[FLOOR] [nchar](3) NULL,
	[QUADRANT] [nchar](3) NULL,
	[EQUIPMENT_NO] [nchar](3) NULL,
	[TIMESTAMP] [datetime] NULL,
	[VALUE] [float] NULL,
PRIMARY KEY CLUSTERED 
(
	[ID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]

GO
/****** Object:  Table [dbo].[345---------001BMSHVAWEATEM---VAL001]    Script Date: 7/22/2013 8:21:56 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[345---------001BMSHVAWEATEM---VAL001](
	[ID] [int] IDENTITY(1,1) NOT NULL,
	[ZONE] [nchar](3) NULL,
	[FLOOR] [nchar](3) NULL,
	[QUADRANT] [nchar](3) NULL,
	[EQUIPMENT_NO] [nchar](3) NULL,
	[TIMESTAMP] [datetime] NULL,
	[VALUE] [float] NULL,
PRIMARY KEY CLUSTERED 
(
	[ID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]

GO
/****** Object:  Table [dbo].[345---------001BMSSTEMET------ALA001]    Script Date: 7/22/2013 8:21:56 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[345---------001BMSSTEMET------ALA001](
	[ID] [int] IDENTITY(1,1) NOT NULL,
	[ZONE] [nchar](3) NULL,
	[FLOOR] [nchar](3) NULL,
	[QUADRANT] [nchar](3) NULL,
	[EQUIPMENT_NO] [nchar](3) NULL,
	[TIMESTAMP] [datetime] NULL,
	[VALUE] [float] NULL,
PRIMARY KEY CLUSTERED 
(
	[ID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]

GO
/****** Object:  Table [dbo].[345---------001BMSSTEMET------ALA002]    Script Date: 7/22/2013 8:21:56 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[345---------001BMSSTEMET------ALA002](
	[ID] [int] IDENTITY(1,1) NOT NULL,
	[ZONE] [nchar](3) NULL,
	[FLOOR] [nchar](3) NULL,
	[QUADRANT] [nchar](3) NULL,
	[EQUIPMENT_NO] [nchar](3) NULL,
	[TIMESTAMP] [datetime] NULL,
	[VALUE] [float] NULL,
PRIMARY KEY CLUSTERED 
(
	[ID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]

GO
/****** Object:  Table [dbo].[345---------001BMSSTEMET------HVA001]    Script Date: 7/22/2013 8:21:56 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[345---------001BMSSTEMET------HVA001](
	[ID] [int] IDENTITY(1,1) NOT NULL,
	[ZONE] [nchar](3) NULL,
	[FLOOR] [nchar](3) NULL,
	[QUADRANT] [nchar](3) NULL,
	[EQUIPMENT_NO] [nchar](3) NULL,
	[TIMESTAMP] [datetime] NULL,
	[VALUE] [float] NULL,
PRIMARY KEY CLUSTERED 
(
	[ID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]

GO
/****** Object:  Table [dbo].[345---------001BMSSTEMET------LVA001]    Script Date: 7/22/2013 8:21:56 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[345---------001BMSSTEMET------LVA001](
	[ID] [int] IDENTITY(1,1) NOT NULL,
	[ZONE] [nchar](3) NULL,
	[FLOOR] [nchar](3) NULL,
	[QUADRANT] [nchar](3) NULL,
	[EQUIPMENT_NO] [nchar](3) NULL,
	[TIMESTAMP] [datetime] NULL,
	[VALUE] [float] NULL,
PRIMARY KEY CLUSTERED 
(
	[ID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]

GO
/****** Object:  Table [dbo].[345---------001BMSSTEMET------MVA001]    Script Date: 7/22/2013 8:21:56 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[345---------001BMSSTEMET------MVA001](
	[ID] [int] IDENTITY(1,1) NOT NULL,
	[ZONE] [nchar](3) NULL,
	[FLOOR] [nchar](3) NULL,
	[QUADRANT] [nchar](3) NULL,
	[EQUIPMENT_NO] [nchar](3) NULL,
	[TIMESTAMP] [datetime] NULL,
	[VALUE] [float] NULL,
PRIMARY KEY CLUSTERED 
(
	[ID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]

GO
/****** Object:  Table [dbo].[345---------001BMSSTEMET------VAL001]    Script Date: 7/22/2013 8:21:56 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[345---------001BMSSTEMET------VAL001](
	[ID] [int] IDENTITY(1,1) NOT NULL,
	[ZONE] [nchar](3) NULL,
	[FLOOR] [nchar](3) NULL,
	[QUADRANT] [nchar](3) NULL,
	[EQUIPMENT_NO] [nchar](3) NULL,
	[TIMESTAMP] [datetime] NULL,
	[VALUE] [float] NULL,
PRIMARY KEY CLUSTERED 
(
	[ID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]

GO
/****** Object:  Table [dbo].[345---------001BMSWATCHIDIF---VAL001]    Script Date: 7/22/2013 8:21:56 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[345---------001BMSWATCHIDIF---VAL001](
	[ID] [int] IDENTITY(1,1) NOT NULL,
	[ZONE] [nchar](3) NULL,
	[FLOOR] [nchar](3) NULL,
	[QUADRANT] [nchar](3) NULL,
	[EQUIPMENT_NO] [nchar](3) NULL,
	[TIMESTAMP] [datetime] NULL,
	[VALUE] [float] NULL,
PRIMARY KEY CLUSTERED 
(
	[ID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]

GO
/****** Object:  Table [dbo].[345---------001BMSWATCHIRET---VAL001]    Script Date: 7/22/2013 8:21:56 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[345---------001BMSWATCHIRET---VAL001](
	[ID] [int] IDENTITY(1,1) NOT NULL,
	[ZONE] [nchar](3) NULL,
	[FLOOR] [nchar](3) NULL,
	[QUADRANT] [nchar](3) NULL,
	[EQUIPMENT_NO] [nchar](3) NULL,
	[TIMESTAMP] [datetime] NULL,
	[VALUE] [float] NULL,
PRIMARY KEY CLUSTERED 
(
	[ID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]

GO
/****** Object:  Table [dbo].[345---------001BMSWATCHISUP---VAL001]    Script Date: 7/22/2013 8:21:56 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[345---------001BMSWATCHISUP---VAL001](
	[ID] [int] IDENTITY(1,1) NOT NULL,
	[ZONE] [nchar](3) NULL,
	[FLOOR] [nchar](3) NULL,
	[QUADRANT] [nchar](3) NULL,
	[EQUIPMENT_NO] [nchar](3) NULL,
	[TIMESTAMP] [datetime] NULL,
	[VALUE] [float] NULL,
PRIMARY KEY CLUSTERED 
(
	[ID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]

GO
/****** Object:  Table [dbo].[345---------001BMSWATHOT------ALA001]    Script Date: 7/22/2013 8:21:56 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[345---------001BMSWATHOT------ALA001](
	[ID] [int] IDENTITY(1,1) NOT NULL,
	[ZONE] [nchar](3) NULL,
	[FLOOR] [nchar](3) NULL,
	[QUADRANT] [nchar](3) NULL,
	[EQUIPMENT_NO] [nchar](3) NULL,
	[TIMESTAMP] [datetime] NULL,
	[VALUE] [float] NULL,
PRIMARY KEY CLUSTERED 
(
	[ID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]

GO
/****** Object:  Table [dbo].[345---------001BMSWATHOT------ALA002]    Script Date: 7/22/2013 8:21:56 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[345---------001BMSWATHOT------ALA002](
	[ID] [int] IDENTITY(1,1) NOT NULL,
	[ZONE] [nchar](3) NULL,
	[FLOOR] [nchar](3) NULL,
	[QUADRANT] [nchar](3) NULL,
	[EQUIPMENT_NO] [nchar](3) NULL,
	[TIMESTAMP] [datetime] NULL,
	[VALUE] [float] NULL,
PRIMARY KEY CLUSTERED 
(
	[ID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]

GO
/****** Object:  Table [dbo].[345---------001BMSWATHOTINT---VAL001]    Script Date: 7/22/2013 8:21:56 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[345---------001BMSWATHOTINT---VAL001](
	[ID] [int] IDENTITY(1,1) NOT NULL,
	[ZONE] [nchar](3) NULL,
	[FLOOR] [nchar](3) NULL,
	[QUADRANT] [nchar](3) NULL,
	[EQUIPMENT_NO] [nchar](3) NULL,
	[TIMESTAMP] [datetime] NULL,
	[VALUE] [float] NULL,
PRIMARY KEY CLUSTERED 
(
	[ID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]

GO
/****** Object:  Table [dbo].[345---------001BMSWATSEC------ALA001]    Script Date: 7/22/2013 8:21:56 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[345---------001BMSWATSEC------ALA001](
	[ID] [int] IDENTITY(1,1) NOT NULL,
	[ZONE] [nchar](3) NULL,
	[FLOOR] [nchar](3) NULL,
	[QUADRANT] [nchar](3) NULL,
	[EQUIPMENT_NO] [nchar](3) NULL,
	[TIMESTAMP] [datetime] NULL,
	[VALUE] [float] NULL,
PRIMARY KEY CLUSTERED 
(
	[ID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]

GO
/****** Object:  Table [dbo].[345---------001BMSWATSEC------ALA002]    Script Date: 7/22/2013 8:21:56 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[345---------001BMSWATSEC------ALA002](
	[ID] [int] IDENTITY(1,1) NOT NULL,
	[ZONE] [nchar](3) NULL,
	[FLOOR] [nchar](3) NULL,
	[QUADRANT] [nchar](3) NULL,
	[EQUIPMENT_NO] [nchar](3) NULL,
	[TIMESTAMP] [datetime] NULL,
	[VALUE] [float] NULL,
PRIMARY KEY CLUSTERED 
(
	[ID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]

GO
/****** Object:  Table [dbo].[345---------001BMSWATSECPUM---ALA001]    Script Date: 7/22/2013 8:21:56 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[345---------001BMSWATSECPUM---ALA001](
	[ID] [int] IDENTITY(1,1) NOT NULL,
	[ZONE] [nchar](3) NULL,
	[FLOOR] [nchar](3) NULL,
	[QUADRANT] [nchar](3) NULL,
	[EQUIPMENT_NO] [nchar](3) NULL,
	[TIMESTAMP] [datetime] NULL,
	[VALUE] [float] NULL,
PRIMARY KEY CLUSTERED 
(
	[ID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]

GO
/****** Object:  Table [dbo].[345---------001BMSWATSECPUM---VAL001]    Script Date: 7/22/2013 8:21:56 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[345---------001BMSWATSECPUM---VAL001](
	[ID] [int] IDENTITY(1,1) NOT NULL,
	[ZONE] [nchar](3) NULL,
	[FLOOR] [nchar](3) NULL,
	[QUADRANT] [nchar](3) NULL,
	[EQUIPMENT_NO] [nchar](3) NULL,
	[TIMESTAMP] [datetime] NULL,
	[VALUE] [float] NULL,
PRIMARY KEY CLUSTERED 
(
	[ID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]

GO
/****** Object:  Table [dbo].[345---------001BMSWATSECRET---VAL001]    Script Date: 7/22/2013 8:21:56 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[345---------001BMSWATSECRET---VAL001](
	[ID] [int] IDENTITY(1,1) NOT NULL,
	[ZONE] [nchar](3) NULL,
	[FLOOR] [nchar](3) NULL,
	[QUADRANT] [nchar](3) NULL,
	[EQUIPMENT_NO] [nchar](3) NULL,
	[TIMESTAMP] [datetime] NULL,
	[VALUE] [float] NULL,
PRIMARY KEY CLUSTERED 
(
	[ID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]

GO
/****** Object:  Table [dbo].[345---------001BMSWATSECSMO---VAL001]    Script Date: 7/22/2013 8:21:56 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[345---------001BMSWATSECSMO---VAL001](
	[ID] [int] IDENTITY(1,1) NOT NULL,
	[ZONE] [nchar](3) NULL,
	[FLOOR] [nchar](3) NULL,
	[QUADRANT] [nchar](3) NULL,
	[EQUIPMENT_NO] [nchar](3) NULL,
	[TIMESTAMP] [datetime] NULL,
	[VALUE] [float] NULL,
PRIMARY KEY CLUSTERED 
(
	[ID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]

GO
/****** Object:  Table [dbo].[345---------001BMSWATSECSUP---VAL001]    Script Date: 7/22/2013 8:21:56 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[345---------001BMSWATSECSUP---VAL001](
	[ID] [int] IDENTITY(1,1) NOT NULL,
	[ZONE] [nchar](3) NULL,
	[FLOOR] [nchar](3) NULL,
	[QUADRANT] [nchar](3) NULL,
	[EQUIPMENT_NO] [nchar](3) NULL,
	[TIMESTAMP] [datetime] NULL,
	[VALUE] [float] NULL,
PRIMARY KEY CLUSTERED 
(
	[ID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]

GO
/****** Object:  Table [dbo].[345---------001BMSWATTNK------ALA001]    Script Date: 7/22/2013 8:21:56 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[345---------001BMSWATTNK------ALA001](
	[ID] [int] IDENTITY(1,1) NOT NULL,
	[ZONE] [nchar](3) NULL,
	[FLOOR] [nchar](3) NULL,
	[QUADRANT] [nchar](3) NULL,
	[EQUIPMENT_NO] [nchar](3) NULL,
	[TIMESTAMP] [datetime] NULL,
	[VALUE] [float] NULL,
PRIMARY KEY CLUSTERED 
(
	[ID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]

GO
/****** Object:  Table [dbo].[345---------001BMSWATTNK------ALA002]    Script Date: 7/22/2013 8:21:56 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[345---------001BMSWATTNK------ALA002](
	[ID] [int] IDENTITY(1,1) NOT NULL,
	[ZONE] [nchar](3) NULL,
	[FLOOR] [nchar](3) NULL,
	[QUADRANT] [nchar](3) NULL,
	[EQUIPMENT_NO] [nchar](3) NULL,
	[TIMESTAMP] [datetime] NULL,
	[VALUE] [float] NULL,
PRIMARY KEY CLUSTERED 
(
	[ID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]

GO
/****** Object:  Table [dbo].[345---------001EMSBMMMET------40001001]    Script Date: 7/22/2013 8:21:56 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[345---------001EMSBMMMET------40001001](
	[ID] [int] IDENTITY(1,1) NOT NULL,
	[ZONE] [nchar](3) NULL,
	[FLOOR] [nchar](3) NULL,
	[QUADRANT] [nchar](3) NULL,
	[EQUIPMENT_NO] [nchar](3) NULL,
	[TIMESTAMP] [datetime] NULL,
	[VALUE] [float] NULL,
PRIMARY KEY CLUSTERED 
(
	[ID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]

GO
/****** Object:  Table [dbo].[345---------001EMSBMMMET------40003001]    Script Date: 7/22/2013 8:21:56 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[345---------001EMSBMMMET------40003001](
	[ID] [int] IDENTITY(1,1) NOT NULL,
	[ZONE] [nchar](3) NULL,
	[FLOOR] [nchar](3) NULL,
	[QUADRANT] [nchar](3) NULL,
	[EQUIPMENT_NO] [nchar](3) NULL,
	[TIMESTAMP] [datetime] NULL,
	[VALUE] [float] NULL,
PRIMARY KEY CLUSTERED 
(
	[ID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]

GO
/****** Object:  Table [dbo].[345---------001EMSBMMMET------40005001]    Script Date: 7/22/2013 8:21:56 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[345---------001EMSBMMMET------40005001](
	[ID] [int] IDENTITY(1,1) NOT NULL,
	[ZONE] [nchar](3) NULL,
	[FLOOR] [nchar](3) NULL,
	[QUADRANT] [nchar](3) NULL,
	[EQUIPMENT_NO] [nchar](3) NULL,
	[TIMESTAMP] [datetime] NULL,
	[VALUE] [float] NULL,
PRIMARY KEY CLUSTERED 
(
	[ID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]

GO
/****** Object:  Table [dbo].[345---------001EMSBMMMET------40007001]    Script Date: 7/22/2013 8:21:56 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[345---------001EMSBMMMET------40007001](
	[ID] [int] IDENTITY(1,1) NOT NULL,
	[ZONE] [nchar](3) NULL,
	[FLOOR] [nchar](3) NULL,
	[QUADRANT] [nchar](3) NULL,
	[EQUIPMENT_NO] [nchar](3) NULL,
	[TIMESTAMP] [datetime] NULL,
	[VALUE] [float] NULL,
PRIMARY KEY CLUSTERED 
(
	[ID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]

GO
/****** Object:  Table [dbo].[345---------001EMSBMMMET------40009001]    Script Date: 7/22/2013 8:21:56 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[345---------001EMSBMMMET------40009001](
	[ID] [int] IDENTITY(1,1) NOT NULL,
	[ZONE] [nchar](3) NULL,
	[FLOOR] [nchar](3) NULL,
	[QUADRANT] [nchar](3) NULL,
	[EQUIPMENT_NO] [nchar](3) NULL,
	[TIMESTAMP] [datetime] NULL,
	[VALUE] [float] NULL,
PRIMARY KEY CLUSTERED 
(
	[ID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]

GO
/****** Object:  Table [dbo].[345---------001EMSBMMMET------40011001]    Script Date: 7/22/2013 8:21:56 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[345---------001EMSBMMMET------40011001](
	[ID] [int] IDENTITY(1,1) NOT NULL,
	[ZONE] [nchar](3) NULL,
	[FLOOR] [nchar](3) NULL,
	[QUADRANT] [nchar](3) NULL,
	[EQUIPMENT_NO] [nchar](3) NULL,
	[TIMESTAMP] [datetime] NULL,
	[VALUE] [float] NULL,
PRIMARY KEY CLUSTERED 
(
	[ID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]

GO
/****** Object:  Table [dbo].[345---------001EMSBMMMET------40013001]    Script Date: 7/22/2013 8:21:56 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[345---------001EMSBMMMET------40013001](
	[ID] [int] IDENTITY(1,1) NOT NULL,
	[ZONE] [nchar](3) NULL,
	[FLOOR] [nchar](3) NULL,
	[QUADRANT] [nchar](3) NULL,
	[EQUIPMENT_NO] [nchar](3) NULL,
	[TIMESTAMP] [datetime] NULL,
	[VALUE] [float] NULL,
PRIMARY KEY CLUSTERED 
(
	[ID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]

GO
/****** Object:  Table [dbo].[345---------001EMSBMMMET------40015001]    Script Date: 7/22/2013 8:21:56 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[345---------001EMSBMMMET------40015001](
	[ID] [int] IDENTITY(1,1) NOT NULL,
	[ZONE] [nchar](3) NULL,
	[FLOOR] [nchar](3) NULL,
	[QUADRANT] [nchar](3) NULL,
	[EQUIPMENT_NO] [nchar](3) NULL,
	[TIMESTAMP] [datetime] NULL,
	[VALUE] [float] NULL,
PRIMARY KEY CLUSTERED 
(
	[ID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]

GO
/****** Object:  Table [dbo].[345---------001EMSBMMMET------40017001]    Script Date: 7/22/2013 8:21:56 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[345---------001EMSBMMMET------40017001](
	[ID] [int] IDENTITY(1,1) NOT NULL,
	[ZONE] [nchar](3) NULL,
	[FLOOR] [nchar](3) NULL,
	[QUADRANT] [nchar](3) NULL,
	[EQUIPMENT_NO] [nchar](3) NULL,
	[TIMESTAMP] [datetime] NULL,
	[VALUE] [float] NULL,
PRIMARY KEY CLUSTERED 
(
	[ID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]

GO
/****** Object:  Table [dbo].[345---------001EMSBMMMET------40019001]    Script Date: 7/22/2013 8:21:56 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[345---------001EMSBMMMET------40019001](
	[ID] [int] IDENTITY(1,1) NOT NULL,
	[ZONE] [nchar](3) NULL,
	[FLOOR] [nchar](3) NULL,
	[QUADRANT] [nchar](3) NULL,
	[EQUIPMENT_NO] [nchar](3) NULL,
	[TIMESTAMP] [datetime] NULL,
	[VALUE] [float] NULL,
PRIMARY KEY CLUSTERED 
(
	[ID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]

GO
/****** Object:  Table [dbo].[345---------001EMSBMMMET------40021001]    Script Date: 7/22/2013 8:21:56 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[345---------001EMSBMMMET------40021001](
	[ID] [int] IDENTITY(1,1) NOT NULL,
	[ZONE] [nchar](3) NULL,
	[FLOOR] [nchar](3) NULL,
	[QUADRANT] [nchar](3) NULL,
	[EQUIPMENT_NO] [nchar](3) NULL,
	[TIMESTAMP] [datetime] NULL,
	[VALUE] [float] NULL,
PRIMARY KEY CLUSTERED 
(
	[ID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]

GO
/****** Object:  Table [dbo].[345---------001EMSBMMMET------40023001]    Script Date: 7/22/2013 8:21:56 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[345---------001EMSBMMMET------40023001](
	[ID] [int] IDENTITY(1,1) NOT NULL,
	[ZONE] [nchar](3) NULL,
	[FLOOR] [nchar](3) NULL,
	[QUADRANT] [nchar](3) NULL,
	[EQUIPMENT_NO] [nchar](3) NULL,
	[TIMESTAMP] [datetime] NULL,
	[VALUE] [float] NULL,
PRIMARY KEY CLUSTERED 
(
	[ID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]

GO
/****** Object:  Table [dbo].[345---------001EMSBMMMET------40025001]    Script Date: 7/22/2013 8:21:56 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[345---------001EMSBMMMET------40025001](
	[ID] [int] IDENTITY(1,1) NOT NULL,
	[ZONE] [nchar](3) NULL,
	[FLOOR] [nchar](3) NULL,
	[QUADRANT] [nchar](3) NULL,
	[EQUIPMENT_NO] [nchar](3) NULL,
	[TIMESTAMP] [datetime] NULL,
	[VALUE] [float] NULL,
PRIMARY KEY CLUSTERED 
(
	[ID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]

GO
/****** Object:  Table [dbo].[345---------001EMSBMMMET------40027001]    Script Date: 7/22/2013 8:21:56 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[345---------001EMSBMMMET------40027001](
	[ID] [int] IDENTITY(1,1) NOT NULL,
	[ZONE] [nchar](3) NULL,
	[FLOOR] [nchar](3) NULL,
	[QUADRANT] [nchar](3) NULL,
	[EQUIPMENT_NO] [nchar](3) NULL,
	[TIMESTAMP] [datetime] NULL,
	[VALUE] [float] NULL,
PRIMARY KEY CLUSTERED 
(
	[ID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]

GO
/****** Object:  Table [dbo].[345---------001EMSBMMMET------40029001]    Script Date: 7/22/2013 8:21:56 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[345---------001EMSBMMMET------40029001](
	[ID] [int] IDENTITY(1,1) NOT NULL,
	[ZONE] [nchar](3) NULL,
	[FLOOR] [nchar](3) NULL,
	[QUADRANT] [nchar](3) NULL,
	[EQUIPMENT_NO] [nchar](3) NULL,
	[TIMESTAMP] [datetime] NULL,
	[VALUE] [float] NULL,
PRIMARY KEY CLUSTERED 
(
	[ID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]

GO
/****** Object:  Table [dbo].[345---------001EMSSMAMET------40120001]    Script Date: 7/22/2013 8:21:56 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[345---------001EMSSMAMET------40120001](
	[ID] [int] IDENTITY(1,1) NOT NULL,
	[ZONE] [nchar](3) NULL,
	[FLOOR] [nchar](3) NULL,
	[QUADRANT] [nchar](3) NULL,
	[EQUIPMENT_NO] [nchar](3) NULL,
	[TIMESTAMP] [datetime] NULL,
	[VALUE] [float] NULL,
PRIMARY KEY CLUSTERED 
(
	[ID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]

GO
/****** Object:  Table [dbo].[345---------001EMSSMAMET------40120002]    Script Date: 7/22/2013 8:21:56 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[345---------001EMSSMAMET------40120002](
	[ID] [int] IDENTITY(1,1) NOT NULL,
	[ZONE] [nchar](3) NULL,
	[FLOOR] [nchar](3) NULL,
	[QUADRANT] [nchar](3) NULL,
	[EQUIPMENT_NO] [nchar](3) NULL,
	[TIMESTAMP] [datetime] NULL,
	[VALUE] [float] NULL,
PRIMARY KEY CLUSTERED 
(
	[ID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]

GO
/****** Object:  Table [dbo].[345---------001EMSSMAMET------40120003]    Script Date: 7/22/2013 8:21:56 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[345---------001EMSSMAMET------40120003](
	[ID] [int] IDENTITY(1,1) NOT NULL,
	[ZONE] [nchar](3) NULL,
	[FLOOR] [nchar](3) NULL,
	[QUADRANT] [nchar](3) NULL,
	[EQUIPMENT_NO] [nchar](3) NULL,
	[TIMESTAMP] [datetime] NULL,
	[VALUE] [float] NULL,
PRIMARY KEY CLUSTERED 
(
	[ID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]

GO
/****** Object:  Table [dbo].[345---------001EMSSMAMET------40120004]    Script Date: 7/22/2013 8:21:56 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[345---------001EMSSMAMET------40120004](
	[ID] [int] IDENTITY(1,1) NOT NULL,
	[ZONE] [nchar](3) NULL,
	[FLOOR] [nchar](3) NULL,
	[QUADRANT] [nchar](3) NULL,
	[EQUIPMENT_NO] [nchar](3) NULL,
	[TIMESTAMP] [datetime] NULL,
	[VALUE] [float] NULL,
PRIMARY KEY CLUSTERED 
(
	[ID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]

GO
/****** Object:  Table [dbo].[345---------001EMSSMAMET------40132001]    Script Date: 7/22/2013 8:21:56 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[345---------001EMSSMAMET------40132001](
	[ID] [int] IDENTITY(1,1) NOT NULL,
	[ZONE] [nchar](3) NULL,
	[FLOOR] [nchar](3) NULL,
	[QUADRANT] [nchar](3) NULL,
	[EQUIPMENT_NO] [nchar](3) NULL,
	[TIMESTAMP] [datetime] NULL,
	[VALUE] [float] NULL,
PRIMARY KEY CLUSTERED 
(
	[ID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]

GO
/****** Object:  Table [dbo].[345---------001EMSSMAMET------40132002]    Script Date: 7/22/2013 8:21:56 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[345---------001EMSSMAMET------40132002](
	[ID] [int] IDENTITY(1,1) NOT NULL,
	[ZONE] [nchar](3) NULL,
	[FLOOR] [nchar](3) NULL,
	[QUADRANT] [nchar](3) NULL,
	[EQUIPMENT_NO] [nchar](3) NULL,
	[TIMESTAMP] [datetime] NULL,
	[VALUE] [float] NULL,
PRIMARY KEY CLUSTERED 
(
	[ID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]

GO
/****** Object:  Table [dbo].[345---------001EMSSMAMET------40132003]    Script Date: 7/22/2013 8:21:56 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[345---------001EMSSMAMET------40132003](
	[ID] [int] IDENTITY(1,1) NOT NULL,
	[ZONE] [nchar](3) NULL,
	[FLOOR] [nchar](3) NULL,
	[QUADRANT] [nchar](3) NULL,
	[EQUIPMENT_NO] [nchar](3) NULL,
	[TIMESTAMP] [datetime] NULL,
	[VALUE] [float] NULL,
PRIMARY KEY CLUSTERED 
(
	[ID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]

GO
/****** Object:  Table [dbo].[345---------001EMSSMAMET------40132004]    Script Date: 7/22/2013 8:21:56 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[345---------001EMSSMAMET------40132004](
	[ID] [int] IDENTITY(1,1) NOT NULL,
	[ZONE] [nchar](3) NULL,
	[FLOOR] [nchar](3) NULL,
	[QUADRANT] [nchar](3) NULL,
	[EQUIPMENT_NO] [nchar](3) NULL,
	[TIMESTAMP] [datetime] NULL,
	[VALUE] [float] NULL,
PRIMARY KEY CLUSTERED 
(
	[ID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]

GO
/****** Object:  Table [dbo].[345---------001EMSSMAMET------40138001]    Script Date: 7/22/2013 8:21:56 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[345---------001EMSSMAMET------40138001](
	[ID] [int] IDENTITY(1,1) NOT NULL,
	[ZONE] [nchar](3) NULL,
	[FLOOR] [nchar](3) NULL,
	[QUADRANT] [nchar](3) NULL,
	[EQUIPMENT_NO] [nchar](3) NULL,
	[TIMESTAMP] [datetime] NULL,
	[VALUE] [float] NULL,
PRIMARY KEY CLUSTERED 
(
	[ID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]

GO
/****** Object:  Table [dbo].[345---------001EMSSMAMET------40138002]    Script Date: 7/22/2013 8:21:56 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[345---------001EMSSMAMET------40138002](
	[ID] [int] IDENTITY(1,1) NOT NULL,
	[ZONE] [nchar](3) NULL,
	[FLOOR] [nchar](3) NULL,
	[QUADRANT] [nchar](3) NULL,
	[EQUIPMENT_NO] [nchar](3) NULL,
	[TIMESTAMP] [datetime] NULL,
	[VALUE] [float] NULL,
PRIMARY KEY CLUSTERED 
(
	[ID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]

GO
/****** Object:  Table [dbo].[345---------001EMSSMAMET------40138003]    Script Date: 7/22/2013 8:21:56 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[345---------001EMSSMAMET------40138003](
	[ID] [int] IDENTITY(1,1) NOT NULL,
	[ZONE] [nchar](3) NULL,
	[FLOOR] [nchar](3) NULL,
	[QUADRANT] [nchar](3) NULL,
	[EQUIPMENT_NO] [nchar](3) NULL,
	[TIMESTAMP] [datetime] NULL,
	[VALUE] [float] NULL,
PRIMARY KEY CLUSTERED 
(
	[ID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]

GO
/****** Object:  Table [dbo].[345---------001EMSSMAMET------40138004]    Script Date: 7/22/2013 8:21:56 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[345---------001EMSSMAMET------40138004](
	[ID] [int] IDENTITY(1,1) NOT NULL,
	[ZONE] [nchar](3) NULL,
	[FLOOR] [nchar](3) NULL,
	[QUADRANT] [nchar](3) NULL,
	[EQUIPMENT_NO] [nchar](3) NULL,
	[TIMESTAMP] [datetime] NULL,
	[VALUE] [float] NULL,
PRIMARY KEY CLUSTERED 
(
	[ID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]

GO
/****** Object:  Table [dbo].[345---------001EMSSMAMET------40140001]    Script Date: 7/22/2013 8:21:56 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[345---------001EMSSMAMET------40140001](
	[ID] [int] IDENTITY(1,1) NOT NULL,
	[ZONE] [nchar](3) NULL,
	[FLOOR] [nchar](3) NULL,
	[QUADRANT] [nchar](3) NULL,
	[EQUIPMENT_NO] [nchar](3) NULL,
	[TIMESTAMP] [datetime] NULL,
	[VALUE] [float] NULL,
PRIMARY KEY CLUSTERED 
(
	[ID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]

GO
/****** Object:  Table [dbo].[345---------001EMSSMAMET------40140002]    Script Date: 7/22/2013 8:21:56 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[345---------001EMSSMAMET------40140002](
	[ID] [int] IDENTITY(1,1) NOT NULL,
	[ZONE] [nchar](3) NULL,
	[FLOOR] [nchar](3) NULL,
	[QUADRANT] [nchar](3) NULL,
	[EQUIPMENT_NO] [nchar](3) NULL,
	[TIMESTAMP] [datetime] NULL,
	[VALUE] [float] NULL,
PRIMARY KEY CLUSTERED 
(
	[ID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]

GO
/****** Object:  Table [dbo].[345---------001EMSSMAMET------40140003]    Script Date: 7/22/2013 8:21:56 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[345---------001EMSSMAMET------40140003](
	[ID] [int] IDENTITY(1,1) NOT NULL,
	[ZONE] [nchar](3) NULL,
	[FLOOR] [nchar](3) NULL,
	[QUADRANT] [nchar](3) NULL,
	[EQUIPMENT_NO] [nchar](3) NULL,
	[TIMESTAMP] [datetime] NULL,
	[VALUE] [float] NULL,
PRIMARY KEY CLUSTERED 
(
	[ID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]

GO
/****** Object:  Table [dbo].[345---------001EMSSMAMET------40140004]    Script Date: 7/22/2013 8:21:56 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[345---------001EMSSMAMET------40140004](
	[ID] [int] IDENTITY(1,1) NOT NULL,
	[ZONE] [nchar](3) NULL,
	[FLOOR] [nchar](3) NULL,
	[QUADRANT] [nchar](3) NULL,
	[EQUIPMENT_NO] [nchar](3) NULL,
	[TIMESTAMP] [datetime] NULL,
	[VALUE] [float] NULL,
PRIMARY KEY CLUSTERED 
(
	[ID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]

GO
/****** Object:  Table [dbo].[Floor_Mapping]    Script Date: 7/22/2013 8:21:56 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[Floor_Mapping](
	[Floor] [int] NOT NULL,
	[CompFloor] [nchar](3) NULL,
 CONSTRAINT [PK_Floor_Mapping] PRIMARY KEY CLUSTERED 
(
	[Floor] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]

GO
/****** Object:  Table [dbo].[Quadrant_Mapping]    Script Date: 7/22/2013 8:21:56 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[Quadrant_Mapping](
	[Quadrant] [nchar](2) NOT NULL,
	[CompQuadrant] [nchar](3) NULL,
 CONSTRAINT [PK_Quadrant_Mapping] PRIMARY KEY CLUSTERED 
(
	[Quadrant] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]

GO
/****** Object:  Table [dbo].[Ramp_Down_Time_DS]    Script Date: 7/22/2013 8:21:56 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[Ramp_Down_Time_DS](
	[ID] [int] NULL,
	[TIMESTAMP] [datetime] NULL,
	[VALUE] [int] NULL
) ON [PRIMARY]

GO
/****** Object:  Table [dbo].[SYNCH_TEST]    Script Date: 7/22/2013 8:21:56 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[SYNCH_TEST](
	[ID] [int] IDENTITY(1,1) NOT NULL,
	[ZONE] [nchar](3) NOT NULL,
	[FLOOR] [nchar](3) NOT NULL,
	[QUADRANT] [nchar](3) NOT NULL,
	[EQUIPMENT_NO] [nchar](3) NOT NULL,
	[TIMESTAMP] [datetime] NOT NULL,
	[VALUE] [float] NOT NULL,
 CONSTRAINT [PK_SYNCH_TEST] PRIMARY KEY CLUSTERED 
(
	[ID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]

GO
/****** Object:  View [dbo].[Space_Temp_Comp]    Script Date: 7/22/2013 8:21:56 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE VIEW [dbo].[Space_Temp_Comp]
AS
SELECT     a.Run_DateTime, a.Prediction_DateTime, a.CompFloor AS Floor, q.CompQuadrant AS Quadrant, a.Prediction_Value, a.Lower_Bound_95, a.Upper_Bound_95, 
                      a.Lower_Bound_68, a.Upper_Bound_68, a.ID
FROM         (SELECT     s.Run_DateTime, s.Prediction_DateTime, f.CompFloor, s.Quadrant, s.Prediction_Value, s.Lower_Bound_95, s.Upper_Bound_95, s.Lower_Bound_68, 
                                              s.Upper_Bound_68, s.ID
                       FROM          dbo.[345---------000TPOFORTEMSPA001---001] AS s INNER JOIN
                                              dbo.Floor_Mapping AS f ON s.Floor = f.Floor) AS a INNER JOIN
                      dbo.Quadrant_Mapping AS q ON a.Quadrant = q.Quadrant

GO
/****** Object:  View [dbo].[Space_Temp_Comp2]    Script Date: 7/22/2013 8:21:56 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE VIEW [dbo].[Space_Temp_Comp2]
AS
SELECT     a.Run_DateTime, a.Prediction_DateTime, a.CompFloor AS Floor, q.CompQuadrant AS Quadrant, a.Prediction_Value, a.Lower_Bound_95, a.Upper_Bound_95, 
                      a.Lower_Bound_68, a.Upper_Bound_68, a.ID
FROM         (SELECT     s.Run_DateTime, s.Prediction_DateTime, f.CompFloor, s.Quadrant, s.Prediction_Value, s.Lower_Bound_95, s.Upper_Bound_95, s.Lower_Bound_68, 
                                              s.Upper_Bound_68, s.ID
                       FROM          dbo.[345---------000TPOFORTEMSPA001---001_orig] AS s INNER JOIN
                                              dbo.Floor_Mapping AS f ON s.Floor = f.Floor) AS a INNER JOIN
                      dbo.Quadrant_Mapping AS q ON a.Quadrant = q.Quadrant

GO
/****** Object:  View [dbo].[Space_Temp_Prediction]    Script Date: 7/22/2013 8:21:56 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO

CREATE VIEW [dbo].[Space_Temp_Prediction]
AS
SELECT     dbo.[345---------000TPOFORTEMSPA001---001].*, dbo.[345_floor_zone_map].ZONE
FROM         dbo.[345_floor_zone_map] INNER JOIN
                      dbo.[345---------000TPOFORTEMSPA001---001] ON dbo.[345_floor_zone_map].FLOOR = dbo.[345---------000TPOFORTEMSPA001---001].Floor

--SELECT     Run_DateTime, Prediction_DateTime, Floor, Quadrant, Prediction_Value, Lower_Bound_95, Upper_Bound_95, Lower_Bound_68, Upper_Bound_68, ID
--FROM         dbo.[345---------000TPOFORTEMSPA001---001] AS a
--WHERE     (Floor = 'F02') OR
--                      (Floor = 'F04') OR
--                      (Floor = 'F05') OR
--                      (Floor = 'F13') OR
--                      (Floor = 'F18') OR
--                      (Floor = 'F20') OR
--                      (Floor = 'F24') OR
--                      (Floor = 'F32') OR
--                      (Floor = 'F38') OR
--                      (Floor = 'F40')


GO
/****** Object:  View [dbo].[TestView]    Script Date: 7/22/2013 8:21:56 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE VIEW [dbo].[TestView]
AS
SELECT     s.Run_DateTime, s.Prediction_DateTime, f.CompFloor, s.Quadrant, s.Prediction_Value, s.Lower_Bound_95, s.Upper_Bound_95, s.Lower_Bound_68, 
                      s.Upper_Bound_68, s.ID
FROM         dbo.[345---------000TPOFORTEMSPA001---001] AS s INNER JOIN
                      dbo.Floor_Mapping AS f ON s.Floor = f.Floor

GO
/****** Object:  View [dbo].[TestView2]    Script Date: 7/22/2013 8:21:56 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE VIEW [dbo].[TestView2]
AS
SELECT     a.Run_DateTime, a.Prediction_DateTime, a.CompFloor, q.CompQuadrant, a.Prediction_Value, a.Lower_Bound_95, a.Upper_Bound_95, a.Lower_Bound_68, 
                      a.Upper_Bound_68, a.ID
FROM         (SELECT     s.Run_DateTime, s.Prediction_DateTime, f.CompFloor, s.Quadrant, s.Prediction_Value, s.Lower_Bound_95, s.Upper_Bound_95, s.Lower_Bound_68, 
                                              s.Upper_Bound_68, s.ID
                       FROM          dbo.[345---------000TPOFORTEMSPA001---001] AS s INNER JOIN
                                              dbo.Floor_Mapping AS f ON s.Floor = f.Floor) AS a INNER JOIN
                      dbo.Quadrant_Mapping AS q ON a.Quadrant = q.Quadrant

GO
/****** Object:  View [dbo].[View_1]    Script Date: 7/22/2013 8:21:56 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE VIEW [dbo].[View_1]
AS
SELECT     Run_DateTime, Prediction_DateTime, CompFloor, Quadrant, Prediction_Value, Lower_Bound_95, Upper_Bound_95, Lower_Bound_68, Upper_Bound_68, ID
FROM         (SELECT     s.Run_DateTime, s.Prediction_DateTime, f.CompFloor, s.Quadrant, s.Prediction_Value, s.Lower_Bound_95, s.Upper_Bound_95, s.Lower_Bound_68, 
                                              s.Upper_Bound_68, s.ID
                       FROM          dbo.[345---------000TPOFORTEMSPA001---001] AS s INNER JOIN
                                              dbo.Floor_Mapping AS f ON s.Floor = f.Floor) AS a

GO
EXEC sys.sp_addextendedproperty @name=N'MS_DiagramPane1', @value=N'[0E232FF0-B466-11cf-A24F-00AA00A3EFFF, 1.00]
Begin DesignProperties = 
   Begin PaneConfigurations = 
      Begin PaneConfiguration = 0
         NumPanes = 4
         Configuration = "(H (1[40] 4[20] 2[20] 3) )"
      End
      Begin PaneConfiguration = 1
         NumPanes = 3
         Configuration = "(H (1 [50] 4 [25] 3))"
      End
      Begin PaneConfiguration = 2
         NumPanes = 3
         Configuration = "(H (1 [50] 2 [25] 3))"
      End
      Begin PaneConfiguration = 3
         NumPanes = 3
         Configuration = "(H (4 [30] 2 [40] 3))"
      End
      Begin PaneConfiguration = 4
         NumPanes = 2
         Configuration = "(H (1 [56] 3))"
      End
      Begin PaneConfiguration = 5
         NumPanes = 2
         Configuration = "(H (2 [66] 3))"
      End
      Begin PaneConfiguration = 6
         NumPanes = 2
         Configuration = "(H (4 [50] 3))"
      End
      Begin PaneConfiguration = 7
         NumPanes = 1
         Configuration = "(V (3))"
      End
      Begin PaneConfiguration = 8
         NumPanes = 3
         Configuration = "(H (1[56] 4[18] 2) )"
      End
      Begin PaneConfiguration = 9
         NumPanes = 2
         Configuration = "(H (1 [75] 4))"
      End
      Begin PaneConfiguration = 10
         NumPanes = 2
         Configuration = "(H (1[66] 2) )"
      End
      Begin PaneConfiguration = 11
         NumPanes = 2
         Configuration = "(H (4 [60] 2))"
      End
      Begin PaneConfiguration = 12
         NumPanes = 1
         Configuration = "(H (1) )"
      End
      Begin PaneConfiguration = 13
         NumPanes = 1
         Configuration = "(V (4))"
      End
      Begin PaneConfiguration = 14
         NumPanes = 1
         Configuration = "(V (2))"
      End
      ActivePaneConfig = 0
   End
   Begin DiagramPane = 
      Begin Origin = 
         Top = 0
         Left = 0
      End
      Begin Tables = 
         Begin Table = "a"
            Begin Extent = 
               Top = 6
               Left = 38
               Bottom = 114
               Right = 216
            End
            DisplayFlags = 280
            TopColumn = 0
         End
         Begin Table = "q"
            Begin Extent = 
               Top = 6
               Left = 254
               Bottom = 84
               Right = 407
            End
            DisplayFlags = 280
            TopColumn = 0
         End
      End
   End
   Begin SQLPane = 
   End
   Begin DataPane = 
      Begin ParameterDefaults = ""
      End
   End
   Begin CriteriaPane = 
      Begin ColumnWidths = 11
         Column = 1440
         Alias = 900
         Table = 1170
         Output = 720
         Append = 1400
         NewValue = 1170
         SortType = 1350
         SortOrder = 1410
         GroupBy = 1350
         Filter = 1350
         Or = 1350
         Or = 1350
         Or = 1350
      End
   End
End
' , @level0type=N'SCHEMA',@level0name=N'dbo', @level1type=N'VIEW',@level1name=N'Space_Temp_Comp'
GO
EXEC sys.sp_addextendedproperty @name=N'MS_DiagramPaneCount', @value=1 , @level0type=N'SCHEMA',@level0name=N'dbo', @level1type=N'VIEW',@level1name=N'Space_Temp_Comp'
GO
EXEC sys.sp_addextendedproperty @name=N'MS_DiagramPane1', @value=N'[0E232FF0-B466-11cf-A24F-00AA00A3EFFF, 1.00]
Begin DesignProperties = 
   Begin PaneConfigurations = 
      Begin PaneConfiguration = 0
         NumPanes = 4
         Configuration = "(H (1[40] 4[20] 2[20] 3) )"
      End
      Begin PaneConfiguration = 1
         NumPanes = 3
         Configuration = "(H (1 [50] 4 [25] 3))"
      End
      Begin PaneConfiguration = 2
         NumPanes = 3
         Configuration = "(H (1 [50] 2 [25] 3))"
      End
      Begin PaneConfiguration = 3
         NumPanes = 3
         Configuration = "(H (4 [30] 2 [40] 3))"
      End
      Begin PaneConfiguration = 4
         NumPanes = 2
         Configuration = "(H (1 [56] 3))"
      End
      Begin PaneConfiguration = 5
         NumPanes = 2
         Configuration = "(H (2 [66] 3))"
      End
      Begin PaneConfiguration = 6
         NumPanes = 2
         Configuration = "(H (4 [50] 3))"
      End
      Begin PaneConfiguration = 7
         NumPanes = 1
         Configuration = "(V (3))"
      End
      Begin PaneConfiguration = 8
         NumPanes = 3
         Configuration = "(H (1[56] 4[18] 2) )"
      End
      Begin PaneConfiguration = 9
         NumPanes = 2
         Configuration = "(H (1 [75] 4))"
      End
      Begin PaneConfiguration = 10
         NumPanes = 2
         Configuration = "(H (1[66] 2) )"
      End
      Begin PaneConfiguration = 11
         NumPanes = 2
         Configuration = "(H (4 [60] 2))"
      End
      Begin PaneConfiguration = 12
         NumPanes = 1
         Configuration = "(H (1) )"
      End
      Begin PaneConfiguration = 13
         NumPanes = 1
         Configuration = "(V (4))"
      End
      Begin PaneConfiguration = 14
         NumPanes = 1
         Configuration = "(V (2))"
      End
      ActivePaneConfig = 0
   End
   Begin DiagramPane = 
      Begin Origin = 
         Top = 0
         Left = 0
      End
      Begin Tables = 
         Begin Table = "a"
            Begin Extent = 
               Top = 6
               Left = 38
               Bottom = 114
               Right = 216
            End
            DisplayFlags = 280
            TopColumn = 0
         End
         Begin Table = "q"
            Begin Extent = 
               Top = 6
               Left = 254
               Bottom = 84
               Right = 407
            End
            DisplayFlags = 280
            TopColumn = 0
         End
      End
   End
   Begin SQLPane = 
   End
   Begin DataPane = 
      Begin ParameterDefaults = ""
      End
      Begin ColumnWidths = 9
         Width = 284
         Width = 1500
         Width = 1500
         Width = 1500
         Width = 1500
         Width = 1500
         Width = 1500
         Width = 1500
         Width = 1500
      End
   End
   Begin CriteriaPane = 
      Begin ColumnWidths = 11
         Column = 1440
         Alias = 900
         Table = 1170
         Output = 720
         Append = 1400
         NewValue = 1170
         SortType = 1350
         SortOrder = 1410
         GroupBy = 1350
         Filter = 1350
         Or = 1350
         Or = 1350
         Or = 1350
      End
   End
End
' , @level0type=N'SCHEMA',@level0name=N'dbo', @level1type=N'VIEW',@level1name=N'Space_Temp_Comp2'
GO
EXEC sys.sp_addextendedproperty @name=N'MS_DiagramPaneCount', @value=1 , @level0type=N'SCHEMA',@level0name=N'dbo', @level1type=N'VIEW',@level1name=N'Space_Temp_Comp2'
GO
EXEC sys.sp_addextendedproperty @name=N'MS_DiagramPane1', @value=N'[0E232FF0-B466-11cf-A24F-00AA00A3EFFF, 1.00]
Begin DesignProperties = 
   Begin PaneConfigurations = 
      Begin PaneConfiguration = 0
         NumPanes = 4
         Configuration = "(H (1[40] 4[20] 2[20] 3) )"
      End
      Begin PaneConfiguration = 1
         NumPanes = 3
         Configuration = "(H (1 [50] 4 [25] 3))"
      End
      Begin PaneConfiguration = 2
         NumPanes = 3
         Configuration = "(H (1 [50] 2 [25] 3))"
      End
      Begin PaneConfiguration = 3
         NumPanes = 3
         Configuration = "(H (4 [30] 2 [40] 3))"
      End
      Begin PaneConfiguration = 4
         NumPanes = 2
         Configuration = "(H (1 [56] 3))"
      End
      Begin PaneConfiguration = 5
         NumPanes = 2
         Configuration = "(H (2 [66] 3))"
      End
      Begin PaneConfiguration = 6
         NumPanes = 2
         Configuration = "(H (4 [50] 3))"
      End
      Begin PaneConfiguration = 7
         NumPanes = 1
         Configuration = "(V (3))"
      End
      Begin PaneConfiguration = 8
         NumPanes = 3
         Configuration = "(H (1[56] 4[18] 2) )"
      End
      Begin PaneConfiguration = 9
         NumPanes = 2
         Configuration = "(H (1 [75] 4))"
      End
      Begin PaneConfiguration = 10
         NumPanes = 2
         Configuration = "(H (1[66] 2) )"
      End
      Begin PaneConfiguration = 11
         NumPanes = 2
         Configuration = "(H (4 [60] 2))"
      End
      Begin PaneConfiguration = 12
         NumPanes = 1
         Configuration = "(H (1) )"
      End
      Begin PaneConfiguration = 13
         NumPanes = 1
         Configuration = "(V (4))"
      End
      Begin PaneConfiguration = 14
         NumPanes = 1
         Configuration = "(V (2))"
      End
      ActivePaneConfig = 0
   End
   Begin DiagramPane = 
      Begin Origin = 
         Top = 0
         Left = 0
      End
      Begin Tables = 
         Begin Table = "a"
            Begin Extent = 
               Top = 6
               Left = 38
               Bottom = 114
               Right = 216
            End
            DisplayFlags = 280
            TopColumn = 0
         End
      End
   End
   Begin SQLPane = 
   End
   Begin DataPane = 
      Begin ParameterDefaults = ""
      End
   End
   Begin CriteriaPane = 
      Begin ColumnWidths = 18
         Column = 1440
         Alias = 900
         Table = 1170
         Output = 720
         Append = 1400
         NewValue = 1170
         SortType = 1350
         SortOrder = 1410
         GroupBy = 1350
         Filter = 1350
         Or = 1350
         Or = 1350
         Or = 1350
         Or = 1350
         Or = 1350
         Or = 1350
         Or = 1350
         Or = 1350
         Or = 1350
         Or = 1350
      End
   End
End
' , @level0type=N'SCHEMA',@level0name=N'dbo', @level1type=N'VIEW',@level1name=N'Space_Temp_Prediction'
GO
EXEC sys.sp_addextendedproperty @name=N'MS_DiagramPaneCount', @value=1 , @level0type=N'SCHEMA',@level0name=N'dbo', @level1type=N'VIEW',@level1name=N'Space_Temp_Prediction'
GO
EXEC sys.sp_addextendedproperty @name=N'MS_DiagramPane1', @value=N'[0E232FF0-B466-11cf-A24F-00AA00A3EFFF, 1.00]
Begin DesignProperties = 
   Begin PaneConfigurations = 
      Begin PaneConfiguration = 0
         NumPanes = 4
         Configuration = "(H (1[40] 4[20] 2[20] 3) )"
      End
      Begin PaneConfiguration = 1
         NumPanes = 3
         Configuration = "(H (1 [50] 4 [25] 3))"
      End
      Begin PaneConfiguration = 2
         NumPanes = 3
         Configuration = "(H (1 [50] 2 [25] 3))"
      End
      Begin PaneConfiguration = 3
         NumPanes = 3
         Configuration = "(H (4 [30] 2 [40] 3))"
      End
      Begin PaneConfiguration = 4
         NumPanes = 2
         Configuration = "(H (1 [56] 3))"
      End
      Begin PaneConfiguration = 5
         NumPanes = 2
         Configuration = "(H (2 [66] 3))"
      End
      Begin PaneConfiguration = 6
         NumPanes = 2
         Configuration = "(H (4 [50] 3))"
      End
      Begin PaneConfiguration = 7
         NumPanes = 1
         Configuration = "(V (3))"
      End
      Begin PaneConfiguration = 8
         NumPanes = 3
         Configuration = "(H (1[56] 4[18] 2) )"
      End
      Begin PaneConfiguration = 9
         NumPanes = 2
         Configuration = "(H (1 [75] 4))"
      End
      Begin PaneConfiguration = 10
         NumPanes = 2
         Configuration = "(H (1[66] 2) )"
      End
      Begin PaneConfiguration = 11
         NumPanes = 2
         Configuration = "(H (4 [60] 2))"
      End
      Begin PaneConfiguration = 12
         NumPanes = 1
         Configuration = "(H (1) )"
      End
      Begin PaneConfiguration = 13
         NumPanes = 1
         Configuration = "(V (4))"
      End
      Begin PaneConfiguration = 14
         NumPanes = 1
         Configuration = "(V (2))"
      End
      ActivePaneConfig = 0
   End
   Begin DiagramPane = 
      Begin Origin = 
         Top = 0
         Left = 0
      End
      Begin Tables = 
         Begin Table = "s"
            Begin Extent = 
               Top = 6
               Left = 38
               Bottom = 114
               Right = 216
            End
            DisplayFlags = 280
            TopColumn = 0
         End
         Begin Table = "f"
            Begin Extent = 
               Top = 6
               Left = 254
               Bottom = 84
               Right = 405
            End
            DisplayFlags = 280
            TopColumn = 0
         End
      End
   End
   Begin SQLPane = 
   End
   Begin DataPane = 
      Begin ParameterDefaults = ""
      End
   End
   Begin CriteriaPane = 
      Begin ColumnWidths = 11
         Column = 1440
         Alias = 900
         Table = 1170
         Output = 720
         Append = 1400
         NewValue = 1170
         SortType = 1350
         SortOrder = 1410
         GroupBy = 1350
         Filter = 1350
         Or = 1350
         Or = 1350
         Or = 1350
      End
   End
End
' , @level0type=N'SCHEMA',@level0name=N'dbo', @level1type=N'VIEW',@level1name=N'TestView'
GO
EXEC sys.sp_addextendedproperty @name=N'MS_DiagramPaneCount', @value=1 , @level0type=N'SCHEMA',@level0name=N'dbo', @level1type=N'VIEW',@level1name=N'TestView'
GO
EXEC sys.sp_addextendedproperty @name=N'MS_DiagramPane1', @value=N'[0E232FF0-B466-11cf-A24F-00AA00A3EFFF, 1.00]
Begin DesignProperties = 
   Begin PaneConfigurations = 
      Begin PaneConfiguration = 0
         NumPanes = 4
         Configuration = "(H (1[40] 4[20] 2[20] 3) )"
      End
      Begin PaneConfiguration = 1
         NumPanes = 3
         Configuration = "(H (1 [50] 4 [25] 3))"
      End
      Begin PaneConfiguration = 2
         NumPanes = 3
         Configuration = "(H (1 [50] 2 [25] 3))"
      End
      Begin PaneConfiguration = 3
         NumPanes = 3
         Configuration = "(H (4 [30] 2 [40] 3))"
      End
      Begin PaneConfiguration = 4
         NumPanes = 2
         Configuration = "(H (1 [56] 3))"
      End
      Begin PaneConfiguration = 5
         NumPanes = 2
         Configuration = "(H (2 [66] 3))"
      End
      Begin PaneConfiguration = 6
         NumPanes = 2
         Configuration = "(H (4 [50] 3))"
      End
      Begin PaneConfiguration = 7
         NumPanes = 1
         Configuration = "(V (3))"
      End
      Begin PaneConfiguration = 8
         NumPanes = 3
         Configuration = "(H (1[56] 4[18] 2) )"
      End
      Begin PaneConfiguration = 9
         NumPanes = 2
         Configuration = "(H (1 [75] 4))"
      End
      Begin PaneConfiguration = 10
         NumPanes = 2
         Configuration = "(H (1[66] 2) )"
      End
      Begin PaneConfiguration = 11
         NumPanes = 2
         Configuration = "(H (4 [60] 2))"
      End
      Begin PaneConfiguration = 12
         NumPanes = 1
         Configuration = "(H (1) )"
      End
      Begin PaneConfiguration = 13
         NumPanes = 1
         Configuration = "(V (4))"
      End
      Begin PaneConfiguration = 14
         NumPanes = 1
         Configuration = "(V (2))"
      End
      ActivePaneConfig = 0
   End
   Begin DiagramPane = 
      Begin Origin = 
         Top = 0
         Left = 0
      End
      Begin Tables = 
         Begin Table = "a"
            Begin Extent = 
               Top = 6
               Left = 38
               Bottom = 114
               Right = 216
            End
            DisplayFlags = 280
            TopColumn = 0
         End
         Begin Table = "q"
            Begin Extent = 
               Top = 6
               Left = 254
               Bottom = 84
               Right = 407
            End
            DisplayFlags = 280
            TopColumn = 0
         End
      End
   End
   Begin SQLPane = 
   End
   Begin DataPane = 
      Begin ParameterDefaults = ""
      End
   End
   Begin CriteriaPane = 
      Begin ColumnWidths = 11
         Column = 1440
         Alias = 900
         Table = 1170
         Output = 720
         Append = 1400
         NewValue = 1170
         SortType = 1350
         SortOrder = 1410
         GroupBy = 1350
         Filter = 1350
         Or = 1350
         Or = 1350
         Or = 1350
      End
   End
End
' , @level0type=N'SCHEMA',@level0name=N'dbo', @level1type=N'VIEW',@level1name=N'TestView2'
GO
EXEC sys.sp_addextendedproperty @name=N'MS_DiagramPaneCount', @value=1 , @level0type=N'SCHEMA',@level0name=N'dbo', @level1type=N'VIEW',@level1name=N'TestView2'
GO
USE [master]
GO
ALTER DATABASE [345] SET  READ_WRITE 
GO
