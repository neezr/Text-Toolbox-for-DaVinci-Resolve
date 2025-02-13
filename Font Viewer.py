# ~ Font Viewer ~
# created by nizar / version 1.0
# contact: http://twitter.com/nizarneezR

# Usage:
# Execute this script from DaVinci Resolve's dropdown menu (Workspace > Scripts)
# A window will open, showing you all fonts used in your projects and if these fonts are installed to your system. 
# Use the copy buttons to copy a list of your projects fonts (all or uninstalled) to your clipboard
# Note: Legacy Text (not Text+) are sadly not supported by this script, because they are not callable from the API

# Install:
# Copy this .py-file into the folder "%appdata%\Blackmagic Design\DaVinci Resolve\Support\Fusion\Scripts\Utility"

try:
    bmd.openurl
except AttributeError:
    import webbrowser

project = resolve.GetProjectManager().GetCurrentProject()

def get_installed_fonts():
    return set(fusion.FontManager.GetFontList().keys())
    
def get_used_fonts():
    used_fonts = set()
    
    for i in range(1, project.GetTimelineCount()+1):
        timeline = project.GetTimelineByIndex(i)
        for j in range(1, timeline.GetTrackCount("video")+1):
            for tl_item in timeline.GetItemListInTrack("video", j):
                for k in range(1, tl_item.GetFusionCompCount()+1):
                    comp = tl_item.GetFusionCompByIndex(k)
                    for node in comp.GetToolList().values():
                        if node.Font: #if node has font option, get font
                            used_fonts.add(node.Font[1])
    return used_fonts

used_fonts = list(get_used_fonts())
installed_fonts = get_installed_fonts()

# DEBUG: Add a non-existing font for testing.
# used_fonts.append("Test Font") # TODO remove


# GUI

import tkinter as tk

def open_font_in_google_fonts(ev):
    try:
        if list_box_left.curselection():
            selected_font_index = list_box_left.curselection()[0]
        if list_box_right.curselection():
            selected_font_index = list_box_right.curselection()[0]
        try:
            bmd.openurl("https://fonts.google.com/?query=" + used_fonts[selected_font_index])
        except AttributeError:
            webbrowser.open("https://fonts.google.com/?query=" + used_fonts[selected_font_index])
    except Exception as e:
        print("Could not open Google Fonts in your browser. Error:", e)

def gui_copy_all_to_clipboard():
    copy_text = "\n".join(used_fonts)
    
    root.clipboard_clear()
    root.clipboard_append(copy_text)
    
def gui_copy_uninstalled_to_clipboard():
    copy_text = "\n".join([f for f in used_fonts if not f in installed_fonts])
    
    root.clipboard_clear()
    root.clipboard_append(copy_text)

root = tk.Tk()
root.title("Nizar's Font Viewer")
BG_COLOR = '#28282e'
FG_COLOR = '#cac5c4'
root.configure(background=BG_COLOR)

list_box_height = len(used_fonts)+2

list_box_left = tk.Listbox(root, width=25, height=list_box_height, bg=BG_COLOR, fg=FG_COLOR)
list_box_left.grid(row=0,column=0, sticky="W", padx=20, pady=(60,10))
for f in used_fonts:
    list_box_left.insert(tk.END, f)
list_box_left.bind('<Double-1>', open_font_in_google_fonts) 
    
list_box_right = tk.Listbox(root, width=25, height=list_box_height, bg=BG_COLOR, fg=FG_COLOR)
list_box_right.grid(row=0,column=1, sticky="W", padx=(0,20), pady=(60,10))
for f in used_fonts:
    if f in installed_fonts:
        list_box_right.insert(tk.END, "Installed!")
    else:
        list_box_right.insert(tk.END, "Not installed!")
list_box_right.bind('<Double-1>', open_font_in_google_fonts) 

button_copy_all = tk.Button(root, text="Copy all fonts\n to clipboard", padx=50, command=gui_copy_all_to_clipboard)
button_copy_all.grid(row=1,column=0, sticky="W", padx=0, pady=10)

button_copy_uninstalled = tk.Button(root, text="Copy uninstalled fonts\n to clipboard", padx=50, command=gui_copy_uninstalled_to_clipboard)
button_copy_uninstalled.grid(row=1,column=1, sticky="W", padx=0, pady=10)

root.mainloop()
