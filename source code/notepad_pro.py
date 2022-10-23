#Notepad Pro

from argparse import FileType
from cProfile import label
from cgitb import text
from dataclasses import replace
from mailbox import mbox
from textwrap import fill
import tkinter as tk
from tkinter import Grid, StringVar, ttk
from tkinter import font,colorchooser,filedialog,messagebox
import os
from unicodedata import name
from click import command
from soupsieve import match

'''DEFINING FUNCTIONS'''

def change_word(event=None):
    global text_change,text_url
    if text_editor.edit_modified():
        text_change = True
        word=len(text_editor.get(1.0,"end-1c").split())
        character=len(text_editor.get(1.0,"end-1c").replace(" ",""))
        status_bar.config(text=f"CHARACTER :{character} WORD :{word}")
    text_editor.edit_modified(False)
    if text_url==None:
        main_app.title(f"untitled* - NOTEPAD_PRO")
    else:
        main_app.title(f"{os.path.basename(text_url)}* - NOTEPAD_PRO")

def change_font(main_app):
    global font_now
    font_now=font_family.get()
    text_editor.configure(font=(font_now,font_size_now))

def change_font_size(main_app):
    global font_size_now
    font_size_now=size_var.get()
    text_editor.configure(font=(font_now,font_size_now))

def bold():
    text_get=tk.font.Font(font=text_editor["font"])
    if text_get.actual()["weight"] == "normal":
        text_editor.configure(font=(font_now,font_size_now,"bold"))
    else:
        text_editor.configure(font=(font_now,font_size_now,"normal"))

def italic():
    text_get=tk.font.Font(font=text_editor["font"])
    if text_get.actual()["slant"] == "roman":
        text_editor.configure(font=(font_now,font_size_now,"italic"))
    else:
        text_editor.configure(font=(font_now,font_size_now,"roman"))

def underline():
    text_get=tk.font.Font(font=text_editor["font"])
    if text_get.actual()["underline"] == 0:
        text_editor.configure(font=(font_now,font_size_now,"underline"))
    else:
        text_editor.configure(font=(font_now,font_size_now,"normal"))

def color():
    color_var=tk.colorchooser.askcolor()
    text_editor.configure(fg=color_var[1])

def left_align():
    text_get=text_editor.get(1.0,"end")
    text_editor.tag_config("left",justify=tk.LEFT)
    text_editor.delete(1.0,tk.END)
    text_editor.insert(tk.INSERT,text_get,"left")

def right_align():
    text_get=text_editor.get(1.0,"end")
    text_editor.tag_config("center",justify=tk.CENTER)
    text_editor.delete(1.0,tk.END)
    text_editor.insert(tk.INSERT,text_get,"center")

def center_align():
    text_get=text_editor.get(1.0,"end")
    text_editor.tag_config("right",justify=tk.RIGHT)
    text_editor.delete(1.0,tk.END)
    text_editor.insert(tk.INSERT,text_get,"right")

def new_file(event=None):
    global text_url
    text_url = None
    text_editor.delete(1.0, tk.END)
    main_app.title("untitled - NOTEPAD_PRO")

def open_file(event=None):
    global text_url
    text_url = filedialog.askopenfilename(initialdir=os.getcwd, title="Select File", filetypes=(
        ("Text file", "*txt"), ("All files", "*.*")))
    try:
        with open(text_url, "r") as for_read:
            text_editor.delete(1.0, tk.END)
            text_editor.insert(1.0, for_read.read())
    except FileNotFoundError:
        return
    except:
        return
    if(str(type(text_url)) == "<class '_io.TextIOWrapper'>"):
        text_url = text_url.name
    main_app.title(f"{os.path.basename(text_url)} - NOTEPAD_PRO")

