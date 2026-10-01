import tkinter as tk
from tkinter import ttk
import threading
from app import run_server


class ServerGuiApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Flask Server Manager")
        self.root.geometry("460x220")  # Slightly reduced height since the browse button is removed
        self.root.resizable(False, False)

        # Light color palette
        self.bg_color = "#ffffff"     # Pure white background
        self.input_bg = "#f5f6fa"     # Light gray background for input fields
        self.text_color = "#2c3e50"   # Dark blue/gray text color for high contrast

        self.root.configure(bg=self.bg_color)

        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.configure_light_styles()

        # Variables to store user input data
        self.ip_var = tk.StringVar(value="127.0.0.1")
        self.port_var = tk.StringVar(value="5000")
        self.path_var = tk.StringVar(value="")

        # Main container frame with padding and white background
        self.main_frame = ttk.Frame(self.root, padding="20 20 20 20", style="Light.TFrame")
        self.main_frame.pack(fill="both", expand=True)

        self.create_widgets()

    def configure_light_styles(self):
        """Configure widget styles for the light theme."""
        self.style.configure("Light.TFrame", background=self.bg_color)
        self.style.configure("TLabel", font=("Segoe UI", 10), background=self.bg_color, foreground=self.text_color)
        self.style.configure("TEntry", font=("Segoe UI", 10), padding=4, fieldbackground=self.input_bg,
                             foreground="#000000")

    def show_custom_message(self, title, message, is_error=False):
        """Display a fully custom, pure-white modal message dialog."""
        msg_window = tk.Toplevel(self.root)
        msg_window.title(title)
        msg_window.geometry("360x140")
        msg_window.resizable(False, False)
        msg_window.configure(bg=self.bg_color)

        # Modality and center alignment relative to the main window
        msg_window.transient(self.root)
        msg_window.grab_set()

        x = self.root.winfo_x() + (self.root.winfo_width() // 2) - 180
        y = self.root.winfo_y() + (self.root.winfo_height() // 2) - 70
        msg_window.geometry(f"+{x}+{y}")

        icon = "❌ " if is_error else "✅ "

        frame = ttk.Frame(msg_window, padding=15, style="Light.TFrame")
        frame.pack(fill="both", expand=True)

        lbl = ttk.Label(frame, text=icon + message, wraplength=320, justify="center", font=("Segoe UI", 10))
        lbl.pack(pady=10)

        # Color schemes for the action button
        btn_color = "#e74c3c" if is_error else "#2ecc71"
        btn_active = "#c0392b" if is_error else "#27ae60"

        close_btn = tk.Button(
            frame, text="OK", font=("Segoe UI", 10, "bold"),
            bg=btn_color, fg="white", activebackground=btn_active, activeforeground="white",
            relief="flat", width=12, command=msg_window.destroy
        )
        close_btn.pack(pady=5)

    def create_widgets(self):
        # --- Row 1: IP Address ---
        ttk.Label(self.main_frame, text="🌐 IP Address:").grid(row=0, column=0, padx=5, pady=8, sticky="w")
        self.ip_entry = ttk.Entry(self.main_frame, textvariable=self.ip_var, width=35)
        self.ip_entry.grid(row=0, column=1, padx=5, pady=8, sticky="we")

        # --- Row 2: Port ---
        ttk.Label(self.main_frame, text="🔌 Port:").grid(row=1, column=0, padx=5, pady=8, sticky="w")
        self.port_entry = ttk.Entry(self.main_frame, textvariable=self.port_var, width=35)
        self.port_entry.grid(row=1, column=1, columnspan=2, padx=5, pady=8, sticky="we")

        # --- Row 3: Target Path ---
        ttk.Label(self.main_frame, text="📁 Video Directory:").grid(row=2, column=0, padx=5, pady=8, sticky="w")
        self.path_entry = ttk.Entry(self.main_frame, textvariable=self.path_var, width=35)
        self.path_entry.grid(row=2, column=1, columnspan=2, padx=5, pady=8, sticky="we")

        # Configure column weights to ensure input entries expand properly
        self.main_frame.columnconfigure(1, weight=1)

        # --- Row 4: Action Button ---
        self.start_btn = tk.Button(
            self.main_frame,
            text="🚀 Start Server",
            font=("Segoe UI", 11, "bold"),
            bg="#2ecc71",
            fg="white",
            activebackground="#27ae60",
            activeforeground="white",
            relief="flat",
            command=self.start_server_thread
        )
        self.start_btn.grid(row=3, column=0, columnspan=2, pady=15, sticky="we")

    def start_server_thread(self):
        """Validate forms and launch the Flask server inside an independent thread."""
        ip = self.ip_var.get().strip()
        port = self.port_var.get().strip()
        path = self.path_var.get().strip()

        if not ip or not port or not path:
            self.show_custom_message("Error", "All fields (IP, Port, and Path) are required!", is_error=True)
            return

        try:
            int(port)
        except ValueError:
            self.show_custom_message("Error", "Port must be a valid number!", is_error=True)
            return

        # Disable all UI element controls and toggle running status
        self.start_btn.config(text="⚙️ Server Running...", state="disabled", bg="#dcdde1")
        self.ip_entry.config(state="disabled")
        self.port_entry.config(state="disabled")
        self.path_entry.config(state="disabled")

        # Launch the Flask server runner as a background daemon thread
        server_thread = threading.Thread(target=run_server, args=(ip, port, path), daemon=True)
        server_thread.start()

        self.show_custom_message("Success", f"Server successfully started on http://{ip}:{port}")


if __name__ == "__main__":
    root = tk.Tk()
    app = ServerGuiApp(root)
    root.mainloop()