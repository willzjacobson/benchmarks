<%@ Page Language="c#" Inherits="SmartBuilding.TPO1BatteryPark" AutoEventWireup="true" CodeFile="TPO1BatteryPark.aspx.cs" %>

<%@ Register Assembly="System.Web.DataVisualization, Version=3.5.0.0, Culture=neutral, PublicKeyToken=31bf3856ad364e35"
    Namespace="System.Web.UI.DataVisualization.Charting" TagPrefix="asp" %>

<%@ Register Assembly="AjaxControlToolkit" Namespace="AjaxControlToolkit" TagPrefix="ajaxToolkit" %>
<%@ Register assembly="System.Web.DataVisualization" namespace="System.Web.UI.DataVisualization.Charting" tagprefix="asp" %>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head runat="server">
    <link rel="shortcut icon" href="images/diboss/favicon.ico" type="image/x-icon" />
	<link rel="apple-touch-icon" href="images/diboss/apple-touch-icon.png" />
    <link media="all" href="Style-diboss.css" type="text/css" rel="stylesheet" />
    <title>TPO</title>
</head>
<body>
    <form id="Chart" method="post" runat="server">
    <ajaxToolkit:ToolkitScriptManager runat="Server" EnableScriptGlobalization="true"
        EnableScriptLocalization="true" ID="ScriptManager1" ScriptMode="Debug" CombineScripts="false" />
    <table width="952" align="center" border="0" cellpadding="0" cellspacing="0">
        <tr>
            <td colspan="2" align="left"><a href="<%= ConfigurationManager.AppSettings["DIBOSS_URL"] %>"><img src="images/diboss/banner.png" border="0" alt="Di-BOSS" /></a></td>
        </tr>
        <tr>
            <td colspan="2" class="nav"><hr /></td>
		</tr>
        <tr>
            <td colspan="2" class="nav"><p>&nbsp;HOME >> One Battery Park Plaza</p></td>
		</tr>
        <tr>
            <td valign="top" align="center">
            <br />
            <table border="0" cellpadding="3" cellspacing="3">
                <tr>
		            <td align="center"><a href="004/SpaceTempPrediction.aspx"><asp:Imagebutton ID="ImageButton1" runat="server" PostBackUrl="004/SpaceTempPrediction.aspx" ImageURL="images/diboss/square-g.png" onmouseover="this.src='images/diboss/square-y.png'" onmouseout="this.src='images/diboss/square-g.png'" /><br />Space Temperature Prediction (Nowcast)</a>
                    </td>
		            <td align="center"><a href="004/SpaceTempPredictionWeek.aspx"><asp:Imagebutton ID="ImageButton2" runat="server" PostBackUrl="004/SpaceTempPredictionWeek.aspx" ImageURL="images/diboss/square-g.png" onmouseover="this.src='images/diboss/square-y.png'" onmouseout="this.src='images/diboss/square-g.png'" /><br />Space Temperature Prediction (Week)</a></td>
		            <td align="center"><a href="004/ElectricityPrediction.aspx"><asp:Imagebutton ID="ImageButton3" runat="server" PostBackUrl="004/ElectricityPrediction.aspx" ImageURL="images/diboss/square-g.png" onmouseover="this.src='images/diboss/square-y.png'" onmouseout="this.src='images/diboss/square-g.png'" /><br />Electricity Usage Prediction</a></td>
                    <td align="center"><a href="004/OccupancyPrediction.aspx"><asp:Imagebutton ID="ImageButton7" runat="server" PostBackUrl="004/OccupancyPrediction.aspx"  ImageURL="images/diboss/square-g.png" onmouseover="this.src='images/diboss/square-y.png'" onmouseout="this.src='images/diboss/square-g.png'" /><br />Occupancy Prediction</a></td>
                </tr>
                <tr>
                    <td colspan="4">&nbsp;<br /><br /></td>
		        </tr>
	            <tr>
                    
		            <td align="center"><a href="004/PredictionScore.aspx"><asp:Imagebutton ID="ImageButton9" runat="server" PostBackUrl="004/PredictionScore.aspx" ImageURL="images/diboss/square-g.png" onmouseover="this.src='images/diboss/square-y.png'" onmouseout="this.src='images/diboss/square-g.png'" /><br />Prediction Score</a></td>
		            <td align="center"><a href="004/PredictionScoreAvg.aspx"><asp:Imagebutton ID="ImageButton10" runat="server" PostBackUrl="004/PredictionScoreAvg.aspx" ImageURL="images/diboss/square-g.png" onmouseover="this.src='images/diboss/square-y.png'" onmouseout="this.src='images/diboss/square-g.png'" /><br />Prediction Score Rolling Average</a></td>
                    <td align="center"></td>
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
