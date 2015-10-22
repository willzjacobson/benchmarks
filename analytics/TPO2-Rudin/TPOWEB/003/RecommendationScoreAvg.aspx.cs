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
    public partial class diboss_003_RecommendationScoreAvg : System.Web.UI.Page
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
                DateFrom.Text = DateTime.Now.AddDays(-90).ToShortDateString();
                DateTo.Text = DateTime.Now.AddDays(1).ToShortDateString();
                fromDate = DateTime.Today.AddDays(-90)/*.AddDays(-1)*/;
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
            SqlCommand myCommand;
            SqlDataReader myReader;
            Series m;

            dbQueryStringms = "SELECT [Actual_DateTime] AS TIMESTAMP, [Agreed]*100 AS Value, (SELECT AVG(a.[Agreed])*100 FROM [4E5].dbo.[Score_Startup_Rampdown] a WHERE a.[Actual_DateTime] >= DATEADD(dd,-14,b.[Actual_DateTime]) AND a.[Actual_DateTime] < b.[Actual_DateTime]) AS Value_AVG FROM [4E5].dbo.[Score_Startup_Rampdown] b WHERE (b.[Actual_DateTime] > '" + fromDate.ToString() + "') AND (b.Actual_DateTime < '" + toDate.ToString() + "') AND ((DATEPART(dw, b.[Actual_DateTime]) + @@DATEFIRST) % 7) NOT IN (0, 1) AND [Tag] = 'startup' AND UPPER(Building) = '4E5' and [Agreed] is not null and [Actual_DateTime] is not null ORDER BY b.[Actual_DateTime]";

            dbQueryStringmr = "SELECT [Actual_DateTime] AS TIMESTAMP, [Agreed]*100 AS Value, (SELECT AVG(a.[Agreed])*100 FROM [4E5].dbo.[Score_Startup_Rampdown] a WHERE a.[Actual_DateTime] >= DATEADD(dd,-14,b.[Actual_DateTime]) AND a.[Actual_DateTime] < b.[Actual_DateTime]) AS Value_AVG FROM [4E5].dbo.[Score_Startup_Rampdown] b WHERE (b.[Actual_DateTime] > '" + fromDate.ToString() + "') AND (b.Actual_DateTime < '" + toDate.ToString() + "') AND ((DATEPART(dw, b.[Actual_DateTime]) + @@DATEFIRST) % 7) NOT IN (0, 1) AND [Tag] = 'rampdown' AND UPPER(Building) = '4E5' and [Agreed] is not null and [Actual_DateTime] is not null ORDER BY b.[Actual_DateTime]";


            myCommand = new SqlCommand(dbQueryStringms, dbConnection);
            myCommand.Connection.Open();
            myReader = myCommand.ExecuteReader(CommandBehavior.CloseConnection);
            m = new Series("Series" + 2);
            m.ChartType = SeriesChartType.FastLine;
            m.ShadowColor = System.Drawing.ColorTranslator.FromHtml("#FFCC66");
            m.BorderColor = System.Drawing.ColorTranslator.FromHtml("#FFCC66");
            m.Points.DataBindXY(myReader, "TIMESTAMP", myReader, "Value_Avg");
            m.LegendText = "Excluding Weekends";
            Chart3.Series.Add(m);

            myCommand = new SqlCommand(dbQueryStringmr, dbConnection);
            myCommand.Connection.Open();
            myReader = myCommand.ExecuteReader(CommandBehavior.CloseConnection);
            m = new Series("Series" + 3);
            m.ChartType = SeriesChartType.FastLine;
            m.ShadowColor = System.Drawing.ColorTranslator.FromHtml("#FFCC66");
            m.BorderColor = System.Drawing.ColorTranslator.FromHtml("#FFCC66");
            m.Points.DataBindXY(myReader, "TIMESTAMP", myReader, "Value_Avg");
            m.LegendText = "Excluding Weekends";
            Chart4.Series.Add(m);

            // Close the reader and the connection
            myReader.Close();
            dbConnection.Close();


        }
        
    }
}
