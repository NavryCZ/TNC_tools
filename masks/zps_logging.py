'''
################################################
  _      ____   _____  _____ _____ _   _  _____
 | |    / __ \ / ____|/ ____|_   _| \ | |/ ____|
 | |   | |  | | |  __| |  __  | | |  \| | |  __
 | |   | |  | | | |_ | | |_ | | | | . ` | | |_ |
 | |___| |__| | |__| | |__| |_| |_| |\  | |__| |
 |______\____/ \_____|\_____|_____|_| \_|\_____|

################################################

v2.3
 - pallet changer signals
 - delay between generating header file from 10 to 120s (prevent downloading corrupted service file)
v2.2
 - added delay between subsriptions 0.1s for optimization
v2.1
 - added cycle update for header for reliability
 - fixed timestamps for TNCScope be able to read it
'''

from logging.handlers import RotatingFileHandler
import logging
import gobject
from time import gmtime, strftime
from COMMON.mnavratil import *
from collections import OrderedDict
from COMMON.plcSymbolDefinitions import *  # included for python
from COMMON.plcgtk import *  # included for python - load plcgtk widgets
from COMMON.get_text import txt              # function to translate a text
# function to set the path and the domain for translation
from COMMON.get_text import bindTextDomain
import os
import time
import sys                  # system functions
import gtk                  # included for python - load plcgtk widgetspygtk functions
# included for python - load plcgtk widgetsjh.gtk class incl. window-registration
import jh.gtk
# included for python - load plcgtk widgetsData-Access interface and Main-function
import jh
hardtest = False


# Logging configuration
output_format = logging.Formatter('%(message)s')

logFile = '/mnt/plc/service/logging.txt'

log_handler = RotatingFileHandler(logFile, mode='a', maxBytes=10*1024*1024,
                                  backupCount=3, encoding=None, delay=1)
log_handler.setFormatter(output_format)
log_handler.setLevel(logging.INFO)

mask_logger = logging.getLogger('main')
mask_logger.setLevel(logging.INFO)

mask_logger.addHandler(log_handler)



def log_add(message='default'):
    pass


class PLC_Logging():
    def __init__(self):
        self.symbols = log_variables
        self.buffer_dict = OrderedDict()
        self.counter = 0

    def add_raw_value(self, name, value):
        self.buffer_dict[str(name)] = str(value)

    def add_special(self, special, seconds=0.1, onchange=False):
        self.handle_special = jh.Subscribe(
            ident=GLOBAL_SYMBOL + special, notify=self.buffer_update, downTime=seconds, onChange=onchange)
        log_add('special "{}" added.'.format(special))

    def start(self):

        for self.symbol in self.symbols:
            # time.sleep(0.1)
            self.handle = jh.Subscribe(
                ident=GLOBAL_SYMBOL + self.symbol, notify=self.buffer_update, downTime=0.5, onChange=True)
            log_add('symbol "{}" added.'.format(self.symbol))

        gobject.timeout_add(1000, self.logdata)

    def buffer_update(self, value_dict=None, event=None):
        value = str(value_dict.values()[0])

        if value == 'True':
            value = '1'

        if value == 'False':
            value = '0'

        self.buffer_dict[value_dict.keys()[0]] = value

        # log_add('updated')

    def logdata(self):
        self.counter += 1
        # log_add(';'.join(self.buffer_dict.values()))
        mask_logger.info(strftime("%Y%m%d%H%M%S;", gmtime()) +
                         ';'.join(self.buffer_dict.values()))
        #log_add(', '.join(self.buffer_dict.keys()))
        if self.counter == 120:
            outfile = open('/mnt/plc/service/logging_header.txt', "w")
            outfile.writelines('YYYYMMDDHHMMSS;' +
                               ';'.join(self.buffer_dict.keys()))
            outfile.close()
            self.counter = 0

        return True


# Console window for debug purposes
'''
my_sw = gtk.ScrolledWindow(hadjustment=None, vadjustment=None)
my_sw.set_policy(hscrollbar_policy=gtk.POLICY_AUTOMATIC, vscrollbar_policy=gtk.POLICY_AUTOMATIC)
my_viewport = gtk.Viewport()
my_VBox = gtk.VBox(homogeneous=False, spacing=0)
my_viewport.add(my_VBox)
my_sw.add(my_viewport)
app.tabs.append_page(my_sw)
app.tabs.set_tab_label_text(my_sw, "console")
'''