def save_file(event=None):
    global text_url
    try:
        if text_url != None:
            content = str(text_editor.get(1.0, tk.END))
            with open(str(text_url), "w", encoding="utf-8") as for_read:
                for_read.write(content)
        else:
            text_url = filedialog.asksaveasfile(mode="w", defaultextension=".txt", filetypes=(
                ("Text file", "*txt"), ("All files", "*.*")))
            content2 = text_editor.get(1.0, tk.END)
            text_url.write(content2)
            text_url.close()
    except:
        return
    if(str(type(text_url)) == "<class '_io.TextIOWrapper'>"):
        text_url=text_url.name
    main_app.title(f"{os.path.basename(text_url)} - NOTEPAD_PRO")

def save_as_file(event=None):
    global text_url,text_editor
    try:
        content = text_editor.get(1.0, tk.END)
        text_url = filedialog.asksaveasfile(mode="w", defaultextension=".txt", filetypes=(
            ("Text file", "*txt"), ("All files", "*.*")))
        text_url.write(content)
        text_url.close()
    except:
        return
    if(str(type(text_url)) == "<class '_io.TextIOWrapper'>"):
        text_url = text_url.name
    main_app.title(f"{os.path.basename(text_url)} - NOTEPAD_PRO")
    # open the save as file
    try:
        with open(text_url, "r") as for_read:
            text_editor.delete(1.0, tk.END)
            text_editor.insert(1.0, for_read.read())
    except:
        return

def exit_program(event=None):
    global text_change, text_url
    try:
        if text_change:
            mbox = messagebox.askyesnocancel(
                "WARNING!", "Do you want to save this file?")
            if mbox is True:
                if text_url:
                    content = text_editor.get(1.0, tk.END)
                    with open(text_url, "w", encoding="utf-8") as for_read:
                        for_read.write(content)
                        main_app.destroy()
                else:
                    content2 = text_editor.get(1.0, tk.END)
                    text_url = filedialog.asksaveasfile(mode="w", defaultextension=".txt", filetypes=(
                        ("Text file", "*txt"), ("All files", "*.*")))
                    text_url.write(content2)
                    text_url.close()
                    main_app.destroy()
            elif mbox is False:
                main_app.destroy()
            else:
                return
        else:
            main_app.destroy()
    except:
        return

def find(event=None):

    def find_func():
        word = find_input.get()
        text_editor.tag_remove("match", "1.0", tk.END)
        matches = 0
        if word:
            start_posn = "1.0"
            while True:
                start_posn = text_editor.search(
                    word, start_posn, stopindex=tk.END)
                if not start_posn:
                    break
                end_posn = f"{start_posn}+{len(word)}c"
                text_editor.tag_add("match", start_posn, end_posn)
                matches += 1
                start_posn = end_posn
                text_editor.tag_config(
                    "match", foreground="red", background="blue")

    def replace_func():
        word = find_input.get()
        replace_text = replace_input.get()
        content = text_editor.get("1.0", tk.END)
        new_content = content.replace(word, replace_text)
        text_editor.delete("1.0", tk.END)
        text_editor.insert("1.0", new_content)

    #pop up window
    find_pop_up = tk.Toplevel()
    find_pop_up.geometry("450x200")
    find_pop_up.title("FIND , REPLACE WORD")
    find_pop_up.resizable(0, 0)

    #frame for find screen
    find_frame = ttk.LabelFrame(find_pop_up, text="Find and Replace Words")
    find_frame.pack(pady=10, padx=10)

    # find and replace labels
    find_text_label = ttk.Label(find_frame, text="FIND")
    replace_text_label = ttk.Label(find_frame, text="REPLACE")
    find_text_label.grid(row=0, column=0, padx=4, pady=4)
    replace_text_label.grid(row=1, column=0, padx=4, pady=4)

    # find and replace text inputs
    find_input = ttk.Entry(find_frame, width=35)
    replace_input = ttk.Entry(find_frame, width=35)
    find_input.grid(row=0, column=1, padx=4, pady=4)
    replace_input.grid(row=1, column=1, padx=4, pady=4)

    # find and replace buttons
    find_btn = ttk.Button(find_frame, text="FIND", command=find_func)
    replace_btn = ttk.Button(find_frame, text="REPLACE", command=replace_func)
    find_btn.grid(row=2, column=0, padx=8, pady=4)
    replace_btn.grid(row=2, column=1, padx=8, pady=4)

