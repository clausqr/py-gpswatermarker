#!/usr/bin/python
__author__ = 'claus'
# -*- coding: UTF-8 -*-
# (c) http://github.com/clausqr

import sys, getopt

import exifread
import os, sys
#sys.setdefaultencoding('utf-8')


import PIL
from PIL import ImageFont
from PIL import Image
from PIL import ImageDraw

def _get_if_exist(data, key):
    if key in data:
        return data[key]

def _convert_to_degress(value):
    """Helper function to convert the GPS coordinates stored in the EXIF to degress in float format"""
    d0 = value[0]['num']
    d1 = value[0]['den']
    d = float(d0) / float(d1)

    m0 = value[1]['num']
    m1 = value[1]['den']
    m = float(m0) / float(m1)

    s0 = value[2]['num']
    s1 = value[2]['den']
    s = float(s0) / float(s1)

    return d + (m / 60.0) + (s / 3600.0)

def get_lat_lon(exif_data):
    """Returns the latitude and longitude, if available, from the provided exif_data (obtained through get_exif_data above)"""
    lat = None
    lon = None

    if "Image GPSInfo" in exif_data:

        gps_latitude = _get_if_exist(exif_data, "GPS GPSLatitude")
        gps_latitude_ref = _get_if_exist(exif_data, 'GPS GPSLatitudeRef')
        gps_longitude = _get_if_exist(exif_data, 'GPS GPSLongitude')
        gps_longitude_ref = _get_if_exist(exif_data, 'GPS GPSLongitudeRef')

        lat = gps_latitude
        lon = gps_longitude
        ns =  gps_latitude_ref
        ew = gps_longitude_ref
    return lat, lon, ns, ew


# Open image file for reading (binary mode)
# path_name = "IMG_4195.jpg"
path_name = sys.argv[1]

outfile = sys.argv[2]


f = open(path_name, 'rb')



# Return Exif tags
tags = exifread.process_file(f)

lat_lon = get_lat_lon(tags)

lat_deg = lat_lon[0].values[0]
lat_min = lat_lon[0].values[1]
lat_sec = float(lat_lon[0].values[2].num)/float(lat_lon[0].values[2].den)

lon_deg = lat_lon[1].values[0]
lon_min = lat_lon[1].values[1]
lon_sec = float(lat_lon[1].values[2].num)/float(lat_lon[1].values[2].den)

ns = lat_lon[2]
ew = lat_lon[3]

degreeChar = u'\N{DEGREE SIGN}'
lat_lon_text = str( ('{0}.{1}\'{2:.3f}"'.format(lat_deg, lat_min, lat_sec) + ns.printable) \
                    + (', {0}.{1}\'{2:.3f}"'.format(lon_deg, lon_min, lon_sec) + ew.printable))

#lat_lon_text = unicode(lat_lon_text).encode('utf-8', 'ignore')


print "Imagen: " + path_name , "..."
print "   EXIF GPS=", \
    lat_lon_text, "..."

im1 = Image.open(path_name)


draw = ImageDraw.Draw(im1)
#Mac OS X
#font = ImageFont.truetype(font='/Library/Fonts/Arial.ttf', size=75)

#Debian
font = ImageFont.truetype('/usr/share/fonts/truetype/msttcorefonts/arial.ttf', size=75)

x = 5
y = 5

# thin border
draw.text((x-1, y), lat_lon_text, font=font, fill='black')
draw.text((x+1, y), lat_lon_text, font=font, fill='black')
draw.text((x, y-1), lat_lon_text, font=font, fill='black')
draw.text((x, y+1), lat_lon_text, font=font, fill='black')

# thicker border
draw.text((x-1, y-1), lat_lon_text, font=font, fill='black')
draw.text((x+1, y-1), lat_lon_text, font=font, fill='black')
draw.text((x-1, y+1), lat_lon_text, font=font, fill='black')
draw.text((x+1, y+1), lat_lon_text, font=font, fill='black')

# now draw the text over it
draw.text((x, y), lat_lon_text, font=font)

draw = ImageDraw.Draw(im1)

print "   Guardando como " + outfile,  "... "

im1.save(outfile)

print "   OK"


