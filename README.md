
## Available screens

 - **Dia_signals.py** - screen for live overview of machine signals including location
 - **Simotion_write.py** - SIMOTION control parameterization screen
 - **zps_logging.py** - Long-term recording of PLC operand values without graphical interface
 - **obrazovka_test.py** - basic template for creating screens

## Installation into PLCdesign project
Most screens require a function library named `mnavratil.py` to work.

 1. Copy `mnavratil.py` into `<ProjectName>/Python/common/` 
 2. Copy all the screens you want into a `<ProjectName>/Python/masks/`