def hide_tool_bar():
    global Show_Tool_Bar, Show_Status_Bar
    if Show_Tool_Bar:
        toolbars_label.pack_forget()
        Show_Tool_Bar = False
    else:
        text_editor.pack_forget()
        status_bar.pack_forget()
        toolbars_label.pack(side=tk.TOP, fill=tk.X)
        text_editor.pack(fill=tk.BOTH, expand=True)
        if Show_Status_Bar:
            status_bar.pack(side=tk.BOTTOM)
        Show_Tool_Bar = True

def hide_status_bar():
    global Show_Status_Bar, Show_Tool_Bar
    if Show_Status_Bar:
        status_bar.pack_forget()
        Show_Status_Bar = False
    else:
        status_bar.pack(side=tk.BOTTOM)
        Show_Status_Bar = True



'''ENDING DEFINING FUNCTIONS'''



main_app = tk.Tk()
main_app.geometry("800x600")
main_app.title("untitled - NOTEPAD_PRO")

main_menu = tk.Menu()

main_app.wm_iconbitmap("notepad_pro.ico")

'''IMPORTED ALL ICONS'''

#File Menu Icons
new_icon = tk.PhotoImage(file = "icons/new_file_icon.png")
open_icon = tk.PhotoImage(file = "icons/open_file_icon.png")
save_icon = tk.PhotoImage(file = "icons/save_file_icon.png")
save_as_icon = tk.PhotoImage(file = "icons/save_as_file_icon.png")
exit_icon = tk.PhotoImage(file = "icons/exit_file_icon.png")

#Edit Menu Icons
copy_icon=tk.PhotoImage(file = "icons/copy_edit_icon.png")
paste_icon=tk.PhotoImage(file = "icons/paste_edit_icon.png")
cut_icon=tk.PhotoImage(file = "icons/cut_edit_icon.png")
clear_all_icon=tk.PhotoImage(file = "icons/clear_all_edit_icon.png")
find_icon=tk.PhotoImage(file = "icons/find_edit_icon.png")

#View Menu Icons
toolbar_icon=tk.PhotoImage(file="icons/toolbar_icon.png")
statusbar_icon=tk.PhotoImage(file="icons/status_bar_icon.png")

#Color Theme
# default_light_icon=tk.PhotoImage(file="icons/")
# light_plus_icon=tk.PhotoImage(file="icons/")
# dark_red_icon=tk.PhotoImage(file="icons/")
# monokai_icon=tk.PhotoImage(file="icons/")
# dark_blue_icon=tk.PhotoImage(file="icons/")


'''
FILE MENU
    The following sub-menus are present in File Menu
        1) NEW
        2) OPEN
        3) SAVE
        4) SAVE AS
        5) EXIT

'''

text_url=None

file_menu = tk.Menu(main_menu,tearoff=False)
main_menu.add_cascade(label="FILE",menu=file_menu)

file_menu.add_command(label="NEW",image = new_icon,compound = tk.LEFT,accelerator="Ctrl+N",command=new_file)
file_menu.add_command(label="OPEN",image = open_icon,compound = tk.LEFT,accelerator="Ctrl+O",command=open_file)
file_menu.add_command(label="SAVE",image = save_icon,compound = tk.LEFT,accelerator="Ctrl+S",command=save_file)
file_menu.add_command(label="SAVE AS",image = save_as_icon,compound = tk.LEFT,accelerator="Ctrl+Shift+S",command=save_as_file)
file_menu.add_command(label="EXIT",image = exit_icon,compound = tk.LEFT,accelerator="Ctrl+Esc",command=exit_program)


