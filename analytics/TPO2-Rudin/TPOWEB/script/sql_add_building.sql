USE [TPOWEB_TEST]
GO

SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE VIEW [dbo].[005_Actual_Space_Temperature_2_CSO]
AS
SELECT [ZONE]
      ,[FLOOR]
      ,[QUADRANT]
      ,[EQUIPMENT_NO]
      ,[TIMESTAMP]
      ,[VALUE]
  FROM [641].[dbo].[641---------005BMSHVATEMSPA---VAL001]
  WHERE [FLOOR] = 'F02' AND [QUADRANT] = 'CSO'
  Go
  
CREATE VIEW [dbo].[005_Actual_Space_Temperature_6_CWE]
AS
SELECT [ZONE]
      ,[FLOOR]
      ,[QUADRANT]
      ,[EQUIPMENT_NO]
      ,[TIMESTAMP]
      ,[VALUE]
  FROM [641].[dbo].[641---------005BMSHVATEMSPA---VAL001]
  WHERE [FLOOR] = 'F06' AND [QUADRANT] = 'CWE'
  
    Go
    
CREATE VIEW [dbo].[005_Actual_Space_Temperature_10_CWE]
AS
SELECT [ZONE]
      ,[FLOOR]
      ,[QUADRANT]
      ,[EQUIPMENT_NO]
      ,[TIMESTAMP]
      ,[VALUE]
  FROM [641].[dbo].[641---------005BMSHVATEMSPA---VAL001]
  WHERE [FLOOR] = 'F10' AND [QUADRANT] = 'CWE'
  
  Go
  
CREATE VIEW [dbo].[005_Actual_Space_Temperature_15_CNO]
AS
SELECT [ZONE]
      ,[FLOOR]
      ,[QUADRANT]
      ,[EQUIPMENT_NO]
      ,[TIMESTAMP]
      ,[VALUE]
  FROM [641].[dbo].[641---------005BMSHVATEMSPA---VAL001]
  WHERE [FLOOR] = 'F15' AND [QUADRANT] = 'CNO'
  
      Go
  
CREATE VIEW [dbo].[005_Actual_Space_Temperature_15_CWE]
AS
SELECT [ZONE]
      ,[FLOOR]
      ,[QUADRANT]
      ,[EQUIPMENT_NO]
      ,[TIMESTAMP]
      ,[VALUE]
  FROM [641].[dbo].[641---------005BMSHVATEMSPA---VAL001]
  WHERE [FLOOR] = 'F15' AND [QUADRANT] = 'CWE'
  
      Go
  
CREATE VIEW [dbo].[005_Actual_Space_Temperature_28_CSO]
AS
SELECT [ZONE]
      ,[FLOOR]
      ,[QUADRANT]
      ,[EQUIPMENT_NO]
      ,[TIMESTAMP]
      ,[VALUE]
  FROM [641].[dbo].[641---------005BMSHVATEMSPA---VAL001]
  WHERE [FLOOR] = 'F28' AND [QUADRANT] = 'CSO'
  
      Go
  
CREATE VIEW [dbo].[005_Actual_Space_Temperature_28_CNO]
AS
SELECT [ZONE]
      ,[FLOOR]
      ,[QUADRANT]
      ,[EQUIPMENT_NO]
      ,[TIMESTAMP]
      ,[VALUE]
  FROM [641].[dbo].[641---------005BMSHVATEMSPA---VAL001]
  WHERE [FLOOR] = 'F28' AND [QUADRANT] = 'CNO'
  
      Go
  
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

USE [TPOWEB]
GO

SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE VIEW [dbo].[005_Prediction_Space_Temperature_2_CSO]
AS
SELECT     TOP (100) PERCENT t1.Prediction_DateTime, t1.Prediction_Value, t1.Lower_Bound_95, t1.Upper_Bound_95, t1.Lower_Bound_68, 
                      t1.Upper_Bound_68
FROM         [641].dbo.[641---------000TPOHVATEMSPA001---001] AS t1 INNER JOIN
                          (SELECT     MAX(Run_DateTime) AS Run_DateTime, Prediction_DateTime
                            FROM          [641].dbo.[641---------000TPOHVATEMSPA001---001]
                            GROUP BY Prediction_DateTime) AS t2 ON t1.Run_DateTime = t2.Run_DateTime AND t1.Prediction_DateTime = t2.Prediction_DateTime
