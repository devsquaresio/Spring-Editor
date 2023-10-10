from customtkinter import *
from tkinter import filedialog
import searchtext, newsyn, os
import tkinter as tk
from tkterm import Terminal

app = CTk()
app.title("New File - Lightning Editor")
app.geometry("800x600")

set_default_color_theme("dark-blue")

find_visibility = False

f_size = 20
f_family = "Victor Mono"
font = CTkFont(family=f_family, size=f_size)
smaller_font = CTkFont(family=f_family, size=10)
auto_complete_font = CTkFont(family=f_family, size=20)
main_textbox = CTkTextbox(app, width=800, height=600, font=font, wrap='none', fg_color="#121211", corner_radius=0, undo=True)

autocorrect = False

indent_num = ''

main_textbox.grid(row=0, column=0, sticky=N+S+E+W)
app.grid_columnconfigure(0, weight=1)
app.grid_rowconfigure(0, weight=1)

last_dir = ''
f_path = last_dir
current_language = 'python'

text_box_text = ''
text_box_regex = False
text_box_case_sensitive = False
text_box_word_list = []
showed_replace = False

def change_regex_boolean():
    global text_box_regex
    text_box_regex = not text_box_regex
    if text_box_regex:
        text_box_find_regex_button.configure(fg_color="#2160c4", hover_color="#2f3030")
    else:
        text_box_find_regex_button.configure(fg_color="#2f3030", hover_color="#2160c4")
    change_text(1)

def change_caps_boolean():
    global text_box_case_sensitive
    text_box_case_sensitive = not text_box_case_sensitive
    if text_box_case_sensitive:
        text_box_find_case_sensitive_button.configure(fg_color="#2160c4", hover_color="#2f3030")
    else:
        text_box_find_case_sensitive_button.configure(fg_color="#2f3030", hover_color="#2160c4")
    change_text(1)

def show_replace():
    global showed_replace, textbox_frame_y
    showed_replace = not showed_replace
    if showed_replace: 
        caret_button_replace.configure(text="v", height=53.5)
        textbox_frame.configure(height=70)
        textbox_frame.place(rely=0.06)
        textbox_frame_y = 0.06
        replace_text_box.place(relx=0.1, rely=0.575)
        replace_confirm_one.place(relx=0.6, rely=0.575)
        replace_confirm_only_once.place(relx=0.7, rely=0.575)
    else:
        caret_button_replace.configure(text=">", height=25)
        textbox_frame.configure(height=35)
        textbox_frame.place(rely=0.03)
        textbox_frame_y = 0.03
        replace_text_box.place_forget()
        replace_confirm_one.place_forget()
        replace_confirm_only_once.place_forget()

def replace_text_type(only_once):
    if text_box_regex:
        import re
        find_txt = text_box.get()
        replace_txt = replace_text_box.get()

        all_text = main_textbox.get("1.0", "end-1c")
        if only_once:
            rep_text = re.sub(find_txt, replace_txt, all_text, count=1)
        else:
            ep_text = re.sub(find_txt, replace_txt, all_text)

        main_textbox.delete("1.0", tk.END)
        main_textbox.insert(tk.END, rep_text)

        update_syntax(1)
        change_text(1)
    else:
        replace_txt = replace_text_box.get()
        reg_text, hashmap = text_box.get(), {}
        for i in text_box_word_list:
            try:
                if hashmap[i[0].split('.')[0]] != None:
                    num = hashmap[i[0].split('.')[0]]
                    main_textbox.delete(f"{int(i[0].split('.')[0])}.{int(i[0].split('.')[1]) - num}", f"{int(i[1].split('.')[0])}.{int(i[1].split('.')[1]) - num}")
                    main_textbox.insert(f"{int(i[0].split('.')[0])}.{int(i[0].split('.')[1]) - num}", replace_txt)
                    hashmap[i[0].split('.')[0]] = hashmap[i[0].split('.')[0]] + len(reg_text) - len(replace_txt)
            except:
                hashmap[i[0].split('.')[0]] = len(reg_text) - len(replace_txt)
                main_textbox.delete(i[0], i[1])
                main_textbox.insert(i[0], replace_txt)
            
            if only_once:
                break
            
        update_syntax(1)
        change_text(1)

