# Those who never attempt to achieve their goals shall fall towards the deepest pits of despair.  
import os
import datetime
import hashlib
import subprocess 
import shutil
import platform
import json
import time
import progressbar


# Defines the base paths of the OS
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SYSROOT = os.path.join(BASE_DIR, "sysroot")
SYSCONF = os.path.join(SYSROOT, "sysconf")
SYSLOG = os.path.join(SYSROOT, "syslog")
SYSHOME = os.path.join(SYSROOT, "syshome")

# Defines the function for calling in a progress bar whenever I need it (funky)
def progressbarsim(n):
    b = progressbar.ProgressBar(maxval=n)
    b.start()
    for i in range(n):
        time.sleep(0.05)
        b.update(i + 1) 
    b.finish()
# Defines the boot function for the OS
def os_boot():
    # Gets the current date and time
    force_reconfig = False
    crt_datetime = datetime.datetime
    # Clears the CLI
    if platform.system() == "Windows":
        subprocess.run("cls")
    else:
        subprocess.run("clear")
    # Begins boot
    print(f"System booting at: {crt_datetime}")
    print("Initializing boot drive")
    progressbarsim(100)
    # Checks for a sysroot directory and switches into it:
    if os.path.exists(SYSROOT):
        os.chdir(SYSROOT)
        with open(os.path.join(SYSLOG,"boot.log"), "w") as bootlog:
        # Checks if the config exists if not invokes the os_config function
            if os.path.exists(os.path.join(SYSCONF,"sysconfig.json")):
              bootlog.writelines("sysconf found")
              with open(os.path.join(SYSCONF, "sysconfig.json"), "r") as config:
                contents = json.load(config)
                sys_dir = contents["system_directory"]
                bootlog.writelines(f"sys_dir copied to boot at {datetime.datetime.now()}\n")
                time.sleep(0.05)
                usr_name = contents["username"]
                bootlog.writelines(f"usr_name copied to boot at {datetime.datetime.now()}\n")
                time.sleep(0.05)
                mchn_name = contents["machine_name"]
                bootlog.writelines(f"mchn_name copied to boot at {datetime.datetime.now()}\n")
                time.sleep(0.05)
                cfg_status = contents["config_status"]
                bootlog.writelines(f"cfg_status copied to boot at {datetime.datetime.now()}\n")
                time.sleep(0.05)
                log_dir = contents["log_directory"]
                bootlog.writelines(f"log_dir copied to boot at {datetime.datetime.now()}\n")
                time.sleep(0.05)
                home_dir = contents["home_directory"]
                bootlog.writelines(f"home_dir copied to boot at {datetime.datetime.now()}\n")
                time.sleep(0.05)
                sys_bin = contents["system_binaries"]
                bootlog.writelines(f"sys_bin copied to bood at {datetime.datetime.now()}\n")
                # Checks all the data by invoking
                print("Begining system integrity check")
                progressbarsim(7)
                force_reconfig=os_int_check(sys_dir,usr_name,mchn_name,cfg_status,log_dir,home_dir,sys_bin,force_reconfig)
                if force_reconfig == True:
                     bootlog.writelines(f"Boot failed due to multiple data corruptions, began reconfiguration at {datetime.datetime.now()}\n")
                     os_config()
                else:
                     bootlog.writelines(f"Boot succeded,cleaning up...")
                     progressbarsim(6)
                     # cleans up after boot
                     del sys_dir
                     del usr_name
                     del mchn_name
                     del cfg_status
                     del log_dir
                     del home_dir
                     logon()
            else:
                print("The OS configuration file does not exist, you will be prompted to configure the OS once again")
                bootlog.writelines(f"Boot failed due to the lack of the configuration file, began reconfiguration at {datetime.datetime.now()}\n")
                os_config()
    else:
            print("The main system path is missing, you will be prompted to configure the system")
            os_config()


