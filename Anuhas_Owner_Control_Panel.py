import webview
import os
import sys

# ========================================================
# ANUHAS TOOLS - NATIVE WEB OWNER CONTROL PANEL APP (.EXE)
# ========================================================

def main():
    icon_path = os.path.join(os.path.dirname(__file__), "app_icon.ico")
    if not os.path.exists(icon_path):
        icon_path = None

    url = "https://manushaanuhas97-glitch.github.io/Anuhas/admin/index.html"

    # Create native Windows desktop window embedding the exact web Admin Panel
    window = webview.create_window(
        title="👑 Anuhas Owner Control Panel",
        url=url,
        width=750,
        height=850,
        resizable=True,
        min_size=(600, 700)
    )

    webview.start(private_mode=False)

if __name__ == "__main__":
    main()