def decipher_syn(arr1):
    syn_list = {"keywords": [],
                    "strings": [],
                    "numbers": [],
                    "comments": [],
                    "functions": [],
                    "errors": []}
    tokens = newsyn.Lexer(lines=arr1).py_decode()
    for i in tokens:
        if i.type == "KEYWORD":
            syn_list["keywords"].append(i)
        elif i.type == "NUMBER":
            syn_list["numbers"].append(i)
        elif i.type == "STRING":
            syn_list["strings"].append(i)
        elif i.type == "FUNCTION":
            syn_list["functions"].append(i)
        elif i.type == "COMMENT":
            syn_list["comments"].append(i)

    return syn_list

textbox_frame = CTkFrame(master=app, width=330, height=35, fg_color="#161717", corner_radius=1.5, border_color="#161717")
text_box = CTkEntry(master=textbox_frame, width=160, height=25, font=smaller_font)
text_box.place(relx=0.1, rely=0.15)
text_box_find_case_sensitive_button = CTkButton(master=textbox_frame, text="Aa", width=25, height=25, fg_color="#2f3030", command=change_caps_boolean, hover_color="#2160c4")
text_box_find_case_sensitive_button.place(relx=0.60, rely=0.15)
text_box_find_regex_button = CTkButton(master=textbox_frame, text=".*", width=27, height=25, fg_color="#2f3030", command=change_regex_boolean, hover_color="#2160c4")
text_box_find_regex_button.place(relx=0.70, rely=0.15)
caret_button_replace = CTkButton(master=textbox_frame, text=">", width=25, height=25, fg_color="#2f3030", command=show_replace)
caret_button_replace.place(relx=0.015, rely=0.15)
replace_text_box = CTkEntry(master=textbox_frame, width=160, height=25, font=smaller_font)
replace_confirm_one = CTkButton(master=textbox_frame, text="1.", width=25, height=25, fg_color="#2f3030", command=lambda: replace_text_type(True))
replace_confirm_only_once = CTkButton(master=textbox_frame, text="*", width=25, height=25,  fg_color="#2f3030", command=lambda: replace_text_type(False))

terminal = Terminal(app)

textbox_frame_y = -0.05

def fetch_lines(file):
    with open(file, 'r') as f:
        for line in f:
            yield line

def update_syntax(event):
    if True:
        if app.title()[-1] != '*':
            app.title(app.title() + '*')
        for i in main_textbox.tag_names():
            if not i.startswith("found"):
                main_textbox.tag_delete(i)
        arr1 = [i for i in main_textbox.get("1.0", "end").split('\n')]
        del arr1[len(arr1)-1]
        if arr1 != ['']:
            for i in range(len(arr1)): 
                if i != len(arr1)-1: arr1[i] += '\n'
            syn_list = decipher_syn(arr1=arr1)
            if syn_list["keywords"] != []:
                for num, i in enumerate(syn_list["keywords"]):
                    start_pos = i.start_line
                    end_pos = i.end_line
                    format1 = f'{start_pos+1}.{i.start_index}'
                    format2 = f'{end_pos+1}.{i.end_index}'
                    main_textbox.tag_add(f"keyword{num}", format1, format2)
                    main_textbox.tag_config(f"keyword{num}", foreground="#f2c233")
            if syn_list["strings"] != []:
                for num, i in enumerate(syn_list["strings"]):
                    start_pos = i.start_line
                    end_pos = i.end_line
                    format1 = f'{start_pos+1}.{i.start_index}'
                    format2 = f'{end_pos+1}.{i.end_index}'
                    main_textbox.tag_add(f"string{num}", format1, format2)
                    main_textbox.tag_config(f"string{num}", foreground="#3bb830")
            if syn_list["comments"] != []:
                for num, i in enumerate(syn_list["comments"]):
                    start_pos = i.start_line
                    end_pos = i.end_line
                    format1 = f'{start_pos+1}.{i.start_index}'
                    format2 = f'{end_pos+1}.{i.end_index}'
                    main_textbox.tag_add(f"comment{num}", format1, format2)
                    main_textbox.tag_config(f"comment{num}", foreground="#464a47")
            if syn_list["functions"] != []:
                for num, i in enumerate(syn_list["functions"]):
                    start_pos = i.start_line
                    end_pos = i.end_line
                    format1 = f'{start_pos+1}.{i.start_index}'
                    format2 = f'{end_pos+1}.{i.end_index}'
                    main_textbox.tag_add(f"function{num}", format1, format2)
                    main_textbox.tag_config(f"function{num}", foreground="#cbf048")
            if syn_list["numbers"] != []:
                for num, i in enumerate(syn_list["numbers"]):
                    start_pos = i.start_line
                    end_pos = i.end_line
                    format1 = f'{start_pos+1}.{i.start_index}'
                    format2 = f'{end_pos+1}.{i.end_index}'
                    main_textbox.tag_add(f"num{num}", format1, format2)
                    main_textbox.tag_config(f"num{num}", foreground="#76f272")
            if syn_list["errors"] != []:
                pass

