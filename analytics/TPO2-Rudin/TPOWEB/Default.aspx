<%@ Page Language="C#" AutoEventWireup="true" CodeFile="Default.aspx.cs" Inherits="_Default" %>

<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head id="Head1" runat="server">
    <link rel="shortcut icon" href="images/diboss/favicon.ico" type="image/x-icon" />
	<link rel="apple-touch-icon" href="images/diboss/apple-touch-icon.png" />
    <link media="all" href="Style-diboss.css" type="text/css" rel="stylesheet" />
    <title>TPO</title>
</head>
<body>
    <form id="form1" runat="server">
    <table width="952" align="center" border="0" cellpadding="0" cellspacing="0">
        <tr>
            <td align="center"><a href="<%= ConfigurationManager.AppSettings["DIBOSS_URL"] %>"><img src="images/diboss/banner.png" border="0" alt="Di-BOSS" /></a></td>
        </tr>
        <tr>
            <td align="center"><br />
                <h2>Rudin Management</h2>
            </td>
        </tr>
        <tr>
            <td align="center">
                <table border="0" cellpadding="5" cellspacing="0">
                    <tr>
                        <td colspan="7">
                            <hr size="1" width="100%" />
                        </td>
                    </tr>
                    <tr>
                        <td>
                            &nbsp;
                        </td>
                        <td align="center" valign="top">
                            <img src="images/building_345park.jpg" alt="345 Park Avenue" /><br /><br />
                        </td>
                        <td valign="top" valign="top">
                            345 Park Avenue<br />
                            New York NY 10154<br />
                            <h3><a href="TPO345Park.aspx">TPO</a></h3><br />
                        </td>
						<td align="left" valign="top">
							
                            <br />
                        </td>
                        <td align="center" valign="top">
                            <img src="images/building_560lexington.jpg" alt="560 Lexington Avenue" /><br /><br />
                            
                        </td>
                        <td valign="top" valign="top">
                            560 Lexington Avenue<br />
                            New York NY 10022<br />
                            <h3><a href="TPO560Lex.aspx">TPO</a></h3><br />
                            
                        </td>
						<td>
                            &nbsp;
                        </td>
                    </tr>
                    <tr>
                        <td colspan="7">
                            <hr size="1" width="100%" />
                        </td>
                    </tr>
                    <tr>
                        <td>
                            &nbsp;
                        </td>
                        <td align="center" valign="top">
                            <img src="images/building_40E52.jpg" alt="40 East 52nd Street" /><br /><br />
                            
                        </td>
                        <td valign="top" valign="top">
                            40 East 52nd Street<br />
                            New York NY 10022<br />
                            <h3><a href="TPO40E52.aspx">TPO</a></h3><br />
                        </td>
						<td align="left" valign="top">
                            
                            <br />
                        </td>
                        <td align="center" valign="top">
                            <img src="images/building_1batterypark.jpg" alt="One Battery Park Plaza" /><br /><br />
                            
                        </td>
                        <td valign="top" valign="top">
                            One Battery Park Plaza<br />
                            New York NY 10004<br />
                            <h3><a href="TPO1BatteryPark.aspx">TPO</a></h3><br />
                        </td>
						<td>
                            &nbsp;
                        </td>
                    </tr>
                    <tr>
                        <td colspan="7">
                            <hr size="1" width="100%" />
                        </td>
                    </tr>
                    <tr>
                        <td>
                            &nbsp;
                        </td>
                        <td align="center" valign="top">
                            <img src="images/building_641Lexington.jpg" alt="641 Lexington" /><br /><br />
                            
                        </td>
                        <td valign="top" valign="top">
                            641 Lexington Avenue<br />
                            New York NY 10022<br />
                            <h3><a href="TPO641Lex.aspx">TPO</a></h3><br />
                        </td>
						<td align="left" valign="top">
                            
                            <br />
                        </td>
                        <td align="center" valign="top">
                            <img src="images/building_1Whitehall.jpg" alt="One White Hall Street" /><br /><br />
                            
                        </td>
                        <td valign="top" valign="top">
                            One Whitehall Street<br />
                            New York NY 10004<br />
                            <h3><a href="TPO1Whitehall.aspx">TPO</a></h3><br />
                        </td>
						<td>
                            &nbsp;
                        </td>
                    </tr>
                    <tr>
                        <td>
                            &nbsp;
                        </td>
                        <td>
                            &nbsp;
                        </td>
                        <td>
                            &nbsp;
                        </td>
                        <td>
                            &nbsp;
                        </td>
                        <td>
                            &nbsp;
                        </td>
                        <td>
                            &nbsp;
                        </td>
                        <td>
                            &nbsp;
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
        </tr>
    </table>
    <br />
    <div align="center" class="copy">
        (<asp:LinkButton runat="server" Text="Log Out" OnClick="btnLogout_Onclick"></asp:LinkButton>)</div>
    <br />
    </form>
</body>
</html>
