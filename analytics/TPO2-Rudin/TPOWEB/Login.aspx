<%@ Page Language="C#" AutoEventWireup="true" CodeFile="Login.aspx.cs" Inherits="Login" %>

<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head id="Head1" runat="server">
    <link rel="shortcut icon" href="images/diboss/favicon.ico" type="image/x-icon" />
	<link rel="apple-touch-icon" href="images/diboss/apple-touch-icon.png" />
    <link media="all" href="Style-diboss.css" type="text/css" rel="stylesheet" />
    <title>TPO</title>
</head>
<body>
    <form id="form2" runat="server">
    <table width="952" align="center" border="0" cellpadding="0" cellspacing="0">
        <tr>
            <td align="center"><a href="<%= ConfigurationManager.AppSettings["DIBOSS_URL"] %>"><img src="images/diboss/banner.png" border="0" alt="Di-BOSS" /></a></td>
        </tr>
        <tr>
            <td colspan="2" class="nav"><hr /></td>
		</tr>
        <tr>
            <td align="center">
            <br /><br />
                <table align="center" cellpadding="4">
                    <tr>
                        <td align="center" colspan="2">
                            <b>Please login:</b>
                        </td>
                    </tr>
                    <tr>
                        <td>
                            <asp:Label ID="lblUsername" runat="server" Text="Username"></asp:Label>
                        </td>
                        <td>
                            <asp:TextBox ID="txtUsername" runat="server"></asp:TextBox>
                        </td>
                    </tr>
                    <tr>
                        <td>
                            <asp:Label ID="lblPassword" runat="server" Text="Password"></asp:Label>
                        </td>
                        <td>
                            <asp:TextBox ID="txtPassword" runat="server" TextMode="Password"></asp:TextBox>
                        </td>
                    </tr>
                    <tr>
                        <td>
                            
                        </td>
                        <td> <asp:Button ID="btnlogin" runat="server" Text="Login" onclick="btnlogin_Click"

Width="60px" />
                            <asp:Button ID="btnCancel" runat="server" Text="Cancel"

onclick="btnCancel_Click" />
                        </td>
                    </tr>
                    <tr>
                        <td colspan="2">
                            <asp:Label ID="lblMessage" runat="server" Text=""></asp:Label>
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
    <div align="center" class="copy"></div>
    <br />
    </form>
</body>
</html>