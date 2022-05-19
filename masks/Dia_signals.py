# -*- coding: UTF-8 -*-

# +----------------------------------+
# |         Signal Diag v2.6         |
# +==================================+
# | + Added Sofina cooling unit      |
# | + Condition for pallet changer   |
# |                                  |
# +----------------------------------+


# IMPORT MODULES
# -----------------------------------------------------------
from COMMON.mnavratil import *
from COMMON.plcSymbolDefinitions import *  # included for python
from COMMON.plcgtk import *  # included for python - load plcgtk widgets
from COMMON.get_text import txt              # function to translate a text
# function to set the path and the domain for translation
from COMMON.get_text import bindTextDomain
import copy
import os
import time
import sys                  # system functions
import gtk                  # included for python - load plcgtk widgetspygtk functions
# included for python - load plcgtk widgetsjh.gtk class incl. window-registration
import jh.gtk
# included for python - load plcgtk widgetsData-Access interface and Main-function
import jh
all_signals_spawned = False


# add few default icons for buttons
ICON_MOT_STATE_1 = 'PLC:\python\picture\signal_diag\prop_off.gif'
ICON_MOT_STATE_2 = 'PLC:\python\picture\signal_diag\prop_on.gif'

FORWARD_ON = os.path.join('PLC:\python\picture\signal_diag', 'forward_on.gif')
FORWARD_OFF = os.path.join(
    'PLC:\python\picture\signal_diag', 'forward_off.gif')
BACKWARD_ON = os.path.join(
    'PLC:\python\picture\signal_diag', 'backward_on.gif')
BACKWARD_OFF = os.path.join(
    'PLC:\python\picture\signal_diag', 'backward_off.gif')

CW_ON = os.path.join('PLC:\python\picture\signal_diag', 'cw_on.gif')
CW_OFF = os.path.join('PLC:\python\picture\signal_diag', 'cw_off.gif')
CCW_ON = os.path.join('PLC:\python\picture\signal_diag', 'ccw_on.gif')
CCW_OFF = os.path.join('PLC:\python\picture\signal_diag', 'ccw_off.gif')

# Get machine type from parameters
# \CFG\CfgOemVersion\version
machine_type = jh.Get('\\CFG\\CfgOemVersion\\version').values()[0]
# 0=no, 1=1gifu, 3=2gifu
gifu_type = int(jh.Get(GLOBAL_SYMBOL + 'NN_DG_Tool_changer_type').values()[0])
oil_aspiration_modules = 1

# add option to show all possible signals for actual machine
show_all_options = 0
mag_pallet_changer = 1

# create main window of mask
app = Diag(plcSymbol=PLC_MG_SK_signals_diag, type=machine_type)

# get last PLC update
lbl_plc_update = gtk.Label('')
plc_time_since_epoch = os.path.getmtime('/mnt/plc/plc/program/MainPgm.src')
date_time_now = time.strftime(
    '%d.%m.%Y %H:%M', time.localtime(plc_time_since_epoch))
lbl_plc_update.set_text('Last PLC update: ' + date_time_now)

app.fixed.put(lbl_plc_update, 10, 800-2)

# wachlist test
# Watchlist(symbol = 'MG_LED_test')


'''
###############################################################################
  __  __  _______      __  __  ___    __   ___             __ ___   ___   ___
 |  \/  |/ ____\ \    / / /_ |/ _ \  / /  / _ \           /_ |__ \ / _ \ / _ \
 | \  / | |     \ \  / /   | | | | |/ /_ | | | |  ______   | |  ) | (_) | | | |
 | |\/| | |      \ \/ /    | | | | | '_ \| | | | |______|  | | / / > _ <| | | |
 | |  | | |____   \  /     | | |_| | (_) | |_| |           | |/ /_| (_) | |_| |
 |_|  |_|\_____|   \/      |_|\___/ \___/ \___/            |_|____|\___/ \___/

###############################################################################

'''

