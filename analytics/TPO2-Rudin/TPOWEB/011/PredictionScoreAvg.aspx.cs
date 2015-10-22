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
    public partial class diboss_011_PredictionScoreAvg : System.Web.UI.Page
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
            string sensorid = "";
            string sensorname = "";
            int i = 0;
            
            if (!Page.IsPostBack)
            {
            // Initialize a connection string    
            string dbConnectionString = ConfigurationManager.ConnectionStrings["TPOWEB"].ToString();

            SqlConnection dbConnection = new SqlConnection(dbConnectionString);


            string querySensor = "SELECT DISTINCT TABLE_NAME, REPLACE(TABLE_NAME, '011_Prediction_Space_Temperature_', '') AS SHORT_NAME FROM Prediction_CONFIG WHERE TABLE_NAME LIKE '%011_Prediction_Space_Temperature%' ORDER BY TABLE_NAME";
            DataSet dsSensor = new DataSet();


            SqlDataAdapter adapter = new SqlDataAdapter();
            adapter.SelectCommand = new SqlCommand(querySensor, dbConnection);
            adapter.Fill(dsSensor, "Sensor_Data");

            SensorTypeList.DataSource = dsSensor;
            SensorTypeList.DataMember = "Sensor_Data";
            SensorTypeList.DataTextField = "SHORT_NAME";
            SensorTypeList.DataValueField = "TABLE_NAME";
            SensorTypeList.DataBind();

            
                //SensorTypeList.Items[0].Selected = true;
                foreach (ListItem sti in SensorTypeList.Items)
                {
                    if (sti.Text == "2_CSO")
                    {
                        sti.Selected = true;
                    }
                }
               // sensorid = "Prediction_Space_Temperature_13_SW";
               // sensorname = "13_SW";

               // PlotChart(sensorid, sensorname);
            }
            /* else
            {
                 //if (SensorTypeList.SelectedIndex > -1)
                 {
                     sensorid = SensorTypeList.SelectedItem.Value;
                     sensorname = SensorTypeList.SelectedItem.Text;

                     PlotChart(sensorid, sensorname);
                 }
            } */

            foreach (ListItem sti in SensorTypeList.Items)
            {
                if (sti.Selected)
                {
                    sensorid = sti.Value;
                    sensorname = sti.Text;

                    i++;

                    PlotTempScoreChart(sensorid, sensorname, i);

                }
            }
            PlotScoreChart();
        }

        private void PlotScoreChart()
        {

            // Initialize a connection string    
            string dbConnectionString = ConfigurationManager.ConnectionStrings["TPOWEB"].ToString();

            SqlConnection dbConnection = new SqlConnection(dbConnectionString);

            string dbQueryStringme;
            string dbQueryStringmo;

            SqlCommand myCommand;
            SqlDataReader myReader;
            Series m;

            dbQueryStringme = "SELECT Prediction_Date AS TIMESTAMP, RMSE AS Value, (SELECT AVG(a.[RMSE]) FROM [845].dbo.[845---------000TPOFORELECON001---001_stats] a WHERE a.[Prediction_Date] >= DATEADD(dd,-14,b.[Prediction_Date]) AND a.[Prediction_Date] < b.[Prediction_Date]) AS Value_AVG FROM [845].dbo.[845---------000TPOFORELECON001---001_stats] b WHERE (b.[Prediction_Date] > '" + fromDate.ToString() + "') AND (b.Prediction_Date < '" + toDate.ToString() + "') AND ((DATEPART(dw, b.[Prediction_Date]) + @@DATEFIRST) % 7) NOT IN (0, 1) ORDER BY b.[Prediction_Date]";

            dbQueryStringmo = "SELECT Prediction_Date AS TIMESTAMP, RMSE AS Value, (SELECT AVG(a.[RMSE]) FROM [845].dbo.[845---------000TPOFORPEOBUI001---001_stats] a WHERE a.[Prediction_Date] >= DATEADD(dd,-14,b.[Prediction_Date]) AND a.[Prediction_Date] < b.[Prediction_Date]) AS Value_AVG FROM [845].dbo.[845---------000TPOFORPEOBUI001---001_stats] b WHERE (b.[Prediction_Date] > '" + fromDate.ToString() + "') AND (b.Prediction_Date < '" + toDate.ToString() + "') AND ((DATEPART(dw, b.[Prediction_Date]) + @@DATEFIRST) % 7) NOT IN (0, 1) ORDER BY b.[Prediction_Date]";

            myCommand = new SqlCommand(dbQueryStringme, dbConnection);
            myCommand.Connection.Open();
            myReader = myCommand.ExecuteReader(CommandBehavior.CloseConnection);
            m = new Series("Series" + 1);
            m.ChartType = SeriesChartType.FastLine;
            m.ShadowColor = System.Drawing.ColorTranslator.FromHtml("#FFCC66");
            m.BorderColor = System.Drawing.ColorTranslator.FromHtml("#FFCC66");
            m.Points.DataBindXY(myReader, "TIMESTAMP", myReader, "Value_Avg");
            m.LegendText = "RMSE (Root Mean Square Error) Excluding Weekends";
            Chart1.Series.Add(m);

            myCommand = new SqlCommand(dbQueryStringmo, dbConnection);
            myCommand.Connection.Open();
            myReader = myCommand.ExecuteReader(CommandBehavior.CloseConnection);
            m = new Series("Series" + 3);
            m.ChartType = SeriesChartType.FastLine;
            m.ShadowColor = System.Drawing.ColorTranslator.FromHtml("#FFCC66");
            m.BorderColor = System.Drawing.ColorTranslator.FromHtml("#FFCC66");
            m.Points.DataBindXY(myReader, "TIMESTAMP", myReader, "Value_Avg");
            m.LegendText = "RMSE (Root Mean Square Error) Excluding Weekends";
            Chart4.Series.Add(m);

            // Close the reader and the connection
            myReader.Close();
            dbConnection.Close();


        }
        

        private void PlotTempScoreChart(string sensorid, string sensorname, int i)
        {

            // Initialize a connection string    
            string dbConnectionString = ConfigurationManager.ConnectionStrings["TPOWEB"].ToString();

            SqlConnection dbConnection = new SqlConnection(dbConnectionString);

            string dbQueryString;
            string dbQueryStringA;
            string dbQueryStringm;

            SqlCommand myCommand;
            SqlDataReader myReader;
            string fl;
            if (sensorname.IndexOf("_") == 1)
            {
                fl = "F0" + sensorname.Substring(0, (sensorname.IndexOf("_")));
            }
            else
            {
                fl = "F" + sensorname.Substring(0, (sensorname.IndexOf("_")));
            }
            string qd = sensorname.Substring((sensorname.IndexOf("_") + 3)); 
            Series m;


            //chart series    
            dbQueryString = "SELECT [Prediction_DateTime] AS TIMESTAMP, [Prediction_Value] AS Prediction, [Lower_Bound_95] AS Lower, [Upper_Bound_95] AS Upper, [Lower_Bound_68] AS Lower2, [Upper_Bound_68] AS Upper2 FROM [" + sensorid + "] where ([Prediction_DateTime] > '" + fromDate.ToString() + "') AND ([Prediction_DateTime] < '" + toDate.ToString() + "') ORDER BY [Prediction_DateTime]";

            dbQueryStringA = "SELECT TIMESTAMP, Value as Actual FROM [011_Actual_Space_Temperature_" + sensorname + "] where (TIMESTAMP > '" + fromDate.ToString() + "') AND (TIMESTAMP < '" + toDate.ToString() + "') ORDER BY TIMESTAMP";


            dbQueryStringm = "SELECT Prediction_Date AS TIMESTAMP, RMSE AS Value, (SELECT AVG(a.[RMSE]) FROM [845].dbo.[845---------000TPOFORTEMSPA001---001_Stats] a WHERE a.[Prediction_Date] >= DATEADD(dd,-14,b.[Prediction_Date]) AND a.[Prediction_Date] < b.[Prediction_Date] AND (Floor = '" + fl + "' AND Quadrant  = '" + qd + "')) AS Value_AVG FROM [845].dbo.[845---------000TPOFORTEMSPA001---001_Stats] b WHERE (b.[Prediction_Date] > '" + fromDate.ToString() + "') AND (b.Prediction_Date < '" + toDate.ToString() + "') AND ((DATEPART(dw, b.[Prediction_Date]) + @@DATEFIRST) % 7) NOT IN (0, 1) AND (Floor = '" + fl + "' AND Quadrant  = '" + qd + "') ORDER BY b.[Prediction_Date]";

            myCommand = new SqlCommand(dbQueryStringm, dbConnection);
            myCommand.Connection.Open();
            myReader = myCommand.ExecuteReader(CommandBehavior.CloseConnection);
            m = new Series("Series_Temp" + i);
            m.ChartType = SeriesChartType.FastLine;
            m.ShadowColor = System.Drawing.ColorTranslator.FromHtml("#FFCC66");
            m.BorderColor = System.Drawing.ColorTranslator.FromHtml("#FFCC66");
            m.Points.DataBindXY(myReader, "TIMESTAMP", myReader, "Value_Avg");
            m.ToolTip = sensorname;
            //m.LegendText = "RMSE (Root Mean Square Error) Excluding Weekends";
            Chart2.Series.Add(m);

            // Close the reader and the connection
            myReader.Close();
            dbConnection.Close();
        }
    }
}
