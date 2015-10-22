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
    public partial class diboss_001_ASC_Output_Electric_Cum : System.Web.UI.Page
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
            string sensorid = "";
            int i = 0;
            
            if (!Page.IsPostBack)
            {
            // Initialize a connection string    
            string dbConnectionString = ConfigurationManager.ConnectionStrings["TPOWEB"].ToString();

            SqlConnection dbConnection = new SqlConnection(dbConnectionString);


            string queryRuntime = "SELECT DISTINCT [RUNTIME] FROM [345].[dbo].[asc_output_electric] ORDER BY [RUNTIME] DESC";

            DataSet dsRuntime = new DataSet();


            SqlDataAdapter adapter = new SqlDataAdapter();
            adapter.SelectCommand = new SqlCommand(queryRuntime, dbConnection);
            adapter.Fill(dsRuntime, "RUNTIME");

            RuntimeList.DataSource = dsRuntime;
            RuntimeList.DataMember = "RUNTIME";
            RuntimeList.DataTextField = "RUNTIME";
            RuntimeList.DataValueField = "RUNTIME";
            RuntimeList.DataBind();

            string querySensor = "SELECT DISTINCT EQUIPMENT_NO AS SHORT_NAME FROM [345].[dbo].[asc_output_electric] ORDER BY EQUIPMENT_NO";
            DataSet dsSensor = new DataSet();


            adapter = new SqlDataAdapter();
            adapter.SelectCommand = new SqlCommand(querySensor, dbConnection);
            adapter.Fill(dsSensor, "Sensor_Data");

            SensorTypeList.DataSource = dsSensor;
            SensorTypeList.DataMember = "Sensor_Data";
            SensorTypeList.DataTextField = "SHORT_NAME";
            SensorTypeList.DataValueField = "SHORT_NAME";
            SensorTypeList.DataBind();
            foreach (ListItem sti in SensorTypeList.Items)
            {
                if (sti.Text == "001")
                {
                    sti.Selected = true;
                }
            }

            }

            if (RuntimeList.SelectedIndex > -1)
            {
                runtime = RuntimeList.SelectedItem.Value;

                foreach (ListItem sti in SensorTypeList.Items)
                {
                    if (sti.Selected)
                    {
                        sensorid = sti.Value;

                        i++;

                        PlotChart(runtime, sensorid, i);

                    }
                }
            }

        }


        private void PlotChart(string runtime, string sensorid, int i)
        {

            // Initialize a connection string    
            string dbConnectionString = ConfigurationManager.ConnectionStrings["TPOWEB"].ToString();

            SqlConnection dbConnection = new SqlConnection(dbConnectionString);

            string dbQueryStringm;
            string dbQueryStringr;
            SqlCommand myCommand;
            SqlDataReader myReader;
            Series m;
            Series r;




            dbQueryStringm = "SELECT [TIMESTAMP],[VALUE] AS Value FROM [TPOWEB].[dbo].[001_ALEVELMETERALLKW_ASC] WHERE [RUNTIME] = '" + runtime + "'  ORDER BY [TIMESTAMP]";

            dbQueryStringr = "SELECT [TIMESTAMP],[VALUE] AS Value FROM  [TPOWEB].[dbo].[001_ALEVELMETERALLKW] WHERE [TIMESTAMP] >= DATEADD(hour,-12,(SELECT MIN([TIMESTAMP]) FROM [345].[dbo].[asc_output_electric] WHERE [RUNTIME] = '" + runtime + "')) AND [TIMESTAMP] <= (SELECT MAX([TIMESTAMP]) FROM [345].[dbo].[asc_output_electric] WHERE [RUNTIME] = '" + runtime + "')  ORDER BY [TIMESTAMP]";

                myCommand = new SqlCommand(dbQueryStringm, dbConnection);
                myCommand.Connection.Open();
                myReader = myCommand.ExecuteReader(CommandBehavior.CloseConnection);
                m = new Series("Series" + i);
                m.ChartType = SeriesChartType.FastLine;
                m.ShadowColor = System.Drawing.ColorTranslator.FromHtml("#FFCC66");
                m.BorderColor = System.Drawing.ColorTranslator.FromHtml("#FFCC66");
                m.Color = System.Drawing.ColorTranslator.FromHtml("#FF0000");
                m.Points.DataBindXY(myReader, "TIMESTAMP", myReader, "Value");
                m.LegendText = "All Meters";
                Chart2.Series.Add(m);


                myCommand = new SqlCommand(dbQueryStringr, dbConnection);
                myCommand.Connection.Open();
                myReader = myCommand.ExecuteReader(CommandBehavior.CloseConnection);
                r = new Series("Series2" + i);
                r.ChartType = SeriesChartType.FastLine;
                r.ShadowColor = System.Drawing.ColorTranslator.FromHtml("#FFCC66");
                r.BorderColor = System.Drawing.ColorTranslator.FromHtml("#FFCC66");
                r.Color = System.Drawing.ColorTranslator.FromHtml("#0000FF");
                r.Points.DataBindXY(myReader, "TIMESTAMP", myReader, "Value");
                r.LegendText = "All Meters Actual";
                Chart2.Series.Add(r);


            // Close  the connection
            dbConnection.Close();


        }


    }
}