def open_file(event):
    global last_dir
    global f_path
    text_file = filedialog.askopenfilename(initialdir=last_dir, title="Open File", filetypes=[("All Files", "*.*")])
    if text_file:
        last_dir = text_file
        f_path = text_file
        id = last_dir.rfind("/")
        lines = fetch_lines(last_dir)
        i = 1
        main_textbox.delete("1.0", "end")
        while 1:
            try: 
                main_textbox.insert(f"{i}.0", next(lines))
                i += 1
            except: 
                break
        update_syntax(1)
        change_text(1)
        app.title(f'{f_path[id+1:]} - Lightning Editor')

def save_as_file(event):
    text_file = filedialog.asksaveasfilename(defaultextension='.*', title='Save As File')
    if text_file:
        last_dir = text_file
        f_path = text_file
        id = last_dir.rfind("/")
        app.title(f'{f_path[id+1:]} - Lightning Editor')
        with open(last_dir, 'w') as f:
            f.writelines(main_textbox.get("1.0", "end"))

def save_file(event):
    if last_dir:
        with open(last_dir, "w") as f:
            f.writelines(main_textbox.get("1.0", "end"))
        id = last_dir.rfind("/")
        app.title(f'{f_path[id+1:]} - Lightning Editor')
    else:
        save_as_file(1)

def increase_size(d):
    global f_size
    f_size += 5
    font.configure(size=f_size)
    main_textbox.configure(require_redraw=True, font=font)

def decrease_size(d):
    global f_size
    f_size -= 5
    font.configure(size=f_size)
    main_textbox.configure(require_redraw=True, font=font)

def resize1(e):
    app.state('zoomed')

def resize2(e):
    ws = app.winfo_screenwidth() # width of the screen
    hs = app.winfo_screenheight() # height of the screen
    app.geometry('%dx%d+%d+%d' % (round(ws/2), hs, 0, 0))

def check_space(line):
    i = 0
    try:
        while line[i] in ' \t': i += 1
    except: pass
    return i * ' '

def indent(e):
    global indent_num
    indent_num = ""
    i1 = main_textbox.index("insert")
    i2 = int(i1.split('.')[0])-2
    arr1 = [i for i in main_textbox.get("1.0", "end").split('\n')]
    del arr1[len(arr1)-1]
    for i in range(len(arr1)): 
        if i != len(arr1)-1: arr1[i] += '\n'
    syn_list = {}
    syn_list = decipher_syn(arr1)
    try:
        i3 = arr1[i2][-2]
    except:
        i3 = ''
        
    if i3 == ':':
        indent_num = check_space(arr1[i2]) + '    '
    else:
        indent_num = check_space(arr1[i2])
    main_textbox.insert('insert', indent_num)

def add_char(e, char):
    if char == '""' or char == "''":
        if main_textbox.get(main_textbox.index("insert-2c"), "insert") == char:
            main_textbox.insert("insert", char)
    main_textbox.insert("insert", char)
    update_syntax(123)
    return "break"

def search_re(pattern):
        import re
        try:
            matches = []
            text = main_textbox.get("1.0", tk.END).splitlines()
            for i, line in enumerate(text):
                for match in re.finditer(pattern, line):
                    matches.append((f"{i + 1}.{match.start()}", f"{i + 1}.{match.end()}"))
            return matches
        except re.error:
            return []
        
def search_regular(pattern):
    matches = []
    text = main_textbox.get("1.0", tk.END).splitlines()
    for i, line in enumerate(text):
        for match in searchtext.search_pattern(pattern, line, case_sensitive=text_box_case_sensitive):
            matches.append((f"{i + 1}.{match[1]}", f"{i + 1}.{match[2]}"))
    return matches

