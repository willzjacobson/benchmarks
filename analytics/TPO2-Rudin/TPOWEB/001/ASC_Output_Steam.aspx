<%@ Page Language="c#" Inherits="SmartBuilding.diboss_001_ASC_Output_Steam" AutoEventWireup="true" CodeFile="ASC_Output_Steam.aspx.cs" %>

<%@ Register Assembly="System.Web.DataVisualization, Version=3.5.0.0, Culture=neutral, PublicKeyToken=31bf3856ad364e35"
    Namespace="System.Web.UI.DataVisualization.Charting" TagPrefix="asp" %>

<%@ Register Assembly="AjaxControlToolkit" Namespace="AjaxControlToolkit" TagPrefix="ajaxToolkit" %>
<%@ Register assembly="System.Web.DataVisualization" namespace="System.Web.UI.DataVisualization.Charting" tagprefix="asp" %>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head id="Head1" runat="server">
    <link rel="shortcut icon" href="../images/diboss/favicon.ico" type="image/x-icon" />
	<link rel="apple-touch-icon" href="../images/diboss/apple-touch-icon.png" />
    <link media="all" href="../Style-diboss.css" type="text/css" rel="stylesheet" />
    <title>TPO</title>
</head>
<body>
    <form id="Chart" method="post" runat="server">
    <ajaxToolkit:ToolkitScriptManager runat="Server" EnableScriptGlobalization="true"
        EnableScriptLocalization="true" ID="ScriptManager1" ScriptMode="Debug" CombineScripts="false" />
    <table width="1152" align="center" border="0" cellpadding="0" cellspacing="0">
        <tr>
            <td colspan="2" align="center"><a href="<%= ConfigurationManager.AppSettings["DIBOSS_URL"] %>"><img src="../images/diboss/banner.png" border="0" alt="Di-BOSS" /></a></td>
        </tr>
        <tr>
            <td colspan="2" class="nav"><hr /></td>
		</tr>
        <tr>
            <td colspan="2" class="nav"><p>&nbsp;<a href="/TPO/TPO345Park.aspx">HOME</a> >> 345 Park Avenue</p></td>
		</tr>
 
        <tr>
			<td valign="top" align="center">
            <br />
                <asp:Chart ID="Chart2" runat="server"
                    ImageType="Png" BackColor="WhiteSmoke" BorderWidth="2" BackGradientStyle="TopBottom"
                    BackSecondaryColor="White" Palette="BrightPastel" BorderlineDashStyle="Solid"
                    BorderColor="26, 59, 105" Height="500px" Width="680px" ImageStorageMode="UseImageLocation" ImageLocation="..\TempImageFiles\ChartPic_#SEQ(300,3)">
                    <Titles>
                        <asp:Title ShadowColor="32, 0, 0, 0" Font="Trebuchet MS, 12pt, style=Bold" ShadowOffset="3"
                            Text="ASC Output Steam" ForeColor="26, 59, 105">
                        </asp:Title>
                    </Titles>
                    <Legends>
                        <asp:Legend Enabled="true" IsTextAutoFit="true" Docking="Bottom" Name="Default" BackColor="Transparent"
                            Font="Trebuchet MS, 8.25pt, style=Bold">
                        </asp:Legend>
                    </Legends>
                    <BorderSkin SkinStyle="Emboss"></BorderSkin>
                    <Series>

                    </Series>
                    <ChartAreas>
                        <asp:ChartArea Name="ChartArea1" BorderColor="64, 64, 64, 64" BorderDashStyle="Solid"
                            BackSecondaryColor="White" BackColor="Gainsboro" ShadowColor="Transparent" BackGradientStyle="TopBottom">
                            <Area3DStyle Rotation="10" Perspective="10" Inclination="15" IsRightAngleAxes="False"
                                WallWidth="0" IsClustered="False"></Area3DStyle>
                            <AxisY LineColor="64, 64, 64, 64" Title="Value" IsLabelAutoFit="False">
                                <LabelStyle Font="Trebuchet MS, 8.25pt, style=Bold" />
                                <MajorGrid LineColor="64, 64, 64, 64" />
                            </AxisY>
                            <AxisX LineColor="64, 64, 64, 64" IsLabelAutoFit="False">
                                <LabelStyle Font="Trebuchet MS, 8.25pt, style=Bold" Format="MM/dd/yyyy HH:mm" Angle="90" />
                                <MajorGrid LineColor="64, 64, 64, 64" />
                            </AxisX>
                        </asp:ChartArea>
                    </ChartAreas>
                </asp:Chart>
            

            </td>
            <td align="left" valign="top">
               
               <table align="center" cellpadding="4">
                    <tr>
                        <td colspan="2">
                            Please select ASC runtime:
                        </td>
                     </tr>
                     <tr>
                        <td  colspan="2" nowrap >
                            <asp:DropDownList ID="RuntimeList" runat="server" AppendDataBoundItems="true" CssClass="cblist">
                            </asp:DropDownList>
                        </td>
                    </tr>
                    <tr>
                        <td colspan="2">
                            Please select sensor:
                        </td>
                     </tr>
                     <tr>
                        <td  colspan="2" nowrap >
                            <asp:CheckBoxList ID="SensorTypeList" runat="server" RepeatColumns="1" AutoPostBack="True" CssClass="cblist">
                            </asp:CheckBoxList>
                        </td>
                    </tr>
                    <tr>
                        <td colspan="2">
                            <asp:Button ID="submit" runat="server" Text="Update" />
                        </td>
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
    </form>
</body>
</html>
