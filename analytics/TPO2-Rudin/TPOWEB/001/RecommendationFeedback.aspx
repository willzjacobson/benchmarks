<%@ Page Language="c#" Inherits="SmartBuilding.diboss_001_RecommendationFeedback" AutoEventWireup="true" CodeFile="RecommendationFeedback.aspx.cs" %>

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
            <td colspan="3" align="left"><a href="<%= ConfigurationManager.AppSettings["DIBOSS_URL"] %>"><img src="../images/diboss/banner.png" border="0" alt="Di-BOSS" /></a></td>
        </tr>
        <tr>
            <td colspan="3" class="nav"><hr /></td>
		</tr>
        <tr>
            <td colspan="3" class="nav"><p>&nbsp;<a href="/TPO/TPO345Park.aspx">HOME</a> >> 345 Park Avenue</p></td>
		</tr>
        <tr>
            <td>
                <br />
                <br />
            </td>
            <td valign="top" align="center">
                
                <table>
                    <tr>
                        <td align="left">
                        <br /><br /><h3>Recommendation Feedback Form</h2><br />
                        <!-- The Form -->

                        <asp:FormView ID="FormView1" runat="server" AllowPaging="True" 
                    DataSourceID="SqlDataSource1" DefaultMode="Edit" 
                     onpageindexchanging="FormView1_PageIndexChanging">
                    <EditItemTemplate>
                        Date:
                        <asp:TextBox ID="FeedbackDateTextBox" runat="server" 
                            Text='<%# Bind("FeedbackDate") %>' />
                        <br />
                        RecType:
                        <asp:TextBox ID="RecTypeTextBox" runat="server" Text='<%# Bind("RecType") %>' />
                        <br />
                        Building:
                        <asp:TextBox ID="BuildingTextBox" runat="server" 
                            Text='<%# Bind("Building") %>' />
                        <br />
                        Actual Time:
                        <asp:TextBox ID="ActualTimeTextBox" runat="server" 
                            Text='<%# Bind("ActualTime") %>' />
                        <br />
                        Recommended Time:
                        <asp:TextBox ID="RecommendedTimeTextBox" runat="server" 
                            Text='<%# Bind("RecommendedTime") %>' />
                        <br />
                        HVAC Mode:
                        <asp:TextBox ID="HVACModeTextBox" runat="server" 
                            Text='<%# Bind("HVACMode") %>' />
                        <br />
                        Dampers:
                        <asp:TextBox ID="DampersTextBox" runat="server" Text='<%# Bind("Dampers") %>' />
                        <br />
                        Chillers:
                        <asp:TextBox ID="ChillersTextBox" runat="server" 
                            Text='<%# Bind("Chillers") %>' />
                        <br />
                        OAT:
                        <asp:TextBox ID="OATTextBox" runat="server" Text='<%# Bind("OAT") %>' />
                        <br />
                        WetBulb Temp:
                        <asp:TextBox ID="WetBulbTempTextBox" runat="server" 
                            Text='<%# Bind("WetBulbTemp") %>' />
                        <br />
                        CW Temp:
                        <asp:TextBox ID="CWTempTextBox" runat="server" Text='<%# Bind("CWTemp") %>' />
                        <br />
                        CW Startup:
                        <asp:TextBox ID="CWStartupTextBox" runat="server" 
                            Text='<%# Bind("CWStartup") %>' />
                        <br />
                        Judgement:
                        <asp:TextBox ID="JudgementTextBox" runat="server" 
                            Text='<%# Bind("Judgement") %>' />
                        <br />
                        Comments:
                        <asp:TextBox ID="CommentsTextBox" runat="server" 
                            Text='<%# Bind("Comments") %>' />
                        <br />
                        <br /><br />
                        <asp:LinkButton ID="UpdateButton" runat="server" CausesValidation="True" 
                            CommandName="Update" Text="Update" />
                        &nbsp;<asp:LinkButton ID="UpdateCancelButton" runat="server" 
                            CausesValidation="False" CommandName="Cancel" Text="Cancel" />
                    </EditItemTemplate>
                    <InsertItemTemplate>
                        <table>
                            <tr>
                                <td>Date:</td><td><asp:TextBox ID="FeedbackDateTextBox" runat="server" 
                            Text='<%# Bind("FeedbackDate") %>' />
                        <br /></td>
                            </tr>
                            <tr>
                                <td>Recommendation Type:</td><td><asp:TextBox ID="RecTypeTextBox" runat="server" Text='<%# Bind("RecType") %>' />
                        <br /></td>
                            </tr>
                            <tr>
                                <td>Building:</td><td><asp:TextBox ID="BuildingTextBox" runat="server" 
                            Text='<%# Bind("Building") %>' />
                        <br /></td>
                            </tr>
                            <tr>
                                <td> Actual Time:</td><td><asp:TextBox ID="ActualTimeTextBox" runat="server" 
                            Text='<%# Bind("ActualTime") %>' />
                        <br /></td>
                            </tr>
                            <tr>
                                <td>Recommended Time:</td><td><asp:TextBox ID="RecommendedTimeTextBox" runat="server" 
                            Text='<%# Bind("RecommendedTime") %>' />
                        <br /></td>
                            </tr>
                            <tr>
                                <td>HVAC Mode:</td><td><asp:TextBox ID="HVACModeTextBox" runat="server" 
                            Text='<%# Bind("HVACMode") %>' />
                        <br /></td>
                            </tr>
                            <tr>
                                <td>Dampers:</td><td><asp:TextBox ID="DampersTextBox" runat="server" Text='<%# Bind("Dampers") %>' />
                        <br /></td>
                            </tr>
                            <tr>
                                <td>Chillers:</td><td><asp:TextBox ID="ChillersTextBox" runat="server" 
                            Text='<%# Bind("Chillers") %>' />
                        <br /></td>
                            </tr>
                            <tr>
                                <td>OAT:</td><td><asp:TextBox ID="OATTextBox" runat="server" Text='<%# Bind("OAT") %>' />
                        <br /></td>
                            </tr>
                            <tr>
                                <td>WetBulb Temp:</td><td><asp:TextBox ID="WetBulbTempTextBox" runat="server" 
                            Text='<%# Bind("WetBulbTemp") %>' />
                        <br /></td>
                            </tr>
                            <tr>
                                <td>CW Temp:</td><td><asp:TextBox ID="CWTempTextBox" runat="server" Text='<%# Bind("CWTemp") %>' />
                        <br /></td>
                            </tr>
                            <tr>
                                <td> CW Startup:</td><td><asp:TextBox ID="CWStartupTextBox" runat="server" 
                            Text='<%# Bind("CWStartup") %>' />
                        <br /></td>
                            </tr>
                            <tr>
                                <td> Judgement:</td><td><asp:TextBox ID="JudgementTextBox" runat="server" 
                            Text='<%# Bind("Judgement") %>' />
                        <br /></td>
                            </tr>
                            <tr>
                                <td>Comments:</td><td><asp:TextBox TextMode="MultiLine" Columns="60" Rows="8" ID="CommentsTextBox" runat="server" 
                            Text='<%# Bind("Comments") %>' />
                        <br /></td>
                            </tr>
                        </table>

                        <br /><br />
                        <asp:LinkButton ID="InsertButton"  runat="server" CausesValidation="True" 
                            CommandName="Insert" Text="Submit" />
                        &nbsp;<asp:LinkButton ID="InsertCancelButton" runat="server" 
                            CausesValidation="False" CommandName="Cancel" Text="Cancel" />
                    </InsertItemTemplate>
                    <ItemTemplate>
                        Date:
                        <asp:Label ID="FeedbackDateLabel" runat="server" 
                            Text='<%# Bind("FeedbackDate") %>' />
                        <br />
                        RecType:
                        <asp:Label ID="RecTypeLabel" runat="server" Text='<%# Bind("RecType") %>' />
                        <br />
                        Building:
                        <asp:Label ID="BuildingLabel" runat="server" Text='<%# Bind("Building") %>' />
                        <br />
                        Actual Time:
                        <asp:Label ID="ActualTimeLabel" runat="server" 
                            Text='<%# Bind("ActualTime") %>' />
                        <br />
                        Recommended Time:
                        <asp:Label ID="RecommendedTimeLabel" runat="server" 
                            Text='<%# Bind("RecommendedTime") %>' />
                        <br />
                        HVAC Mode:
                        <asp:Label ID="HVACModeLabel" runat="server" Text='<%# Bind("HVACMode") %>' />
                        <br />
                        Dampers:
                        <asp:Label ID="DampersLabel" runat="server" Text='<%# Bind("Dampers") %>' />
                        <br />
                        Chillers:
                        <asp:Label ID="ChillersLabel" runat="server" Text='<%# Bind("Chillers") %>' />
                        <br />
                        OAT:
                        <asp:Label ID="OATLabel" runat="server" Text='<%# Bind("OAT") %>' />
                        <br />
                        WetBulb Temp:
                        <asp:Label ID="WetBulbTempLabel" runat="server" 
                            Text='<%# Bind("WetBulbTemp") %>' />
                        <br />
                        CW Temp:
                        <asp:Label ID="CWTempLabel" runat="server" Text='<%# Bind("CWTemp") %>' />
                        <br />
                        CW Startup:
                        <asp:Label ID="CWStartupLabel" runat="server" Text='<%# Bind("CWStartup") %>' />
                        <br />
                        Judgement:
                        <asp:Label ID="JudgementLabel" runat="server" Text='<%# Bind("Judgement") %>' />
                        <br />
                        Comments:
                        <asp:Label ID="CommentsLabel" runat="server" Text='<%# Bind("Comments") %>' />
                        <br />
                        <br /><br />
                    </ItemTemplate>
                </asp:FormView>
                <asp:SqlDataSource ID="SqlDataSource1" runat="server" 
                    ConnectionString="<%$ ConnectionStrings:TPOWEB %>" 
                    SelectCommand="SELECT [FeedbackDate],[RecType],[Building],[ActualTime],[RecommendedTime],[HVACMode],[Dampers],[Chillers],[OAT],[WetBulbTemp],[CWTemp],[CWStartup],[Judgement],[Comments] FROM [SROprFeedback] WHERE [FeedbackDate] = '2013-11-20'"  
                    UpdateCommand="UPDATE [SROprFeedback] SET [FeedbackDate]=@FeedbackDate,[RecType]=@RecType,[Building]=@Building,[ActualTime]=@ActualTime,[RecommendedTime]=@RecommendedTime,[HVACMode]=@HVACMode,[Dampers]=@Dampers,[Chillers]=@Chillers,[OAT]=@OAT,[WetBulbTemp]=@WetBulbTemp,[CWTemp]=@CWTemp,[CWStartup]=@CWStartup,[Judgement]=@Judgement,[Comments]@Comments WHERE [FeedbackDate] = '2013-11-20'" 
                    InsertCommand="INSERT INTO [SROprFeedback] ([FeedbackDate],[RecType],[Building],[ActualTime],[RecommendedTime],[HVACMode],[Dampers],[Chillers],[OAT],[WetBulbTemp],[CWTemp],[CWStartup],[Judgement],[Comments]) VALUES(@FeedbackDate,@RecType, @Building, @ActualTime, @RecommendedTime, @HVACMode, @Dampers, @Chillers,@OAT, @WetBulbTemp, @CWTemp, @CWStartup, @Judgement, @Comments)" 
                    onselecting="SqlDataSource1_Selecting"></asp:SqlDataSource>
                <br />
                
                <br />




                        <!-- End of The Form -->
                        
                        </td>
                    
                    </tr>
                </table>
            </td>
            <td align="left" valign="top">
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
