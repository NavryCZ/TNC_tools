
'''
INFO:
    Diagnostic mask for setting up Simotion from HH
    Mask should be under password

Mask I/O usage:
    OB977   -   OB_PLC_S_number_axis
    OW978   -   OW_S_PL_writepar_value_high_word
    IB981   -   IB_S_PLC_o_rdpar_status
    IW982   -   IW_S_PL_diag_message_high_word
    OW982   -   OW_PLC_S_par_number
    OW984   -   OW_PLC_S_par_index



UPDATES:
--------------------------------------------------------
Simotion_write v2.0
    Added comments for future users

    Fixed writing into simotion

Simotion_write v1.9
    Added doubleWord PLC compatibility for writing
    Added signed integer compatibility

    Fixed offset readings
    Fixed crashing when empty string is entered


'''

# IMPORT MODULS
# -----------------------------------------------------------
# included for python - load plcgtk widgetsData-Access interface and Main-function
import jh
# included for python - load plcgtk widgetsjh.gtk class incl. window-registration
import jh.gtk
import gtk                  # included for python - load plcgtk widgetspygtk functions
import sys                  # system functions
import time
import struct

from COMMON.get_text import bindTextDomain
from COMMON.get_text import txt              # function to translate a text
from COMMON.plcgtk import *  # included for python - load plcgtk widgets
from COMMON.plcSymbolDefinitions import *  # included for python

ICON_GREEN = 'PLC:\Python\PICTURE\ICON_GREEN_SMALL.GIF'
ICON_GRAY = 'PLC:\Python\PICTURE\ICON_GRAY_SMALL.GIF'
ICON_RED = 'PLC:\Python\PICTURE\ICON_RED_SMALL.GIF'


# WIDGETS
# -----------------------------------------------------------
myWindow = embeddedWindow(usage='PLCmedium', title=txt(
    'SIMOTION READ WRITE PARAMS'), focus=True, plcSymbol='MG_SK_camera_display')


# init


class bigLabel(gtk.Label):
    def __init__(self, text):
        self.text = text

        gtk.Label.__init__(self)
        self.set_text(self.text)
        self.modify_font(pango.FontDescription("Monospace 16"))


def get_double_word():
    '''
    Function to get decimal number from 2 doublewords
        scheme:
            -> get each word as decimal number from PLC
            -> if first word has negative mark before, it means the whole doubleword will be negative, so
                convert each word to positive binary string and invert them via mask to negative bytes
            -> only second word decimal can be ngative only, when value is out of signed 2-byte range, so
                set offset and convert for second, bcs first is positive, that means the whole doublword will be
                positive
            -> take both binary strings and join them together
            -> take joined 4-byte binary string and convert to decimal value
            -> set the decimal value as input value and then do other stuff like HEX conversion
    '''

    first = int(str(jh.Get(ident=GLOBAL_SYMBOL +
                'IW_S_PL_diag_message_high_word').values()[0]))
    second = int(
        str(jh.Get(ident=GLOBAL_SYMBOL + 'IW_S_PL_diag_message_low_word').values()[0]))

    if first < 0:
        firstbin = "{0:016b}".format(first & 0xffff)
        secondbin = "{0:016b}".format(second & 0xffff)
    else:
        if second < 0:
            second = 65536 + second
            secondbin = "{0:016b}".format(second & 0xffff)

        firstbin = "{0:016b}".format(first)
        secondbin = "{0:016b}".format(second)

    joined = str(firstbin) + str(secondbin)

    sig_converted = str(struct.unpack('l', struct.pack('P', int(joined, 2)))[
                        0])  # convert 32-bit to signed doubleword
    bin_in.set_text(firstbin)  # for debug
    value_to_format.set_text(sig_converted)
    formatChanged()


def actualValue(plcValue, event=None):
    get_double_word()


def formatChanged(widget=None):
    '''
    This function is for preview value in requested format
    '''

    # 0-HEX 1-DECIMAL 2-FLOAT
    raw = int(value_to_format.get_text())

    selectedIndex = fcb.get_active()

    # hex there
    if selectedIndex == 0:
        out = '{0:08x}'.format(raw)
        pv.set_text(str(out).upper())

    # dec here
    elif selectedIndex == 1:
        out = raw
        pv.set_text(str(out))

    # float here
    elif selectedIndex == 2:
        out = raw/1000.0
        pv.set_text(str(out))

    else:
        out = raw
        pv.set_text(str(out))

    updateOutput(None)

# startwrite is called when button clicked and after 0.2 sec is deactivated


def startWrite(widget):
    IB177.set_text(str(int(axe_output.get_text()) + 16))
    jh.Put({'OB_PLC_S_number_axis': int(IB177.get_text())}, GLOBAL_SYMBOL)

    time.sleep(0.2)
    autoRelease()