if int(machine_type) in range(1060, 1281):

    app.scheme_name = 'S404E1B_EN.PDF'

    app.fixed.put(app.table, 840, 10)
    app.fixed.put(app.hlp_img, 863, 448+20)

    # add semafor
    app.fixed.put(Semafor('red', 'orange', 'green'), 30, 50)

    # app.fixed.put(Semafor('blue'),200,50)
    # app.fixed.put(Semafor('orange','green','orange'),300,50)
    # app.fixed.put(Semafor('red','orange','blue','green'),400,50)

    # options
    if (jh.Get(GLOBAL_SYMBOL + 'MG_Ax04_active_in_SIK').values()[0] == True or show_all_options):
        app.add(sig_name='SP51', type='pressure sensor', symbol='I_Ax04_sensor_unclamped', location='hydraulic', frame='1', frame_pos={
                "x": 36, "y": 240}, img_active=ICON_GREEN_BIG, img_inactive=ICON_RED_BIG, description='', help_img='sp51_52.jpg', size=10)
        app.add(sig_name='SP52', type='pressure sensor', symbol='I_Ax04_sensor_clamped', location='hydraulic', frame='1', frame_pos={
                "x": 36, "y": 260}, img_active=ICON_GREEN_BIG, img_inactive=ICON_RED_BIG, description='', help_img='sp51_52.jpg', size=10)

    if (jh.Get(GLOBAL_SYMBOL + 'MG_Ax05_active_in_SIK').values()[0] == True or show_all_options):
        app.add(sig_name='SP46', type='pressure sensor', symbol='I_Ax05_sensor_unclamped', location='hydraulic', frame='1', frame_pos={
                "x": 36, "y": 320}, img_active=ICON_GREEN_BIG, img_inactive=ICON_RED_BIG, description='', help_img='sp46_47.jpg', size=10)
        app.add(sig_name='SP47', type='pressure sensor', symbol='I_Ax05_sensor_clamped', location='hydraulic', frame='1', frame_pos={
                "x": 36, "y": 340}, img_active=ICON_GREEN_BIG, img_inactive=ICON_RED_BIG, description='', help_img='sp46_47.jpg', size=10)

    if (jh.Get(GLOBAL_SYMBOL + 'NN_MG_Oil_aspiration_active').values()[0] == True and oil_aspiration_modules == 1 and gifu_type in [0, 1] or show_all_options):
        app.add(sig_name='M75', type='oil aspiration', symbol='O_oil_aspiration', location='working area', frame='1', frame_pos={
                "x": 587, "y": 523}, img_active=CW_ON, img_inactive=CW_OFF, description='', help_img='', size=24)
        if gifu_type == 1:
            app.set_bg(os.path.join(
                'PLC:\python\picture\signal_diag', '1060_gifu.png'))

    if (jh.Get(GLOBAL_SYMBOL + 'NN_MG_Oil_aspiration_active').values()[0] == True and oil_aspiration_modules == 1 and gifu_type == 3 or show_all_options):
        app.add(sig_name='M75', type='oil aspiration', symbol='O_oil_aspiration', location='working area', frame='1', frame_pos={
                "x": 380, "y": 180-20}, img_active=CW_ON, img_inactive=CW_OFF, description='', help_img='', size=28)
        app.set_bg(os.path.join(
            'PLC:\python\picture\signal_diag', '1060_2gifu_oil.png'))

    if (jh.Get(GLOBAL_SYMBOL + 'NN_MG_Oil_aspiration_active').values()[0] == False and oil_aspiration_modules == 1 and gifu_type == 3 or show_all_options):
        app.set_bg(os.path.join('PLC:\python\picture\signal_diag',
                   '1060_2gifu.png'))  # 2 gifu

    if (jh.Get(GLOBAL_SYMBOL + 'BG_Hydraulic_unit_type').values()[0] == 1 or show_all_options):
        app.add(sig_name='SP36', type='pressure sensor', symbol='I_hydraulic_low_pressure_ok', location='hydraulic', frame='1', frame_pos={
                "x": 36, "y": 280}, img_active=ICON_GREEN_BIG, img_inactive=ICON_RED_BIG, description='', help_img='sp36_37.jpg', size=10)
        app.add(sig_name='SP37', type='pressure sensor', symbol='I_hydraulic_pressure_ok', location='hydraulic', frame='1', frame_pos={
                "x": 36, "y": 300}, img_active=ICON_GREEN_BIG, img_inactive=ICON_RED_BIG, description='', help_img='sp36_37.jpg', size=10)

    # hydraulic unit type ([1,4] - tank + M36, SP36, SP37 , [2,3] - only M36
    if (jh.Get(GLOBAL_SYMBOL + 'BG_Hydraulic_unit_type').values()[0] in range(1, 5) or show_all_options):
        if (jh.Get(GLOBAL_SYMBOL + 'BG_Hydraulic_unit_type').values()[0] in [1, 4] or show_all_options):
            app.add(sig_name='SP36', type='pressure sensor', symbol='I_hydraulic_low_pressure_ok', location='hydraulic', frame='1', frame_pos={
                    "x": 36, "y": 280}, img_active=ICON_GREEN_BIG, img_inactive=ICON_RED_BIG, description='', help_img='sp36_37.jpg', size=12)
            app.add(sig_name='SP37', type='pressure sensor', symbol='I_hydraulic_pressure_ok', location='hydraulic', frame='1', frame_pos={
                    "x": 36, "y": 300}, img_active=ICON_GREEN_BIG, img_inactive=ICON_RED_BIG, description='', help_img='', size=12)
        
        app.add(sig_name='M36', type='hydraulic unit', symbol='O_hydraulic_on', location='hydraulic box', frame='1', frame_pos={
                "x": 36+55, "y": 320-30}, img_active=ICON_GREEN_BIG, img_inactive=ICON_RED_BIG, description='', help_img='', size=14)

    # manual washing option -> O_manual_washing_on -> M73
    if (jh.Get(GLOBAL_SYMBOL + 'NN_MG_manual_washing_active').values()[0] == True or show_all_options):
        app.add(sig_name='M73', type='water pump', symbol='O_manual_washing_on', location='tank', frame='1', frame_pos={
                "x": 775, "y": 220+125}, img_active=ICON_GREEN_BIG, img_inactive=ICON_RED_BIG, description='', help_img='', size=14)

    # Lubrication number is >2 -> O_lubrication_on -> M8
    if (jh.Get("\\PLC\\program\\symbol\\module\\'LubricationAxes.src'\\BL_DG_lubrication_axes_unit_type").values()[0] > 2 or show_all_options):
        app.add(sig_name='M8', type='oil pump', symbol='O_lubrication_on', location='hydraulic', frame='1', frame_pos={
                "x": 36+55, "y": 320-10}, img_active=ICON_GREEN_BIG, img_inactive=ICON_RED_BIG, description='', help_img='', size=14)

    # M07 with air option -> O_M07_air_on -> YV8
    if (jh.Get(GLOBAL_SYMBOL + 'NN_MG_M07_with_air').values()[0] == True or show_all_options):
        app.add(sig_name='YV8', type='air valve', symbol='O_M07_air_on', location='tank', frame='1', frame_pos={
                "x": 36+55, "y": 320-30}, img_active=ICON_GREEN_BIG, img_inactive=ICON_RED_BIG, description='', help_img='', size=14)

    # M07 transfer pump option -> O_M07_transfer_pump_on -> M6
    if (jh.Get(GLOBAL_SYMBOL + 'NN_MG_M7_transfer_pump_active').values()[0] == True or show_all_options):
        app.add(sig_name='M6', type='water pump', symbol='O_M07_transfer_pump_on', location='tank', frame='1', frame_pos={
                "x": 775, "y": 220+75}, img_active=ICON_GREEN_BIG, img_inactive=ICON_RED_BIG, description='', help_img='pumpa_zadni.jpg', size=14)

    # M07 with water option -> O_M07_water_on -> M5
    if (jh.Get(GLOBAL_SYMBOL + 'NN_MG_M07_with_water').values()[0] == True or show_all_options):
        app.add(sig_name='M5', type='water pump', symbol='O_M07_water_on', location='tank', frame='1', frame_pos={
                "x": 775, "y": 220+50}, img_active=ICON_GREEN_BIG, img_inactive=ICON_RED_BIG, description='', help_img='pumpa_zadni.jpg', size=14)

    # M08 with air option
    if (jh.Get(GLOBAL_SYMBOL + 'NN_MG_M08_with_air').values()[0] == True or show_all_options):
        app.add(sig_name='YV34', type='air valve', symbol='O_M08_air_on', location='tank', frame='1', frame_pos={
                "x": 36+55, "y": 320-50}, img_active=ICON_GREEN_BIG, img_inactive=ICON_RED_BIG, description='', help_img='', size=14)

    # M08 with water option
    if (jh.Get(GLOBAL_SYMBOL + 'NN_MG_M08_with_water').values()[0] == True or show_all_options):
        app.add(sig_name='M2', type='water pump', symbol='O_M08_water_on', location='tank', frame='1', frame_pos={
                "x": 775, "y": 220}, img_active=ICON_GREEN_BIG, img_inactive=ICON_RED_BIG, description='', help_img='pumpa_zadni.jpg', size=14)

    if (jh.Get(GLOBAL_SYMBOL + 'NN_MG_chip_pump_up_active').values()[0] == True or show_all_options):
        app.add(sig_name='M7', type='water pump', symbol='O_chip_clear_pump_up_on', location='tank', frame='1', frame_pos={
                "x": 775, "y": 220+100}, img_active=ICON_GREEN_BIG, img_inactive=ICON_RED_BIG, description='', help_img='', size=14)

    app.add(sig_name='COOLING_OK', type='fan', symbol='I_cabinet_cooling_unit_ready', location='box of drivers', frame='1', frame_pos={
            "x": 600, "y": 163}, img_active=ICON_GREEN_BIG, img_inactive=ICON_RED_BIG, description='', help_img='', size=14)

    # Pumps:
    app.add(sig_name='M4', type='water pump', symbol='O_chip_clear_pump_on', location='tank', frame='1', frame_pos={
            "x": 775, "y": 220+25}, img_active=ICON_GREEN_BIG, img_inactive=ICON_RED_BIG, description='', help_img='', size=14)

    # external input pressure
    app.add(sig_name='SP10', type='air pressure sensor', symbol='I_pneumatic_pressure_ok', location='pneumatic', frame='1', frame_pos={
            "x": 36, "y": 360}, img_active=ICON_GREEN_BIG, img_inactive=ICON_RED_BIG, description='', help_img='sp51_52.jpg', size=10)

    # Chip conveyor M3, SK19
    app.add(sig_name='SK19', type='running sensor', symbol='I_chip_conveyor_1_running_sensor', location='tank', frame='1', frame_pos={
            "x": 970, "y": 770}, img_active=ICON_MOT_STATE_1, img_inactive=ICON_MOT_STATE_2, description='', help_img='sk19_m3.jpg', size=18)
    app.add(sig_name='M3', type='motor contactor', symbol='O_chip_conveyor', location='contactor box', frame='1', frame_pos={
            "x": 980, "y": 640}, img_active=FORWARD_ON, img_inactive=FORWARD_OFF, description='', help_img='sk19_m3.jpg', size=14)
    app.add(sig_name='M3', type='motor contactor', symbol='O_chip_conveyor_back', location='contactor box', frame='1', frame_pos={
            "x": 980, "y": 670}, img_active=BACKWARD_ON, img_inactive=BACKWARD_OFF, description='', help_img='sk19_m3.jpg', size=14)

    # spindle air valve
    app.add(sig_name='YV50', type='air valve', symbol='O_S1_air_release_valve', location='spindle', frame='1', frame_pos={
            "x": 382, "y": 606}, img_active=ICON_GREEN_BIG, img_inactive=ICON_RED_BIG, description='', help_img='', size=14)

    # Chip conveyor 2 - M31, SK26 (KM34)
    # app.add(sig_name = 'SK26', type = 'running sensor', symbol='I_chip_conveyor_2_running_sensor', location = 'tank', frame='1', frame_pos = {"x":970, "y":770},img_active= ICON_MOT_STATE_1,img_inactive = ICON_MOT_STATE_2, description = '', help_img = '', size = 18)
    # app.add(sig_name = 'M31', type = 'motor contactor', symbol='O_auxiliary_chip_conveyers_ON', location = 'contactor box', frame='1', frame_pos = {"x":980, "y":640},img_active= FORWARD_ON,img_inactive = FORWARD_OFF, description = '', help_img = '', size = 14)

    # Chip conveyor 3 - M32, SK27
    # app.add(sig_name = 'SK26', type = 'running sensor', symbol='I_chip_conveyor_3_running_sensor', location = 'tank', frame='1', frame_pos = {"x":970, "y":770},img_active= ICON_MOT_STATE_1,img_inactive = ICON_MOT_STATE_2, description = '', help_img = '', size = 18)
    # app.add(sig_name = 'M31', type = 'motor contactor', symbol='O_auxiliary_chip_conveyers_ON', location = 'contactor box', frame='1', frame_pos = {"x":980, "y":640},img_active= FORWARD_ON,img_inactive = FORWARD_OFF, description = '', help_img = '', size = 14)

    # Gearbox cooling
    app.add(sig_name='M50', type='gearbox cooling', symbol='O_Spindle_gear_cooling_on', location='cooling', frame='1', frame_pos={
            "x": 136, "y": 246}, img_active=ICON_GREEN_BIG, img_inactive=ICON_RED_BIG, description='', help_img='', size=14)

    if gifu_type in [1, 3]:
        # GIFU 1
        app.add(sig_name='M401', type='motor contactor', symbol='O_TC_arm_turn_cw', location='GIFU', frame='1', frame_pos={
                "x": 276, "y": 505}, img_active=ICON_GREEN_BIG, img_inactive=ICON_RED_BIG, description='', help_img='', size=14)

        app.add(sig_name='POCKET_IN', type='GIFU input', symbol='I_TM_1_pocket_in', location='', frame='1', frame_pos={
                "x": 175+70, "y": 440}, img_active=ICON_GREEN_BIG, img_inactive=ICON_RED_BIG, description='', help_img='', size=14)
        app.add(sig_name='POCKET_OUT', type='GIFU input', symbol='I_TM_1_pocket_out', location='', frame='1', frame_pos={
                "x": 175+70, "y": 440+25}, img_active=ICON_GREEN_BIG, img_inactive=ICON_RED_BIG, description='', help_img='', size=14)
        app.add(sig_name='YV402', type='GIFU output', symbol='O_TM_1_pocket_put_in', location='', frame='1', frame_pos={
                "x": 175, "y": 440}, img_active=ICON_GREEN_BIG, img_inactive=ICON_RED_BIG, description='', help_img='', size=14)
        app.add(sig_name='YV403', type='GIFU output', symbol='O_TM_1_pocket_put_out', location='', frame='1', frame_pos={
                "x": 175, "y": 440+25}, img_active=ICON_GREEN_BIG, img_inactive=ICON_RED_BIG, description='', help_img='', size=14)

        app.add(sig_name='ARM_BRAKE_POS', type='GIFU input', symbol='I_TC_arm_brake_pos', location='', frame='1', frame_pos={
                "x": 220, "y": 560}, img_active=ICON_GREEN_BIG, img_inactive=ICON_RED_BIG, description='', help_img='', size=14)
        app.add(sig_name='ARM_BASIC_POS', type='GIFU input', symbol='I_TC_arm_basic_pos', location='', frame='1', frame_pos={
                "x": 220, "y": 560+25}, img_active=ICON_GREEN_BIG, img_inactive=ICON_RED_BIG, description='', help_img='', size=14)
        app.add(sig_name='ARM_SPINDLE_POS', type='GIFU input', symbol='I_TC_arm_spindle_pos', location='', frame='1', frame_pos={
                "x": 220, "y": 560+50}, img_active=ICON_GREEN_BIG, img_inactive=ICON_RED_BIG, description='', help_img='', size=14)

        app.add(sig_name='TM1_COUNTER', type='GIFU input', symbol='I_TM_1_counter', location='', frame='1', frame_pos={
                "x": 60, "y": 550}, img_active=ICON_GREEN_BIG, img_inactive=ICON_RED_BIG, description='', help_img='', size=14)
        app.add(sig_name='TM1_REFERENCE', type='GIFU input', symbol='I_TM_1_reference', location='', frame='1', frame_pos={
                "x": 60, "y": 550+25}, img_active=ICON_GREEN_BIG, img_inactive=ICON_RED_BIG, description='', help_img='', size=14)

        app.add(sig_name='KM403', type='GIFU CW output', symbol='O_TM_1_plus', location='', frame='1', frame_pos={
                "x": 65, "y": 450}, img_active=CW_ON, img_inactive=CW_OFF, description='', help_img='', size=18)
        app.add(sig_name='KM404', type='GIFU CCW output', symbol='O_TM_1_minus', location='', frame='1', frame_pos={
                "x": 65, "y": 450+30}, img_active=CCW_ON, img_inactive=CCW_OFF, description='', help_img='', size=18)

    if gifu_type == 3:
        # GIFU 2
        app.add(sig_name='M401.2', type='motor contactor', symbol='O_TC_arm_2G_turn_cw', location='GIFU', frame='1', frame_pos={
                "x": 486, "y": 505}, img_active=ICON_GREEN_BIG, img_inactive=ICON_RED_BIG, description='', help_img='', size=14)

        app.add(sig_name='POCKET_IN', type='GIFU input', symbol='I_TM_2_pocket_in', location='', frame='1', frame_pos={
                "x": 500, "y": 440}, img_active=ICON_GREEN_BIG, img_inactive=ICON_RED_BIG, description='', help_img='', size=14)
        app.add(sig_name='POCKET_OUT', type='GIFU input', symbol='I_TM_2_pocket_out', location='', frame='1', frame_pos={
                "x": 500, "y": 440+25}, img_active=ICON_GREEN_BIG, img_inactive=ICON_RED_BIG, description='', help_img='', size=14)
        app.add(sig_name='YV402.2', type='GIFU output', symbol='O_TM_2_pocket_put_in', location='', frame='1', frame_pos={
                "x": 600, "y": 440}, img_active=ICON_GREEN_BIG, img_inactive=ICON_RED_BIG, description='', help_img='', size=14)
        app.add(sig_name='YV403.2', type='GIFU output', symbol='O_TM_2_pocket_put_out', location='', frame='1', frame_pos={
                "x": 600, "y": 440+25}, img_active=ICON_GREEN_BIG, img_inactive=ICON_RED_BIG, description='', help_img='', size=14)

        app.add(sig_name='ARM_BRAKE_POS', type='GIFU input', symbol='I_TC_arm_2G_brake_pos', location='', frame='1', frame_pos={
                "x": 560, "y": 560}, img_active=ICON_GREEN_BIG, img_inactive=ICON_RED_BIG, description='', help_img='', size=14)
        app.add(sig_name='ARM_BASIC_POS', type='GIFU input', symbol='I_TC_arm_2G_basic_pos', location='', frame='1', frame_pos={
                "x": 560, "y": 560+25}, img_active=ICON_GREEN_BIG, img_inactive=ICON_RED_BIG, description='', help_img='', size=14)
        app.add(sig_name='ARM_SPINDLE_POS', type='GIFU input', symbol='I_TC_arm_2G_spindle_pos', location='', frame='1', frame_pos={
                "x": 560, "y": 560+50}, img_active=ICON_GREEN_BIG, img_inactive=ICON_RED_BIG, description='', help_img='', size=14)

        app.add(sig_name='TM1_COUNTER', type='GIFU input', symbol='I_TM_2_counter', location='', frame='1', frame_pos={
                "x": 690, "y": 550}, img_active=ICON_GREEN_BIG, img_inactive=ICON_RED_BIG, description='', help_img='', size=14)
        app.add(sig_name='TM1_REFERENCE', type='GIFU input', symbol='I_TM_2_reference', location='', frame='1', frame_pos={
                "x": 690, "y": 550+25}, img_active=ICON_GREEN_BIG, img_inactive=ICON_RED_BIG, description='', help_img='', size=14)

        app.add(sig_name='KM403.2', type='GIFU CW output', symbol='O_TM_2_plus', location='', frame='1', frame_pos={
                "x": 65+620, "y": 450}, img_active=CW_ON, img_inactive=CW_OFF, description='', help_img='', size=18)
        app.add(sig_name='KM404.2', type='GIFU CCW output', symbol='O_TM_2_minus', location='', frame='1', frame_pos={
                "x": 65+620, "y": 450+30}, img_active=CCW_ON, img_inactive=CCW_OFF, description='', help_img='', size=18)

    # classic spindle sensor
    if (jh.Get(GLOBAL_SYMBOL + PLC_KESSLER_ACTIVE).values()[0] == False or show_all_options):
        app.add(sig_name='SQ1', type='induction sensor', symbol='I_sensor_S1_clamped', location='spindle', frame='1', frame_pos={
                "x": 410-2, "y": 585}, img_active=ICON_GREEN_BIG, img_inactive=ICON_RED_BIG, description='', help_img='', size=14)
        app.add(sig_name='SQ2', type='induction sensor', symbol='I_sensor_S1_unclamped', location='spindle', frame='1', frame_pos={
                "x": 410-2+5, "y": 585-20}, img_active=ICON_GREEN_BIG, img_inactive=ICON_RED_BIG, description='', help_img='', size=14)
        app.add(sig_name='SQ9', type='induction sensor', symbol='I_sensor_tool_not_located_in_spindle', location='spindle', frame='1', frame_pos={
                "x": 360-2, "y": 585}, img_active=ICON_GREEN_BIG, img_inactive=ICON_RED_BIG, description='', help_img='', size=14)
        app.add(sig_name='BT7', type='proximity sensor', symbol='I_S1_leakage_monitoring_ok', location='', frame='1', frame_pos={
                "x": 390+5, "y": 565-20}, img_active=ICON_GREEN_BIG, img_inactive=ICON_RED_BIG, description='', help_img='', size=14)
        app.add(sig_name='BT1', type='PT100 TSK-PT4A11', symbol='IW_temperature_spindle_head', location='spindle ledge', frame='1',
                frame_pos={"x": 440, "y": 270}, img_active=ICON_GREEN_BIG, img_inactive=ICON_RED_BIG, description='', help_img='', size=14)
        app.add(sig_name='BT4', type='PT100 TSK-PT4A11', symbol='IW_temperature_spindle_Pt100', location='spindle tubus', frame='1',
                frame_pos={"x": 390-30, "y": 565}, img_active=ICON_GREEN_BIG, img_inactive=ICON_RED_BIG, description='', help_img='', size=14)

    # kessler spindle
    if (jh.Get(GLOBAL_SYMBOL + PLC_KESSLER_ACTIVE).values()[0] == True or show_all_options):
        app.add(sig_name='CLAMPED', type='kessler clamped', symbol='I_S1_clamped', location='spindle', frame='1', frame_pos={
                "x": 410-2, "y": 585}, img_active=ICON_GREEN_BIG, img_inactive=ICON_RED_BIG, description='', help_img='', size=14)
        app.add(sig_name='S4', type='Analog voltage *0.01V', symbol='IW_S1_analog_clamping_position', location='spindle', frame='1',
                frame_pos={"x": 360, "y": 585}, img_active=ICON_GREEN_BIG, img_inactive=ICON_RED_BIG, description='', help_img='', size=14)

        app.add(sig_name='T_IN', type='kessler tool in', symbol='I_tool_located_in_spindle', location='spindle', frame='1', frame_pos={
                "x": 382, "y": 585-20}, img_active=ICON_GREEN_BIG, img_inactive=ICON_RED_BIG, description='', help_img='', size=14)
        #app.add(sig_name='S11', type='kessler piston back', symbol='I_S1_piston_back', location='spindle', frame='1', frame_pos={"x": 360-2, "y": 585}, img_active=ICON_RED_BIG, img_inactive=ICON_GREEN_BIG, description='', help_img='', size=14)

        app.fixed.put(Dia_image(OPTION_IMAGE), 110, 50)
        app.fixed.put(gtk.Label('KESSLER SPINDLE'), 160, 52)
        app.add(sig_name='S8', type='spindle bearing temp*0.01', symbol='IW_temperature_spindle_head', location='spindle', frame='1',
                frame_pos={"x": 125, "y": 80}, img_active=ICON_GREEN_BIG, img_inactive=ICON_RED_BIG, description='', help_img='', size=12)
        app.add(sig_name='YV8', type='inner air cooling', symbol='O_M07_air_on', location='spindle', frame='1', frame_pos={
                "x": 125, "y": 100}, img_active=ICON_GREEN_BIG, img_inactive=ICON_RED_BIG, description='', help_img='', size=12)
        app.add(sig_name='BT4', type='PT100 TSK-PT4A11', symbol='IW_temperature_spindle_Pt100', location='spindle tubus', frame='1',
                frame_pos={"x": 125, "y": 120}, img_active=ICON_GREEN_BIG, img_inactive=ICON_RED_BIG, description='', help_img='', size=12)
        app.add(sig_name='S10', type='proximity sensor', symbol='I_S1_leakage_monitoring_ok', location='', frame='1', frame_pos={
                "x": 125, "y": 140}, img_active=ICON_GREEN_BIG, img_inactive=ICON_RED_BIG, description='', help_img='', size=12)
        app.add(sig_name='S11', type='kessler piston back', symbol='I_S1_piston_back', location='spindle', frame='1', frame_pos={
                "x": 125, "y": 160}, img_active=ICON_RED_BIG, img_inactive=ICON_GREEN_BIG, description='', help_img='', size=12)

        app.add(sig_name='SP80', type='pressure sensor', symbol='I_S1_lubricant_oil_pressure_ok', location='pneumatic', frame='1', frame_pos={
                "x": 36, "y": 380}, img_active=ICON_GREEN_BIG, img_inactive=ICON_RED_BIG, description='', help_img='sp51_52.jpg', size=10)
        app.add(sig_name='SP81', type='pressure sensor', symbol='I_S1_lubricant_air_pressure_ok', location='pneumatic', frame='1', frame_pos={
                "x": 36, "y": 400}, img_active=ICON_GREEN_BIG, img_inactive=ICON_RED_BIG, description='', help_img='sp51_52.jpg', size=10)

    # temperature sensor
    app.add(sig_name='BT2', type='PT100 TSK-PT4A11', symbol='IW_temperature_machine_Pt100', location='basis', frame='1',
            frame_pos={"x": 264, "y": 251}, img_active=ICON_GREEN_BIG, img_inactive=ICON_RED_BIG, description='', help_img='', size=14)
    app.add(sig_name='BT3', type='proximity sensor', symbol='I_S1_gear_oil_flow_ok', location='', frame='1', frame_pos={
            "x": 136+10, "y": 246+30}, img_active=ICON_GREEN_BIG, img_inactive=ICON_RED_BIG, description='', help_img='', size=14)

    # doors
    app.add(sig_name='LOCKED', type='door', symbol='I_guard_1_closed_locked', location='', frame='1', frame_pos={
            "x": 340, "y": 680+20}, img_active=ICON_GREEN_BIG, img_inactive=ICON_RED_BIG, description='', help_img='', size=12)
    app.add(sig_name='UNLOCK', type='door', symbol='MG_FS_guard_1_unlock', location='', frame='1', frame_pos={
            "x": 340, "y": 680+40}, img_active=ICON_GREEN_BIG, img_inactive=ICON_RED_BIG, description='', help_img='', size=12)
    app.add(sig_name='CLOSED', type='door', symbol='I_guard_1_closed', location='', frame='1', frame_pos={
            "x": 340, "y": 680}, img_active=ICON_GREEN_BIG, img_inactive=ICON_RED_BIG, description='', help_img='', size=12)


