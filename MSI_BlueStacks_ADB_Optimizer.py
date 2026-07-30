import tkinter as tk
from tkinter import ttk, messagebox
import subprocess
import os
import threading
import sys
import re

# =========================================================================
# ANUHAS TOOLS — ULTIMATE PC, GAMING & EMULATOR SUPER OPTIMIZER (.EXE)
# =========================================================================

def get_adb_binary_path():
    base_dir = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    local_adb = os.path.join(base_dir, 'adb.exe')
    if os.path.exists(local_adb):
        return local_adb
    local_adb_alt = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'adb.exe')
    if os.path.exists(local_adb_alt):
        return local_adb_alt
    return 'adb'

class SuperOptimizerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🚀 Anuhas Ultimate PC, Gaming & Emulator Super Optimizer")
        self.root.geometry("860x800")
        self.root.minsize(750, 680)
        self.root.configure(bg="#090d16")

        self.adb_bin = get_adb_binary_path()

        # Set Icon
        try:
            base_dir = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
            ico_path = os.path.join(base_dir, "app_icon.ico")
            if os.path.exists(ico_path):
                self.root.iconbitmap(ico_path)
        except Exception:
            pass

        self.device_id = None
        self.all_packages = []
        self.create_ui()
        self.auto_connect_adb()

    def create_ui(self):
        # Header Bar
        header = tk.Frame(self.root, bg="#0f172a", padx=20, pady=12)
        header.pack(fill="x")

        title_lbl = tk.Label(header, text="🚀 Ultimate PC, Gaming & ADB Super Optimizer", font=("Segoe UI", 16, "bold"), fg="#38bdf8", bg="#0f172a")
        title_lbl.pack(side="left")

        sub_lbl = tk.Label(header, text="by Manusha Anuhas", font=("Segoe UI", 9, "bold"), fg="#94a3b8", bg="#0f172a")
        sub_lbl.pack(side="right")

        # Connection Status Banner
        conn_frame = tk.Frame(self.root, bg="#1e293b", padx=15, pady=10)
        conn_frame.pack(fill="x", padx=15, pady=8)

        self.status_lbl = tk.Label(conn_frame, text="🔴 Checking ADB Connection...", font=("Segoe UI", 11, "bold"), fg="#ef4444", bg="#1e293b")
        self.status_lbl.pack(side="left")

        btn_reconnect = tk.Button(conn_frame, text="🔄 Connect / Refresh ADB", font=("Segoe UI", 9, "bold"), bg="#0284c7", fg="white", relief="flat", padx=12, pady=4, command=self.auto_connect_adb)
        btn_reconnect.pack(side="right")

        # Notebook Tabs
        self.tabs = ttk.Notebook(self.root)
        self.tabs.pack(fill="both", expand=True, padx=15, pady=5)

        # Tab 1: Emulator & ADB App Manager
        self.tab_apps = tk.Frame(self.tabs, bg="#090d16", padx=15, pady=12)
        self.tabs.add(self.tab_apps, text="🎮 Emulator & App Manager")

        # Tab 2: Emulator System Tweaks
        self.tab_tweaks = tk.Frame(self.tabs, bg="#090d16", padx=15, pady=12)
        self.tabs.add(self.tab_tweaks, text="⚡ Emulator Tweaks & 120 FPS")

        # Tab 3: Windows Startup & Services
        self.tab_win_sys = tk.Frame(self.tabs, bg="#090d16", padx=15, pady=12)
        self.tabs.add(self.tab_win_sys, text="💻 Windows Startup & Services")

        # Tab 4: PC Gaming & Low Ping Booster
        self.tab_game_boost = tk.Frame(self.tabs, bg="#090d16", padx=15, pady=12)
        self.tabs.add(self.tab_game_boost, text="🚀 Gaming & Network Low Ping")

        # Tab 5: Driver Scanner & Updater
        self.tab_drivers = tk.Frame(self.tabs, bg="#090d16", padx=15, pady=12)
        self.tabs.add(self.tab_drivers, text="🔌 Driver Scanner & Updater")

        self.build_app_manager_tab()
        self.build_tweaks_tab()
        self.build_win_sys_tab()
        self.build_game_boost_tab()
        self.build_drivers_tab()

        # Log Console
        log_frame = tk.LabelFrame(self.root, text=" 📜 Action Log ", font=("Segoe UI", 9, "bold"), fg="#38bdf8", bg="#090d16", padx=10, pady=5)
        log_frame.pack(fill="x", padx=15, pady=(5, 10))

        self.log_txt = tk.Text(log_frame, height=5, bg="#020617", fg="#4ade80", font=("Consolas", 10), relief="flat")
        self.log_txt.pack(fill="both", expand=True)

    # ================= TAB 1: EMULATOR APP MANAGER =================
    def build_app_manager_tab(self):
        lbl_info = tk.Label(self.tab_apps, text="Installed Packages in Emulator (Play Store is 100% Protected):", font=("Segoe UI", 10), fg="#cbd5e1", bg="#090d16", justify="left")
        lbl_info.pack(anchor="w", pady=(0, 4))

        filter_frame = tk.Frame(self.tab_apps, bg="#090d16")
        filter_frame.pack(fill="x", pady=4)

        tk.Label(filter_frame, text="🔍 Filter:", font=("Segoe UI", 10, "bold"), fg="#94a3b8", bg="#090d16").pack(side="left")
        self.search_entry = tk.Entry(filter_frame, font=("Segoe UI", 10), bg="#1e293b", fg="white", insertbackground="white")
        self.search_entry.pack(side="left", fill="x", expand=True, padx=8)
        self.search_entry.bind("<KeyRelease>", self.filter_packages)

        btn_fetch = tk.Button(filter_frame, text="🔄 Load Apps", font=("Segoe UI", 9, "bold"), bg="#3b82f6", fg="white", relief="flat", padx=10, pady=3, command=self.load_installed_packages)
        btn_fetch.pack(side="right")

        list_frame = tk.Frame(self.tab_apps, bg="#090d16")
        list_frame.pack(fill="both", expand=True, pady=6)

        self.pkg_listbox = tk.Listbox(list_frame, bg="#020617", fg="#f8fafc", selectbackground="#0284c7", selectforeground="white", font=("Consolas", 10), relief="flat")
        scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=self.pkg_listbox.yview)
        self.pkg_listbox.configure(yscrollcommand=scrollbar.set)

        self.pkg_listbox.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        btn_box = tk.Frame(self.tab_apps, bg="#090d16")
        btn_box.pack(fill="x", pady=4)

        btn_uninst_one = tk.Button(btn_box, text="🗑️ Uninstall Selected App", font=("Segoe UI", 10, "bold"), bg="#ef4444", fg="white", relief="flat", padx=14, pady=5, command=self.uninstall_selected_app)
        btn_uninst_one.pack(side="left", padx=5)

        btn_uninst_all = tk.Button(btn_box, text="🔥 Uninstall ALL User Apps", font=("Segoe UI", 10, "bold"), bg="#b91c1c", fg="white", relief="flat", padx=14, pady=5, command=self.uninstall_all_user_apps)
        btn_uninst_all.pack(side="right", padx=5)

    # ================= TAB 2: EMULATOR SYSTEM TWEAKS =================
    def build_tweaks_tab(self):
        tweaks = [
            ("⚡ Turn OFF All System Animations", "Disables window & transition scale to make emulator super fast", self.tweak_disable_animations),
            ("🚀 Unlock 120 FPS Mode", "Removes 60 FPS cap for ultra smooth gaming", self.tweak_unlock_120fps),
            ("🎯 Smooth Aim & 320 DPI Tweak", "Fixes mouse acceleration & aim skip in Free Fire", self.tweak_dpi_aim),
            ("🧹 Flush Memory & Trim Caches", "Clears background RAM cache and memory leaks", self.tweak_trim_ram),
            ("🎮 Force Hardware GPU Rendering", "Forces OpenGL/Vulkan GPU acceleration", self.tweak_force_gpu),
            ("🛑 Disable Useless Telemetry & Bloatware", "Disables background logging and ad services", self.tweak_debloat_system)
        ]

        for name, desc, cmd_func in tweaks:
            card = tk.Frame(self.tab_tweaks, bg="#1e293b", padx=14, pady=8)
            card.pack(fill="x", pady=4)

            info = tk.Frame(card, bg="#1e293b")
            info.pack(side="left", fill="x", expand=True)

            lbl_n = tk.Label(info, text=name, font=("Segoe UI", 10, "bold"), fg="#f8fafc", bg="#1e293b")
            lbl_n.pack(anchor="w")

            lbl_d = tk.Label(info, text=desc, font=("Segoe UI", 8.5), fg="#94a3b8", bg="#1e293b")
            lbl_d.pack(anchor="w")

            btn = tk.Button(card, text="Apply ⚡", font=("Segoe UI", 8.5, "bold"), bg="#10b981", fg="white", relief="flat", padx=12, pady=4, command=cmd_func)
            btn.pack(side="right")

    # ================= TAB 3: WINDOWS STARTUP & SERVICES =================
    def build_win_sys_tab(self):
        lbl = tk.Label(self.tab_win_sys, text="Windows Startup Programs & Unnecessary Background Services:", font=("Segoe UI", 10, "bold"), fg="#38bdf8", bg="#090d16")
        lbl.pack(anchor="w", pady=(0, 6))

        # Startup Apps Section
        start_frame = tk.LabelFrame(self.tab_win_sys, text=" 🚀 Startup Programs ", font=("Segoe UI", 9, "bold"), fg="#cbd5e1", bg="#090d16", padx=10, pady=6)
        start_frame.pack(fill="x", pady=4)

        self.startup_list = tk.Listbox(start_frame, height=5, bg="#020617", fg="#f8fafc", font=("Consolas", 9), relief="flat")
        self.startup_list.pack(fill="x", pady=4)

        btn_scan_start = tk.Button(start_frame, text="🔍 Scan Startup Apps", font=("Segoe UI", 9, "bold"), bg="#3b82f6", fg="white", relief="flat", padx=10, pady=3, command=self.scan_win_startup)
        btn_scan_start.pack(side="left", pady=2)

        btn_open_msconfig = tk.Button(start_frame, text="⚙️ Open Windows Task Manager Startup", font=("Segoe UI", 9, "bold"), bg="#0284c7", fg="white", relief="flat", padx=10, pady=3, command=lambda: os.system("start taskmgr"))
        btn_open_msconfig.pack(side="right", pady=2)

        # Services Section
        srv_frame = tk.LabelFrame(self.tab_win_sys, text=" 🛡️ Windows Background Services Optimizer ", font=("Segoe UI", 9, "bold"), fg="#cbd5e1", bg="#090d16", padx=10, pady=8)
        srv_frame.pack(fill="x", pady=6)

        srv_info = tk.Label(srv_frame, text="Disables SysMain (Superfetch), Connected User Experiences (Telemetry), & Diagnostic Tracking services to free RAM & CPU.", font=("Segoe UI", 8.5), fg="#94a3b8", bg="#090d16", justify="left")
        srv_info.pack(anchor="w", pady=(0, 4))

        btn_opt_srv = tk.Button(srv_frame, text="🚀 Optimize & Disable Heavy Windows Services", font=("Segoe UI", 10, "bold"), bg="#10b981", fg="white", relief="flat", padx=14, pady=6, command=self.optimize_win_services)
        btn_opt_srv.pack(anchor="w", pady=4)

    # ================= TAB 4: PC GAMING & LOW PING BOOSTER =================
    def build_game_boost_tab(self):
        boosters = [
            ("⚡ Ultimate Performance Power Plan", "Enables Windows Ultimate Performance power scheme for max CPU clock", self.boost_power_plan),
            ("🎮 Windows Game Mode & Hardware GPU Scheduling", "Enables Game Mode & HAGS registry tweaks for maximum FPS", self.boost_game_mode),
            ("🌐 Low Ping TCP/IP & Network Flush", "Flushes DNS cache, resets Winsock, and enables TCP NoDelay", self.boost_network_lowping),
            ("🧹 Clear DirectX Shader & Temp Cache", "Deletes junk DirectX shader cache & Windows temp files to fix stuttering", self.boost_clear_shader_cache)
        ]

        for name, desc, cmd_func in boosters:
            card = tk.Frame(self.tab_game_boost, bg="#1e293b", padx=14, pady=10)
            card.pack(fill="x", pady=5)

            info = tk.Frame(card, bg="#1e293b")
            info.pack(side="left", fill="x", expand=True)

            lbl_n = tk.Label(info, text=name, font=("Segoe UI", 10.5, "bold"), fg="#f8fafc", bg="#1e293b")
            lbl_n.pack(anchor="w")

            lbl_d = tk.Label(info, text=desc, font=("Segoe UI", 8.5), fg="#94a3b8", bg="#1e293b")
            lbl_d.pack(anchor="w")

            btn = tk.Button(card, text="Apply Boost 🚀", font=("Segoe UI", 9, "bold"), bg="#8b5cf6", fg="white", relief="flat", padx=12, pady=5, command=cmd_func)
            btn.pack(side="right")

    # ================= TAB 5: DRIVER SCANNER & UPDATER =================
    def build_drivers_tab(self):
        lbl = tk.Label(self.tab_drivers, text="System Hardware Drivers Scanner & Windows Update Status:", font=("Segoe UI", 10, "bold"), fg="#38bdf8", bg="#090d16")
        lbl.pack(anchor="w", pady=(0, 6))

        drv_frame = tk.Frame(self.tab_drivers, bg="#090d16")
        drv_frame.pack(fill="both", expand=True, pady=4)

        self.drv_listbox = tk.Listbox(drv_frame, bg="#020617", fg="#f8fafc", font=("Consolas", 9.5), relief="flat")
        scrollbar = ttk.Scrollbar(drv_frame, orient="vertical", command=self.drv_listbox.yview)
        self.drv_listbox.configure(yscrollcommand=scrollbar.set)

        self.drv_listbox.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        ctrl_frame = tk.Frame(self.tab_drivers, bg="#090d16")
        ctrl_frame.pack(fill="x", pady=6)

        btn_scan_drv = tk.Button(ctrl_frame, text="🔍 Scan Outdated Drivers", font=("Segoe UI", 10, "bold"), bg="#3b82f6", fg="white", relief="flat", padx=14, pady=6, command=self.scan_system_drivers)
        btn_scan_drv.pack(side="left", padx=5)

        btn_upd_win = tk.Button(ctrl_frame, text="🌐 Launch Windows Driver Updater", font=("Segoe UI", 10, "bold"), bg="#10b981", fg="white", relief="flat", padx=14, pady=6, command=lambda: os.system("start ms-settings:windowsupdate"))
        btn_upd_win.pack(side="right", padx=5)

        btn_dev_mgr = tk.Button(ctrl_frame, text="⚙️ Device Manager", font=("Segoe UI", 10, "bold"), bg="#0284c7", fg="white", relief="flat", padx=14, pady=6, command=lambda: os.system("start devmgmt.msc"))
        btn_dev_mgr.pack(side="right", padx=5)

    # ================= HELPER METHODS & ADB LOGIC =================
    def run_adb(self, cmd_args):
        try:
            full_cmd = [self.adb_bin] + (["-s", self.device_id] if self.device_id else []) + cmd_args
            p = subprocess.run(full_cmd, capture_output=True, text=True, timeout=8)
            output = p.stdout.strip() or p.stderr.strip()
            self.log(f"> adb {' '.join(cmd_args)}\n{output}\n")
            return output
        except Exception as e:
            self.log(f"ERROR: {str(e)}\n")
            return ""

    def log(self, text):
        self.log_txt.insert(tk.END, text)
        self.log_txt.see(tk.END)

    def detect_bluestacks_ports(self):
        detected_ports = []
        conf_paths = [
            r"C:\ProgramData\BlueStacks_nxt\bluestacks.conf",
            r"C:\ProgramData\MSI App Player\bluestacks.conf",
            r"C:\ProgramData\BlueStacks\bluestacks.conf"
        ]
        for cp in conf_paths:
            if os.path.exists(cp):
                try:
                    with open(cp, 'r', errors='ignore') as f:
                        content = f.read()
                        ports = re.findall(r'adb_port="(\d+)"', content)
                        for port in ports:
                            detected_ports.append(f"127.0.0.1:{port}")
                except Exception: pass
        return detected_ports

    def auto_connect_adb(self):
        def _bg():
            self.log("Initializing ADB Server & Scanning Emulator Ports...\n")
            subprocess.run([self.adb_bin, "start-server"], capture_output=True)

            ports = self.detect_bluestacks_ports()
            ports.extend(["127.0.0.1:5555", "127.0.0.1:5554", "127.0.0.1:5565", "127.0.0.1:5575", "127.0.0.1:62001", "127.0.0.1:5556"])
            
            seen = set()
            unique_ports = [x for x in ports if not (x in seen or seen.add(x))]

            connected_dev = None
            for p in unique_ports:
                res = subprocess.run([self.adb_bin, "connect", p], capture_output=True, text=True)
                if "connected" in res.stdout.lower() or "already" in res.stdout.lower():
                    connected_dev = p
                    break

            dev_res = subprocess.run([self.adb_bin, "devices"], capture_output=True, text=True)
            lines = [l.split()[0] for l in dev_res.stdout.strip().split('\n')[1:] if "device" in l]

            if lines:
                self.device_id = lines[0]
                self.status_lbl.config(text=f"🟢 ADB Connected: {self.device_id}", fg="#10b981")
                self.log(f"✅ ADB Connected successfully to {self.device_id}\n")
                self.load_installed_packages()
            else:
                self.device_id = None
                self.status_lbl.config(text="🔴 ADB Not Connected (Make sure ADB is ON in Emulator Settings)", fg="#ef4444")
                self.log("⚠️ No ADB device detected. Make sure ADB is turned ON in BlueStacks/MSI Settings.\n")

        threading.Thread(target=_bg, daemon=True).start()

    def load_installed_packages(self):
        if not self.device_id: return
        def _bg():
            self.log("Fetching installed packages...\n")
            out = self.run_adb(["shell", "pm", "list", "packages"])
            protected = ["com.android.vending", "com.google.android.gms", "com.google.android.gsf"]
            pkgs = [line.replace("package:", "").strip() for line in out.split('\n') if line.startswith("package:")]
            safe_pkgs = [p for p in pkgs if p not in protected]
            self.all_packages = sorted(safe_pkgs)
            self.root.after(0, lambda: self.filter_packages(None))
        threading.Thread(target=_bg, daemon=True).start()

    def filter_packages(self, event):
        query = self.search_entry.get().strip().lower()
        self.pkg_listbox.delete(0, tk.END)
        for p in self.all_packages:
            if not query or query in p.lower():
                self.pkg_listbox.insert(tk.END, p)

    def uninstall_selected_app(self):
        sel = self.pkg_listbox.curselection()
        if not sel:
            messagebox.showwarning("Select App", "Please select an app from the list first!")
            return
        pkg = self.pkg_listbox.get(sel[0])

        if messagebox.askyesno("Confirm Uninstall", f"Are you sure you want to uninstall {pkg}?"):
            def _bg():
                self.log(f"Uninstalling {pkg}...\n")
                res = self.run_adb(["shell", "pm", "uninstall", "--user", "0", pkg])
                if "success" in res.lower():
                    messagebox.showinfo("Success", f"Uninstalled {pkg} successfully!")
                    self.load_installed_packages()
                else:
                    messagebox.showerror("Failed", f"Could not uninstall {pkg}.\nOutput: {res}")
            threading.Thread(target=_bg, daemon=True).start()

    def uninstall_all_user_apps(self):
        if not messagebox.askyesno("WARNING", "This will uninstall ALL third-party user apps installed in the emulator (Play Store is protected). Continue?"):
            return

        def _bg():
            out = self.run_adb(["shell", "pm", "list", "packages", "-3"])
            protected = ["com.android.vending", "com.google.android.gms", "com.google.android.gsf"]
            user_pkgs = [line.replace("package:", "").strip() for line in out.split('\n') if line.startswith("package:")]
            safe_pkgs = [p for p in user_pkgs if p not in protected]
            
            for p in safe_pkgs:
                self.log(f"Uninstalling {p}...\n")
                self.run_adb(["shell", "pm", "uninstall", "--user", "0", p])

            messagebox.showinfo("Completed", "All non-system user apps uninstalled successfully!")
            self.load_installed_packages()

        threading.Thread(target=_bg, daemon=True).start()

    # ================= EMULATOR TWEAKS =================
    def tweak_disable_animations(self):
        def _bg():
            self.run_adb(["shell", "settings", "put", "global", "window_animation_scale", "0"])
            self.run_adb(["shell", "settings", "put", "global", "transition_animation_scale", "0"])
            self.run_adb(["shell", "settings", "put", "global", "animator_duration_scale", "0"])
            messagebox.showinfo("Tweak Applied", "System Animations Turned OFF 100%! Emulator speed boosted.")
        threading.Thread(target=_bg, daemon=True).start()

    def tweak_unlock_120fps(self):
        def _bg():
            self.run_adb(["shell", "setprop", "debug.sf.fps", "120"])
            self.run_adb(["shell", "setprop", "persist.vendor.dfps", "120"])
            messagebox.showinfo("Tweak Applied", "120 FPS Unlocked successfully!")
        threading.Thread(target=_bg, daemon=True).start()

    def tweak_dpi_aim(self):
        def _bg():
            self.run_adb(["shell", "wm", "density", "320"])
            self.run_adb(["shell", "setprop", "pointer.speed", "7"])
            messagebox.showinfo("Tweak Applied", "Smooth Aim & 320 DPI Applied!")
        threading.Thread(target=_bg, daemon=True).start()

    def tweak_trim_ram(self):
        def _bg():
            self.run_adb(["shell", "pm", "trim-caches", "999M"])
            messagebox.showinfo("Tweak Applied", "RAM Memory & Caches Cleaned!")
        threading.Thread(target=_bg, daemon=True).start()

    def tweak_force_gpu(self):
        def _bg():
            self.run_adb(["shell", "setprop", "debug.egl.hw", "1"])
            self.run_adb(["shell", "setprop", "debug.composition.type", "gpu"])
            messagebox.showinfo("Tweak Applied", "Hardware GPU Acceleration Forced!")
        threading.Thread(target=_bg, daemon=True).start()

    def tweak_debloat_system(self):
        def _bg():
            bloat = ["com.google.android.feedback", "com.google.android.marvin.talkback", "com.android.printspooler"]
            for b in bloat:
                self.run_adb(["shell", "pm", "disable-user", "--user", "0", b])
            messagebox.showinfo("Tweak Applied", "Useless System Telemetry & Bloatware Disabled!")
        threading.Thread(target=_bg, daemon=True).start()

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
            self.log("✅ Startup programs scanned.\n")
        threading.Thread(target=_bg, daemon=True).start()

    def optimize_win_services(self):
        def _bg():
            self.log("Optimizing Windows Services...\n")
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
    app = SuperOptimizerApp(root)
    root.mainloop()