WHERE     (t1.Floor = 'F02' AND t1.Quadrant = 'CSO') 
ORDER BY t1.Prediction_DateTime

Go

CREATE VIEW [dbo].[005_Prediction_Space_Temperature_2_CSO_Derivative]
AS
SELECT     t1.Run_DateTime, t1.Prediction_DateTime, t1.Floor, t1.Value
FROM         (SELECT     Run_DateTime, Prediction_DateTime, Floor, Value
                       FROM         [641].dbo.[641---------000TPONOWTEMSPA001---001]
                       WHERE      (Floor = 'F02' AND Quadrant = 'CSO')) AS t1 INNER JOIN
                          (SELECT     MAX(Run_DateTime) AS Run_DateTime, Prediction_DateTime
                            FROM          [641].dbo.[641---------000TPONOWTEMSPA001---001] AS Derivative_1
                            WHERE      (Floor = 'F02' AND Quadrant = 'CSO')
                            GROUP BY Prediction_DateTime) AS t2 ON t1.Prediction_DateTime = t2.Prediction_DateTime AND t1.Run_DateTime = t2.Run_DateTime

GO

CREATE VIEW [dbo].[005_Prediction_Space_Temperature_2_CSO_Start]
AS
SELECT     TOP (1) TIMESTAMP, VALUE
FROM         [TPOWEB].[dbo].[005_Actual_Space_Temperature_2_CSO]
ORDER BY TIMESTAMP DESC

GO

CREATE VIEW [dbo].[005_Prediction_Space_Temperature_2_CSO_End]
AS
SELECT     TOP (7) Prediction_DateTime AS TIMESTAMP, Value
FROM         dbo.[005_Prediction_Space_Temperature_2_CSO_Derivative]
ORDER BY TIMESTAMP DESC

Go



CREATE VIEW [dbo].[005_Prediction_Space_Temperature_6_CWE]
AS
SELECT     TOP (100) PERCENT t1.Prediction_DateTime, t1.Prediction_Value, t1.Lower_Bound_95, t1.Upper_Bound_95, t1.Lower_Bound_68, 
                      t1.Upper_Bound_68
FROM         [641].dbo.[641---------000TPOHVATEMSPA001---001] AS t1 INNER JOIN
                          (SELECT     MAX(Run_DateTime) AS Run_DateTime, Prediction_DateTime
                            FROM          [641].dbo.[641---------000TPOHVATEMSPA001---001]
                            GROUP BY Prediction_DateTime) AS t2 ON t1.Run_DateTime = t2.Run_DateTime AND t1.Prediction_DateTime = t2.Prediction_DateTime
WHERE     (t1.Floor = 'F06' AND t1.Quadrant = 'CWE') 
ORDER BY t1.Prediction_DateTime

Go

CREATE VIEW [dbo].[005_Prediction_Space_Temperature_6_CWE_Derivative]
AS
SELECT     t1.Run_DateTime, t1.Prediction_DateTime, t1.Floor, t1.Value
FROM         (SELECT     Run_DateTime, Prediction_DateTime, Floor, Value
                       FROM         [641].dbo.[641---------000TPONOWTEMSPA001---001]
                       WHERE      (Floor = 'F06' AND Quadrant = 'CWE')) AS t1 INNER JOIN
                          (SELECT     MAX(Run_DateTime) AS Run_DateTime, Prediction_DateTime
                            FROM          [641].dbo.[641---------000TPONOWTEMSPA001---001] AS Derivative_1
                            WHERE      (Floor = 'F06' AND Quadrant = 'CWE')
                            GROUP BY Prediction_DateTime) AS t2 ON t1.Prediction_DateTime = t2.Prediction_DateTime AND t1.Run_DateTime = t2.Run_DateTime

GO

CREATE VIEW [dbo].[005_Prediction_Space_Temperature_6_CWE_Start]
AS
SELECT     TOP (1) TIMESTAMP, VALUE
FROM         [TPOWEB].[dbo].[005_Actual_Space_Temperature_6_CWE]
ORDER BY TIMESTAMP DESC

GO

CREATE VIEW [dbo].[005_Prediction_Space_Temperature_6_CWE_End]
AS
SELECT     TOP (7) Prediction_DateTime AS TIMESTAMP, Value
FROM         dbo.[005_Prediction_Space_Temperature_6_CWE_Derivative]
ORDER BY TIMESTAMP DESC

