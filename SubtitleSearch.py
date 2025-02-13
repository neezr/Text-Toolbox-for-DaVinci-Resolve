timeline = resolve.GetProjectManager().GetCurrentProject().GetCurrentTimeline()

node_timecodes = []
node_texts = []
timecode2text = dict()

for i in range(1, timeline.GetTrackCount("subtitle")+1):
    for tl_item in timeline.GetItemListInTrack("subtitle", i):
        timecode = tl_item.GetStart()
        text = tl_item.GetName()
        
        node_timecodes.append(timecode)
        node_texts.append(text)
        timecode2text[timecode] = text
        
def word_match(w1, w2, case_sensitive=False):
    if case_sensitive:
        return w1 in w2
    else:
        return w1.lower() in w2.lower()

def search(substr, case_sensitive=False) -> list:
    results = []
    for text, timecode in zip(node_texts, node_timecodes):
        if word_match(substr, text, case_sensitive):
            results.append(timecode)
    return results
    
def format_timecode_from_frames(timecode_in_frames: int) -> str:
    #return str(timecode_in_frames)
    
    frame_rate = round(float(timeline.GetSetting("timelineFrameRate")))
    
    frames = timecode_in_frames % frame_rate
    seconds = (timecode_in_frames // frame_rate) % 60
    minutes = ((timecode_in_frames // frame_rate) // 60) % 60
    hours = ((timecode_in_frames // frame_rate) // 60) // 60
    
    return f"{hours:02}:{minutes:02}:{seconds:02}:{frames:02}"    


# GUI

import tkinter

search_results = []

def gui_update_search_results():
    global search_results
    query = fld_search_bar.get()
    search_results = search(query)
    
    lbx_search_results.config(height = len(search_results) + 1)
    
    lbx_search_results.delete(0, tkinter.END)
    for result in search_results:
        search_repr = format_timecode_from_frames(result) + ": " + timecode2text.get(result, "")
        lbx_search_results.insert(tkinter.END, search_repr)
    
    
def gui_jump_to_tl_item(ev):
    global search_results
    selected_idx = lbx_search_results.curselection()[0]
    selected_timecode = format_timecode_from_frames(search_results[selected_idx])
    timeline.SetCurrentTimecode(selected_timecode)


root = tkinter.Tk()
root.title("Nizar's Subtitle Search for DaVinci Resolve")
BG_COLOR = '#28282e'
FG_COLOR = '#cac5c4'
root.configure(background=BG_COLOR)

fld_search_bar = tkinter.Entry(root, width=50)
fld_search_bar.grid(row=0,column=0, sticky="W", padx=20, pady=50)
btn_search_button = tkinter.Button(root, text="Search", padx=50, command=gui_update_search_results)
btn_search_button.grid(row=0,column=1, sticky="W", padx=20, pady=50)

lbx_search_results = tkinter.Listbox(root, width=50, height=1, bg=BG_COLOR, fg=FG_COLOR)
lbx_search_results.grid(row=1,column=0, sticky="W", padx=(20, 50), pady=(60,10))
lbx_search_results.bind('<Double-1>', gui_jump_to_tl_item) 

root.mainloop()
