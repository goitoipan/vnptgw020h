#!/usr/bin/python3
"""
bitreverser-ui.py
Copyright © 2025-2026 Expl01tHunt3r, collaborators and contributors.

Note: Must use FkrystalLib included in this repository.
"""
import FkrystalLib as lib

def invert_file_chunked(filepath, stop_event, progress_callback):
    try:
        file_size = lib.os.path.getsize(filepath)
        chunk_size = 1024 * 1024
        processed_parts = []
        bytes_read = 0
        with open(filepath, "rb") as f:
            while True:
                if stop_event.is_set():
                    return None
                chunk = f.read(chunk_size)
                if not chunk:
                    break
                inverted_chunk = chunk.translate(bytes.maketrans(bytes(range(256)), bytes((x ^ 0xFF) for x in range(256))))
                processed_parts.append(inverted_chunk)
                bytes_read += len(chunk)
                if file_size > 0:
                    percent = (bytes_read / file_size) * 100
                    progress_callback(percent)

        full_bytes = b"".join(processed_parts)
        return full_bytes.decode('utf-8', errors='replace')
    except Exception as e:
        return f"Error: {e}"

class SyntaxHighlighter:
    def __init__(self, text_widget):
        self.txt = text_widget
        self.txt.tag_configure("asp_block", background="#fff9c4")
        self.txt.tag_configure("asp_kw", foreground="#7f0055", font=("Consolas", 11, "bold"))
        self.txt.tag_configure("asp_func", foreground="#000099", font=("Consolas", 11, "italic"))
        self.txt.tag_configure("html_tag", foreground="#0000ff")
        self.txt.tag_configure("html_attr", foreground="#ff0000")
        self.txt.tag_configure("js_kw", foreground="#000033", font=("Consolas", 11, "bold"))
        self.txt.tag_configure("str", foreground="#2a00ff")
        self.txt.tag_configure("com", foreground="#3f7f5f")

    def highlight(self):
        content = self.txt.get("1.0", lib.tkinter.END)
        for tag in ["asp_block", "asp_kw", "asp_func", "html_tag", "html_attr", "js_kw", "str", "com"]:
            self.txt.tag_remove(tag, "1.0", lib.tkinter.END)
        for match in lib.re.finditer(r"<%.*?%>", content, lib.re.DOTALL):
            self.txt.tag_add("asp_block", f"1.0 + {match.start()} chars", f"1.0 + {match.end()} chars")
        for match in lib.re.finditer(r"<[/?]?([a-zA-Z0-9]+).*?>", content):
            self.txt.tag_add("html_tag", f"1.0 + {match.start()} chars", f"1.0 + {match.end()} chars")
        asp_keywords = r"\b(if|then|else|end|for|next|dim|set|request_Form|tcWebApi_get|tcWebApi_set|tcWebApi_commit|asp_Write)\b"
        for match in lib.re.finditer(asp_keywords, content, lib.re.IGNORECASE):
            self.txt.tag_add("asp_kw", f"1.0 + {match.start()} chars", f"1.0 + {match.end()} chars")
        js_keywords = r"\b(function|var|document|getElementById|parseInt|alert|return|eval|window)\b"
        for match in lib.re.finditer(js_keywords, content):
            self.txt.tag_add("js_kw", f"1.0 + {match.start()} chars", f"1.0 + {match.end()} chars")
        for match in lib.re.finditer(r'"[^"]*"', content):
            self.txt.tag_add("str", f"1.0 + {match.start()} chars", f"1.0 + {match.end()} chars")

