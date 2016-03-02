#!/usr/bin/env python

from __future__ import division
import os, sys, stat
import cgi
import cgitb; cgitb.enable()
import datetime, time
import forecastio
from itertools import groupby
from moviepy.editor import VideoFileClip, CompositeVideoClip, concatenate_videoclips
from geopy.geocoders import Nominatim
import oauth2 as oauth2




# Families of weather conditions
weather = {
  "Clear":                      "clear",
  "Sunny":                      "clear",
  "Clear Skies":                "clear",
  "Partly Cloudy":              "partly_cloudy",
  "Mostly Cloudy":              "partly_cloudy",
  "Cloudy":                     "cloudy",
  "Overcast":                   "cloudy",
  "Foggy":                      "cloudy",
  "Windy":                      "windy",
  "Breezy":                     "windy",
  "Breezy and Partly Cloudy":   "windy",
  "Drizzle":                    "rainy",
  "Light Rain":                 "rainy",
  "Light Rain and Breezy":      "rainy",
  "Rain":                       "rainy",
  "Light Snow":                 "snowy",
  "Snow":                       "snowy",
  "Heavy Snow":                 "snowy",
  "Blizzard":                   "snowy",
  "Flurries":                   "snowy",
  "Snow and Breezy":            "snowy",
  "Heavy Snow and Breezy":      "snowy",
  "Thunderstorm":               "stormy",
  "Storm":                      "stormy",
  "Hail":                       "hail"
  }

weather_footage = {
  "clear":          "clear.mov",
  "partly_cloudy":  "partly_cloudy.mp4",
  "cloudy":         "partly_cloudy.mp4",
  "rainy":          "rainy.mp4",
  "snowy":          "snowy.mp4",
  "stormy":         "rainy.mp4",
  "hail":           "rainy.mp4",
  "windy":          "rainy.mp4"
}



# Forecastio API init
api_key = "0a821ac78b5c0f2e8e78535f0e21d9b5"
timestamp = str(int(time.time()))





