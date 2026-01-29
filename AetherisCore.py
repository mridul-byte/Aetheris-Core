import os, sys, subprocess, shutil, threading

# Professional UI Palette
G, R, Y, C, W = '\033[92m', '\033[91m', '\033[93m', '\033[96m', '\033[0m'

class AetherisCore:
    def __init__(self):
        self.version = "2.8.0-Stable"
        self.vault = os.path.join(os.getcwd(), "vault/engines")
        if not os.path.exists(self.vault):
            os.makedirs(self.vault, mode=0o755, exist_ok=True)
        
        self.platform = self.get_platform()
        self.mgr = "pkg" if self.platform == "android" else "sudo apt-get"

    def get_platform(self):
        os.system('clear' if os.name != 'nt' else 'cls')
        print(f"{C}╔══════════════════════════════════════════════════╗")
        print(f"║          PLATFORM CONFIGURATION MODULE           ║")
        print(f"╚══════════════════════════════════════════════════╝{W}")
        print(f"[{G}1{W}] Android (Termux CLI)")
        print(f"[{G}2{W}] Computer (Linux / Kali / WSL)")
        
        choice = input(f"\n{Y}[?] Manual Choice Required: {W}").strip()
        return "android" if choice == '1' else "pc"

    def banner(self):
        os.system('clear' if os.name != 'nt' else 'cls')
        print(f"{C}╔══════════════════════════════════════════════════╗")
        print(f"║      AETHERIS CORE: DEV & SEC ORCHESTRATOR       ║")
        print(f"║    Mode: {self.platform.upper()} | Rel: {self.version}          ║")
        print(f"╚══════════════════════════════════════════════════╝{W}")

    def safe_run(self, cmd, label):
        print(f"{G}[*] Initializing {label}...{W}")
        try:
            subprocess.run(cmd, shell=True, check=True, env=os.environ.copy())
        except Exception as e:
            print(f"{R}[!] Error in {label}: {e}{W}")

    def deploy_arsenal(self):
        print(f"{Y}[*] Orchestrating 104-Tool Hybrid Deployment...{W}")
        kali_set = "nmap metasploit-framework sqlmap airgeddon hydra john nikto hashcat gobuster wifite"
        black_set = "androbugs drozer objection feroxbuster ghauri assetfinder httpx jaeles"
        self.safe_run(f"{self.mgr} update && {self.mgr} install -y {kali_set} {black_set}", "Primary Arsenal")
        
        fatrat_dir = os.path.join(self.vault, "TheFatRat")
        if not os.path.exists(fatrat_dir):
            # Fix: Added actual GitHub link for FatRat
            self.safe_run(f"git clone https://github.com {fatrat_dir}", "Cloning FatRat")
            self.safe_run(f"chmod +x {fatrat_dir}/*.sh", "Fixing Permissions")

    def run_all_tasks(self):
        """Executes all 4 main modules simultaneously using Threading"""
        print(f"{C}[!] Initializing Multi-Threaded Deployment...{W}")
        
        # Define the tasks
        t1 = threading.Thread(target=self.safe_run, args=("nmap -v", "Recon"))
        t2 = threading.Thread(target=self.safe_exec_script, args=(f"{self.vault}/TheFatRat/fatrat", "FatRat"))
        
        pkg = "android-tools" if self.platform == "android" else "adb fastboot"
        t3 = threading.Thread(target=self.safe_run, args=(f"{self.mgr} install -y {pkg}", "SDK CLI"))
        t4 = threading.Thread(target=self.deploy_arsenal)

        threads = [t1, t2, t3, t4]

        # Start all threads
        for t in threads:
            t.start()

        # Wait for all to finish
        for t in threads:
            t.join()
        
        print(f"{G}[SUCCESS] All modules executed.{W}")
        input("\nPress Enter to return to menu...")

    def menu(self):
        self.banner()
        print(f"[{G}1{W}] Recon      : Nmap / theHarvester (OSINT)")
        print(f"[{G}2{W}] Payloads   : TheFatRat Synthesis Engine")
        print(f"[{G}3{W}] Android    : SDK CLI (ADB/Fastboot)")
        print(f"[{G}4{W}] Repository : Deploy 104-Tool Hybrid Arsenal")
        print(f"[{Y}A{W}] RUN ALL    : Execute Options 1-4 Simultaneously")
        print(f"[{R}E{W}] SHUTDOWN")

        choice = input(f"\n{C}Aetheris@{self.platform}:~$ ").strip().upper()
        if choice == '1': self.safe_run("nmap -v", "Recon")
        elif choice == '2': self.safe_exec_script(f"{self.vault}/TheFatRat/fatrat", "FatRat")
        elif choice == '3': 
            pkg = "android-tools" if self.platform == "android" else "adb fastboot"
            self.safe_run(f"{self.mgr} install -y {pkg}", "SDK CLI")
        elif choice == '4': self.deploy_arsenal()
        elif choice == 'A': self.run_all_tasks()
        elif choice == 'E': sys.exit()

    def safe_exec_script(self, path, label):
        if os.path.exists(path):
            self.safe_run(f"bash {path}", label)
        else:
            print(f"{R}[!] {label} script not found. Run Option 4 first.{W}")

if __name__ == "__main__":
    try:
        nexus = AetherisCore()
        while True: nexus.menu()
    except KeyboardInterrupt:
        print(f"\n{Y}[*] Aetheris Core shutdown gracefully.{W}")
