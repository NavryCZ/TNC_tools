# included for python - load plcgtk widgetsData-Access interface and Main-function
import jh
# included for python - load plcgtk widgetsjh.gtk class incl. window-registration
import jh.gtk
import gtk                  # included for python - load plcgtk widgetspygtk functions
import sys                  # system functions
import time
import struct
import os
import shlex
from subprocess import Popen

# function to set the path and the domain for translation
from COMMON.get_text import bindTextDomain
from COMMON.get_text import txt              # function to translate a text
from COMMON.plcgtk import *  # included for python - load plcgtk widgets


ICON_GREEN = 'PLC:\python\picture\iconGreenSmall.gif'
ICON_GRAY = 'PLC:\python\picture\iconGraySmall.gif'
ICON_RED = 'PLC:\python\picture\iconRedSmall.gif'
ICON_RED_BIG = 'PLC:\python\picture\iconRed.gif'
ICON_GREEN_BIG = 'PLC:\python\picture\iconGreen.gif'
ICON_GRAY_BIG = 'PLC:\python\picture\iconGray.gif'

IMG_FRAME_1 = os.path.join(
    'PLC:\python\picture\signal_diag', '1060_gifu_oil.jpg')
IMG_FRAME_2 = 'PLC:\python\picture\signal_diag\spindle.png'
BLANK_IMAGE = os.path.join('PLC:\python\picture\signal_diag', 'blank_img.jpg')
OPTION_IMAGE = os.path.join(
    'PLC:\python\picture\signal_diag', 'option_box.png')

S_R_OFF = os.path.join('PLC:\python\picture\signal_diag\semafor', 'r_off.jpg')
S_R_ON = os.path.join('PLC:\python\picture\signal_diag\semafor', 'r_on.jpg')
S_O_OFF = os.path.join('PLC:\python\picture\signal_diag\semafor', 'o_off.jpg')
S_O_ON = os.path.join('PLC:\python\picture\signal_diag\semafor', 'o_on.jpg')
S_G_OFF = os.path.join('PLC:\python\picture\signal_diag\semafor', 'g_off.jpg')
S_G_ON = os.path.join('PLC:\python\picture\signal_diag\semafor', 'g_on.jpg')
S_B_OFF = os.path.join('PLC:\python\picture\signal_diag\semafor', 'b_off.jpg')
S_B_ON = os.path.join('PLC:\python\picture\signal_diag\semafor', 'b_on.jpg')

S_BOTTOM = os.path.join(
    'PLC:\python\picture\signal_diag\semafor', 'bottom.jpg')
S_TOP = os.path.join('PLC:\python\picture\signal_diag\semafor', 'top.jpg')
S_SEP = os.path.join(
    'PLC:\python\picture\signal_diag\semafor', 'separator.jpg')


def find_io_of(symbol):
    phase = symbol
    path = os.path.join(os.sep, 'mnt', 'plc', 'plc', 'program', 'IOconfig.def')
    file_io_cfg = open(path, 'r')

    content = file_io_cfg.readlines()
    for line in content:
        if phase in line:
            string = line.split()[1:3]
            try:
                if 'M' in string[0]:
                    return 'I/O: not active'
            except:
                pass
            if phase in string:
                string.remove(phase)
                if '&MG_marker_one' in string:
                    string.remove('&MG_marker_one')
                    # return 'I/O' + ''.join(string[:-1])
                    return 'impossible'
            return 'I/O: ' + ''.join(string[:])
    return 'I/O: Not in IOConfig, SPLC?'


class bigLabel(gtk.Label):
    def __init__(self, text):
        self.text = text

        gtk.Label.__init__(self)
        self.set_text(self.text)
        self.modify_font(pango.FontDescription("Monospace 16"))


class Dia_image(gtk.Image):
    def __init__(self, path):
        self.path = path
        gtk.Image.__init__(self)
        if 'PLC' in self.path[:4]:
            self.set_from_file(jh.ResPath(path))
        else:
            self.set_from_file(path)


