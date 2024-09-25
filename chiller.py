
import os
import sys
import serial 
import serial.tools.list_ports
import argparse
import json
import time
import colorama
import datetime
from pathlib import Path
from colorama import init,Style,Fore,Back


p = Path(__file__).with_name('config.json')
perc = p.absolute()
with open(perc,'r') as jfile:
    json_data = jfile.read()
dictio = json.loads(json_data)

path=dictio["path"]
defr=dictio["default_rate"]
d_fmt=dictio["date_format"]
t_lim=dictio["temp_lim"]


gen = serial.Serial()
genport = '/dev/ttyUSB0'


#check comunication 
try:  
    gen.port = genport
    gen.stopbits = 1
    gen.timeout = 1
    gen.bytesize = 8
    gen.xonxoff = True
    gen.open()
    
except: 
    print('> ' + "[ERROR]: Problems with starting communication with THE CHILLER.")
    if gen.isOpen():
        gen.close()
    exinterface()
gen.flush()


init(autoreset=True)

#cOLORS
red=Fore.RED+Style.BRIGHT
green=Fore.WHITE+Style.BRIGHT+Back.GREEN
error=Fore.WHITE+Style.BRIGHT+Back.RED
ok=Fore.GREEN+Style.BRIGHT
white=Fore.WHITE+Style.BRIGHT
info=Fore.CYAN+Style.NORMAL
reset=Style.RESET_ALL
temp=Fore.YELLOW+Style.NORMAL



#==================
#  WRITING
#==================



#Function for writi ng and reading the response of the intrument
def write_cmd(cmd):
    gen.write(bytes(cmd.encode('utf-8'))+b"\r\n")
     
    lettura = gen.readline()

    if (lettura != b''): 
         lettura = lettura.decode('utf-8').replace('\r\n','')
         
         print(ok+f">   {lettura}")



#Function for checking that input temperature has ONLY ONE DECIMAL FIGURE, it accepts both comma and point and rounds up if necessary 
def check_dec(number:float):
    print('\nSetting temperature...')
    num_str = str(number) #convert in string format
    
    if '.' in num_str:
        integer_part, decimal_part = num_str.split('.')
        if len(decimal_part) == 1:
            out=number
            
        else:
            out=round(number, 1)
            print('[INFO]: Temperature has been rounded up to one decimal figure.')
            
    else:
        print(error+'[ERROR]: *TEMPERATURE FORMATTING ERROR, please insert an integer or a one decimal figure float.')
    return out    
        


#Function for powering on and off the device
def power(on=True):
    if on:
        cmd = 'START'
        write_cmd(cmd)
    else:
        cmd='STOP'    
        write_cmd(cmd)
        

#Function for controlling the temperature of coolant reservoir
def temperature(temp) :
    if isinstance(temp,float):
        
        cmd= 'OUT_SP_00_'+ str(check_dec(temp)) 
        
    else:
        print(error+'[ERROR]: **TEMPERATURE FORMATTING ERROR, please insert an integer or a one decimal figure float.')
    return cmd




#==================
#  READING
#==================


#Function for writing a reading command
def read_cmd(cmd,d_fmt):
    gen.write(bytes(cmd.encode('utf-8'))+b"\r\n")
     
    lettura = gen.readline()

    if (lettura != b''): 
         lettura = lettura.decode('utf-8').replace('\r\n','')
         lettura=str(float(lettura))    #it removes the zero in front of string

    timestamp=datetime.datetime.now().strftime(d_fmt)         #time instant when the signal returns to pc 

    return timestamp, lettura



#Function for reading the SET TEMPERATURE
def read_set_temp():
    cmd='IN_SP_00'
    a=read_cmd(cmd,d_fmt)
    return a

#Function for reading the CURRENT TEMPERATURE OF RESERVOIR
def read_inside_temp():
    cmd='IN_PV_00'
    a=read_cmd(cmd,d_fmt)
    return a
#Function for reading high limit
def read_set_temp_hi():
    cmd='IN_SP_04'
    a=read_cmd(cmd,d_fmt)
    return a
#Function for reading low limit
def read_set_temp_lo():
    cmd='IN_SP_05'
    a=read_cmd(cmd,d_fmt)
    return a


#Function for reading device status
def status():
    cmd='IN_MODE_02'
    a=read_cmd(cmd,d_fmt)
    return a