def suggest_completion(event):
    if autocorrect:
        import jedi
        line, column = main_textbox.index("insert").split('.')
        line, column = int(line), int(column)
        source_code = main_textbox.get("1.0", "end")
        script = jedi.Script(source_code, path=last_dir)
        completions = script.complete(line, column)
        suggestions = [c.name for c in completions]
        if main_textbox.get(main_textbox.index(f'{line}.{column-1}'), main_textbox.index("insert")) in '" \t\'({[':
            suggestions = []
        suggestions_frame.place_forget()
        for i in suggestions_frame.winfo_children():
            i.destroy()

        cursor_index = main_textbox.index("insert")
        bbox = main_textbox.bbox(cursor_index)
        
        if bbox:
            cursor_x, cursor_y, _, _ = bbox
            m_height = 200
            s_height = min(len(suggestions)*5, m_height)
            suggestions_frame.place(x=15+cursor_x + main_textbox.winfo_x(), y=30+cursor_y + main_textbox.winfo_y())
            for suggestion in suggestions:
                suggestion_label = CTkLabel(suggestions_frame, text=suggestion, font=auto_complete_font, anchor='w', justify='left')
                suggestions_frame.configure(height=s_height)
                suggestion_label.pack(fill=tk.X)
            if suggestions_frame.winfo_children() == []:
                suggestions_frame.place_forget()

def switch_autocorrect(e):
    global autocorrect
    autocorrect = not autocorrect

def change_text(e):
    global text_box_text, text_box, main_textbox, find_visibility, text_box_regex, text_box_word_list
    text_box_text = text_box.get()
    if find_visibility:
        for i in main_textbox.tag_names():
            if i.startswith("found"):
                main_textbox.tag_delete(i)
        if text_box_text:
            text_box_word_list = []
            if text_box_regex:
                for match in search_re(text_box_text):
                    text_box_word_list.append([match[0], match[1]])
                    main_textbox.tag_add("found", match[0], match[1])
                    main_textbox.tag_config("found", background="#40403f")
            else:
                for match in search_regular(text_box_text):
                    text_box_word_list.append([match[0], match[1]])
                    main_textbox.tag_add("found", match[0], match[1])
                    main_textbox.tag_config("found", background="#40403f")

def move_up():
    global textbox_frame_y
    if textbox_frame_y < 0.03:
        textbox_frame_y += 0.008
        textbox_frame.place(relx=0.75, rely=textbox_frame_y, anchor=CENTER)
        textbox_frame.after(10, move_up)

def move_down():
    global textbox_frame_y
    if textbox_frame_y > -0.05:
        textbox_frame_y -= 0.008
        textbox_frame.place(relx=0.75, rely=textbox_frame_y, anchor=CENTER)
        textbox_frame.after(10, move_down)

def find_enable(e):
    global find_visibility, text_box, textbox_frame
    find_visibility = not find_visibility
    if find_visibility:
        move_up()
        text_box.focus_set()
        change_text(1)
    else:
        change_text(1)
        for i in main_textbox.tag_names():
            if i.startswith("found"):
                main_textbox.tag_delete(i)
        caret_button_replace.configure(text=">", height=25)
        textbox_frame.configure(height=35)
        textbox_frame.place(rely=0.03)
        textbox_frame_y = 0.03
        replace_text_box.place_forget()
        replace_confirm_one.place_forget()
        replace_confirm_only_once.place_forget()
        move_down()

suggestions_frame = CTkScrollableFrame(app, corner_radius=0.5, width=500)
app.bind("<KeyRelease>", suggest_completion)

def do_key_stuff(e):
    update_syntax(1)
    change_text(1)

app.bind('<Key>', do_key_stuff)
app.bind('<Control_L>m', open_file)
app.bind('<Control_L>g', save_as_file)
app.bind('<Control_L>s', save_file)
app.bind('<Control_L>=', increase_size)
app.bind('<Control_L>-', decrease_size)
app.bind('<Control_L>1', resize1)
app.bind('<Control_L>2', resize2)
app.bind('<Control_L>f', find_enable)
app.bind('<Return>', indent)
app.bind('<Control_L>k', switch_autocorrect)

main_textbox.bind('(', lambda a: add_char(e=1, char='()'))
main_textbox.bind('{', lambda a: add_char(e=1, char='{}'))
main_textbox.bind('[', lambda a: add_char(e=1, char='[]'))
main_textbox.bind('"', lambda a: add_char(e=1, char='""'))
main_textbox.bind("'", lambda a: add_char(e=1, char="''"))

app.mainloop()
