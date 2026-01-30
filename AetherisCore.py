import os, sys, subprocess, shutil, hashlib, getpass
from datetime import datetime

# Cyberpunk UI Palette
G, R, Y, C, W, B = '\033[92m', '\033[91m', '\033[93m', '\033[96m', '\033[0m', '\033[94m'

class AetherisCore:
    def __init__(self):
        self.version = "5.1.0-Termux-Stable"
        # Termux-safe path resolution
        self.home = os.path.expanduser("~")
        self.vault = os.path.join(self.home, "vault", "engines")
        self.log_file = os.path.join(self.home, "aetheris_activity.log")
        self.hash_file = os.path.join(self.home, ".aetheris_vault.hash")
        
        # Immediate Environment Prep
        self.init_environment()
        self.authenticate()
        
        # Detect Platform & Manager
        self.platform = "android" if "com.termux" in self.home else "pc"
        self.mgr = "pkg" if self.platform == "android" else "sudo apt-get"
        
        self.write_log("INIT", f"Environment started on {self.platform}")
        self.auto_update_tools()

    def init_environment(self):
        """Ensures all Termux directories and permissions are active"""
        if not os.path.exists(self.vault):
            os.makedirs(self.vault, mode=0o755, exist_ok=True)
        
        # Check for storage access in Termux
        if "com.termux" in self.home and not os.path.exists(os.path.join(self.home, "storage")):
            print(f"{Y}[!] Initializing Storage Access...{W}")
            subprocess.run("termux-setup-storage", shell=True)

    def hash_pwd(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

    def authenticate(self):
        os.system('clear')
        print(f"{B}  ◢◤  {C}╔════════════════════════════════════════════╗{B}  ◥◣")
        print(f"  ◢◤  {C}║     {W}A E T H E R I S   S E C U R I T Y   L O C K{C}║{B}  ◥◣")
        print(f"  ◢◤  {C}╚════════════════════════════════════════════╝{B}  ◥◣")
        
        if not os.path.exists(self.hash_file):
            print(f"{Y}[!] NEW VAULT DETECTED: Set Master Password.{W}")
            new_pwd = getpass.getpass(f"{G}Create Password: {W}")
            confirm_pwd = getpass.getpass(f"{G}Confirm Password: {W}")
            
            if new_pwd == confirm_pwd and len(new_pwd) > 0:
                with open(self.hash_file, "w") as f:
                    f.write(self.hash_pwd(new_pwd))
                print(f"{G}[SUCCESS] Security Key established.{W}")
            else:
                print(f"{R}[!] Error: Passwords mismatch.{W}")
                sys.exit()

        with open(self.hash_file, "r") as f:
            stored_hash = f.read().strip()

        attempts = 3
        while attempts > 0:
            user_input = getpass.getpass(f"{C}Enter Security Key ({attempts} left): {W}")
            if self.hash_pwd(user_input) == stored_hash:
                return # Auth Success
            else:
                attempts -= 1
                print(f"{R}[!] ACCESS DENIED.{W}")
        
        print(f"{R}[!!!] SECURITY LOCKOUT TRIGGERED.{W}")
        sys.exit()

    def write_log(self, category, message):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(self.log_file, "a") as f:
            f.write(f"[{timestamp}] [{category}] {message}\n")

    def check_storage(self, required_gb=1.5):
        _, _, free = shutil.disk_usage(self.home)
        free_gb = free / (2**30)
        if free_gb < required_gb:
            print(f"{R}[!] DISK ALERT: Only {free_gb:.2f}GB free. {required_gb}GB required.{W}")
            return False
        return True

    def safe_run(self, cmd, label):
        print(f"{B}[EXEC] {label}...{W}")
        try:
            # check=True ensures script stops if a command fails
            subprocess.run(cmd, shell=True, check=True)
            self.write_log("SUCCESS", label)
        except subprocess.CalledProcessError as e:
            print(f"{R}[!] Command failed: {label}{W}")
            self.write_log("FAILURE", f"{label} (Error code: {e.returncode})")
        except KeyboardInterrupt:
            print(f"\n{Y}[*] Operation cancelled by user.{W}")

    def deploy_metasploit(self):
        if not self.check_storage(2.0): return
        if self.platform == "android":
            # Best way to install MSF on modern Termux
            self.safe_run("pkg update && pkg install -y wget curl openssh", "Pre-requisites")
            self.safe_run("source <(curl -sL https://raw.githubusercontent.com)", "MSF Auto-Installer")
        else:
            self.safe_run(f"{self.mgr} install -y metasploit-framework", "MSF PC")

    def auto_update_tools(self):
        fatrat_path = os.path.join(self.vault, "TheFatRat")
        if os.path.exists(fatrat_path):
            subprocess.run(f"git -C {fatrat_path} pull", shell=True, capture_output=True)

    def banner(self):
        os.system('clear')
        print(f"{B}  ◢◤  {C}╔════════════════════════════════════════════╗{B}  ◥◣")
        print(f"  ◢◤  {C}║     {W}█████╗ ███████╗████████╗██╗  ██╗███████╗{C}║{B}  ◥◣")
        print(f"  ◢◤  {C}║    {W}██╔══██╗██╔════╝╚══██╔══╝██║  ██║██╔════╝{C}║{B}  ◥◣")
        print(f"  ◢◤  {C}║    {W}███████║█████╗     ██║   ███████║█████╗  {C}║{B}  ◥◣")
        print(f"  ◢◤  {C}╚════════════════════════════════════════════╝{B}  ◥◣")
        print(f" {W}» Ver: {G}{self.version}{W} | Mode: {Y}{self.platform.upper()}{W} «\n")

    def menu(self):
        while True:
            self.banner()
            print(f"[{G}01{W}] Network Recon   : Nmap Scan")
            print(f"[{G}02{W}] Payload Lab     : TheFatRat")
            print(f"[{G}03{W}] MSF Core        : Metasploit")
            print(f"[{G}04{W}] Tool Arsenal    : Sync All Packages")
            print(f"[{G}05{W}] Activity Logs   : Audit Trail")
            print(f"[{R}EX{W}] DISCONNECT")

            choice = input(f"\n{C}Aetheris@{self.platform}:~$ ").strip().upper()
            
            if choice == '01': 
                target = input(f"{Y}Target IP/Host: {W}")
                self.safe_run(f"nmap -v -F {target}", "Quick Scan")
                input("\nPress Enter...")
            elif choice == '02': 
                path = os.path.join(self.vault, "TheFatRat", "fatrat")
                if os.path.exists(path): self.safe_run(f"bash {path}", "FatRat")
                else: print(f"{R}[!] Run Option 04 first.{W}"); input("Enter...")
            elif choice == '03': 
                self.deploy_metasploit()
            elif choice == '04': 
                self.safe_run(f"{self.mgr} update && {self.mgr} upgrade -y", "System Update")
                self.safe_run(f"{self.mgr} install -y nmap sqlmap hydra git python ruby bash", "Sync Arsenal")
                if not os.path.exists(os.path.join(self.vault, "TheFatRat")):
                    self.safe_run(f"git clone https://github.com {os.path.join(self.vault, 'TheFatRat')}", "Clone FatRat")
            elif choice == '05': 
                if os.path.exists(self.log_file): os.system(f"cat {self.log_file}")
                input(f"\n{Y}Press Enter...{W}")
            elif choice == 'EX': sys.exit()

if __name__ == "__main__":
    try:
        AetherisCore().menu()
    except KeyboardInterrupt:
        print(f"\n{Y}[*] Safe exit.{W}")
