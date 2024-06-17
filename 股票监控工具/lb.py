# -*- coding: utf-8 -*-

import tkinter as tk
#import winsound
import akshare as ak
from threading import Thread
import time
import pandas as pd
from loguru import logger


def fetch_data(period_entry, market_value_max, volume_ratio, output, status_label, root, frame):
    while True:
        cur_time = pd.Timestamp.now().strftime('%H:%M:%S')
        logger.info(f'当前时间：{cur_time}')
        if cur_time < "09:30:00" or cur_time > "15:00:00":
            status_label.config(text="未到交易时间...")
            time.sleep(1)
        else:
            break

    logger.info(f'---------------------------------  开始第一次检测 --------------------------------------------')
    status_label.config(text="程序正在运行...")
    time.sleep(period_entry)
    global df_0
    for i in range(60):
        cur_time = pd.Timestamp.now().strftime('%H:%M:%S')
        logger.info(f'当前时间：{cur_time}')
        cur_time = cur_time.split(":")[-1]
        if cur_time >= "57":
            df_0 = ak.stock_zh_a_spot_em()
            df_0['时间'] = pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')
            # logger.info(f'第一次检测数据：{df_0}')
            # spath = r"./data_0.csv"
            # df_0.to_csv(spath, encoding="utf_8_sig", index=False)
            break
        else:
            time.sleep(1)

    code_list = []

    while True:
        logger.info(f'---------------------------------  开始检测 --------------------------------------------')
        time.sleep(period_entry - 1)
        df_1 = ak.stock_zh_a_spot_em()
        df_1['时间'] = pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')
        # logger.info(f'第N次检测数据：{df_1}')
        # spath = r"./data_1.csv"
        # df_1.to_csv(spath, encoding="utf_8_sig", index=False)

        # 预先计算并存储需要的数据
        df_1_quantities = df_1.set_index('代码')['量比']
        df_0_quantities = df_0.set_index('代码')['量比']
        zsz = df_0.set_index('代码')['总市值']
        syl = df_0.set_index('代码')['市盈率-动态']
        zs = df_0.set_index('代码')['涨速']

        # 循环遍历代码
        for code in df_1['代码']:
            # logger.info(f'第一次的量比：{df_0_quantities[code]}')
            # logger.info(f'第N次的量比：{df_1_quantities[code]}')
            if (code not in code_list and df_1_quantities[code] > df_0_quantities[code] and syl[code] > 0
                    and zs[code] > 0 and zsz[code] / 100000000 < market_value_max and str(
                        df_1_quantities[code]) > volume_ratio):
                code_list.append(code)
                output.insert(tk.END, str(code) + '   ' + str(df_1_quantities[code]) + '\n')
                logger.info(f'证券代码：{str(code)}     量比：{str(df_1_quantities[code])}')
                #winsound.Beep(1000, 3000)
                frame.config(bg='red')
                root.after(250, lambda: frame.config(bg='white'))
                root.after(500, lambda: frame.config(bg='red'))
                root.after(750, lambda: frame.config(bg='white'))


def create_gui():
    root = tk.Tk()
    root.title("股票数据监控")
    root.geometry("300x400")

    frame = tk.Frame(root, highlightbackground="black", highlightthickness=1)
    frame.grid(row=0, column=0, rowspan=5, columnspan=3, sticky='nsew')

    tk.Label(frame, text="周期(秒):").grid(row=0, column=0)
    period_entry = tk.Entry(frame)
    period_entry.insert(0, "60")
    period_entry.config(fg='blue')
    period_entry.grid(row=0, column=1)

    tk.Label(frame, text="最大市值(亿):").grid(row=1, column=0)
    market_value_max_entry = tk.Entry(frame)
    market_value_max_entry.insert(0, "200")
    market_value_max_entry.config(fg='blue')
    market_value_max_entry.grid(row=1, column=1)

    tk.Label(frame, text="量比:").grid(row=2, column=0)
    volume_ratio_entry = tk.Entry(frame)
    volume_ratio_entry.insert(0, "5")
    volume_ratio_entry.config(fg='blue')
    volume_ratio_entry.grid(row=2, column=1)

    start_button = tk.Button(frame, text="开始监控",
                             command=lambda: start_thread(period_entry.get(), market_value_max_entry.get(),
                                                          volume_ratio_entry.get(),
                                                          output_text, status_label, root, frame))
    start_button.grid(row=3, column=0, columnspan=2)

    output_text = tk.Text(frame, height=20, width=40)
    output_text.grid(row=4, column=0, columnspan=2)
    scrollbar = tk.Scrollbar(frame, command=output_text.yview)
    scrollbar.grid(row=4, column=2, sticky='ns')
    output_text.config(yscrollcommand=scrollbar.set)

    status_label = tk.Label(frame, text="")
    status_label.grid(row=5, column=0, columnspan=2)

    root.mainloop()


def start_thread(period, market_value_max, volume_ratio, output, status_label, root, frame):
    period = int(period)
    market_value_max = float(market_value_max)
    status_label.config(text="程序正在运行...")
    thread = Thread(target=fetch_data, args=(period, market_value_max, volume_ratio, output, status_label, root, frame))
    thread.daemon = True
    thread.start()


if __name__ == '__main__':
    create_gui()