Go


CREATE VIEW [dbo].[005_Prediction_Space_Temperature_10_CWE]
AS
SELECT     TOP (100) PERCENT t1.Prediction_DateTime, t1.Prediction_Value, t1.Lower_Bound_95, t1.Upper_Bound_95, t1.Lower_Bound_68, 
                      t1.Upper_Bound_68
FROM         [641].dbo.[641---------000TPOHVATEMSPA001---001] AS t1 INNER JOIN
                          (SELECT     MAX(Run_DateTime) AS Run_DateTime, Prediction_DateTime
                            FROM          [641].dbo.[641---------000TPOHVATEMSPA001---001]
                            GROUP BY Prediction_DateTime) AS t2 ON t1.Run_DateTime = t2.Run_DateTime AND t1.Prediction_DateTime = t2.Prediction_DateTime
WHERE     (t1.Floor = 'F10' AND t1.Quadrant = 'CWE') 
ORDER BY t1.Prediction_DateTime

Go

CREATE VIEW [dbo].[005_Prediction_Space_Temperature_10_CWE_Derivative]
AS
SELECT     t1.Run_DateTime, t1.Prediction_DateTime, t1.Floor, t1.Value
FROM         (SELECT     Run_DateTime, Prediction_DateTime, Floor, Value
                       FROM         [641].dbo.[641---------000TPONOWTEMSPA001---001]
                       WHERE      (Floor = 'F10' AND Quadrant = 'CWE')) AS t1 INNER JOIN
                          (SELECT     MAX(Run_DateTime) AS Run_DateTime, Prediction_DateTime
                            FROM          [641].dbo.[641---------000TPONOWTEMSPA001---001] AS Derivative_1
                            WHERE      (Floor = 'F10' AND Quadrant = 'CWE')
                            GROUP BY Prediction_DateTime) AS t2 ON t1.Prediction_DateTime = t2.Prediction_DateTime AND t1.Run_DateTime = t2.Run_DateTime

GO

CREATE VIEW [dbo].[005_Prediction_Space_Temperature_10_CWE_Start]
AS
SELECT     TOP (1) TIMESTAMP, VALUE
FROM         [TPOWEB].[dbo].[005_Actual_Space_Temperature_10_CWE]
ORDER BY TIMESTAMP DESC

GO

CREATE VIEW [dbo].[005_Prediction_Space_Temperature_10_CWE_End]
AS
SELECT     TOP (7) Prediction_DateTime AS TIMESTAMP, Value
FROM         dbo.[005_Prediction_Space_Temperature_10_CWE_Derivative]
ORDER BY TIMESTAMP DESC

Go


CREATE VIEW [dbo].[005_Prediction_Space_Temperature_15_CNO]
AS
SELECT     TOP (100) PERCENT t1.Prediction_DateTime, t1.Prediction_Value, t1.Lower_Bound_95, t1.Upper_Bound_95, t1.Lower_Bound_68, 
                      t1.Upper_Bound_68
FROM         [641].dbo.[641---------000TPOHVATEMSPA001---001] AS t1 INNER JOIN
                          (SELECT     MAX(Run_DateTime) AS Run_DateTime, Prediction_DateTime
                            FROM          [641].dbo.[641---------000TPOHVATEMSPA001---001]
                            GROUP BY Prediction_DateTime) AS t2 ON t1.Run_DateTime = t2.Run_DateTime AND t1.Prediction_DateTime = t2.Prediction_DateTime
WHERE     (t1.Floor = 'F15' AND t1.Quadrant = 'CNO') 
ORDER BY t1.Prediction_DateTime

Go

CREATE VIEW [dbo].[005_Prediction_Space_Temperature_15_CNO_Derivative]
AS
SELECT     t1.Run_DateTime, t1.Prediction_DateTime, t1.Floor, t1.Value
FROM         (SELECT     Run_DateTime, Prediction_DateTime, Floor, Value
                       FROM         [641].dbo.[641---------000TPONOWTEMSPA001---001]
                       WHERE      (Floor = 'F15' AND Quadrant = 'CNO')) AS t1 INNER JOIN
                          (SELECT     MAX(Run_DateTime) AS Run_DateTime, Prediction_DateTime
                            FROM          [641].dbo.[641---------000TPONOWTEMSPA001---001] AS Derivative_1
                            WHERE      (Floor = 'F15' AND Quadrant = 'CNO')
                            GROUP BY Prediction_DateTime) AS t2 ON t1.Prediction_DateTime = t2.Prediction_DateTime AND t1.Run_DateTime = t2.Run_DateTime

