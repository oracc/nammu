"""
Compilation of methods to be used from all Nammu classes.
"""

from java.lang import ClassLoader
from java.awt import Font
        
def set_font(font_name):
    """
    Loads font from resources' ttf file. 
    """
    path_to_ttf = 'resources/fonts/dejavu233/ttf/{}.ttf'.format(font_name)
    loader = ClassLoader.getSystemClassLoader()
    stream = loader.getResourceAsStream(path_to_ttf)
    font = Font.createFont(Font.TRUETYPE_FONT, stream)
    font = font.deriveFont(Font.PLAIN, 14)
    return font