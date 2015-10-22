using System;
using System.Collections;
using System.ComponentModel;
using System.Configuration;
using System.Data;
using System.Data.SqlClient;
using System.Data.OleDb;
using System.Drawing;
using System.Web;
using System.Web.SessionState;
using System.Web.UI;
using System.Web.UI.WebControls;
using System.Web.UI.HtmlControls;
using System.Web.UI.DataVisualization.Charting;
using System.Web.Security;

namespace SmartBuilding
{
    /// <summary>
    /// Summary description for FastLineChart.
    /// </summary>
    public partial class diboss_001_ASCPumpHistory : System.Web.UI.Page
    {

        bool useDateRange = false;
        DateTime fromDate;
        DateTime toDate;

        protected void btnLogout_Onclick(object sender, EventArgs e)
        {
            FormsAuthentication.SignOut(); Response.Redirect(Page.Request.Url.ToString());
        }

        protected void Page_Load(object sender, System.EventArgs e)
        {



            FillData();


            


        }

        #region Web Form Designer generated code
        override protected void OnInit(EventArgs e)
        {
            //
            // CODEGEN: This call is required by the ASP.NET Web Form Designer.
            //
            InitializeComponent();
            base.OnInit(e);
        }

        /// <summary>
        /// Required method for Designer support - do not modify
        /// the contents of this method with the code editor.
        /// </summary>
        private void InitializeComponent()
        {

        }
        #endregion

        private void FillData()
        {

            //sensorlist
            string runtime = "";
            
            if (!Page.IsPostBack)
            {
            // Initialize a connection string    
            string dbConnectionString = ConfigurationManager.ConnectionStrings["TPOWEB"].ToString();

            SqlConnection dbConnection = new SqlConnection(dbConnectionString);


            string queryRuntime = "SELECT DISTINCT [RUNTIME] FROM [345].[dbo].[345---------001TPOWATSECPUM---VAL001] ORDER BY [RUNTIME] DESC";

            DataSet dsRuntime = new DataSet();


            SqlDataAdapter adapter = new SqlDataAdapter();
            adapter.SelectCommand = new SqlCommand(queryRuntime, dbConnection);
            adapter.Fill(dsRuntime, "RUNTIME");

            RuntimeList.DataSource = dsRuntime;
            RuntimeList.DataMember = "RUNTIME";
            RuntimeList.DataTextField = "RUNTIME";
            RuntimeList.DataValueField = "RUNTIME";
            RuntimeList.DataBind();

            }

            if (RuntimeList.SelectedIndex > -1)
            {
                runtime = RuntimeList.SelectedItem.Value;

                PlotChart(runtime);
            }

        }


        private void PlotChart(string runtime)
        {

            // Initialize a connection string    
            string dbConnectionString = ConfigurationManager.ConnectionStrings["TPOWEB"].ToString();

            SqlConnection dbConnection = new SqlConnection(dbConnectionString);

            string dbQueryStringm;
            SqlCommand myCommand;
            SqlDataReader myReader;
            Series m;

         
            string queryPump = "SELECT DISTINCT EQUIPMENT_NO FROM [345].[dbo].[345---------001TPOWATSECPUM---VAL001] ORDER BY EQUIPMENT_NO";
            DataSet dsPump = new DataSet();


            SqlDataAdapter adapter = new SqlDataAdapter();
            adapter.SelectCommand = new SqlCommand(queryPump, dbConnection);
            adapter.Fill(dsPump, "EQUIPMENT_NO");
            int ct = 0;
            foreach (DataRow data in dsPump.Tables[0].Rows)
            {

                dbQueryStringm = "SELECT [TIMESTAMP],([VALUE]+" + ct + ") AS Value FROM [345].[dbo].[345---------001TPOWATSECPUM---VAL001] WHERE EQUIPMENT_NO= '" + data[0] + "' AND [RUNTIME] = '" + runtime + "'  ORDER BY [TIMESTAMP]";


                myCommand = new SqlCommand(dbQueryStringm, dbConnection);
                myCommand.Connection.Open();
                myReader = myCommand.ExecuteReader(CommandBehavior.CloseConnection);
                m = new Series("Series" + 4 + ct);
                m.ChartType = SeriesChartType.FastLine;
                m.ShadowColor = System.Drawing.ColorTranslator.FromHtml("#FFCC66");
                m.BorderColor = System.Drawing.ColorTranslator.FromHtml("#FFCC66");
                m.Points.DataBindXY(myReader, "TIMESTAMP", myReader, "Value");
                m.LegendText = data[0].ToString();
                Chart3.Series.Add(m);

                ct++;
            }


            // Close  the connection
            dbConnection.Close();


        }


    }
}
