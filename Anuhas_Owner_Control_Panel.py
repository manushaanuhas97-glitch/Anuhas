import tkinter as tk
from tkinter import messagebox, ttk
import urllib.request
import json
import webbrowser
import os

# ========================================================
# ANUHAS TOOLS - OWNER DESKTOP CONTROL APPLICATION (.EXE)
# ========================================================

OWNER_PASSWORD = "20070630"
CONFIG_FILE = os.path.join(os.path.expanduser("~"), ".anuhas_admin_config.json")

class OwnerControlApp:
    def __init__(self, root):
        self.root = root
        self.root.title("👑 Anuhas Owner Control Panel")
        self.root.geometry("520x620")
        self.root.configure(bg="#050711")

        self.style = ttk.Style()
        self.style.theme_use('clam')

        self.create_login_ui()

    def create_login_ui(self):
        self.login_frame = tk.Frame(self.root, bg="#050711", padding=20)
        self.login_frame.pack(expand=True, fill="both", padx=30, pady=40)

        title = tk.Label(self.login_frame, text="👑 Owner Control Panel", font=("Segoe UI", 18, "bold"), fg="#c084fc", bg="#050711")
        title.pack(pady=10)

        sub = tk.Label(self.login_frame, text="Enter Security Password to access Owner Dashboard:", font=("Segoe UI", 10), fg="#94a3b8", bg="#050711")
        sub.pack(pady=5)

        self.pass_entry = tk.Entry(self.login_frame, show="*", font=("Consolas", 14), width=20, justify="center")
        self.pass_entry.pack(pady=15)
        self.pass_entry.focus()

        btn = tk.Button(self.login_frame, text="Unlock Dashboard 🔑", font=("Segoe UI", 11, "bold"), bg="#9333ea", fg="white", activebackground="#a855f7", activeforeground="white", relief="flat", padx=15, pady=8, command=self.verify_password)
        btn.pack(pady=10)

    def verify_password(self):
        if self.pass_entry.get() == OWNER_PASSWORD:
            self.login_frame.destroy()
            self.create_dashboard_ui()
        else:
            messagebox.showerror("Access Denied", "Incorrect Password! Access Denied.")

    def create_dashboard_ui(self):
        dash = tk.Frame(self.root, bg="#050711", padx=20, pady=20)
        dash.pack(expand=True, fill="both")

        header = tk.Label(dash, text="⚡ Anuhas Control Dashboard", font=("Segoe UI", 16, "bold"), fg="#67e8f9", bg="#050711")
        header.pack(anchor="w", pady=(0, 5))

        status = tk.Label(dash, text="Logged in as Owner (Manusha Anuhas)", font=("Segoe UI", 9, "bold"), fg="#10b981", bg="#050711")
        status.pack(anchor="w", pady=(0, 15))

        # Toggles
        toggles_frame = tk.LabelFrame(dash, text=" 🛑 Maintenance Mode (ON/OFF Tools) ", font=("Segoe UI", 10, "bold"), fg="#c084fc", bg="#050711", padx=15, pady=10)
        toggles_frame.pack(fill="x", pady=10)

        self.tools_vars = {}
        tools = [
            ("pc-optimizer", "🎮 PC & Gaming Optimizer Hub"),
            ("wage-saver", "💰 Wage Saver Tool"),
            ("unit-converter", "🔢 Unit Converter"),
            ("stopwatch", "⏱️ Stopwatch & Timer"),
            ("color-picker", "🎨 Color Picker & Palette"),
            ("password-generator", "🔐 Password Generator"),
            ("qr-generator", "⚡ Universal QR Studio"),
            ("notes", "📝 Smart Notes & Todo"),
            ("calculator", "🧮 Scientific Calculator")
        ]

        config = self.load_config()

        for key, name in tools:
            var = tk.BooleanVar(value=config.get(key, True))
            self.tools_vars[key] = var
            chk = tk.Checkbutton(toggles_frame, text=name, variable=var, font=("Segoe UI", 9.5), fg="#f8fafc", bg="#050711", selectcolor="#050711", activebackground="#050711", activeforeground="white")
            chk.pack(anchor="w", pady=2)

        # Announcement
        notice_frame = tk.LabelFrame(dash, text=" 📢 Global Broadcast Announcement ", font=("Segoe UI", 10, "bold"), fg="#67e8f9", bg="#050711", padx=15, pady=10)
        notice_frame.pack(fill="x", pady=10)

        self.notice_entry = tk.Entry(notice_frame, font=("Segoe UI", 10), bg="#1e293b", fg="white", insertbackground="white")
        self.notice_entry.pack(fill="x", pady=5)
        self.notice_entry.insert(0, config.get("notice", ""))

        # Action Buttons
        btn_frame = tk.Frame(dash, bg="#050711")
        btn_frame.pack(fill="x", pady=15)

        btn_save = tk.Button(btn_frame, text="💾 Save Changes", font=("Segoe UI", 10, "bold"), bg="#10b981", fg="white", padx=15, pady=8, relief="flat", command=self.save_config)
        btn_save.pack(side="left", padx=5)

        btn_open = tk.Button(btn_frame, text="🌐 Open Live Site", font=("Segoe UI", 10, "bold"), bg="#06b6d4", fg="white", padx=15, pady=8, relief="flat", command=lambda: webbrowser.open("https://tinyurl.com/anuhas-lk"))
        btn_open.pack(side="right", padx=5)

    def load_config(self):
        if os.path.exists(CONFIG_FILE):
            try:
                with open(CONFIG_FILE, 'r') as f:
                    return json.load(f)
            except: pass
        return {}

    def save_config(self):
        config = {key: var.get() for key, var in self.tools_vars.items()}
        config["notice"] = self.notice_entry.get()
        with open(CONFIG_FILE, 'w') as f:
            json.dump(config, f)
        messagebox.showinfo("Saved", "Settings saved successfully!")

if __name__ == "__main__":
    root = tk.Tk()
    app = OwnerControlApp(root)
    root.mainloop()
