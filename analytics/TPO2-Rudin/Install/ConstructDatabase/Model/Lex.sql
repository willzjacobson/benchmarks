USE [$database$]
GO

/****** Object:  User [rudin_db_reader]    Script Date: 07/23/2013 01:14:38 ******/
CREATE USER [rudin_db_reader] FOR LOGIN [rudin_db_reader] WITH DEFAULT_SCHEMA=[dbo]
GO
/****** Object:  User [rudin_user]    Script Date: 07/23/2013 01:14:38 ******/
CREATE USER [rudin_user] FOR LOGIN [rudin_user] WITH DEFAULT_SCHEMA=[dbo]
GO
/****** Object:  User [rudin_user2]    Script Date: 07/23/2013 01:14:38 ******/
CREATE USER [rudin_user2] FOR LOGIN [rudin_user2] WITH DEFAULT_SCHEMA=[dbo]
GO
/****** Object:  User [tpo]    Script Date: 07/23/2013 01:14:38 ******/
CREATE USER [tpo] FOR LOGIN [tpo] WITH DEFAULT_SCHEMA=[dbo]
GO
/****** Object:  User [TPOWEB_USER]    Script Date: 07/23/2013 01:14:38 ******/
CREATE USER [TPOWEB_USER] FOR LOGIN [TPOWEB_USER] WITH DEFAULT_SCHEMA=[dbo]
GO
/****** Object:  Table [dbo].[Ramp_Down_Time_DS]    Script Date: 07/23/2013 01:14:38 ******/
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
/****** Object:  Table [dbo].[Quadrant_Mapping]    Script Date: 07/23/2013 01:14:38 ******/
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
/****** Object:  Table [dbo].[Floor_Mapping]    Script Date: 07/23/2013 01:14:38 ******/
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
/****** Object:  Table [dbo].[$database$---------002BMSWATHOT------VAL001]    Script Date: 07/23/2013 01:14:38 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[$database$---------002BMSWATHOT------VAL001](
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
/****** Object:  Table [dbo].[$database$---------002BMSWATCHITEM---VAL001]    Script Date: 07/23/2013 01:14:38 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[$database$---------002BMSWATCHITEM---VAL001](
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
/****** Object:  Table [dbo].[$database$---------002BMSWATCHISUP---VAL001]    Script Date: 07/23/2013 01:14:38 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[$database$---------002BMSWATCHISUP---VAL001](
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
/****** Object:  Table [dbo].[$database$---------002BMSWATCHIRET---VAL001]    Script Date: 07/23/2013 01:14:38 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[$database$---------002BMSWATCHIRET---VAL001](
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
/****** Object:  Table [dbo].[$database$---------002BMSWATCHIHUM---VAL001]    Script Date: 07/23/2013 01:14:38 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[$database$---------002BMSWATCHIHUM---VAL001](
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
/****** Object:  Table [dbo].[$database$---------002BMSHVATEMSPA---VAL001]    Script Date: 07/23/2013 01:14:38 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[$database$---------002BMSHVATEMSPA---VAL001](
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
/****** Object:  Table [dbo].[$database$---------002BMSHVAFAN------VAL001]    Script Date: 07/23/2013 01:14:38 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[$database$---------002BMSHVAFAN------VAL001](
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
/****** Object:  Table [dbo].[$database$---------002BMSHVAFANSAT---VAL001]    Script Date: 07/23/2013 01:14:38 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[$database$---------002BMSHVAFANSAT---VAL001](
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
/****** Object:  Table [dbo].[$database$---------002BMSHVAFANRAT---VAL001]    Script Date: 07/23/2013 01:14:38 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[$database$---------002BMSHVAFANRAT---VAL001](
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
/****** Object:  Table [dbo].[$database$---------002BMSELEMET------VAL001]    Script Date: 07/23/2013 01:14:38 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[$database$---------002BMSELEMET------VAL001](
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
/****** Object:  Table [dbo].[$database$---------000TPOOPTTEMUPT001---001]    Script Date: 07/23/2013 01:14:38 ******/
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
/****** Object:  Table [dbo].[$database$---------000TPOOPTTEMRDW001---001]    Script Date: 07/23/2013 01:14:38 ******/
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
/****** Object:  Table [dbo].[$database$---------000TPONOWTEMSPA001---001]    Script Date: 07/23/2013 01:14:38 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[$database$---------000TPONOWTEMSPA001---001](
	[Run_DateTime] [datetime] NOT NULL,
	[Prediction_DateTime] [datetime] NOT NULL,
	[Value] [real] NULL,
	[Floor] [nchar](3) NOT NULL,
	[Quadrant] [nchar](3) NOT NULL,
	[Prediction_Timestep] [int] NOT NULL,
	[ID] [int] IDENTITY(1,1) NOT NULL,
	[Control_Setting] [float] NULL,
 CONSTRAINT [PK_$database$---------000TPONOWTEMSPA001---001] PRIMARY KEY CLUSTERED 
(
	[Run_DateTime] ASC,
	[Prediction_DateTime] ASC,
	[Floor] ASC,
	[Quadrant] ASC
)WITH (PAD_INDEX  = OFF, STATISTICS_NORECOMPUTE  = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS  = ON, ALLOW_PAGE_LOCKS  = ON) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[$database$---------000TPOFORTEMSPA001---001_Stats]    Script Date: 07/23/2013 01:14:38 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[$database$---------000TPOFORTEMSPA001---001_Stats](
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
)WITH (PAD_INDEX  = OFF, STATISTICS_NORECOMPUTE  = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS  = ON, ALLOW_PAGE_LOCKS  = ON) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[$database$---------000TPOFORTEMSPA001---001_RBF_Params]    Script Date: 07/23/2013 01:14:38 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[$database$---------000TPOFORTEMSPA001---001_RBF_Params](
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
)WITH (PAD_INDEX  = OFF, STATISTICS_NORECOMPUTE  = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS  = ON, ALLOW_PAGE_LOCKS  = ON) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[$database$---------000TPOFORTEMSPA001---001_orig]    Script Date: 07/23/2013 01:14:38 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[$database$---------000TPOFORTEMSPA001---001_orig](
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
)WITH (PAD_INDEX  = OFF, STATISTICS_NORECOMPUTE  = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS  = ON, ALLOW_PAGE_LOCKS  = ON) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[$database$---------000TPOFORTEMSPA001---001_Derivative]    Script Date: 07/23/2013 01:14:38 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[$database$---------000TPOFORTEMSPA001---001_Derivative](
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
)WITH (PAD_INDEX  = OFF, STATISTICS_NORECOMPUTE  = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS  = ON, ALLOW_PAGE_LOCKS  = ON) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[$database$---------000TPOFORTEMSPA001---001_Deltas]    Script Date: 07/23/2013 01:14:38 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[$database$---------000TPOFORTEMSPA001---001_Deltas](
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
)WITH (PAD_INDEX  = OFF, STATISTICS_NORECOMPUTE  = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS  = ON, ALLOW_PAGE_LOCKS  = ON) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[$database$---------000TPOFORTEMSPA001---001]    Script Date: 07/23/2013 01:14:38 ******/
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
/****** Object:  Table [dbo].[$database$---------000TPOFORELECON001---001_Stats]    Script Date: 07/23/2013 01:14:38 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[$database$---------000TPOFORELECON001---001_Stats](
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
/****** Object:  Table [dbo].[$database$---------000TPOFORELECON001---001_RBF_Params]    Script Date: 07/23/2013 01:14:38 ******/
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
/****** Object:  Table [dbo].[$database$---------000TPOFORELECON001---001]    Script Date: 07/23/2013 01:14:38 ******/
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
 CONSTRAINT [PK__Electric__B1D96F1829572725] PRIMARY KEY CLUSTERED 
