@echo off
echo.
echo -----------------------------
echo      TPOWEB INSTALLATION
echo -----------------------------
echo.
echo STEP 1. CREATE DATABASE VIEWS USING SQL SCRIPT
echo.
sqlcmd -U TPOWEB_USER -P rud1n2013! -S anderson.ldeo.columbia.edu -d TPOWEB -i C:\Web\TPO\script\sql_add_building.sql -o C:\Web\TPO\script\sql_results.txt
echo.
echo DATABASE CREATED - SQL RESULTS AT C:\Web\TPO\script\sql_results.txt
echo.
echo.
echo STEP 2. CREATE WEB DIRECTORY
echo.
echo.
set /p UserInputPath= Which building ID do you want to create (format as 00X)?
echo. 
echo CREATING WEB DIRECTORY......
echo.
md C:\Web\TPO\%UserInputPath%
echo.
echo PREPARING WEB DIRECTORY......
xcopy /s C:\Web\TPO\000Templates C:\Web\TPO\%UserInputPath%
echo.
echo NEW WEB DIRECTORY /TPO/%UserInputPath% CREATED
echo.
echo --------------------------------------
echo     TPOWEB SUCCESSFULLY INSTALLED
echo --------------------------------------
echo.
echo.