'''
##################################################################################
  __  __  _______      __  __   __   ___   ___             ___   ___   ___   ___
 |  \/  |/ ____\ \    / / /_ | / /  / _ \ / _ \           |__ \ / _ \ / _ \ / _ \
 | \  / | |     \ \  / /   | |/ /_ | (_) | | | |  ______     ) | | | | (_) | | | |
 | |\/| | |      \ \/ /    | | '_ \ > _ <| | | | |______|   / /| | | |> _ <| | | |
 | |  | | |____   \  /     | | (_) | (_) | |_| |           / /_| |_| | (_) | |_| |
 |_|  |_|\_____|   \/      |_|\___/ \___/ \___/           |____|\___/ \___/ \___/

##################################################################################
'''
# Get main parameters
py_NN_MG_M7_cooling_unit_active = jh.Get(
    GLOBAL_SYMBOL + 'NN_MG_M7_cooling_unit_active').values()[0]
py_NN_MG_M07_with_water = jh.Get(
    GLOBAL_SYMBOL + 'NN_MG_M07_with_water').values()[0]
py_NN_MG_M7_transfer_pump_active = jh.Get(
    GLOBAL_SYMBOL + 'NN_MG_M7_transfer_pump_active').values()[0]
py_NN_MG_M7_M8_cooling_unit_filter_clog_active = jh.Get(
    GLOBAL_SYMBOL + 'NN_MG_M7_M8_cooling_unit_filter_clog_active').values()[0]

