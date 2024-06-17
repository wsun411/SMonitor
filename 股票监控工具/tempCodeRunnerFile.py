def flash_text_widget(text_widget, count):
    if count % 2 == 0:
        text_widget.config(bg='white', fg='red')
    else:
        text_widget.config(bg='red', fg='white')
    if count < 4:
        text_widget.after(500, flash_text_widget, text_widget, count + 1)