class BitReverserUI:
    def __init__(self, root):
        self.root = root
        self.root.title("BitReverser - Fkrystal")
        self.root.geometry("1100x700")
        self.toolbar = lib.tkinter.ttk.Frame(root, relief="raised", padding=2)
        self.toolbar.pack(side="top", fill="x")
        lib.tkinter.ttk.Button(self.toolbar, text="Open Folder", command=self.open_directory).pack(side="left", padx=2)
        lib.tkinter.ttk.Button(self.toolbar, text="Save Current", command=self.save_file).pack(side="left", padx=2)
        lib.tkinter.ttk.Button(self.toolbar, text="Close Tab", command=self.close_current_tab).pack(side="left", padx=10)
        lib.tkinter.ttk.Label(self.toolbar, text="  (Double-click file to Process)", font=("Segoe UI", 9, "italic")).pack(side="left", padx=10)
        self.paned = lib.tkinter.ttk.PanedWindow(root, orient="horizontal")
        self.paned.pack(fill="both", expand=True)
        self.sidebar = lib.tkinter.ttk.Frame(self.paned, width=250)
        self.tree = lib.tkinter.ttk.Treeview(self.sidebar)
        self.tree.heading("#0", text="Directory", anchor="w")
        self.tree.pack(fill="both", expand=True)
        self.tree.bind("<Double-1>", self.on_tree_double_click)
        self.paned.add(self.sidebar, weight=1)
        self.notebook = lib.tkinter.ttk.Notebook(self.paned)
        self.paned.add(self.notebook, weight=4)

    def open_directory(self):
        path = lib.tkinter.filedialog.askdirectory()
        if not path:
            return
        for item in self.tree.get_children():
            self.tree.delete(item)
        root_node = self.tree.insert("", "end", text=lib.os.path.basename(path), open=True)
        for root_dirs, dirs, files in lib.os.walk(path):
            for file in files:
                self.tree.insert(root_node, "end", text=file, values=(lib.os.path.join(root_dirs, file),))

    def on_tree_double_click(self, event):
        selection = self.tree.selection()
        if not selection: return
        item_id = selection[0]
        file_path = self.tree.item(item_id, "values")
        if file_path:
            full_path = file_path[0]
            filename = lib.os.path.basename(full_path)
            for tab_id in self.notebook.tabs():
                if self.notebook.tab(tab_id, "text") == filename:
                    self.notebook.select(tab_id)
                    return
            self.stop_event = lib.threading.Event()
            self.loading_dialog = lib.tkinter.Toplevel(self.root)
            self.loading_dialog.title("Processing File")
            self.loading_dialog.geometry("400x150")
            self.loading_dialog.resizable(False, False)
            self.loading_dialog.transient(self.root)
            self.loading_dialog.grab_set()
            x = self.root.winfo_x() + (self.root.winfo_width() // 2) - 200
            y = self.root.winfo_y() + (self.root.winfo_height() // 2) - 75
            self.loading_dialog.geometry(f"+{x}+{y}")
            self.status_label = lib.tkinter.Label(self.loading_dialog, text=f"Reading {filename} (0%)...")
            self.status_label.pack(pady=(20, 5))
            self.progress = lib.tkinter.ttk.Progressbar(self.loading_dialog, mode='determinate', length=300)
            self.progress.pack(pady=5)
            self.indeterminate_progress = lib.tkinter.ttk.Progressbar(self.loading_dialog, mode='indeterminate', length=300)
            btn = lib.tkinter.ttk.Button(self.loading_dialog, text="Cancel", command=self.cancel_processing)
            btn.pack(pady=10)
            self.thread_result = None
            t = lib.threading.Thread(target=self._run_heavy_task, args=(full_path,))
            t.daemon = True
            t.start()
            self.root.after(100, self._check_thread_done, t, filename)

    def _run_heavy_task(self, filepath):
        def update_ui(percent):
            self.root.after(0, lambda: self._update_progress_bar(percent))
        self.thread_result = invert_file_chunked(filepath, self.stop_event, update_ui)

    def _update_progress_bar(self, percent):
        if hasattr(self, 'progress') and self.progress.winfo_exists():
            self.progress['value'] = percent
            self.status_label.config(text=f"Processing... {int(percent)}%")

    def cancel_processing(self):
        self.stop_event.set()
        self.loading_dialog.destroy()

    def _check_thread_done(self, thread, filename):
        if thread.is_alive():
            self.root.after(100, self._check_thread_done, thread, filename)
        else:            
            if self.thread_result is not None:
                if str(self.thread_result).startswith("Error:"):
                    self.loading_dialog.destroy()
                    lib.tkinter.messagebox.showerror("Error", self.thread_result)
                else:
                    if self.loading_dialog.winfo_exists():
                        self.status_label.config(text="Rendering text... (App will freeze)")
                        self.progress.pack_forget()
                        self.indeterminate_progress.pack(pady=5)
                        self.indeterminate_progress.start(5)
                        self.loading_dialog.update()
                    self.create_new_tab(filename, self.thread_result)
                    if self.loading_dialog.winfo_exists():
                        self.loading_dialog.destroy()
            else:
                if self.loading_dialog.winfo_exists():
                    self.loading_dialog.destroy()

    def create_new_tab(self, title, content):
        frame = lib.tkinter.ttk.Frame(self.notebook)
        text_area = lib.tkinter.Text(frame, wrap="none", font=("Consolas", 11), undo=False, maxundo=0)
        text_area.bind("<Control-a>", self.select_all)
        text_area.bind("<Control-A>", self.select_all)
        v_scroll = lib.tkinter.ttk.Scrollbar(frame, orient="vertical", command=text_area.yview)
        h_scroll = lib.tkinter.ttk.Scrollbar(frame, orient="horizontal", command=text_area.xview)
        text_area.configure(yscrollcommand=v_scroll.set, xscrollcommand=h_scroll.set)
        v_scroll.pack(side="right", fill="y")
        h_scroll.pack(side="bottom", fill="x")
        text_area.pack(side="left", fill="both", expand=True)
        text_area.insert("1.0", content)
        if len(content) < 1_000_000:
            highlighter = SyntaxHighlighter(text_area)
            highlighter.highlight()
        text_area.config(state="disabled")
        self.notebook.add(frame, text=title)
        self.notebook.select(frame)

    def close_current_tab(self):
        current = self.notebook.select()
        if current:
            self.notebook.forget(current)

    def select_all(self, event):
        event.widget.tag_add("sel", "1.0", "end")
        return "break"

    def save_file(self):
        current_tab_id = self.notebook.select()
        if not current_tab_id: return
        tab_frame = self.notebook.nametowidget(current_tab_id)
        for child in tab_frame.winfo_children():
            if isinstance(child, lib.tkinter.Text):
                content = child.get("1.0", lib.tkinter.END)
                file_path = lib.tkinter.filedialog.asksaveasfilename()
                if file_path:
                    with open(file_path, "w", encoding="utf-8") as f:
                        f.write(content)
                break

if __name__ == "__main__":
    root = lib.tkinter.Tk(className="FkrysBitReverser")
    root.iconphoto(True, lib.tkinter.PhotoImage(data=lib.i))
    BitReverserUI(root)
    root.mainloop()
