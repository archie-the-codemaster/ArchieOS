import os
import datetime
import hashlib
import shutil
import json

### PATHS ###
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SYSROOT = os.path.join(BASE_DIR, "sysroot")
SYSCONF = os.path.join(SYSROOT, "sysconf")
SYSLOG = os.path.join(SYSROOT, "syslog")
SYSHOME = os.path.join(SYSROOT, "syshome")

### UTILITIES ###

def log_write(log_file, message):
    log_file.write(f"{message}\n")


def sha256(text: str) -> str:
    return hashlib.sha256(text.encode()).hexdigest()


### INSTALLER ###

def run_installer():
    print("Welcome to the OS configuration wizard.")
    choice = input("Would you like to configure the system? (y/n): ").strip().lower()

    if choice != "y":
        print("Exiting installer.")
        return

    # Check for SYSROOT
    if os.path.exists(SYSROOT):
        print("Existing installation detected.")
        action = input("Repair or reinstall? (r/i): ").strip().lower()

        if action == "r":
            # TO DO: Add repair mode
            print("Repair mode not implemented yet.")
            return

        if action == "i":
            print("Removing existing installation...")
            shutil.rmtree(SYSROOT)
        else:
            print("Invalid option. Aborting.")
            return

    # Create base structure
    print("Starting installation...")
    os.makedirs(SYSROOT, exist_ok=True)
    os.makedirs(SYSCONF, exist_ok=True)
    os.makedirs(SYSLOG, exist_ok=True)
    os.makedirs(SYSHOME, exist_ok=True)

    log_path = os.path.join(SYSLOG, "install.log")

    with open(log_path, "w") as log:
        log_write(log, f"Install started at {datetime.datetime.now()}")

        # User config
        username = input("Enter username: ").strip()
        log_write(log, "Username acquired")

        password = input("Would you like a password? (y/n): ").strip().lower()
        hashed_password = ""

        if password == "y":
            raw_pw = input("Enter password: ")
            hashed_password = sha256(raw_pw)
            del raw_pw
            log_write(log, "Password set and hashed")
        else:
            log_write(log, "No password set")

        machine_name = input("Enter machine name (lowercase recommended): ").strip()
        log_write(log, "Machine name acquired")

        # Config file
        config = {
            "rootdir": SYSROOT,
            "confdir": SYSCONF,
            "logdir": SYSLOG,
            "homedir": SYSHOME,
            "username": username,
            "password": hashed_password,
            "machine": machine_name,
        }

        config_path = os.path.join(SYSCONF, "config.json")
        with open(config_path, "w") as cfg:
            json.dump(config, cfg, indent=4)

        log_write(log, f"Config written to {config_path}")

        # Hashes used for integrity checks (TO ADD LATER)
        hashes = {
            "rootdir": sha256(SYSROOT),
            "confdir": sha256(SYSCONF),
            "logdir": sha256(SYSLOG),
            "homedir": sha256(SYSHOME),
            "username": sha256(username),
            "password": sha256(hashed_password),
            "machine": sha256(machine_name),
        }

        hash_path = os.path.join(SYSCONF, "conf_hash.json")
        with open(hash_path, "w") as hf:
            json.dump(hashes, hf, indent=4)

        log_write(log, f"Hashes written to {hash_path}")
        log_write(log, f"Install finished at {datetime.datetime.now()}")

    print("Cleaning up...")
    del choice, action, config, hashes
    print("Installation complete.")



### INTEGRITY CHECK ###
def integrity_check():
    # Defines necessary variables and paths
    integrity_status = False
    error_count = 0
    log_path = os.path.join(SYSLOG, "integrity.log")
    config_path = os.path.join(SYSCONF, "config.json")
    hashes_path = os.path.join(SYSCONF, "conf_hash.json")

    # Opens the log file 
    with open(log_path, "w") as int_log:
        log_write(int_log, f"Began integrity check at: {datetime.datetime.now()}")
        # Loads the configuration file
        with open(config_path, "r") as config_raw:
            config = json.load(config_raw)
            log_write(int_log, f"Began loading config files at: {datetime.datetime.now()}")
            syspath = config["rootdir"]
            confpath = config["confdir"]
            logpath = config["logdir"]
            homepath = config["homedir"]
            username = config["username"]
            machine_name = config["machine"]
            log_write(int_log, f"Loaded config files at: {datetime.datetime.now()}")
        # Loads the hashes file
        with open(hashes_path, "r") as hashes_raw:
            hashes = json.load(hashes_raw)
            log_write(int_log, f"Began loading hash file at: {datetime.datetime.now()}")
            syspath_hash = config["rootdir"]
            confpath_hash = config["confdir"]
            logpath_hash = config["logdir"]
            homepath_hash = config["homedir"]
            username_hash = config["username"]
            machine_name_hash = config["machine"]

        # Compares the config files to the hashed files
        if sha256(syspath) == syspath_hash: # System path
            log_write(int_log, f"Sytem path passed integrity check at {datetime.datetime.now()}")
        else:
            log_write(int_log, f"System path failed integrity check at {datetime.datetime.now()}")
            error_count += 1
        
        if sha256(confpath) == confpath_hash: # Config path
            log_write(int_log, f"Config path passed integrity check at {datetime.datetime.now()}")
        else:
            log_write(int_log, f"Config path failed integrity chek at {datetime.datetime.now()}")
            error_count += 1

        if sha256(logpath) == logpath_hash: # Log path
            log_write(int_log, f"Log path passed integrity check at {datetime.datetime.now()}")
        else:
            log_write(int_log, f"Log path failed integrity check at {datetime.datetime.now()}")
            error_count += 1

        if sha256(homepath) == homepath_hash: # Home path
            log_write(int_log, f"Home path passed integrity check at {datetime.datetime.now()}")
        else: 
            log_write(int_log, f"Home path failed integrity check at {datetime.datetime.now()}")
            error_count += 1

        if sha256(username) == username_hash: # Username
            log_write(int_log, f"Username passed integrity check at {datetime.datetime.now()}")
        else:
            log_write(int_log, f"Username failed integrity check at {datetime.datetime.now()}")
            error_count += 1

        if sha256(machine_name) == machine_name_hash: # Machine name
            log_write(int_log, f"Machine name passed integrity check at {datetime.datetime.now()}")
        else: 
            log_write(int_log, f"Machine name failed integrity check at {datetime.datetime.now()}")
            error_count += 1

        # Checks error count
        if error_count == 0:
            print("Integrity check passed.")
            integrity_status == True
        else:
            print("Integrity check failed! \n Bailing out, you're on your own!")
            integrity_status == False
    
    return(integrity_status)

### BOOT SEQUENCE ###
def boot():
    # TO DO: ADD BOOT SEQUENCE
    pass


if __name__ == "__main__":

    run_installer()
