#!/usr/bin/python3
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
import re

def invert_file_logic(input_path):
    try:
        with open(input_path, "rb") as f:
            data = f.read()
        return bytes((b ^ 0xFF) for b in data).decode('utf-8', errors='replace')
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
        content = self.txt.get("1.0", tk.END)
        for tag in ["asp_block", "asp_kw", "asp_func", "html_tag", "html_attr", "js_kw", "str", "com"]:
            self.txt.tag_remove(tag, "1.0", tk.END)
        for match in re.finditer(r"<%.*?%>", content, re.DOTALL):
            self.txt.tag_add("asp_block", f"1.0 + {match.start()} chars", f"1.0 + {match.end()} chars")
        for match in re.finditer(r"<[/?]?([a-zA-Z0-9]+).*?>", content):
            self.txt.tag_add("html_tag", f"1.0 + {match.start()} chars", f"1.0 + {match.end()} chars")
        asp_keywords = r"\b(if|then|else|end|for|next|dim|set|request_Form|tcWebApi_get|tcWebApi_set|tcWebApi_commit|asp_Write)\b"
        for match in re.finditer(asp_keywords, content, re.IGNORECASE):
            self.txt.tag_add("asp_kw", f"1.0 + {match.start()} chars", f"1.0 + {match.end()} chars")
        js_keywords = r"\b(function|var|document|getElementById|parseInt|alert|return|eval|window)\b"
        for match in re.finditer(js_keywords, content):
            self.txt.tag_add("js_kw", f"1.0 + {match.start()} chars", f"1.0 + {match.end()} chars")
        for match in re.finditer(r'"[^"]*"', content):
            self.txt.tag_add("str", f"1.0 + {match.start()} chars", f"1.0 + {match.end()} chars")

class ASPDecompilerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("VNPT ASP Decoder - Fkrystal")
        self.root.geometry("1100x700")

        self.toolbar = ttk.Frame(root, relief="raised", padding=2)
        self.toolbar.pack(side="top", fill="x")
        
        ttk.Button(self.toolbar, text="Open Folder", command=self.open_directory).pack(side="left", padx=2)
        ttk.Button(self.toolbar, text="Save Current", command=self.save_file).pack(side="left", padx=2)
        ttk.Button(self.toolbar, text="Close Tab", command=self.close_current_tab).pack(side="left", padx=10)


        self.paned = ttk.PanedWindow(root, orient="horizontal")
        self.paned.pack(fill="both", expand=True)

        self.sidebar = ttk.Frame(self.paned, width=250)
        self.tree = ttk.Treeview(self.sidebar)
        self.tree.heading("#0", text="Directory", anchor="w")
        self.tree.pack(fill="both", expand=True)
        self.tree.bind("<Double-1>", self.on_tree_double_click)
        self.paned.add(self.sidebar, weight=1)

        self.notebook = ttk.Notebook(self.paned)
        self.paned.add(self.notebook, weight=4)

    def open_directory(self):
        path = filedialog.askdirectory()
        if not path:
            return

        for item in self.tree.get_children():
            self.tree.delete(item)

        root_node = self.tree.insert("", "end", text=os.path.basename(path), open=True)
        
        for root_dirs, dirs, files in os.walk(path):
            for file in files:
                if file.lower().endswith(".asp"):
                    full_path = os.path.join(root_dirs, file)
                    self.tree.insert(root_node, "end", text=file, values=(full_path,))

    def on_tree_double_click(self, event):
        item_id = self.tree.selection()[0]
        file_path = self.tree.item(item_id, "values")
        
        if file_path:
            full_path = file_path[0]
            filename = os.path.basename(full_path)
            
            for tab_id in self.notebook.tabs():
                if self.notebook.tab(tab_id, "text") == filename:
                    self.notebook.select(tab_id)
                    return

            content = invert_file_logic(full_path)
            self.create_new_tab(filename, content)

    def create_new_tab(self, title, content):
        frame = ttk.Frame(self.notebook)
        text_area = tk.Text(frame, wrap="none", font=("Consolas", 11))

        text_area.bind("<Control-a>", self.select_all)
        text_area.bind("<Control-A>", self.select_all)

        v_scroll = ttk.Scrollbar(frame, orient="vertical", command=text_area.yview)
        h_scroll = ttk.Scrollbar(frame, orient="horizontal", command=text_area.xview)
        text_area.configure(yscrollcommand=v_scroll.set, xscrollcommand=h_scroll.set)

        v_scroll.pack(side="right", fill="y")
        h_scroll.pack(side="bottom", fill="x")
        text_area.pack(side="left", fill="both", expand=True)

        text_area.insert("1.0", content)
        
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
            if isinstance(child, tk.Text):
                content = child.get("1.0", tk.END)
                file_path = filedialog.asksaveasfilename(defaultextension=".asp")
                if file_path:
                    with open(file_path, "w", encoding="utf-8") as f:
                        f.write(content)
                break

if __name__ == "__main__":
    root = tk.Tk()
    app = ASPDecompilerGUI(root)
    root.mainloop()