def main():
  """
  Run load_forecast() with the given lat, lon, and time args
  """




  # Fetch HTTP GET arguments
  arguments = cgi.FieldStorage()
  lat = arguments.getvalue('lat')
  lon = arguments.getvalue('lon')
  loc = arguments.getvalue('q')


  # Fetch Location info
  geolocator = Nominatim()
  

  # Fetch coordinates from city name
  if loc:
    location = geolocator.geocode(loc)
    lat = location.latitude
    lon = location.longitude


  # Fetch Geocoded Location Name from coordinates
  location = geolocator.reverse(str(lat) + ", " + str(lon), language='en')
  
    # "City, State, Country" for HTML
  location_city = ""
  if 'city' in location.raw['address'].keys():
    location_city = location.raw['address']['city']
  elif 'town' in location.raw['address'].keys():
    location_city = location.raw['address']['town']

  location_state = location.raw['address']['state']
  location_country = location.raw['address']['country']

  location_name = location_city + ", " + location_state + ", " + location_country
  location_name = location_name.encode('utf8')

  # "City_State_Country_DateTime" for video filename
  
  video_filename = location_city + "_" + location_state + "_" + location_country + "_" + timestamp
                   


  #lat = 42.36565 #51.5072 
  #lon = -71.108322 #-0.1275
  #time = datetime.datetime(2016, 3, 1, 21, 0, 0)

  # Forecastio API call
  forecast = forecastio.load_forecast(api_key, lat, lon)
  by_hour = forecast.hourly()


  # Array "Clip"
  # Array needed to preserve sequence
  clip_array = []
  final_array = []

  # Pre-processing: Remap the data to conform to major families of weather conditions
  for hourly_data_point in by_hour.data:
    # Append mapped values to array
    default = 'Clear'
    weather_condition = weather.get(hourly_data_point.summary, default)
    clip_array.append(weather_condition)

  print(clip_array)

  
  # Reduce freq / repeats into dict
  clip_array = [(k, len(list(g))) for k, g in groupby(clip_array)]



  # Reduce noise:

  # if current value is 1 hr, then check the previous & next conditions.
  # merge with whichever has a longer pattern.
  # In the example, you'd merge with PC1, not PC2.

  # ex: Partly Cloudy - 5 hrs
  #     Clear         - 1 hr
  #     Partly Cloudy - 2 hr

  
  for index, obj in enumerate(clip_array):

    # Current key-value
    (k0, v0) = obj

    # If this is noise (conditions lasting 1 hr):
    if v0 == 1:

      # If this obj is first in the array
      if index == 0:

        # Append to next item in array
        (k1, v1) = clip_array[index + 1]
        clip_array[index + 1] = (k1, v1 + v0)

        # Remove item from array
        clip_array.remove(obj)

      # If this obj is last in the array
      elif index == len(clip_array) - 1:

        # Append to prev item in array
        (k2, v2) = clip_array[index - 1]
        clip_array[index - 1] = (k2, v2 + v0)

        # Remove item from array
        clip_array.remove(obj)

      # Mid-array cases
      elif index > 0 and index < len(clip_array) - 1:

        # Get prev/next key-values
        (pk, pv) = clip_array[index - 1]
        (nk, nv) = clip_array[index + 1]

        # If prev value is greater/equal, then add to prev
        if pv >= nv:
          clip_array[index - 1] = (pk, pv + v0)
        elif pv < nv:
          clip_array[index + 1] = (nk, nv + v0)

        # Delete this item
        clip_array.remove(obj)


            
  '''
  # Reduce any array elem that's been left out
  for idx, obj in enumerate(clip_array):
    # Next key/values in array
      if idx + 1 < len(clip_array):
        
        next_clip = clip_array[idx + 1]

        if next_clip:
          (k1, v1) = next_clip

          if v1 == 1:

            count = 1

            clip_array[idx] = (k0, v0 + count)
            clip_array.remove(next_clip)
  '''

  # Create list of video footages
  footages = []

  for k, v in clip_array:
    share_of_video = v / 49.000 * 12.000
    footage = VideoFileClip("cgi-bin/" + weather_footage[k]).subclip(0, share_of_video)
    footages.append(footage)


  file_address = "cgi-bin/forecast_clips/" + video_filename + ".mp4"
  #final_clip.write_gif("Forecast.gif", fps=15)
  

  final_clip = concatenate_videoclips(footages, method="compose")
  #final_clip = CompositeVideoClip(footages)
  final_clip.fps = 15
  final_clip.write_videofile(file_address)
  

  # convert text into Unicode
  hourly_summary = by_hour.summary


  # Create web content
  print 'Content-Type: text/html'
  print
  print '<html>'
  print '<head>'
  print '<title>Welcome to Skycast</title>'
  print '<link href="http://vjs.zencdn.net/5.7.1/video-js.css" rel="stylesheet">'
  print '<script src="http://vjs.zencdn.net/ie8/1.1.2/videojs-ie8.min.js"></script>'
  print '</head>'
  print '<body>'
  print '<h2>Welcome to Skycast</h2>'
  print '<h3>Here are the hourly forecasts for %s:</h3>' % location_name

  print "<h4>====================Current Data====================</h4>"
  current_weather = forecast.currently()
  print "<h5>Current Weather: %s</h5>" % (current_weather.summary)
  print "<h5>Current Temperature: %s</h5>" % (current_weather.temperature)

  print "<h4>====================Hourly Data====================</h4>"

  print "<video controls preload width='640' height=''>"
  print "<source src='%s' type='video/mp4;codecs=\"avc1.42E01E, mp4a.40.2\"'>" % "rainy.mp4" #(video_filename + ".mp4")
  print "</video>"
  
  print "<h5>Hourly Summary: %s</h5>" % hourly_summary.encode('utf8')

  print '<ul>'
  for c, l in clip_array:
    print '<li>%s for %s hours</li>' % (c, l)
  #print '<li>%s</li>' % clip_array
  print '</ul>'

  print '<ul>'
  for hourly_data_point in by_hour.data:
    print '<li>Weather: %s</li>' % (hourly_data_point.summary)
  print '</ul>'


  '''
  print "<h4>====================Daily Data====================</h4>"
  by_day = forecast.daily()
  print "<h5>Daily Summary: %s</h5>" % (by_day.summary)

  for daily_data_point in by_day.data:
    print '<li>Weather: %s</li>' % (daily_data_point.summary)
  '''


if __name__ == "__main__":
  main()


