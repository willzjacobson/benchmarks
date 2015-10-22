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
    public partial class diboss_004_Weather_History : System.Web.UI.Page
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

            if (!Page.IsPostBack)
            {
                DateFrom.Text = DateTime.Now.AddDays(-30).ToShortDateString();
                DateTo.Text = DateTime.Now.AddDays(1).ToShortDateString();
                fromDate = DateTime.Today.AddDays(-30)/*.AddDays(-1)*/;
                toDate = DateTime.Today.AddDays(2);
            }
            else
            {
                if (DateRange.SelectedItem.Value == "default")
                {
                    useDateRange = false;
                    fromDate = DateTime.Today.AddDays(-1)/*.AddDays(-1)*/;
                    toDate = DateTime.Today.AddDays(2);
                }
                else
                {
                    useDateRange = true;
                    //if (DateFrom.Text != "" && DateTo.Text != "")
                    //{
                    fromDate = Convert.ToDateTime(DateFrom.Text);
                    toDate = Convert.ToDateTime(DateTo.Text);
                    //} else {
                    //fromDate = DateTime.Now.AddDays(-2);
                    //toDate = DateTime.Now;
                    //}

                }


            }

            PlotScoreChart();

            
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


        private void PlotScoreChart()
        {

            // Initialize a connection string    
            string dbConnectionString = ConfigurationManager.ConnectionStrings["TPOWEB"].ToString();

            SqlConnection dbConnection = new SqlConnection(dbConnectionString);

            string dbQueryStringms;
            string dbQueryStringmr;
            string dbQueryStringmh;
            SqlCommand myCommand;
            SqlDataReader myReader;
            Series m;

            dbQueryStringms = "SELECT [Date] AS TIMESTAMP, [TempA] AS Value FROM [TPOWEB].[dbo].[Weather_Observations_History] b WHERE (b.[Date] > '" + fromDate.ToString() + "') AND (b.[Date] < '" + toDate.ToString() + "') AND [TempA] > -100 ORDER BY b.[Date]";

            dbQueryStringmr = "SELECT [Date] AS TIMESTAMP, [DewPointA] AS Value FROM [TPOWEB].[dbo].[Weather_Observations_History] b WHERE (b.[Date] > '" + fromDate.ToString() + "') AND (b.[Date] < '" + toDate.ToString() + "') AND [DewPointA] > -100 ORDER BY b.[Date]";

            dbQueryStringmh = "SELECT [Date] AS TIMESTAMP, [Humidity] AS Value FROM [TPOWEB].[dbo].[Weather_Observations_History] b WHERE (b.[Date] > '" + fromDate.ToString() + "') AND (b.[Date] < '" + toDate.ToString() + "') AND [Humidity] > -100 ORDER BY b.[Date]";


            myCommand = new SqlCommand(dbQueryStringms, dbConnection);
            myCommand.Connection.Open();
            myReader = myCommand.ExecuteReader(CommandBehavior.CloseConnection);
            m = new Series("Series" + 2);
            m.ChartType = SeriesChartType.FastLine;
            m.ShadowColor = System.Drawing.ColorTranslator.FromHtml("#FFCC66");
            m.BorderColor = System.Drawing.ColorTranslator.FromHtml("#FFCC66");
            m.Points.DataBindXY(myReader, "TIMESTAMP", myReader, "Value");
            m.LegendText = "Temperature";
            Chart3.Series.Add(m);

            myCommand = new SqlCommand(dbQueryStringmr, dbConnection);
            myCommand.Connection.Open();
            myReader = myCommand.ExecuteReader(CommandBehavior.CloseConnection);
            m = new Series("Series" + 3);
            m.ChartType = SeriesChartType.FastLine;
            m.ShadowColor = System.Drawing.ColorTranslator.FromHtml("#FFCC66");
            m.BorderColor = System.Drawing.ColorTranslator.FromHtml("#FFCC66");
            m.Points.DataBindXY(myReader, "TIMESTAMP", myReader, "Value");
            m.LegendText = "DewPoint";
            Chart4.Series.Add(m);

            myCommand = new SqlCommand(dbQueryStringmh, dbConnection);
            myCommand.Connection.Open();
            myReader = myCommand.ExecuteReader(CommandBehavior.CloseConnection);
            m = new Series("Series" + 3);
            m.ChartType = SeriesChartType.FastLine;
            m.ShadowColor = System.Drawing.ColorTranslator.FromHtml("#FFCC66");
            m.BorderColor = System.Drawing.ColorTranslator.FromHtml("#FFCC66");
            m.Points.DataBindXY(myReader, "TIMESTAMP", myReader, "Value");
            m.LegendText = "Humidity";
            Chart1.Series.Add(m);

            // Close the reader and the connection
            myReader.Close();
            dbConnection.Close();


        }
        
    }
}