'''
EDIT MENU
    The following sub-menus are present in EDIT Menu
        1) COPY
        2) PASTE
        3) CUT
        4) CLEAR ALL
        5) EXIT

'''
edit_menu = tk.Menu(main_menu,tearoff=False)
main_menu.add_cascade(label="EDIT",menu=edit_menu)

edit_menu.add_command(label="COPY", image=copy_icon, compound=tk.LEFT,
                      accelerator="Ctrl+C", command=lambda: text_editor.event_generate("<Control c>"))
edit_menu.add_command(label="PASTE", image=paste_icon, compound=tk.LEFT,
                      accelerator="Ctrl+V", command=lambda: text_editor.event_generate("<Control v>"))
edit_menu.add_command(label="CUT", image=cut_icon, compound=tk.LEFT,
                      accelerator="Ctrl+X", command=lambda: text_editor.event_generate("<Control x>"))
edit_menu.add_command(label="CLEAR ALL", image=clear_all_icon, compound=tk.LEFT,
                      accelerator="Ctrl+Shift+A", command=lambda: text_editor.delete(1.0,tk.END))
edit_menu.add_command(label="FIND", image=find_icon, compound=tk.LEFT,
                      accelerator="Ctrl+F", command=find)

'''
VIEW MENU
    The following sub-menus are present in EDIT Menu
        1) TOOLBAR
        2) STATUS

'''

toolbars_label = ttk.Label(main_app)
toolbars_label.pack(side=tk.TOP, fill=tk.X)

status_bar = ttk.Label(main_app, text="STATUS BAR")
status_bar.pack(side=tk.BOTTOM)

#Hide ToolBar and StatusBar

Show_Status_Bar = tk.BooleanVar()
Show_Status_Bar.set(True)
Show_Tool_Bar = tk.BooleanVar()
Show_Tool_Bar.set(True)

view_menu = tk.Menu(main_menu,tearoff=False)
main_menu.add_cascade(label="VIEW",menu=view_menu)

view_menu.add_checkbutton(label="TOOL BAR", image=toolbar_icon, onvalue=1, offvalue=0,
                          variable=Show_Tool_Bar, compound=tk.LEFT, command=hide_tool_bar)
view_menu.add_checkbutton(label="STATUS BAR",image=statusbar_icon, onvalue=1, offvalue=0,
                          variable=Show_Status_Bar, compound=tk.LEFT, command=hide_status_bar)


'''
COLOR THEME MENU
    The following sub-menus are present in EDIT Menu
        1) TOOLBAR
        2) STATUS

'''

#COLOR THEME FUNCTION
def color_theme_func():
    get_theme=theme_choose.get()
    color_tuple=color_dict.get(get_theme)
    fg_color,bg_color=color_tuple[0],color_tuple[1]
    text_editor.config(background=bg_color,fg=fg_color)

color_theme_menu = tk.Menu(main_menu,tearoff=False)

theme_choose = tk.StringVar(value='Light Default')

main_menu.add_cascade(label="COLOR THEME",menu=color_theme_menu)


#Color Theme

light_default_theme_icon = tk.PhotoImage(file="icons/light_theme.png")
light_plus_theme_icon = tk.PhotoImage(file="icons/light_theme_plus.png")
dark_theme_icon = tk.PhotoImage(file="icons/dark_theme.png")
red_theme_icon = tk.PhotoImage(file="icons/red_theme.png")
monokai_theme_icon = tk.PhotoImage(file="icons/monokai_theme.png")
night_blue_theme_icon = tk.PhotoImage(file="icons/night_blue_theme.png")

color_icons=(light_default_theme_icon,light_plus_theme_icon,dark_theme_icon,red_theme_icon,monokai_theme_icon,night_blue_theme_icon)

color_dict = {
    'Light Default': ('#000000', '#ffffff'),
    'Light Plus': ('#474747', '#e0e0e0'),
    'Dark': ('#c4c4c4', '#2d2d2d'),
    'Red': ('#2d2d2d', '#ffe8e8'),
    'Monokai': ('#d3b774', '#474747'),
    'Night Blue': ('#ededed', '#6b9dc2')
}

