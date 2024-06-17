import threading
import time
import tkinter as tk
import pandas as pd
import akshare as ak
import winsound


def flash_text_widget(text_widget, count):
    if count % 2 == 0:
        text_widget.config(bg='white', fg='red')
    else:
        text_widget.config(bg='red', fg='white')
    if count < 4:
        text_widget.after(500, flash_text_widget, text_widget, count + 1)


def start_monitor_thread(code, rate, text_widget):
    def run():
        # 读取Excel文件
        df = pd.read_excel('换手率.xlsx', dtype={'证券代码': str})
        code_list = df['证券代码'].tolist()
        turnover_rate = df['换手率'].tolist()
        print(code_list)
        print(turnover_rate)
        while True:
            time.sleep(10)
            df_0 = ak.stock_zh_a_spot_em()
            df_0 = df_0[['代码', '换手率']]
            df_0['时间'] = pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')
            # spath = r"./data_0.csv"
            # df_0.to_csv(spath, encoding="utf_8_sig", index=False)

            for index, row in df_0.iterrows():
                code = row['代码']
                if code in code_list:
                    print(code)
                    idx = code_list.index(code)
                    if float(row['换手率']) > float(turnover_rate[idx]):
                        text_widget.insert(tk.END, str(code) + '\n')
                        winsound.Beep(1000, 2000)
                        flash_text_widget(text_widget, 0)

    thread = threading.Thread(target=run)
    thread.daemon = True
    thread.start()


def on_start():
    code = code_entry.get().split()
    turnover = turnover_entry.get().split()
    status_label.config(text="程序正在运行")
    start_monitor_thread(code, turnover, text)


root = tk.Tk()
root.title("换手率监控")
root.geometry("300x400")

tk.Label(root, text="证券代码", anchor="w").grid(row=0, column=0, sticky=tk.W + tk.E)
code_entry = tk.Entry(root, width=60)
code_entry.grid(row=0, column=1, columnspan=2, sticky=tk.W + tk.E)

tk.Label(root, text="换手率", anchor="w").grid(row=1, column=0, sticky=tk.W + tk.E)
turnover_entry = tk.Entry(root, width=60)
turnover_entry.grid(row=1, column=1, columnspan=2, sticky=tk.W + tk.E)

start_button = tk.Button(root, text="开始", command=on_start)
start_button.grid(row=2, column=0, pady=(10, 0), columnspan=3)

text = tk.Text(root)
text.grid(row=3, column=0, columnspan=3, sticky=tk.N + tk.S + tk.W + tk.E, padx=5, pady=5)

scrollbar = tk.Scrollbar(root, command=text.yview)
scrollbar.grid(row=3, column=3, sticky=tk.N + tk.S)
text.config(yscrollcommand=scrollbar.set)

status_label = tk.Label(root, text="", anchor="w")
status_label.grid(row=4, column=0, columnspan=3, sticky=tk.W + tk.E)

root.columnconfigure(0, weight=1)
root.columnconfigure(1, weight=1)
root.columnconfigure(2, weight=1)
root.rowconfigure(3, weight=1)

root.mainloop()
