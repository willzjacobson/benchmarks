USE [master]
GO
/****** Object:  Database [560]    Script Date: 7/23/2013 2:53:27 AM ******/
CREATE DATABASE [560] ON  PRIMARY 
( NAME = N'560', FILENAME = N'E:\Microsoft SQL Server\MSSQL10_50.MSSQLSERVER\MSSQL\DATA\560.mdf' , SIZE = 437248KB , MAXSIZE = UNLIMITED, FILEGROWTH = 1024KB )
 LOG ON 
( NAME = N'560_log', FILENAME = N'E:\Microsoft SQL Server\MSSQL10_50.MSSQLSERVER\MSSQL\DATA\560_log.ldf' , SIZE = 1008000KB , MAXSIZE = 2048GB , FILEGROWTH = 10%)
GO
ALTER DATABASE [560] SET COMPATIBILITY_LEVEL = 100
GO
IF (1 = FULLTEXTSERVICEPROPERTY('IsFullTextInstalled'))
begin
EXEC [560].[dbo].[sp_fulltext_database] @action = 'enable'
end
GO
ALTER DATABASE [560] SET ANSI_NULL_DEFAULT OFF 
GO
ALTER DATABASE [560] SET ANSI_NULLS OFF 
GO
ALTER DATABASE [560] SET ANSI_PADDING OFF 
GO
ALTER DATABASE [560] SET ANSI_WARNINGS OFF 
GO
ALTER DATABASE [560] SET ARITHABORT OFF 
GO
ALTER DATABASE [560] SET AUTO_CLOSE OFF 
GO
ALTER DATABASE [560] SET AUTO_CREATE_STATISTICS ON 
GO
ALTER DATABASE [560] SET AUTO_SHRINK OFF 
GO
ALTER DATABASE [560] SET AUTO_UPDATE_STATISTICS ON 
GO
ALTER DATABASE [560] SET CURSOR_CLOSE_ON_COMMIT OFF 
GO
ALTER DATABASE [560] SET CURSOR_DEFAULT  GLOBAL 
GO
ALTER DATABASE [560] SET CONCAT_NULL_YIELDS_NULL OFF 
GO
ALTER DATABASE [560] SET NUMERIC_ROUNDABORT OFF 
GO
ALTER DATABASE [560] SET QUOTED_IDENTIFIER OFF 
GO
ALTER DATABASE [560] SET RECURSIVE_TRIGGERS OFF 
GO
ALTER DATABASE [560] SET  DISABLE_BROKER 
GO
ALTER DATABASE [560] SET AUTO_UPDATE_STATISTICS_ASYNC OFF 
GO
ALTER DATABASE [560] SET DATE_CORRELATION_OPTIMIZATION OFF 
GO
ALTER DATABASE [560] SET TRUSTWORTHY OFF 
GO
ALTER DATABASE [560] SET ALLOW_SNAPSHOT_ISOLATION OFF 
GO
ALTER DATABASE [560] SET PARAMETERIZATION SIMPLE 
GO
ALTER DATABASE [560] SET READ_COMMITTED_SNAPSHOT OFF 
GO
ALTER DATABASE [560] SET HONOR_BROKER_PRIORITY OFF 
GO
ALTER DATABASE [560] SET RECOVERY FULL 
GO
ALTER DATABASE [560] SET  MULTI_USER 
GO
ALTER DATABASE [560] SET PAGE_VERIFY CHECKSUM  
GO
ALTER DATABASE [560] SET DB_CHAINING OFF 
GO
USE [560]
GO
/****** Object:  User [TPOWEB_USER]    Script Date: 7/23/2013 2:53:27 AM ******/
CREATE USER [TPOWEB_USER] FOR LOGIN [TPOWEB_USER] WITH DEFAULT_SCHEMA=[dbo]
GO
/****** Object:  User [tpo]    Script Date: 7/23/2013 2:53:27 AM ******/
CREATE USER [tpo] FOR LOGIN [tpo] WITH DEFAULT_SCHEMA=[dbo]
GO
/****** Object:  User [rudin_user2]    Script Date: 7/23/2013 2:53:27 AM ******/
CREATE USER [rudin_user2] FOR LOGIN [rudin_user2] WITH DEFAULT_SCHEMA=[dbo]
GO
/****** Object:  User [rudin_user]    Script Date: 7/23/2013 2:53:27 AM ******/
CREATE USER [rudin_user] FOR LOGIN [rudin_user] WITH DEFAULT_SCHEMA=[dbo]
GO
/****** Object:  User [rudin_db_reader]    Script Date: 7/23/2013 2:53:27 AM ******/
CREATE USER [rudin_db_reader] FOR LOGIN [rudin_db_reader] WITH DEFAULT_SCHEMA=[dbo]
GO
/****** Object:  User [ANDERSON\ashwath]    Script Date: 7/23/2013 2:53:27 AM ******/
CREATE USER [ANDERSON\ashwath] FOR LOGIN [ANDERSON\ashwath] WITH DEFAULT_SCHEMA=[dbo]
GO
/****** Object:  User [ANDERSON\agagneja]    Script Date: 7/23/2013 2:53:28 AM ******/
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
ALTER ROLE [db_datareader] ADD MEMBER [rudin_db_reader]
GO
ALTER ROLE [db_datawriter] ADD MEMBER [rudin_db_reader]
GO
ALTER ROLE [db_owner] ADD MEMBER [ANDERSON\ashwath]
GO
ALTER ROLE [db_owner] ADD MEMBER [ANDERSON\agagneja]
GO
/****** Object:  Table [dbo].[560---------000ACS---TURINC---IN001]    Script Date: 7/23/2013 2:53:29 AM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[560---------000ACS---TURINC---IN001](
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
/****** Object:  Table [dbo].[560---------000ACS---TUROUT---OUT001]    Script Date: 7/23/2013 2:53:29 AM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[560---------000ACS---TUROUT---OUT001](
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
/****** Object:  Table [dbo].[560---------000SECCNTPEOBUI---INC001]    Script Date: 7/23/2013 2:53:29 AM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[560---------000SECCNTPEOBUI---INC001](
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
/****** Object:  Table [dbo].[560---------000SECCNTPEOBUI---OUT001]    Script Date: 7/23/2013 2:53:29 AM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[560---------000SECCNTPEOBUI---OUT001](
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
/****** Object:  Table [dbo].[560---------000SECCNTPEOBUI---VAL001]    Script Date: 7/23/2013 2:53:29 AM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[560---------000SECCNTPEOBUI---VAL001](
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
/****** Object:  Table [dbo].[560---------000TPO---ALA---001]    Script Date: 7/23/2013 2:53:29 AM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
SET ANSI_PADDING ON
GO
CREATE TABLE [dbo].[560---------000TPO---ALA---001](
	[ID] [int] IDENTITY(1,1) NOT NULL,
	[STATE] [int] NULL,
	[PROPERTY_PRIO] [int] NULL,
	[INTERNAL] [int] NULL,
	[INITTS] [datetime] NULL,
	[NORMTS] [datetime] NULL,
	[PBS] [varchar](10) NULL,
	[SIGN] [varchar](100) NULL,
 CONSTRAINT [PK_560---------000TPO---ALA---001] PRIMARY KEY CLUSTERED 
(
	[ID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]

GO
SET ANSI_PADDING OFF
GO
/****** Object:  Table [dbo].[560---------000TPOFORELECON001---001]    Script Date: 7/23/2013 2:53:29 AM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[560---------000TPOFORELECON001---001](
	[Run_DateTime] [datetime] NOT NULL,
	[Prediction_DateTime] [datetime] NOT NULL,
	[Prediction_Value] [float] NULL,
	[Lower_Bound_95] [float] NULL,
	[Upper_Bound_95] [float] NULL,
	[Lower_Bound_68] [float] NULL,
	[Upper_Bound_68] [float] NULL,
	[ID] [int] IDENTITY(1,1) NOT NULL,
 CONSTRAINT [PK__Electric__B1D96F1829572725] PRIMARY KEY CLUSTERED 
(
	[Run_DateTime] ASC,
	[Prediction_DateTime] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]

GO
/****** Object:  Table [dbo].[560---------000TPOFORELECON001---001_RBF_Params]    Script Date: 7/23/2013 2:53:29 AM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[560---------000TPOFORELECON001---001_RBF_Params](
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
/****** Object:  Table [dbo].[560---------000TPOFORELECON001---001_Stats]    Script Date: 7/23/2013 2:53:29 AM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[560---------000TPOFORELECON001---001_Stats](
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
/****** Object:  Table [dbo].[560---------000TPOFORTEMSPA001---001]    Script Date: 7/23/2013 2:53:29 AM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[560---------000TPOFORTEMSPA001---001](
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
/****** Object:  Table [dbo].[560---------000TPOFORTEMSPA001---001_Deltas]    Script Date: 7/23/2013 2:53:29 AM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[560---------000TPOFORTEMSPA001---001_Deltas](
	[Timestamp] [datetime] NOT NULL,
	[Floor] [nvarchar](50) NOT NULL,
	[Quadrant] [nvarchar](50) NOT NULL,
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
/****** Object:  Table [dbo].[560---------000TPOFORTEMSPA001---001_Derivative]    Script Date: 7/23/2013 2:53:29 AM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[560---------000TPOFORTEMSPA001---001_Derivative](
	[Run_DateTime] [datetime] NOT NULL,
	[Prediction_DateTime] [datetime] NOT NULL,
	[Floor] [nvarchar](50) NOT NULL,
	[Quadrant] [nvarchar](50) NOT NULL,
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
/****** Object:  Table [dbo].[560---------000TPOFORTEMSPA001---001_orig]    Script Date: 7/23/2013 2:53:29 AM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[560---------000TPOFORTEMSPA001---001_orig](
	[Run_DateTime] [datetime] NOT NULL,
	[Prediction_DateTime] [datetime] NOT NULL,
	[Floor] [int] NOT NULL,
	[Controller] [nvarchar](50) NOT NULL,
	[SubController] [nvarchar](50) NOT NULL,
	[Prediction_Value] [float] NULL,
	[Lower_Bound_95] [float] NULL,
	[Upper_Bound_95] [float] NULL,
	[Lower_Bound_68] [float] NULL,
	[Upper_Bound_68] [float] NULL,
	[ID] [int] IDENTITY(1,1) NOT NULL,
 CONSTRAINT [PK__Space_Te__4A90E7C825869641] PRIMARY KEY CLUSTERED 
(
	[Run_DateTime] ASC,
	[Prediction_DateTime] ASC,
	[Floor] ASC,
	[Controller] ASC,
	[SubController] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]

GO
/****** Object:  Table [dbo].[560---------000TPOFORTEMSPA001---001_RBF_Params]    Script Date: 7/23/2013 2:53:29 AM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[560---------000TPOFORTEMSPA001---001_RBF_Params](
	[Run_DateTime] [datetime] NOT NULL,
	[Floor] [nvarchar](50) NOT NULL,
	[Quadrant] [nvarchar](50) NOT NULL,
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
/****** Object:  Table [dbo].[560---------000TPOFORTEMSPA001---001_Stats]    Script Date: 7/23/2013 2:53:29 AM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[560---------000TPOFORTEMSPA001---001_Stats](
	[Prediction_Date] [datetime] NOT NULL,
	[Floor] [nvarchar](50) NOT NULL,
	[Quadrant] [nvarchar](50) NOT NULL,
	[RMSE] [float] NOT NULL,
	[MAE] [float] NOT NULL,
	[MAPE] [float] NOT NULL,
PRIMARY KEY CLUSTERED 
(
	[Prediction_Date] ASC,
	[Floor] ASC,
	[Quadrant] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]

GO
/****** Object:  Table [dbo].[560---------000TPONOWTEMSPA001---001]    Script Date: 7/23/2013 2:53:29 AM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[560---------000TPONOWTEMSPA001---001](
	[Run_DateTime] [datetime] NOT NULL,
	[Prediction_DateTime] [datetime] NOT NULL,
	[Value] [real] NULL,
	[Floor] [nchar](3) NOT NULL,
	[Quadrant] [nchar](3) NOT NULL,
	[Prediction_Timestep] [int] NOT NULL,
	[ID] [int] IDENTITY(1,1) NOT NULL,
	[Control_Setting] [float] NULL,
 CONSTRAINT [PK_560---------000TPONOWTEMSPA001---001] PRIMARY KEY CLUSTERED 
(
	[Run_DateTime] ASC,
	[Prediction_DateTime] ASC,
	[Floor] ASC,
	[Quadrant] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]

GO
/****** Object:  Table [dbo].[560---------000TPOOPTTEMRDW001---001]    Script Date: 7/23/2013 2:53:29 AM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[560---------000TPOOPTTEMRDW001---001](
	[ID] [int] IDENTITY(1,1) NOT NULL,
	[Run_DateTime] [datetime] NULL,
	[Prediction_DateTime] [datetime] NULL,
 CONSTRAINT [PK_rampdown_time_rec] PRIMARY KEY CLUSTERED 
(
	[ID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]

GO
/****** Object:  Table [dbo].[560---------000TPOOPTTEMUPT001---001]    Script Date: 7/23/2013 2:53:29 AM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[560---------000TPOOPTTEMUPT001---001](
	[ID] [int] IDENTITY(1,1) NOT NULL,
	[Run_DateTime] [datetime] NULL,
	[Prediction_DateTime] [datetime] NULL,
 CONSTRAINT [PK_startup_time_rec] PRIMARY KEY CLUSTERED 
(
	[ID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]

GO
/****** Object:  Table [dbo].[560---------002BMSELEMET------VAL001]    Script Date: 7/23/2013 2:53:29 AM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[560---------002BMSELEMET------VAL001](
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
/****** Object:  Table [dbo].[560---------002BMSHVAFANRAT---VAL001]    Script Date: 7/23/2013 2:53:29 AM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[560---------002BMSHVAFANRAT---VAL001](
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
/****** Object:  Table [dbo].[560---------002BMSHVAFANSAT---VAL001]    Script Date: 7/23/2013 2:53:29 AM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[560---------002BMSHVAFANSAT---VAL001](
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
/****** Object:  Table [dbo].[560---------002BMSHVAFAN------VAL001]    Script Date: 7/23/2013 2:53:29 AM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[560---------002BMSHVAFAN------VAL001](
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
/****** Object:  Table [dbo].[560---------002BMSHVATEMSPA---VAL001]    Script Date: 7/23/2013 2:53:29 AM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[560---------002BMSHVATEMSPA---VAL001](
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
/****** Object:  Table [dbo].[560---------002BMSWATCHIHUM---VAL001]    Script Date: 7/23/2013 2:53:29 AM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[560---------002BMSWATCHIHUM---VAL001](
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
/****** Object:  Table [dbo].[560---------002BMSWATCHIRET---VAL001]    Script Date: 7/23/2013 2:53:29 AM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[560---------002BMSWATCHIRET---VAL001](
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
/****** Object:  Table [dbo].[560---------002BMSWATCHISUP---VAL001]    Script Date: 7/23/2013 2:53:29 AM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[560---------002BMSWATCHISUP---VAL001](
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
/****** Object:  Table [dbo].[560---------002BMSWATCHITEM---VAL001]    Script Date: 7/23/2013 2:53:29 AM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[560---------002BMSWATCHITEM---VAL001](
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
/****** Object:  Table [dbo].[560---------002BMSWATHOT------VAL001]    Script Date: 7/23/2013 2:53:29 AM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[560---------002BMSWATHOT------VAL001](
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
/****** Object:  Table [dbo].[dummyTable]    Script Date: 7/23/2013 2:53:29 AM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[dummyTable](
	[Run_DateTime] [datetime] NULL,
	[Prediction_DateTime] [datetime] NULL,
	[Value] [real] NULL,
	[Floor] [nchar](3) NULL,
	[Quadrant] [nchar](3) NULL,
	[Prediction_Timestep] [int] NOT NULL,
	[ID] [int] IDENTITY(1,1) NOT NULL,
	[Control_Setting] [float] NULL,
 CONSTRAINT [PK_dummyTable] PRIMARY KEY CLUSTERED 
(
	[ID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]

GO
/****** Object:  Table [dbo].[Floor_Mapping]    Script Date: 7/23/2013 2:53:29 AM ******/
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
/****** Object:  Table [dbo].[Quadrant_Mapping]    Script Date: 7/23/2013 2:53:29 AM ******/
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
/****** Object:  Table [dbo].[Ramp_Down_Time_DS]    Script Date: 7/23/2013 2:53:29 AM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[Ramp_Down_Time_DS](
	[ID] [int] NULL,
	[TIMESTAMP] [datetime] NULL,
	[Value] [int] NULL
) ON [PRIMARY]

GO
/****** Object:  Table [dbo].[SYNCH_TEST]    Script Date: 7/23/2013 2:53:29 AM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[SYNCH_TEST](
	[ID] [int] IDENTITY(1,1) NOT NULL,
	[ZONE] [nchar](3) NULL,
	[FLOOR] [nchar](3) NULL,
	[QUADRANT] [nchar](3) NULL,
	[EQUIPMENT_NO] [nchar](3) NULL,
	[TIMESTAMP] [datetime] NULL,
	[VALUE] [float] NULL,
 CONSTRAINT [PK_SYNCH_TEST] PRIMARY KEY CLUSTERED 
(
	[ID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]

GO
/****** Object:  View [dbo].[Space_Temp_Comp]    Script Date: 7/23/2013 2:53:29 AM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE VIEW [dbo].[Space_Temp_Comp]
AS
SELECT     s.Run_DateTime, s.Prediction_DateTime, f.CompFloor AS Floor, s.Prediction_Value, s.Lower_Bound_95, s.Upper_Bound_95, s.Lower_Bound_68, s.Upper_Bound_68, 
                      s.ID
FROM         dbo.[560---------000TPOFORTEMSPA001---001_orig] AS s INNER JOIN
                      dbo.Floor_Mapping AS f ON s.Floor = f.Floor

GO
/****** Object:  View [dbo].[Space_Temp_Prediction]    Script Date: 7/23/2013 2:53:29 AM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE VIEW [dbo].[Space_Temp_Prediction]
AS
SELECT     Run_DateTime, Prediction_DateTime, Floor, Prediction_Value, Lower_Bound_95, Upper_Bound_95, Lower_Bound_68, Upper_Bound_68, ID
FROM         dbo.[560---------000TPOFORTEMSPA001---001]

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
      End
   End
   Begin SQLPane = 
   End
   Begin DataPane = 
      Begin ParameterDefaults = ""
      End
      Begin ColumnWidths = 10
         Width = 284
         Width = 1500
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
         Begin Table = "560---------000TPOFORTEMSPA001---001"
            Begin Extent = 
               Top = 6
               Left = 38
               Bottom = 114
               Right = 216
            End
            DisplayFlags = 280
            TopColumn = 6
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
' , @level0type=N'SCHEMA',@level0name=N'dbo', @level1type=N'VIEW',@level1name=N'Space_Temp_Prediction'
GO
EXEC sys.sp_addextendedproperty @name=N'MS_DiagramPaneCount', @value=1 , @level0type=N'SCHEMA',@level0name=N'dbo', @level1type=N'VIEW',@level1name=N'Space_Temp_Prediction'
GO
USE [master]
GO
ALTER DATABASE [560] SET  READ_WRITE 
GO
