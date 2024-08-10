# LAUDA LOOP L250 CHILLER Software

Software for controlling power, temperature and data logging via RS232 serial communication.

## Hardware setup 

The device must has to be powered on and filled with the appropriate heat exchange liquid.


## Software setup 
### Port authorizations

The port, in which the device is connected, before establishing the comunication, has to be authorized by the os for writing and reading:

- on Linux
    write a file in '/etc/udev/rules.d/' called 'chiller.rules' which contains: 

    ```
    SUBSYSTEM=="tty", ACTION=="add", ATTRS{idVendor}=="null", ATTRS{idProduct}=="null", ATTRS{serial}=="null", MODE="0666"
     ```

    in which, substitute 'null' with the information provided by typing in terminal:
    
        usb-devices  

    Be sure to know at what port the device is connected by launching the following command:

        dmesg | grep tty
    
    Reload udev rules:

        sudo udevadm control --reload-rules && sudo udevadm trigger
    
    Log out from current user or restart pc.

### Python lybraries
For correct functioning is necessary installing the Pyserial and colorama library, write in terminal:

    pip3 install serial
    pip3 install colorama

All other packages are installed by default with Python.

## Program features
The chiller is controllable via terminal by adding to the execute command multiple keys like:
    -h  message of help;
    --on    switch on the pump and heating/cooling;
    --off   switch off the pump and heating/cooling;
    -t TEMP set the temperature (substitute the temperature wanted in place of 'TEMP');
    --log LOG   set the interval of sampling in seconds;
    -q  don't show log on terminal nor save it to txt file.

If the script does not receive anything in input it displays the current temperature of the reservoir and the set temperature. If log it isn't specified, by default the program logs data every 60 second (1 minute).

With the script, it's provided a "config.json" file:

    {
    "path":"r'C:\\User\\...\\python\\log'",
    "default_rate":"60",
    "port":"'/dev/ttyUSB0'",
    "date_format":"'%d-%m-%Y %H:%M:%S'"
    }


 in which are itemized the path of the temperature logging file, the default sampling rate, the format of time logging and the PORT IN WHICH THE DEVICE IS CONNECTED: it can be changed to your needs. It's necessary to format as strings every field but the def_rate: respect the example format ("  '...'  ").
 


