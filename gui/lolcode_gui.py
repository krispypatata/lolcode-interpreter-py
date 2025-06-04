import tkinter as tk
from tkinter import ttk # For tables
from tkinter import filedialog # For opening files
import os
import tkinter.font as tkfont

from tkterminal import Terminal

# ═══════════════════════════════════════════════════════════════════════════════════════════════
class CodeEditor(tk.Frame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent)
        
        # Create line number text widget
        self.lineNumbers = tk.Text(self, width=4, padx=3, takefocus=0,
                                   border=0, state='disabled', wrap='none',
                                   background='#f0f0f0', foreground='#666666')
        
        # Create main text widget
        self.textWidget = tk.Text(self, wrap='none', **kwargs)
        
        # Create scrollbars
        self.verticalScrollbar = ttk.Scrollbar(self, orient='vertical')
        self.horizontalScrollbar = ttk.Scrollbar(self, orient='horizontal')

        # Initialize scrollbars
        self.verticalScrollbar.grid(row=0, column=2, sticky='ns')
        self.horizontalScrollbar.grid(row=1, column=1, sticky='ew')
        
        # Configure scrollbar commands
        self.verticalScrollbar.config(command=self.on_scrollbar)
        self.horizontalScrollbar.config(command=self.textWidget.xview)
        self.textWidget.config(yscrollcommand=self.on_textscroll)
        self.textWidget.config(xscrollcommand=self.horizontalScrollbar.set)
        
        # Grid layout
        self.lineNumbers.grid(row=0, column=0, sticky='ns')
        self.textWidget.grid(row=0, column=1, sticky='nsew')
        
        # Configure grid weights
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        
        # Bind events
        self.textWidget.bind('<Key>', self.on_content_changed)
        self.textWidget.bind('<Button-1>', self.on_left_click)
        self.textWidget.bind('<MouseWheel>', self.on_mousewheel)
        self.textWidget.bind('<Button-3>', self.show_context_menu)  # Right click
        
        # Bind left click to line numbers as well
        self.lineNumbers.bind('<Button-1>', self.on_left_click)
        
        # Keyboard shortcuts
        self.textWidget.bind('<Control-c>', self.copy_text)
        self.textWidget.bind('<Control-x>', self.cut_text)
        self.textWidget.bind('<Control-v>', self.paste_text)
        self.textWidget.bind('<Control-a>', self.select_all)
        
        # Initialize line numbers
        self.update_line_numbers()
        
        # Create context menu
        self.contextMenu = tk.Menu(self, tearoff=0)
        self.contextMenu.add_command(label="Copy", command=self.copy_text, accelerator="Ctrl+C")
        self.contextMenu.add_command(label="Cut", command=self.cut_text, accelerator="Ctrl+X")
        self.contextMenu.add_command(label="Paste", command=self.paste_text, accelerator="Ctrl+V")
        self.contextMenu.add_separator()
        self.contextMenu.add_command(label="Select All", command=self.select_all_menu, accelerator="Ctrl+A")

        # Bind mouse click outside the context menu (right click menu) to hide it (so it doesn't stay open)
        root.bind('<Button-1>', self.hide_context_menu)

    def on_scrollbar(self, *args):
        """Handle vertical scrollbar movement"""
        self.textWidget.yview(*args)
        self.lineNumbers.yview(*args)
    
    def on_textscroll(self, *args):
        """Handle text widget scrolling"""
        self.verticalScrollbar.set(*args)
        self.lineNumbers.yview_moveto(args[0])
    
    def on_mousewheel(self, event):
        """Handle mouse wheel scrolling"""
        self.lineNumbers.yview_scroll(int(-1 * (event.delta / 120)), "units")
    
    def on_left_click(self, event=None):
        """Handle left click events"""
        self.hide_context_menu()
        self.after_idle(self.update_line_numbers)
    
    def on_content_changed(self, event=None):
        """Handle content changes"""
        self.after_idle(self.update_line_numbers)
    
    def update_line_numbers(self):
        """Update line numbers display"""
        self.lineNumbers.config(state='normal')
        self.lineNumbers.delete('1.0', tk.END)
        
        # Get number of lines in text widget
        end_line = int(self.textWidget.index(tk.END).split('.')[0])
        
        # Generate line numbers
        lineNumbersText = '\n'.join(str(i) for i in range(1, end_line))
        self.lineNumbers.insert('1.0', lineNumbersText)
        
        self.lineNumbers.config(state='disabled')

    def show_context_menu(self, event):
        """Show right-click context menu"""
        try:
            self.contextMenu.tk_popup(event.x_root, event.y_root)

        finally:
            self.contextMenu.grab_release()

        
    def hide_context_menu(self, event=None):
        """Hide context menu"""
        try:
            self.contextMenu.unpost()
        except:
            pass

        # Prevent context menu from appearing when clicking outside the code editor
        if event and event.widget not in (self.textWidget, self.lineNumbers):
            return
        return "break"
    
    def copy_text(self, event=None):
        """Copy selected text"""
        try:
            self.textWidget.event_generate("<<Copy>>")
        except tk.TclError:
            pass
        return "break"
    
    def cut_text(self, event=None):
        """Cut selected text"""
        try:
            self.textWidget.event_generate("<<Cut>>")
            self.update_line_numbers()
        except tk.TclError:
            pass
        return "break"
    
    def paste_text(self, event=None):
        """Paste text"""
        try:
            self.textWidget.event_generate("<<Paste>>")
            self.update_line_numbers()
        except tk.TclError:
            pass
        return "break"
    
    def select_all(self, event=None):
        """Select all text (keyboard shortcut)"""
        self.textWidget.tag_add(tk.SEL, "1.0", tk.END)
        self.textWidget.mark_set(tk.INSERT, "1.0")
        self.textWidget.see(tk.INSERT)
        return "break"
    
    def select_all_menu(self):
        """Select all text (menu command)"""
        self.select_all()
    
    def get(self, start, end=None):
        """Get text content"""
        return self.textWidget.get(start, end)
    
    def insert(self, index, text):
        """Insert text"""
        self.textWidget.insert(index, text)
        self.update_line_numbers()
    
    def delete(self, start, end=None):
        """Delete text"""
        self.textWidget.delete(start, end)
        self.update_line_numbers()