GO

CREATE VIEW [dbo].[005_Prediction_Space_Temperature_15_CNO_Start]
AS
SELECT     TOP (1) TIMESTAMP, VALUE
FROM         [TPOWEB].[dbo].[005_Actual_Space_Temperature_15_CNO]
ORDER BY TIMESTAMP DESC

GO

CREATE VIEW [dbo].[005_Prediction_Space_Temperature_15_CNO_End]
AS
SELECT     TOP (7) Prediction_DateTime AS TIMESTAMP, Value
FROM         dbo.[005_Prediction_Space_Temperature_15_CNO_Derivative]
ORDER BY TIMESTAMP DESC

Go


CREATE VIEW [dbo].[005_Prediction_Space_Temperature_15_CWE]
AS
SELECT     TOP (100) PERCENT t1.Prediction_DateTime, t1.Prediction_Value, t1.Lower_Bound_95, t1.Upper_Bound_95, t1.Lower_Bound_68, 
                      t1.Upper_Bound_68
FROM         [641].dbo.[641---------000TPOHVATEMSPA001---001] AS t1 INNER JOIN
                          (SELECT     MAX(Run_DateTime) AS Run_DateTime, Prediction_DateTime
                            FROM          [641].dbo.[641---------000TPOHVATEMSPA001---001]
                            GROUP BY Prediction_DateTime) AS t2 ON t1.Run_DateTime = t2.Run_DateTime AND t1.Prediction_DateTime = t2.Prediction_DateTime
WHERE     (t1.Floor = 'F15' AND t1.Quadrant = 'CWE') 
ORDER BY t1.Prediction_DateTime

Go

CREATE VIEW [dbo].[005_Prediction_Space_Temperature_15_CWE_Derivative]
AS
SELECT     t1.Run_DateTime, t1.Prediction_DateTime, t1.Floor, t1.Value
FROM         (SELECT     Run_DateTime, Prediction_DateTime, Floor, Value
                       FROM         [641].dbo.[641---------000TPONOWTEMSPA001---001]
                       WHERE      (Floor = 'F15' AND Quadrant = 'CWE')) AS t1 INNER JOIN
                          (SELECT     MAX(Run_DateTime) AS Run_DateTime, Prediction_DateTime
                            FROM          [641].dbo.[641---------000TPONOWTEMSPA001---001] AS Derivative_1
                            WHERE      (Floor = 'F15' AND Quadrant = 'CWE')
                            GROUP BY Prediction_DateTime) AS t2 ON t1.Prediction_DateTime = t2.Prediction_DateTime AND t1.Run_DateTime = t2.Run_DateTime

GO

CREATE VIEW [dbo].[005_Prediction_Space_Temperature_15_CWE_Start]
AS
SELECT     TOP (1) TIMESTAMP, VALUE
FROM         [TPOWEB].[dbo].[005_Actual_Space_Temperature_15_CWE]
ORDER BY TIMESTAMP DESC

GO

CREATE VIEW [dbo].[005_Prediction_Space_Temperature_15_CWE_End]
AS
SELECT     TOP (7) Prediction_DateTime AS TIMESTAMP, Value
FROM         dbo.[005_Prediction_Space_Temperature_15_CWE_Derivative]
ORDER BY TIMESTAMP DESC

Go



CREATE VIEW [dbo].[005_Prediction_Space_Temperature_28_CSO]
AS
SELECT     TOP (100) PERCENT t1.Prediction_DateTime, t1.Prediction_Value, t1.Lower_Bound_95, t1.Upper_Bound_95, t1.Lower_Bound_68, 
                      t1.Upper_Bound_68
FROM         [641].dbo.[641---------000TPOHVATEMSPA001---001] AS t1 INNER JOIN
                          (SELECT     MAX(Run_DateTime) AS Run_DateTime, Prediction_DateTime
                            FROM          [641].dbo.[641---------000TPOHVATEMSPA001---001]
                            GROUP BY Prediction_DateTime) AS t2 ON t1.Run_DateTime = t2.Run_DateTime AND t1.Prediction_DateTime = t2.Prediction_DateTime
