<%@ Page Language="c#" Inherits="SmartBuilding.diboss_KPMG_SpaceTempPredictionTenant" AutoEventWireup="true" CodeFile="SpaceTempPredictionTenant.aspx.cs" %>

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
    <table width="952" align="center" border="0" cellpadding="0" cellspacing="0">
        <tr>
            <td colspan="2" align="left"><a href
            ="https://diboss.selex-es.com/"><img src="../images/diboss/banner.png" border="0" alt="Di-BOSS" /></a></td>
        </tr>
        <tr>
            <td colspan="2" class="nav"><hr /></td>
		</tr>
        <tr>
            <td colspan="2" class="nav"><p>&nbsp;<a href="/TPO/TPOKPMG.aspx">HOME</a> >> 345 Park Avenue</p></td>
		</tr>
        <tr>
            <td valign="top" align="center">
            <br />
                <asp:Chart ID="Chart1" runat="server"
                    ImageType="Png" BackColor="WhiteSmoke" BorderWidth="2" BackGradientStyle="TopBottom"
                    BackSecondaryColor="White" Palette="BrightPastel" BorderlineDashStyle="Solid"
                    BorderColor="26, 59, 105" Height="700px" Width="680px" ImageStorageMode="UseImageLocation" ImageLocation="..\TempImageFiles\ChartPic_#SEQ(300,3)">
                    <Titles>
                        <asp:Title ShadowColor="32, 0, 0, 0" Font="Trebuchet MS, 12pt, style=Bold" ShadowOffset="3"
                            Text="Tenant Space Temperature Prediction versus Actual" ForeColor="26, 59, 105">
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
                            <AxisY LineColor="64, 64, 64, 64" Title="°Fahrenheit" Minimum="50" Maximum="90" IsLabelAutoFit="False">
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
                <asp:Chart ID="Chart2" runat="server"
                    ImageType="Png" BackColor="WhiteSmoke" BorderWidth="2" BackGradientStyle="TopBottom"
                    BackSecondaryColor="White" Palette="BrightPastel" BorderlineDashStyle="Solid"
                    BorderColor="26, 59, 105" Height="400px" Width="680px" ImageStorageMode="UseImageLocation" ImageLocation="..\TempImageFiles\ChartPic_#SEQ(300,3)">
                    <Titles>
                        <asp:Title ShadowColor="32, 0, 0, 0" Font="Trebuchet MS, 12pt, style=Bold" ShadowOffset="3"
                            Text="Mean Absolute Percentage Error (MAPE)" ForeColor="26, 59, 105">
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
                            <AxisY LineColor="64, 64, 64, 64" IsLabelAutoFit="False">
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
                            Please select type:
                        </td>
                     </tr>
                     <tr>
                        <td  colspan="2" nowrap >
                            <asp:RadioButtonList ID="SensorTypeList" runat="server" AutoPostBack="true" RepeatColumns="1" CssClass="cblist">
                            </asp:RadioButtonList>
                        </td>
                    </tr>
                    <tr>
                        <td colspan="2">
                            Please select date:
                        </td>
                     </tr>
                    <tr>
                        <td  colspan="2" nowrap >
                            <asp:RadioButtonList id="DateRange" runat="server">
                               <asp:ListItem Value="default">Day-Ahead vs Actual</asp:ListItem>
                               <asp:ListItem Value="custom" selected="true">Use Date Range Below</asp:ListItem>
                            </asp:RadioButtonList>
                        </td>
                    </tr>
                    <tr>
                        <td>&nbsp;&nbsp;From: </td>
                        <td nowrap>
                        <asp:TextBox runat="server" Width="100" ID="DateFrom" />
        <asp:ImageButton runat="Server" ID="Image1" ImageUrl="~/images/Calendar_scheduleHS.png" AlternateText="Click to show calendar" /><br />
        <ajaxToolkit:CalendarExtender ID="calendarButtonExtender" runat="server" TargetControlID="DateFrom" 
            PopupButtonID="Image1" />
                        <asp:RegularExpressionValidator ID="RegularExpressionValidator1" runat="server" ControlToValidate="DateFrom" ErrorMessage="Invalid date format" 
                        ValidationExpression="^([1-9]|1[012])[- /.]([1-9]|[12][0-9]|3[01])[- /.](19|20)\d\d$"></asp:RegularExpressionValidator>
                        <asp:RangeValidator ID="RangeValidator1" runat="server" ControlToValidate="DateFrom" MinimumValue="12/31/1950" MaximumValue="1/1/2100" Type="Date" Text="Invalid date value" Display="Dynamic" />
                        <asp:RequiredFieldValidator ID="RequiredFieldValidator1" ControlToValidate="DateFrom" Text="Empty date" runat="server" />
                        </td>
                    </tr>
                    <tr>
                        <td>&nbsp;&nbsp;To: </td>
                        <td nowrap>
                        <asp:TextBox runat="server" Width="100" ID="DateTo" />
        <asp:ImageButton runat="Server" ID="Image2" ImageUrl="~/images/Calendar_scheduleHS.png" AlternateText="Click to show calendar" /><br />
        <ajaxToolkit:CalendarExtender ID="CalendarExtender1" runat="server" TargetControlID="DateTo" 
            PopupButtonID="Image2" />
                        <asp:RegularExpressionValidator ID="RegularExpressionValidator2" runat="server" ControlToValidate="DateTo" ErrorMessage="Invalid date format" 
                        ValidationExpression="^([1-9]|1[012])[- /.]([1-9]|[12][0-9]|3[01])[- /.](19|20)\d\d$"></asp:RegularExpressionValidator>
                        <asp:RangeValidator ID="RangeValidator2" runat="server" ControlToValidate="DateTo" MinimumValue="12/31/1950" MaximumValue="1/1/2100" Type="Date" Text="Invalid date value" Display="Dynamic" />
                        <asp:RequiredFieldValidator ID="RequiredFieldValidator2" ControlToValidate="DateTo" Text="Empty date" runat="server" />
                        </td>
                    </tr>
                    <tr>
                        <td colspan="2">
                            <asp:CheckBox runat="server" ID="ShowBounds" Checked="false" Text="Show 95% Confidence" />
                        </td>
                     </tr>
                     <tr>
                        <td colspan="2">
                            <asp:CheckBox runat="server" ID="ShowBounds2" Checked="true" Text="Show 68% Confidence" />
                        </td>
                     </tr>
                     <tr>
                        <td colspan="2">
                            <asp:CheckBox runat="server" ID="ShowNowcast" Checked="false" Text="Show Nowcast" />
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
