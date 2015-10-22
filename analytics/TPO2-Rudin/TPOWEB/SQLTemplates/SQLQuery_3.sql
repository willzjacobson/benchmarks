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




