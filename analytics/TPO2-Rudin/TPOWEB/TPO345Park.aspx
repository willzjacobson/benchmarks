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
            <td colspan="2" align="left"><a href="<%= ConfigurationManager.AppSettings["DIBOSS_URL"] %>"><img src="images/diboss/banner.png" border="0" alt="Di-BOSS" /></a></td>
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
		            <td align="center"><a href="001/SpaceTempPrediction.aspx"><asp:Imagebutton ID="ImageButton1" runat="server" PostBackUrl="001/SpaceTempPrediction.aspx" ImageURL="images/diboss/square-g.png" onmouseover="this.src='images/diboss/square-y.png'" onmouseout="this.src='images/diboss/square-g.png'" /><br />Space Temperature Prediction (Nowcast)</a></td>
		            <td align="center"><a href="001/SpaceTempPredictionWeek.aspx"><asp:Imagebutton ID="ImageButton2" runat="server" PostBackUrl="001/SpaceTempPredictionWeek.aspx"  ImageURL="images/diboss/square-g.png" onmouseover="this.src='images/diboss/square-y.png'" onmouseout="this.src='images/diboss/square-g.png'" /><br />Space Temperature Prediction (Week)</a></td>
		            <td align="center"><a href="001/ElectricityPrediction.aspx"><asp:Imagebutton ID="ImageButton3" runat="server" PostBackUrl="001/ElectricityPrediction.aspx"  ImageURL="images/diboss/square-g.png" onmouseover="this.src='images/diboss/square-y.png'" onmouseout="this.src='images/diboss/square-g.png'" /><br />Electricity Usage Prediction</a></td>
		            <td align="center"><a href="001/SteamPrediction.aspx"><asp:Imagebutton ID="ImageButton4" runat="server" PostBackUrl="001/SteamPrediction.aspx" ImageURL="images/diboss/square-g.png" onmouseover="this.src='images/diboss/square-y.png'" onmouseout="this.src='images/diboss/square-g.png'" /><br />Steam Usage Prediction</a></td>
	            </tr>
                <tr>
                    <td colspan="4">&nbsp;<br /><br /></td>
		        </tr>
	            <tr>
                	<td align="center"><a href="001/OccupancyPrediction.aspx"><asp:Imagebutton ID="ImageButton7" runat="server" PostBackUrl="001/OccupancyPrediction.aspx"  ImageURL="images/diboss/square-g.png" onmouseover="this.src='images/diboss/square-y.png'" onmouseout="this.src='images/diboss/square-g.png'" /><br />Occupancy Prediction</a></td>
		            <td align="center"><a href="001/SpaceTempPredictionTenant.aspx"><asp:Imagebutton ID="ImageButton5" runat="server" PostBackUrl="001/SpaceTempPredictionTenant.aspx" ImageURL="images/diboss/square-g.png" onmouseover="this.src='images/diboss/square-y.png'" onmouseout="this.src='images/diboss/square-g.png'" /><br />Space Temperature Prediction (KPMG)</a></td>
		            <td align="center"><a href="001/ElectricityPredictionTenant.aspx"><asp:Imagebutton ID="ImageButton6" runat="server" PostBackUrl="001/ElectricityPredictionTenant.aspx" ImageURL="images/diboss/square-g.png" onmouseover="this.src='images/diboss/square-y.png'" onmouseout="this.src='images/diboss/square-g.png'" /><br />Electricity Usage Prediction (KPMG)</a></td>
		            <td align="center"><a href="001/ElectricityPredictionTenantBlackstone.aspx"><asp:Imagebutton ID="ImageButton8" runat="server" PostBackUrl="001/ElectricityPredictionTenantBlackstone.aspx" ImageURL="images/diboss/square-g.png" onmouseover="this.src='images/diboss/square-y.png'" onmouseout="this.src='images/diboss/square-g.png'" /><br />Electricity Usage Prediction (Blackstone)</a></td>

	            </tr>
                <tr>
                    <td colspan="4">&nbsp;<br /><br /></td>
		        </tr>
	            <tr>

                    <td align="center"><a href="001/ElectricityPredictionTenantNFL.aspx"><asp:Imagebutton ID="ImageButton15" runat="server" PostBackUrl="001/ElectricityPredictionTenantNFL.aspx" ImageURL="images/diboss/square-g.png" onmouseover="this.src='images/diboss/square-y.png'" onmouseout="this.src='images/diboss/square-g.png'" /><br />Electricity Usage Prediction (NFL)</a></td>
		            <td align="center"><a href="001/ElectricityPredictionTenantDBank.aspx"><asp:Imagebutton ID="ImageButton11" runat="server" PostBackUrl="001/ElectricityPredictionTenantDBank.aspx" ImageURL="images/diboss/square-g.png" onmouseover="this.src='images/diboss/square-y.png'" onmouseout="this.src='images/diboss/square-g.png'" /><br />Electricity Usage Prediction (Deutsche Bank)</a></td>
		            <td align="center"><a href="001/ElectricityPredictionTenantLadder.aspx"><asp:Imagebutton ID="ImageButton12" runat="server" PostBackUrl="001/ElectricityPredictionTenantLadder.aspx" ImageURL="images/diboss/square-g.png" onmouseover="this.src='images/diboss/square-y.png'" onmouseout="this.src='images/diboss/square-g.png'" /><br />Electricity Usage Prediction (Ladder Capital)</a></td>
                    <td align="center"><a href="001/PredictionScore.aspx"><asp:Imagebutton ID="ImageButton9" runat="server" PostBackUrl="001/PredictionScore.aspx" ImageURL="images/diboss/square-g.png" onmouseover="this.src='images/diboss/square-y.png'" onmouseout="this.src='images/diboss/square-g.png'" /><br />Prediction Score</a></td>
		            

	            </tr>
                <tr>
                    <td colspan="4">&nbsp;<br /><br /></td>
		        </tr>
	            <tr>
                    
                    <td align="center"><a href="001/PredictionScoreAvg.aspx"><asp:Imagebutton ID="ImageButton10" runat="server" PostBackUrl="001/PredictionScoreAvg.aspx" ImageURL="images/diboss/square-g.png" onmouseover="this.src='images/diboss/square-y.png'" onmouseout="this.src='images/diboss/square-g.png'" /><br />Prediction Score Rolling Average</a></td>
		            <td align="center"><a href="001/RecommendationScore.aspx"><asp:Imagebutton ID="ImageButton13" runat="server" PostBackUrl="001/RecommendationScore.aspx" ImageURL="images/diboss/square-g.png" onmouseover="this.src='images/diboss/square-y.png'" onmouseout="this.src='images/diboss/square-g.png'" /><br />Recommendation Score</a></td>
		            <td align="center"><a href="001/RecommendationScoreAvg.aspx"><asp:Imagebutton ID="ImageButton14" runat="server" PostBackUrl="001/RecommendationScoreAvg.aspx" ImageURL="images/diboss/square-g.png" onmouseover="this.src='images/diboss/square-y.png'" onmouseout="this.src='images/diboss/square-g.png'" /><br />Recommendation Score Rolling Average</a></td>
                    <td align="center"><a href="001/Weather_History.aspx"><asp:Imagebutton ID="ImageButton16" runat="server" PostBackUrl="001/Weather_History.aspx" ImageURL="images/diboss/square-g.png" onmouseover="this.src='images/diboss/square-y.png'" onmouseout="this.src='images/diboss/square-g.png'" /><br />Weather History</a></td>

	            </tr>
                <tr>
                    <td colspan="4">&nbsp;<br /><br /></td>
		        </tr>
	            <tr>
                    
                    <td align="center"><a href="001/ASCFan.aspx"><asp:Imagebutton ID="ImageButton17" runat="server" PostBackUrl="001/ASCFan.aspx" ImageURL="images/diboss/square-g.png" onmouseover="this.src='images/diboss/square-y.png'" onmouseout="this.src='images/diboss/square-g.png'" /><br />Thermal ASC</a></td>
		            <td align="center"><a href="001/ASCPumpHistory.aspx"><asp:Imagebutton ID="ImageButton18" runat="server" PostBackUrl="001/ASCPumpHistory.aspx" ImageURL="images/diboss/square-g.png" onmouseover="this.src='images/diboss/square-y.png'" onmouseout="this.src='images/diboss/square-g.png'" /><br />Thermal ASC Pump History</a></td>
		            <td align="center"><a href="001/ASCFanHistory.aspx"><asp:Imagebutton ID="ImageButton19" runat="server" PostBackUrl="001/ASCFanHistory.aspx" ImageURL="images/diboss/square-g.png" onmouseover="this.src='images/diboss/square-y.png'" onmouseout="this.src='images/diboss/square-g.png'" /><br />Thermal ASC Fan History</a></td>
                    <td align="center"><a href="001/ASC_Output_VFD.aspx"><asp:Imagebutton ID="ImageButton20" runat="server" PostBackUrl="001/ASC_Output_VFD.aspx" ImageURL="images/diboss/square-g.png" onmouseover="this.src='images/diboss/square-y.png'" onmouseout="this.src='images/diboss/square-g.png'" /><br />VFD</a></td>

	            </tr>
                <tr>
                    <td colspan="4">&nbsp;<br /><br /></td>
		        </tr>
	            <tr>
                    
                    <td align="center"><a href="001/ASC_Output_Electric.aspx"><asp:Imagebutton ID="ImageButton21" runat="server" PostBackUrl="001/ASC_Output_Electric.aspx" ImageURL="images/diboss/square-g.png" onmouseover="this.src='images/diboss/square-y.png'" onmouseout="this.src='images/diboss/square-g.png'" /><br />ASC Output Electric</a></td>
                    <td align="center"><a href="001/ASC_Output_Electric_Cum.aspx"><asp:Imagebutton ID="ImageButton30" runat="server" PostBackUrl="001/ASC_Output_Electric_Cum.aspx" ImageURL="images/diboss/square-g.png" onmouseover="this.src='images/diboss/square-y.png'" onmouseout="this.src='images/diboss/square-g.png'" /><br />ASC Output Electric Cum</a></td>
		            <td align="center"><a href="001/ASC_Output_Steam.aspx"><asp:Imagebutton ID="ImageButton22" runat="server" PostBackUrl="001/ASC_Output_Steam.aspx" ImageURL="images/diboss/square-g.png" onmouseover="this.src='images/diboss/square-y.png'" onmouseout="this.src='images/diboss/square-g.png'" /><br />ASC Output Steam</a></td>
		            <td align="center"><a href="001/ASC_Output_Occupancy.aspx"><asp:Imagebutton ID="ImageButton23" runat="server" PostBackUrl="001/ASC_Output_Occupancy.aspx" ImageURL="images/diboss/square-g.png" onmouseover="this.src='images/diboss/square-y.png'" onmouseout="this.src='images/diboss/square-g.png'" /><br />ASC Output Occupancy</a></td>
 
	            </tr>
                <tr>
                    <td colspan="4">&nbsp;<br /><br /></td>
		        </tr>
	            <tr>

                    <td align="center"><a href="001/ASC_Output_Temp.aspx"><asp:Imagebutton ID="ImageButton29" runat="server" PostBackUrl="001/ASC_Output_Temp.aspx" ImageURL="images/diboss/square-g.png" onmouseover="this.src='images/diboss/square-y.png'" onmouseout="this.src='images/diboss/square-g.png'" /><br />ASC Output Temp</a></td>
                    <td align="center"><a href="001/PredictionScoreASC.aspx"><asp:Imagebutton ID="ImageButton24" runat="server" PostBackUrl="001/PredictionScoreASC.aspx" ImageURL="images/diboss/square-g.png" onmouseover="this.src='images/diboss/square-y.png'" onmouseout="this.src='images/diboss/square-g.png'" /><br />ASC Prediction Score</a></td>
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