if int(machine_type) in range(1680, 2081):
    # NN_MG_M7_M8_filter2_clog_signal_positive
    app.scheme_name = 'S454E1_EN.pdf'
    app.set_bg(os.path.join('PLC:\python\picture\signal_diag', '2080_gifu.png'))
    app.fixed.put(app.watch_send_btn, 860, 310+8+225)

    app.fixed.put(app.table, 840, 235)
    app.fixed.put(app.hlp_img, 863, 650)

    # add semafor
    app.fixed.put(Semafor('red', 'orange', 'green'), 10, 60)

   # app.fixed.put(Semafor('blue'),200,50)
   # app.fixed.put(Semafor('orange','green','orange'),300,50)
   # app.fixed.put(Semafor('red','orange','blue','green'),400,50)

   # options

    if (jh.Get(GLOBAL_SYMBOL + 'MG_Ax04_active_in_SIK').values()[0] == True or show_all_options):
        app.add(sig_name='SP51', type='pressure sensor', symbol='I_Ax04_sensor_unclamped', location='hydraulic', frame='1', frame_pos={
                "x": 55+25, "y": 235}, img_active=ICON_GREEN_BIG, img_inactive=ICON_RED_BIG, description='', help_img='sp51_52.jpg', size=12)
        app.add(sig_name='SP52', type='pressure sensor', symbol='I_Ax04_sensor_clamped', location='hydraulic', frame='1', frame_pos={
                "x": 55+25, "y": 255}, img_active=ICON_GREEN_BIG, img_inactive=ICON_RED_BIG, description='', help_img='sp51_52.jpg', size=12)

    if (jh.Get(GLOBAL_SYMBOL + 'MG_Ax05_active_in_SIK').values()[0] == True or show_all_options):
        app.add(sig_name='SP46', type='pressure sensor', symbol='I_Ax05_sensor_unclamped', location='hydraulic', frame='1', frame_pos={
                "x": 55+25, "y": 235+45}, img_active=ICON_GREEN_BIG, img_inactive=ICON_RED_BIG, description='', help_img='sp46_47.jpg', size=12)
        app.add(sig_name='SP47', type='pressure sensor', symbol='I_Ax05_sensor_clamped', location='hydraulic', frame='1', frame_pos={
                "x": 55+25, "y": 255+45}, img_active=ICON_GREEN_BIG, img_inactive=ICON_RED_BIG, description='', help_img='sp46_47.jpg', size=12)

    if (jh.Get(GLOBAL_SYMBOL + 'NN_MG_Oil_aspiration_active').values()[0] == True and oil_aspiration_modules == 1 and gifu_type in [0, 1] or show_all_options):
        app.add(sig_name='M75', type='oil aspiration', symbol='O_oil_aspiration', location='working area', frame='1', frame_pos={
                "x": 765, "y": 494}, img_active=CW_ON, img_inactive=CW_OFF, description='', help_img='', size=32)
        app.add(sig_name='M75', type='oil aspiration', symbol='O_oil_aspiration', location='working area', frame='1', frame_pos={
                "x": 86, "y": 494}, img_active=CW_ON, img_inactive=CW_OFF, description='', help_img='', size=32)
        if gifu_type == 1:
            # gifu with oil aspiration
            app.set_bg(os.path.join(
                'PLC:\python\picture\signal_diag', '2080_gifu.png'))

    if (jh.Get(GLOBAL_SYMBOL + 'NN_MG_Oil_aspiration_active').values()[0] == True and oil_aspiration_modules == 1 and gifu_type == 3 or show_all_options):
        app.add(sig_name='M75', type='oil aspiration', symbol='O_oil_aspiration', location='working area', frame='1', frame_pos={
                "x": 765, "y": 494}, img_active=CW_ON, img_inactive=CW_OFF, description='', help_img='', size=32)
        app.add(sig_name='M75', type='oil aspiration', symbol='O_oil_aspiration', location='working area', frame='1', frame_pos={
                "x": 86, "y": 494}, img_active=CW_ON, img_inactive=CW_OFF, description='', help_img='', size=32)
        app.set_bg(os.path.join('PLC:\python\picture\signal_diag',
                   '2080_gifu.png'))  # 2 gifu with oil aspiration

    if (jh.Get(GLOBAL_SYMBOL + 'NN_MG_Oil_aspiration_active').values()[0] == False and oil_aspiration_modules == 1 and gifu_type == 3 or show_all_options):
        app.set_bg(os.path.join('PLC:\python\picture\signal_diag',
                   '2080_gifu.png'))  # 2 gifu without oil aspiration

    # hydraulic unit type ([1,4] - tank + M36, SP36, SP37 , [2,3] - only M36
    if (jh.Get(GLOBAL_SYMBOL + 'BG_Hydraulic_unit_type').values()[0] in range(1, 5) or show_all_options):
        if (jh.Get(GLOBAL_SYMBOL + 'BG_Hydraulic_unit_type').values()[0] in [1, 4] or show_all_options):
            app.add(sig_name='SP36', type='pressure sensor', symbol='I_hydraulic_low_pressure_ok', location='hydraulic', frame='1', frame_pos={
                    "x": 110+25, "y": 235}, img_active=ICON_GREEN_BIG, img_inactive=ICON_RED_BIG, description='', help_img='sp36_37.jpg', size=12)
            app.add(sig_name='SP37', type='pressure sensor', symbol='I_hydraulic_pressure_ok', location='hydraulic', frame='1', frame_pos={
                    "x": 110+25, "y": 255}, img_active=ICON_GREEN_BIG, img_inactive=ICON_RED_BIG, description='', help_img='', size=12)
        app.add(sig_name='M36', type='hydraulic unit', symbol='O_hydraulic_on', location='hydraulic box', frame='1', frame_pos={
                "x": 30, "y": 235+43}, img_active=ICON_GREEN_BIG, img_inactive=ICON_RED_BIG, description='', help_img='', size=14)

    # manual washing option -> O_manual_washing_on -> M73
    if (jh.Get(GLOBAL_SYMBOL + 'NN_MG_manual_washing_active').values()[0] == True or show_all_options):
        app.add(sig_name='M73', type='water pump', symbol='O_manual_washing_on', location='tank', frame='1', frame_pos={
                "x": 820+50, "y": 70+50}, img_active=ICON_GREEN_BIG, img_inactive=ICON_RED_BIG, description='', help_img='', size=14)

    # Lubrication number is >2 -> O_lubrication_on -> M8
    if (jh.Get("\\PLC\\program\\symbol\\module\\'LubricationAxes.src'\\BL_DG_lubrication_axes_unit_type").values()[0] > 2 or show_all_options):
        app.add(sig_name='M8', type='oil pump', symbol='O_lubrication_on', location='hydraulic', frame='1', frame_pos={
                "x": 110+25, "y": 255+22}, img_active=ICON_GREEN_BIG, img_inactive=ICON_RED_BIG, description='', help_img='', size=14)

    # M07 with air option -> O_M07_air_on -> YV8
    if (jh.Get(GLOBAL_SYMBOL + 'NN_MG_M07_with_air').values()[0] == True or show_all_options):
        app.add(sig_name='YV8', type='air valve', symbol='O_M07_air_on', location='tank', frame='1', frame_pos={
                "x": 30, "y": 255}, img_active=ICON_GREEN_BIG, img_inactive=ICON_RED_BIG, description='', help_img='', size=12)

    # M07 transfer pump option -> O_M07_transfer_pump_on -> M6
    if (jh.Get(GLOBAL_SYMBOL + 'NN_MG_M7_transfer_pump_active').values()[0] == True or show_all_options):
        app.add(sig_name='M6', type='water pump', symbol='O_M07_transfer_pump_on', location='tank', frame='1', frame_pos={
                "x": 820+50, "y": 70}, img_active=ICON_GREEN_BIG, img_inactive=ICON_RED_BIG, description='', help_img='pumpa_zadni.jpg', size=14)

    # M07 with water option -> O_M07_water_on -> M5
    if (jh.Get(GLOBAL_SYMBOL + 'NN_MG_M07_with_water').values()[0] == True or show_all_options):
        app.add(sig_name='M5', type='water pump', symbol='O_M07_water_on', location='tank', frame='1', frame_pos={
                "x": 820, "y": 70+50}, img_active=ICON_GREEN_BIG, img_inactive=ICON_RED_BIG, description='', help_img='pumpa_zadni.jpg', size=14)

    # M08 with air option
    if (jh.Get(GLOBAL_SYMBOL + 'NN_MG_M08_with_air').values()[0] == True or show_all_options):
        app.add(sig_name='YV34', type='air valve', symbol='O_M08_air_on', location='tank', frame='1', frame_pos={
                "x": 30, "y": 235}, img_active=ICON_GREEN_BIG, img_inactive=ICON_RED_BIG, description='', help_img='', size=12)

    # M08 with water option
    if (jh.Get(GLOBAL_SYMBOL + 'NN_MG_M08_with_water').values()[0] == True or show_all_options):
        app.add(sig_name='M2', type='water pump', symbol='O_M08_water_on', location='tank', frame='1', frame_pos={
                "x": 820, "y": 70}, img_active=ICON_GREEN_BIG, img_inactive=ICON_RED_BIG, description='', help_img='pumpa_zadni.jpg', size=14)

    if (jh.Get(GLOBAL_SYMBOL + 'NN_MG_chip_pump_up_active').values()[0] == True or show_all_options):
        app.add(sig_name='M7', type='water pump', symbol='O_chip_clear_pump_up_on', location='tank', frame='1', frame_pos={
                "x": 820+50, "y": 70+25}, img_active=ICON_GREEN_BIG, img_inactive=ICON_RED_BIG, description='', help_img='', size=14)

    app.add(sig_name='COOLING_OK', type='fan', symbol='I_cabinet_cooling_unit_ready', location='box of drivers', frame='1', frame_pos={
            "x": 653, "y": 212}, img_active=ICON_GREEN_BIG, img_inactive=ICON_RED_BIG, description='', help_img='', size=14)

    # FILTRATION UNIT TECNIMETAL
    if (jh.Get(GLOBAL_SYMBOL + 'NN_MG_M7_transfer_pump_active').values()[0] == True and jh.Get(GLOBAL_SYMBOL + 'NN_MG_M7_M8_cooling_unit_filter_clog_active').values()[0] == True or show_all_options):
        app.fixed.put(Dia_image(OPTION_IMAGE), 27, 664)
        app.fixed.put(gtk.Label('FILTERING UNIT TECNIMETAL'), 40, 667)
        app.add(sig_name='QM5', type='circuit breaker', symbol='I_QM5_2_cbreaker_ok', location='contactor box', frame='1', frame_pos={
                "x": 45, "y": 695}, img_active=ICON_GREEN_BIG, img_inactive=ICON_RED_BIG, description='', help_img='', size=14)
        app.add(sig_name='COOLING_SWITCH_ON', type='cooling switch on', symbol='O_M07_water_on', location='filtration unit', frame='1',
                frame_pos={"x": 95, "y": 695}, img_active=ICON_GREEN_BIG, img_inactive=ICON_RED_BIG, description='', help_img='', size=12)
        app.add(sig_name='COOLING_OK', type='input signal from unit', symbol='I_coolant_M07_unit_OK', location='filtration unit', frame='1',
                frame_pos={"x": 95, "y": 695+20}, img_active=ICON_GREEN_BIG, img_inactive=ICON_RED_BIG, description='', help_img='', size=12)
        app.add(sig_name='FILTERING_OK', type='input signal from unit', symbol='I_coolant_M07_1_water_filter_OK', location='filtration unit',
                frame='1', frame_pos={"x": 95, "y": 695+40}, img_active=ICON_GREEN_BIG, img_inactive=ICON_RED_BIG, description='', help_img='', size=12)
        app.add(sig_name='WATER_FILTER_OK', type='input signal from unit', symbol='I_coolant_M07_2_water_filter_OK', location='filtration unit',
                frame='1', frame_pos={"x": 95, "y": 695+60}, img_active=ICON_GREEN_BIG, img_inactive=ICON_RED_BIG, description='', help_img='', size=12)
        app.add(sig_name='WATER_LEVEL_OK', type='input signal from unit', symbol='I_CoolCircuit_level_ok', location='filtration unit', frame='1',
                frame_pos={"x": 95, "y": 695+80}, img_active=ICON_GREEN_BIG, img_inactive=ICON_RED_BIG, description='', help_img='', size=12)

    # FILTRATION UNIT JV40
    if (py_NN_MG_M7_transfer_pump_active == True and py_NN_MG_M7_M8_cooling_unit_filter_clog_active == False and py_NN_MG_M07_with_water == True and py_NN_MG_M7_cooling_unit_active == False or show_all_options):
        app.fixed.put(Dia_image(OPTION_IMAGE), 27+300, 664)
        app.fixed.put(gtk.Label('CHIPBLASTER JV40'), 40+300+30, 667)
        app.add(sig_name='UNIT_OK', type='input signal from unit', symbol='I_coolant_M07_unit_OK', location='filtration unit', frame='1', frame_pos={
                "x": 45+300, "y": 695}, img_active=ICON_GREEN_BIG, img_inactive=ICON_RED_BIG, description='', help_img='', size=12)
        app.add(sig_name='COOLING_ON', type='cooling switch on', symbol='O_M07_water_on', location='filtration unit', frame='1', frame_pos={
                "x": 95+300+40, "y": 695}, img_active=ICON_GREEN_BIG, img_inactive=ICON_RED_BIG, description='', help_img='', size=12)
        app.add(sig_name='M371', type='M func, set pressure', symbol='MG_M371_act_pressure_1', location='filtration unit', frame='1', frame_pos={
                "x": 95+300+40, "y": 695+20}, img_active=ICON_GREEN_BIG, img_inactive=ICON_RED_BIG, description='', help_img='', size=12)
        app.add(sig_name='M372', type='M func, set pressure', symbol='MG_M372_act_pressure_2', location='filtration unit', frame='1', frame_pos={
                "x": 95+300+40, "y": 695+40}, img_active=ICON_GREEN_BIG, img_inactive=ICON_RED_BIG, description='', help_img='', size=12)
        app.add(sig_name='M373', type='M func, set pressure', symbol='MG_M373_act_pressure_3', location='filtration unit', frame='1', frame_pos={
                "x": 95+300+40, "y": 695+60}, img_active=ICON_GREEN_BIG, img_inactive=ICON_RED_BIG, description='', help_img='', size=12)
        app.add(sig_name='M374', type='M func, set pressure', symbol='MG_M374_act_pressure_4', location='filtration unit', frame='1', frame_pos={
                "x": 95+300+40, "y": 695+80}, img_active=ICON_GREEN_BIG, img_inactive=ICON_RED_BIG, description='', help_img='', size=12)

    # FILTRATION UNIT Sofima
        # NN_MG_M7_cooling_unit_active                  -> False
        # NN_MG_M07_with_water                          -> True
        # NN_MG_M7_transfer_pump_active                 -> False
        # NN_MG_M7_M8_cooling_unit_filter_clog_active   -> True

    if (py_NN_MG_M7_transfer_pump_active == False and py_NN_MG_M7_M8_cooling_unit_filter_clog_active == True and py_NN_MG_M07_with_water == True and py_NN_MG_M7_cooling_unit_active == False or show_all_options):
        app.fixed.put(Dia_image(OPTION_IMAGE), 27+300, 664)
        app.fixed.put(gtk.Label('Sofima'), 40+300+30, 667)
        #app.add(sig_name='UNIT_OK', type='input signal from unit', symbol='I_coolant_M07_unit_OK', location='filtration unit', frame='1', frame_pos={"x": 45+300, "y": 695}, img_active=ICON_GREEN_BIG, img_inactive=ICON_RED_BIG, description='', help_img='', size=12)
        app.add(sig_name='COOLING_ON', type='cooling switch on', symbol='O_CoolCircuit_2_on', location='filtration unit', frame='1', frame_pos={
                "x": 95+300, "y": 695}, img_active=ICON_GREEN_BIG, img_inactive=ICON_RED_BIG, description='', help_img='', size=12)
        app.add(sig_name='FILTER_OK', type='filter ok state', symbol='I_coolant_M07_1_water_filter_OK', location='filtration unit', frame='1',
                frame_pos={"x": 95+300, "y": 695+25}, img_active=ICON_GREEN_BIG, img_inactive=ICON_RED_BIG, description='', help_img='', size=12)
        #app.add(sig_name='M371', type='M func, set pressure', symbol='MG_M371_act_pressure_1', location='filtration unit', frame='1', frame_pos={"x": 95+300+40, "y": 695+20}, img_active=ICON_GREEN_BIG, img_inactive=ICON_RED_BIG, description='', help_img='', size=12)
        #app.add(sig_name='M372', type='M func, set pressure', symbol='MG_M372_act_pressure_2', location='filtration unit', frame='1', frame_pos={"x": 95+300+40, "y": 695+40}, img_active=ICON_GREEN_BIG, img_inactive=ICON_RED_BIG, description='', help_img='', size=12)
        #app.add(sig_name='M373', type='M func, set pressure', symbol='MG_M373_act_pressure_3', location='filtration unit', frame='1', frame_pos={"x": 95+300+40, "y": 695+60}, img_active=ICON_GREEN_BIG, img_inactive=ICON_RED_BIG, description='', help_img='', size=12)
        #app.add(sig_name='M374', type='M func, set pressure', symbol='MG_M374_act_pressure_4', location='filtration unit', frame='1', frame_pos={"x": 95+300+40, "y": 695+80}, img_active=ICON_GREEN_BIG, img_inactive=ICON_RED_BIG, description='', help_img='', size=12)

    # Pumps:
    app.add(sig_name='M4', type='water pump', symbol='O_chip_clear_pump_on', location='tank', frame='1', frame_pos={
            "x": 820, "y": 70+25}, img_active=ICON_GREEN_BIG, img_inactive=ICON_RED_BIG, description='', help_img='', size=14)

    # external input pressure
    app.add(sig_name='SP10', type='air pressure sensor', symbol='I_pneumatic_pressure_ok', location='pneumatic', frame='1', frame_pos={
            "x": 30, "y": 255+45}, img_active=ICON_GREEN_BIG, img_inactive=ICON_RED_BIG, description='', help_img='sp51_52.jpg', size=12)

    # Chip conveyor M3, SK19
    app.add(sig_name='SK19', type='running sensor', symbol='I_chip_conveyor_1_running_sensor', location='tank', frame='1', frame_pos={
            "x": 1050, "y": 160}, img_active=ICON_MOT_STATE_1, img_inactive=ICON_MOT_STATE_2, description='', help_img='sk19_m3.jpg', size=18)
    app.add(sig_name='M3', type='motor contactor', symbol='O_chip_conveyor', location='contactor box', frame='1', frame_pos={
            "x": 1065, "y": 110}, img_active=FORWARD_ON, img_inactive=FORWARD_OFF, description='', help_img='sk19_m3.jpg', size=14)
    app.add(sig_name='M3', type='motor contactor', symbol='O_chip_conveyor_back', location='contactor box', frame='1', frame_pos={
            "x": 1000, "y": 110}, img_active=BACKWARD_ON, img_inactive=BACKWARD_OFF, description='', help_img='sk19_m3.jpg', size=14)

    # spindle air valve
    app.add(sig_name='YV50', type='air valve', symbol='O_S1_air_release_valve', location='spindle', frame='1', frame_pos={
            "x": 382+45, "y": 606-115}, img_active=ICON_GREEN_BIG, img_inactive=ICON_RED_BIG, description='', help_img='', size=14)

    # Chip conveyor 2 - M31, SK26 (KM34)
    app.add(sig_name='M31', type='chip conveyor motor', symbol='O_auxiliary_chip_conveyers_ON', location='tank', frame='1', frame_pos={
            "x": 590, "y": 180+30}, img_active=ICON_GREEN_BIG, img_inactive=ICON_RED_BIG, description='', help_img='', size=14)
    app.add(sig_name='SK26', type='running sensor', symbol='I_chip_conveyor_2_running_sensor', location='tank', frame='1', frame_pos={
            "x": 590, "y": 150+30}, img_active=ICON_MOT_STATE_1, img_inactive=ICON_MOT_STATE_2, description='', help_img='', size=18)

    # Chip conveyor 3 - M32, SK27
    app.add(sig_name='M32', type='chip conveyor motor', symbol='O_auxiliary_chip_conveyers_ON', location='tank', frame='1', frame_pos={
            "x": 200, "y": 180+30}, img_active=ICON_GREEN_BIG, img_inactive=ICON_RED_BIG, description='', help_img='', size=14)
    app.add(sig_name='SK27', type='running sensor', symbol='I_chip_conveyor_3_running_sensor', location='tank', frame='1', frame_pos={
            "x": 200, "y": 150+30}, img_active=ICON_MOT_STATE_1, img_inactive=ICON_MOT_STATE_2, description='', help_img='', size=18)

    # Gearbox cooling
    app.add(sig_name='M50', type='gearbox cooling', symbol='O_Spindle_gear_cooling_on', location='cooling', frame='1', frame_pos={
            "x": 180, "y": 280}, img_active=ICON_GREEN_BIG, img_inactive=ICON_RED_BIG, description='', help_img='', size=14)

    if gifu_type in [1, 3]:
        # GIFU 1
        app.add(sig_name='M401', type='motor contactor', symbol='O_TC_arm_turn_cw', location='GIFU', frame='1', frame_pos={
                "x": 355, "y": 442}, img_active=ICON_GREEN_BIG, img_inactive=ICON_RED_BIG, description='', help_img='', size=14)

        app.add(sig_name='POCKET_IN', type='GIFU input', symbol='I_TM_1_pocket_in', location='', frame='1', frame_pos={
                "x": 175+70+45, "y": 440-70}, img_active=ICON_GREEN_BIG, img_inactive=ICON_RED_BIG, description='', help_img='', size=14)
        app.add(sig_name='POCKET_OUT', type='GIFU input', symbol='I_TM_1_pocket_out', location='', frame='1', frame_pos={
                "x": 175+70+45, "y": 440+25-70}, img_active=ICON_GREEN_BIG, img_inactive=ICON_RED_BIG, description='', help_img='', size=14)
        app.add(sig_name='YV402', type='GIFU output', symbol='O_TM_1_pocket_put_in', location='', frame='1', frame_pos={
                "x": 175+45, "y": 440-70}, img_active=ICON_GREEN_BIG, img_inactive=ICON_RED_BIG, description='', help_img='', size=14)
        app.add(sig_name='YV403', type='GIFU output', symbol='O_TM_1_pocket_put_out', location='', frame='1', frame_pos={
                "x": 175+45, "y": 440+25-70}, img_active=ICON_GREEN_BIG, img_inactive=ICON_RED_BIG, description='', help_img='', size=14)

        app.add(sig_name='ARM_BRAKE_POS', type='GIFU input', symbol='I_TC_arm_brake_pos', location='', frame='1', frame_pos={
                "x": 220, "y": 430}, img_active=ICON_GREEN_BIG, img_inactive=ICON_RED_BIG, description='', help_img='', size=14)
        app.add(sig_name='ARM_BASIC_POS', type='GIFU input', symbol='I_TC_arm_basic_pos', location='', frame='1', frame_pos={
                "x": 220, "y": 430+25}, img_active=ICON_GREEN_BIG, img_inactive=ICON_RED_BIG, description='', help_img='', size=14)
        app.add(sig_name='ARM_SPINDLE_POS', type='GIFU input', symbol='I_TC_arm_spindle_pos', location='', frame='1', frame_pos={
                "x": 220, "y": 430+50}, img_active=ICON_GREEN_BIG, img_inactive=ICON_RED_BIG, description='', help_img='', size=14)

        app.add(sig_name='TM1_COUNTER', type='GIFU input', symbol='I_TM_1_counter', location='', frame='1', frame_pos={
                "x": 220, "y": 430+85}, img_active=ICON_GREEN_BIG, img_inactive=ICON_RED_BIG, description='', help_img='', size=14)
        app.add(sig_name='TM1_REFERENCE', type='GIFU input', symbol='I_TM_1_reference', location='', frame='1', frame_pos={
                "x": 220, "y": 430+110}, img_active=ICON_GREEN_BIG, img_inactive=ICON_RED_BIG, description='', help_img='', size=14)

        app.add(sig_name='KM403', type='GIFU CW output', symbol='O_TM_1_plus', location='', frame='1', frame_pos={
                "x": 150, "y": 440}, img_active=CW_ON, img_inactive=CW_OFF, description='', help_img='', size=18)
        app.add(sig_name='KM404', type='GIFU CCW output', symbol='O_TM_1_minus', location='', frame='1', frame_pos={
                "x": 150, "y": 470}, img_active=CCW_ON, img_inactive=CCW_OFF, description='', help_img='', size=18)

    if gifu_type == 3:
        # GIFU 2
        app.add(sig_name='M401.2', type='motor contactor', symbol='O_TC_arm_2G_turn_cw', location='GIFU', frame='1', frame_pos={
                "x": 486, "y": 505}, img_active=ICON_GREEN_BIG, img_inactive=ICON_RED_BIG, description='', help_img='', size=14)

        app.add(sig_name='POCKET_IN', type='GIFU input', symbol='I_TM_2_pocket_in', location='', frame='1', frame_pos={
                "x": 500, "y": 440}, img_active=ICON_GREEN_BIG, img_inactive=ICON_RED_BIG, description='', help_img='', size=14)
        app.add(sig_name='POCKET_OUT', type='GIFU input', symbol='I_TM_2_pocket_out', location='', frame='1', frame_pos={
                "x": 500, "y": 440+25}, img_active=ICON_GREEN_BIG, img_inactive=ICON_RED_BIG, description='', help_img='', size=14)
        app.add(sig_name='YV402.2', type='GIFU output', symbol='O_TM_2_pocket_put_in', location='', frame='1', frame_pos={
                "x": 600, "y": 440}, img_active=ICON_GREEN_BIG, img_inactive=ICON_RED_BIG, description='', help_img='', size=14)
        app.add(sig_name='YV403.2', type='GIFU output', symbol='O_TM_2_pocket_put_out', location='', frame='1', frame_pos={
                "x": 600, "y": 440+25}, img_active=ICON_GREEN_BIG, img_inactive=ICON_RED_BIG, description='', help_img='', size=14)

        app.add(sig_name='ARM_BRAKE_POS', type='GIFU input', symbol='I_TC_arm_2G_brake_pos', location='', frame='1', frame_pos={
                "x": 560, "y": 560}, img_active=ICON_GREEN_BIG, img_inactive=ICON_RED_BIG, description='', help_img='', size=14)
        app.add(sig_name='ARM_BASIC_POS', type='GIFU input', symbol='I_TC_arm_2G_basic_pos', location='', frame='1', frame_pos={
                "x": 560, "y": 560+25}, img_active=ICON_GREEN_BIG, img_inactive=ICON_RED_BIG, description='', help_img='', size=14)
        app.add(sig_name='ARM_SPINDLE_POS', type='GIFU input', symbol='I_TC_arm_2G_spindle_pos', location='', frame='1', frame_pos={
                "x": 560, "y": 560+50}, img_active=ICON_GREEN_BIG, img_inactive=ICON_RED_BIG, description='', help_img='', size=14)

        app.add(sig_name='TM1_COUNTER', type='GIFU input', symbol='I_TM_2_counter', location='', frame='1', frame_pos={
                "x": 690, "y": 550}, img_active=ICON_GREEN_BIG, img_inactive=ICON_RED_BIG, description='', help_img='', size=14)
        app.add(sig_name='TM1_REFERENCE', type='GIFU input', symbol='I_TM_2_reference', location='', frame='1', frame_pos={
                "x": 690, "y": 550+25}, img_active=ICON_GREEN_BIG, img_inactive=ICON_RED_BIG, description='', help_img='', size=14)

        app.add(sig_name='KM403.2', type='GIFU CW output', symbol='O_TM_2_plus', location='', frame='1', frame_pos={
                "x": 65+620, "y": 450}, img_active=CW_ON, img_inactive=CW_OFF, description='', help_img='', size=18)
        app.add(sig_name='KM404.2', type='GIFU CCW output', symbol='O_TM_2_minus', location='', frame='1', frame_pos={
                "x": 65+620, "y": 450+30}, img_active=CCW_ON, img_inactive=CCW_OFF, description='', help_img='', size=18)

    # classic spindle sensor
    app.add(sig_name='SQ1', type='induction sensor', symbol='I_sensor_S1_clamped', location='spindle', frame='1', frame_pos={
            "x": 408+45, "y": 585-115}, img_active=ICON_GREEN_BIG, img_inactive=ICON_RED_BIG, description='', help_img='', size=14)
    app.add(sig_name='SQ2', type='induction sensor', symbol='I_sensor_S1_unclamped', location='spindle', frame='1', frame_pos={
            "x": 410-2+5+45, "y": 585-20-115}, img_active=ICON_GREEN_BIG, img_inactive=ICON_RED_BIG, description='', help_img='', size=14)
    app.add(sig_name='SQ9', type='induction sensor', symbol='I_sensor_tool_not_located_in_spindle', location='spindle', frame='1', frame_pos={
            "x": 360-2+45, "y": 585-115}, img_active=ICON_GREEN_BIG, img_inactive=ICON_RED_BIG, description='', help_img='', size=14)

    # temperature sensor
    app.add(sig_name='BT1', type='PT100 TSK-PT4A11', symbol='IW_temperature_spindle_head', location='spindle ledge', frame='1',
            frame_pos={"x": 440+25, "y": 350}, img_active=ICON_GREEN_BIG, img_inactive=ICON_RED_BIG, description='', help_img='', size=14)
    app.add(sig_name='BT2', type='PT100 TSK-PT4A11', symbol='IW_temperature_machine_Pt100', location='basis', frame='1',
            frame_pos={"x": 370, "y": 240}, img_active=ICON_GREEN_BIG, img_inactive=ICON_RED_BIG, description='', help_img='', size=14)
    app.add(sig_name='BT3', type='proximity sensor', symbol='I_S1_gear_oil_flow_ok', location='', frame='1', frame_pos={
            "x": 110+25, "y": 255+45}, img_active=ICON_GREEN_BIG, img_inactive=ICON_RED_BIG, description='', help_img='', size=12)

    app.add(sig_name='BT4', type='PT100 TSK-PT4A11', symbol='IW_temperature_spindle_Pt100', location='spindle tubus', frame='1',
            frame_pos={"x": 390-30+45, "y": 565-115}, img_active=ICON_GREEN_BIG, img_inactive=ICON_RED_BIG, description='', help_img='', size=14)
    app.add(sig_name='BT7', type='proximity sensor', symbol='I_S1_leakage_monitoring_ok', location='', frame='1', frame_pos={
            "x": 390+5+45, "y": 565-20-115}, img_active=ICON_GREEN_BIG, img_inactive=ICON_RED_BIG, description='', help_img='', size=14)

    # doors
    app.add(sig_name='LOCKED', type='door', symbol='I_guard_1_closed_locked', location='', frame='1', frame_pos={
            "x": 400, "y": 570+20}, img_active=ICON_GREEN_BIG, img_inactive=ICON_RED_BIG, description='', help_img='', size=12)
    app.add(sig_name='UNLOCK', type='door', symbol='MG_FS_guard_1_unlock', location='', frame='1', frame_pos={
            "x": 400, "y": 570+40}, img_active=ICON_GREEN_BIG, img_inactive=ICON_RED_BIG, description='', help_img='', size=12)
    app.add(sig_name='CLOSED', type='door', symbol='I_guard_1_closed', location='', frame='1', frame_pos={
            "x": 400, "y": 570}, img_active=ICON_GREEN_BIG, img_inactive=ICON_RED_BIG, description='', help_img='', size=12)