class Signal_icon(gtk.Button):
    def __init__(self, sig_name='default_name', type='btn', symbol=None, location='Default location', img_active='PLC:\python\picture\iconGreen.gif', img_inactive='PLC:\python\picture\iconRed.gif', description=None, help_img=None, size=14):

        self.sig_name = sig_name
        self.type = type
        self.symbol = symbol
        self.location = location
        self.img_active = gtk.Image()
        self.img_inactive = gtk.Image()
        self.description = description
        self.help_img = help_img
        self.size = size

        # resize image
        desired_width = self.size*2-12
        desired_height = self.size*2-12

        pixbuf_active = gtk.gdk.pixbuf_new_from_file(jh.ResPath(img_active))
        pixbuf_active = pixbuf_active.scale_simple(
            desired_width, desired_height, gtk.gdk.INTERP_BILINEAR)
        image_active = gtk.image_new_from_pixbuf(pixbuf_active)

        pixbuf_inactive = gtk.gdk.pixbuf_new_from_file(
            jh.ResPath(img_inactive))
        pixbuf_inactive = pixbuf_inactive.scale_simple(
            desired_width, desired_height, gtk.gdk.INTERP_BILINEAR)
        image_inactive = gtk.image_new_from_pixbuf(pixbuf_inactive)
        #

        # self.img_active.set_from_file(jh.ResPath(img_active))
        # self.img_inactive.set_from_file(jh.ResPath(img_inactive))
        self.img_active.set_from_pixbuf(pixbuf_active)
        self.img_inactive.set_from_pixbuf(pixbuf_inactive)

        gtk.Button.__init__(self)

        self.set_relief(gtk.RELIEF_NONE)
        self.set_image(self.img_inactive)
        self.set_size_request(self.size*2, self.size*2)

        try:
            self.handle = jh.Subscribe(
                ident=GLOBAL_SYMBOL + self.symbol, notify=self.set_color, downTime=0.2, onChange=True)
        except:
            pass

    def set_color(self, value, event=None):

        if '*0.01V' in self.type:
            raw_volt_val = value.values()[0]
            val_converted = raw_volt_val/100.0
            if int(val_converted * 100) in range(1, 1200):
                self.set_image(self.img_active)
            else:
                self.set_image(self.img_inactive)

        elif 'temp*0.1' in self.type or 'temp*0.01' in self.type or 'temp*0.001' in self.type or 'PT100' in self.type:
            raw_temp_val = value.values()[0]

            if 'PT100' in self.type:
                val_converted = raw_temp_val/100.0

            elif 'temp*0.1' in self.type:
                val_converted = raw_temp_val/10.0
            elif 'temp*0.01' in self.type:
                val_converted = raw_temp_val/100.0
            elif 'temp*0.001' in self.type:
                val_converted = raw_temp_val/1000.0
            else:
                val_converted = raw_temp_val

            if int(val_converted * 100) in range(1, 12000):
                self.set_image(self.img_active)
            else:
                self.set_image(self.img_inactive)

        else:
            if int(value.values()[0]):
                self.set_image(self.img_active)
            else:
                self.set_image(self.img_inactive)


