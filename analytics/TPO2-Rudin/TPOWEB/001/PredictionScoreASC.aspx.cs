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
    public partial class diboss_001_PredictionScoreASC : System.Web.UI.Page
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
            int i=0;
            
            if (!Page.IsPostBack)
            {
            // Initialize a connection string    
            string dbConnectionString = ConfigurationManager.ConnectionStrings["TPOWEB"].ToString();

            SqlConnection dbConnection = new SqlConnection(dbConnectionString);


            string querySensor = "SELECT DISTINCT Floor + '_' +  Quadrant AS SHORT_NAME FROM [345].[dbo].[Thermal_ASC_spc_temp_scores] ORDER BY Floor + '_' +  Quadrant";
            DataSet dsSensor = new DataSet();


            SqlDataAdapter adapter = new SqlDataAdapter();
            adapter.SelectCommand = new SqlCommand(querySensor, dbConnection);
            adapter.Fill(dsSensor, "Sensor_Data");

            SensorTypeList.DataSource = dsSensor;
            SensorTypeList.DataMember = "Sensor_Data";
            SensorTypeList.DataTextField = "SHORT_NAME";
            SensorTypeList.DataValueField = "SHORT_NAME";
            SensorTypeList.DataBind();

            
                //SensorTypeList.Items[0].Selected = true;
                foreach (ListItem sti in SensorTypeList.Items)
                {
                    if (sti.Text == "F02_CNW")
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
            string dbQueryStringms;
            string dbQueryStringmo;
            SqlCommand myCommand;
            SqlDataReader myReader;

            Series m;


            //chart series    

            dbQueryStringme = "SELECT [Date] AS TIMESTAMP, [RMSE] AS Value FROM [345].dbo.[Thermal_ASC_electric_scores] WHERE ([Date] > '" + fromDate.ToString() + "') AND ([Date] < '" + toDate.ToString() + "') AND ((DATEPART(dw, [Date]) + @@DATEFIRST) % 7) NOT IN (0, 1) ORDER BY [Date]";

            dbQueryStringms = "SELECT [Date] AS TIMESTAMP, [RMSE] AS Value FROM [345].[dbo].[Thermal_ASC_steam_scores] WHERE ([Date] > '" + fromDate.ToString() + "') AND ([Date] < '" + toDate.ToString() + "') AND ((DATEPART(dw, [Date]) + @@DATEFIRST) % 7) NOT IN (0, 1) ORDER BY [Date]";

            dbQueryStringmo = "SELECT [Date] AS TIMESTAMP, [RMSE] AS Value FROM [345].dbo.[Thermal_ASC_occupancy_scores] WHERE ([Date] > '" + fromDate.ToString() + "') AND ([Date] < '" + toDate.ToString() + "') AND ((DATEPART(dw, [Date]) + @@DATEFIRST) % 7) NOT IN (0, 1) ORDER BY [Date]";


            myCommand = new SqlCommand(dbQueryStringme, dbConnection);
            myCommand.Connection.Open();
            myReader = myCommand.ExecuteReader(CommandBehavior.CloseConnection);
            m = new Series("Series" + 1);
            m.ChartType = SeriesChartType.FastLine;
            m.ShadowColor = System.Drawing.ColorTranslator.FromHtml("#FFCC66");
            m.BorderColor = System.Drawing.ColorTranslator.FromHtml("#FFCC66");
            m.Points.DataBindXY(myReader, "TIMESTAMP", myReader, "Value");
            m.LegendText = "RMSE (Root Mean Square Error) Excluding Weekends";
            Chart1.Series.Add(m);

            myCommand = new SqlCommand(dbQueryStringms, dbConnection);
            myCommand.Connection.Open();
            myReader = myCommand.ExecuteReader(CommandBehavior.CloseConnection);
            m = new Series("Series" + 2);
            m.ChartType = SeriesChartType.FastLine;
            m.ShadowColor = System.Drawing.ColorTranslator.FromHtml("#FFCC66");
            m.BorderColor = System.Drawing.ColorTranslator.FromHtml("#FFCC66");
            m.Points.DataBindXY(myReader, "TIMESTAMP", myReader, "Value");
            m.LegendText = "RMSE (Root Mean Square Error) Excluding Weekends";
            Chart3.Series.Add(m);

            myCommand = new SqlCommand(dbQueryStringmo, dbConnection);
            myCommand.Connection.Open();
            myReader = myCommand.ExecuteReader(CommandBehavior.CloseConnection);
            m = new Series("Series" + 3);
            m.ChartType = SeriesChartType.FastLine;
            m.ShadowColor = System.Drawing.ColorTranslator.FromHtml("#FFCC66");
            m.BorderColor = System.Drawing.ColorTranslator.FromHtml("#FFCC66");
            m.Points.DataBindXY(myReader, "TIMESTAMP", myReader, "Value");
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


            string dbQueryStringm;
            SqlCommand myCommand;
            SqlDataReader myReader;
            string fl;
            Series m;





            dbQueryStringm = "SELECT [Date] AS TIMESTAMP, [RMSE] AS Value FROM [345].dbo.[Thermal_ASC_spc_temp_scores] WHERE ([Date] > '" + fromDate.ToString() + "') AND ([Date] < '" + toDate.ToString() + "') AND ((DATEPART(dw, [Date]) + @@DATEFIRST) % 7) NOT IN (0, 1)  AND (Floor + '_' +  Quadrant = '" + sensorname + "') ORDER BY [Date]";

            myCommand = new SqlCommand(dbQueryStringm, dbConnection);
            myCommand.Connection.Open();
            myReader = myCommand.ExecuteReader(CommandBehavior.CloseConnection);
            m = new Series("Series_Temp_" + i);
            m.ChartType = SeriesChartType.FastLine;
            m.ShadowColor = System.Drawing.ColorTranslator.FromHtml("#FFCC66");
            m.BorderColor = System.Drawing.ColorTranslator.FromHtml("#FFCC66");
            m.Points.DataBindXY(myReader, "TIMESTAMP", myReader, "Value");
            m.ToolTip = sensorname;
            //m.LegendText = "RMSE (Root Mean Square Error) Excluding Weekends";
            Chart2.Series.Add(m);



            // Close the reader and the connection
            myReader.Close();
            dbConnection.Close();


        }
        

    }
}
