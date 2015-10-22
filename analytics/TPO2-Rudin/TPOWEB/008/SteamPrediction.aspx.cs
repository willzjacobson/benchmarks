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
    public partial class diboss_008_SteamPrediction : System.Web.UI.Page
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
                DateFrom.Text = DateTime.Now.AddDays(-8).ToShortDateString();
                DateTo.Text = DateTime.Now.AddDays(1).ToShortDateString();
                fromDate = DateTime.Today.AddDays(-7);
                toDate = DateTime.Today.AddDays(2);
            }
            else
            {
                if (DateRange.SelectedItem.Value == "default")
                {
                    useDateRange = false;
                    fromDate = DateTime.Today.AddDays(-1);
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

            Chart1.Series["Series1"].ChartType = SeriesChartType.Line;
            Chart1.ChartAreas[0].AxisX.MinorTickMark.Enabled = true;
            
            //AddHorizGreenStripLines();
            //AddHorizYellowStripLines1();
            //AddHorizYellowStripLines2();

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
            // Initialize a connection string    
            string dbConnectionString = ConfigurationManager.ConnectionStrings["TPOWEB"].ToString();

            SqlConnection dbConnection = new SqlConnection(dbConnectionString);

            //sensorlist
            string sensorid = "";
            string sensorname = "";
            string querySensor = "SELECT DISTINCT TABLE_NAME, REPLACE(TABLE_NAME, '008_Prediction_', '') AS SHORT_NAME FROM Prediction_CONFIG WHERE TABLE_NAME LIKE '%008_Prediction_STEAM%' ORDER BY TABLE_NAME";
            DataSet dsSensor = new DataSet();
            string dbQueryString;
            string dbQueryStringa;
            string dbQueryStringm;
            string dbQueryPreheatTime;
            string dbQueryStartUpTime;
            string dbQueryRampDownTime;
            SqlCommand myCommand;
            SqlDataReader myReader;
            Series s;
            Series s_upper;
            Series a;
            Series m;
            int i = 0;

            SqlDataAdapter adapter = new SqlDataAdapter();
            adapter.SelectCommand = new SqlCommand(querySensor, dbConnection);
            adapter.Fill(dsSensor, "Sensor_Data");

            SensorTypeList.DataSource = dsSensor;
            SensorTypeList.DataMember = "Sensor_Data";
            SensorTypeList.DataTextField = "SHORT_NAME";
            SensorTypeList.DataValueField = "TABLE_NAME";
            SensorTypeList.DataBind();

            //if (!Page.IsPostBack)
            //{
                SensorTypeList.Items[0].Selected = true;
            //}

            foreach (ListItem sti in SensorTypeList.Items)
            {
                if (sti.Selected)
                {
                    sensorid = sti.Value ;
                    sensorname = sti.Text;
                }
            }

            //chart series    
            dbQueryString = "SELECT [TIMESTAMP] AS TIMESTAMP, Prediction, [Lower_Bound_95] AS Lower, [Upper_Bound_95] AS Upper, [Lower_Bound_68] AS Lower2, [Upper_Bound_68] AS Upper2 FROM [" + sensorid + "] where (TIMESTAMP > '" + fromDate.ToString() + "') AND (TIMESTAMP < '" + toDate.ToString() + "') ORDER BY TIMESTAMP";

            dbQueryStringa = "SELECT Value AS Actual, TIMESTAMP FROM [41M].dbo.[41M---------008BMSSTEMET------VAL001] where (TIMESTAMP > '" + fromDate.ToString() + "') AND (TIMESTAMP < '" + toDate.ToString() + "') ORDER BY TIMESTAMP";

            dbQueryStringm = "SELECT [Prediction_Date] AS TIMESTAMP, [RMSE] AS Value FROM [41M].[dbo].[41M---------000TPOFORSTECON001---001_Stats] WHERE ([Prediction_Date] > '" + fromDate.ToString() + "') AND (Prediction_Date < '" + toDate.ToString() + "') ORDER BY [Prediction_Date]";

            if (ShowBounds.Checked)
            {
                myCommand = new SqlCommand(dbQueryString, dbConnection);
                myCommand.Connection.Open();
                myReader = myCommand.ExecuteReader(CommandBehavior.Default);
                s_upper = new Series("Series_upper");
                s_upper.ChartType = SeriesChartType.SplineRange;
                s_upper.YValuesPerPoint = 2;
                s_upper.Points.DataBindXY(myReader, "TIMESTAMP", myReader, "Upper,Lower");
                s_upper.Color = System.Drawing.ColorTranslator.FromHtml("#FFCCCC");
                s_upper.BorderColor = System.Drawing.Color.White;
                s_upper["LineTension"] = "1.2";
                s_upper.LegendText = "Upper/Lower Bound (95% confidence)";
                Chart1.Series.Add(s_upper);

                myCommand.Connection.Close();

            }

            if (ShowBounds2.Checked)
            {
                myCommand = new SqlCommand(dbQueryString, dbConnection);
                myCommand.Connection.Open();
                myReader = myCommand.ExecuteReader(CommandBehavior.Default);
                s_upper = new Series("Series_upper2");
                s_upper.ChartType = SeriesChartType.SplineRange;
                s_upper.YValuesPerPoint = 2;
                s_upper.Points.DataBindXY(myReader, "TIMESTAMP", myReader, "Upper2,Lower2");
                s_upper.Color = System.Drawing.ColorTranslator.FromHtml("#FF8C00");
                s_upper.BorderColor = System.Drawing.Color.White;
                s_upper["LineTension"] = "1.2";
                s_upper.LegendText = "Upper/Lower Bound (68% confidence)";
                Chart1.Series.Add(s_upper);

                myCommand.Connection.Close();

            }

            myCommand = new SqlCommand(dbQueryString, dbConnection);
            myCommand.Connection.Open();
            myReader = myCommand.ExecuteReader(CommandBehavior.CloseConnection);

            // Since the reader implements and IEnumerable, pass the reader directly into
            // the DataBindTable method with the name of the Column to be used as the XValue
            //Chart1.DataBindTable(myReader, "DateTime");
            s = new Series("Series" + 1);
            s.ChartType = SeriesChartType.FastLine;
            s.ShadowColor = System.Drawing.ColorTranslator.FromHtml("#FFCC66");
            s.BorderColor = System.Drawing.ColorTranslator.FromHtml("#FFCC66");
            s.Color = System.Drawing.ColorTranslator.FromHtml("#FF0000");
            s.Points.DataBindXY(myReader, "TIMESTAMP", myReader, "Prediction");
            s.LegendText = "Prediction";
            Chart1.Series.Add(s);

            myCommand = new SqlCommand(dbQueryStringa, dbConnection);
            myCommand.Connection.Open();
            myReader = myCommand.ExecuteReader(CommandBehavior.CloseConnection);
            a = new Series("Series" + 2);
            a.ChartType = SeriesChartType.FastLine;
            a.ShadowColor = System.Drawing.ColorTranslator.FromHtml("#FFCC66");
            a.BorderColor = System.Drawing.ColorTranslator.FromHtml("#FFCC66");
            a.Color = System.Drawing.ColorTranslator.FromHtml("#3300CC");
            a.Points.DataBindXY(myReader, "TIMESTAMP", myReader, "Actual");
            a.LegendText = "Actual";
            Chart1.Series.Add(a);


            //Preheat start-up ramp-down series
            /* No preheat for 40E52
            dbQueryPreheatTime = "SELECT 40 AS Value, TIMESTAMP FROM [001_Prediction_Preheat_Time] WHERE (TIMESTAMP > '" + fromDate.ToString() + "') AND (TIMESTAMP < '" + toDate.ToString() + "') ORDER BY TIMESTAMP";
            myCommand = new SqlCommand(dbQueryPreheatTime, dbConnection);
            myCommand.Connection.Open();
            myReader = myCommand.ExecuteReader(CommandBehavior.CloseConnection);
            s = new Series("Series Preaheat Time");
            s.ChartType = SeriesChartType.Point;
            s.ShadowColor = System.Drawing.ColorTranslator.FromHtml("#FFCC66");
            s.BorderColor = System.Drawing.ColorTranslator.FromHtml("#FFCC66");
            s.Color = System.Drawing.ColorTranslator.FromHtml("#FF00FF");
            s.MarkerSize = 10;
            s.MarkerStyle = MarkerStyle.Triangle;
            s.LegendText = "Preheat Time";
            s.ToolTip = "Preheat Time: #TIMESTAMP";
            s.Points.DataBind(myReader, "TIMESTAMP", "Value", "Tooltip=TIMESTAMP{F}");
            Chart1.Series.Add(s);
             * */

            dbQueryStartUpTime = "SELECT 30 AS Value, TIMESTAMP FROM [008_Prediction_Start_Up_Time] WHERE (TIMESTAMP > '" + fromDate.ToString() + "') AND (TIMESTAMP < '" + toDate.ToString() + "') ORDER BY TIMESTAMP";
            myCommand = new SqlCommand(dbQueryStartUpTime, dbConnection);
            myCommand.Connection.Open();
            myReader = myCommand.ExecuteReader(CommandBehavior.CloseConnection);
            s = new Series("Series Start-Up Time");
            s.ChartType = SeriesChartType.Point;
            s.ShadowColor = System.Drawing.ColorTranslator.FromHtml("#FFCC66");
            s.BorderColor = System.Drawing.ColorTranslator.FromHtml("#FFCC66");
            s.Color = System.Drawing.ColorTranslator.FromHtml("#CC0000");
            s.MarkerSize = 10;
            s.MarkerStyle = MarkerStyle.Square;
            s.LegendText = "Start-Up Time";
            s.ToolTip = "Start-Up Time: #TIMESTAMP";
            s.Points.DataBind(myReader, "TIMESTAMP", "Value", "Tooltip=TIMESTAMP{F}");
            Chart1.Series.Add(s);

            dbQueryRampDownTime = "SELECT 0 AS Value, TIMESTAMP FROM [008_Prediction_Ramp_Down_Time] WHERE (TIMESTAMP > '" + fromDate.ToString() + "') AND (TIMESTAMP < '" + toDate.ToString() + "') ORDER BY TIMESTAMP";
            myCommand = new SqlCommand(dbQueryRampDownTime, dbConnection);
            myCommand.Connection.Open();
            myReader = myCommand.ExecuteReader(CommandBehavior.CloseConnection);
            s = new Series("Series Ramp-Down Time");
            s.ChartType = SeriesChartType.Point;
            s.ShadowColor = System.Drawing.ColorTranslator.FromHtml("#FFCC66");
            s.BorderColor = System.Drawing.ColorTranslator.FromHtml("#FFCC66");
            s.Color = System.Drawing.ColorTranslator.FromHtml("#0000FF");
            s.MarkerSize = 10;
            s.MarkerStyle = MarkerStyle.Circle;
            s.LegendText = "Ramp-Down Time";
            s.ToolTip = "Ramp-Down Time: #TIMESTAMP";
            s.Points.DataBind(myReader, "TIMESTAMP", "Value", "Tooltip=TIMESTAMP{F}");
            Chart1.Series.Add(s);

            myCommand = new SqlCommand(dbQueryStringm, dbConnection);
            myCommand.Connection.Open();
            myReader = myCommand.ExecuteReader(CommandBehavior.CloseConnection);
            m = new Series("Series" + 3);
            m.ChartType = SeriesChartType.FastLine;
            m.ShadowColor = System.Drawing.ColorTranslator.FromHtml("#FFCC66");
            m.BorderColor = System.Drawing.ColorTranslator.FromHtml("#FFCC66");
            m.Points.DataBindXY(myReader, "TIMESTAMP", myReader, "Value");
            m.LegendText = "RMSE";
            Chart2.Series.Add(m);

            // Close the reader and the connection
            myReader.Close();
            dbConnection.Close();

        }

        private void AddHorizGreenStripLines()
        {
            // Instantiate new strip line
            StripLine stripLine1 = new StripLine();
            stripLine1.StripWidth = 3;
            stripLine1.BorderColor = Color.Green;
            stripLine1.BorderWidth = 1;
            stripLine1.Interval = 18;
            stripLine1.IntervalOffset = 12;

            // Consider adding transparency so that the strip lines are lighter
            stripLine1.BackColor = Color.FromArgb(120, Color.Green);
            //stripLine1.BackSecondaryColor = Color.Black;
            //stripLine1.BackGradientStyle = GradientStyle.LeftRight;

            // Add the strip line to the chart
            Chart1.ChartAreas[0].AxisY.StripLines.Add(stripLine1);
        }

        private void AddHorizYellowStripLines1()
        {
            // Instantiate new strip line
            StripLine stripLine1 = new StripLine();
            stripLine1.StripWidth = 2;
            stripLine1.BorderColor = Color.Yellow;
            stripLine1.BorderWidth = 1;
            stripLine1.Interval = 18;
            stripLine1.IntervalOffset = 10;

            // Consider adding transparency so that the strip lines are lighter
            stripLine1.BackColor = Color.FromArgb(120, Color.Yellow);
            //stripLine1.BackSecondaryColor = Color.Black;
            //stripLine1.BackGradientStyle = GradientStyle.LeftRight;

            // Add the strip line to the chart
            Chart1.ChartAreas[0].AxisY.StripLines.Add(stripLine1);
        }

        private void AddHorizYellowStripLines2()
        {
            // Instantiate new strip line
            StripLine stripLine1 = new StripLine();
            stripLine1.StripWidth = 2;
            stripLine1.BorderColor = Color.Yellow;
            stripLine1.BorderWidth = 1;
            stripLine1.Interval = 18;
            stripLine1.IntervalOffset = 15;

            // Consider adding transparency so that the strip lines are lighter
            stripLine1.BackColor = Color.FromArgb(120, Color.Yellow);
            //stripLine1.BackSecondaryColor = Color.Black;
            //stripLine1.BackGradientStyle = GradientStyle.LeftRight;

            // Add the strip line to the chart
            Chart1.ChartAreas[0].AxisY.StripLines.Add(stripLine1);
        }

    }
}
