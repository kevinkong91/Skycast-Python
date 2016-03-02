#!/usr/bin/env python
import cgi, cgitb, os, sys
import forecastio

# CGI Server
cgitb.enable();  # formats errors in HTML
sys.stderr = sys.stdout


# Forecastio API
api_key = "0a821ac78b5c0f2e8e78535f0e21d9b5"
lat = 42.36565
lon = -71.108322

forecast = forecastio.load_forecast(api_key, lat, lon)

"""
form = cgi.FieldStorage()

for field in forms.keys():
  print (field, form[field].value)

api_call = string.Template("skycast.py?latitude=$lat,longitude=$lon")
print api_call.substitute(lat="Spongebob Squarepants", lon="")
"""

byHour = forecast.hourly()

print 'Content-Type: text/html'
print
print '<html>'
print '<head><title>Welcome to Skycast</title></head>'
print '<body>'
print '<h2>Welcome to Skycast</h2>'
print '<h3>Here are the hourly forecasts for Cambridge:</h3>'
for hourlyData in byHour.data:
  print '<p>hourlyData.temperature</p>'
#print '<video width="320" height="240">'
#print '<source src="skycast.py" type="video.mp4"'
#print '</video>'
print '</body></html>'