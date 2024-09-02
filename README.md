# LAUDA LOOP L250 CHILLER Software (by Giovanni Maria Maiero)


Software for controlling power, temperature and data logging via RS232 serial communication.

## Hardware setup 

The device must be powered on and filled with the appropriate heat exchange liquid.


## Software setup 
### Port authorizations

The port, in which the device is connected, before establishing the communication, has to be authorized by the os for writing and reading:

- on Linux
    write a file in '/etc/udev/rules.d/' called 'chiller.rules' which contains: 

    ```
    SUBSYSTEM=="tty", ACTION=="add", ATTRS{idVendor}=="null", ATTRS{idProduct}=="null", ATTRS{serial}=="null", MODE="0666"
     ```

    in which, substitute 'null' with the information provided by typing in the terminal:
    
        usb-devices  

    Be sure to know at what port the device is connected by launching the following command:

        dmesg | grep tty
    
    Reload udev rules:

        sudo udevadm control --reload-rules && sudo udevadm trigger
    
    Log out from the current user or restart pc.

### Python libraries
For correct functioning, it is necessary to install the Pyserial and colorama libraries, so write in the terminal:

    pip3 install serial
    pip3 install colorama

All other packages are installed by default with Python.

## Program features
The chiller is controllable via the terminal by adding, to the execution command, multiple keys like:

    -h  message of help;
    --on    switch on the pump and heating/cooling;
    --off   switch off the pump and heating/cooling;
    -t TEMP set the temperature;
    --log LOG   set the interval of sampling in seconds;
    -q  don't show the log on the terminal nor save it to a txt file.

A configuration file ("config.json") is provided with the main script:

    {
    "path":"r'C:\\User\\...\\python\\log'",
    "default_rate":"60",
    "date_format":"'%d-%m-%Y %H:%M:%S'"
    }

in which are itemized the path of the log file, the default sampling rate and the format of time logging: the file can be changed to your needs. It's necessary to format as strings every field but the def_rate: respect the example format ("  '...'  ").

## How to use it
When executing the script like this

    my_pc:~/home/chiller$ python3 chiller.py

If the program does not receive any keys in input, it displays the current temperature of the reservoir and the set temperature:

    [TEMP]:'02-09-2024 16:17:59'	The temperature is set at 20.0°C
    [TEMP]:'02-09-2024 16:17:59'	The current temperature of the reservoir is 20.0°C 

WARNING: IT IS RECOMMENDED TO ALWAYS ADD NO KEYS BEFORE STARTING UP THE CHILLER, SO YOU CAN CHECK THE SET TEMPERATURE FIRST!

### Keys:
#### --on    
If it receives the "--on" key, it starts the chiller, communicates the temperatures and starts logging time and temperature in  a txt file in the folder specified in "config.json" and prints them on terminal screen. 
The phrase "turn on the chiller" means "start chilling the DUT at the selected temperature" (the chiller must be already turned on).

To terminate the logging procedure the user has to type in the command line "^C" (ctrl + c): no more logging and the chiller remains on, cooling the DUT.
To restart the log it is necessary to only execute the script without adding any keys.


#### -t
*If the "-t TEMP" key is added, the script communicates to the chiller to set the temperature to the value TEMP written after "-t". It accepts integers and decimal numbers between 4°C and 80°C. If the value is outside this range, the scripts sends an error message. The temperature cannot be set after the log has begun. It's possible to change it when it isn't logging or it is not chilling (chiller turned off).


#### --log 
*If the "--log LOG" key is added, the user can change the interval of sampling from the default value to what is specified after the key "--log". Mind that the value is intended in seconds. If "--log" isn't specified, by default the program logs data every 60 seconds (1 minute).


#### -q
*If the "-q" key is added, the log procedure doesn't start, and no log either on screen or on file occurs. It can be beneficial when the user wants to only turn the chiller on or change the temperature.


#### --off
*If the "--off" key is specified, the chiller turns off the pump and cooling/heating plate, not thermostating anymore the DUT.

###
Now you know everything, so start chilling!

