USE [TPOWEB]
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
  