# ───────────────────────────────────────────────────────────────────────────────────────────────
# Class for tooltips for tables
# Functionality: If the text in a cell is longer than the column width, a tooltip will appear when hovering over the cell
class TreeviewTooltip:
    def __init__(self, treeview):
        self.treeview = treeview
        self.tooltip = None
        self.current_item = None
        self.current_column = None
        self.treeview.bind('<Motion>', self._on_motion)
        self.treeview.bind('<Leave>', self._hide_tooltip)
        
    def _on_motion(self, event):
        # Get the item and column under the cursor
        item = self.treeview.identify_row(event.y)
        column = self.treeview.identify_column(event.x)
        
        # Check if we've moved to a different cell
        if item != self.current_item or column != self.current_column:
            # Hide current tooltip since we've moved to a different cell
            self._hide_tooltip()
            
            # Update current position
            self.current_item = item
            self.current_column = column
            
            if item and column:
                # Get column index (tkinter uses 1-based indexing for columns)
                columnIndex = int(column.replace('#', '')) - 1
                
                # Get the text in the cell
                values = self.treeview.item(item, 'values')
                if columnIndex < len(values):
                    text = str(values[columnIndex])
                    
                    # Get column width
                    col_name = self.treeview['columns'][columnIndex]
                    col_width = self.treeview.column(col_name, 'width')
                    
                    # Check if text is longer than what can fit in the column
                    # Use default font
                    font = tkfont.nametofont("TkDefaultFont")
                    text_width = font.measure(text)
                    
                    if text_width > col_width - 10:  # (-10) for padding
                        self._show_tooltip(event, text)
        elif self.tooltip:
            # We're in the same cell but cursor moved - update tooltip position
            self._update_tooltip_position(event)
    
    def _show_tooltip(self, event, text):
        if self.tooltip:
            self.tooltip.destroy()
            
        # Create a tooltip window
        self.tooltip = tk.Toplevel(self.treeview)
        self.tooltip.wm_overrideredirect(True)
        
        # Initially place the tooltip window outside the screen (not visible to the users) - this is to fix flickering issues
        self.tooltip.wm_geometry(f"+{-1000}+{-1000}")
        
        self.tooltip.configure(bg='lightyellow', relief='solid', borderwidth=1)
        label = tk.Label(self.tooltip, text=text, bg='lightyellow', 
                         wraplength=300, justify='left', font=('TkDefaultFont', 10))
        label.pack(padx=2, pady=1)
        
        # Update the tooltip to get actual dimensions
        self.tooltip.update_idletasks()
        tooltip_height = self.tooltip.winfo_reqheight()
        
        # Calculate final position
        x_pos = event.x_root + 10
        y_pos = event.y_root - tooltip_height - 5  # offset above cursor
        
        # Move tooltip to final position
        self.tooltip.wm_geometry(f"+{x_pos}+{y_pos}")
        
        # Make tooltip visible
        self.tooltip.deiconify()
        
    def _update_tooltip_position(self, event):
        """Update tooltip position to follow cursor within the same cell"""
        if self.tooltip:
            # Get tooltip dimensions
            tooltip_height = self.tooltip.winfo_reqheight()
            
            # Calculate new position
            x_pos = event.x_root + 10
            y_pos = event.y_root - tooltip_height - 5  # offset above cursor
            
            # Move tooltip to new position
            self.tooltip.wm_geometry(f"+{x_pos}+{y_pos}")
    
    def _hide_tooltip(self, event=None):
        if self.tooltip:
            self.tooltip.destroy()
            self.tooltip = None
        # Reset current position tracking
        self.current_item = None
        self.current_column = None

