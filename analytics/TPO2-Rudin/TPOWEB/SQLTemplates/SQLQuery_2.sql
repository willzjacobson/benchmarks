USE [TPOWEB]
GO

SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE VIEW [dbo].[005_ALEVELMETERALLKW]
AS

SELECT TOP (100) PERCENT CONVERT(SMALLDATETIME, [TIMESTAMP]) AS TIMESTAMP, SUM([VALUE]) AS VALUE
    FROM  (select distinct timestamp, equipment_no, value from [641].dbo.[641---------005BMSELEMET------VAL001]) t 
    GROUP BY CONVERT(SMALLDATETIME, [TIMESTAMP])
    ORDER BY TIMESTAMP DESC

Go

CREATE VIEW [dbo].[005_ALEVELMETERALLKW_UNION]
AS
SELECT [TIMESTAMP]
      ,[VALUE]
  FROM [641].dbo.[641---------005BMSELEMET------VAL001] WHERE EQUIPMENT_NO IN ('001', '002')

Go

CREATE VIEW [dbo].[005_Prediction_Electricity]
AS
SELECT t1.Prediction_DateTime AS TIMESTAMP, t1.Prediction_Value AS Prediction, t1.Lower_Bound_95, t1.Upper_Bound_95, 
                      t1.Lower_Bound_68, t1.Upper_Bound_68
  FROM 
	(SELECT * FROM
	[641].dbo.[641---------000TPOFORELECON001---001]
	) t1

  INNER JOIN

	(SELECT MAX([Run_DateTime]) Run_DateTime, [Prediction_DateTime]
	FROM [641].dbo.[641---------000TPOFORELECON001---001]
	
	GROUP BY Prediction_DateTime) t2

  ON t1.Prediction_DateTime = t2.Prediction_DateTime AND t1.Run_DateTime = t2.Run_DateTime

Go

CREATE VIEW [dbo].[005_Prediction_Steam]
AS
SELECT t1.Prediction_DateTime AS TIMESTAMP, t1.Prediction_Value AS Prediction, t1.Lower_Bound_95, t1.Upper_Bound_95, 
                      t1.Lower_Bound_68, t1.Upper_Bound_68
  FROM 
	(SELECT * FROM
	[641].dbo.[641---------000TPOFORSTECON001---001]
	) t1

  INNER JOIN

	(SELECT MAX([Run_DateTime]) Run_DateTime, [Prediction_DateTime]
	FROM [641].dbo.[641---------000TPOFORSTECON001---001]
	
	GROUP BY Prediction_DateTime) t2

  ON t1.Prediction_DateTime = t2.Prediction_DateTime AND t1.Run_DateTime = t2.Run_DateTime

Go

CREATE VIEW [dbo].[005_Prediction_Occupancy]
AS
SELECT t1.Prediction_DateTime AS TIMESTAMP, t1.Prediction_Value AS Prediction, t1.Lower_Bound_95, t1.Upper_Bound_95, 
                      t1.Lower_Bound_68, t1.Upper_Bound_68
  FROM 
	(SELECT * FROM
	[641].dbo.[641---------000TPOFORPEOBUI001---001]
	) t1

  INNER JOIN

	(SELECT MAX([Run_DateTime]) Run_DateTime, [Prediction_DateTime]
	FROM [641].dbo.[641---------000TPOFORPEOBUI001---001]
	
	GROUP BY Prediction_DateTime) t2

  ON t1.Prediction_DateTime = t2.Prediction_DateTime AND t1.Run_DateTime = t2.Run_DateTime

Go


CREATE VIEW [dbo].[005_Prediction_Ramp_Down_Time_Rec]
AS
SELECT     Run_DateTime, Prediction_DateTime, DATEADD(dd, 0, DATEDIFF(dd, 0, Prediction_DateTime)) AS Prediction_Day
FROM        [641].dbo.[641---------000TPOOPTTEMRDW001---001]

Go

CREATE VIEW [dbo].[005_Prediction_Ramp_Down_Time]
AS
SELECT     t1.Prediction_Day, t1.Prediction_DateTime AS TIMESTAMP
FROM         (SELECT     Run_DateTime, Prediction_Day, Prediction_DateTime
                       FROM          dbo.[005_Prediction_Ramp_Down_Time_Rec]) AS t1 INNER JOIN
                          (SELECT     MAX(Run_DateTime) AS Run_DateTime, Prediction_Day
                            FROM          dbo.[005_Prediction_Ramp_Down_Time_Rec] AS Prediction_Ramp_Down_Time_Rec_1
                            GROUP BY Prediction_Day) AS t2 ON t1.Prediction_Day = t2.Prediction_Day AND t1.Run_DateTime = t2.Run_DateTime

Go

CREATE VIEW [dbo].[005_Prediction_Start_Up_Time_Rec]
AS
SELECT     Run_DateTime, Prediction_DateTime, DATEADD(dd, 0, DATEDIFF(dd, 0, Prediction_DateTime)) AS Prediction_Day
FROM         [641].dbo.[641---------000TPOOPTTEMUPT001---001]


Go

CREATE VIEW [dbo].[005_Prediction_Start_Up_Time]
AS
SELECT     t1.Prediction_Day, t1.Prediction_DateTime AS TIMESTAMP
FROM         (SELECT     Run_DateTime, Prediction_Day, Prediction_DateTime
                       FROM          dbo.[005_Prediction_Start_Up_Time_Rec]) AS t1 INNER JOIN
                          (SELECT     MAX(Run_DateTime) AS Run_DateTime, Prediction_Day
                            FROM          dbo.[005_Prediction_Start_Up_Time_Rec] AS Prediction_Start_Up_Time_Rec_1
                            GROUP BY Prediction_Day) AS t2 ON t1.Prediction_Day = t2.Prediction_Day AND t1.Run_DateTime = t2.Run_DateTime


Go


