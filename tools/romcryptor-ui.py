#!/usr/bin/python3
"""
romcryptor-ui.py
Copyright © 2025-2026 Expl01tHunt3r, collaborators and contributors.

Note: Must use FkrystalLib included in this repository and install PyCryptodome (pip install pycryptodome).
"""
import FkrystalLib as lib
try:
    from Crypto.Cipher import AES
    from Crypto.Util.Padding import pad, unpad
except ImportError:
    lib.tkinter.messagebox.showerror("Error", "Missing library. Please run: pip install pycryptodome")
    lib.sys.exit(1)

MODELS = {
    "-NS": {
        "key": bytes.fromhex("2f52536c386d4d70373073554a506a7841327a54773152377272752f6e673d3d"),
        "iv":  bytes.fromhex("3530397a30567641743057452f573745")
    },
    "-H": {
        "key": bytes.fromhex("774257516156556c4b6d62354e774171394e47325634414d5a41454478513d3d"),
        "iv":  bytes.fromhex("2b6656744e5432514271484d5a7a4f50")
    }
}

MAX_CIPHER_CHUNK = 0x410

def encrypt_stream_chunked(inp_path, out_path, key, iv, stop_event, progress_callback):
    file_size = lib.os.path.getsize(inp_path)
    bytes_processed = 0
    with open(inp_path, "rb") as fin, open(out_path, "wb") as fout:
        cur = fin.read(MAX_CIPHER_CHUNK)
        if len(cur) == 0: return
        while True:
            if stop_event.is_set(): return False
            nxt = fin.read(MAX_CIPHER_CHUNK)
            cipher = AES.new(key, AES.MODE_CBC, iv)
            if nxt:
                if len(cur) % AES.block_size != 0:
                    raise ValueError(f"Input stream error: Chunk size {len(cur)} not aligned.")
                ciphertext = cipher.encrypt(cur)
                fout.write(ciphertext)                
                bytes_processed += len(cur)
                if file_size > 0:
                    progress_callback((bytes_processed / file_size) * 100)
                cur = nxt
            else:
                padded_data = pad(cur, AES.block_size)
                ciphertext = cipher.encrypt(padded_data)
                fout.write(ciphertext)
                progress_callback(100)
                break
    return True

def decrypt_stream_chunked(inp_path, out_path, key, iv, stop_event, progress_callback):
    file_size = lib.os.path.getsize(inp_path)
    bytes_processed = 0
    with open(inp_path, "rb") as fin, open(out_path, "wb") as fout:
        cur = fin.read(MAX_CIPHER_CHUNK)
        if not cur: return
        while True:
            if stop_event.is_set(): return False
            nxt = fin.read(MAX_CIPHER_CHUNK)
            cipher = AES.new(key, AES.MODE_CBC, iv)
            plain = cipher.decrypt(cur)
            if nxt:
                fout.write(plain)
                bytes_processed += len(cur)
                if file_size > 0:
                    progress_callback((bytes_processed / file_size) * 100)
                cur = nxt
            else:
                try:
                    plain = unpad(plain, AES.block_size)
                except ValueError as e:
                    raise ValueError(f"Padding Error (Wrong Key?): {e}")
                fout.write(plain)
                progress_callback(100)
                break
    return True

