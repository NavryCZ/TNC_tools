
# included for python - load plcgtk widgetsData-Access interface and Main-function
import jh
# included for python - load plcgtk widgetsjh.gtk class incl. window-registration
import jh.gtk
import gtk                  # included for python - load plcgtk widgetspygtk functions
import sys                  # system functions

# function to set the path and the domain for translation
from COMMON.get_text import bindTextDomain
from COMMON.get_text import txt              # function to translate a text
from COMMON.plcgtk import *  # included for python - load plcgtk widgets
from COMMON.plcSymbolDefinitions import *  # included for python


# vytvoreni okna
myWindow = embeddedWindow(usage='PLClarge',
                          title=txt('OPTIONS LIST'),
                          focus=True,
                          plcSymbol=PLC_SYMBOL_OPTIONS)
col = gtk.gdk.Color('#E0E9FE')
myWindow.Viewport.modify_bg(gtk.STATE_NORMAL, col)


def hide(widget=None):
    '''This function will hide this window'''
    jh.Put({(GLOBAL_SYMBOL + PLC_SYMBOL_OPTIONS): 0})


# top right close button
btn_exit = gtk.Button(' X ')
btn_exit.connect('released', hide)
myWindow.headerHBox.pack_start(btn_exit, expand=False, fill=False, padding=10)



# 2 Gifu -> changer_type = 3
# 1 Gifu -> changer_type = 1
# 0 Gifu -> changer_type = 0

all_options = [
    ('NN_MG_BLUM_laser_active', ''),
    ('NN_MG_BLUM_laser_digilog_active', ''),
    ('NN_MG_M07_with_air', ''),
    ('NN_MG_M07_with_mini_lub', ''),
    ('NN_MG_M07_with_water', ''),
    ('NN_MG_M08_with_air', ''),
    ('NN_MG_M08_with_mini_lub', ''),
    ('NN_MG_M08_with_water', ''),
    ('NN_MG_M7_M8_cooling_unit_filter_clog_active', ''),
    ('NN_MG_M7_M8_filter1_clog_signal_positive', ''),
    ('NN_MG_M7_M8_filter2_clog_signal_positive', ''),
    ('NN_MG_M7_M8_together_prohibited', ''),
    ('NN_MG_M7_coolant_level_signal_positive', ''),
    ('NN_MG_M7_cooling_unit_active', ''),
    ('NN_MG_M7_transfer_pump_active', ''),
    ('NN_MG_M8_cooling_unit_active', ''),
    ('NN_MG_Manual_washing_active', ''),
    ('NN_MG_NC4_laser_active', ''),
    ('NN_MG_Oil_aspiration_active', ''),
    ('NN_MG_S1_Kessler_active', ''),
    ('NN_MG_S1_TC_spindle_orient_active', ''),
    ('NN_MG_S1_analog_clamping_active', ''),
    ('NN_MG_S1_check_piston_back_inactive', ''),
    ('NN_MG_S1_checking_leakage_active', ''),
    ('NN_MG_S1_cooling_unit_active', ''),
    ('NN_MG_S1_lubrication_unit_active', ''),

    ('NN_MG_S1_overpressure_air_pressure_switch_active', ''),
    ('NN_MG_S1_overpressure_delay_active', ''),
    ('NN_MG_S1_test_piston_back_inactive', ''),
    ('NN_MG_S1_vibrodiag_active', ''),
    ('NN_MG_S1_warmup_active', ''),
    ('NN_MG_S_override_no_F_stop', ''),
    ('NN_MG_Visiport_active', ''),
    ('NN_MG_axes_with_signal_clamped_Ax4_Ax5', ''),
    ('NN_MG_axes_with_signal_unclamped_Ax4_Ax5', ''),
    ('NN_MG_checked_PT100_sensors', ''),
    ('NN_MG_chip_pump_up_active', ''),
    ('NN_MG_chip_pump_with_Cycle_start', ''),
    ('NN_MG_chipconv_Knoll_active', ''),
    ('NN_MG_commissioning', ''),
    ('NN_MG_coolant_circuit_without_S_start', ''),
    ('NN_MG_el_cabinet_cooling_unit_active', ''),
    ('NN_MG_guard_inactive', ''),
    ('NN_MG_hibernation_active', ''),
    ('NN_MG_hydraulic_pressure_under_piston_active', ''),
    ('NN_MG_pallet_change_inactive', ''),
    ('NN_MG_power_on_clamping_mode_off_Ax4_Ax5', ''),
    ('NN_MG_temperature_comp_inactive', ''),
    ('NN_MG_tool_in_spindle_wrong_monitoring_inactive', ''),
    ('NN_MG_tool_monitoring_inactive', ''),

    ('NN_DG_F_Fmax_override_coupling', ''),
    ('NN_DG_S_max_temperature', ''),
    ('NN_DG_TM_number_of_pockets', ''),
    ('NN_DG_TempComp_type', ''),
    ('NN_DG_Tool_changer_type', ''),
    ('NN_DG_Vibration_level', ''),
    ('NN_DG_clamping_device_type', ''),
    ('NN_DG_feed_PLC', ''),
    ('NN_DG_feed_service', ''),
    ('NN_DG_feed_special_mode', ''),
    ('NN_DG_hydraulic_unit_type', ''),
    ('NN_DG_lubrication_axes_unit_type', ''),
    ('NN_DG_nr_chip_conveyors_active', ''),
    ('NP_DG_nr_level_switches_in_tank', ''),
    ('NN_DG_PC_pos_Ax01_pal1', ''),
    ('NN_DG_S1_U_clamping_kessler', '')


]