WHERE     (t1.Floor = 'F28' AND t1.Quadrant = 'CSO') 
ORDER BY t1.Prediction_DateTime

Go

CREATE VIEW [dbo].[005_Prediction_Space_Temperature_28_CSO_Derivative]
AS
SELECT     t1.Run_DateTime, t1.Prediction_DateTime, t1.Floor, t1.Value
FROM         (SELECT     Run_DateTime, Prediction_DateTime, Floor, Value
                       FROM         [641].dbo.[641---------000TPONOWTEMSPA001---001]
                       WHERE      (Floor = 'F28' AND Quadrant = 'CSO')) AS t1 INNER JOIN
                          (SELECT     MAX(Run_DateTime) AS Run_DateTime, Prediction_DateTime
                            FROM          [641].dbo.[641---------000TPONOWTEMSPA001---001] AS Derivative_1
                            WHERE      (Floor = 'F28' AND Quadrant = 'CSO')
                            GROUP BY Prediction_DateTime) AS t2 ON t1.Prediction_DateTime = t2.Prediction_DateTime AND t1.Run_DateTime = t2.Run_DateTime

GO

CREATE VIEW [dbo].[005_Prediction_Space_Temperature_28_CSO_Start]
AS
SELECT     TOP (1) TIMESTAMP, VALUE
FROM         [TPOWEB].[dbo].[005_Actual_Space_Temperature_28_CSO]
ORDER BY TIMESTAMP DESC

GO

CREATE VIEW [dbo].[005_Prediction_Space_Temperature_28_CSO_End]
AS
SELECT     TOP (7) Prediction_DateTime AS TIMESTAMP, Value
FROM         dbo.[005_Prediction_Space_Temperature_28_CSO_Derivative]
ORDER BY TIMESTAMP DESC

Go


CREATE VIEW [dbo].[005_Prediction_Space_Temperature_28_CNO]
AS
SELECT     TOP (100) PERCENT t1.Prediction_DateTime, t1.Prediction_Value, t1.Lower_Bound_95, t1.Upper_Bound_95, t1.Lower_Bound_68, 
                      t1.Upper_Bound_68
FROM         [641].dbo.[641---------000TPOHVATEMSPA001---001] AS t1 INNER JOIN
                          (SELECT     MAX(Run_DateTime) AS Run_DateTime, Prediction_DateTime
                            FROM          [641].dbo.[641---------000TPOHVATEMSPA001---001]
                            GROUP BY Prediction_DateTime) AS t2 ON t1.Run_DateTime = t2.Run_DateTime AND t1.Prediction_DateTime = t2.Prediction_DateTime
WHERE     (t1.Floor = 'F28' AND t1.Quadrant = 'CNO') 
ORDER BY t1.Prediction_DateTime

Go

CREATE VIEW [dbo].[005_Prediction_Space_Temperature_28_CNO_Derivative]
AS
SELECT     t1.Run_DateTime, t1.Prediction_DateTime, t1.Floor, t1.Value
FROM         (SELECT     Run_DateTime, Prediction_DateTime, Floor, Value
                       FROM         [641].dbo.[641---------000TPONOWTEMSPA001---001]
                       WHERE      (Floor = 'F28' AND Quadrant = 'CNO')) AS t1 INNER JOIN
                          (SELECT     MAX(Run_DateTime) AS Run_DateTime, Prediction_DateTime
                            FROM          [641].dbo.[641---------000TPONOWTEMSPA001---001] AS Derivative_1
                            WHERE      (Floor = 'F28' AND Quadrant = 'CNO')
                            GROUP BY Prediction_DateTime) AS t2 ON t1.Prediction_DateTime = t2.Prediction_DateTime AND t1.Run_DateTime = t2.Run_DateTime

GO

CREATE VIEW [dbo].[005_Prediction_Space_Temperature_28_CNO_Start]
AS
SELECT     TOP (1) TIMESTAMP, VALUE
FROM         [TPOWEB].[dbo].[005_Actual_Space_Temperature_28_CNO]
ORDER BY TIMESTAMP DESC

GO

CREATE VIEW [dbo].[005_Prediction_Space_Temperature_28_CNO_End]
AS
SELECT     TOP (7) Prediction_DateTime AS TIMESTAMP, Value
FROM         dbo.[005_Prediction_Space_Temperature_28_CNO_Derivative]
ORDER BY TIMESTAMP DESC

Go