def autoRelease():
    IB177.set_text(axe_output.get_text())
    jh.Put({'OB_PLC_S_number_axis': int(IB177.get_text())}, GLOBAL_SYMBOL)
    time.sleep(0.1)
    btn_write.set_state(gtk.STATE_NORMAL)


def stopWrite(widget):
    pass

# func to convert writed value to decimal for simotion as expected


def updateOutput(widget):
    if pe.get_text():
        IW182.set_text(pe.get_text())
    if pi.get_text():
        IW184.set_text(pi.get_text())

    if fcb.get_active() == 0:
        if pvn.get_text():
            ID178.set_text(str(int(pvn.get_text(), 16)))

    elif fcb.get_active() == 1:
        try:
            ID178.set_text(str(int(str(pvn.get_text()), base=10)))
        except ValueError:
            ID178.set_text('0')

    elif fcb.get_active() == 2:
        try:
            ID178.set_text(str(int(round(float(pvn.get_text()) * 1000.0, 0))))
        except ValueError:
            ID178.set_text('0')
    else:
        if pvn.get_text():
            ID178.set_text(pvn.get_text())

    if ID178.get_text() and not -2147483648 <= int(ID178.get_text()) <= 2147483647:
        pvn.set_text('0')

    # splitting procedure
    if int(ID178.get_text()) < 0:
        bin_value_to_send = "{0:032b}".format(
            int(ID178.get_text()) & 0xffffffff)
    else:
        bin_value_to_send = "{0:032b}".format(int(ID178.get_text()))

    b_start_d = bin_value_to_send[:16]
    b_end_d = bin_value_to_send[16:]

    dec_start_d = int(b_start_d, 2)
    dec_end_d = int(b_end_d, 2)

    if dec_end_d > 32767:
        dec_end_d = dec_end_d - 65536

    bin_val_send.set_text(str(bin_value_to_send))

    # GUI

    jh.Put({'OW_PLC_S_par_number': int(IW182.get_text()),
            'OW_PLC_S_par_index': int(IW184.get_text()),
            'OB_PLC_S_number_axis': int(IB177.get_text()),
            'OW_S_PL_writepar_value_high_word': int(dec_start_d),
            'OW_S_PL_writepar_value_low_word': int(dec_end_d)
            }, GLOBAL_SYMBOL)


def axeValUpdate(widget):
    selectedIndex = widget.get_active()
    if selectedIndex == 2:
        axe_output.set_text('7')
    else:
        axe_output.set_text(str(selectedIndex))

    IB177.set_text(axe_output.get_text())
    updateOutput(None)


def setDefaultValues(plcVal, event=None):
    if plcVal.values()[0] == True:
        pe.set_text('0')
        pi.set_text('0')
        pv.set_text('0')
        pvn.set_text('0')
        pch.set_text('None')
        cb.set_active(0)  # set first option as default
        fcb.set_active(1)  # set decimal as default
        updateOutput(None)


def paramOk(plcVal, event=None):
    if str(plcVal.values()[0]) == '1':
        pch.set_text('PLATI')
    else:
        pch.set_text('CHYBA')


# first 3 bits are axis number and 4th bit is write signal
IB177 = gtk.Label('')
ID178 = gtk.Label('')  # value to be written into simotion

IB181 = gtk.Label('')  # is value valid; 1-ok ; 0-err
QD182 = gtk.Label('')  # actual value (recieved from sim)

IW182 = gtk.Label('')  # parameter number
IW184 = gtk.Label('')  # parameter index

bin_in = gtk.Label('')  # binin debug
bin_val_send = gtk.Label('')

axe_output = gtk.Label('0')
value_to_format = gtk.Label('1105723392')

md = gtk.MessageDialog(None, gtk.DIALOG_DESTROY_WITH_PARENT,
                       gtk.MESSAGE_WARNING, gtk.BUTTONS_CLOSE, "Value is out of range!\n")

# Test entry:
# testEntry = plcEntry('IW_S_PL_diag_message_high_word')

# COMBO BOX for axe selecting:
cb = gtk.combo_box_new_text()
cb.append_text('RUKA')
cb.append_text('ZASOBNIK')
cb.append_text('CU320')
cb.modify_font(pango.FontDescription('Monospace Bold 16'))
cb.connect('changed', axeValUpdate)
cb.set_size_request(width=100, height=30)

# INPUT BOX for param number write
pe = gtk.Entry()
pe.set_text('0')
pe.set_editable(True)
pe.set_sensitive(True)
pe.set_size_request(width=200, height=30)

# INPUT BOX for param index write
pi = gtk.Entry()
pi.set_text('0')
pi.set_editable(True)
pi.set_sensitive(True)
pi.set_size_request(width=100, height=30)