# Logging
axis_count = (jh.Get(GLOBAL_SYMBOL + 'ApiGen.NN_GenAxCount')).values()[0]
spindle_count = (jh.Get(GLOBAL_SYMBOL + 'ApiGen.NN_GenSpiCount')).values()[0]


log_variables = []


# spindles
for i in range(0, spindle_count):
    spindle_log_count = (
        jh.Get(GLOBAL_SYMBOL + 'ApiSpin[{}].NN_SpiLogNumber'.format(i))).values()[0]
    if spindle_log_count > -1:
        log_variables.extend(['Spindle[{}].DG_actual_rpm'.format(i),
                              'Spindle[{}].DG_motor_temperature'.format(i),
                              'Spindle[{}].DG_motor_utilization'.format(i),
                              'Spindle[{}].DG_tool_in_spindle'.format(i),
                              'Spindle[{}].MG_brake_active'.format(i),
                              'Spindle[{}].MG_brake_unclamped'.format(i),
                              'Spindle[{}].MG_clamped'.format(i),
                              'Spindle[{}].MG_unclamped'.format(i),
                              'Spindle[{}].MG_tool_in_spindle_index'.format(i),
                              'Spindle[{}].MG_touch_probe_active'.format(i)])

    if (jh.Get(GLOBAL_SYMBOL + 'Spindle[{}].MG_spindle_with_gear'.format(i))).values()[0] == True:
        log_variables.extend(['I_S1_gear_range_1', 'I_S1_gear_range_2'])
        log_variables.extend(['Spindle[{}].MG_gear_change_active'.format(i),
                              'Spindle[{}].MG_gear_range_activation'.format(i),
                              'Spindle[{}].MG_gear_range_ok'.format(i)])

# axes
for i in range(0, axis_count):
    axis_log_count = (
        jh.Get(GLOBAL_SYMBOL + 'ApiAxis[{}].NN_AxLogNumber'.format(i))).values()[0]
    if axis_log_count > -1:
        log_variables.extend(['Axes[{}].BG_step_axes'.format(i),
                              'Axes[{}].DG_actual_position'.format(i),
                              'Axes[{}].DG_actual_rpm'.format(i),
                              'Axes[{}].DG_motor_temperature'.format(i),
                              'Axes[{}].DG_motor_utilization'.format(i),
                              'Axes[{}].MG_active'.format(i),
                              'Axes[{}].MG_brake_test_configured'.format(i),
                              'Axes[{}].MG_brake_test_sequenz_started'.format(i)])


# vibro

log_variables.append('DG_spin_vibration_x10_mm_s')

# temperatur
log_variables.extend(['DG_temperature_machine_Pt100',
                     'DG_temperature_spindle_Pt100'])

# selftest
log_variables.extend(['NN_GenSafetySelftest', 'ApiGen.NN_GenSafetySelftest'])

# pallet changer
log_variables.extend(['MG_PC_active', 'I_mag_alarm_channel',
                     'O_M_PC_XYZ_in_pos_pal2', 'O_M_PC_XYZ_in_pos_pal1'])

# all signals from siemens pallet changer
log_variables.extend(['I_PC_M_in_basic_position',
                      'I_PC_position_1_occupy',
                      'I_PC_position_2_occupy',
                      'I_PC_M_pal1_enabled',
                      'I_PC_M_pal2_enabled',
                      'I_PC_M_operation_complete',
                      'I_PC_M_Help_active',
                      'I_PC_M_XYZ_to_pal1',
                      'I_PC_M_XYZ_to_pal2',
                      'I_PC_M_unclamp_table',
                      'I_PC_M_clamp_table',
                      'I_PC_M_changer_alarm',
                      'I_PC_M_maintenance_mode',
                      'I_PC_M_Air_blow_high_pressure_ready',
                      'I_PC_M_lifebit'])

#log_handle_subscribe = jh.Subscribe(ident=GLOBAL_SYMBOL + 'MG_clock_3_s', notify=plc_log, downTime=0.2, onChange=True)


logging = PLC_Logging()


logging.start()
