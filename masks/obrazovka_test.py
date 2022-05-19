'''simplest possible screen'''
from masks import *

# window init
myWindow = embeddedWindow(usage='PLCmedium',
                          title=txt('Custom window text'),
                          focus=True,
                          plcSymbol='MG_SK_obrazovka_test_show')

# blue background
bg_color = gtk.gdk.Color('#E0E9FE')
myWindow.Viewport.modify_bg(gtk.STATE_NORMAL, bg_color)

# add widget into window
myWindow.pack_start(gtk.Label('Label Test'))
