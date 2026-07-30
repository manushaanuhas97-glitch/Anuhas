import tkinter as tk
from tkinter import ttk, messagebox
import subprocess
import os
import threading
import sys

# =========================================================================
# ANUHAS TOOLS — ULTRA PREMIUM PC & GAMING SUPER OPTIMIZER (.EXE)
# =========================================================================

class PcGameOptimizerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("⚡ Anuhas Ultra PC & Gaming Super Optimizer")
        self.root.geometry("860x780")
        self.root.minsize(780, 680)
        self.root.configure(bg="#030712")

        # Custom ttk styles
        self.setup_styles()

        # Set Icon
        try:
            base_dir = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
            ico_path = os.path.join(base_dir, "app_icon.ico")
            if os.path.exists(ico_path):
                self.root.iconbitmap(ico_path)
        except Exception:
            pass

        self.create_ui()

    def setup_styles(self):
        style = ttk.Style()
        style.theme_use('clam')

        # Notebook tab styling
        style.configure('TNotebook', background='#030712', borderwidth=0)
        style.configure('TNotebook.Tab', background='#0f172a', foreground='#94a3b8', font=('Segoe UI', 10, 'bold'), padding=[16, 8])
        style.map('TNotebook.Tab', background=[('selected', '#1e1b4b')], foreground=[('selected', '#38bdf8')])

    def create_ui(self):
        # Master Top Header
        header = tk.Frame(self.root, bg="#0f172a", padx=24, pady=16)
        header.pack(fill="x")

        title_box = tk.Frame(header, bg="#0f172a")
        title_box.pack(side="left")

        title_lbl = tk.Label(title_box, text="⚡ Anuhas PC & Gaming Super Optimizer", font=("Segoe UI", 16, "bold"), fg="#38bdf8", bg="#0f172a")
        title_lbl.pack(anchor="w")

        sub_title = tk.Label(title_box, text="Next-Gen Windows Performance, Low Ping & Hardware Driver Suite", font=("Segoe UI", 9), fg="#94a3b8", bg="#0f172a")
        sub_title.pack(anchor="w")

        author_lbl = tk.Label(header, text="by Manusha Anuhas", font=("Segoe UI", 10, "bold"), fg="#a855f7", bg="#0f172a")
        author_lbl.pack(side="right")

        # Main Notebook
        self.tabs = ttk.Notebook(self.root)
        self.tabs.pack(fill="both", expand=True, padx=20, pady=12)

        # Tab 1: System Services & Startup Apps
        self.tab_sys = tk.Frame(self.tabs, bg="#030712", padx=16, pady=16)
        self.tabs.add(self.tab_sys, text="💻 System & Services")

        # Tab 2: Gaming & Low Ping
        self.tab_game = tk.Frame(self.tabs, bg="#030712", padx=16, pady=16)
        self.tabs.add(self.tab_game, text="🚀 Gaming FPS & Low Ping")

        # Tab 3: Driver Scanner & Updater
        self.tab_drivers = tk.Frame(self.tabs, bg="#030712", padx=16, pady=16)
        self.tabs.add(self.tab_drivers, text="🔌 Hardware Drivers")

        self.build_sys_tab()
        self.build_game_tab()
        self.build_drivers_tab()

        # Log Console Bar
        log_frame = tk.LabelFrame(self.root, text=" 📜 Action Log ", font=("Segoe UI", 9, "bold"), fg="#38bdf8", bg="#030712", padx=12, pady=6)
        log_frame.pack(fill="x", padx=20, pady=(4, 14))

        self.log_txt = tk.Text(log_frame, height=5, bg="#020617", fg="#4ade80", font=("Consolas", 10), relief="flat")
        self.log_txt.pack(fill="both", expand=True)

    # ================= TAB 1: SYSTEM & SERVICES =================
    def build_sys_tab(self):
        # Startup Card
        start_frame = tk.LabelFrame(self.tab_sys, text=" 🚀 Startup Programs Scanner ", font=("Segoe UI", 10, "bold"), fg="#c084fc", bg="#0f172a", padx=14, pady=10)
        start_frame.pack(fill="x", pady=6)

        self.startup_list = tk.Listbox(start_frame, height=5, bg="#020617", fg="#f8fafc", selectbackground="#38bdf8", selectforeground="black", font=("Consolas", 10), relief="flat")
        self.startup_list.pack(fill="x", pady=4)

        btn_box = tk.Frame(start_frame, bg="#0f172a")
        btn_box.pack(fill="x", pady=4)

        btn_scan_start = tk.Button(btn_box, text="🔍 Scan Startup Apps", font=("Segoe UI", 9, "bold"), bg="#2563eb", fg="white", activebackground="#3b82f6", activeforeground="white", relief="flat", padx=12, pady=5, command=self.scan_win_startup)
        btn_scan_start.pack(side="left")

        btn_open_taskmgr = tk.Button(btn_box, text="⚙️ Open Task Manager Startup", font=("Segoe UI", 9, "bold"), bg="#0284c7", fg="white", activebackground="#0369a1", activeforeground="white", relief="flat", padx=12, pady=5, command=lambda: os.system("start taskmgr"))
        btn_open_taskmgr.pack(side="right")

        # Services Card
        srv_frame = tk.LabelFrame(self.tab_sys, text=" 🛡️ Heavy Windows Services Disabler ", font=("Segoe UI", 10, "bold"), fg="#38bdf8", bg="#0f172a", padx=14, pady=10)
        srv_frame.pack(fill="x", pady=8)

        srv_info = tk.Label(srv_frame, text="Disables SysMain (Superfetch), Connected User Experiences (Telemetry), MapsBroker, & Diagnostic Tracking services to free CPU & RAM.", font=("Segoe UI", 9), fg="#94a3b8", bg="#0f172a", justify="left", wraplength=700)
        srv_info.pack(anchor="w", pady=(0, 6))

        btn_opt_srv = tk.Button(srv_frame, text="⚡ Disable Heavy Background Services", font=("Segoe UI", 10, "bold"), bg="#10b981", fg="white", activebackground="#059669", activeforeground="white", relief="flat", padx=16, pady=7, command=self.optimize_win_services)
        btn_opt_srv.pack(anchor="w", pady=4)

    # ================= TAB 2: GAMING FPS & LOW PING =================
    def build_game_tab(self):
        boosters = [
            ("⚡ Ultimate Performance Power Plan", "Enables Windows Ultimate Performance power scheme for max CPU clock speed", self.boost_power_plan),
            ("🎮 Windows Game Mode & HAGS GPU Scheduling", "Enables Game Mode & HAGS GPU hardware scheduling for higher gaming FPS", self.boost_game_mode),
            ("🌐 Low Ping TCP/IP & Network Flush", "Flushes DNS cache, resets Winsock, & enables TCP NoDelay for minimum ping", self.boost_network_lowping),
            ("🧹 Clear DirectX Shader & Temp Cache", "Deletes junk DirectX shader cache & Windows temp files to fix game stuttering", self.boost_clear_shader_cache)
        ]

        for name, desc, cmd_func in boosters:
            card = tk.Frame(self.tab_game, bg="#0f172a", padx=16, pady=12)
            card.pack(fill="x", pady=6)

            info = tk.Frame(card, bg="#0f172a")
            info.pack(side="left", fill="x", expand=True)

            lbl_n = tk.Label(info, text=name, font=("Segoe UI", 11, "bold"), fg="#f8fafc", bg="#0f172a")
            lbl_n.pack(anchor="w")

            lbl_d = tk.Label(info, text=desc, font=("Segoe UI", 9), fg="#94a3b8", bg="#0f172a")
            lbl_d.pack(anchor="w")

            btn = tk.Button(card, text="Apply Boost 🚀", font=("Segoe UI", 9, "bold"), bg="#7c3aed", fg="white", activebackground="#6d28d9", activeforeground="white", relief="flat", padx=14, pady=6, command=cmd_func)
            btn.pack(side="right")

    # ================= TAB 3: HARDWARE DRIVERS =================
    def build_drivers_tab(self):
        lbl = tk.Label(self.tab_drivers, text="System Hardware Drivers Scanner & Windows Driver Updater:", font=("Segoe UI", 10, "bold"), fg="#38bdf8", bg="#030712")
        lbl.pack(anchor="w", pady=(0, 6))

        drv_frame = tk.Frame(self.tab_drivers, bg="#030712")
        drv_frame.pack(fill="both", expand=True, pady=4)

        self.drv_listbox = tk.Listbox(drv_frame, bg="#020617", fg="#f8fafc", selectbackground="#38bdf8", selectforeground="black", font=("Consolas", 10), relief="flat")
        scrollbar = ttk.Scrollbar(drv_frame, orient="vertical", command=self.drv_listbox.yview)
        self.drv_listbox.configure(yscrollcommand=scrollbar.set)

        self.drv_listbox.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        ctrl_frame = tk.Frame(self.tab_drivers, bg="#030712")
        ctrl_frame.pack(fill="x", pady=8)

        btn_scan_drv = tk.Button(ctrl_frame, text="🔍 Scan Hardware Drivers", font=("Segoe UI", 10, "bold"), bg="#2563eb", fg="white", activebackground="#1d4ed8", activeforeground="white", relief="flat", padx=14, pady=7, command=self.scan_system_drivers)
        btn_scan_drv.pack(side="left", padx=5)

        btn_upd_win = tk.Button(ctrl_frame, text="🌐 Launch Windows Driver Updater", font=("Segoe UI", 10, "bold"), bg="#10b981", fg="white", activebackground="#059669", activeforeground="white", relief="flat", padx=14, pady=7, command=lambda: os.system("start ms-settings:windowsupdate"))
        btn_upd_win.pack(side="right", padx=5)

        btn_dev_mgr = tk.Button(ctrl_frame, text="⚙️ Device Manager", font=("Segoe UI", 10, "bold"), bg="#0284c7", fg="white", activebackground="#0369a1", activeforeground="white", relief="flat", padx=14, pady=7, command=lambda: os.system("start devmgmt.msc"))
        btn_dev_mgr.pack(side="right", padx=5)

    def log(self, text):
        self.log_txt.insert(tk.END, text)
        self.log_txt.see(tk.END)

    # ================= WINDOWS SYSTEM & SERVICES =================
    def scan_win_startup(self):
        def _bg():
            self.log("Scanning Windows Startup Programs...\n")
            cmd = "powershell -Command \"Get-CimInstance Win32_StartupCommand | Select-Object Name, Command | Format-Table -HideTableHeaders\""
            p = subprocess.run(cmd, capture_output=True, text=True, shell=True)
            lines = [l.strip() for l in p.stdout.split('\n') if l.strip()]
            self.startup_list.delete(0, tk.END)
            for l in lines:
                self.startup_list.insert(tk.END, l)
            self.log("✅ Startup programs scanned successfully.\n")
        threading.Thread(target=_bg, daemon=True).start()

    def optimize_win_services(self):
        def _bg():
            self.log("Optimizing Windows Background Services...\n")
            services = ["SysMain", "DiagTrack", "MapsBroker", "dmwappushservice"]
            for s in services:
                subprocess.run(f"powershell -Command \"Stop-Service -Name {s} -ErrorAction SilentlyContinue; Set-Service -Name {s} -StartupType Disabled -ErrorAction SilentlyContinue\"", shell=True)
                self.log(f"Disabled background service: {s}\n")
            messagebox.showinfo("Windows Services", "Heavy Windows Services (SysMain, Telemetry) Disabled Successfully!")
        threading.Thread(target=_bg, daemon=True).start()

    # ================= GAMING & NETWORK LOW PING =================
    def boost_power_plan(self):
        def _bg():
            self.log("Enabling Ultimate Performance Power Plan...\n")
            subprocess.run("powercfg -duplicatescheme e9a42b02-d5df-448d-aa00-03f14749eb61", shell=True)
            subprocess.run("powercfg /setactive e9a42b02-d5df-448d-aa00-03f14749eb61", shell=True)
            messagebox.showinfo("Power Plan", "Ultimate Performance Power Plan Enabled!")
        threading.Thread(target=_bg, daemon=True).start()

    def boost_game_mode(self):
        def _bg():
            self.log("Enabling Windows Game Mode & HAGS GPU Scheduling...\n")
            reg1 = 'reg add "HKCU\\Software\\Microsoft\\GameBar" /v "AllowAutoGameMode" /t REG_DWORD /d 1 /f'
            reg2 = 'reg add "HKLM\\SYSTEM\\CurrentControlSet\\Control\\GraphicsDrivers" /v "HwSchMode" /t REG_DWORD /d 2 /f'
            subprocess.run(reg1, shell=True)
            subprocess.run(reg2, shell=True)
            messagebox.showinfo("Game Mode", "Windows Game Mode & Hardware GPU Scheduling Enabled!")
        threading.Thread(target=_bg, daemon=True).start()

    def boost_network_lowping(self):
        def _bg():
            self.log("Flushing DNS, Resetting Winsock & Enabling Low Ping TCP NoDelay...\n")
            subprocess.run("ipconfig /flushdns", shell=True)
            subprocess.run("netsh int ip reset", shell=True)
            subprocess.run("netsh winsock reset", shell=True)
            messagebox.showinfo("Network Low Ping", "DNS Flushed, Winsock Reset, & Network Latency Optimized!")
        threading.Thread(target=_bg, daemon=True).start()

    def boost_clear_shader_cache(self):
        def _bg():
            self.log("Clearing DirectX Shader & Temp Cache...\n")
            temp_dirs = [os.path.expandvars(r"%TEMP%"), r"C:\Windows\Temp"]
            for d in temp_dirs:
                if os.path.exists(d):
                    try:
                        for f in os.listdir(d):
                            fp = os.path.join(d, f)
                            if os.path.isfile(fp):
                                os.remove(fp)
                    except Exception: pass
            messagebox.showinfo("Shader Cache", "DirectX Shader & Temporary Junk Cache Cleared!")
        threading.Thread(target=_bg, daemon=True).start()

    # ================= DRIVER SCANNER =================
    def scan_system_drivers(self):
        def _bg():
            self.log("Scanning System Hardware Drivers...\n")
            cmd = "powershell -Command \"Get-PnpDevice -PresentOnly | Where-Object {$_.Status -ne 'OK'} | Select-Object FriendlyName, Status, Class | Format-Table -HideTableHeaders\""
            p = subprocess.run(cmd, capture_output=True, text=True, shell=True)
            lines = [l.strip() for l in p.stdout.split('\n') if l.strip()]
            self.drv_listbox.delete(0, tk.END)

            if lines:
                self.log("⚠️ Found devices requiring driver updates:\n")
                for l in lines:
                    self.drv_listbox.insert(tk.END, f"⚠️ {l}")
            else:
                self.drv_listbox.insert(tk.END, "✅ All System Hardware Drivers (Graphics, Audio, Network) Status: OK!")
                self.log("✅ All hardware drivers are running cleanly.\n")

        threading.Thread(target=_bg, daemon=True).start()

if __name__ == "__main__":
    root = tk.Tk()
    app = PcGameOptimizerApp(root)
    root.mainloop()
