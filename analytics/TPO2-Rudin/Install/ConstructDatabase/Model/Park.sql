USE [$database$]
GO

/****** Object:  User [rudin_db_user2]    Script Date: 07/23/2013 01:51:14 ******/
CREATE USER [rudin_db_user2] FOR LOGIN [rudin_db_user2] WITH DEFAULT_SCHEMA=[dbo]
GO
/****** Object:  User [rudin_user]    Script Date: 07/23/2013 01:51:14 ******/
CREATE USER [rudin_user] FOR LOGIN [rudin_user] WITH DEFAULT_SCHEMA=[dbo]
GO
/****** Object:  User [rudin_user2]    Script Date: 07/23/2013 01:51:14 ******/
CREATE USER [rudin_user2] FOR LOGIN [rudin_user2] WITH DEFAULT_SCHEMA=[dbo]
GO
/****** Object:  User [tpo]    Script Date: 07/23/2013 01:51:14 ******/
CREATE USER [tpo] FOR LOGIN [tpo] WITH DEFAULT_SCHEMA=[dbo]
GO
/****** Object:  User [TPOWEB_USER]    Script Date: 07/23/2013 01:51:14 ******/
CREATE USER [TPOWEB_USER] FOR LOGIN [TPOWEB_USER] WITH DEFAULT_SCHEMA=[dbo]
GO
/****** Object:  Table [dbo].[Ramp_Down_Time_DS]    Script Date: 07/23/2013 01:51:13 ******/
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
/****** Object:  Table [dbo].[Quadrant_Mapping]    Script Date: 07/23/2013 01:51:13 ******/
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
)WITH (PAD_INDEX  = OFF, STATISTICS_NORECOMPUTE  = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS  = ON, ALLOW_PAGE_LOCKS  = ON) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[Floor_Mapping]    Script Date: 07/23/2013 01:51:13 ******/
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
)WITH (PAD_INDEX  = OFF, STATISTICS_NORECOMPUTE  = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS  = ON, ALLOW_PAGE_LOCKS  = ON) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[$database$---------001EMSSMAMET------40140004]    Script Date: 07/23/2013 01:51:13 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[$database$---------001EMSSMAMET------40140004](
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
)WITH (PAD_INDEX  = OFF, STATISTICS_NORECOMPUTE  = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS  = ON, ALLOW_PAGE_LOCKS  = ON) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[$database$---------001EMSSMAMET------40140003]    Script Date: 07/23/2013 01:51:13 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[$database$---------001EMSSMAMET------40140003](
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
)WITH (PAD_INDEX  = OFF, STATISTICS_NORECOMPUTE  = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS  = ON, ALLOW_PAGE_LOCKS  = ON) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[$database$---------001EMSSMAMET------40140002]    Script Date: 07/23/2013 01:51:13 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[$database$---------001EMSSMAMET------40140002](
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
)WITH (PAD_INDEX  = OFF, STATISTICS_NORECOMPUTE  = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS  = ON, ALLOW_PAGE_LOCKS  = ON) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[$database$---------001EMSSMAMET------40140001]    Script Date: 07/23/2013 01:51:13 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[$database$---------001EMSSMAMET------40140001](
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
)WITH (PAD_INDEX  = OFF, STATISTICS_NORECOMPUTE  = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS  = ON, ALLOW_PAGE_LOCKS  = ON) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[$database$---------001EMSSMAMET------40138004]    Script Date: 07/23/2013 01:51:13 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[$database$---------001EMSSMAMET------40138004](
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
)WITH (PAD_INDEX  = OFF, STATISTICS_NORECOMPUTE  = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS  = ON, ALLOW_PAGE_LOCKS  = ON) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[$database$---------001EMSSMAMET------40138003]    Script Date: 07/23/2013 01:51:13 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[$database$---------001EMSSMAMET------40138003](
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
)WITH (PAD_INDEX  = OFF, STATISTICS_NORECOMPUTE  = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS  = ON, ALLOW_PAGE_LOCKS  = ON) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[$database$---------001EMSSMAMET------40138002]    Script Date: 07/23/2013 01:51:13 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[$database$---------001EMSSMAMET------40138002](
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
)WITH (PAD_INDEX  = OFF, STATISTICS_NORECOMPUTE  = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS  = ON, ALLOW_PAGE_LOCKS  = ON) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[$database$---------001EMSSMAMET------40138001]    Script Date: 07/23/2013 01:51:13 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[$database$---------001EMSSMAMET------40138001](
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
)WITH (PAD_INDEX  = OFF, STATISTICS_NORECOMPUTE  = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS  = ON, ALLOW_PAGE_LOCKS  = ON) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[$database$---------001EMSSMAMET------40132004]    Script Date: 07/23/2013 01:51:13 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[$database$---------001EMSSMAMET------40132004](
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
)WITH (PAD_INDEX  = OFF, STATISTICS_NORECOMPUTE  = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS  = ON, ALLOW_PAGE_LOCKS  = ON) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[$database$---------001EMSSMAMET------40132003]    Script Date: 07/23/2013 01:51:13 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[$database$---------001EMSSMAMET------40132003](
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
)WITH (PAD_INDEX  = OFF, STATISTICS_NORECOMPUTE  = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS  = ON, ALLOW_PAGE_LOCKS  = ON) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[$database$---------001EMSSMAMET------40132002]    Script Date: 07/23/2013 01:51:13 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[$database$---------001EMSSMAMET------40132002](
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
)WITH (PAD_INDEX  = OFF, STATISTICS_NORECOMPUTE  = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS  = ON, ALLOW_PAGE_LOCKS  = ON) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[$database$---------001EMSSMAMET------40132001]    Script Date: 07/23/2013 01:51:13 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[$database$---------001EMSSMAMET------40132001](
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
)WITH (PAD_INDEX  = OFF, STATISTICS_NORECOMPUTE  = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS  = ON, ALLOW_PAGE_LOCKS  = ON) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[$database$---------001EMSSMAMET------40120004]    Script Date: 07/23/2013 01:51:13 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[$database$---------001EMSSMAMET------40120004](
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
)WITH (PAD_INDEX  = OFF, STATISTICS_NORECOMPUTE  = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS  = ON, ALLOW_PAGE_LOCKS  = ON) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[$database$---------001EMSSMAMET------40120003]    Script Date: 07/23/2013 01:51:13 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[$database$---------001EMSSMAMET------40120003](
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
)WITH (PAD_INDEX  = OFF, STATISTICS_NORECOMPUTE  = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS  = ON, ALLOW_PAGE_LOCKS  = ON) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[$database$---------001EMSSMAMET------40120002]    Script Date: 07/23/2013 01:51:13 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[$database$---------001EMSSMAMET------40120002](
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
)WITH (PAD_INDEX  = OFF, STATISTICS_NORECOMPUTE  = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS  = ON, ALLOW_PAGE_LOCKS  = ON) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[$database$---------001EMSSMAMET------40120001]    Script Date: 07/23/2013 01:51:13 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[$database$---------001EMSSMAMET------40120001](
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
)WITH (PAD_INDEX  = OFF, STATISTICS_NORECOMPUTE  = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS  = ON, ALLOW_PAGE_LOCKS  = ON) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[$database$---------001EMSBMMMET------40029001]    Script Date: 07/23/2013 01:51:13 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[$database$---------001EMSBMMMET------40029001](
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
)WITH (PAD_INDEX  = OFF, STATISTICS_NORECOMPUTE  = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS  = ON, ALLOW_PAGE_LOCKS  = ON) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[$database$---------001EMSBMMMET------40027001]    Script Date: 07/23/2013 01:51:13 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[$database$---------001EMSBMMMET------40027001](
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
)WITH (PAD_INDEX  = OFF, STATISTICS_NORECOMPUTE  = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS  = ON, ALLOW_PAGE_LOCKS  = ON) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[$database$---------001EMSBMMMET------40025001]    Script Date: 07/23/2013 01:51:13 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[$database$---------001EMSBMMMET------40025001](
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
)WITH (PAD_INDEX  = OFF, STATISTICS_NORECOMPUTE  = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS  = ON, ALLOW_PAGE_LOCKS  = ON) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[$database$---------001EMSBMMMET------40023001]    Script Date: 07/23/2013 01:51:13 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[$database$---------001EMSBMMMET------40023001](
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
)WITH (PAD_INDEX  = OFF, STATISTICS_NORECOMPUTE  = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS  = ON, ALLOW_PAGE_LOCKS  = ON) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[$database$---------001EMSBMMMET------40021001]    Script Date: 07/23/2013 01:51:13 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[$database$---------001EMSBMMMET------40021001](
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
)WITH (PAD_INDEX  = OFF, STATISTICS_NORECOMPUTE  = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS  = ON, ALLOW_PAGE_LOCKS  = ON) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[$database$---------001EMSBMMMET------40019001]    Script Date: 07/23/2013 01:51:13 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[$database$---------001EMSBMMMET------40019001](
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
)WITH (PAD_INDEX  = OFF, STATISTICS_NORECOMPUTE  = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS  = ON, ALLOW_PAGE_LOCKS  = ON) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[$database$---------001EMSBMMMET------40017001]    Script Date: 07/23/2013 01:51:13 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[$database$---------001EMSBMMMET------40017001](
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
)WITH (PAD_INDEX  = OFF, STATISTICS_NORECOMPUTE  = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS  = ON, ALLOW_PAGE_LOCKS  = ON) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[$database$---------001EMSBMMMET------40015001]    Script Date: 07/23/2013 01:51:13 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[$database$---------001EMSBMMMET------40015001](
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
)WITH (PAD_INDEX  = OFF, STATISTICS_NORECOMPUTE  = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS  = ON, ALLOW_PAGE_LOCKS  = ON) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[$database$---------001EMSBMMMET------40013001]    Script Date: 07/23/2013 01:51:13 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[$database$---------001EMSBMMMET------40013001](
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
)WITH (PAD_INDEX  = OFF, STATISTICS_NORECOMPUTE  = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS  = ON, ALLOW_PAGE_LOCKS  = ON) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[$database$---------001EMSBMMMET------40011001]    Script Date: 07/23/2013 01:51:13 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[$database$---------001EMSBMMMET------40011001](
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
)WITH (PAD_INDEX  = OFF, STATISTICS_NORECOMPUTE  = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS  = ON, ALLOW_PAGE_LOCKS  = ON) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[$database$---------001EMSBMMMET------40009001]    Script Date: 07/23/2013 01:51:13 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[$database$---------001EMSBMMMET------40009001](
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
)WITH (PAD_INDEX  = OFF, STATISTICS_NORECOMPUTE  = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS  = ON, ALLOW_PAGE_LOCKS  = ON) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[$database$---------001EMSBMMMET------40007001]    Script Date: 07/23/2013 01:51:13 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[$database$---------001EMSBMMMET------40007001](
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
)WITH (PAD_INDEX  = OFF, STATISTICS_NORECOMPUTE  = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS  = ON, ALLOW_PAGE_LOCKS  = ON) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[$database$---------001EMSBMMMET------40005001]    Script Date: 07/23/2013 01:51:13 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[$database$---------001EMSBMMMET------40005001](
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
)WITH (PAD_INDEX  = OFF, STATISTICS_NORECOMPUTE  = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS  = ON, ALLOW_PAGE_LOCKS  = ON) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[$database$---------001EMSBMMMET------40003001]    Script Date: 07/23/2013 01:51:13 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[$database$---------001EMSBMMMET------40003001](
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
)WITH (PAD_INDEX  = OFF, STATISTICS_NORECOMPUTE  = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS  = ON, ALLOW_PAGE_LOCKS  = ON) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[$database$---------001EMSBMMMET------40001001]    Script Date: 07/23/2013 01:51:13 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[$database$---------001EMSBMMMET------40001001](
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
)WITH (PAD_INDEX  = OFF, STATISTICS_NORECOMPUTE  = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS  = ON, ALLOW_PAGE_LOCKS  = ON) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[$database$---------001BMSWATTNK------ALA002]    Script Date: 07/23/2013 01:51:13 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[$database$---------001BMSWATTNK------ALA002](
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
)WITH (PAD_INDEX  = OFF, STATISTICS_NORECOMPUTE  = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS  = ON, ALLOW_PAGE_LOCKS  = ON) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[$database$---------001BMSWATTNK------ALA001]    Script Date: 07/23/2013 01:51:13 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[$database$---------001BMSWATTNK------ALA001](
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
)WITH (PAD_INDEX  = OFF, STATISTICS_NORECOMPUTE  = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS  = ON, ALLOW_PAGE_LOCKS  = ON) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[$database$---------001BMSWATSECSUP---VAL001]    Script Date: 07/23/2013 01:51:13 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[$database$---------001BMSWATSECSUP---VAL001](
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
)WITH (PAD_INDEX  = OFF, STATISTICS_NORECOMPUTE  = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS  = ON, ALLOW_PAGE_LOCKS  = ON) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[$database$---------001BMSWATSECSMO---VAL001]    Script Date: 07/23/2013 01:51:13 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[$database$---------001BMSWATSECSMO---VAL001](
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
)WITH (PAD_INDEX  = OFF, STATISTICS_NORECOMPUTE  = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS  = ON, ALLOW_PAGE_LOCKS  = ON) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[$database$---------001BMSWATSECRET---VAL001]    Script Date: 07/23/2013 01:51:13 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[$database$---------001BMSWATSECRET---VAL001](
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
)WITH (PAD_INDEX  = OFF, STATISTICS_NORECOMPUTE  = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS  = ON, ALLOW_PAGE_LOCKS  = ON) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[$database$---------001BMSWATSECPUM---VAL001]    Script Date: 07/23/2013 01:51:13 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[$database$---------001BMSWATSECPUM---VAL001](
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
)WITH (PAD_INDEX  = OFF, STATISTICS_NORECOMPUTE  = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS  = ON, ALLOW_PAGE_LOCKS  = ON) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[$database$---------001BMSWATSECPUM---ALA001]    Script Date: 07/23/2013 01:51:13 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[$database$---------001BMSWATSECPUM---ALA001](
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
)WITH (PAD_INDEX  = OFF, STATISTICS_NORECOMPUTE  = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS  = ON, ALLOW_PAGE_LOCKS  = ON) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[$database$---------001BMSWATSEC------ALA002]    Script Date: 07/23/2013 01:51:13 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[$database$---------001BMSWATSEC------ALA002](
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
)WITH (PAD_INDEX  = OFF, STATISTICS_NORECOMPUTE  = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS  = ON, ALLOW_PAGE_LOCKS  = ON) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[$database$---------001BMSWATSEC------ALA001]    Script Date: 07/23/2013 01:51:13 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[$database$---------001BMSWATSEC------ALA001](
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
)WITH (PAD_INDEX  = OFF, STATISTICS_NORECOMPUTE  = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS  = ON, ALLOW_PAGE_LOCKS  = ON) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[$database$---------001BMSWATHOTINT---VAL001]    Script Date: 07/23/2013 01:51:13 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[$database$---------001BMSWATHOTINT---VAL001](
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
)WITH (PAD_INDEX  = OFF, STATISTICS_NORECOMPUTE  = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS  = ON, ALLOW_PAGE_LOCKS  = ON) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[$database$---------001BMSWATHOT------ALA002]    Script Date: 07/23/2013 01:51:13 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[$database$---------001BMSWATHOT------ALA002](
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
)WITH (PAD_INDEX  = OFF, STATISTICS_NORECOMPUTE  = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS  = ON, ALLOW_PAGE_LOCKS  = ON) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[$database$---------001BMSWATHOT------ALA001]    Script Date: 07/23/2013 01:51:13 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[$database$---------001BMSWATHOT------ALA001](
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
)WITH (PAD_INDEX  = OFF, STATISTICS_NORECOMPUTE  = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS  = ON, ALLOW_PAGE_LOCKS  = ON) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[$database$---------001BMSWATCHISUP---VAL001]    Script Date: 07/23/2013 01:51:13 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[$database$---------001BMSWATCHISUP---VAL001](
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
)WITH (PAD_INDEX  = OFF, STATISTICS_NORECOMPUTE  = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS  = ON, ALLOW_PAGE_LOCKS  = ON) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[$database$---------001BMSWATCHIRET---VAL001]    Script Date: 07/23/2013 01:51:13 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[$database$---------001BMSWATCHIRET---VAL001](
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
)WITH (PAD_INDEX  = OFF, STATISTICS_NORECOMPUTE  = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS  = ON, ALLOW_PAGE_LOCKS  = ON) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[$database$---------001BMSWATCHIDIF---VAL001]    Script Date: 07/23/2013 01:51:13 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[$database$---------001BMSWATCHIDIF---VAL001](
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
)WITH (PAD_INDEX  = OFF, STATISTICS_NORECOMPUTE  = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS  = ON, ALLOW_PAGE_LOCKS  = ON) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[$database$---------001BMSSTEMET------VAL001]    Script Date: 07/23/2013 01:51:13 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[$database$---------001BMSSTEMET------VAL001](
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
)WITH (PAD_INDEX  = OFF, STATISTICS_NORECOMPUTE  = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS  = ON, ALLOW_PAGE_LOCKS  = ON) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[$database$---------001BMSSTEMET------MVA001]    Script Date: 07/23/2013 01:51:13 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[$database$---------001BMSSTEMET------MVA001](
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
)WITH (PAD_INDEX  = OFF, STATISTICS_NORECOMPUTE  = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS  = ON, ALLOW_PAGE_LOCKS  = ON) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[$database$---------001BMSSTEMET------LVA001]    Script Date: 07/23/2013 01:51:13 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[$database$---------001BMSSTEMET------LVA001](
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
)WITH (PAD_INDEX  = OFF, STATISTICS_NORECOMPUTE  = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS  = ON, ALLOW_PAGE_LOCKS  = ON) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[$database$---------001BMSSTEMET------HVA001]    Script Date: 07/23/2013 01:51:13 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[$database$---------001BMSSTEMET------HVA001](
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
)WITH (PAD_INDEX  = OFF, STATISTICS_NORECOMPUTE  = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS  = ON, ALLOW_PAGE_LOCKS  = ON) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[$database$---------001BMSSTEMET------ALA002]    Script Date: 07/23/2013 01:51:13 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[$database$---------001BMSSTEMET------ALA002](
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
)WITH (PAD_INDEX  = OFF, STATISTICS_NORECOMPUTE  = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS  = ON, ALLOW_PAGE_LOCKS  = ON) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[$database$---------001BMSSTEMET------ALA001]    Script Date: 07/23/2013 01:51:13 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[$database$---------001BMSSTEMET------ALA001](
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
)WITH (PAD_INDEX  = OFF, STATISTICS_NORECOMPUTE  = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS  = ON, ALLOW_PAGE_LOCKS  = ON) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[$database$---------001BMSHVAWEATEM---VAL001]    Script Date: 07/23/2013 01:51:13 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[$database$---------001BMSHVAWEATEM---VAL001](
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
)WITH (PAD_INDEX  = OFF, STATISTICS_NORECOMPUTE  = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS  = ON, ALLOW_PAGE_LOCKS  = ON) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[$database$---------001BMSHVAWEATEM---AVG001]    Script Date: 07/23/2013 01:51:13 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[$database$---------001BMSHVAWEATEM---AVG001](
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
)WITH (PAD_INDEX  = OFF, STATISTICS_NORECOMPUTE  = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS  = ON, ALLOW_PAGE_LOCKS  = ON) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[$database$---------001BMSHVAWEAHUM---VAL001]    Script Date: 07/23/2013 01:51:13 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[$database$---------001BMSHVAWEAHUM---VAL001](
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
)WITH (PAD_INDEX  = OFF, STATISTICS_NORECOMPUTE  = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS  = ON, ALLOW_PAGE_LOCKS  = ON) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[$database$---------001BMSHVAWEAHUM---AVG001]    Script Date: 07/23/2013 01:51:13 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[$database$---------001BMSHVAWEAHUM---AVG001](
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
)WITH (PAD_INDEX  = OFF, STATISTICS_NORECOMPUTE  = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS  = ON, ALLOW_PAGE_LOCKS  = ON) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[$database$---------001BMSHVATEMSPA---VAL001]    Script Date: 07/23/2013 01:51:13 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[$database$---------001BMSHVATEMSPA---VAL001](
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
)WITH (PAD_INDEX  = OFF, STATISTICS_NORECOMPUTE  = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS  = ON, ALLOW_PAGE_LOCKS  = ON) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[$database$---------001BMSHVATEMPSP---VAL001]    Script Date: 07/23/2013 01:51:13 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[$database$---------001BMSHVATEMPSP---VAL001](
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
)WITH (PAD_INDEX  = OFF, STATISTICS_NORECOMPUTE  = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS  = ON, ALLOW_PAGE_LOCKS  = ON) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[$database$---------001BMSHVATCT------ALA003]    Script Date: 07/23/2013 01:51:13 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[$database$---------001BMSHVATCT------ALA003](
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
)WITH (PAD_INDEX  = OFF, STATISTICS_NORECOMPUTE  = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS  = ON, ALLOW_PAGE_LOCKS  = ON) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[$database$---------001BMSHVATCT------ALA002]    Script Date: 07/23/2013 01:51:13 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[$database$---------001BMSHVATCT------ALA002](
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
)WITH (PAD_INDEX  = OFF, STATISTICS_NORECOMPUTE  = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS  = ON, ALLOW_PAGE_LOCKS  = ON) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[$database$---------001BMSHVATCT------ALA001]    Script Date: 07/23/2013 01:51:13 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[$database$---------001BMSHVATCT------ALA001](
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
)WITH (PAD_INDEX  = OFF, STATISTICS_NORECOMPUTE  = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS  = ON, ALLOW_PAGE_LOCKS  = ON) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[$database$---------001BMSHVAPNE------ALA001]    Script Date: 07/23/2013 01:51:13 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[$database$---------001BMSHVAPNE------ALA001](
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
)WITH (PAD_INDEX  = OFF, STATISTICS_NORECOMPUTE  = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS  = ON, ALLOW_PAGE_LOCKS  = ON) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[$database$---------001BMSHVAPFASAT---SPV001]    Script Date: 07/23/2013 01:51:13 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[$database$---------001BMSHVAPFASAT---SPV001](
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
)WITH (PAD_INDEX  = OFF, STATISTICS_NORECOMPUTE  = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS  = ON, ALLOW_PAGE_LOCKS  = ON) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[$database$---------001BMSHVAPFARHC---VAL001]    Script Date: 07/23/2013 01:51:13 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[$database$---------001BMSHVAPFARHC---VAL001](
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
)WITH (PAD_INDEX  = OFF, STATISTICS_NORECOMPUTE  = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS  = ON, ALLOW_PAGE_LOCKS  = ON) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[$database$---------001BMSHVAPFARAT---VAL001]    Script Date: 07/23/2013 01:51:13 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[$database$---------001BMSHVAPFARAT---VAL001](
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
)WITH (PAD_INDEX  = OFF, STATISTICS_NORECOMPUTE  = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS  = ON, ALLOW_PAGE_LOCKS  = ON) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[$database$---------001BMSHVAPFALCP---VAL001]    Script Date: 07/23/2013 01:51:13 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[$database$---------001BMSHVAPFALCP---VAL001](
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
)WITH (PAD_INDEX  = OFF, STATISTICS_NORECOMPUTE  = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS  = ON, ALLOW_PAGE_LOCKS  = ON) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[$database$---------001BMSHVAPFACWV---VAL001]    Script Date: 07/23/2013 01:51:13 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[$database$---------001BMSHVAPFACWV---VAL001](
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
)WITH (PAD_INDEX  = OFF, STATISTICS_NORECOMPUTE  = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS  = ON, ALLOW_PAGE_LOCKS  = ON) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[$database$---------001BMSHVAMCT------ALA005]    Script Date: 07/23/2013 01:51:13 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[$database$---------001BMSHVAMCT------ALA005](
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
)WITH (PAD_INDEX  = OFF, STATISTICS_NORECOMPUTE  = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS  = ON, ALLOW_PAGE_LOCKS  = ON) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[$database$---------001BMSHVAMCT------ALA004]    Script Date: 07/23/2013 01:51:13 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[$database$---------001BMSHVAMCT------ALA004](
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
)WITH (PAD_INDEX  = OFF, STATISTICS_NORECOMPUTE  = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS  = ON, ALLOW_PAGE_LOCKS  = ON) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[$database$---------001BMSHVAMCT------ALA003]    Script Date: 07/23/2013 01:51:13 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[$database$---------001BMSHVAMCT------ALA003](
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
)WITH (PAD_INDEX  = OFF, STATISTICS_NORECOMPUTE  = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS  = ON, ALLOW_PAGE_LOCKS  = ON) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[$database$---------001BMSHVAMCT------ALA002]    Script Date: 07/23/2013 01:51:13 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[$database$---------001BMSHVAMCT------ALA002](
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
)WITH (PAD_INDEX  = OFF, STATISTICS_NORECOMPUTE  = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS  = ON, ALLOW_PAGE_LOCKS  = ON) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[$database$---------001BMSHVAMCT------ALA001]    Script Date: 07/23/2013 01:51:13 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[$database$---------001BMSHVAMCT------ALA001](
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
)WITH (PAD_INDEX  = OFF, STATISTICS_NORECOMPUTE  = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS  = ON, ALLOW_PAGE_LOCKS  = ON) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[$database$---------001BMSHVAFANSAT---VAL001]    Script Date: 07/23/2013 01:51:13 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[$database$---------001BMSHVAFANSAT---VAL001](
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
)WITH (PAD_INDEX  = OFF, STATISTICS_NORECOMPUTE  = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS  = ON, ALLOW_PAGE_LOCKS  = ON) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[$database$---------001BMSHVAFANSAT---SPV001]    Script Date: 07/23/2013 01:51:13 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[$database$---------001BMSHVAFANSAT---SPV001](
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
)WITH (PAD_INDEX  = OFF, STATISTICS_NORECOMPUTE  = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS  = ON, ALLOW_PAGE_LOCKS  = ON) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[$database$---------001BMSHVAFANRHC---VAL001]    Script Date: 07/23/2013 01:51:13 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[$database$---------001BMSHVAFANRHC---VAL001](
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
)WITH (PAD_INDEX  = OFF, STATISTICS_NORECOMPUTE  = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS  = ON, ALLOW_PAGE_LOCKS  = ON) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[$database$---------001BMSHVAFANRHC---SPV001]    Script Date: 07/23/2013 01:51:13 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[$database$---------001BMSHVAFANRHC---SPV001](
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
)WITH (PAD_INDEX  = OFF, STATISTICS_NORECOMPUTE  = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS  = ON, ALLOW_PAGE_LOCKS  = ON) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[$database$---------001BMSHVAFANRAT---VAL001]    Script Date: 07/23/2013 01:51:13 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[$database$---------001BMSHVAFANRAT---VAL001](
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
)WITH (PAD_INDEX  = OFF, STATISTICS_NORECOMPUTE  = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS  = ON, ALLOW_PAGE_LOCKS  = ON) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[$database$---------001BMSHVAFANLCP---VAL001]    Script Date: 07/23/2013 01:51:13 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[$database$---------001BMSHVAFANLCP---VAL001](
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
)WITH (PAD_INDEX  = OFF, STATISTICS_NORECOMPUTE  = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS  = ON, ALLOW_PAGE_LOCKS  = ON) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[$database$---------001BMSHVAFANCWV---VAL001]    Script Date: 07/23/2013 01:51:13 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[$database$---------001BMSHVAFANCWV---VAL001](
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
)WITH (PAD_INDEX  = OFF, STATISTICS_NORECOMPUTE  = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS  = ON, ALLOW_PAGE_LOCKS  = ON) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[$database$---------001BMSELEMET------VAL001]    Script Date: 07/23/2013 01:51:13 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[$database$---------001BMSELEMET------VAL001](
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
)WITH (PAD_INDEX  = OFF, STATISTICS_NORECOMPUTE  = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS  = ON, ALLOW_PAGE_LOCKS  = ON) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[$database$---------000TPOOPTTEMUPT001---001]    Script Date: 07/23/2013 01:51:13 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[$database$---------000TPOOPTTEMUPT001---001](
	[ID] [int] IDENTITY(1,1) NOT NULL,
	[Run_DateTime] [datetime] NULL,
	[Prediction_DateTime] [datetime] NULL,
 CONSTRAINT [PK_startup_time_rec] PRIMARY KEY CLUSTERED 
(
	[ID] ASC
)WITH (PAD_INDEX  = OFF, STATISTICS_NORECOMPUTE  = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS  = ON, ALLOW_PAGE_LOCKS  = ON) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[$database$---------000TPOOPTTEMRDW001---001]    Script Date: 07/23/2013 01:51:13 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[$database$---------000TPOOPTTEMRDW001---001](
	[ID] [int] IDENTITY(1,1) NOT NULL,
	[Run_DateTime] [datetime] NULL,
	[Prediction_DateTime] [datetime] NULL,
 CONSTRAINT [PK_rampdown_time_rec] PRIMARY KEY CLUSTERED 
(
	[ID] ASC
)WITH (PAD_INDEX  = OFF, STATISTICS_NORECOMPUTE  = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS  = ON, ALLOW_PAGE_LOCKS  = ON) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[$database$---------000TPONOWTEMSPA001---001]    Script Date: 07/23/2013 01:51:13 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[$database$---------000TPONOWTEMSPA001---001](
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
)WITH (PAD_INDEX  = OFF, STATISTICS_NORECOMPUTE  = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS  = ON, ALLOW_PAGE_LOCKS  = ON) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[$database$---------000TPOFORTEMSPA001---001_Stats_orig]    Script Date: 07/23/2013 01:51:13 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[$database$---------000TPOFORTEMSPA001---001_Stats_orig](
	[Prediction_Date] [datetime] NOT NULL,
	[Floor] [smallint] NOT NULL,
	[Quadrant] [nvarchar](2) NOT NULL,
	[RMSE] [float] NOT NULL,
	[MAE] [float] NOT NULL,
	[MAPE] [float] NOT NULL
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[$database$---------000TPOFORTEMSPA001---001_Stats]    Script Date: 07/23/2013 01:51:13 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[$database$---------000TPOFORTEMSPA001---001_Stats](
	[Prediction_Date] [datetime] NOT NULL,
	[Floor] [nvarchar](20) NOT NULL,
	[Quadrant] [nvarchar](20) NOT NULL,
	[RMSE] [float] NOT NULL,
	[MAE] [float] NOT NULL,
	[MAPE] [float] NOT NULL
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[$database$---------000TPOFORTEMSPA001---001_RBF_Params_orig]    Script Date: 07/23/2013 01:51:13 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[$database$---------000TPOFORTEMSPA001---001_RBF_Params_orig](
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
)WITH (PAD_INDEX  = OFF, STATISTICS_NORECOMPUTE  = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS  = ON, ALLOW_PAGE_LOCKS  = ON) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[$database$---------000TPOFORTEMSPA001---001_RBF_Params]    Script Date: 07/23/2013 01:51:13 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[$database$---------000TPOFORTEMSPA001---001_RBF_Params](
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
)WITH (PAD_INDEX  = OFF, STATISTICS_NORECOMPUTE  = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS  = ON, ALLOW_PAGE_LOCKS  = ON) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[$database$---------000TPOFORTEMSPA001---001_orig]    Script Date: 07/23/2013 01:51:13 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[$database$---------000TPOFORTEMSPA001---001_orig](
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
)WITH (PAD_INDEX  = OFF, STATISTICS_NORECOMPUTE  = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS  = ON, ALLOW_PAGE_LOCKS  = ON) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[$database$---------000TPOFORTEMSPA001---001_Derivative_orig]    Script Date: 07/23/2013 01:51:13 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[$database$---------000TPOFORTEMSPA001---001_Derivative_orig](
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
)WITH (PAD_INDEX  = OFF, STATISTICS_NORECOMPUTE  = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS  = ON, ALLOW_PAGE_LOCKS  = ON) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[$database$---------000TPOFORTEMSPA001---001_Derivative]    Script Date: 07/23/2013 01:51:13 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[$database$---------000TPOFORTEMSPA001---001_Derivative](
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
)WITH (PAD_INDEX  = OFF, STATISTICS_NORECOMPUTE  = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS  = ON, ALLOW_PAGE_LOCKS  = ON) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[$database$---------000TPOFORTEMSPA001---001_Deltas_orig]    Script Date: 07/23/2013 01:51:13 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[$database$---------000TPOFORTEMSPA001---001_Deltas_orig](
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
)WITH (PAD_INDEX  = OFF, STATISTICS_NORECOMPUTE  = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS  = ON, ALLOW_PAGE_LOCKS  = ON) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[$database$---------000TPOFORTEMSPA001---001_Deltas]    Script Date: 07/23/2013 01:51:13 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[$database$---------000TPOFORTEMSPA001---001_Deltas](
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
)WITH (PAD_INDEX  = OFF, STATISTICS_NORECOMPUTE  = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS  = ON, ALLOW_PAGE_LOCKS  = ON) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[$database$---------000TPOFORTEMSPA001---001]    Script Date: 07/23/2013 01:51:13 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[$database$---------000TPOFORTEMSPA001---001](
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
)WITH (PAD_INDEX  = OFF, STATISTICS_NORECOMPUTE  = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS  = ON, ALLOW_PAGE_LOCKS  = ON) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[$database$---------000TPOFORSTECON001---001_Stats]    Script Date: 07/23/2013 01:51:13 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[$database$---------000TPOFORSTECON001---001_Stats](
	[Prediction_Date] [datetime] NOT NULL,
	[RMSE] [float] NOT NULL,
	[MAE] [float] NOT NULL,
	[MAPE] [float] NOT NULL,
PRIMARY KEY CLUSTERED 
(
	[Prediction_Date] ASC
)WITH (PAD_INDEX  = OFF, STATISTICS_NORECOMPUTE  = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS  = ON, ALLOW_PAGE_LOCKS  = ON) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[$database$---------000TPOFORSTECON001---001_RBF_Params]    Script Date: 07/23/2013 01:51:13 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[$database$---------000TPOFORSTECON001---001_RBF_Params](
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
)WITH (PAD_INDEX  = OFF, STATISTICS_NORECOMPUTE  = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS  = ON, ALLOW_PAGE_LOCKS  = ON) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[$database$---------000TPOFORSTECON001---001]    Script Date: 07/23/2013 01:51:13 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[$database$---------000TPOFORSTECON001---001](
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
)WITH (PAD_INDEX  = OFF, STATISTICS_NORECOMPUTE  = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS  = ON, ALLOW_PAGE_LOCKS  = ON) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[$database$---------000TPOFORELECON001---001_stats]    Script Date: 07/23/2013 01:51:13 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[$database$---------000TPOFORELECON001---001_stats](
	[Prediction_Date] [datetime] NOT NULL,
	[RMSE] [float] NOT NULL,
	[MAE] [float] NOT NULL,
	[MAPE] [float] NOT NULL,
PRIMARY KEY CLUSTERED 
(
	[Prediction_Date] ASC
)WITH (PAD_INDEX  = OFF, STATISTICS_NORECOMPUTE  = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS  = ON, ALLOW_PAGE_LOCKS  = ON) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[$database$---------000TPOFORELECON001---001_RBF_Params]    Script Date: 07/23/2013 01:51:13 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[$database$---------000TPOFORELECON001---001_RBF_Params](
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
)WITH (PAD_INDEX  = OFF, STATISTICS_NORECOMPUTE  = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS  = ON, ALLOW_PAGE_LOCKS  = ON) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[$database$---------000TPOFORELECON001---001_NFL_stats]    Script Date: 07/23/2013 01:51:13 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[$database$---------000TPOFORELECON001---001_NFL_stats](
	[Prediction_Date] [datetime] NOT NULL,
	[RMSE] [float] NOT NULL,
	[MAE] [float] NOT NULL,
	[MAPE] [float] NOT NULL,
PRIMARY KEY CLUSTERED 
(
	[Prediction_Date] ASC
)WITH (PAD_INDEX  = OFF, STATISTICS_NORECOMPUTE  = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS  = ON, ALLOW_PAGE_LOCKS  = ON) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[$database$---------000TPOFORELECON001---001_NFL_RBF_Params]    Script Date: 07/23/2013 01:51:13 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[$database$---------000TPOFORELECON001---001_NFL_RBF_Params](
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
)WITH (PAD_INDEX  = OFF, STATISTICS_NORECOMPUTE  = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS  = ON, ALLOW_PAGE_LOCKS  = ON) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[$database$---------000TPOFORELECON001---001_NFL]    Script Date: 07/23/2013 01:51:13 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[$database$---------000TPOFORELECON001---001_NFL](
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
)WITH (PAD_INDEX  = OFF, STATISTICS_NORECOMPUTE  = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS  = ON, ALLOW_PAGE_LOCKS  = ON) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[$database$---------000TPOFORELECON001---001_KPMG_stats]    Script Date: 07/23/2013 01:51:13 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[$database$---------000TPOFORELECON001---001_KPMG_stats](
	[Prediction_Date] [datetime] NOT NULL,
	[RMSE] [float] NOT NULL,
	[MAE] [float] NOT NULL,
	[MAPE] [float] NOT NULL,
PRIMARY KEY CLUSTERED 
(
	[Prediction_Date] ASC
)WITH (PAD_INDEX  = OFF, STATISTICS_NORECOMPUTE  = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS  = ON, ALLOW_PAGE_LOCKS  = ON) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[$database$---------000TPOFORELECON001---001_KPMG_RBF_Params]    Script Date: 07/23/2013 01:51:13 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[$database$---------000TPOFORELECON001---001_KPMG_RBF_Params](
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
)WITH (PAD_INDEX  = OFF, STATISTICS_NORECOMPUTE  = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS  = ON, ALLOW_PAGE_LOCKS  = ON) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[$database$---------000TPOFORELECON001---001_KPMG]    Script Date: 07/23/2013 01:51:13 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[$database$---------000TPOFORELECON001---001_KPMG](
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
)WITH (PAD_INDEX  = OFF, STATISTICS_NORECOMPUTE  = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS  = ON, ALLOW_PAGE_LOCKS  = ON) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[$database$---------000TPOFORELECON001---001]    Script Date: 07/23/2013 01:51:13 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[$database$---------000TPOFORELECON001---001](
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
)WITH (PAD_INDEX  = OFF, STATISTICS_NORECOMPUTE  = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS  = ON, ALLOW_PAGE_LOCKS  = ON) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[$database$---------000TPO---ALA---001]    Script Date: 07/23/2013 01:51:13 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
SET ANSI_PADDING ON
GO
CREATE TABLE [dbo].[$database$---------000TPO---ALA---001](
	[ID] [int] IDENTITY(1,1) NOT NULL,
	[STATE] [int] NULL,
	[PROPERTY_PRIO] [int] NULL,
	[INTERNAL] [int] NULL,
	[INITTS] [datetime] NULL,
	[NORMTS] [datetime] NULL,
	[PBS] [varchar](10) NULL,
	[SIGN] [varchar](100) NULL,
 CONSTRAINT [PK_$database$---------000TPO---ALA---001] PRIMARY KEY CLUSTERED 
(
	[ID] ASC
)WITH (PAD_INDEX  = OFF, STATISTICS_NORECOMPUTE  = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS  = ON, ALLOW_PAGE_LOCKS  = ON) ON [PRIMARY]
) ON [PRIMARY]
GO
SET ANSI_PADDING OFF
GO
/****** Object:  Table [dbo].[$database$---------000SECCNTPEOBUI---VAL001]    Script Date: 07/23/2013 01:51:13 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[$database$---------000SECCNTPEOBUI---VAL001](
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
)WITH (PAD_INDEX  = OFF, STATISTICS_NORECOMPUTE  = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS  = ON, ALLOW_PAGE_LOCKS  = ON) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[$database$---------000SECCNTPEOBUI---OUT001]    Script Date: 07/23/2013 01:51:13 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[$database$---------000SECCNTPEOBUI---OUT001](
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
)WITH (PAD_INDEX  = OFF, STATISTICS_NORECOMPUTE  = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS  = ON, ALLOW_PAGE_LOCKS  = ON) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[$database$---------000SECCNTPEOBUI---INC001]    Script Date: 07/23/2013 01:51:13 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[$database$---------000SECCNTPEOBUI---INC001](
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
)WITH (PAD_INDEX  = OFF, STATISTICS_NORECOMPUTE  = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS  = ON, ALLOW_PAGE_LOCKS  = ON) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[$database$---------000ACS---TUROUT---OUT001]    Script Date: 07/23/2013 01:51:13 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[$database$---------000ACS---TUROUT---OUT001](
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
)WITH (PAD_INDEX  = OFF, STATISTICS_NORECOMPUTE  = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS  = ON, ALLOW_PAGE_LOCKS  = ON) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[$database$---------000ACS---TURINC---IN001]    Script Date: 07/23/2013 01:51:13 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[$database$---------000ACS---TURINC---IN001](
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
)WITH (PAD_INDEX  = OFF, STATISTICS_NORECOMPUTE  = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS  = ON, ALLOW_PAGE_LOCKS  = ON) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[$database$_floor_zone_map]    Script Date: 07/23/2013 01:51:13 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[$database$_floor_zone_map](
	[FLOOR] [nvarchar](4) NOT NULL,
	[ZONE] [smallint] NOT NULL
) ON [PRIMARY]
GO
/****** Object:  View [dbo].[Space_Temp_Prediction]    Script Date: 07/23/2013 01:51:14 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE VIEW [dbo].[Space_Temp_Prediction]
AS
SELECT     dbo.[$database$---------000TPOFORTEMSPA001---001].*, dbo.[$database$_floor_zone_map].ZONE
FROM         dbo.[$database$_floor_zone_map] INNER JOIN
                      dbo.[$database$---------000TPOFORTEMSPA001---001] ON dbo.[$database$_floor_zone_map].FLOOR = dbo.[$database$---------000TPOFORTEMSPA001---001].Floor

--SELECT     Run_DateTime, Prediction_DateTime, Floor, Quadrant, Prediction_Value, Lower_Bound_95, Upper_Bound_95, Lower_Bound_68, Upper_Bound_68, ID
--FROM         dbo.[$database$---------000TPOFORTEMSPA001---001] AS a
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

/****** Object:  View [dbo].[Space_Temp_Comp2]    Script Date: 07/23/2013 01:51:14 ******/
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
                       FROM          dbo.[$database$---------000TPOFORTEMSPA001---001_orig] AS s INNER JOIN
                                              dbo.Floor_Mapping AS f ON s.Floor = f.Floor) AS a INNER JOIN
                      dbo.Quadrant_Mapping AS q ON a.Quadrant = q.Quadrant
GO

/****** Object:  View [dbo].[Space_Temp_Comp]    Script Date: 07/23/2013 01:51:14 ******/
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
                       FROM          dbo.[$database$---------000TPOFORTEMSPA001---001] AS s INNER JOIN
                                              dbo.Floor_Mapping AS f ON s.Floor = f.Floor) AS a INNER JOIN
                      dbo.Quadrant_Mapping AS q ON a.Quadrant = q.Quadrant
GO
