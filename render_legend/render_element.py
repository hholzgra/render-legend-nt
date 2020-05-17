import os
import tempfile
import shutil
from PIL import Image, ImageChops
from colour import Color

import mapnik
mapnik.logger.set_severity(mapnik.severity_type.Error)

from osm_xml import create_osm_tree, add_osm_element

def render_element(style_file, db_name, element_type, zoom, tags, width, png_path):
    """ render a single legend element

    Arguments:
    * style_file - a mapnik xml style file
    * db_name - osm2pgsql db name for style_file
    * element_type - point, line, etc...
    * zoom - zoom factor to render for
    * tags - OSM element tags
    * width - width of image to generate, height will be auto-calculated
    * png_path - where to store the result image

    """
    tmpdir = tempfile.mkdtemp()
    osm_xml = os.path.join(tmpdir, 'data.osm')
    rendered_img = os.path.join(tmpdir, 'result.png')
    
    tree = create_osm_tree()
    osm = tree.getroot()
    bound = add_osm_element(osm, element_type, zoom, tags)
    tree.write(osm_xml, pretty_print=True)

    cmd= "osm2pgsql --create --database=%s --merc --slim --hstore-all --style=import.style --tag-transform-script=import.lua %s 2>/dev/null" % (db_name, osm_xml)
    os.system(cmd)

    lonlat_proj = mapnik.Projection('+proj=longlat +datum=WGS84')

    ratio = abs((bound[2]-bound[0])/(bound[3]-bound[1]))
    height = int(width/ratio*1) 

    map = mapnik.Map(width,height)
    mapnik.load_map(map, style_file)
    mapnik.background = Color('white')
    
    map.srs = lonlat_proj.params()

    bbox = lonlat_proj.forward(mapnik.Box2d(mapnik.Coord(bound[0],bound[1]), mapnik.Coord(bound[2],bound[3])))

    map.zoom_to_box(bbox)
    im = mapnik.Image(width,height)
    mapnik.render(map, im)

    view = im.view(0,0,width,height)
    view.save(rendered_img,'png')

    img = Image.open(rendered_img)
    
    if len(img.getcolors()) == 1:
        return False
    
    img256=img.convert('L')
    imgbg=ImageChops.constant(img256,img256.getpixel((0,0)))
    box=ImageChops.difference(img256, imgbg).getbbox()
    out=img.crop(box)
    out.save(png_path,'png')

    shutil.rmtree(tmpdir)
    
    return True