class Diag(gtk.Object):
    def __init__(self, plcSymbol='NONE', type='1060'):

        self.app = embeddedWindow(
            usage='PLClarge', title=None, focus=True, plcSymbol=plcSymbol)
        self.app.ScrolledWindow.set_policy(
            hscrollbar_policy=gtk.POLICY_NEVER, vscrollbar_policy=gtk.POLICY_NEVER)
        self.tabs = gtk.Notebook()
        self.tabs.set_tab_pos(gtk.POS_TOP)

        self.value_handle = None
        self.scheme_name = 'S404E1A_EN.PDF'
        #
        # 1st page

        #
        self.lbl_debug = gtk.Label('')

        self.bg_image = gtk.Image()
        self.bg_image.set_from_file(jh.ResPath(IMG_FRAME_1))

        self.hlp_img = gtk.Image()
        self.hlp_img.set_from_file(jh.ResPath(BLANK_IMAGE))

        self.table = table()
        self.table.set_border_width(5)

        self.lbl_sig_name = bigLabel('')
        self.lbl_type = bigLabel('')
        self.lbl_value = bigLabel('')
        self.lbl_location = bigLabel('')
        self.lbl_plc_symbol = gtk.Label('')
        self.lbl_plc_symbol.set_selectable(True)
        self.lbl_description = gtk.Label('')

        self.si = None

        self.fixed = gtk.Fixed()
        self.fixed.put(self.bg_image, 0, 0)

        self.fill_table()
        self.set_t_labels()

        self.tabs.append_page(self.fixed)

        self.tabs.set_tab_label_text(self.fixed, "PUDORYS")
        #self.tabs.set_tab_label_text(self.fixed_spindle, "VRETENO")

    def set_t_labels(self, widget=None, sig_name='<name>', type='<0_type>', location='<0_location>', plc_symbol='MG_LED_test', description='<0_description>', help_img=None):

        if help_img == None or help_img == '':
            self.hlp_img.set_from_file(jh.ResPath(BLANK_IMAGE))
        else:
            self.hlp_img.set_from_file(jh.ResPath(os.path.join(
                'PLC:\python\picture\signal_diag', help_img)))

        self.lbl_sig_name.set_text(sig_name)
        self.lbl_type.set_text(type)
        self.lbl_location.set_text(location)
        self.lbl_plc_symbol.set_text(plc_symbol)

        self.io_text = find_io_of(plc_symbol)

        self.lbl_description.set_text(description)
        self.find_scheme_btn.set_label(self.io_text)
        self.find_scheme_btn.set_size_request(270, 21)

        if self.value_handle is not None:
            try:
                jh.UnSubscribe(self.value_handle)
            except:
                pass

        if self.lbl_plc_symbol is not None:
            try:
                self.lbl_value.set_text('Cant get value...')
                self.value_handle = jh.Subscribe(ident=GLOBAL_SYMBOL + self.lbl_plc_symbol.get_text(
                ), notify=self.set_t_value, downTime=0.2, onChange=False)
            except:
                pass

    def set_t_value(self, value, event=None):
        val = value.values()[0]

        if val == 0 and ('temp*0.1' in self.lbl_type.get_text() or 'temp*0.01' in self.lbl_type.get_text() or 'temp*0.001' in self.lbl_type.get_text() or 'PT100' in self.lbl_type.get_text()):
            self.lbl_value.set_text('0' + u"\u00b0" + 'C')
            return True

        if val == 0 and ('*0.01V' in self.lbl_type.get_text()):
            self.lbl_value.set_text('0V')
            return True

        if 'PT100' in self.lbl_type.get_text():
            self.lbl_value.set_text(str(val/100.0) + u"\u00b0" + 'C')

        elif 'temp*0.1' in self.lbl_type.get_text():
            self.lbl_value.set_text(str(val/10.0) + u"\u00b0" + 'C')
        elif '*0.01V' in self.lbl_type.get_text():
            self.lbl_value.set_text(str(val/100.0) + 'V')
        elif 'temp*0.01' in self.lbl_type.get_text():
            self.lbl_value.set_text(str(val/100.0) + u"\u00b0" + 'C')
        elif 'temp*0.001' in self.lbl_type.get_text():
            self.lbl_value.set_text(str(val/1000.0) + u"\u00b0" + 'C')
        else:
            self.lbl_value.set_text(str(val))

    def fill_table(self):

        self.table.attachToCell(
            bigLabel('name:'), xpadding=5, ypadding=2, col=1, row=1)
        self.table.attachToCell(
            self.lbl_sig_name, xpadding=15, ypadding=2, col=1, row=2)
        self.table.attachToCell(bigLabel('\ntype:'),
                                xpadding=5, ypadding=2, col=1, row=3)
        self.table.attachToCell(
            self.lbl_type, xpadding=15, ypadding=2, col=1, row=4)
        self.table.attachToCell(bigLabel('\nvalue:'),
                                xpadding=5, ypadding=2, col=1, row=5)
        self.table.attachToCell(
            self.lbl_value, xpadding=15, ypadding=2, col=1, row=6)
        self.table.attachToCell(bigLabel('\nlocation:'),
                                xpadding=5, ypadding=2, col=1, row=7)
        self.table.attachToCell(
            self.lbl_location, xpadding=15, ypadding=2, col=1, row=8)

        self.watch_send_btn = gtk.Button('add to watchlist')
        self.watch_send_btn.set_size_request(150, 20)
        self.watch_send_btn.connect(
            'clicked', self.watch_add, self.lbl_plc_symbol)
        # self.fixed.put(self.watch_send_btn,860,310+8)

        self.find_scheme_txt = find_io_of(self.lbl_plc_symbol.get_text())

        self.find_scheme_btn = gtk.Button(self.find_scheme_txt)
        self.find_scheme_btn.set_size_request(270, 21)
        self.find_scheme_btn.set_can_focus(False)
        self.find_scheme_btn.set_relief(gtk.RELIEF_NONE)
        self.find_scheme_btn.connect('clicked', self.find_scheme)

        self.table.attachToCell(bigLabel('\nplc_symbol:'),
                                xpadding=5, ypadding=2, col=1, row=9)
        #self.table.attachToCell(self.watch_list_box, xpadding=5, ypadding=2, col=1, row=9)

        self.table.attachToCell(self.lbl_plc_symbol,
                                xpadding=15, ypadding=2, col=1, row=10)
        self.table.attachToCell(
            bigLabel('\ndescription:'), xpadding=5, ypadding=2, col=1, row=11)
        self.table.attachToCell(self.find_scheme_btn,
                                xpadding=7, ypadding=0, col=1, row=12)
        self.table.attachToCell(self.lbl_description,
                                xpadding=15, ypadding=2, col=1, row=13)

    def find_scheme(self, widget=None):
        string = find_io_of(self.lbl_plc_symbol.get_text()).split(' ')[1]
        file = os.path.join('/mnt', 'plc', 'python',
                            'picture', 'signal_diag', self.scheme_name)
        #command = '[\'' +'evince\''+', \''+'--find='+string+']'
        #command = "['evince', '{}', --find={}]".format(file,string)
        # self.lbl_description.set_text(command)
        Popen(['xdotool', 'key', 'ctrl+F4'])
        p = Popen(['evince', file, '--fullscreen', '--find={}'.format(string)])
        #p = os.spawnlp(os.P_NOWAIT, "envince", "mycmd", "myarg")
        #command = ['envince']
        #command = 'evince /mnt/plc/python/picture/signal_diag/S403E1_EN.pdf'
        #os.spawnlp(os.P_WAIT, *shlex.split(command))
        # self.lbl_debug.set_text('ok')

    def add(self, sig_name='default_name', type='btn', symbol=None, location='Default location', frame=1,
            frame_pos={"x": 50, "y": 50}, img_active=ICON_GREEN,
            img_inactive=ICON_RED, description=None, help_img=None, size=14):

        self.label_offset = size

        self.si = Signal_icon(sig_name, type, symbol, location,
                              img_active, img_inactive, description, help_img, size)
        self.si.connect('clicked', self.set_t_labels, self.si.sig_name, self.si.type,
                        self.si.location, self.si.symbol, self.si.description, self.si.help_img)

        self.icon_label_f = gtk.Label(sig_name)
        self.icon_label_f.set_use_markup(True)
        self.icon_label_f.set_markup(
            '<span font_family="monospace" background="yellow" foreground="black"><b>' + sig_name + '</b></span>')

        if frame == '1':
            self.fixed.put(self.icon_label_f, frame_pos['x']-self.label_offset +
                           self.label_offset*2 - 4, frame_pos['y']-self.label_offset+(self.label_offset - 9))
            self.fixed.put(
                self.si, frame_pos['x']-self.label_offset, frame_pos['y']-self.label_offset)
        elif frame == '2':
            self.fixed_pc.put(
                self.si, frame_pos['x']-self.label_offset, frame_pos['y']-self.label_offset)
            self.fixed_pc.put(self.icon_label_f, frame_pos['x']-self.label_offset +
                              self.label_offset*2 - 4, frame_pos['y']-self.label_offset+(self.label_offset - 9))

    def watch_add(self, widget=None, symbol='test', list_name='python'):
        self.list_file_extension = '.wlt'
        self.list_file_name = list_name
        self.list_path = '/mnt/plc/table'
        self.list_symbol = symbol.get_text()

        file = open(os.path.join(self.list_path,
                    self.list_file_name + self.list_file_extension), 'a+')
        file.write(self.list_symbol + ' "<Global>" d ""\n')
        file.close()

    def set_bg(self, path):
        self.bg_image.set_from_file(jh.ResPath(path))

    def show(self):
        self.fixed.put(self.lbl_debug, 20, 20)
        self.app.pack_start(self.tabs)


