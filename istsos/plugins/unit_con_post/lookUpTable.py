# -*- coding: utf-8 -*-
# istSOS. See https://istsos.org/
# License: https://github.com/istSOS/istsos3/master/LICENSE.md
# Version: v3.0.0

lookups = {
    "°C":["°C", "C", "celcius", "degree Celsius", "degree-celsius", "degree-celsius", "degree", "degree centigrade", "degcelsius", "degC"],
    "°F":["°F", "F", "fahrenheit", "degfahrenheit", "degF", "degfahrenheit", "degree-fahrenheit", "degree fahrenheit"],
    "°K":["°K", "K", "kelvin", "degK", "tempK"],
    "°R":["°R", "R", "Rankine", "°Ra"],

    "mm":["mm", "millimeter", "milli-meter"],
    "cm":["cm", "centi-meter", "centi", "centimeter"],
    "m":["m", "meter"],
    "in":["in", "inch"],
    "ft":["ft", "feet", "foot"],
    "fathom":["fathom"],
    "mi":["mi", "miles", "mile"],

    "ns":["ns"],
    "ms":["ms","millisecond"],
    "s":["s"],
    "min":["min"],
    "h":["h","hour"],
    "d":["day"],
    "week":["week"],
    "month":["month"],
    "year":["year"],

    "Hz":["Hz"],
    "mHz":["mHz"],
    "kHz":["kHz"],
    "MHz":["MHz"],
    "GHz":["GHz"],
    "THz":["THz"],
    "rpm":["rpm"],
    "deg/s":["deg/s"],
    "radian/s":["radian/s", "rad/s"],

    "mm/s":["mm/s", "millimeter/s", "milli-meter/s"],
    "cm/s":["cm/s", "centi-meter/s", "centi/s", "centimeter/s"],
    "m/s":["m/s", "meter/s"],
    "m/h":["m/h", "meter/h"],
    "in/s":["in/s", "inch/s"],
    "ft/s":["ft/s", "feet/s", "foot/s"],
    "mi/h":["mi/h", "miles/h", "mile/h"],
    "knot":["knot"],

    "mm^2":["mm^2", "mm2", "millimeter-2", "millimeter2", "mm square" ],
    "cm^2":["cm^2", "cm2", "centimeter-2", "centimeter2", "cm square"],
    "m^2":["m^2", "m2","meter2", "meter square"],
    "ha":["ha", "hactare"],
    "km^2":["km^2", "km2", "kilometer2", "kilometer square"],
    "in^2":["in^2", "in2", "inch2", "inch^2", "inch-square", "inch square"],
    "ft^2":["ft^2" , "ft2", "feet2", "feetsquare"],
    "acre":["ac", "acre"],
    "mi^2":["mi^2", "miles square", "miles2", "miles^2"],

    "mm^3":["mm^3", "mm3", "millimeter-3", "millimeter3", "mm cube" ],
    "cm^3":["cm^3", "cm3", "centimeter-3", "centimeter3", "cm cube"],
    "m^3":["m^3", "m3","meter3", "meter cube"],
    "km^3":["km^3", "km3", "kilometer3", "kilometer cube"],
    "in^3":["in^3", "in3", "inch3", "inch^3", "inch-cube", "inch cube"],
    "ft^3":["ft^3" , "ft3", "feet3", "feetcube"],
    "mi^3":["mi^3", "miles cube", "miles3", "miles^3"],
    "ml":["ml", "milliliter"],
    "l":["l", "liter"],
    "kl":["kl", "kiloliter"],
    "tsp":["tsp", "teaspoon"],
    "in^3":["in^3"],
    "cup":["cup"],
    "qt":["qt"],
    "gal":["gal","gallon"],
    "yd^3":["yd^3","yd3"],

    "mcg":["mcg"],
    "mg":["mg"],
    "g":["g"],
    "kg":["kg"],
    "oz":["oz"],
    "lb":["lb"],
    "mt":["mt"],
    "t":["t"],

    "mm^3/s":["mm^3/s", "mm3/s", "millimeter-3/s", "millimeter3/s", "mm cube/s" ],
    "cm^3/s":["cm^3/s", "cm3/s", "centimeter-3/s", "centimeter3/s", "cm cube/s"],
    "m^3/s":["m^3/s", "m3/s","meter3/s", "meter cube/s"],
    "ml/s":["ml/s", "milliliter/s"],
    "kl/s":["kl/s", "kl/s", "kiloliter/s", "kiloliter/s"],
    "kl/min":["kl/min", "kiloliter/min", "kiloliter/min"],
    "kl/h":["kl/h", "kl/h", "kiloliter/h", "kiloliter/h"],
    "km^3/h":["km^3/h", "km3/h", "kilometer3/h", "kilometer cube/h"],
    "cl/s":["cl/s", "cl/s", "cl/s", "cl/s"],
    "dl/s":["dl/s"],
    "l/s":["l/s", "liter/s"],
    "l/min":["l/min", "liter/min"],
    "l/h":["l/h", "liter/h"],
    "ft^3/s":["ft^3/s" , "ft3/s", "feet3/s", "feetcube/s"],
    "mi^3/s":["mi^3/s", "miles cube/s", "miles3/s", "miles^3/s"],
    "tsp/s":["tsp/s", "teaspoon/s"],
    "in^3/s":["in^3/s"],
    "cup/s":["cup/s"],
    "qt/s":["qt/s"],
    "gal/s":["gal/s","gallon/s"],
    "gal/min":["gal/min","gallon/min"],
    "yd^3/s":["yd^3/s","yd3/s"],

    "s/m":["s/m"],
    "min/m":["min/m"],
    "s/ft":["s/ft"],
    "min/km":["min/km"],

    "Pa":["Pa"],
    "hPa":["hPa"],
    "kPa":["kPa"],
    "MPa":["MPa"],
    "bar":["bar"],
    "torr":["torr"],
    "psi":["psi"],
    "ksi":["ksi"],

    "byte":["byte"],
    "B":["B"],
    "kB":["kB"],
    "KB":["KB"],
    "MB":["MB"],
    "GB":["GB"],
    "TB":["TB"],

    "lx":["lx"],

    "ppm":["ppm"],
    "ppb":["ppb"],
    "ppt":["ppt"],

    "V":["V"],
    "mV":["mV"],
    "kV":["kV"],

    "A":["A"],
    "mA":["mA"],
    "kA":["kA"],

    "W":["W"],
    "mW":["mW"],
    "kW":["kW"],
    "MW":["MW"],
    "GW":["GW"],

    "Wh":["Wh"],
    "mWh":["mWh"],
    "MWh":["MWh"],
    "GWh":["GWh"],
    "J":["J"],
    "kJ":["kJ"],

    "deg":["deg"],
    "radian":["radian", "rad"],
    "arcmin":["arcmin"],
    "arcsec":["arcsec"],

    "C":["C"],
    "mC":["mC"],
    "μC":["μC"],
    "nC":["nC"],
    "pC":["pC"],

    "N":["N"],
    "kN":["kN"],
    "lbf":["lbf"],

    "gravity":["gravity", "gravity"],
    "m/s^2":["m/s^2"]

     }


import asyncio

class LookUpTable(object):
	@asyncio.coroutine
	def findLookUp(self, unit):
		for key, value in lookups.items():
			if str(unit).lower() in (n.lower() for n in value):
				return key
		return(unit)