def global_parameter_check(parameter):
    folders = ['\\CFG\\CfgOemBool\\',
               '\\CFG\\CfgOemInt\\', '\\CFG\\CfgOemPosition\\']
    for folder in folders:
        param_val = jh.Get(str(folder + parameter))
        if param_val is not None:
            return param_val


def generate_data(options):
    data = []
    for i in range(len(options)):

        parameter = global_parameter_check(options[i][0])

        if parameter == None:
            continue

        first_value = parameter.values()[0]

        if options[i][0] == 'NN_DG_nr_chip_conveyors_active':
            all_values = '|'.join(format(int(x), 'b')
                                  for x in parameter.values()[:6] if x != None)
        else:
            all_values = '|'.join(str(int(x)) if x % 1 == 0 else str(
                x) for x in parameter.values()[:6] if x != None)

        data.append(
            tuple([bool(first_value), options[i][0], all_values, options[i][1]]))

    return data


options_data = generate_data(all_options)


class OptionList(gtk.VBox):
    def __init__(self):
        gtk.VBox.__init__(self)

        store = self.create_model()

        treeView = gtk.TreeView(store)
        treeView.connect("row-activated", self.on_activated)
        treeView.set_rules_hint(True)

        self.pack_start(treeView)

        self.create_columns(treeView)
        self.statusbar = gtk.Statusbar()


        self.show_all()

    def create_model(self):
        store = gtk.ListStore(gobject.TYPE_BOOLEAN, str, str, str)

        for opt in options_data:
            store.append([opt[0], opt[1], opt[2], opt[3]])

        return store

    def create_columns(self, treeView):

        mrenderer = gtk.CellRendererToggle()

        column = gtk.TreeViewColumn("Active", mrenderer, active=0)
        column.set_sort_column_id(0)
        treeView.append_column(column)

        column = gtk.TreeViewColumn("Name", gtk.CellRendererText(), text=1)
        column.set_sort_column_id(1)
        treeView.append_column(column)

        column = gtk.TreeViewColumn("Value", gtk.CellRendererText(), text=2)
        column.set_sort_column_id(2)
        treeView.append_column(column)

        column = gtk.TreeViewColumn(
            "Description", gtk.CellRendererText(), text=3)
        column.set_sort_column_id(3)
        treeView.append_column(column)

    def on_activated(self, widget, row, col):

        model = widget.get_model()
        text = model[row][0] + ", " + model[row][1] + ", " + model[row][2]
        self.statusbar.push(0, text)

    def fixed_toggled(self, cell, path, model):
        # get toggled iter
        iter = model.get_iter((int(path),))
        fixed = model.get_value(iter, COLUMN_FIXED)

        # do something with the value
        fixed = not fixed

        # set new value
        model.set(iter, COLUMN_FIXED, fixed)


myWindow.pack_start(OptionList())

#############################################################################


def mask_show_handler(value, event=None):
    if value.values()[0] in [369]:
        jh.Put({(GLOBAL_SYMBOL + PLC_SYMBOL_OPTIONS): 1})
        jh.Put({(GLOBAL_SYMBOL + 'ApiGen.NP_GenModCode'): -1})


def hide_on_mode_switch(value, event=None):
    if value.values()[0] in [448, 453, 456, 451, 450, 449]:
        jh.Put({(GLOBAL_SYMBOL + PLC_SYMBOL_OPTIONS): 0})


jh.Subscribe(ident=GLOBAL_SYMBOL + 'ApiGen.NP_GenModCode',
             notify=mask_show_handler, downTime=0.2, onChange=True)
jh.Subscribe(ident=GLOBAL_SYMBOL + 'ApiGen.NP_GenKeyCode',
             notify=hide_on_mode_switch, downTime=0.2, onChange=True)
