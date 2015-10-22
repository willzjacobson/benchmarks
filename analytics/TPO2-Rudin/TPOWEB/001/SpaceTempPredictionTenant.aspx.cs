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
    public partial class diboss_001_SpaceTempPredictionTenant : System.Web.UI.Page
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
                DateFrom.Text = DateTime.Now.AddDays(-7).ToShortDateString();
                DateTo.Text = DateTime.Now.AddDays(1).ToShortDateString();
                fromDate = DateTime.Today.AddDays(-7)/*.AddDays(-1)*/;
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

            Chart1.Series["Series1"].ChartType = SeriesChartType.Line;
            Chart1.ChartAreas[0].AxisX.MinorTickMark.Enabled = true;
            
            AddHorizGreenStripLines();
            AddHorizGreenStripLines2();
            AddHorizYellowStripLines1();
            AddHorizYellowStripLines2();

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
            
            if (!Page.IsPostBack)
            {
            // Initialize a connection string    
            string dbConnectionString = ConfigurationManager.ConnectionStrings["TPOWEB"].ToString();

            SqlConnection dbConnection = new SqlConnection(dbConnectionString);


            string querySensor = "SELECT DISTINCT TABLE_NAME, REPLACE(TABLE_NAME, '001_Prediction_Space_Temperature_', '') AS SHORT_NAME FROM Prediction_CONFIG WHERE TABLE_NAME LIKE '%001_Prediction_Space_Temperature%' AND TABLE_NAME IN ('001_Prediction_Space_Temperature_13_SW', '001_Prediction_Space_Temperature_2_NW', '001_Prediction_Space_Temperature_4_NW','001_Prediction_Space_Temperature_38_NW','001_Prediction_Space_Temperature_40_NE') ORDER BY TABLE_NAME";
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
                    if (sti.Text == "2_NW")
                    {
                        sti.Selected = true;
                    }
                }
               // sensorid = "Prediction_Space_Temperature_13_SW";
               // sensorname = "13_SW";

               // PlotChart(sensorid, sensorname);
            }
           // else
           // {
                if (SensorTypeList.SelectedIndex > -1)
                {
                    sensorid = SensorTypeList.SelectedItem.Value;
                    sensorname = SensorTypeList.SelectedItem.Text;

                    PlotChart(sensorid, sensorname);
                }
          //  }
        }


        private void PlotChart(string sensorid, string sensorname)
        {

            // Initialize a connection string    
            string dbConnectionString = ConfigurationManager.ConnectionStrings["TPOWEB"].ToString();

            SqlConnection dbConnection = new SqlConnection(dbConnectionString);

            string dbQueryString;
            string dbQueryStringA;
            string dbQueryStringm;
            SqlCommand myCommand;
            SqlDataReader myReader;
            string dbQueryStartUpTime;
            string dbQueryRampDownTime;
            string sensorSATid;
            string fl;
            string dbQueryStringSAT;
            string dbQueryStringSATSP;
            string dbQueryStringVariance;
            string dbQueryStringArrow;
            Series s;
            Series s_upper;
            Series a;
            Series m;
            int i = 0;

            //chart series    
            dbQueryString = "SELECT [Prediction_DateTime] AS TIMESTAMP, [Prediction_Value] AS Prediction, [Lower_Bound_95] AS Lower, [Upper_Bound_95] AS Upper, [Lower_Bound_68] AS Lower2, [Upper_Bound_68] AS Upper2 FROM [" + sensorid + "] where ([Prediction_DateTime] > '" + fromDate.ToString() + "') AND ([Prediction_DateTime] < '" + toDate.ToString() + "') ORDER BY [Prediction_DateTime]";

            dbQueryStringA = "SELECT TIMESTAMP, Value as Actual FROM [001_Actual_Space_Temperature_" + sensorname + "] where (TIMESTAMP > '" + fromDate.ToString() + "') AND (TIMESTAMP < '" + toDate.ToString() + "') ORDER BY TIMESTAMP";

           
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
            s.ToolTip = sensorname;
            Chart1.Series.Add(s);


            myCommand = new SqlCommand(dbQueryStringA, dbConnection);
            myCommand.Connection.Open();
            myReader = myCommand.ExecuteReader(CommandBehavior.CloseConnection);
            a = new Series("Series" + 2);
            a.ChartType = SeriesChartType.FastLine;
            a.ShadowColor = System.Drawing.ColorTranslator.FromHtml("#FFCC66");
            a.BorderColor = System.Drawing.ColorTranslator.FromHtml("#FFCC66");
            a.Color = System.Drawing.ColorTranslator.FromHtml("#3300CC");
            a.Points.DataBindXY(myReader, "TIMESTAMP", myReader, "Actual");
            a.LegendText = "Actual";
            a.ToolTip = sensorname;
            Chart1.Series.Add(a);


            //start-up ramp-down series
            dbQueryStartUpTime = "SELECT 80 AS Value, TIMESTAMP FROM [001_Prediction_Start_Up_Time] WHERE (TIMESTAMP > '" + fromDate.ToString() + "') AND (TIMESTAMP < '" + toDate.ToString() + "') ORDER BY TIMESTAMP";
            myCommand = new SqlCommand(dbQueryStartUpTime, dbConnection);
            myCommand.Connection.Open();
            myReader = myCommand.ExecuteReader(CommandBehavior.CloseConnection);
            s = new Series("Series Start-Up Time");
            s.ChartType = SeriesChartType.Point;
            s.ShadowColor = System.Drawing.ColorTranslator.FromHtml("#FFCC66");
            s.BorderColor = System.Drawing.ColorTranslator.FromHtml("#FFCC66");
            s.Color = System.Drawing.ColorTranslator.FromHtml("#CC0000");
            s.MarkerSize = 10;
            s.LegendText = "Start-Up Time";
            s.ToolTip = "Start-Up Time: #TIMESTAMP";
            s.Points.DataBind(myReader, "TIMESTAMP", "Value", "Tooltip=TIMESTAMP{F}");

            Chart1.Series.Add(s);

            dbQueryRampDownTime = "SELECT 65 AS Value, TIMESTAMP FROM [001_Prediction_Ramp_Down_Time] WHERE (TIMESTAMP > '" + fromDate.ToString() + "') AND (TIMESTAMP < '" + toDate.ToString() + "') ORDER BY TIMESTAMP";
            myCommand = new SqlCommand(dbQueryRampDownTime, dbConnection);
            myCommand.Connection.Open();
            myReader = myCommand.ExecuteReader(CommandBehavior.CloseConnection);
            s = new Series("Series Ramp-Down Time");
            s.ChartType = SeriesChartType.Point;
            s.ShadowColor = System.Drawing.ColorTranslator.FromHtml("#FFCC66");
            s.BorderColor = System.Drawing.ColorTranslator.FromHtml("#FFCC66");
            s.Color = System.Drawing.ColorTranslator.FromHtml("#0000FF");
            s.MarkerSize = 10;
            s.LegendText = "Ramp-Down Time";
            s.ToolTip = "Ramp-Down Time: #TIMESTAMP";
            s.Points.DataBind(myReader, "TIMESTAMP", "Value", "Tooltip=TIMESTAMP{F}");

            Chart1.Series.Add(s);


            switch (sensorname)
            {
                case "13_SW":
                    sensorSATid = "09";
                    fl = "13";
                    break;
                case "18_SE":
                    sensorSATid = "11";
                    fl = "18";
                    break;
                case "2_NW":
                    sensorSATid = "10";
                    fl = "02";
                    break;
                case "20_SW":
                    sensorSATid = "04";
                    fl = "20";
                    break;
                case "24_SE":
                    sensorSATid = "06";
                    fl = "24";
                    break;
                case "32_NW":
                    sensorSATid = "04";
                    fl = "32";
                    break;
                case "38_NW":
                    sensorSATid = "03";
                    fl = "38";
                    break;
                case "40_NE":
                    sensorSATid = "05";
                    fl = "40";
                    break;
                case "5_SE":
                    sensorSATid = "12";
                    fl = "05";
                    break;
                default:
                    sensorSATid = "09";
                    fl = "13";
                    break;
            }



            //chart series    
            dbQueryStringSAT = "SELECT Value, TIMESTAMP FROM [345].dbo.[345---------001BMSHVAFANSAT---VAL001] WHERE (EQUIPMENT_NO = '0" + sensorSATid + "') AND (TIMESTAMP > '" + fromDate.ToString() + "') AND (TIMESTAMP < '" + toDate.ToString() + "') ORDER BY TIMESTAMP";
            myCommand = new SqlCommand(dbQueryStringSAT, dbConnection);
            myCommand.Connection.Open();
            myReader = myCommand.ExecuteReader(CommandBehavior.CloseConnection);

            // Since the reader implements and IEnumerable, pass the reader directly into
            // the DataBindTable method with the name of the Column to be used as the XValue
            //Chart1.DataBindTable(myReader, "DateTime");
            s = new Series("Series_SAT" + 1);
            s.ChartType = SeriesChartType.FastLine;
            s.ShadowColor = System.Drawing.ColorTranslator.FromHtml("#FFCC66");
            s.BorderColor = System.Drawing.ColorTranslator.FromHtml("#FFCC66");
            s.Points.DataBindXY(myReader, "TIMESTAMP", myReader, "Value");
            s.LegendText = "S" + sensorSATid + "_SAT";
            s.ToolTip = s.LegendText;

            Chart1.Series.Add(s);

            //SAT set-points
            dbQueryStringSATSP = "SELECT Value, TIMESTAMP FROM [345].dbo.[345---------001BMSHVAFANSAT---SPV001] WHERE (EQUIPMENT_NO = '0" + sensorSATid + "') AND (TIMESTAMP > '" + fromDate.ToString() + "') AND (TIMESTAMP < '" + toDate.ToString() + "') ORDER BY TIMESTAMP";
            myCommand = new SqlCommand(dbQueryStringSATSP, dbConnection);
            myCommand.Connection.Open();
            myReader = myCommand.ExecuteReader(CommandBehavior.CloseConnection);

            // Since the reader implements and IEnumerable, pass the reader directly into
            // the DataBindTable method with the name of the Column to be used as the XValue
            //Chart1.DataBindTable(myReader, "DateTime");
            s = new Series("Series_SAT" + 2);
            s.ChartType = SeriesChartType.FastLine;
            s.ShadowColor = System.Drawing.ColorTranslator.FromHtml("#FFCC66");
            s.BorderColor = System.Drawing.ColorTranslator.FromHtml("#FFCC66");
            s.Color = System.Drawing.ColorTranslator.FromHtml("#989898");
            s.Points.DataBindXY(myReader, "TIMESTAMP", myReader, "Value");
            s.LegendText = "S" + sensorSATid + "_SAT_SP";
            s.ToolTip = s.LegendText;

            Chart1.Series.Add(s);


            dbQueryStringm = "SELECT [Prediction_Date] AS TIMESTAMP, [MAPE] AS Value FROM [345].dbo.[345---------000TPOFORTEMSPA001---001_Stats] WHERE ([Prediction_Date] > '" + fromDate.ToString() + "') AND (Prediction_Date < '" + toDate.ToString() + "') AND (Floor = 'F" + fl + "') ORDER BY [Prediction_Date]";

            myCommand = new SqlCommand(dbQueryStringm, dbConnection);
            myCommand.Connection.Open();
            myReader = myCommand.ExecuteReader(CommandBehavior.CloseConnection);
            m = new Series("Series" + 3);
            m.ChartType = SeriesChartType.FastLine;
            m.ShadowColor = System.Drawing.ColorTranslator.FromHtml("#FFCC66");
            m.BorderColor = System.Drawing.ColorTranslator.FromHtml("#FFCC66");
            m.Points.DataBindXY(myReader, "TIMESTAMP", myReader, "Value");
            m.LegendText = "MAPE";
            Chart2.Series.Add(m);

            //arrow for nowcast
            dbQueryStringArrow = "SELECT  [TIMESTAMP], [Value] FROM [dbo].[001_Prediction_Space_Temperature_" + sensorname + "_Start] UNION SELECT  [TIMESTAMP], [Value] FROM [dbo].[001_Prediction_Space_Temperature_" + sensorname + "_End] where (TIMESTAMP > '" + fromDate.ToString() + "') AND (TIMESTAMP < '" + toDate.ToString() + "') ORDER BY TIMESTAMP";

            if (ShowNowcast.Checked)
            {
                myCommand = new SqlCommand(dbQueryStringArrow, dbConnection);
                myCommand.Connection.Open();
                myReader = myCommand.ExecuteReader(CommandBehavior.CloseConnection);
                a = new Series("Series" + 4);
                a.ChartType = SeriesChartType.Line;
                a.ShadowColor = System.Drawing.ColorTranslator.FromHtml("#FFCC66");
                a.BorderColor = System.Drawing.ColorTranslator.FromHtml("#FFCC66");
                a.Color = System.Drawing.ColorTranslator.FromHtml("#ff0066");
                a.Points.DataBindXY(myReader, "TIMESTAMP", myReader, "Value");
                a.MarkerSize = 10;
                a.MarkerStep = 7;
                a.BorderWidth = 4;
                a.MarkerStyle = MarkerStyle.Triangle;
                a.LegendText = "Arrow";
                a.ToolTip = sensorname;
                Chart1.Series.Add(a);
            }

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
            stripLine1.Interval = 40;
            stripLine1.IntervalOffset = -18;

            // Consider adding transparency so that the strip lines are lighter
            stripLine1.BackColor = Color.FromArgb(120, Color.Green);
            //stripLine1.BackSecondaryColor = Color.Black;
            //stripLine1.BackGradientStyle = GradientStyle.LeftRight;

            // Add the strip line to the chart
            Chart1.ChartAreas[0].AxisY.StripLines.Add(stripLine1);
        }

        private void AddHorizGreenStripLines2()
        {
            // Instantiate new strip line
            StripLine stripLine1 = new StripLine();
            stripLine1.StripWidth = 6;
            stripLine1.BorderColor = Color.Green;
            stripLine1.BorderWidth = 1;
            stripLine1.Interval = 50;
            stripLine1.IntervalOffset = 5;

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
            stripLine1.Interval = 40;
            stripLine1.IntervalOffset = -20;

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
            stripLine1.Interval = 40;
            stripLine1.IntervalOffset = -15;

            // Consider adding transparency so that the strip lines are lighter
            stripLine1.BackColor = Color.FromArgb(120, Color.Yellow);
            //stripLine1.BackSecondaryColor = Color.Black;
            //stripLine1.BackGradientStyle = GradientStyle.LeftRight;

            // Add the strip line to the chart
            Chart1.ChartAreas[0].AxisY.StripLines.Add(stripLine1);
        }

    }
}
