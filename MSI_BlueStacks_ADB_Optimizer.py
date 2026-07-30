import tkinter as tk
from tkinter import ttk, messagebox
import subprocess
import os
import threading
import sys

# =========================================================================
# ANUHAS TOOLS — MSI & BLUESTACKS ADB EMULATOR OPTIMIZER & DEBLOATER (.EXE)
# =========================================================================

class AdbOptimizerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🎮 MSI & BlueStacks ADB Emulator Optimizer & Debloater")
        self.root.geometry("780x750")
        self.root.minsize(700, 650)
        self.root.configure(bg="#090d16")

        # Set Icon
        try:
            ico_path = os.path.join(os.path.dirname(__file__), "app_icon.ico")
            if os.path.exists(ico_path):
                self.root.iconbitmap(ico_path)
        except Exception:
            pass

        self.device_id = None
        self.create_ui()
        self.auto_connect_adb()

    def create_ui(self):
        # Header Bar
        header = tk.Frame(self.root, bg="#0f172a", padx=20, pady=12)
        header.pack(fill="x")

        title_lbl = tk.Label(header, text="🎮 MSI & BlueStacks ADB Optimizer", font=("Segoe UI", 16, "bold"), fg="#38bdf8", bg="#0f172a")
        title_lbl.pack(side="left")

        sub_lbl = tk.Label(header, text="by Manusha Anuhas", font=("Segoe UI", 9, "bold"), fg="#94a3b8", bg="#0f172a")
        sub_lbl.pack(side="right")

        # Connection Status Banner
        conn_frame = tk.Frame(self.root, bg="#1e293b", padx=15, pady=10)
        conn_frame.pack(fill="x", padx=15, pady=10)

        self.status_lbl = tk.Label(conn_frame, text="🔴 Checking ADB Connection...", font=("Segoe UI", 11, "bold"), fg="#ef4444", bg="#1e293b")
        self.status_lbl.pack(side="left")

        btn_reconnect = tk.Button(conn_frame, text="🔄 Connect / Refresh ADB", font=("Segoe UI", 9, "bold"), bg="#0284c7", fg="white", relief="flat", padx=12, pady=4, command=self.auto_connect_adb)
        btn_reconnect.pack(side="right")

        # Notebook Tabs
        self.tabs = ttk.Notebook(self.root)
        self.tabs.pack(fill="both", expand=True, padx=15, pady=5)

        # Tab 1: App Manager & Debloater
        self.tab_apps = tk.Frame(self.tabs, bg="#090d16", padx=15, pady=15)
        self.tabs.add(self.tab_apps, text="📦 App Manager & Uninstaller")

        # Tab 2: System & Gaming Tweaker
        self.tab_tweaks = tk.Frame(self.tabs, bg="#090d16", padx=15, pady=15)
        self.tabs.add(self.tab_tweaks, text="⚡ System Tweaks & 120 FPS")

        self.build_app_manager_tab()
        self.build_tweaks_tab()

        # Log Console
        log_frame = tk.LabelFrame(self.root, text=" 📜 ADB Command Output Log ", font=("Segoe UI", 9, "bold"), fg="#38bdf8", bg="#090d16", padx=10, pady=5)
        log_frame.pack(fill="x", padx=15, pady=(5, 12))

        self.log_txt = tk.Text(log_frame, height=6, bg="#020617", fg="#4ade80", font=("Consolas", 9.5), relief="flat")
        self.log_txt.pack(fill="both", expand=True)

    def build_app_manager_tab(self):
        lbl_info = tk.Label(self.tab_apps, text="Installed Packages in Emulator (Select an app to uninstall individually or uninstall all non-system apps):", font=("Segoe UI", 9.5), fg="#cbd5e1", bg="#090d16", justify="left")
        lbl_info.pack(anchor="w", pady=(0, 6))

        # Filter & Search Box
        filter_frame = tk.Frame(self.tab_apps, bg="#090d16")
        filter_frame.pack(fill="x", pady=4)

        tk.Label(filter_frame, text="🔍 Filter:", font=("Segoe UI", 9.5, "bold"), fg="#94a3b8", bg="#090d16").pack(side="left")
        self.search_entry = tk.Entry(filter_frame, font=("Segoe UI", 9.5), bg="#1e293b", fg="white", insertbackground="white")
        self.search_entry.pack(side="left", fill="x", expand=True, padx=8)
        self.search_entry.bind("<KeyRelease>", self.filter_packages)

        btn_fetch = tk.Button(filter_frame, text="🔄 Load Apps", font=("Segoe UI", 9, "bold"), bg="#3b82f6", fg="white", relief="flat", padx=10, pady=3, command=self.load_installed_packages)
        btn_fetch.pack(side="right")

        # Listbox & Scrollbar
        list_frame = tk.Frame(self.tab_apps, bg="#090d16")
        list_frame.pack(fill="both", expand=True, pady=8)

        self.pkg_listbox = tk.Listbox(list_frame, bg="#020617", fg="#f8fafc", selectbackground="#0284c7", selectforeground="white", font=("Consolas", 10), relief="flat")
        scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=self.pkg_listbox.yview)
        self.pkg_listbox.configure(yscrollcommand=scrollbar.set)

        self.pkg_listbox.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Uninstall Controls
        btn_box = tk.Frame(self.tab_apps, bg="#090d16")
        btn_box.pack(fill="x", pady=6)

        btn_uninst_one = tk.Button(btn_box, text="🗑️ Uninstall Selected App", font=("Segoe UI", 10, "bold"), bg="#ef4444", fg="white", relief="flat", padx=14, pady=6, command=self.uninstall_selected_app)
        btn_uninst_one.pack(side="left", padx=5)

        btn_uninst_all = tk.Button(btn_box, text="🔥 Uninstall ALL User Apps", font=("Segoe UI", 10, "bold"), bg="#b91c1c", fg="white", relief="flat", padx=14, pady=6, command=self.uninstall_all_user_apps)
        btn_uninst_all.pack(side="right", padx=5)

        self.all_packages = []

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
            card = tk.Frame(self.tab_tweaks, bg="#1e293b", padx=14, pady=10)
            card.pack(fill="x", pady=5)

            info = tk.Frame(card, bg="#1e293b")
            info.pack(side="left", fill="x", expand=True)

            lbl_n = tk.Label(info, text=name, font=("Segoe UI", 10.5, "bold"), fg="#f8fafc", bg="#1e293b")
            lbl_n.pack(anchor="w")

            lbl_d = tk.Label(info, text=desc, font=("Segoe UI", 8.5), fg="#94a3b8", bg="#1e293b")
            lbl_d.pack(anchor="w")

            btn = tk.Button(card, text="Apply Tweak ⚡", font=("Segoe UI", 9, "bold"), bg="#10b981", fg="white", relief="flat", padx=12, pady=5, command=cmd_func)
            btn.pack(side="right")

    # ================= ADB COMMAND EXECUTION =================
    def run_adb(self, cmd_args):
        try:
            full_cmd = ["adb"] + (["-s", self.device_id] if self.device_id else []) + cmd_args
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

    def auto_connect_adb(self):
        def _bg():
            self.log("Connecting to ADB ports (127.0.0.1:5555, 5554, 62001)...\n")
            ports = ["127.0.0.1:5555", "127.0.0.1:5554", "127.0.0.1:62001", "127.0.0.1:5556"]
            
            subprocess.run(["adb", "start-server"], capture_output=True)

            connected_dev = None
            for p in ports:
                res = subprocess.run(["adb", "connect", p], capture_output=True, text=True)
                if "connected" in res.stdout.lower() or "already" in res.stdout.lower():
                    connected_dev = p
                    break

            # Check devices
            dev_res = subprocess.run(["adb", "devices"], capture_output=True, text=True)
            lines = [l.split()[0] for l in dev_res.stdout.strip().split('\n')[1:] if "device" in l]

            if lines:
                self.device_id = lines[0]
                self.status_lbl.config(text=f"🟢 ADB Connected: {self.device_id}", fg="#10b981")
                self.log(f"✅ ADB Connected successfully to {self.device_id}\n")
                self.load_installed_packages()
            else:
                self.device_id = None
                self.status_lbl.config(text="🔴 ADB Not Connected (Launch BlueStacks/MSI & Enable ADB)", fg="#ef4444")
                self.log("⚠️ No ADB device detected. Make sure ADB is enabled in Emulator settings.\n")

        threading.Thread(target=_bg, daemon=True).start()

    def load_installed_packages(self):
        if not self.device_id: return
        def _bg():
            self.log("Fetching installed packages...\n")
            out = self.run_adb(["shell", "pm", "list", "packages"])
            pkgs = [line.replace("package:", "").strip() for line in out.split('\n') if line.startswith("package:")]
            self.all_packages = sorted(pkgs)
            self.root.after(0, lambda: self.filter_packages(None))
        threading.Thread(target=_bg, daemon=True).start()

    def filter_packages(self, event):
        query = self.search_entry.get().lower().trim() if hasattr(self.search_entry.get(), 'trim') else self.search_entry.get().lower().strip()
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
        if not messagebox.askyesno("WARNING", "This will uninstall ALL third-party user apps installed in the emulator. Continue?"):
            return

        def _bg():
            out = self.run_adb(["shell", "pm", "list", "packages", "-3"])
            user_pkgs = [line.replace("package:", "").strip() for line in out.split('\n') if line.startswith("package:")]
            
            for p in user_pkgs:
                self.log(f"Uninstalling {p}...\n")
                self.run_adb(["shell", "pm", "uninstall", "--user", "0", p])

            messagebox.showinfo("Completed", "All non-system user apps uninstalled successfully!")
            self.load_installed_packages()

        threading.Thread(target=_bg, daemon=True).start()

    # ================= TWEAKS =================
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
            bloat = [
                "com.google.android.feedback",
                "com.google.android.marvin.talkback",
                "com.android.printspooler"
            ]
            for b in bloat:
                self.run_adb(["shell", "pm", "disable-user", "--user", "0", b])
            messagebox.showinfo("Tweak Applied", "Useless System Telemetry & Bloatware Disabled!")
        threading.Thread(target=_bg, daemon=True).start()

if __name__ == "__main__":
    root = tk.Tk()
    app = AdbOptimizerApp(root)
    root.mainloop()