'''
##################################
  _   __                    _ __
 | | / /_ ____ _  ___ ___  (_) /__
 | |/ / // /  ' \/ -_) _ \/ /  '_/
 |___/\_, /_/_/_/\__/_//_/_/_/\_\
     /___/
##################################



# for this we will create another tab on top of the screen
'''
PAL1_IN = os.path.join('PLC:\python\picture\signal_diag', 'pal_1_in.png')
PAL1_TEXT = os.path.join('PLC:\python\picture\signal_diag', 'pal_1_text.png')
PAL2_IN = os.path.join('PLC:\python\picture\signal_diag', 'pal_2_in.png')
PAL2_TEXT = os.path.join('PLC:\python\picture\signal_diag', 'pal_2_text.png')
PAL_OUT = os.path.join('PLC:\python\picture\signal_diag', 'pal_out.png')


def switch_parent(tab, page=None, page_num=None):
    #jh.note.Show(str(page_num), 'EditScreen')

    if str(page_num) == '1':
        app.table.reparent(app.fixed_pc)
        app.fixed_pc.move(app.table, 840, 445)
    if str(page_num) == '0':
        app.table.reparent(app.fixed)
        app.fixed.move(app.table, 840, 235)


def set_pallete(value, event=None):
    end_switch_1 = int(
        jh.Get(GLOBAL_SYMBOL + 'I_PC_position_1_occupy').values()[0])
    end_switch_2 = int(
        jh.Get(GLOBAL_SYMBOL + 'I_PC_position_2_occupy').values()[0])

    if end_switch_1 and end_switch_2:
        app.img_bg_pc.set_from_file(jh.ResPath(PAL_OUT))

    if not end_switch_1 and end_switch_2:
        app.img_bg_pc.set_from_file(jh.ResPath(PAL1_IN))
    if end_switch_1 and not end_switch_2:
        app.img_bg_pc.set_from_file(jh.ResPath(PAL2_IN))

##############
# DEBUG
##############
# x802 addr 20