# COMBO BOX for value format:
fcb = gtk.combo_box_new_text()
fcb.modify_font(pango.FontDescription('Monospace Bold 16'))
fcb.append_text('HEX')
fcb.append_text('DECIMAL')
fcb.append_text('FLOAT')
fcb.connect('changed', formatChanged)
fcb.set_size_request(width=100, height=30)

# INPUT BOX for paramter value (read only)
pv = gtk.Entry()
pv.set_text('0')
pv.set_editable(True)
pv.set_sensitive(False)
pv.set_size_request(width=100, height=30)

# INPUT BOX for new paramter value
pvn = gtk.Entry()
pvn.set_text('0')
pvn.set_editable(True)
pvn.set_sensitive(True)
pvn.set_size_request(width=100, height=30)

# INPUT BOX parameter check ok
pch = gtk.Entry()
pch.set_text('None')
pch.set_editable(True)
pch.set_sensitive(False)
pch.set_size_request(width=60, height=30)

# Button for write param
btn_write = gtk.Button('WRITE')
btn_write.set_size_request(width=100, height=40)
btn_write.set_alignment(0.5, 0.5)
btn_write.connect('pressed', startWrite)
btn_write.connect('released', stopWrite)

qct = table()
qct.set_border_width(5)

qct.attachToCell(bigLabel('OSA'), xpadding=5, ypadding=5, col=1,
                 row=1)                              # static text
qct.attachToCell(bigLabel('CISLO PARAMETRU'), xpadding=5, ypadding=5,
                 col=1, row=2)                              # static text
qct.attachToCell(bigLabel('INDEX'), xpadding=5, ypadding=5,
                 col=1, row=3)                                # static text
qct.attachToCell(bigLabel('FORMAT VYSLEDKU'), xpadding=5, ypadding=5,
                 col=1, row=4)                                # static text
qct.attachToCell(bigLabel('HODNOTA PARAMETRU'),
                 xpadding=5, ypadding=5, col=1, row=5)
qct.attachToCell(bigLabel('NOVA HODNOTA'),
                 xpadding=5, ypadding=5, col=1, row=6)

#qct.attachToCell(plcEntry(plcSymbol='MG_SK_Simotion_write'), xpadding = 5, ypadding = 5, col=1, row=7)

qct.attachToCell(cb, xpadding=20, ypadding=5, col=2,
                 row=1)    # b190.7    &  B191
qct.attachToCell(pe, xpadding=20, ypadding=5,
                 col=2, row=2)   # b190.6    &  B192
qct.attachToCell(pi, xpadding=20, ypadding=5,
                 col=2, row=3)   # b190.5    &  B193
qct.attachToCell(fcb, xpadding=20, ypadding=5,
                 col=2, row=4)  # b190.4    &  B194
qct.attachToCell(pv, xpadding=20, ypadding=5,
                 col=2, row=5)  # b190.4    &  B194
qct.attachToCell(pvn, xpadding=20, ypadding=5,
                 col=2, row=6)  # b190.4    &  B194
#qct.attachToCell(bin_in,xpadding=20, ypadding=5, col=2, row=12)

qct.attachToCell(pch, xpadding=2, ypadding=5,
                 col=3, row=5)  # b190.4    &  B194
qct.attachToCell(axe_output, xpadding=20, col=3, row=1)

IB177.set_text(axe_output.get_text())
IW182.set_text(pe.get_text())
IW184.set_text(pi.get_text())
ID178.set_text(pvn.get_text())

pe.connect('changed', updateOutput)
pi.connect('changed', updateOutput)
pvn.connect('changed', updateOutput)

#qct.attachToCell(IB177, xpadding=20, ypadding=5, col=2, row=7)
#qct.attachToCell(IW182, xpadding=20, ypadding=5, col=2, row=8)
#qct.attachToCell(IW184, xpadding=20, ypadding=5, col=2, row=9)
#qct.attachToCell(ID178, xpadding=20, ypadding=5, col=2, row=10)
qct.attachToCell(btn_write, xpadding=20, ypadding=50, col=2, row=11)

# init default options for combo boxes
cb.set_active(0)  # set first option as default
fcb.set_active(1)  # set decimal as default

# MAIN

jh.Subscribe(ident=GLOBAL_SYMBOL + 'IW_S_PL_diag_message_low_word',
             notify=actualValue, downTime=0.2, onChange=False)
jh.Subscribe(ident=GLOBAL_SYMBOL + 'MG_SK_Simotion_write',
             notify=setDefaultValues, downTime=0.2, onChange=True)
jh.Subscribe(ident=GLOBAL_SYMBOL + 'IB_S_PLC_o_rdpar_status',
             notify=paramOk, downTime=0.2, onChange=False)

myWindow.pack_start(qct)
