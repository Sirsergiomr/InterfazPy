from tkinter import *
import ModelAndView
def main():
    raiz = Tk()
    raiz.title("Agenda Telefónica Py V1")
    raiz.configure(bg="#3a4241")
    raiz.geometry("+250+80")
    raiz.resizable(False,False)
    ModelAndView.Agenda(raiz)
    raiz.mainloop()
if __name__ == "__main__":
    main()