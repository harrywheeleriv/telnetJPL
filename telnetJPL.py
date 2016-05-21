# telnet script to connect to JPL horizons system to grab
# ulysses ephemeris info


import sys
import telnetlib
import numpy as np

class telnetJPL():
    def __init__(self,startdate,enddate):
        self.startdate = startdate
        self.enddate = enddate
        
        HOST = "horizons.jpl.nasa.gov"

        tn = telnetlib.Telnet(HOST, "6775")

        tn.write("vt102\n".encode('ascii'))
        print tn.read_until("Horizons> ",10)


        tn.write("ulysses".encode('ascii') + "\r\n".encode('ascii'))
        #tn.write("\r")
        print tn.read_until(" Select ... [E]phemeris, [F]tp, [M]ail, [R]edisplay, ?, <cr>: ",20)


        tn.write("E".encode('ascii') + "\r\n".encode('ascii'))
        print tn.read_until(" Observe, Elements, Vectors  [o,e,v,?] : ",20)

        tn.write("v\r\n".encode('ascii'))
        print tn.read_until(" Coordinate center [ <id>,coord,geo  ] : ",10)

        tn.write("@sun\r\n".encode("ascii"))
        print tn.read_until(" Reference plane [eclip, frame, body ] : ",10)

        tn.write("eclip\r\n".encode("ascii"))
        print tn.read_until(" Starting CT  [>=   1990-Oct-06 19:05] : ",10)

        tn.write(self.startdate.encode("ascii") + "\r\n".encode("ascii"))
        print tn.read_until(" Ending   CT  [<=   2050-Jan-01 12:00] : ",10)

        tn.write(self.enddate.encode("ascii") + "\r\n".encode("ascii"))
        print tn.read_until(" Output interval [ex: 10m, 1h, 1d, ? ] : ",10)

        tn.write("10m" + "\r\n".encode("ascii"))
        print tn.read_until(" Accept default output [ cr=(y), n, ?] : ",10)

        tn.write("n" + "\r\n".encode("ascii"))
        print tn.read_until(" Output reference frame [J2000, B1950] : ",10)
        
        tn.write("J2000" + "\r\n".encode("ascii"))
        print tn.read_until(" Corrections [ 1=NONE, 2=LT, 3=LT+S ]  : ",10)

        tn.write("NONE" + "\r\n".encode("ascii"))
        print tn.read_until(" Output units [1=KM-S, 2=AU-D, 3=KM-D] : ",10)

        tn.write("1" + "\r\n".encode("ascii"))
        print tn.read_until(" Spreadsheet CSV format    [ YES, NO ] : ",10)

        tn.write("YES"+ "\r\n".encode("ascii"))        
        print tn.read_until(" Label cartesian output    [ YES, NO ] : ",10)

        tn.write("YES"+ "\r\n".encode("ascii"))
        print tn.read_until("  Select output table type  [ 1-6, ?  ] : ",10)

        tn.write("2"+ "\r\n".encode("ascii"))
        self.ephemerisRawString = tn.read_until(" >>> Select... [A]gain, [N]ew-case, [F]tp, [K]ermit, [M]ail, [R]edisplay, ? : ",20)

        self.processEphemeris()

        
    def processEphemeris(self):
        """
            Creates a list of the ephemeris data from the raw string. The ephemeris data will be presented in columnar format where
                JD, date, X, Y, Z, vx, vy, vz.

                Outputs Ephemeris Average as X, Y, Z, vx, vy, vz
        """
        self.ephemerisRawdata = self.ephemerisRawString.split("$$")[1][3:]
        self.ephemeris = list(chunks([row.replace('\r\n','').replace('A.D. ','').replace(' ','') for row in self.ephemerisRawdata.split(',')],8))
        self.ephemeris.pop(-1)
        self.ephemerisAverage = [ self.component(value) for value in range(2,8)]
        
    def component(self,component):
        return np.mean([float(row[component]) for row in self.ephemeris])
        
def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in xrange(0, len(l), n):
        yield l[i:i+n]
        
def main():

    startdate = "1990-Oct-06 19:10"
    enddate ="1990-Oct-06 20:10"
    
    horizons = telnetJPL(startdate,enddate)

    return horizons

if __name__ == '__main__':
    horizons = main()
