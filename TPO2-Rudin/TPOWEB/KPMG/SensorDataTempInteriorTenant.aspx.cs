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
    public partial class diboss_KPMG_SensorDataTempInteriorTenant : System.Web.UI.Page
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
                DateFrom.Text = DateTime.Now.AddDays(-2).ToShortDateString();
                DateTo.Text = DateTime.Now.ToShortDateString();
                fromDate = DateTime.Now.AddDays(-1);
                toDate = DateTime.Now;
            }
            else
            {
                if (DateRange.SelectedItem.Value == "default")
                {
                    useDateRange = false;
                    fromDate = DateTime.Now.AddDays(-1);
                    toDate = DateTime.Now;
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
            // Initialize a connection string    
            string dbConnectionString = ConfigurationManager.ConnectionStrings["Rudin_345Park"].ToString();


            SqlConnection dbConnection = new SqlConnection(dbConnectionString);

            //sensorlist
            string sensorid = "";
            string querySensor = "SELECT DISTINCT TABLE_NAME, REPLACE(REPLACE(TABLE_NAME, '_SpaceTemp', ''), 'RUDINSERVER_', '') AS SHORT_NAME FROM HISTORY_CONFIG WHERE (TABLE_NAME NOT LIKE '%PJONES%') AND (TABLE_NAME NOT LIKE '%_EAST%') AND (TABLE_NAME NOT LIKE '%_NORTH%') AND (TABLE_NAME NOT LIKE '%_SOUTH%') AND (TABLE_NAME NOT LIKE '%_WEST%') AND (TABLE_NAME LIKE '%_SpaceTemp%' AND TABLE_NAME NOT LIKE '%ROOM_SPACE_TEMPERATURES%' AND TABLE_NAME LIKE '%RUDINSERVER_FL%') AND ((TABLE_NAME LIKE '%FL2_[A-Z]%') OR (TABLE_NAME LIKE '%FL4%') OR (TABLE_NAME LIKE '%FL13%') OR (TABLE_NAME LIKE '%FL35%') OR (TABLE_NAME LIKE '%FL38%') OR (TABLE_NAME LIKE '%FL40%')) ORDER BY TABLE_NAME";
            DataSet dsSensor = new DataSet();
            string dbQueryString;
            SqlCommand myCommand;
            SqlDataReader myReader;
            Series s;
            int i = 0;

            SqlDataAdapter adapter = new SqlDataAdapter();
            adapter.SelectCommand = new SqlCommand(querySensor, dbConnection);
            adapter.Fill(dsSensor, "Sensor_Data");

            if (!Page.IsPostBack)
            {
                SensorTypeList.DataSource = dsSensor;
                SensorTypeList.DataMember = "Sensor_Data";
                SensorTypeList.DataTextField = "SHORT_NAME";
                SensorTypeList.DataValueField = "TABLE_NAME";
                SensorTypeList.DataBind();
                sensorid = "RUDINSERVER_FL13_NE_SPACETEMP";

                //chart series    
                dbQueryString = "SELECT Value, TIMESTAMP FROM [" + sensorid + "] where (TIMESTAMP > '" + fromDate.ToString() + "') AND (TIMESTAMP < '" + toDate.ToString() + "') ORDER BY TIMESTAMP";
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
                s.Points.DataBindXY(myReader, "TIMESTAMP", myReader, "Value");
				s.LegendText = "FL13_NE";
                s.ToolTip = s.LegendText;
                Chart1.Series.Add(s);

                // Close the reader and the connection
                myReader.Close();
                dbConnection.Close();

                foreach (ListItem sti in SensorTypeList.Items)
                {
                    if (sti.Text == "FL13_NE")
                    {
                        sti.Selected= true;
                    }
                }

            }
            else
            {
                foreach (ListItem sti in SensorTypeList.Items)
                {
                    if (sti.Selected)
                    {
                        sensorid = sti.Value; 
                        i++;
                        dbQueryString = "SELECT Value, TIMESTAMP FROM [" + sensorid + "] where (TIMESTAMP > '" + fromDate.ToString() + "') AND (TIMESTAMP < '" + toDate.ToString() + "') ORDER BY TIMESTAMP";
                        myCommand = new SqlCommand(dbQueryString, dbConnection);
                        myCommand.Connection.Open();
                        myReader = myCommand.ExecuteReader(CommandBehavior.CloseConnection);
                        s = new Series("Series" + i);
                        s.ChartType = SeriesChartType.FastLine;
                        s.ShadowColor = System.Drawing.ColorTranslator.FromHtml("#FFCC66");
                        s.BorderColor = System.Drawing.ColorTranslator.FromHtml("#FFCC66");
                        s.Points.DataBindXY(myReader, "TIMESTAMP", myReader, "Value");
                        s.LegendText = sti.Text;
                        s.ToolTip = s.LegendText;
                        Chart1.Series.Add(s);

                        // Close the reader and the connection
                        myReader.Close();
                        dbConnection.Close();
                    }
                }
            }
        }

        private void AddHorizGreenStripLines()
        {
            // Instantiate new strip line
            StripLine stripLine1 = new StripLine();
            stripLine1.StripWidth = 3;
            stripLine1.BorderColor = Color.Green;
            stripLine1.BorderWidth = 1;
            stripLine1.Interval = 50;
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
            stripLine1.Interval = 50;
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
            stripLine1.Interval = 50;
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
