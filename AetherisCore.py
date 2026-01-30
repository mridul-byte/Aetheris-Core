import os, sys, subprocess, shutil, threading, hashlib, getpass
from datetime import datetime

# Cyberpunk UI Palette
G, R, Y, C, W, B = '\033[92m', '\033[91m', '\033[93m', '\033[96m', '\033[0m', '\033[94m'

class AetherisCore:
    def __init__(self):
        self.version = "5.0.0-Security-Lock"
        self.home = os.environ.get('HOME', '/data/data/com.termux/files/home')
        self.vault = os.path.join(self.home, "vault/engines")
        self.log_file = os.path.join(self.home, "aetheris_activity.log")
        self.hash_file = os.path.join(self.home, ".aetheris_vault.hash")
        
        if not os.path.exists(self.vault):
            os.makedirs(self.vault, mode=0o755, exist_ok=True)
        
        # Enforce Authentication before anything else
        self.authenticate()
        
        self.platform = self.get_platform()
        self.mgr = "pkg" if self.platform == "android" else "sudo apt-get"
        self.write_log("AUTH", "Authorized access granted.")
        self.auto_update_tools()

    def hash_pwd(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

    def authenticate(self):
        """Security lock mechanism for unauthorized access prevention"""
        os.system('clear')
        print(f"{B}  ◢◤  {C}╔════════════════════════════════════════════╗{B}  ◥◣")
        print(f"  ◢◤  {C}║     {W}A E T H E R I S   S E C U R I T Y   L O C K{C}║{B}  ◥◣")
        print(f"  ◢◤  {C}╚════════════════════════════════════════════╝{B}  ◥◣")
        
        if not os.path.exists(self.hash_file):
            print(f"{Y}[!] INITIALIZATION: Set your Master Password now.{W}")
            new_pwd = getpass.getpass(f"{G}Create Password: {W}")
            confirm_pwd = getpass.getpass(f"{G}Confirm Password: {W}")
            
            if new_pwd == confirm_pwd and len(new_pwd) > 0:
                with open(self.hash_file, "w") as f:
                    f.write(self.hash_pwd(new_pwd))
                print(f"{G}[SUCCESS] Password set securely.{W}")
                input("\nPress Enter to continue...")
            else:
                print(f"{R}[!] Passwords do not match or are empty. Restarting...{W}")
                sys.exit()

        # Login Attempt
        with open(self.hash_file, "r") as f:
            stored_hash = f.read().strip()

        attempts = 3
        while attempts > 0:
            user_input = getpass.getpass(f"{C}Enter Security Key ({attempts} attempts left): {W}")
            if self.hash_pwd(user_input) == stored_hash:
                return True
            else:
                attempts -= 1
                print(f"{R}[!] ACCESS DENIED.{W}")
                self.write_log("SECURITY_ALERT", "Failed login attempt detected.")
        
        print(f"{R}[!!!] INTRUSION DETECTED. SHUTTING DOWN.{W}")
        sys.exit()

    def get_platform(self):
        os.system('clear')
        print(f"{C}    ___   _________________  _______  ________ ")
        print(f"   /   | / ____/_  __/ __ \\/ ____/ __ \\/  _/ ___/")
        print(f"  / /| |/ __/   / / / / / / __/ / /_/ // / \\__ \\ ")
        print(f" / ___ / /___  / / / /_/ / /___/ _, _// / ___/ / ")
        print(f"/_/  |_\\____/ /_/  \\____/_____/_/ |_/___//____/  {W}")
        print(f"\n{Y}[!] SELECT ENVIRONMENT{W}")
        print(f"[{G}1{W}] Android (Termux)  |  [{G}2{W}] Desktop (Linux)")
        choice = input(f"\n{C}Deployment Mode > {W}").strip()
        return "android" if choice == '1' else "pc"

    def write_log(self, category, message):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(self.log_file, "a") as f:
            f.write(f"[{timestamp}] [{category}] {message}\n")

    def check_storage(self, required_gb=1.5):
        _, _, free = shutil.disk_usage(self.home)
        free_gb = free / (2**30)
        if free_gb < required_gb:
            print(f"{R}[!] DISK ALERT: {free_gb:.2f}GB available.{W}")
            return False
        return True

    def deploy_metasploit(self):
        if not self.check_storage(2.0): return
        self.write_log("INSTALL", "Metasploit deployment started.")
        if self.platform == "android":
            msf_url = "https://github.com"
            self.safe_run(f"pkg install -y wget curl && wget {msf_url} -O msf_install.sh", "Downloading MSF")
            self.safe_run("chmod +x msf_install.sh && ./msf_install.sh", "Running Installer")
        else:
            self.safe_run(f"{self.mgr} install -y metasploit-framework", "MSF Linux")

    def auto_update_tools(self):
        fatrat_path = os.path.join(self.vault, "TheFatRat")
        if os.path.exists(fatrat_path):
            subprocess.run(f"cd {fatrat_path} && git pull", shell=True, capture_output=True)

    def banner(self):
        os.system('clear')
        print(f"{B}  ◢◤  {C}╔════════════════════════════════════════════╗{B}  ◥◣")
        print(f"  ◢◤  {C}║     {W}█████╗ ███████╗████████╗██╗  ██╗███████╗{C}║{B}  ◥◣")
        print(f"  ◢◤  {C}║    {W}██╔══██╗██╔════╝╚══██╔══╝██║  ██║██╔════╝{C}║{B}  ◥◣")
        print(f"  ◢◤  {C}║    {W}███████║█████╗     ██║   ███████║█████╗  {C}║{B}  ◥◣")
        print(f"  ◢◤  {C}║    {W}██╔══██║██╔══╝     ██║   ██╔══██║██╔══╝  {C}║{B}  ◥◣")
        print(f"  ◢◤  {C}║    {W}██║  ██║███████╗   ██║   ██║  ██║███████╗{C}║{B}  ◥◣")
        print(f"  ◢◤  {C}╚════════════════════════════════════════════╝{B}  ◥◣")
        print(f" {W}» Ver: {G}{self.version}{W} | Environment: {Y}{self.platform.upper()}{W} «\n")

    def safe_run(self, cmd, label):
        print(f"{B}[EXEC] {label}...{W}")
        try:
            subprocess.run(cmd, shell=True, check=True)
            self.write_log("SUCCESS", label)
        except:
            self.write_log("FAILURE", label)

    def menu(self):
        self.banner()
        print(f"[{G}01{W}] Network Recon   : Nmap Active Scan")
        print(f"[{G}02{W}] Payload Lab     : TheFatRat Menu")
        print(f"[{G}03{W}] MSF Core        : Metasploit Framework")
        print(f"[{G}04{W}] Tool Arsenal    : Deploy + Sync 100+ Tools")
        print(f"[{G}05{W}] Activity Logs   : View Secure Audit Log")
        print(f"[{R}EX{W}] DISCONNECT")

        choice = input(f"\n{C}Aetheris@{self.platform}:~$ ").strip().upper()
        if choice == '01': self.safe_run("nmap -v", "Nmap Scan")
        elif choice == '02': 
            path = f"{self.vault}/TheFatRat/fatrat"
            if os.path.exists(path): self.safe_run(f"bash {path}", "FatRat")
            else: print(f"{R}[!] Error: Run Option 04 First.{W}")
        elif choice == '03': self.deploy_metasploit()
        elif choice == '04': 
            self.safe_run(f"{self.mgr} install -y nmap sqlmap hydra git python ruby", "Arsenal")
            if not os.path.exists(os.path.join(self.vault, "TheFatRat")):
                self.safe_run(f"git clone https://github.com {os.path.join(self.vault, 'TheFatRat')}", "FatRat")
        elif choice == '05': 
            os.system(f"cat {self.log_file}")
            input(f"\n{Y}Press Enter...{W}")
        elif choice == 'EX': sys.exit()

if __name__ == "__main__":
    try:
        AetherisCore().menu()
    except KeyboardInterrupt:
        print(f"\n{Y}[*] Session closed.{W}")