cnt=0
for i in color_dict:
    color_theme_menu.add_radiobutton(
        label=i, compound=tk.LEFT, image=color_icons[cnt], command=color_theme_func,variable=theme_choose)
    cnt+=1


#fontbox

font_tuple=tk.font.families()
font_family=tk.StringVar()
font_box=ttk.Combobox(toolbars_label,width="30",textvariable=font_family,state="readonly")
font_box["values"] = font_tuple
font_box.current(font_tuple.index("Arial"))
font_box.grid(row=0,column=0,padx=5,pady=5)

#size box

size_var=tk.IntVar()
font_size=ttk.Combobox(toolbars_label,width=20,textvariable=size_var,state="readonly")
font_size_tuple=tuple([6,7,8,9,10,11,12,13,14,15,16,18,20,22,24,26,28,32,36,40,44,48,54,60,66,72,80,88,96])
font_size["values"] = font_size_tuple
font_size.current(10)
font_size.grid(row=0,column=1,padx=5,pady=5)

main_app.config(menu = main_menu)

#bold button

bold_icon=tk.PhotoImage(file="icons/bold_icon.png")
bold_btn=tk.Button(toolbars_label,image=bold_icon)
bold_btn.grid(row=0,column=2,padx=5,pady=5)

#italic button

italic_icon=tk.PhotoImage(file="icons/italic_icon.png")
italic_btn=tk.Button(toolbars_label,image=italic_icon)
italic_btn.grid(row=0,column=3,padx=5,pady=5)

#underline button

under_line_icon=tk.PhotoImage(file="icons/under_line_icon.png")
under_line_btn=tk.Button(toolbars_label,image=under_line_icon)
under_line_btn.grid(row=0,column=4,padx=5,pady=5)

#color button

color_icon=tk.PhotoImage(file="icons/color_icon.png")
color_btn=tk.Button(toolbars_label,image=color_icon)
color_btn.grid(row=0,column=5,padx=5,pady=5)

#left align button

left_align_icon=tk.PhotoImage(file="icons/left_align_icon.png")
left_align_btn=tk.Button(toolbars_label,image=left_align_icon)
left_align_btn.grid(row=0,column=6,padx=5,pady=5)

#right align button

right_align_icon=tk.PhotoImage(file="icons/right_align_icon.png")
right_align_btn=tk.Button(toolbars_label,image=right_align_icon)
right_align_btn.grid(row=0,column=7,padx=5,pady=5)

#center align button

center_align_icon=tk.PhotoImage(file="icons/center_align_icon.png")
center_align_btn=tk.Button(toolbars_label,image=center_align_icon)
center_align_btn.grid(row=0,column=8,padx=5,pady=5)

#text editor

text_editor=tk.Text(main_app)
text_editor.config(wrap="word",relief=tk.FLAT)
text_editor.focus_set()
scroll_bar=tk.Scrollbar(main_app)
scroll_bar.pack(side=tk.RIGHT,fill=tk.Y)
text_editor.pack(fill=tk.BOTH,expand=True)
scroll_bar.config(command=text_editor.yview)
text_editor.config(yscrollcommand=scroll_bar.set)

#status bar -> word and character count

text_change=False
text_editor.bind("<<Modified>>",change_word)

#font family and function

font_now="Arial"
font_size_now="16"
font_box.bind("<<ComboboxSelected>>",change_font)
font_size.bind("<<ComboboxSelected>>",change_font_size)


'''
    print(tk.font.Font(font=text_editor["font"]).actual())
'''


#bold,italic,underline,color,left-alignment,right-alignment,center-alignment

bold_btn.configure(command=bold)
italic_btn.configure(command=italic)
under_line_btn.configure(command=underline)
color_btn.configure(command=color)
left_align_btn.configure(command=left_align)
right_align_btn.configure(command=right_align)
center_align_btn.configure(command=center_align)

main_app.mainloop()