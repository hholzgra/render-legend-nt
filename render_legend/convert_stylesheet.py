from lxml import etree
from os import path

def convert_stylesheet(old_file, new_file, old_db_name, new_db_name):
    """ Convert a Mapnik XML stylesheet for legend creation use
    * removes all Mapnik layers not using the "postgis" input plugin
    * removes all "postgis" layers not referring to the "old_db_name"
    * rewrites database name in remaining layers
    """

    # parse original XML file
    tree = etree.parse(old_file)
    root = tree.getroot()

    # parse global <Datasource> enntries that Layer datasources
    # can refer to, replace "dbname" attribute right away
    datasources = {}
    for datasource in root.findall("./Datasource"):
        datasource_name = datasource.get("name")
        params = {}
        for param in datasource.findall("./Parameter"):
            pname = param.get("name")
            ptext = param.text
            if pname == 'dbname' and ptext == old_db_name:
               param.text = new_db_name 
            params[pname] = ptext
        datasources[datasource_name] = params

    # process all Layers
    for layer in root.findall("./Layer"):
        datasource = layer.find("./Datasource")

        # if Datasource refers to a global one: take Parameter
        # defaults from there
        if datasource.get("base"):
            params = datasources[datasource.get("base")]
        else:
            params = {}

        # collect actual Datasource Parameters, overwriting
        # parameters inherited form global Datasource
        for param in datasource.findall("./Parameter"):
            params[param.get("name")] = param.text

        # remove unwanted layers, change "dbname" on those we keep
        if params["type"] != "postgis":
            root.remove(layer)
        elif 'dbname' not in params:
            root.remove(layer)
        elif params["dbname"] != old_db_name:
            root.remove(layer)
        else:
            dbname = datasource.find("./Parameter[@name='dbname']")
            if dbname is not None:
                dbname.text = new_db_name

    # make file="..." attribute paths absolute
    old_dir = path.dirname(path.realpath(old_file))
    for tag in root.findall(".//*[@file]"):
        filename = tag.get("file")
        if not path.isabs(filename):
            filename = path.join(old_dir, filename)
            tag.set("file", filename)

    # write back modified XML stylesheet
    tree.write(new_file)