# ───────────────────────────────────────────────────────────────────────────────────────────────
# Function to choose a file and load its content into the code editor
def choose_file(fileChooserButton, codeEditor):
    """Open a file dialog to choose a LOLCODE file and load its content into the code editor."""
    fileTypes = [
        ("LOLCODE files", "*.lol"),
        ("All files", "*.*"),
    ]
    filePath = filedialog.askopenfilename(
        title="Open file",
        filetypes=fileTypes,
        defaultextension=".lol"
    )
    if filePath:
        filename = os.path.basename(filePath)
        fileChooserButton.config(text=filename) 
        try:
            with open(filePath, "r", encoding="utf-8") as f:
                content = f.read()
            codeEditor.textWidget.delete("1.0", tk.END)
            codeEditor.textWidget.insert("1.0", content)
            codeEditor.update_line_numbers()
        except Exception as e:
            print(f"Failed to open file: {e}")

# ───────────────────────────────────────────────────────────────────────────────────────────────
# Function to update the contents of a table (tree) with new data
def update_table_contents(table, data):
    """
        Update the contents of a table (tree) with new data.
        Data are expected to be a list of tuples, where each tuple represents a row.
    """
    # Clear existing data
    for item in table.get_children():
        table.delete(item)
    
    # Insert new data
    for row in data:
        table.insert("", "end", values=row)

# ───────────────────────────────────────────────────────────────────────────────────────────────
# Function for popping up a window to get user input
def get_user_input():
    def clear_input():
        userInput.delete(0, tk.END)

    def submit_input():
        nonlocal result
        result = userInput.get()
        popup.destroy()

    result = None
    popup = tk.Toplevel(root)
    popup.title("User Input")
    popup.resizable(False, False)  # Prevent window resizing and maximizing
    popup.grab_set()  # Make popup modal

    tk.Label(popup, text="Enter something:").pack(pady=10)

    userInput = tk.Entry(popup, 
                        #  width=30  # Optional (to widen the entire popup window)
                         )
    userInput.pack(padx=10, pady=5, fill="x")

    buttonFrame = tk.Frame(popup)
    buttonFrame.pack(pady=10)

    clearBtn = tk.Button(buttonFrame, text="Clear", command=clear_input)
    clearBtn.pack(side="left", padx=10, ipadx=5, ipady=5)

    submitBtn = tk.Button(buttonFrame, text="Submit", command=submit_input)
    submitBtn.pack(side="left", padx=10, ipadx=5, ipady=5)

    popup.wait_window()  # Wait until popup closes
    return result

