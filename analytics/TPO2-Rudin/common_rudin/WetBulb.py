__author__ = 'SuperCell93'

# Code to calculate wet bulb

# connection to sql server (anderson) on anderson SQL, there's a weather database
# insde there's database diagrams--> tables--> dbo.Hourly_Forecast
# fcst date--> when forecast fetched
# forecast date is the actual day being forecasted for
# there are overlaps--> each forecast pulls data for 36 hours
# write a function. Given the minimum things you need. Separately write the script
# to get started, we have code connected If access to joule or ferante, inside C\Rudin\common_rudin there's helpers.py which is already created
# code will also connect to the database.

# NOAA formula using the Arden Buck Equation to find the water vapor mixing ratios
import os
import math




# Add error handling
class WetBulb(object):
    def __init__(self):
        self.inputtemperature = []
        self.inputpressure=[]
        self.inputdew=[]
        self.wetbulb = []

    def computebulb(self, fTemperature, fdew, Pressure):
        cTemperature = self.convertFtoC(fTemperature)
        cdew = self.convertFtoC(fdew)
        pressuremb = self.converttopressurenmb(Pressure)
        E = float(self.esubx(cdew))
        Es = float(self.esubx(cTemperature))
        E2 = self.inverted_RH(Es, self.relative_hum(cTemperature, cdew), cTemperature)
        Twguess = 0  # guess that the wetbulb is the dewpoint
        increase = 10  # start by increasing by 10
        previoussign = 1
        ediff = 1

        bulb = self.calculatebulb(ediff, Twguess, cTemperature, pressuremb, E2, previoussign, increase)
        return bulb

    def convertFtoC(self, mytempf):  # define conversion function
        C_temperature = (float(5) / float(9)) * (mytempf - 32)  # Convert F to C
        return C_temperature


    def converttopressurenmb(self, inHgpressure):
        mb = 33.8639 * inHgpressure
        return mb


    def esubx(self, tempforconvert):  # accept C temp
        ex = 6.112 * math.exp(
            (17.67 * tempforconvert) / (tempforconvert + 243.5))  # flag--> code on srh.noaa uses 243.5 this seems off
        return ex


    def calculatebulb(self, Edifference, wetguess, thetemp, MBpress, E, previoussign, increase):
        while (abs(Edifference) > 0.05):
            Ewguess = float(6.112) * math.exp((float(17.67) * wetguess) / (wetguess + float(243.5)))
            Eguess = Ewguess - MBpress * (float(thetemp) - float(wetguess)) * float(0.00066) * (
            1 + (float(0.00115) * wetguess))
            Edifference = float(E) - float(Eguess)
            increase = float(increase)
            if Edifference == 0:
                break

            else:
                if Edifference < 0:
                    cursign = -1
                    if cursign != previoussign:
                        previoussign = cursign
                        increase /= 10
                    else:
                        increase = increase

                else:
                    cursign = 1
                    if cursign != previoussign:
                        previoussign = cursign
                        increase /= 10
                    else:
                        increase = increase
            if (abs(Edifference) <= 0.05 ):
                break
            else:
                wetguess += increase * previoussign

        wetbulb = wetguess
        # assert isinstance(wetbulb, WetBulb)
        return wetbulb

    def relative_hum(self, temperature, dewpoint):
        Rh = 100 * (
        math.exp((17.625 * dewpoint) / (243.04 + dewpoint)) / math.exp((17.625 * temperature) / (243.04 + temperature)))
        return Rh

    def inverted_RH(self, Es, rh, temp):
        E = Es * (float(rh) / float(100))
        return E

# Ctemp = convertFtoC(fTemperature)  # convert temp to C. F has smaller scale than C. For every degree C, there are 1.8 F.  # CDew = convertFtoC(fdew)

# if Ctemp < CDew


# Convert temperature from F to C. F scale has smaller scale. For every degree C, there are 1.8 degrees F.
# need

# A = WetBulb()
# temp = 45
# pressure = 29.7
# dewpoint = 32

# trs = WetBulb.computebulb(WetBulb(), your_ftemp, your_fdewpoint, your_inHgpressure)

# print(trs)




#
# inst_wetbulb = WetBulb()
# temp_c = .convertFtoC(56)
