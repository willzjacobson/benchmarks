using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;
using System.Web.UI;
using System.Web.UI.WebControls;
using System.Data;
using System.Data.SqlClient;
using System.Data.OleDb;
using System.Configuration;
using System.Web.Security;

public partial class Login : System.Web.UI.Page
{
    protected void Page_Load(object sender, EventArgs e)
    {

    }

    protected void Page_Init(object sender, EventArgs e)
    {

        int Results = 0;
        string username = "diboss";
        string password = "tpo";

        if (Request.QueryString["K"] != string.Empty)
        {

            Results = Validate_LoginGUID(Request.QueryString["K"]);

            if (Results == 1)
            {

                lblMessage.Text = "Login is successful";

                FormsAuthentication.SetAuthCookie(username, true);
                FormsAuthentication.Authenticate(username, password);

                if (Request.QueryString["BID"] == "345Park")
                {
                    Response.Redirect("TPO345Park.aspx");
                }
                else if (Request.QueryString["BID"] == "560Lex")
                {
                    Response.Redirect("TPO560Lex.aspx");
                }
                else if (Request.QueryString["BID"] == "40E52")
                {
                    Response.Redirect("TPO40E52.aspx");
                }
                else if (Request.QueryString["BID"] == "1BP")
                {
                    Response.Redirect("TPO1BatteryPark.aspx");
                }
                else if (Request.QueryString["BID"] == "641Lex")
                {
                    Response.Redirect("TPO641Lex.aspx");
                }
                else if (Request.QueryString["BID"] == "1WH")
                {
                    Response.Redirect("TPO1Whitehall.aspx");
                }
            }
            else
            {

                lblMessage.Text = "Invalid Login";

                lblMessage.ForeColor = System.Drawing.Color.Red;

            }

        }

        else
        {

            lblMessage.Text = "Invalid Login";
            lblMessage.ForeColor = System.Drawing.Color.Red;

        }


    }

    public int Validate_LoginGUID(String Password)
    {
        string dbConnectionString = ConfigurationManager.ConnectionStrings["TPOWEB"].ToString();

        SqlConnection con = new SqlConnection(dbConnectionString);

        SqlCommand cmdselect = new SqlCommand();

        cmdselect.CommandType = CommandType.StoredProcedure;

        cmdselect.CommandText = "[dbo].[prcLoginGUID]";

        cmdselect.Parameters.Add("@UGUID", SqlDbType.VarChar, 50).Value = Password;

        cmdselect.Parameters.Add("@OutRes", SqlDbType.Int, 4);

        cmdselect.Parameters["@OutRes"].Direction = ParameterDirection.Output;

        cmdselect.Connection = con;

        int Results = 0;

        try
        {

            con.Open();

            cmdselect.ExecuteNonQuery();

            Results = (int)cmdselect.Parameters["@OutRes"].Value;

        }

        catch (SqlException ex)
        {

            lblMessage.Text = ex.Message;

        }

        finally
        {

            cmdselect.Dispose();

            if (con != null)
            {

                con.Close();

            }

        }

        return Results;

    } 

    public int Validate_Login(String Username, String Password)
    {
        string dbConnectionString = ConfigurationManager.ConnectionStrings["TPOWEB"].ToString();

        SqlConnection con = new SqlConnection(dbConnectionString);

        SqlCommand cmdselect = new SqlCommand();

        cmdselect.CommandType = CommandType.StoredProcedure;

        cmdselect.CommandText = "[dbo].[prcLoginv]";

        cmdselect.Parameters.Add("@Username", SqlDbType.VarChar, 50).Value = Username;

        cmdselect.Parameters.Add("@UPassword", SqlDbType.VarChar, 50).Value = Password;

        cmdselect.Parameters.Add("@OutRes", SqlDbType.Int, 4);

        cmdselect.Parameters["@OutRes"].Direction = ParameterDirection.Output;

        cmdselect.Connection = con;

        int Results = 0;

        try
        {

            con.Open();

            cmdselect.ExecuteNonQuery();

            Results = (int)cmdselect.Parameters["@OutRes"].Value;

        }

        catch (SqlException ex)
        {

            lblMessage.Text = ex.Message;

        }

        finally
        {

            cmdselect.Dispose();

            if (con != null)
            {

                con.Close();

            }

        }

        return Results;

    } 

    protected void btnlogin_Click(object sender, EventArgs e)
    {
        int Results = 0;

        if (txtUsername.Text != string.Empty && txtPassword.Text != string.Empty)
        {

            Results = Validate_Login(txtUsername.Text.Trim(), txtPassword.Text.Trim());

            if (Results == 1)
            {

                lblMessage.Text = "Login is successful";

                FormsAuthentication.RedirectFromLoginPage(txtUsername.Text, true);

            }

            else
            {

                lblMessage.Text = "Invalid Login";

                lblMessage.ForeColor = System.Drawing.Color.Red;

            }

        }

        else
        {

            lblMessage.Text = "Invalid Login";
            lblMessage.ForeColor = System.Drawing.Color.Red;

        }
    }
    protected void btnCancel_Click(object sender, EventArgs e)
    {
        txtUsername.Text = "";
        txtPassword.Text = "";
    }
}