class RomCryptorUI:
    def __init__(self, root):
        self.root = root
        self.root.title("RomCryptor - Fkrystal")
        self.root.geometry("1000x600")
        self.current_model_name = "-NS"
        self.current_key = MODELS[self.current_model_name]["key"]
        self.current_iv = MODELS[self.current_model_name]["iv"]
        self.toolbar = lib.tkinter.ttk.Frame(root, relief="raised", padding=2)
        self.toolbar.pack(side="top", fill="x")
        lib.tkinter.ttk.Button(self.toolbar, text="Open Directory", command=self.open_directory).pack(side="left", padx=2)
        self.btn_config = lib.tkinter.ttk.Button(self.toolbar, text=f"Keyset: {self.current_model_name}", command=self.open_model_selector)
        self.btn_config.pack(side="left", padx=2)
        lib.tkinter.ttk.Label(self.toolbar, text="  (Double-click file to Process)", font=("Segoe UI", 9, "italic")).pack(side="left", padx=10)
        self.paned = lib.tkinter.ttk.PanedWindow(root, orient="horizontal")
        self.paned.pack(fill="both", expand=True)
        self.sidebar = lib.tkinter.ttk.Frame(self.paned, width=300)
        self.tree = lib.tkinter.ttk.Treeview(self.sidebar)
        self.tree.heading("#0", text="File Explorer", anchor="w")
        self.tree.pack(fill="both", expand=True)
        self.tree.bind("<Double-1>", self.on_tree_double_click)
        self.paned.add(self.sidebar, weight=1)
        self.notebook = lib.tkinter.ttk.Notebook(self.paned)
        self.paned.add(self.notebook, weight=3)

    def open_model_selector(self):
        dialog = lib.tkinter.Toplevel(self.root)
        dialog.title("Encryption Model")
        dialog.geometry("350x150")
        dialog.transient(self.root)
        dialog.grab_set()
        x = self.root.winfo_x() + (self.root.winfo_width() // 2) - 175
        y = self.root.winfo_y() + (self.root.winfo_height() // 2) - 75
        dialog.geometry(f"+{x}+{y}")
        lib.tkinter.Label(dialog, text="Choose Key/IV Set:", font=("Segoe UI", 10)).pack(pady=(15, 5))
        model_names = list(MODELS.keys())
        combo = lib.tkinter.ttk.Combobox(dialog, values=model_names, state="readonly", width=30)
        combo.set(self.current_model_name)
        combo.pack(pady=5)
        def apply_selection():
            new_model = combo.get()
            if new_model in MODELS:
                self.current_model_name = new_model
                self.current_key = MODELS[new_model]["key"]
                self.current_iv = MODELS[new_model]["iv"]
                self.btn_config.config(text=f"Key: {new_model}")
                dialog.destroy()
        lib.tkinter.ttk.Button(dialog, text="Apply", command=apply_selection).pack(pady=15)

    def open_directory(self):
        path = lib.tkinter.filedialog.askdirectory()
        if not path: return
        for item in self.tree.get_children():
            self.tree.delete(item)
        root_node = self.tree.insert("", "end", text=lib.os.path.basename(path), open=True)
        for root_dirs, dirs, files in lib.os.walk(path):
            for file in files:
                full_path = lib.os.path.join(root_dirs, file)
                self.tree.insert(root_node, "end", text=file, values=(full_path,))

    def on_tree_double_click(self, event):
        selection = self.tree.selection()
        if not selection: return
        item_id = selection[0]
        values = self.tree.item(item_id, "values")
        if not values: return
        full_path = values[0]
        filename = lib.os.path.basename(full_path)
        choice = ChoiceDialog(self.root, "Select Action", f"Action for: {filename}\nUsing: {self.current_model_name}", ["Encrypt", "Decrypt"])
        self.root.wait_window(choice.top)
        if not choice.result: return
        mode = choice.result
        suffix = ".enc" if mode == "Encrypt" else ".dec"
        out_path = full_path + suffix
        self.start_processing_task(full_path, out_path, mode, filename)

    def start_processing_task(self, inp_path, out_path, mode, filename):
        self.stop_event = lib.threading.Event()
        self.loading_dialog = lib.tkinter.Toplevel(self.root)
        self.loading_dialog.title(f"{mode}ing...")
        self.loading_dialog.geometry("400x150")
        self.loading_dialog.transient(self.root)
        self.loading_dialog.grab_set()
        x = self.root.winfo_x() + (self.root.winfo_width() // 2) - 200
        y = self.root.winfo_y() + (self.root.winfo_height() // 2) - 75
        self.loading_dialog.geometry(f"+{x}+{y}")
        self.status_label = lib.tkinter.Label(self.loading_dialog, text=f"Starting {mode}...")
        self.status_label.pack(pady=(20, 5))
        self.progress = lib.tkinter.ttk.Progressbar(self.loading_dialog, mode='determinate', length=300)
        self.progress.pack(pady=5)
        lib.tkinter.ttk.Button(self.loading_dialog, text="Cancel", command=self.cancel_processing).pack(pady=10)
        self.thread_result = None
        self.thread_error = None
        t = lib.threading.Thread(target=self._run_heavy_task, args=(inp_path, out_path, mode, self.stop_event, self.current_key, self.current_iv))
        t.daemon = True
        t.start()
        self.root.after(100, self._check_thread_done, t, filename, out_path)

    def _run_heavy_task(self, inp, out, mode, stop_event, key, iv):
        def update_ui(p):
            self.root.after(0, lambda: self._update_progress_bar(p))
        try:
            if mode == "Encrypt":
                success = encrypt_stream_chunked(inp, out, key, iv, stop_event, update_ui)
            else:
                success = decrypt_stream_chunked(inp, out, key, iv, stop_event, update_ui)
            if not success:
                if lib.os.path.exists(out): lib.os.remove(out)
                self.thread_result = "Cancelled"
            else:
                self.thread_result = "Success"
        except Exception as e:
            self.thread_error = str(e)
            if lib.os.path.exists(out): lib.os.remove(out)

    def _update_progress_bar(self, percent):
        if hasattr(self, 'progress') and self.progress.winfo_exists():
            self.progress['value'] = percent
            self.status_label.config(text=f"Processing... {int(percent)}%")

    def cancel_processing(self):
        self.stop_event.set()
        self.status_label.config(text="Cancelling...")

    def _check_thread_done(self, thread, filename, out_path):
        if thread.is_alive():
            self.root.after(100, self._check_thread_done, thread, filename, out_path)
        else:
            if self.loading_dialog.winfo_exists(): self.loading_dialog.destroy()
            if self.thread_error:
                lib.tkinter.messagebox.showerror("Error", f"Operation Failed:\n{self.thread_error}")
            elif self.thread_result == "Success":
                self.create_report_tab(filename, out_path)
            elif self.thread_result == "Cancelled":
                lib.tkinter.messagebox.showinfo("Info", "Operation Cancelled.")

    def create_report_tab(self, original_name, out_path):
        frame = lib.tkinter.ttk.Frame(self.notebook)
        lib.tkinter.Label(frame, text="Operation Completed", font=("Segoe UI", 14, "bold"), fg="green").pack(pady=(20, 10))
        info_text = f"Original File: {original_name}\nOutput File:   {lib.os.path.basename(out_path)}\nModel Used:    {self.current_model_name}"
        lib.tkinter.Label(frame, text=info_text, justify="left", font=("Consolas", 10)).pack(pady=10)
        lib.tkinter.ttk.Button(frame, text="Close Tab", command=lambda: self.notebook.forget(frame)).pack(pady=20)
        self.notebook.add(frame, text=f"Result: {original_name}")
        self.notebook.select(frame)

class ChoiceDialog:
    def __init__(self, parent, title, question, options):
        self.result = None
        self.top = lib.tkinter.Toplevel(parent)
        self.top.title(title)
        self.top.geometry("300x150")
        self.top.transient(parent)
        self.top.grab_set()
        x = parent.winfo_x() + (parent.winfo_width() // 2) - 150
        y = parent.winfo_y() + (parent.winfo_height() // 2) - 75
        self.top.geometry(f"+{x}+{y}")
        lib.tkinter.Label(self.top, text=question, pady=10).pack()
        btn_frame = lib.tkinter.ttk.Frame(self.top)
        btn_frame.pack(fill="x", pady=10)
        for opt in options:
            lib.tkinter.ttk.Button(btn_frame, text=opt, command=lambda o=opt: self.set_choice(o)).pack(side="left", expand=True, padx=5)
    def set_choice(self, choice):
        self.result = choice
        self.top.destroy()

if __name__ == "__main__":
    root = lib.tkinter.Tk(className="FkrysRomCryptor")
    root.iconphoto(True, lib.tkinter.PhotoImage(data=lib.i))
    RomCryptorUI(root)
    root.mainloop()