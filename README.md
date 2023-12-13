# pietgenerator

Generate a Piet program (image file in PNG format) that outputs the input message.

## usage
python -m pietgenerator [message] [output_path] [options]

### positional arguments
* message: Messages output by the program.
* output_path: Output generated Piet program file path.

### options
* --help: show this help message and exit
* --start_color: Start color of generated Piet program. Default color is LIGHT_RED.
  * LIGHT_RED
  * RED
  * DARK_RED
  * LIGHT_YELLOW
  * YELLOW
  * DARK_YELLOW
  * LIGHT_GREEN
  * GREEN
  * DARK_GREEN
  * LIGHT_CYAN
  * CYAN
  * DARK_CYAN
  * LIGHT_BLUE
  * BLUE
  * DARK_BLUE
  * LIGHT_MAGENTA
  * MAGENTA
  * DARK_MAGENTA
* --end_color: End color of generated Piet program. Default color is LIGHT_GREEN.
  * LIGHT_RED
  * RED
  * DARK_RED
  * LIGHT_YELLOW
  * YELLOW
  * DARK_YELLOW
  * LIGHT_GREEN
  * GREEN
  * DARK_GREEN
  * LIGHT_CYAN
  * CYAN
  * DARK_CYAN
  * LIGHT_BLUE
  * BLUE
  * DARK_BLUE
  * LIGHT_MAGENTA
  * MAGENTA
  * DARK_MAGENTA
* --codel_size: Pixel size of Codel. Set an int value greater than 0. Default size is 10 pixels.