#==================
#  LOGGING
#==================

def naming(cartella):
    timestamp=datetime.datetime.now().strftime("%d%m%Y_%H%M%S")
    file_name=os.path.join(cartella,timestamp+'.txt')
    return file_name

def logging(file_name,time,t_res,t_set):
    
    with open(file_name,'a',encoding='utf-8') as fnpy:
            fnpy.write(f'{time}\t{t_res}\t{t_set}\n\r')

def sampling(arg):
        rate=arg
        print(info+f"\n\n[INFO]:"+reset+f"Sampling rate set to {rate} seconds")
        return rate





#==================
#  MAIN
#==================



if __name__=="__main__":
    
  
    parser = argparse.ArgumentParser(description="\nScript for controlling LAUDA LOOP L250 chiller.",formatter_class=argparse.RawTextHelpFormatter,epilog='\nIf no argument is inserted, the program returns the set temperature and the current reservoir temperature.\n\rIf this is the first attempt to run the program, be sure to have set the datalog file path in the "config.json" file.\n\r')
    parser.add_argument('--on',action='store_true', help="Turn device on, from standby ")
    parser.add_argument('--off',action='store_true', help="Switch the device in standby, switch pump and peltier off")
    parser.add_argument('--temperature','-t', type=float, help="Set outflow coolant temperature") 
    parser.add_argument('--log', default=defr,help="Set the sampling rate (in sec) for logging temperatures (Default: 60 sec)")
    parser.add_argument('--quiet','-q',  action='store_true', help="Do not log temperature data")
    
    args = parser.parse_args()
    

        

    if args.on:
            time_stat, stat = status()
            if stat=='1.0':
                print(f'\n{time_stat}\tTurning '+green+ 'ON'+ reset+ ' the chiller.')

                power(True)
                
            elif stat=='0.0':
              print('\n-----------------------------\n\r The device is already on.\n\r-----------------------------')
            

    if args.off:
            time_stat, stat = status()
            if stat=='1.0':
                print('\n-----------------------------\n\r The device is already off.\n\r-----------------------------')

            elif stat=='0.0':
                print(f'\n{time_stat}\tTurning '+error+ 'OFF'+ reset+ ' the chiller.')

                power(False)

    

    if args.temperature is not None:
        
        if args.temperature>=4.0 and args.temperature<=80.0:
            write_cmd(temperature(args.temperature))
            
             
        else:
            print('\n[WARNING]: The temperature must be over 4°C and below 80°C. Please readjust.\n')

    if not args.quiet:
        
        time_stat, stat = status()
        
        if stat=='0.0':
            
                
            file_name=naming(path)
            rate=sampling(args.log)

            print(temp+f"\n[TEMP]:"+reset+f"{time_set}\tThe temperature is set at {t_set}°C")
            print(temp+f"[TEMP]:"+reset+f"{time_res}\tThe current temperature of the reservoir is {t_res}°C\n")

            print(info+f"\n[INFO]:"+reset+f" {time_stat}  Logging...\n\r")
            print(white+'\t\t========= TIME ======== CURRENT TEMP ===== SET TEMP =====\r\n')

            while True:
                try:
                    
                    time_res,t_res = read_inside_temp()
                    time_set,t_set = read_set_temp()
                    logging(file_name,time_res,t_res,t_set)
                    if t_res > t_set+t_lim:
                        print(error+f'\t\t  {time_res}\t    {t_res}\t     {t_set}\n\r')
                    else:
                        print(f'\t\t  {time_res}\t    {t_res}\t     {t_set}\n\r')
                    time.sleep(int(rate))
                    
                except KeyboardInterrupt:
                    print(white+'\t\t=========================FINISH!========================\r\n')
                    time_stat, stat = status()
                    print(info+f"\n\r[INFO]:"+reset+f"{time_stat}  Interruption caused by user")
                    print(info+f"[INFO]:"+reset+f"{time_stat}  Logging concluded, data saved to {file_name}\n\r")
                    break

        else:
            exit

    
    time_res,t_res = read_inside_temp()
    time_set,t_set = read_set_temp()
    print(temp+f"\n[TEMP]:"+reset+f"{time_set}\tThe temperature is set at {t_set}°C")
    print(temp+f"[TEMP]:"+reset+f"{time_res}\tThe current temperature of the reservoir is {t_res}°C\n")

    
        
   
