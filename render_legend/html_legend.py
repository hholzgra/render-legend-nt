from render_element import render_element

def html_legend(legend, style_xml, db_name, zoom=18, width=100):
    n = 1
    
    print("<html>")
    print("  <head><title>%s</title></head>" % legend['title'])
    print("  <body>")
    print("    <h1>%s</h1>" % legend['title'])

    for section in legend['sections']:
        print("    <h2>%s</h2>" % section['title'])
        print("    <table>")

        for line in section['lines']:
            print("      <tr valign='middle'>")
            print("        <td halign='middle'>")

            for element in line['elements']:
                img = 'pics/imt-%d.png' % n
                n = n + 1
                if render_element(style_xml, db_name, element['type'], zoom, element['tags'], width, img):
                    print("          <img src='%s' title='%s'/>" % (img, element['caption']))

            print("        </td>")
            print("        <td halign='left'>")
            print("          %s" % line['title'])
            print("        </td>")
            print("      </tr>")

        print("    </table>")

    print("  </body>")
    print("</html>")
