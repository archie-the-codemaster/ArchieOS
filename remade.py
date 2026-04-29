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

    print("Installation complete.")


if __name__ == "__main__":
    run_installer()