# ───────────────────────────────────────────────────────────────────────────────────────────────
# Function to generate dummy data for tables
def generate_dummy_date_for_tables():
    sample_data = []
    for i in range(20):
        sample_data.append((f"lexLONGTEXTEXAMPLE{i}", f"Additional Parameter Variable{i%3}", i+1))
    
    update_table_contents(lexemeTree, sample_data)

    sample_data = []
    for i in range(20):
        sample_data.append((f"symbolsymbol{i}", f"value{i}"))

    update_table_contents(symbolTree, sample_data)


# ═══════════════════════════════════════════════════════════════════════════════════════════════
root = tk.Tk()
root.title("LOLCODE Interpreter")

MIN_WIDTH = 1280 # Preferrably divisible by 5
MIN_HEIGHT = 720 
TABLE_VIEWS_FIXED_WIDTH = (MIN_WIDTH * 2) // 4  # Fixed width for table views

# Set minimum size
root.minsize(MIN_WIDTH, MIN_HEIGHT)
root.geometry(f"{MIN_WIDTH}x{MIN_HEIGHT}") # Window size on launch

# ───────────────────────────────────────────────────────────────────────────────────────────────
# Create frames for different areas of the GUI and add them to the root (window)
# Top and bottom views should equally occupy the available space, whereas the center view should have a fixed height
topView = tk.Frame(root)
centerView = tk.Frame(root, height=50) 
bottomView = tk.Frame(root)

root.grid_rowconfigure(0, weight=1)  # Top view
root.grid_rowconfigure(1, weight=0)  # Center view
root.grid_rowconfigure(2, weight=1)  # Bottom view
root.grid_columnconfigure(0, weight=1)

topView.grid(row=0, column=0, sticky="nsew")
centerView.grid(row=1, column=0, sticky="ew")
centerView.grid_propagate(False) 
bottomView.grid(row=2, column=0, sticky="nsew")
# ═══════════════════════════════════════════════════════════════════════════════════════════════
# Top view
topView.columnconfigure(0, weight=1)
topView.columnconfigure(1, weight=0, minsize=TABLE_VIEWS_FIXED_WIDTH)
topView.rowconfigure(0, weight=1)
# ───────────────────────────────────────────────────────────────────────────────────────────────
# Left side
codeEditorView = tk.Frame(topView)
codeEditorView.grid(row=0, column=0, sticky="nsew")

# Grid configuration for the code editor view (top = file chooser, bottom = code editor)
codeEditorView.columnconfigure(0, weight=1)
codeEditorView.rowconfigure(0, weight=0)
codeEditorView.rowconfigure(1, weight=1)

# Bottom (code editor)
codeEditor = CodeEditor(codeEditorView, background="white")
codeEditor.grid(row=1, column=0, sticky="nsew")

# Top (file chooser)
# Wrap in a frame to for ce the button to have a fixed height
fileChooserFrame = tk.Frame(codeEditorView, height=27)
fileChooserFrame.grid(row=0, column=0, sticky="ew")
fileChooserFrame.grid_propagate(False)  # Prevent resizing

fileChooserButton = tk.Button(fileChooserFrame, text="Open LOLCODE file", 
                            #   command=lambda: choose_file(fileChooserButton, codeEditor),
                            command=get_user_input, # For testing purposes 
                              anchor="w")
fileChooserButton.place(x=0, y=0, relwidth=1, relheight=1)

# ───────────────────────────────────────────────────────────────────────────────────────────────
# Right side
tableViews = tk.Frame(topView)
tableViews.grid(row=0, column=1, sticky="ns")

