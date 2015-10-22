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
    public partial class diboss_001_VFD : System.Web.UI.Page
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
            string floor = "";
            
            if (!Page.IsPostBack)
            {
            // Initialize a connection string    
            string dbConnectionString = ConfigurationManager.ConnectionStrings["TPOWEB"].ToString();

            SqlConnection dbConnection = new SqlConnection(dbConnectionString);


            string queryFloor = "select distinct [FLOOR] from [345].[dbo].[345---------001BMSHVAFANFDB---VAL001] order by [Floor]";

            DataSet dsFloor = new DataSet();


            SqlDataAdapter adapter = new SqlDataAdapter();
            adapter.SelectCommand = new SqlCommand(queryFloor, dbConnection);
            adapter.Fill(dsFloor, "Floor");

            RuntimeList.DataSource = dsFloor;
            RuntimeList.DataMember = "Floor";
            RuntimeList.DataTextField = "Floor";
            RuntimeList.DataValueField = "Floor";
            RuntimeList.DataBind();

            }

            if (RuntimeList.SelectedIndex > -1)
            {
                floor = RuntimeList.SelectedItem.Value;

                PlotChart(floor);
            }

        }


        private void PlotChart(string floor)
        {

            // Initialize a connection string    
            string dbConnectionString = ConfigurationManager.ConnectionStrings["TPOWEB"].ToString();

            SqlConnection dbConnection = new SqlConnection(dbConnectionString);

            string dbQueryStringm;
            string dbQueryStringr;
            string dbQueryStringn;
            SqlCommand myCommand;
            SqlDataReader myReader;
            Series m;
            Series r;
            Series n;


            string queryEquipment = "SELECT DISTINCT EQUIPMENT_NO FROM [345].[dbo].[345---------001BMSHVAFANFDB---VAL001] WHERE [Floor] = '" + floor + "' ORDER BY EQUIPMENT_NO";
            DataSet dsEquipment = new DataSet();


            SqlDataAdapter adapter = new SqlDataAdapter();
            adapter.SelectCommand = new SqlCommand(queryEquipment, dbConnection);
            adapter.Fill(dsEquipment, "EQUIPMENT_NO");
            int count = 0;
            foreach (DataRow data in dsEquipment.Tables[0].Rows)
            {


                dbQueryStringm = "SELECT [TIMESTAMP],([VALUE]) AS Value FROM [345].[dbo].[345---------001BMSHVAFANFDB---VAL001] WHERE EQUIPMENT_NO = '" + data[0] + "' AND [Floor] = '" + floor + "' AND ([TIMESTAMP] > '" + fromDate.ToString() + "') AND ([TIMESTAMP] < '" + toDate.ToString() + "')  ORDER BY [TIMESTAMP]";

                myCommand = new SqlCommand(dbQueryStringm, dbConnection);
                myCommand.Connection.Open();
                myReader = myCommand.ExecuteReader(CommandBehavior.CloseConnection);
                m = new Series("Series_m_" + count);
                m.ChartType = SeriesChartType.FastLine;
                m.Color = System.Drawing.ColorTranslator.FromHtml("#0000FF");
                m.ShadowColor = System.Drawing.ColorTranslator.FromHtml("#FFCC66");
                m.BorderColor = System.Drawing.ColorTranslator.FromHtml("#FFCC66");
                m.Points.DataBindXY(myReader, "TIMESTAMP", myReader, "Value");
                m.LegendText = data[0].ToString() + " Actual";
                Chart2.Series.Add(m);

                dbQueryStringr = "SELECT [TIMESTAMP],([VALUE]) AS Value FROM [345].[dbo].[345---------001TPOHVAFANFDB---VAL001] WHERE ([VALUE]) >0 AND EQUIPMENT_NO = '" + data[0] + "' AND [Floor] = '" + floor + "' AND ([TIMESTAMP] > '" + fromDate.ToString() + "') AND ([TIMESTAMP] < '" + toDate.ToString() + "')  ORDER BY [TIMESTAMP]";

                myCommand = new SqlCommand(dbQueryStringr, dbConnection);
                myCommand.Connection.Open();
                myReader = myCommand.ExecuteReader(CommandBehavior.CloseConnection);
                r = new Series("Series_r_" + count);
                r.ChartType = SeriesChartType.FastLine;
                r.Color = System.Drawing.ColorTranslator.FromHtml("#FF0000");
                r.ShadowColor = System.Drawing.ColorTranslator.FromHtml("#FFCC66");
                r.BorderColor = System.Drawing.ColorTranslator.FromHtml("#FFCC66");
                r.Points.DataBindXY(myReader, "TIMESTAMP", myReader, "Value");
                r.LegendText = data[0].ToString();
                Chart2.Series.Add(r);

                dbQueryStringn = "SELECT [TIMESTAMP],([VALUE]) AS Value FROM [345].[dbo].[345---------001BMSHVAFANFDB---VAL002] WHERE EQUIPMENT_NO = '" + data[0] + "' AND [Floor] = '" + floor + "' AND ([TIMESTAMP] > '" + fromDate.ToString() + "') AND ([TIMESTAMP] < '" + toDate.ToString() + "')  ORDER BY [TIMESTAMP]";

                myCommand = new SqlCommand(dbQueryStringn, dbConnection);
                myCommand.Connection.Open();
                myReader = myCommand.ExecuteReader(CommandBehavior.CloseConnection);
                n = new Series("Series_n_" + count);
                n.ChartType = SeriesChartType.FastLine;
                n.Color = System.Drawing.ColorTranslator.FromHtml("#0000FF");
                n.ShadowColor = System.Drawing.ColorTranslator.FromHtml("#FFCC66");
                n.BorderColor = System.Drawing.ColorTranslator.FromHtml("#FFCC66");
                n.Points.DataBindXY(myReader, "TIMESTAMP", myReader, "Value");
                n.LegendText = data[0].ToString();
                Chart1.Series.Add(n);

                count++;
            }


            // Close  the connection
            dbConnection.Close();


        }


    }
}
