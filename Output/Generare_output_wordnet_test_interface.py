"""
Modul creat de Andrei Iacob grupa 3A5
"""
import Generare_output_wordnet
import Tkinter as tk
from idlelib.WidgetRedirector import WidgetRedirector

class ReadOnlyText(tk.Text):
     def __init__(self, *args, **kwargs):
         tk.Text.__init__(self, *args, **kwargs)
         self.redirector = WidgetRedirector(self)
         self.insert = self.redirector.register("insert", lambda *args, **kw: "break")
         self.delete = self.redirector.register("delete", lambda *args, **kw: "break")

class ExampleApp(tk.Tk):
    def add_to_text(self):
        question=self.input.get()
        self.textbox.insert(tk.END,"You: " + question +'\n')
        self.textbox.insert(tk.END,"Best chatbot 2016 (copyright A5): "+ Generare_output_wordnet.answer_question(question)+'\n')
        self.remaining = 30
    
    def __init__(self):
        tk.Tk.__init__(self)
        self.label = tk.Label(self, text="", width=10)
        self.label.pack()
        self.textbox = ReadOnlyText(self, width=100,height=30)
        self.textbox.pack()
        self.input = tk.Entry(width=100)
        self.input.pack()
        self.button = tk.Button(self,command=self.add_to_text,text="send",)
        self.button.pack()
        self.remaining = 0
        self.countdown(30)
        
        
    def countdown(self, remaining = None):
        if remaining is not None:
            self.remaining = remaining

        if self.remaining <= 0:
            self.textbox.insert(tk.END,Generare_output_wordnet.generate_question('topic')+'\n')
            self.remaining = 30
            self.label.configure(text="%d" % self.remaining)
            self.remaining = self.remaining - 1
            self.after(1000, self.countdown)
        else:
            self.label.configure(text="%d" % self.remaining)
            self.remaining = self.remaining - 1
            self.after(1000, self.countdown)



app = ExampleApp()
app.mainloop()
