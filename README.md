# Skycast
Weather meets Giphy


## What It Is
Skycast.py is a simple Python script that turns weather data into summary videos.

## What It Does
Skycast.py takes location name or geocoordinates as parameters and fetches corresponding weather data.
This script only parses through the hourly forecast. The script also reduces "noise": weather conditions that only last an
hour are disregarded. The script outputs a 12-second .mp4 video splicing together clips of weather footages that
summarize the conditions of the next 48 hours.

## Libraries Used:
* [Forecastio Python Client](https://github.com/ZeevG/python-forecast.io) for [Forecast.io](http://forecast.io)
* [GeoPy](https://github.com/geopy/geopy)
* [MoviePy](https://github.com/Zulko/moviepy)

### Future Features / Room for Improvement
* Make this consumable via mobile app - or translate Python scripts into Swift/Obj-C
* Time-based footage selection (e.g. Clear[Day] v. Clear[Night])
* Location-based footage selection (e.g. Clear day in Dubai v. clear day in Siberia)
* Text overlays for time/temp/conditions
* Convert to GIFs
* API-ify the output
* Create videos only if no video from the same location around the same time has not been created yet.