# Defines the function to check for errors within the system config
def os_int_check(sys_dir, usr_name, mchn_name, cfg_status,log_dir,home_dir,sys_bin,force_reconfig):
   err_cntr = 0
   with open(os.path.join(SYSCONF,"hashes.json"), "r") as hashes:
    checklist = json.load(hashes)
    if cfg_status == True:
        with open(os.path.join(SYSLOG,"checklog.log"),'w') as checklog:
            if hashlib.sha256(sys_dir.encode()).hexdigest() == checklist["system_directory"]:
                print("sys_dir has passed the integrity check, moving on...")
                checklog.writelines(f"sys_dir has passed the integrity check at: {datetime.datetime.now()}\n")
            else:
                print("sys_dir has failed the integrity check, please reconfigure the OS if you encounter any issues")
                checklog.writelines(f"sys_dir has failed the integrity check at: {datetime.datetime.now()}, please verify line 1 in the configuration file located in the sysroot dir.\n")
                err_cntr += 1

            if hashlib.sha256(usr_name.encode()).hexdigest() == checklist["username"]:
                print("usr_name has passed the integrity check, moving on...")
                checklog.writelines(f"usr_name has passed the integrity check at: {datetime.datetime.now()}\n")
            else:
                print("usr_name has failed the integrity check, this might cause log-on issue, please reconfigure the OS if you encounter any issues")
                checklog.writelines(f"usr_name has failed the integrity check at: {datetime.datetime.now()}, please verify the configuration file located in the sysroot dir.\n")
                err_cntr += 1

            if hashlib.sha256(mchn_name.encode()).hexdigest() == checklist["machine_name"]:
                print(f"mchn_name has passed the integrity check at {datetime.datetime.now()}")
                checklog.writelines(f"mchn_name has passed the integrity check at: {datetime.datetime.now()}\n")
            else:
                print("mchn_name has failed the integrity check, this might cause issues, if you encounter any of them, please reconfigure the OS")
                checklog.writelines(f"mchn_name has failed the integrity check at: {datetime.datetime.now()}\n")
                err_cntr += 1
            if hashlib.sha256(log_dir.encode()).hexdigest() == checklist["log_directory"]:
                print("log_dir has passed the integrity check, moving on")
                checklog.writelines(f"log_dir has passed the integrity check at {datetime.datetime.now()}")
            else:
                print(f"log_dir has failed the system integrity check at {datetime.datetime.now()}\n")
                checklog.writelines(f"log_dir has failed the system integrity check at {datetime.datetime.now()}\n")
                err_cntr += 1
            if hashlib.sha256(home_dir.encode()).hexdigest() == checklist["home_directory"]:
                print(f"home_dir has passed the integrity check at: {datetime.datetime.now()}\n")
                checklog.writelines(f"home_dir has passed the integrity check at {datetime.datetime.now()}\n")
            else:
                print(f"home_dir has failed the integrity check, please reconfigure the OS manually")
                checklog.writelines(f"home_dir has failed the integrity check at {datetime.datetime.now()}, please verify line 7 in the config file \n")
                err_cntr += 1
            if hashlib.sha256(sys_bin.encode()).hexdigest() == checklist["system_binaries"]:
                print(f"sys_bin has passed the integrity check")
                checklog.writelines(f"sys_bin has passed the integrity check at {datetime.datetime.now()}")
            else:
                print(f"sys_bin has failed the integrity check at {datetime.datetime.now()}, if you encounter any issues please reconfigure the OS")
                checklog.writelines(f"sys_bin has failed the integrity check at {datetime.datetime.now()}")
                err_cntr += 1

            if err_cntr >= 2:
                print(f"The system check has failed, you will be prompted to reconfigure the OS")
                force_reconfig = True
            else:
                force_reconfig = False
    else:
        print(f"cfg_status is set as false, if you have configured the system, please check the file")
    return(force_reconfig)
    


