#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2017 sboynton <sboynton@C02SG09NG8WQ-sboynton>
#
# Distributed under terms of the MIT license.

"""
Returns a JSON dict of SB harbor wind conditions from weatherforyou.com.
https://www.weatherforyou.com/reports/index.php?config=&forecast=pass&pass=hourly&pands=santa+barbara+harbor%2Ccalifornia&zipcode=&place=santa%20barbara%20harbor&state=ca&country=US&icao=KSBA
"""

from flask import Flask, jsonify
from bs4 import BeautifulSoup
from flask_cache import Cache
import json
import requests

app = Flask(__name__)
cache = Cache(app, config={'CACHE_TYPE': 'simple'})

@app.route('/')
@cache.cached(timeout=1800) # Caching for 30 minutes
def index():
    r = requests.get("https://www.weatherforyou.com/reports/index.php?config=&forecast=pass&pass=hourly&pands=santa+barbara+harbor%2Ccalifornia&zipcode=&place=santa%20barbara%20harbor&state=ca&country=US&icao=KSBA")
    data = r.text
    soup = BeautifulSoup(data, "html.parser")

    daily_forecast = {}
    i = 0

    location, state, country = soup.find("span", {"class": "headerText"}).get_text().split(",")
    daily_forecast["location"] = location
    daily_forecast["state"] = state
    daily_forecast["country"] = country

    for col in soup.find_all("div", class_="hourly_cal_colwrap"):
        hourly_forecast = {}

        hour = col.span
        day = hour.find_next_sibling("span")
        temp = day.find_next_sibling("span")
        temp_wind = temp.find_next_sibling("span")
        precip = temp.find_next_sibling("a")
        dew = precip.find_next_sibling("a")
        humidity = dew.find_next_sibling("a")
        wind_dir = humidity.find_next_sibling("a")
        wind_spd = wind_dir.find("a")

        hourly_forecast["time"] = hour.get_text()
        hourly_forecast["day"] = day.get_text()
        hourly_forecast["temp"] = temp.get_text()
        hourly_forecast["feels_like"] = temp_wind.get_text()
        hourly_forecast["precip"] = precip.find("span").get_text()
        hourly_forecast["dew_pt"] = dew.find("span").get_text()
        hourly_forecast["humidity"] = humidity.find("span").get_text()
        hourly_forecast["wind_dir"] = wind_dir.find("span").get_text()
        hourly_forecast["wind_spd"] = wind_spd.find("span").get_text()[:-4]

        daily_forecast[i] = hourly_forecast
        i += 1

    return jsonify(daily_forecast)