class Semafor_light(gtk.Image):

    def __init__(self, color='red'):
        self.color = color
        gtk.Image.__init__(self)

        if self.color == 'red':
            self.path_active = jh.ResPath(S_R_ON)
            self.path_inactive = jh.ResPath(S_R_OFF)

            self.set_from_file(jh.ResPath(self.path_inactive))
            self.handle = jh.Subscribe(
                ident=GLOBAL_SYMBOL + 'O_LED_TNC_alarm', notify=self.update_color, downTime=0.2, onChange=False)

        elif self.color == 'orange':
            self.path_active = jh.ResPath(S_O_ON)
            self.path_inactive = jh.ResPath(S_O_OFF)

            self.set_from_file(jh.ResPath(self.path_inactive))
            self.handle = jh.Subscribe(ident=GLOBAL_SYMBOL + 'O_LED_program_end',
                                       notify=self.update_color, downTime=0.2, onChange=False)

        elif self.color == 'green':
            self.path_active = jh.ResPath(S_G_ON)
            self.path_inactive = jh.ResPath(S_G_OFF)

            self.set_from_file(jh.ResPath(self.path_inactive))
            self.handle = jh.Subscribe(ident=GLOBAL_SYMBOL + 'O_LED_machine_in_cycle',
                                       notify=self.update_color, downTime=0.2, onChange=False)

        elif self.color == 'blue':
            self.path_active = jh.ResPath(S_B_ON)
            self.path_inactive = jh.ResPath(S_B_OFF)

            self.set_from_file(jh.ResPath(self.path_inactive))
            self.handle = jh.Subscribe(ident=GLOBAL_SYMBOL + 'O_LED_machine_in_cycle',
                                       notify=self.update_color, downTime=0.2, onChange=False)

        elif self.color == 'top':
            self.set_from_file(jh.ResPath(S_TOP))

        elif self.color == 'bottom':
            self.set_from_file(jh.ResPath(S_BOTTOM))

        elif self.color == 'separator':
            self.set_from_file(jh.ResPath(S_SEP))
        else:
            pass

    def update_color(self, value, event=None):
        active = value.values()[0]
        if active:
            self.set_from_file(jh.ResPath(self.path_active))
        else:
            self.set_from_file(jh.ResPath(self.path_inactive))


class Semafor(gtk.VBox):
    def __init__(self, *lights):
        gtk.VBox.__init__(self)

        self.pack_start(Semafor_light('top'))
        counter = 0

        for light in lights:
            self.pack_start(Semafor_light(light))
            if not counter == len(lights)-1:
                self.pack_start(Semafor_light('separator'))

            counter = counter + 1
        self.pack_start(Semafor_light('bottom'))


if __name__ == "__main__":
    print 'this is for import only'