if jh.Get(GLOBAL_SYMBOL + 'NN_MG_pallet_change_inactive').values()[0]:

    def show_all_signals(value, event=None):
        global all_signals_spawned
        if all_signals_spawned == False and value.values()[0] == True:
            all_signals_spawned = True
            my_x_pos = mx = 50
            mx2 = 350

            # a802
            app.fixed_pc.put(bigLabel('a802 ' + 50*'-'), 20, 850)

            app.add(sig_name='O_M_PC_XYZ_in_pos_pal1', type='pc', symbol='O_M_PC_XYZ_in_pos_pal1', location='', frame='2', frame_pos={
                    "x": mx, "y": 890 + 0*vm}, img_active=ICON_GREEN_BIG, img_inactive=ICON_RED_BIG, description='', help_img='', size=14)
            app.add(sig_name='O_M_PC_XYZ_in_pos_pal2', type='pc', symbol='O_M_PC_XYZ_in_pos_pal2', location='', frame='2', frame_pos={
                    "x": mx, "y": 890 + 1*vm}, img_active=ICON_GREEN_BIG, img_inactive=ICON_RED_BIG, description='', help_img='', size=14)
            app.add(sig_name='O_M_PC_unclamped', type='pc', symbol='O_M_PC_unclamped', location='', frame='2', frame_pos={
                    "x": mx, "y": 890 + 2*vm}, img_active=ICON_GREEN_BIG, img_inactive=ICON_RED_BIG, description='', help_img='', size=14)
            app.add(sig_name='O_M_PC_clamped', type='pc', symbol='O_M_PC_clamped', location='', frame='2', frame_pos={
                    "x": mx, "y": 890 + 3*vm}, img_active=ICON_GREEN_BIG, img_inactive=ICON_RED_BIG, description='', help_img='', size=14)
            app.add(sig_name='O_M_PC_M60_active', type='pc', symbol='O_M_PC_M60_active', location='', frame='2', frame_pos={
                    "x": mx, "y": 890 + 4*vm}, img_active=ICON_GREEN_BIG, img_inactive=ICON_RED_BIG, description='', help_img='', size=14)
            app.add(sig_name='O_M_PC_M61_active', type='pc', symbol='O_M_PC_M61_active', location='', frame='2', frame_pos={
                    "x": mx, "y": 890 + 5*vm}, img_active=ICON_GREEN_BIG, img_inactive=ICON_RED_BIG, description='', help_img='', size=14)
            app.add(sig_name='O_M_PC_M62_active', type='pc', symbol='O_M_PC_M62_active', location='', frame='2', frame_pos={
                    "x": mx, "y": 890 + 6*vm}, img_active=ICON_GREEN_BIG, img_inactive=ICON_RED_BIG, description='', help_img='', size=14)
            app.add(sig_name='O_M_PC_M63_active', type='pc', symbol='O_M_PC_M63_active', location='', frame='2', frame_pos={
                    "x": mx, "y": 890 + 7*vm}, img_active=ICON_GREEN_BIG, img_inactive=ICON_RED_BIG, description='', help_img='', size=14)
            app.add(sig_name='O_M_PC_help_conditions_ok', type='pc', symbol='O_M_PC_help_conditions_ok', location='', frame='2', frame_pos={
                    "x": mx, "y": 890 + 8*vm}, img_active=ICON_GREEN_BIG, img_inactive=ICON_RED_BIG, description='', help_img='', size=14)
            app.add(sig_name='O_M_PC_alarm_active', type='pc', symbol='O_M_PC_alarm_active', location='', frame='2', frame_pos={
                    "x": mx, "y": 890 + 9*vm}, img_active=ICON_GREEN_BIG, img_inactive=ICON_RED_BIG, description='', help_img='', size=14)
            app.add(sig_name='O_M_PC_Cover_up', type='pc', symbol='O_M_PC_Cover_up', location='', frame='2', frame_pos={
                    "x": mx, "y": 890 + 10*vm}, img_active=ICON_GREEN_BIG, img_inactive=ICON_RED_BIG, description='', help_img='', size=14)
            app.add(sig_name='O_M_PC_door_closed', type='pc', symbol='O_M_PC_door_closed', location='', frame='2', frame_pos={
                    "x": mx, "y": 890 + 11*vm}, img_active=ICON_GREEN_BIG, img_inactive=ICON_RED_BIG, description='', help_img='', size=14)
            app.add(sig_name='O_M_PC_Reset', type='pc', symbol='O_M_PC_Reset', location='', frame='2', frame_pos={
                    "x": mx, "y": 890 + 12*vm}, img_active=ICON_GREEN_BIG, img_inactive=ICON_RED_BIG, description='', help_img='', size=14)
            app.add(sig_name='O_M_PC_Emergency_stop_NotActive', type='pc', symbol='O_M_PC_Emergency_stop_NotActive', location='', frame='2', frame_pos={
                    "x": mx, "y": 890 + 13*vm}, img_active=ICON_GREEN_BIG, img_inactive=ICON_RED_BIG, description='', help_img='', size=14)
            app.add(sig_name='O_M_PC_communication_OK', type='pc', symbol='O_M_PC_communication_OK', location='', frame='2', frame_pos={
                    "x": mx, "y": 890 + 14*vm}, img_active=ICON_GREEN_BIG, img_inactive=ICON_RED_BIG, description='', help_img='', size=14)
            app.add(sig_name='O_M_PC_Ax01_in_safe_position', type='pc', symbol='O_M_PC_Ax01_in_safe_position', location='', frame='2', frame_pos={
                    "x": mx, "y": 890 + 15*vm}, img_active=ICON_GREEN_BIG, img_inactive=ICON_RED_BIG, description='', help_img='', size=14)

            app.add(sig_name='I_PC_M_in_basic_position', type='pc', symbol='I_PC_M_in_basic_position', location='', frame='2', frame_pos={
                    "x": mx2, "y": 890 + 0*vm}, img_active=ICON_GREEN_BIG, img_inactive=ICON_RED_BIG, description='', help_img='', size=14)
            app.add(sig_name='I_PC_position_1_occupy', type='pc', symbol='I_PC_position_1_occupy', location='', frame='2', frame_pos={
                    "x": mx2, "y": 890 + 1*vm}, img_active=ICON_GREEN_BIG, img_inactive=ICON_RED_BIG, description='', help_img='', size=14)
            app.add(sig_name='I_PC_position_2_occupy', type='pc', symbol='I_PC_position_2_occupy', location='', frame='2', frame_pos={
                    "x": mx2, "y": 890 + 2*vm}, img_active=ICON_GREEN_BIG, img_inactive=ICON_RED_BIG, description='', help_img='', size=14)
            app.add(sig_name='I_PC_M_pal1_enabled', type='pc', symbol='I_PC_M_pal1_enabled', location='', frame='2', frame_pos={
                    "x": mx2, "y": 890 + 3*vm}, img_active=ICON_GREEN_BIG, img_inactive=ICON_RED_BIG, description='', help_img='', size=14)
            app.add(sig_name='I_PC_M_pal2_enabled', type='pc', symbol='I_PC_M_pal2_enabled', location='', frame='2', frame_pos={
                    "x": mx2, "y": 890 + 4*vm}, img_active=ICON_GREEN_BIG, img_inactive=ICON_RED_BIG, description='', help_img='', size=14)
            app.add(sig_name='I_PC_M_operation_complete', type='pc', symbol='I_PC_M_operation_complete', location='', frame='2', frame_pos={
                    "x": mx2, "y": 890 + 5*vm}, img_active=ICON_GREEN_BIG, img_inactive=ICON_RED_BIG, description='', help_img='', size=14)
            app.add(sig_name='I_PC_M_Help_active', type='pc', symbol='I_PC_M_Help_active', location='', frame='2', frame_pos={
                    "x": mx2, "y": 890 + 6*vm}, img_active=ICON_GREEN_BIG, img_inactive=ICON_RED_BIG, description='', help_img='', size=14)
            app.add(sig_name='I_PC_M_XYZ_to_pal1', type='pc', symbol='I_PC_M_XYZ_to_pal1', location='', frame='2', frame_pos={
                    "x": mx2, "y": 890 + 7*vm}, img_active=ICON_GREEN_BIG, img_inactive=ICON_RED_BIG, description='', help_img='', size=14)
            app.add(sig_name='I_PC_M_XYZ_to_pal2', type='pc', symbol='I_PC_M_XYZ_to_pal2', location='', frame='2', frame_pos={
                    "x": mx2, "y": 890 + 8*vm}, img_active=ICON_GREEN_BIG, img_inactive=ICON_RED_BIG, description='', help_img='', size=14)
            app.add(sig_name='I_PC_M_unclamp_table', type='pc', symbol='I_PC_M_unclamp_table', location='', frame='2', frame_pos={
                    "x": mx2, "y": 890 + 9*vm}, img_active=ICON_GREEN_BIG, img_inactive=ICON_RED_BIG, description='', help_img='', size=14)
            app.add(sig_name='I_PC_M_clamp_table', type='pc', symbol='I_PC_M_clamp_table', location='', frame='2', frame_pos={
                    "x": mx2, "y": 890 + 10*vm}, img_active=ICON_GREEN_BIG, img_inactive=ICON_RED_BIG, description='', help_img='', size=14)
            app.add(sig_name='I_PC_M_changer_alarm', type='pc', symbol='I_PC_M_changer_alarm', location='', frame='2', frame_pos={
                    "x": mx2, "y": 890 + 11*vm}, img_active=ICON_GREEN_BIG, img_inactive=ICON_RED_BIG, description='', help_img='', size=14)
            app.add(sig_name='I_PC_M_maintenance_mode', type='pc', symbol='I_PC_M_maintenance_mode', location='', frame='2', frame_pos={
                    "x": mx2, "y": 890 + 12*vm}, img_active=ICON_GREEN_BIG, img_inactive=ICON_RED_BIG, description='', help_img='', size=14)
            app.add(sig_name='I_PC_M_Air_blow_high_pressure_ready', type='pc', symbol='I_PC_M_Air_blow_high_pressure_ready', location='', frame='2', frame_pos={
                    "x": mx2, "y": 890 + 13*vm}, img_active=ICON_GREEN_BIG, img_inactive=ICON_RED_BIG, description='', help_img='', size=14)
            app.add(sig_name='I_PC_M_lifebit', type='pc', symbol='I_PC_M_lifebit', location='', frame='2', frame_pos={
                    "x": mx2, "y": 890 + 14*vm}, img_active=ICON_GREEN_BIG, img_inactive=ICON_RED_BIG, description='', help_img='', size=14)

            # pallete [1] O
            app.add(sig_name='O_M_PC1_cover_closed', type='pc', symbol='O_M_PC1_cover_closed', location='', frame='2', frame_pos={
                    "x": mx, "y": 890 + 17*vm}, img_active=ICON_GREEN_BIG, img_inactive=ICON_RED_BIG, description='', help_img='', size=14)
            app.add(sig_name='O_M_PC1_cover_opened', type='pc', symbol='O_M_PC1_cover_opened', location='', frame='2', frame_pos={
                    "x": mx, "y": 890 + 18*vm}, img_active=ICON_GREEN_BIG, img_inactive=ICON_RED_BIG, description='', help_img='', size=14)
            app.add(sig_name='O_M_PC1_hydro_down', type='pc', symbol='O_M_PC1_hydro_down', location='', frame='2', frame_pos={
                    "x": mx, "y": 890 + 19*vm}, img_active=ICON_GREEN_BIG, img_inactive=ICON_RED_BIG, description='', help_img='', size=14)
            app.add(sig_name='O_M_PC1_hydro_up', type='pc', symbol='O_M_PC1_hydro_up', location='', frame='2', frame_pos={
                    "x": mx, "y": 890 + 20*vm}, img_active=ICON_GREEN_BIG, img_inactive=ICON_RED_BIG, description='', help_img='', size=14)
            app.add(sig_name='O_M_PC1_elect_in', type='pc', symbol='O_M_PC1_elect_in', location='', frame='2', frame_pos={
                    "x": mx, "y": 890 + 21*vm}, img_active=ICON_GREEN_BIG, img_inactive=ICON_RED_BIG, description='', help_img='', size=14)
            app.add(sig_name='O_M_PC1_elect_out', type='pc', symbol='O_M_PC1_elect_out', location='', frame='2', frame_pos={
                    "x": mx, "y": 890 + 22*vm}, img_active=ICON_GREEN_BIG, img_inactive=ICON_RED_BIG, description='', help_img='', size=14)
            app.add(sig_name='O_M_PC1_clamping_device_active', type='pc', symbol='O_M_PC1_clamping_device_active', location='', frame='2', frame_pos={
                    "x": mx, "y": 890 + 23*vm}, img_active=ICON_GREEN_BIG, img_inactive=ICON_RED_BIG, description='', help_img='', size=14)
            app.add(sig_name='O_M_PC1_worpiece_clamped', type='pc', symbol='O_M_PC1_worpiece_clamped', location='', frame='2', frame_pos={
                    "x": mx, "y": 890 + 24*vm}, img_active=ICON_GREEN_BIG, img_inactive=ICON_RED_BIG, description='', help_img='', size=14)
            app.add(sig_name='O_M_PC1_not_check_clamping_signal', type='pc', symbol='O_M_PC1_not_check_clamping_signal', location='', frame='2', frame_pos={
                    "x": mx, "y": 890 + 25*vm}, img_active=ICON_GREEN_BIG, img_inactive=ICON_RED_BIG, description='', help_img='', size=14)

            # pallete [1] I
            app.add(sig_name='I_PC1_M_cover_close', type='pc', symbol='I_PC1_M_cover_close', location='', frame='2', frame_pos={
                    "x": mx2, "y": 890 + 17*vm}, img_active=ICON_GREEN_BIG, img_inactive=ICON_RED_BIG, description='', help_img='', size=14)
            app.add(sig_name='I_PC1_M_cover_open', type='pc', symbol='I_PC1_M_cover_open', location='', frame='2', frame_pos={
                    "x": mx2, "y": 890 + 18*vm}, img_active=ICON_GREEN_BIG, img_inactive=ICON_RED_BIG, description='', help_img='', size=14)
            app.add(sig_name='I_PC1_M_hydro_disconnect', type='pc', symbol='I_PC1_M_hydro_disconnect', location='', frame='2', frame_pos={
                    "x": mx2, "y": 890 + 19*vm}, img_active=ICON_GREEN_BIG, img_inactive=ICON_RED_BIG, description='', help_img='', size=14)
            app.add(sig_name='I_PC1_M_hydro_connect', type='pc', symbol='I_PC1_M_hydro_connect', location='', frame='2', frame_pos={
                    "x": mx2, "y": 890 + 20*vm}, img_active=ICON_GREEN_BIG, img_inactive=ICON_RED_BIG, description='', help_img='', size=14)
            app.add(sig_name='I_PC1_M_elect_disconnect', type='pc', symbol='I_PC1_M_elect_disconnect', location='', frame='2', frame_pos={
                    "x": mx2, "y": 890 + 21*vm}, img_active=ICON_GREEN_BIG, img_inactive=ICON_RED_BIG, description='', help_img='', size=14)
            app.add(sig_name='I_PC1_M_elect_connect', type='pc', symbol='I_PC1_M_elect_connect', location='', frame='2', frame_pos={
                    "x": mx2, "y": 890 + 22*vm}, img_active=ICON_GREEN_BIG, img_inactive=ICON_RED_BIG, description='', help_img='', size=14)
            app.add(sig_name='I_PC1_M_air_blow', type='pc', symbol='I_PC1_M_air_blow', location='', frame='2', frame_pos={
                    "x": mx2, "y": 890 + 23*vm}, img_active=ICON_GREEN_BIG, img_inactive=ICON_RED_BIG, description='', help_img='', size=14)
            app.add(sig_name='I_PC1_M_air_to_pallete', type='pc', symbol='I_PC1_M_air_to_pallete', location='', frame='2', frame_pos={
                    "x": mx2, "y": 890 + 24*vm}, img_active=ICON_GREEN_BIG, img_inactive=ICON_RED_BIG, description='', help_img='', size=14)

            # pallete [2] O
            app.add(sig_name='O_M_PC2_cover_closed', type='pc', symbol='O_M_PC2_cover_closed', location='', frame='2', frame_pos={
                    "x": mx, "y": 890 + 27*vm}, img_active=ICON_GREEN_BIG, img_inactive=ICON_RED_BIG, description='', help_img='', size=14)
            app.add(sig_name='O_M_PC2_cover_opened', type='pc', symbol='O_M_PC2_cover_opened', location='', frame='2', frame_pos={
                    "x": mx, "y": 890 + 28*vm}, img_active=ICON_GREEN_BIG, img_inactive=ICON_RED_BIG, description='', help_img='', size=14)
            app.add(sig_name='O_M_PC2_hydro_down', type='pc', symbol='O_M_PC2_hydro_down', location='', frame='2', frame_pos={
                    "x": mx, "y": 890 + 29*vm}, img_active=ICON_GREEN_BIG, img_inactive=ICON_RED_BIG, description='', help_img='', size=14)
            app.add(sig_name='O_M_PC2_hydro_up', type='pc', symbol='O_M_PC2_hydro_up', location='', frame='2', frame_pos={
                    "x": mx, "y": 890 + 30*vm}, img_active=ICON_GREEN_BIG, img_inactive=ICON_RED_BIG, description='', help_img='', size=14)
            app.add(sig_name='O_M_PC2_elect_in', type='pc', symbol='O_M_PC2_elect_in', location='', frame='2', frame_pos={
                    "x": mx, "y": 890 + 31*vm}, img_active=ICON_GREEN_BIG, img_inactive=ICON_RED_BIG, description='', help_img='', size=14)
            app.add(sig_name='O_M_PC2_elect_out', type='pc', symbol='O_M_PC2_elect_out', location='', frame='2', frame_pos={
                    "x": mx, "y": 890 + 32*vm}, img_active=ICON_GREEN_BIG, img_inactive=ICON_RED_BIG, description='', help_img='', size=14)
            app.add(sig_name='O_M_PC2_clamping_device_active', type='pc', symbol='O_M_PC2_clamping_device_active', location='', frame='2', frame_pos={
                    "x": mx, "y": 890 + 33*vm}, img_active=ICON_GREEN_BIG, img_inactive=ICON_RED_BIG, description='', help_img='', size=14)
            app.add(sig_name='O_M_PC2_worpiece_clamped', type='pc', symbol='O_M_PC2_worpiece_clamped', location='', frame='2', frame_pos={
                    "x": mx, "y": 890 + 34*vm}, img_active=ICON_GREEN_BIG, img_inactive=ICON_RED_BIG, description='', help_img='', size=14)
            app.add(sig_name='O_M_PC2_not_check_clamping_signal', type='pc', symbol='O_M_PC2_not_check_clamping_signal', location='', frame='2', frame_pos={
                    "x": mx, "y": 890 + 35*vm}, img_active=ICON_GREEN_BIG, img_inactive=ICON_RED_BIG, description='', help_img='', size=14)

            # pallete [2] I
            app.add(sig_name='I_PC2_M_cover_close', type='pc', symbol='I_PC2_M_cover_close', location='', frame='2', frame_pos={
                    "x": mx2, "y": 890 + 27*vm}, img_active=ICON_GREEN_BIG, img_inactive=ICON_RED_BIG, description='', help_img='', size=14)
            app.add(sig_name='I_PC2_M_cover_open', type='pc', symbol='I_PC2_M_cover_open', location='', frame='2', frame_pos={
                    "x": mx2, "y": 890 + 28*vm}, img_active=ICON_GREEN_BIG, img_inactive=ICON_RED_BIG, description='', help_img='', size=14)
            app.add(sig_name='I_PC2_M_hydro_disconnect', type='pc', symbol='I_PC2_M_hydro_disconnect', location='', frame='2', frame_pos={
                    "x": mx2, "y": 890 + 29*vm}, img_active=ICON_GREEN_BIG, img_inactive=ICON_RED_BIG, description='', help_img='', size=14)
            app.add(sig_name='I_PC2_M_hydro_connect', type='pc', symbol='I_PC2_M_hydro_connect', location='', frame='2', frame_pos={
                    "x": mx2, "y": 890 + 30*vm}, img_active=ICON_GREEN_BIG, img_inactive=ICON_RED_BIG, description='', help_img='', size=14)
            app.add(sig_name='I_PC2_M_elect_disconnect', type='pc', symbol='I_PC2_M_elect_disconnect', location='', frame='2', frame_pos={
                    "x": mx2, "y": 890 + 31*vm}, img_active=ICON_GREEN_BIG, img_inactive=ICON_RED_BIG, description='', help_img='', size=14)
            app.add(sig_name='I_PC2_M_elect_connect', type='pc', symbol='I_PC2_M_elect_connect', location='', frame='2', frame_pos={
                    "x": mx2, "y": 890 + 32*vm}, img_active=ICON_GREEN_BIG, img_inactive=ICON_RED_BIG, description='', help_img='', size=14)
            app.add(sig_name='I_PC2_M_air_blow', type='pc', symbol='I_PC2_M_air_blow', location='', frame='2', frame_pos={
                    "x": mx2, "y": 890 + 33*vm}, img_active=ICON_GREEN_BIG, img_inactive=ICON_RED_BIG, description='', help_img='', size=14)
            app.add(sig_name='I_PC2_M_air_to_pallete', type='pc', symbol='I_PC2_M_air_to_pallete', location='', frame='2', frame_pos={
                    "x": mx2, "y": 890 + 34*vm}, img_active=ICON_GREEN_BIG, img_inactive=ICON_RED_BIG, description='', help_img='', size=14)

            # x89
            app.fixed_pc.put(bigLabel('x89 ' + 50*'-'), 20, 890+37*vm)
            app.add(sig_name='O_PC_blow_clean1', type='pc', symbol='O_PC_blow_clean1', location='', frame='2', frame_pos={
                    "x": mx, "y": 890 + 39*vm}, img_active=ICON_GREEN_BIG, img_inactive=ICON_RED_BIG, description='', help_img='', size=14)
            app.add(sig_name='O_PC_air_vent_pressurizing', type='pc', symbol='O_PC_air_vent_pressurizing', location='', frame='2', frame_pos={
                    "x": mx, "y": 890 + 40*vm}, img_active=ICON_GREEN_BIG, img_inactive=ICON_RED_BIG, description='', help_img='', size=14)
            app.add(sig_name='O_PC_air_vent_bleeding', type='pc', symbol='O_PC_air_vent_bleeding', location='', frame='2', frame_pos={
                    "x": mx, "y": 890 + 41*vm}, img_active=ICON_GREEN_BIG, img_inactive=ICON_RED_BIG, description='', help_img='', size=14)
            app.add(sig_name='O_PC_high_pressure_air_blow', type='pc', symbol='O_PC_high_pressure_air_blow', location='', frame='2', frame_pos={
                    "x": mx, "y": 890 + 42*vm}, img_active=ICON_GREEN_BIG, img_inactive=ICON_RED_BIG, description='', help_img='', size=14)
            app.add(sig_name='O_Blum_laser_air_on', type='pc', symbol='O_Blum_laser_air_on', location='', frame='2', frame_pos={
                    "x": mx, "y": 890 + 43*vm}, img_active=ICON_GREEN_BIG, img_inactive=ICON_RED_BIG, description='', help_img='', size=14)
            app.add(sig_name='O_PC1_suction', type='pc', symbol='O_PC1_suction', location='', frame='2', frame_pos={
                    "x": mx, "y": 890 + 44*vm}, img_active=ICON_GREEN_BIG, img_inactive=ICON_RED_BIG, description='', help_img='', size=14)
            app.add(sig_name='O_PC2_suction', type='pc', symbol='O_PC2_suction', location='', frame='2', frame_pos={
                    "x": mx, "y": 890 + 45*vm}, img_active=ICON_GREEN_BIG, img_inactive=ICON_RED_BIG, description='', help_img='', size=14)

            # x91
            app.fixed_pc.put(bigLabel('x91 ' + 50*'-'), 20, 890+47*vm)
            app.add(sig_name='O_PC1_cover_close', type='pc', symbol='O_PC1_cover_close', location='', frame='2', frame_pos={
                    "x": mx, "y": 890 + 49*vm}, img_active=ICON_GREEN_BIG, img_inactive=ICON_RED_BIG, description='', help_img='', size=14)
            app.add(sig_name='O_PC1_cover_open', type='pc', symbol='O_PC1_cover_open', location='', frame='2', frame_pos={
                    "x": mx, "y": 890 + 50*vm}, img_active=ICON_GREEN_BIG, img_inactive=ICON_RED_BIG, description='', help_img='', size=14)
            app.add(sig_name='O_PC1_hydro_disconnect', type='pc', symbol='O_PC1_hydro_disconnect', location='', frame='2', frame_pos={
                    "x": mx, "y": 890 + 51*vm}, img_active=ICON_GREEN_BIG, img_inactive=ICON_RED_BIG, description='', help_img='', size=14)
            app.add(sig_name='O_PC1_hydro_connect', type='pc', symbol='O_PC1_hydro_connect', location='', frame='2', frame_pos={
                    "x": mx, "y": 890 + 52*vm}, img_active=ICON_GREEN_BIG, img_inactive=ICON_RED_BIG, description='', help_img='', size=14)
            app.add(sig_name='O_PC1_el_disconnect', type='pc', symbol='O_PC1_el_disconnect', location='', frame='2', frame_pos={
                    "x": mx, "y": 890 + 53*vm}, img_active=ICON_GREEN_BIG, img_inactive=ICON_RED_BIG, description='', help_img='', size=14)
            app.add(sig_name='O_PC1_el_connect', type='pc', symbol='O_PC1_el_connect', location='', frame='2', frame_pos={
                    "x": mx, "y": 890 + 54*vm}, img_active=ICON_GREEN_BIG, img_inactive=ICON_RED_BIG, description='', help_img='', size=14)
            app.add(sig_name='O_PC1_Air_blow', type='pc', symbol='O_PC1_Air_blow', location='', frame='2', frame_pos={
                    "x": mx, "y": 890 + 55*vm}, img_active=ICON_GREEN_BIG, img_inactive=ICON_RED_BIG, description='', help_img='', size=14)
            app.add(sig_name='O_PC1_air_to_pallete', type='pc', symbol='O_PC1_air_to_pallete', location='', frame='2', frame_pos={
                    "x": mx, "y": 890 + 56*vm}, img_active=ICON_GREEN_BIG, img_inactive=ICON_RED_BIG, description='', help_img='', size=14)

            app.add(sig_name='I_PC1_cover_closed', type='pc', symbol='I_PC1_cover_closed', location='', frame='2', frame_pos={
                    "x": mx2, "y": 890 + 49*vm}, img_active=ICON_GREEN_BIG, img_inactive=ICON_RED_BIG, description='', help_img='', size=14)
            app.add(sig_name='I_PC1_cover_opened', type='pc', symbol='I_PC1_cover_opened', location='', frame='2', frame_pos={
                    "x": mx2, "y": 890 + 50*vm}, img_active=ICON_GREEN_BIG, img_inactive=ICON_RED_BIG, description='', help_img='', size=14)
            app.add(sig_name='I_PC1_hydro_disconnected', type='pc', symbol='I_PC1_hydro_disconnected', location='', frame='2', frame_pos={
                    "x": mx2, "y": 890 + 51*vm}, img_active=ICON_GREEN_BIG, img_inactive=ICON_RED_BIG, description='', help_img='', size=14)
            app.add(sig_name='I_PC1_hydro_connected', type='pc', symbol='I_PC1_hydro_connected', location='', frame='2', frame_pos={
                    "x": mx2, "y": 890 + 52*vm}, img_active=ICON_GREEN_BIG, img_inactive=ICON_RED_BIG, description='', help_img='', size=14)
            app.add(sig_name='I_PC1_el_disconnected', type='pc', symbol='I_PC1_el_disconnected', location='', frame='2', frame_pos={
                    "x": mx2, "y": 890 + 53*vm}, img_active=ICON_GREEN_BIG, img_inactive=ICON_RED_BIG, description='', help_img='', size=14)
            app.add(sig_name='I_PC1_el_connected', type='pc', symbol='I_PC1_el_connected', location='', frame='2', frame_pos={
                    "x": mx2, "y": 890 + 54*vm}, img_active=ICON_GREEN_BIG, img_inactive=ICON_RED_BIG, description='', help_img='', size=14)

            # x92
            app.fixed_pc.put(bigLabel('x92 ' + 50*'-'), 20, 890+58*vm)
            app.add(sig_name='O_PC1_cover_close', type='pc', symbol='O_PC1_cover_close', location='', frame='2', frame_pos={
                    "x": mx, "y": 890 + 60*vm}, img_active=ICON_GREEN_BIG, img_inactive=ICON_RED_BIG, description='', help_img='', size=14)
            app.add(sig_name='O_PC1_cover_open', type='pc', symbol='O_PC1_cover_open', location='', frame='2', frame_pos={
                    "x": mx, "y": 890 + 61*vm}, img_active=ICON_GREEN_BIG, img_inactive=ICON_RED_BIG, description='', help_img='', size=14)
            app.add(sig_name='O_PC1_hydro_disconnect', type='pc', symbol='O_PC1_hydro_disconnect', location='', frame='2', frame_pos={
                    "x": mx, "y": 890 + 62*vm}, img_active=ICON_GREEN_BIG, img_inactive=ICON_RED_BIG, description='', help_img='', size=14)
            app.add(sig_name='O_PC1_hydro_connect', type='pc', symbol='O_PC1_hydro_connect', location='', frame='2', frame_pos={
                    "x": mx, "y": 890 + 63*vm}, img_active=ICON_GREEN_BIG, img_inactive=ICON_RED_BIG, description='', help_img='', size=14)
            app.add(sig_name='O_PC1_el_disconnect', type='pc', symbol='O_PC1_el_disconnect', location='', frame='2', frame_pos={
                    "x": mx, "y": 890 + 64*vm}, img_active=ICON_GREEN_BIG, img_inactive=ICON_RED_BIG, description='', help_img='', size=14)
            app.add(sig_name='O_PC1_el_connect', type='pc', symbol='O_PC1_el_connect', location='', frame='2', frame_pos={
                    "x": mx, "y": 890 + 65*vm}, img_active=ICON_GREEN_BIG, img_inactive=ICON_RED_BIG, description='', help_img='', size=14)
            app.add(sig_name='O_PC1_Air_blow', type='pc', symbol='O_PC1_Air_blow', location='', frame='2', frame_pos={
                    "x": mx, "y": 890 + 66*vm}, img_active=ICON_GREEN_BIG, img_inactive=ICON_RED_BIG, description='', help_img='', size=14)
            app.add(sig_name='O_PC1_air_to_pallete', type='pc', symbol='O_PC1_air_to_pallete', location='', frame='2', frame_pos={
                    "x": mx, "y": 890 + 67*vm}, img_active=ICON_GREEN_BIG, img_inactive=ICON_RED_BIG, description='', help_img='', size=14)

            app.add(sig_name='I_PC1_cover_closed', type='pc', symbol='I_PC1_cover_closed', location='', frame='2', frame_pos={
                    "x": mx2, "y": 890 + 60*vm}, img_active=ICON_GREEN_BIG, img_inactive=ICON_RED_BIG, description='', help_img='', size=14)
            app.add(sig_name='I_PC1_cover_opened', type='pc', symbol='I_PC1_cover_opened', location='', frame='2', frame_pos={
                    "x": mx2, "y": 890 + 61*vm}, img_active=ICON_GREEN_BIG, img_inactive=ICON_RED_BIG, description='', help_img='', size=14)
            app.add(sig_name='I_PC1_hydro_disconnected', type='pc', symbol='I_PC1_hydro_disconnected', location='', frame='2', frame_pos={
                    "x": mx2, "y": 890 + 62*vm}, img_active=ICON_GREEN_BIG, img_inactive=ICON_RED_BIG, description='', help_img='', size=14)
            app.add(sig_name='I_PC1_hydro_connected', type='pc', symbol='I_PC1_hydro_connected', location='', frame='2', frame_pos={
                    "x": mx2, "y": 890 + 63*vm}, img_active=ICON_GREEN_BIG, img_inactive=ICON_RED_BIG, description='', help_img='', size=14)
            app.add(sig_name='I_PC1_el_disconnected', type='pc', symbol='I_PC1_el_disconnected', location='', frame='2', frame_pos={
                    "x": mx2, "y": 890 + 64*vm}, img_active=ICON_GREEN_BIG, img_inactive=ICON_RED_BIG, description='', help_img='', size=14)
            app.add(sig_name='I_PC1_el_connected', type='pc', symbol='I_PC1_el_connected', location='', frame='2', frame_pos={
                    "x": mx2, "y": 890 + 65*vm}, img_active=ICON_GREEN_BIG, img_inactive=ICON_RED_BIG, description='', help_img='', size=14)

            app.show()
        else:
            pass
    ##############################
    # default signals starts here

    if mag_pallet_changer:
        a802_enable = False
        mag_table = False

        app.img_bg_pc = gtk.Image()
        app.img_bg_pc.set_from_file(jh.ResPath(PAL_OUT))
        app.fixed_pc = gtk.Fixed()
        app.fixed_pc.put(app.img_bg_pc, 0, 0)
        app.tabs.append_page(app.fixed_pc)
        app.tabs.set_tab_label_text(app.fixed_pc, "VYMENIK PALET")
        app.tabs.connect('switch-page', switch_parent)

        pal1_text = gtk.Image()
        pal2_text = gtk.Image()

        pal1_text.set_from_file(jh.ResPath(PAL1_TEXT))
        pal2_text.set_from_file(jh.ResPath(PAL2_TEXT))

        app.fixed_pc.put(pal1_text, 2, 280)
        app.fixed_pc.put(pal2_text, 2, 40)

        vm = vertical_margin = 20  # 25 pixels between rows

        pallet_1_occupy_handle = jh.Subscribe(
            ident=GLOBAL_SYMBOL + 'I_PC_position_1_occupy', notify=set_pallete, downTime=0.2, onChange=True)
        pallet_2_occupy_handle = jh.Subscribe(
            ident=GLOBAL_SYMBOL + 'I_PC_position_2_occupy', notify=set_pallete, downTime=0.2, onChange=True)
        all_signals_handle = jh.Subscribe(
            ident=GLOBAL_SYMBOL + 'MG_SK_OEM_machine_display', notify=show_all_signals, downTime=0.2, onChange=True)

        app.add(sig_name='SK121', type='end_switch', symbol='I_PC_position_2_occupy', location='', frame='2', frame_pos={
                "x": 180, "y": 200 + 0*vm}, img_active=ICON_GREEN_BIG, img_inactive=ICON_RED_BIG, description='', help_img='', size=14)
        app.add(sig_name='SK111', type='end_switch', symbol='I_PC_position_1_occupy', location='', frame='2', frame_pos={
                "x": 180, "y": 370 + 0*vm}, img_active=ICON_GREEN_BIG, img_inactive=ICON_RED_BIG, description='', help_img='', size=14)

        app.add(sig_name='BASIC_POS', type='basic_position', symbol='I_PC_M_in_basic_position', location='', frame='2', frame_pos={
                "x": 57, "y": 225 + 0*vm}, img_active=ICON_GREEN_BIG, img_inactive=ICON_RED_BIG, description='', help_img='', size=14)
        app.add(sig_name='LIFEBIT', type='lifebit', symbol='I_PC_M_lifebit', location='', frame='2', frame_pos={
                "x": 57, "y": 255 + 0*vm}, img_active=ICON_GREEN_BIG, img_inactive=ICON_RED_BIG, description='', help_img='', size=14)

        app.add(sig_name='O_PC1_suction', type='pc', symbol='O_PC1_suction', location='', frame='2', frame_pos={
                "x": 180, "y": 425}, img_active=ICON_GREEN_BIG, img_inactive=ICON_RED_BIG, description='', help_img='', size=14)
        app.add(sig_name='O_PC2_suction', type='pc', symbol='O_PC2_suction', location='', frame='2', frame_pos={
                "x": 180, "y": 55}, img_active=ICON_GREEN_BIG, img_inactive=ICON_RED_BIG, description='', help_img='', size=14)

        # PC STATUS
        mag_table_x = 290
        mag_table_y = 465
        app.fixed_pc.put(Dia_image(OPTION_IMAGE), mag_table_x, mag_table_y)
        app.fixed_pc.put(gtk.Label('PC STATUS'),
                         mag_table_x + 40, mag_table_y + 2)
        app.add(sig_name='MG_PC_active', type='', symbol='MG_PC_active', location='pc', frame='2', frame_pos={
                "x": mag_table_x + 20, "y": mag_table_y + 30 + 0*vm}, img_active=ICON_GREEN_BIG, img_inactive=ICON_RED_BIG, description='', help_img='', size=12)

        # magnetic board
        if mag_table:

            mag_table_x = 40
            mag_table_y = 465
            app.fixed_pc.put(Dia_image(OPTION_IMAGE), mag_table_x, mag_table_y)
            app.fixed_pc.put(gtk.Label('PC MAG BOARD 1'),
                             mag_table_x + 30, mag_table_y + 2)
            app.add(sig_name='O_mag_start_mag', type='', symbol='O_mag_start_mag', location='mag', frame='2', frame_pos={
                    "x": mag_table_x + 20, "y": mag_table_y + 30 + 0*vm}, img_active=ICON_GREEN_BIG, img_inactive=ICON_RED_BIG, description='', help_img='', size=12)
            app.add(sig_name='O_mag_start_demag', type='', symbol='O_mag_start_demag', location='mag unit', frame='2', frame_pos={
                    "x": mag_table_x + 20, "y": mag_table_y + 30 + 1*vm}, img_active=ICON_GREEN_BIG, img_inactive=ICON_RED_BIG, description='', help_img='', size=12)
            app.add(sig_name='O_mag_channel_1', type='', symbol='O_mag_channel_1', location='mag unit', frame='2', frame_pos={
                    "x": mag_table_x + 20, "y": mag_table_y + 30 + 2*vm}, img_active=ICON_GREEN_BIG, img_inactive=ICON_RED_BIG, description='', help_img='', size=12)
            app.add(sig_name='O_mag_channel_2', type='', symbol='O_mag_channel_2', location='mag unit', frame='2', frame_pos={
                    "x": mag_table_x + 20, "y": mag_table_y + 30 + 3*vm}, img_active=ICON_GREEN_BIG, img_inactive=ICON_RED_BIG, description='', help_img='', size=12)

            mag_table_x = 40
            mag_table_y = 600
            app.fixed_pc.put(Dia_image(OPTION_IMAGE), mag_table_x, mag_table_y)
            app.fixed_pc.put(gtk.Label('PC MAG BOARD 2'),
                             mag_table_x + 30, mag_table_y + 2)
            app.add(sig_name='I_mag_signal_mag_ok', type='', symbol='I_mag_signal_mag_ok', location='mag', frame='2', frame_pos={
                    "x": mag_table_x + 20, "y": mag_table_y + 30 + 0*vm}, img_active=ICON_GREEN_BIG, img_inactive=ICON_RED_BIG, description='', help_img='', size=12)
            app.add(sig_name='I_mag_signal_demag_ok', type='', symbol='I_mag_signal_demag_ok', location='mag unit', frame='2', frame_pos={
                    "x": mag_table_x + 20, "y": mag_table_y + 30 + 1*vm}, img_active=ICON_GREEN_BIG, img_inactive=ICON_RED_BIG, description='', help_img='', size=12)
            app.add(sig_name='I_mag_alarm_channel', type='', symbol='I_mag_alarm_channel', location='mag unit', frame='2', frame_pos={
                    "x": mag_table_x + 20, "y": mag_table_y + 30 + 2*vm}, img_active=ICON_GREEN_BIG, img_inactive=ICON_RED_BIG, description='', help_img='', size=12)
            app.add(sig_name='I_mag_board_connected', type='', symbol='I_mag_board_connected', location='mag unit', frame='2', frame_pos={
                    "x": mag_table_x + 20, "y": mag_table_y + 30 + 3*vm}, img_active=ICON_GREEN_BIG, img_inactive=ICON_RED_BIG, description='', help_img='', size=12)
            app.add(sig_name='I_wpiece_on_mag_board_clamped', type='', symbol='I_wpiece_on_mag_board_clamped', location='mag unit', frame='2', frame_pos={
                    "x": mag_table_x + 20, "y": mag_table_y + 30 + 4*vm}, img_active=ICON_GREEN_BIG, img_inactive=ICON_RED_BIG, description='', help_img='', size=12)

        # x89 addr 25 (stroj)
        app.add(sig_name='O_M_PC_XYZ_in_pos_pal2', type='pc', symbol='O_M_PC_XYZ_in_pos_pal2', location='', frame='2', frame_pos={
                "x": 700, "y": 90 + 0*vm}, img_active=ICON_GREEN_BIG, img_inactive=ICON_RED_BIG, description='', help_img='', size=14)
        app.add(sig_name='O_M_PC_XYZ_in_pos_pal1', type='pc', symbol='O_M_PC_XYZ_in_pos_pal1', location='', frame='2', frame_pos={
                "x": 700, "y": 385 + 0*vm}, img_active=ICON_GREEN_BIG, img_inactive=ICON_RED_BIG, description='', help_img='', size=14)

        app.add(sig_name='CLAMPED', type='pc', symbol='I_pallet_in_machine_clamped', location='', frame='2', frame_pos={
                "x": 720, "y": 190 + 0*vm-40}, img_active=ICON_GREEN_BIG, img_inactive=ICON_RED_BIG, description='', help_img='', size=14)
        app.add(sig_name='UNCLAMPED', type='pc', symbol='I_pallet_in_machine_unclamped', location='', frame='2', frame_pos={
                "x": 720, "y": 190 + 1*vm-40}, img_active=ICON_GREEN_BIG, img_inactive=ICON_RED_BIG, description='', help_img='', size=14)

        app.add(sig_name='O_PC_air_vent_pressurizing', type='pc', symbol='O_PC_air_vent_pressurizing', location='', frame='2', frame_pos={
                "x": 520, "y": 20 + 0*vm}, img_active=ICON_GREEN_BIG, img_inactive=ICON_RED_BIG, description='', help_img='', size=14)
        app.add(sig_name='O_PC_air_vent_bleeding', type='pc', symbol='O_PC_air_vent_bleeding', location='', frame='2', frame_pos={
                "x": 520, "y": 20 + 1*vm}, img_active=ICON_GREEN_BIG, img_inactive=ICON_RED_BIG, description='', help_img='', size=14)

        app.add(sig_name='O_mag_channel_1', type='pc', symbol='O_mag_channel_1', location='', frame='2', frame_pos={
                "x": 820, "y": 190 + 0*vm-40}, img_active=ICON_GREEN_BIG, img_inactive=ICON_RED_BIG, description='', help_img='', size=14)
        app.add(sig_name='I_mag_ch1_status', type='pc', symbol='I_mag_ch1_status', location='', frame='2', frame_pos={
                "x": 820, "y": 190 + 1*vm-40}, img_active=ICON_GREEN_BIG, img_inactive=ICON_RED_BIG, description='', help_img='', size=14)
        app.add(sig_name='I_mag_ch1_mag_ok', type='pc', symbol='I_mag_ch1_mag_ok', location='', frame='2', frame_pos={
                "x": 820, "y": 190 + 2*vm-40}, img_active=ICON_GREEN_BIG, img_inactive=ICON_RED_BIG, description='', help_img='', size=14)
        #app.add(sig_name='LEFT UNMAGZE ', type='pc', symbol='MG_marker_zero', location='', frame='2', frame_pos={"x": 820, "y": 190 + 3*vm}, img_active=ICON_GREEN_BIG, img_inactive=ICON_RED_BIG, description='', help_img='', size=14)
        #app.add(sig_name='LEFT EMPTY', type='pc', symbol='MG_marker_zero', location='', frame='2', frame_pos={"x": 820, "y": 190 + 4*vm}, img_active=ICON_GREEN_BIG, img_inactive=ICON_RED_BIG, description='', help_img='', size=14)
        #app.add(sig_name='LEFT EMPTY', type='pc', symbol='MG_marker_zero', location='', frame='2', frame_pos={"x": 820, "y": 190 + 5*vm}, img_active=ICON_GREEN_BIG, img_inactive=ICON_RED_BIG, description='', help_img='', size=14)

        app.add(sig_name='O_mag_channel_2', type='pc', symbol='O_mag_channel_2', location='', frame='2', frame_pos={
                "x": 970, "y": 190 + 0*vm-40}, img_active=ICON_GREEN_BIG, img_inactive=ICON_RED_BIG, description='', help_img='', size=14)
        app.add(sig_name='I_mag_ch2_status', type='pc', symbol='I_mag_ch2_status', location='', frame='2', frame_pos={
                "x": 970, "y": 190 + 1*vm-40}, img_active=ICON_GREEN_BIG, img_inactive=ICON_RED_BIG, description='', help_img='', size=14)
        app.add(sig_name='I_mag_ch2_mag_ok', type='pc', symbol='I_mag_ch2_mag_ok', location='', frame='2', frame_pos={
                "x": 970, "y": 190 + 2*vm-40}, img_active=ICON_GREEN_BIG, img_inactive=ICON_RED_BIG, description='', help_img='', size=14)
        #app.add(sig_name='RIGHT UNMAGZE ', type='pc', symbol='MG_marker_zero', location='', frame='2', frame_pos={"x": 970, "y": 190 + 3*vm}, img_active=ICON_GREEN_BIG, img_inactive=ICON_RED_BIG, description='', help_img='', size=14)
        #app.add(sig_name='RIGHT EMPTY', type='pc', symbol='MG_marker_zero', location='', frame='2', frame_pos={"x": 970, "y": 190 + 4*vm}, img_active=ICON_GREEN_BIG, img_inactive=ICON_RED_BIG, description='', help_img='', size=14)
        #app.add(sig_name='RIGHT EMPTY', type='pc', symbol='MG_marker_zero', location='', frame='2', frame_pos={"x": 970, "y": 190 + 5*vm}, img_active=ICON_GREEN_BIG, img_inactive=ICON_RED_BIG, description='', help_img='', size=14)
        app.add(sig_name='O_mag_start_mag', type='pc', symbol='O_mag_start_mag', location='', frame='2', frame_pos={
                "x": 895, "y": 190 + 3*vm-40}, img_active=ICON_GREEN_BIG, img_inactive=ICON_RED_BIG, description='', help_img='', size=14)
        app.add(sig_name='O_mag_start_demag', type='pc', symbol='O_mag_start_demag', location='', frame='2', frame_pos={
                "x": 895, "y": 190 + 4*vm-40}, img_active=ICON_GREEN_BIG, img_inactive=ICON_RED_BIG, description='', help_img='', size=14)
        app.add(sig_name='I_mag_signal_demag_ok', type='pc', symbol='I_mag_signal_demag_ok', location='', frame='2', frame_pos={
                "x": 895, "y": 190 + 5*vm-40}, img_active=ICON_GREEN_BIG, img_inactive=ICON_RED_BIG, description='', help_img='', size=14)
        app.add(sig_name='I_mag_signal_mag_ok', type='pc', symbol='I_mag_signal_mag_ok', location='', frame='2', frame_pos={
                "x": 895, "y": 190 + 6*vm-40}, img_active=ICON_GREEN_BIG, img_inactive=ICON_RED_BIG, description='', help_img='', size=14)
        app.add(sig_name='I_mag_alarm_channel', type='pc', symbol='I_mag_alarm_channel', location='', frame='2', frame_pos={
                "x": 895, "y": 190 + 7*vm-40}, img_active=ICON_GREEN_BIG, img_inactive=ICON_RED_BIG, description='', help_img='', size=14)
        app.add(sig_name='I_mag_alarm_mag_demag', type='pc', symbol='I_mag_alarm_mag_demag', location='', frame='2', frame_pos={
                "x": 895, "y": 190 + 8*vm-40}, img_active=ICON_GREEN_BIG, img_inactive=ICON_RED_BIG, description='', help_img='', size=14)

        # (pal 1)
        #app.add(sig_name='O_PC1_cover_close', type='pc', symbol='O_PC1_cover_close', location='', frame='2', frame_pos={"x": 240, "y": 255 + 0*vm}, img_active=ICON_GREEN_BIG, img_inactive=ICON_RED_BIG, description='', help_img='', size=14)
        #app.add(sig_name='O_PC1_cover_open', type='pc', symbol='O_PC1_cover_open', location='', frame='2', frame_pos={"x": 240, "y": 255 + 1*vm}, img_active=ICON_GREEN_BIG, img_inactive=ICON_RED_BIG, description='', help_img='', size=14)
        #app.add(sig_name='O_PC1_hydro_disconnect', type='pc', symbol='O_PC1_hydro_disconnect', location='', frame='2', frame_pos={"x": 240, "y": 255 + 2*vm}, img_active=ICON_GREEN_BIG, img_inactive=ICON_RED_BIG, description='', help_img='', size=14)
        #app.add(sig_name='O_PC1_hydro_connect', type='pc', symbol='O_PC1_hydro_connect', location='', frame='2', frame_pos={"x": 240, "y": 255 + 3*vm}, img_active=ICON_GREEN_BIG, img_inactive=ICON_RED_BIG, description='', help_img='', size=14)
        #app.add(sig_name='O_PC1_el_disconnect', type='pc', symbol='O_PC1_el_disconnect', location='', frame='2', frame_pos={"x": 240, "y": 255 + 4*vm}, img_active=ICON_GREEN_BIG, img_inactive=ICON_RED_BIG, description='', help_img='', size=14)
        #app.add(sig_name='O_PC1_el_connect', type='pc', symbol='O_PC1_el_connect', location='', frame='2', frame_pos={"x": 240, "y": 255 + 5*vm}, img_active=ICON_GREEN_BIG, img_inactive=ICON_RED_BIG, description='', help_img='', size=14)
        app.add(sig_name='I_PC_pal1_wpc_clamped', type='pc', symbol='I_PC_pal1_wpc_clamped', location='', frame='2', frame_pos={
                "x": 150, "y": 255 + 3*vm}, img_active=ICON_GREEN_BIG, img_inactive=ICON_RED_BIG, description='', help_img='', size=14)
        app.add(sig_name='O_PC_pal1_enable_mag_demag', type='pc', symbol='O_PC_pal1_enable_mag_demag', location='', frame='2', frame_pos={
                "x": 150, "y": 255 + 4*vm}, img_active=ICON_GREEN_BIG, img_inactive=ICON_RED_BIG, description='', help_img='', size=14)

        app.add(sig_name='I_PC1_cover_closed', type='pc', symbol='I_PC1_cover_closed', location='', frame='2', frame_pos={
                "x": 445, "y": 255 + 0*vm}, img_active=ICON_GREEN_BIG, img_inactive=ICON_RED_BIG, description='', help_img='', size=14)
        #app.add(sig_name='I_PC1_cover_opened', type='pc', symbol='I_PC1_cover_opened', location='', frame='2', frame_pos={"x": 445, "y": 255 + 1*vm}, img_active=ICON_GREEN_BIG, img_inactive=ICON_RED_BIG, description='', help_img='', size=14)
        #app.add(sig_name='I_PC1_hydro_disconnected', type='pc', symbol='I_PC1_hydro_disconnected', location='', frame='2', frame_pos={"x": 445, "y": 255 + 1*vm}, img_active=ICON_GREEN_BIG, img_inactive=ICON_RED_BIG, description='', help_img='', size=14)
        app.add(sig_name='I_PC1_hydro_connected', type='pc', symbol='I_PC1_hydro_connected', location='', frame='2', frame_pos={
                "x": 445, "y": 255 + 1*vm}, img_active=ICON_GREEN_BIG, img_inactive=ICON_RED_BIG, description='', help_img='', size=14)
        #app.add(sig_name='I_PC1_el_disconnected', type='pc', symbol='I_PC1_el_disconnected', location='', frame='2', frame_pos={"x": 445, "y": 255 + 2*vm}, img_active=ICON_GREEN_BIG, img_inactive=ICON_RED_BIG, description='', help_img='', size=14)
        app.add(sig_name='I_PC1_el_connected', type='pc', symbol='I_PC1_el_connected', location='', frame='2', frame_pos={
                "x": 445, "y": 255 + 2*vm}, img_active=ICON_GREEN_BIG, img_inactive=ICON_RED_BIG, description='', help_img='', size=14)

        # (pal 2)

        #app.add(sig_name='O_PC2_cover_close', type='pc', symbol='O_PC2_cover_close', location='', frame='2', frame_pos={"x": 240, "y": 85 + 0*vm}, img_active=ICON_GREEN_BIG, img_inactive=ICON_RED_BIG, description='', help_img='', size=14)
        #app.add(sig_name='O_PC2_cover_open', type='pc', symbol='O_PC2_cover_open', location='', frame='2', frame_pos={"x": 240, "y": 85 + 1*vm}, img_active=ICON_GREEN_BIG, img_inactive=ICON_RED_BIG, description='', help_img='', size=14)
        #app.add(sig_name='O_PC2_hydro_disconnect', type='pc', symbol='O_PC2_hydro_disconnect', location='', frame='2', frame_pos={"x": 240, "y": 85 + 2*vm}, img_active=ICON_GREEN_BIG, img_inactive=ICON_RED_BIG, description='', help_img='', size=14)
        #app.add(sig_name='O_PC2_hydro_connect', type='pc', symbol='O_PC2_hydro_connect', location='', frame='2', frame_pos={"x": 240, "y": 85 + 3*vm}, img_active=ICON_GREEN_BIG, img_inactive=ICON_RED_BIG, description='', help_img='', size=14)
        #app.add(sig_name='O_PC2_el_disconnect', type='pc', symbol='O_PC2_el_disconnect', location='', frame='2', frame_pos={"x": 240, "y": 85 + 4*vm}, img_active=ICON_GREEN_BIG, img_inactive=ICON_RED_BIG, description='', help_img='', size=14)
        #app.add(sig_name='O_PC2_el_connect', type='pc', symbol='O_PC2_el_connect', location='', frame='2', frame_pos={"x": 240, "y": 85 + 5*vm}, img_active=ICON_GREEN_BIG, img_inactive=ICON_RED_BIG, description='', help_img='', size=14)
        app.add(sig_name='I_PC_pal2_wpc_clamped', type='pc', symbol='I_PC_pal2_wpc_clamped', location='', frame='2', frame_pos={
                "x": 150, "y": 85 + 3*vm}, img_active=ICON_GREEN_BIG, img_inactive=ICON_RED_BIG, description='', help_img='', size=14)
        app.add(sig_name='O_PC_pal2_enable_mag_demag', type='pc', symbol='O_PC_pal2_enable_mag_demag', location='', frame='2', frame_pos={
                "x": 150, "y": 85 + 4*vm}, img_active=ICON_GREEN_BIG, img_inactive=ICON_RED_BIG, description='', help_img='', size=14)

        app.add(sig_name='I_PC2_cover_closed', type='pc', symbol='I_PC2_cover_closed', location='', frame='2', frame_pos={
                "x": 445, "y": 85 + 0*vm}, img_active=ICON_GREEN_BIG, img_inactive=ICON_RED_BIG, description='', help_img='', size=14)
        #app.add(sig_name='I_PC2_cover_opened', type='pc', symbol='I_PC2_cover_opened', location='', frame='2', frame_pos={"x": 445, "y": 85 + 1*vm}, img_active=ICON_GREEN_BIG, img_inactive=ICON_RED_BIG, description='', help_img='', size=14)
        #app.add(sig_name='I_PC2_hydro_disconnected', type='pc', symbol='I_PC2_hydro_disconnected', location='', frame='2', frame_pos={"x": 445, "y": 85 + 2*vm}, img_active=ICON_GREEN_BIG, img_inactive=ICON_RED_BIG, description='', help_img='', size=14)
        app.add(sig_name='I_PC2_hydro_connected', type='pc', symbol='I_PC2_hydro_connected', location='', frame='2', frame_pos={
                "x": 445, "y": 85 + 1*vm}, img_active=ICON_GREEN_BIG, img_inactive=ICON_RED_BIG, description='', help_img='', size=14)
        #app.add(sig_name='I_PC2_el_disconnected', type='pc', symbol='I_PC2_el_disconnected', location='', frame='2', frame_pos={"x": 445, "y": 85 + 4*vm}, img_active=ICON_GREEN_BIG, img_inactive=ICON_RED_BIG, description='', help_img='', size=14)
        app.add(sig_name='I_PC2_el_connected', type='pc', symbol='I_PC2_el_connected', location='', frame='2', frame_pos={
                "x": 445, "y": 85 + 2*vm}, img_active=ICON_GREEN_BIG, img_inactive=ICON_RED_BIG, description='', help_img='', size=14)


app.show()
