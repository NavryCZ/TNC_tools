# TNC Tools

TNC Tools is a set of screens for TNC control systems that simplify diagnostics and reduce service time


## Available screens

 - **Dia_signals.py** - screen for live overview of machine signals including location
 - **Simotion_write.py** - SIMOTION control parameterization screen
 - **zps_logging.py** - Long-term recording of PLC operand values without graphical interface
 - **obrazovka_test.py** - basic template for creating screens

## Installation into PLCdesign project
Most screens require a function library named `mnavratil.py` to work.

 1. Copy `mnavratil.py` into `<ProjectName>/Python/common/` 
 2. Copy all the screens you want into a `<ProjectName>/Python/masks/`
 3. Open definiton file, by default `<ProjectName>/Program/Definitions/MarkerByte.def` and add operands for displaying and hiding screens.
 4. Import screens into `PyMasks.py` file
 5. Compile PLC and upload into control
 6. Upload screens  files into control
 7. Restart TNC
 8. Upload `PyMasks.py` file
 9. Restart TNC

## Usage
If the files are loaded in the control, it should now be possible to display the screens by toggling the PLC value of the screen operand.


## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License
[MIT](https://choosealicense.com/licenses/mit/)
