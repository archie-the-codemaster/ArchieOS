# Those who never attempt to achieve their goals shall fall towards the deepest pits of despair. 
import sys 
import os
from colorama import init
from termcolor import colored
import datetime

# Defines the boot function for the OS
def os_boot():
    # Gets the current date and time
    boot_fin = False
    while boot_fin == False:
        crt_datetime = datetime.datetime.now()
    
    print(f"System booting at: {crt_datetime}")
    print("Initializing boot drive")
    # Checks for a sysroot directory and switches into it:
    if os.path.exists("sysroot") == True:
        os.chdir("sysroot")
        # Checks if the config exists if not invokes the os_config function
        if os.path.exists("config.cnfg") == True:
           config = open("config.cnfg", "r")
           contents = config.readlines()
           sys_dir = contents[0]
           usr_name = contents[1]
           usr_psswd_status = contents[2]
           if usr_psswd_status.lower == "y":
            usr_psswd = contents[3]
           else:
            pass
           mchn_name = contents[4]
           cfg_status = contents[5]
           # Checks all the data by invoking
           print("Begining system integrity check")
        else:
            print("The OS configuration file does not exist, you will be prompted to configure the OS once again")
            os_config()
# TO DO: ADD THE BOOT LOG FUNCTION


# Defines the function to check for errors within the system config
def os_int_check(sys_dir, usr_name,usr_psswd_status, mchn_name, cfg_status):
    hashes = open("hashes.chk", "r")
    syscheck_log = open("syschecklog.log", "w")
    checklist = hashes.readlines()
    if cfg_status == True:
        if hash(sys_dir) == checklist[0]:
            print(f"sys_dir matches the stored hash: {hash(sys_dir)}")
            syscheck_log.write(f"sys_dir passed check with hash {hash(sys_dir)}\n")
        else:
            print(f"sys_dir failed to match the stored hash, sys_dir hash is: {checklist[0]}, hash computed at boot is: {hash(sys_dir)}")
            syscheck_log.write(f"sys_dir failed to pass check, sys_dir hash is: {checklist[0]}, hash computed at boot is: {hash(sys_dir)}")
            
    pass # Work in progress


# Defines the config function for the OS
def os_config():
    inpt = input("Would you like to begin the configuration, any configuration created before will be deleted Y/N")
    if inpt.lower() == "y":
        print("Welcome to the configuration wizard")
        # Creates the sysroot directory of the system and changes into it for the config
        os.mkdir("sysroot")
        os.chdir("sysroot")
        sys_dir = "sysroot"

        # Gets the username
        usr_name = input("Please input a username")
        
        # Asks the user if they want a password
        usr_psswd_status = input("Would you like a password for your login? (Y/N)")
        if usr_psswd_status.lower() == "y":
            usr_psswd = input("Please input a password")
        elif usr_psswd_status.lower == "n":
            pass
        
        # Gets the machine name
        mchn_name = input("Please input a name for your machine")
        
        # Finishes the config by writing the data to a file
        cfg_status = True
        
        # Creates a file for the config
        config = open("config.cnfg", "w")
        config.writelines([sys_dir,usr_name,usr_psswd_status,usr_psswd,mchn_name,cfg_status])
        config.close()
        # Creates a file for the system hashes
        hashes = open("hashes.chk", "w")
        hashes = writelines(hash(sys_dir),[hash(usr_name),hash(usr_psswd_status),hash(usr_psswd),hash(mchn_name)])
        hashes.close()
        




