import requests
import sys
import time
import tkinter as tk
from tkinter import ttk

ip = None
request_type = None
interval = None
program_type = None
stop_flag = False
running = False
font_style = ("Arial Black", 10, "bold")

class gui:
    def run():
        def create_aura_label(parent, text, aura_color):
            aura_label = ttk.Label(parent, text=text, font=font_style, background=aura_color)
            aura_label.pack(padx=5, pady=5)
        def toggle_button():
            global running
            running = not running  # Toggle the state (True to False or False to True)

            if running:
                send_button.config(text="Остановить", bg="red", fg="white", command=stop_request)
            else:
                send_button.config(text="Отправить", bg="green", fg="white", command=send_request)
        def stop_request():
            global stop_flag
            stop_flag = True
            toggle_button()

        def send_request():
            global stop_flag
            ip = ip_var.get()
            interval = interval_var.get()
            request_type = request_var.get()  

            if request_type == "GET":
                requests.get(ip) 
            elif request_type == "HEAD":
                requests.head(ip)

            log_text.insert(tk.END, f"Запрос {request_type} отправлен на {ip}\n")
            
            if not stop_flag:
                root.after(interval * 1000, send_request)
            else:
                stop_flag = False

        def validate_fields():
            ip = ip_var.get()
            interval = interval_var.get()
            
            ip_entry.configure(style='TEntry')
            interval_entry.configure(style='TEntry')
            log_text.delete(1.0, tk.END)  # Clear any previous messages
            
            if not ip or not interval:
                if not ip:
                    ip_entry.configure(style='Error.TEntry')
                if not interval:
                    interval_entry.configure(style='Error.TEntry')
                log_text.insert(tk.END, "Заполните все поля!\n", "error_text")
            else:
                toggle_button()
                send_request()
        root = tk.Tk()
        root.title("Накрутчик переходов")
        root.geometry("575x385")
        root.configure(bg='#212121')
        style = ttk.Style()
        style.configure('TEntry', background='white', foreground='black')
        style.configure('Error.TEntry', background='white', foreground='black', bordercolor='red', borderwidth=2)
        style.configure('Отправить.TButton', font=font_style)
        style.configure('Остановить.TButton', font=font_style)
        
        ip_var = tk.StringVar()
        interval_var = tk.IntVar(value='1')
        request_var = tk.StringVar(value='HEAD')

        ip_label = ttk.Label(root, text="IP адрес или домен:", font=font_style)
        ip_entry = ttk.Entry(root, textvariable=ip_var, font=font_style, background="green", foreground="black", width=40)
        ip_label.configure(foreground="white", background="#52009e")
        #create_aura_label(root, "IP адрес или домен:", "#4e387e")

        interval_label = ttk.Label(root, text="Интервал (сек):", font=font_style)
        interval_entry = ttk.Entry(root, textvariable=interval_var, font=font_style)
        interval_label.configure(foreground="white", background="#52009e")
        interval_entry.configure(foreground="black", font=font_style)
        #create_aura_label(root, "Интервал (сек):", "#4e387e")

        request_label = ttk.Label(root, text="Тип запроса:", font=font_style)
        request_combo = ttk.Combobox(root, textvariable=request_var, values=["GET", "HEAD"], font=font_style, state="readonly")
        request_combo.current(1)
        request_label.configure(foreground="white", background="#52009e")
        request_combo.configure(foreground="black", font=font_style)
        #create_aura_label(root, "Тип запроса:", "#4e387e")

        send_button = tk.Button(root, text="Отправить", font=font_style, bg="green", fg="white")
        send_button.config(command=validate_fields)

        #stop_button = ttk.Button(root, text="Остановить", style="TButton", command=stop_requests)
        #stop_button.grid(row=3, column=1, sticky="w")
        
        log_text = tk.Text(root, height=10, font=font_style)
        log_text.pack(side="bottom")
        log_text.configure(bg="#141414", fg="#00730f")

        ip_label.pack(anchor="nw")
        ip_entry.pack(anchor="ne")

        interval_label.pack(anchor="nw") 
        interval_entry.pack(anchor="ne")

        request_label.pack(anchor="nw")
        request_combo.pack(anchor="ne")  
        
        send_button.pack()

        log_text.tag_configure("error_text", foreground="red")

        root.mainloop()

def console():
    try:
        while not request_type or request_type.lower() != 'get' and request_type.lower() != 'head' and request_type.lower() != 'stop' and request_type.lower() != 'exit': request_type = input("Тип запроса: GET/HEAD\n> ")
    except KeyboardInterrupt:
            print("=============")
            print("    ВЫХОД    ")
            print("=============")
            sys.exit(0)
    try:
        while not ip or not "http" in ip.lower() or not "." in ip.lower(): ip = input("IP адрес или домен для накрутки\n> ")
    except KeyboardInterrupt:
            print("=============")
            print("    ВЫХОД    ")
            print("=============")
            sys.exit(0)
    try:
        while interval is None: interval = int(input("Интервал между запросами (в секундах)\n> "))
    except KeyboardInterrupt:
            print("=============")
            print("    ВЫХОД    ")
            print("=============")
            sys.exit(0)

    while True:
        try:
            if request_type.lower() == 'get':
                try: 
                    requests.get(ip)
                    print(f"Запрос GET отправлен на {ip}")
                except Exception: break
            elif request_type.lower() == 'head':
                try: 
                    requests.get(ip)
                    print(f"Запрос HEAD отправлен на {ip}")
                except Exception: break
            elif request_type.lower() == "exit" or request_type.lower() == "stop":
                sys.exit(0)
            else:
                print("Указан неверный тип запроса")
            time.sleep(interval)
        except Exception as e:
            print(f"Ошибка: {e}")
            break
        except KeyboardInterrupt:
            print("=============")
            print("    ВЫХОД    ")
            print("=============")
            sys.exit(0)

print("+========================================================+")
print("+ Программа накрутки переходов на сайт приветствует вас! +")
print("+                Для выхода используйте                  +")
print("+ Ctrl+C во время отправки запросов(при работе в CONSOLE)+")
print("+                       или                              +")
print("+       exit или stop в меню выбора типа запроса         +")
print("+========================================================+")

try:
    while not program_type or program_type.lower() != "gui" and program_type.lower() != "console": program_type = input("Выберите вид программы: GUI/CONSOLE\n> ")

    if program_type.lower() == "gui":
        gui.run()
    elif program_type.lower() == "console":
        console()
    elif program_type.lower() == "exit" or program_type.lower() == "stop":
        sys.exit(0)
except Exception as e:
    print(f"Ошибка: {e}")
except KeyboardInterrupt:
    print("=============")
    print("    ВЫХОД    ")
    print("=============")
    sys.exit(0)