# Defines the config function for the OS
def os_config():
    inpt = input("Would you like to begin the configuration, any configuration created before will be deleted Y/N: ")
    if inpt.lower() == "y":
        os.chdir(BASE_DIR)
        if os.path.exists("sysroot"):
            shutil.rmtree("sysroot")
        print("Welcome to the configuration wizard")
        # checks for sysroot and creates the sysroot directory of the system and changes into it for the config if it does not exist, if it does it just changes into it
        os.makedirs("sysroot", exist_ok= True)
        os.chdir("sysroot")
        sys_dir = "sysroot"
        # Creates the log directory 
        os.makedirs("syslog", exist_ok= True)
        log_dir = "syslog"
        # Creates the config directory
        os.makedirs("sysconf", exist_ok= True)
        conf_dir = "sysconf"
        # Creates the home directory
        os.makedirs("syshome", exist_ok= True)
        home_dir = "syshome"
        os.makedirs(os.path.join(SYSHOME, "sysbin"))
        sys_bin = os.path.join(SYSHOME, "sysbin")
        with open("syslog/config.log", "w") as conflog:
            # Gets the username
            usr_name = input("Please input a username: ")
            conflog.writelines(f"Username written to configuration file as {usr_name} at {datetime.datetime.now()}\n")
            # Asks the user if they want a password
            usr_psswd_status = input("Would you like a password for your login? (Y/N): ")
            usr_psswd_status = usr_psswd_status.lower()
            hashed_psswd = ""
            if usr_psswd_status.lower() == "y":
                usr_psswd = input("Please input a password: ")
                hashed_psswd = hashlib.sha256(usr_psswd.encode()).hexdigest()
                conflog.writelines(f"Password hashed and written as {hashed_psswd} at {datetime.datetime.now()}\n")
            elif usr_psswd_status.lower() == "n":
                conflog.writelines(f"No password has been configured\n")
                pass
            
            # Gets the machine name
            mchn_name = input("Please input a name for your machine: ")
            conflog.write(f"Machine name written to configuration file as {mchn_name} at {datetime.datetime.now()}\n")

            # Finishes the config by writing the data to a file
            cfg_status = True
            conflog.writelines(f"Configuration status has been set as {cfg_status} at {datetime.datetime.now()}")
            print("Writing files to configuration")
            progressbarsim(8)
            # Creates a file for the config
            config = {
                "system_directory": sys_dir,
                "log_directory": log_dir,
                "home_directory": home_dir,
                "system_binaries": sys_bin,
                "username": usr_name,
                "password_enabled": usr_psswd_status,
                "machine_name": mchn_name,
                "config_status": cfg_status
            }
            with open("sysconf/sysconfig.json","w") as config_file:
                json.dump(config,config_file, indent=4)
            conflog.writelines(f"Configuration has been written to the main config file at {datetime.datetime.now()}")
            # Creates a file for hashed data from the config file used in integrity checks
            print("Hashing configuration")
            progressbarsim(7)
            hashes = {
                "system_directory": hashlib.sha256(sys_dir.encode()).hexdigest(),
                "log_directory": hashlib.sha256(log_dir.encode()).hexdigest(),
                "home_directory": hashlib.sha256(home_dir.encode()).hexdigest(),
                "system_binaries": hashlib.sha256(sys_bin.encode()).hexdigest(),
                "username": hashlib.sha256(usr_name.encode()).hexdigest(),
                "machine_name": hashlib.sha256(mchn_name.encode()).hexdigest(),
                "user_password": hashed_psswd
            }
            with open("sysconf/hashes.json", "w") as hashfile:
                json.dump(hashes,hashfile, indent=4)
            conflog.writelines(f"Hashes have been written to the hash file")
        reboot()

# Defines the function responsible for logon
def logon():
    logged_on = False
    username = input("Username: ")
    password = input("Password: ")
    with open(os.path.join(SYSCONF, "hashes.json"), "r") as hashfile:
        hashes = json.load(hashfile)
    with open(os.path.join(SYSCONF, "sysconfig.json"), "r") as configfile:
        config = json.load(configfile)
    if config["password_enabled"] == "y":
        if (
            hashlib.sha256(username.encode()).hexdigest() == hashes["username"]
            and hashlib.sha256(password.encode()).hexdigest() == hashes["user_password"]
        ):
            logged_on = True
    else:
        if hashlib.sha256(username.encode()).hexdigest() == hashes["username"]:
            logged_on = True
    if logged_on:
        print(f"logged on at {datetime.datetime.now()}")
        print(f"Welcome to ArchieOS: {username}")
        main_cli(True)
    else:
        print("Login failed.")
        logon()

# Defines the function to run the main cli
def main_cli(logged_on):
    os.chdir(SYSHOME)
    print("CLI is online")
    while logged_on == True:
        usr_cmd = input()
        if usr_cmd == "edit":
            edit() 
        elif usr_cmd == "crdir":
            crdir()
        elif usr_cmd == "chdir":
            chdir()
        elif usr_cmd == "shutdown":
            shutdown()
        elif usr_cmd == "clr":
            clr()
        elif usr_cmd == "slam":
            slam_status = True
            slam(slam_status)