tableViews.columnconfigure(0, weight=3)
tableViews.columnconfigure(1, weight=2)
tableViews.rowconfigure(0, weight=1)

# -----------------------------------------------------------------------------------------------
# Left side of the right side
lexemeTableView = tk.Frame(tableViews)
lexemeTableView.grid(row=0, column=0, sticky="nsew")

lexemeTableLabel = tk.Label(lexemeTableView, text="Lexeme Table")
lexemeTableLabel.pack(fill="x")

lexemeColumns = ("Lexeme", "Classification", "Line #")
lexemeTree = ttk.Treeview(lexemeTableView, columns=lexemeColumns, show="headings", height=10)

# Format column widths
LEXEME_TABLE_WIDTH = (TABLE_VIEWS_FIXED_WIDTH * 3) // 5

# First column
lexemeTree.heading(lexemeColumns[0], text=lexemeColumns[0])
lexemeTree.column(lexemeColumns[0], width=int(LEXEME_TABLE_WIDTH * 2 / 5), anchor="w")

# Second column
lexemeTree.heading(lexemeColumns[1], text=lexemeColumns[1])
lexemeTree.column(lexemeColumns[1], width=int(LEXEME_TABLE_WIDTH * 2 / 5), anchor="w")

# Third column
lexemeTree.heading(lexemeColumns[2], text=lexemeColumns[2])
lexemeTree.column(lexemeColumns[2], width=int(LEXEME_TABLE_WIDTH * 1 / 5), anchor="center")

lexemeScrollbar = ttk.Scrollbar(lexemeTableView, orient="vertical", command=lexemeTree.yview)
lexemeTree.configure(yscrollcommand=lexemeScrollbar.set)

lexemeTree.pack(side="left", fill="both", expand=True)
lexemeScrollbar.pack(side="right", fill="y")

# Add tooltip functionality to the lexeme table
lexemeTooltip = TreeviewTooltip(lexemeTree)

# -----------------------------------------------------------------------------------------------
# Right side of the right side
symbolTableView = tk.Frame(tableViews)
symbolTableView.grid(row=0, column=1, sticky="nsew")

symbolTableLabel = tk.Label(symbolTableView, text="Symbol Table")
symbolTableLabel.pack(fill="x")

symbolColumns = ("Symbol", "Value")
symbolTree = ttk.Treeview(symbolTableView, columns=symbolColumns, show="headings", height=10)

# Format column widths
SYMBOL_TABLE_WIDTH = (TABLE_VIEWS_FIXED_WIDTH * 2) // 5

# First column
symbolTree.heading(symbolColumns[0], text=symbolColumns[0])
symbolTree.column(symbolColumns[0], width=int(SYMBOL_TABLE_WIDTH / 2), anchor="w")

# Second column
symbolTree.heading(symbolColumns[1], text=symbolColumns[1])
symbolTree.column(symbolColumns[1], width=int(SYMBOL_TABLE_WIDTH / 2), anchor="w")

symbolScrollbar = ttk.Scrollbar(symbolTableView, orient="vertical", command=symbolTree.yview)
symbolTree.configure(yscrollcommand=symbolScrollbar.set)

symbolTree.pack(side="left", fill="both", expand=True)
symbolScrollbar.pack(side="right", fill="y")

# Add tooltip functionality to the symbol table
symbolTooltip = TreeviewTooltip(symbolTree)
# ═══════════════════════════════════════════════════════════════════════════════════════════════
# Center view
executeButton = tk.Button(centerView, text="Execute", command=lambda: print("Executing..."))
executeButton.pack(fill = "both", expand=True, padx=5, pady=5)

# ═══════════════════════════════════════════════════════════════════════════════════════════════
# Bottom view
console = Terminal(bottomView)
console.pack(fill="both", expand=True)

# ───────────────────────────────────────────────────────────────────────────────────────────────
generate_dummy_date_for_tables()


root.mainloop()