(
	[Run_DateTime] ASC,
	[Prediction_DateTime] ASC
)WITH (PAD_INDEX  = OFF, STATISTICS_NORECOMPUTE  = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS  = ON, ALLOW_PAGE_LOCKS  = ON) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[$database$---------000TPO---ALA---001]    Script Date: 07/23/2013 01:14:38 ******/
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
/****** Object:  Table [dbo].[$database$---------000SECCNTPEOBUI---VAL001]    Script Date: 07/23/2013 01:14:38 ******/
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
/****** Object:  Table [dbo].[$database$---------000SECCNTPEOBUI---OUT001]    Script Date: 07/23/2013 01:14:38 ******/
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
/****** Object:  Table [dbo].[$database$---------000SECCNTPEOBUI---INC001]    Script Date: 07/23/2013 01:14:38 ******/
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
/****** Object:  Table [dbo].[$database$---------000ACS---TUROUT---OUT001]    Script Date: 07/23/2013 01:14:38 ******/
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
/****** Object:  Table [dbo].[$database$---------000ACS---TURINC---IN001]    Script Date: 07/23/2013 01:14:38 ******/
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
/****** Object:  View [dbo].[Space_Temp_Prediction]    Script Date: 07/23/2013 01:14:38 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE VIEW [dbo].[Space_Temp_Prediction]
AS
SELECT     Run_DateTime, Prediction_DateTime, Floor, Prediction_Value, Lower_Bound_95, Upper_Bound_95, Lower_Bound_68, Upper_Bound_68, ID
FROM         dbo.[$database$---------000TPOFORTEMSPA001---001]
GO

/****** Object:  View [dbo].[Space_Temp_Comp]    Script Date: 07/23/2013 01:14:38 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE VIEW [dbo].[Space_Temp_Comp]
AS
SELECT     s.Run_DateTime, s.Prediction_DateTime, f.CompFloor AS Floor, s.Prediction_Value, s.Lower_Bound_95, s.Upper_Bound_95, s.Lower_Bound_68, s.Upper_Bound_68, 
                      s.ID
FROM         dbo.[$database$---------000TPOFORTEMSPA001---001_orig] AS s INNER JOIN
                      dbo.Floor_Mapping AS f ON s.Floor = f.Floor
GO

