import tkinter
BG_COLOR = '#28282e'
FG_COLOR = '#cac5c4'

resolve.OpenPage("fusion") # useable as Utility script and Tool script both on "fusion" and "edit"/"cut"

try:
    if not tool:
        tool = comp.ActiveTool
except NameError:
    tool = comp.ActiveTool
    # this captures both if tool is not in namespace or tool = None

if not tool.StyledText:
    from sys import exit
    err_root = tkinter.Tk()
    err_root.title("Nizar's Word Wrapper for DaVinci Resolve")

    err_root.configure(background=BG_COLOR)
    
    lbl_err_msg = tkinter.Label(err_root, text="'Word Wrapper' can only be used on Fusion nodes with a Text input field.", bg=BG_COLOR, fg=FG_COLOR)
    lbl_err_msg.grid(row=0, column=0, sticky="W", padx=20, pady=10)
    err_root.mainloop()
    
    exit("'Word Wrapper' can only be used on Fusion nodes with a Text input field.")

def set_node_text(new_text):
    tool.StyledText[0] = new_text

def get_node_text():
    return tool.StyledText[0]


def break_text_by_chars(text, max_width):
    new_text = []
    ptr = 0
    while ptr < len(text):
        new_text.append(text[ptr:ptr+max_width])
        ptr += max_width
    return "\n".join(new_text)

def break_text_by_words(text, max_width):
    result = []
    current_line = ""
    
    for word in text.split():
        if len(current_line) + len(word) + 1 > max_width:
            # If adding the word exceeds maxWidth, start a new line
            result.append(current_line)
            current_line = word
        else:
            # Otherwise, add the word to the current line
            if len(current_line) > 0:
                current_line = current_line + " " + word
            else:
                current_line = word
                
    # Add last line
    if len(current_line) > 0:
        result.append(current_line)
    
    return "\n".join(result)

node_text = get_node_text()
original_node_text = node_text


# GUI

def gui_update_node(_ev, update_text_from_node=True):
    global node_text
    keep_words = var_keep_words.get()
    if update_text_from_node:
        node_text = get_node_text()#.replace("\n", " ")
    max_width = scl_width_scale.get()
    if keep_words:
        set_node_text(break_text_by_words(node_text, max_width))
    else:
        set_node_text(break_text_by_chars(node_text, max_width))

def gui_update_supertext_label():
    if var_keep_words.get():
        lbl_super_text.config(text=f"Word Wrapping for '{tool.GetAttrs('TOOLS_Name')}' node\nMax. words per line:")
    else:
        lbl_super_text.config(text=f"Word Wrapping for '{tool.GetAttrs('TOOLS_Name')}' node\nMax. characters per line:")
    gui_update_node(None, update_text_from_node=False)
        
def gui_reset_node_text():
    node_text = original_node_text
    set_node_text(original_node_text)

root = tkinter.Tk()
root.title("Nizar's Word Wrapper for DaVinci Resolve")
root.configure(background=BG_COLOR)

var_keep_words = tkinter.BooleanVar()

lbl_super_text = tkinter.Label(root, text=f"Word Wrapping for '{tool.GetAttrs('TOOLS_Name')}' node\nMax. words per line:", bg=BG_COLOR, fg=FG_COLOR, justify=tkinter.LEFT)
lbl_super_text.grid(row=0, column=0, sticky="W", padx=20, pady=10)

scl_width_scale = tkinter.Scale(root, bg=BG_COLOR, fg=FG_COLOR, orient=tkinter.HORIZONTAL, command=gui_update_node, from_=1, to=len(node_text))
scl_width_scale.grid(row=1, column=0, sticky="W", padx=20, pady=10)

btn_keep_words = tkinter.Checkbutton(root, text='Keep Words', variable=var_keep_words, onvalue=True, offvalue=False, command=gui_update_supertext_label, anchor="w", bg=BG_COLOR, activebackground = BG_COLOR, highlightbackground = "gray", highlightthickness=2, fg="gray")
btn_keep_words.select()
btn_keep_words.grid(row=2, column=1, sticky="W", padx=20, pady=10)

btn_reset = tkinter.Button(root, text="Restore original text", padx=50, command=gui_reset_node_text)
btn_reset.grid(row=3, column=1, sticky="W", padx=20, pady=10)

root.mainloop()
