<%@ Page Language="c#" Inherits="SmartBuilding.TPO345Park" AutoEventWireup="true" CodeFile="TPO345Park.aspx.cs" %>

<%@ Register Assembly="System.Web.DataVisualization, Version=3.5.0.0, Culture=neutral, PublicKeyToken=31bf3856ad364e35"
    Namespace="System.Web.UI.DataVisualization.Charting" TagPrefix="asp" %>

<%@ Register Assembly="AjaxControlToolkit" Namespace="AjaxControlToolkit" TagPrefix="ajaxToolkit" %>
<%@ Register assembly="System.Web.DataVisualization" namespace="System.Web.UI.DataVisualization.Charting" tagprefix="asp" %>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head id="Head1" runat="server">
    <link rel="shortcut icon" href="images/diboss/favicon.ico" type="image/x-icon" />
	<link rel="apple-touch-icon" href="images/diboss/apple-touch-icon.png" />
    <link media="all" href="Style-diboss.css" type="text/css" rel="stylesheet" />
    <title>TPO</title>
</head>
<body>
    <form id="Form1" method="post" runat="server">
    <ajaxToolkit:ToolkitScriptManager runat="Server" EnableScriptGlobalization="true"
        EnableScriptLocalization="true" ID="ToolkitScriptManager1" ScriptMode="Debug" CombineScripts="false" />
    <table width="952" align="center" border="0" cellpadding="0" cellspacing="0">
        <tr>
            <td colspan="2" align="left"><a href
            ="https://diboss.selex-es.com/"><img src="images/diboss/banner.png" border="0" alt="Di-BOSS" /></a></td>
        </tr>
        <tr>
            <td colspan="2" class="nav"><hr /></td>
		</tr>
        <tr>
            <td colspan="2" class="nav"><p>&nbsp;HOME >> 345 Park Avenue</p></td>
		</tr>
        <tr>
            <td valign="top" align="center">
            <br />
            <table border="0" cellpadding="3" cellspacing="3">
	            <tr>
                    <td align="center"><a href="KPMG/SensorDataTempInteriorTenant.aspx"><asp:Imagebutton ID="ImageButton1" runat="server" PostBackUrl="KPMG/SensorDataTempInteriorTenant.aspx" ImageURL="images/diboss/square-g.png" onmouseover="this.src='images/diboss/square-y.png'" onmouseout="this.src='images/diboss/square-g.png'" /><br />Space Temperature (Tenant)</a></td>
		            <td align="center"><a href="KPMG/SpaceTempPredictionTenant.aspx"><asp:Imagebutton ID="ImageButton5" runat="server" PostBackUrl="KPMG/SpaceTempPredictionTenant.aspx" ImageURL="images/diboss/square-g.png" onmouseover="this.src='images/diboss/square-y.png'" onmouseout="this.src='images/diboss/square-g.png'" /><br />Space Temperature Prediction (Tenant)</a></td>
		            <td align="center"><a href="KPMG/ElectricityPredictionTenant.aspx"><asp:Imagebutton ID="ImageButton6" runat="server" PostBackUrl="KPMG/ElectricityPredictionTenant.aspx" ImageURL="images/diboss/square-g.png" onmouseover="this.src='images/diboss/square-y.png'" onmouseout="this.src='images/diboss/square-g.png'" /><br />Electricity Usage Prediction (Tenant)</a></td>
		            <td align="center"></td>
	            </tr>
            </table>
            </td>
        </tr>
        <tr>
            <td>
                <br />
                <br />
            </td>
            <td>
                <br />
                <br />
            </td>
        </tr>
    </table>
    <br />
    <div align="center" class="copy">
        </div>
    <br />
    </form>
</body>
</html>
