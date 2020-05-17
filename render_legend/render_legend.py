import os
import yaml

from convert_stylesheet import convert_stylesheet
from html_legend import html_legend

zoom = 19
width = 100

style_xml = '/home/maposmatic/styles/openstreetmap-carto/osm.xml'
new_style_xml = 'new_style.xml'

old_db_name = 'gis'
new_db_name = 'foo'

convert_stylesheet(style_xml, new_style_xml, old_db_name, new_db_name)

with open(r'legend.yml') as file:
    legend = yaml.load(file, Loader=yaml.FullLoader)

html_legend(legend, new_style_xml, new_db_name, zoom, width)
    