################################ Space reserved for core system tools #####################################
# Defines a simple text editor
def edit():
    txt_input = ""
    txt_lines = []
    file_path = input("Specify the file name: ")
    if os.path.exists(file_path) != True:
        print("The file you specified does not exist, if you pick w you will create it, but you cannot append or read it")
        file_exists = False
    else:
        pass
    modus_operandi = input("Specify what to do with the file (w,a,r): ")
    # Writes to the file
    if modus_operandi == "w":
        with open(file_path, "w") as working_file:
            print(f"To save the file type $writeout\n To delete a line type $del")
            print("######### WRITING TO FILE #########")
            while True:
                txt_input = input()
                if txt_input == "$writeout":
                    print("######### FILE SAVED #########")
                    break
                elif txt_input == "$del":
                    try:
                     line = int(input("Specify which line to delete: "))
                     if 1 <= line <= len(txt_lines):
                        del txt_lines[line - 1]  
                        print(f"Deleted line {line}")
                     else:
                        print("Invalid line number.")
                    except:
                        print("Invalid input.")
                    continue
                txt_lines.append(f"{txt_input}\n")
            working_file.writelines(txt_lines)
    # Appends to file
    elif modus_operandi == "a":        
            try:
                with open(file_path, "a") as working_file:
                    print("To save the file type $writeout")
                    print("######### APPENDING TO FILE #########")
                    while True:
                        txt_input = input()
                        if txt_input == "$writeout":
                            print("######### FILE SAVED #########")
                            break
                        txt_lines.append(txt_input + "\n")
                    working_file.writelines(txt_lines)
            except:
                print("The file does not exist, continuing")
    # Outputs file to console
    elif modus_operandi == "r":
        try:
            with open(file_path,"r") as working_file:
                print("######### READING FILE #########")
                file_content = working_file.readlines()
                for i in range(len(file_content)):
                    print(file_content[i].strip())
                    i += 1
                print("######### END OF FILE #########")
        except:
            print("File does not exist")



# Defines the create dir function
def crdir():
    cr_dir = input("Specify directory name")
    os.makedirs(cr_dir,exist_ok=True)

# Defines the change dir function
def chdir():
    ch_dir = input("Specify path: ")
    os.chdir(ch_dir)

# Defines the function to shutdown the system
def shutdown():
    log_path = os.path.join(SYSLOG,"shutdown.log")
    clr()
    print("Cleaning up system")
    progressbarsim(1)
    with open(log_path, "w") as shtd_log:
        shtd_log.write(f"Shutdown at {datetime.datetime.now()}\n")
    print("Clearing system SWAP")
    progressbarsim(10)
    print("Shutting down")
    progressbarsim(100)
    exit(0)
# Defines the function to reboot the system
def reboot():
    if platform.system() == "Windows":
        subprocess.run("cls")
    else:
        subprocess.run("clear")
    os_boot()

# defines a function to clear the cli
def clr():
    if platform.system() == "Windows":
        subprocess.run("cls")
    else:
        subprocess.run("clear")

# Declares a simple file executor
def execs():
    name = input("Executable name: ")
    file_path = os.path.join(SYSHOME, "bin", f"{name}.py")

    if os.path.exists(file_path):
        subprocess.run(["python3", file_path])
    else:
        print("Executable not found.")



# Declares a simple package manager
def slam(slam_status):
    print("Welcome to SLAM, type $help for help")
    while slam_status == True:
        slam_cmd = input()
        if slam_cmd == "$help":
            print(f"$help - prints this text \n $syncdb - syncs the database \n $inst - installs a package from the, specify the exact name \n $uninst - uninstalls a package \n $exit - exits SLAM")
        elif slam_cmd == "$syncdb":
            try:
                if os.path.exists(os.path.join(BASE_DIR, "pacdb")):
                    with open(os.path.join(BASE_DIR,"pacdb","paclist.pcl"),"r") as paclist:
                        packages = paclist.readlines()
            except:
                print("The package list does not exist!")
        elif slam_cmd == "$inst":
            if os.path.exists(os.path.join(BASE_DIR, "pacdb")):
                try:
                    with open(os.path.join(BASE_DIR,"pacdb","paclist.pcl"),"r") as paclist:
                        packages = paclist.readlines()
                    pacname = input("Input the name of the package: ")
                    if pacname.lower().strip() in packages:
                        shutil.copytree(os.path.join(BASE_DIR, "pacdb", pacname), os.path.join(SYSHOME,"sysbin"))
                except:
                    print("The package database does not exist!")
        elif slam_cmd == "$uninst":
            pass
        elif slam_cmd == "$exit":
            print("SLAM has exited without any issues")
            slam_status = False

os_boot()