from tkinter import *
from tkinter import ttk
from tkinter import messagebox as MessageBox
import csv

#<-----Mensajes de error----->

def Dialog_AltaContacto():
    MessageBox.showinfo("Advertencia", "Necesitas Todos los campos para anadir un contacto con \"Añadir\"")
def delete_mesageBox(name):
    nombre = str(name)
    if nombre == '':
        Dialog_AltaContacto()
    else:
        search = MessageBox.askquestion("Advertencia","¿Estas seguro de borrar al siguiente contacto?\n" + nombre)
        if search == "yes":
            return True
        else:
            return False
def Dialog_ModificarContacto(contact):
    name = str(contact[0])
    phone = str(contact[1])
    email = str(contact[2])
    search = MessageBox.askquestion("Advertencia","¿Quieres modificar al siguiente contacto?\n" + " Nombre:" + name + "\n Telf:" + phone + "\n Correo:" + email)
    if search == "yes":
        return True
    else:
        return False
def FaltanCampos():
    MessageBox.showinfo("Error encontrado", "Faltan campos")

def NoExiste(var):
    v = str(var)
    MessageBox.showinfo("Error encontrado", v + ' ' + "No existe")

#<-----CONFIGURACION DE LA VENTANA ----->

class Agenda():
    def __init__(self, raiz):
        self.window = raiz
        panel_1 = LabelFrame(self.window, bg= "#3a4241")
        panel_1.grid(row=0, column=0)

        Label(panel_1, text = 'Nombre',bg="#3a4241", fg = "#33a4f5", font = ("Comic Sans MS", "11", "normal")).grid(row = 0, column = 0)
        cuadro_nombre = Entry(panel_1, font = ("Comic Sans MS", "11", "normal"), width = 28)
        cuadro_nombre.grid(row = 1, column = 0)
        cuadro_nombre.focus()

        Label(panel_1, text = 'Telefono',bg="#3a4241", fg = "#33a4f5", font = ("Comic Sans MS", "11", "normal")).grid(row = 0, column = 1)
        cuadro_telefono = Entry(panel_1, font = ("Comic Sans MS", "11", "normal"), width = 20)
        cuadro_telefono.grid(row = 1, column = 1)

        Label(panel_1, text = 'Correo',bg="#3a4241", fg = "#33a4f5", font = ("Comic Sans MS", "11", "normal")).grid(row = 0, column = 2)
        cuadro_correo = Entry(panel_1, font = ("Comic Sans MS", "11", "normal"), width = 30)
        cuadro_correo.grid(row = 1, column = 2)

        panel_botones = LabelFrame(self.window, bg = "#3a4241")
        panel_botones.grid(row = 2, column = 0)

        buttonAltaContacto = Button(panel_botones, command=lambda: add(), text='Añadir', width=20)
        buttonAltaContacto.configure(bg="#3a4241",fg="#f7fffe", cursor='hand2', font=("Comic Sans MS", "10", "normal"))
        buttonAltaContacto.grid(row=0, column=0, padx=2, pady=3, sticky=W + E)

        buttonBuscar = Button(panel_botones, command=lambda: search(), text='Buscar', width=20)
        buttonBuscar.configure(bg="#3a4241",fg="#f7fffe" ,cursor='hand2', font=("Comic Sans MS", "10", "normal"))
        buttonBuscar.grid(row=0, column=1, padx=2, pady=3, sticky=W + E)

        buttonBorrar = Button(panel_botones, command=lambda: delete(), text='Borrar', width=20)
        buttonBorrar.configure(bg="#F26262", cursor='hand2', font=("Comic Sans MS", "10", "normal"))
        buttonBorrar.grid(row=1, column=0, padx=2, pady=3, sticky=W + E)

        buttonModificar = Button(panel_botones, command=lambda: modify(), text='Modificar')
        buttonModificar.configure(bg="#3a4241",fg="#f7fffe", cursor='hand2', font=("Comic Sans MS", "10", "normal"))
        buttonModificar.grid(row=1, column=1, padx=2, pady=3, sticky=W + E)

        buttonMostrar = Button(panel_botones, command=lambda: show_contacts(), text='Mostrar', width=20)
        buttonMostrar.configure(bg="#3a4241",fg="#f7fffe", cursor='hand2', font=("Comic Sans MS", "10", "normal"))
        buttonMostrar.grid(row=0, column=2, padx=2, pady=3, sticky=W + E)

        buttonGuardar = Button(panel_botones, command=lambda: clean(), text='Guardar', width=20)
        buttonGuardar.configure(bg="#3a4241",fg="#f7fffe", cursor='hand2', font=("Comic Sans MS", "10", "normal"))
        buttonGuardar.grid(row=1, column=2, padx=2, pady=3, sticky=W + E)

        Label(panel_botones, text='Selecciona lo que \nquieras Buscar o Modificar', bg="#3a4241", fg = "#33a4f5", font=("Comic Sans MS", "10", "normal")).grid(
            row=0, column=3, columnspan=3)

        combo = ttk.Combobox(panel_botones, state='readonly', width=17, justify='center',
                             font=("Comic Sans MS", "10", "normal"))
        combo["values"] = ['Nombre', 'Telefono', 'Correo']
        combo.grid(row=1, column=3, padx=15)
        combo.current(0)

        Panel_Tabla = LabelFrame(self.window, bg="#3a4241")
        Panel_Tabla.grid(row = 4, column = 0)

        self.tree = ttk.Treeview(Panel_Tabla, height=20, columns=("one", "two"))
        self.tree.grid(padx=5, pady=5, row=0, column=0, columnspan=1)
        self.tree.heading("#0", text='Nombre', anchor=CENTER)
        self.tree.heading("one", text='Telefono', anchor=CENTER)
        self.tree.heading("two", text='Correo', anchor=CENTER)

        # Scroll de la tabla
        scrollVert = Scrollbar(Panel_Tabla, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollVert.set)
        scrollVert.grid(row=0, column=1, sticky="nsew")

        scroll_x = Scrollbar(Panel_Tabla, command=self.tree.xview, orient=HORIZONTAL)
        self.tree.configure(xscrollcommand=scroll_x.set)
        scroll_x.grid(row=2, column=0, columnspan=1, sticky="nsew")
        def _view_csv():
            with open('contacts_list.csv', 'r') as f:
                reader = csv.reader(f)
                for i, row in enumerate(reader):
                    nombre = str(row[0])
                    telefono = str(row[1])
                    correo = str(row[2])
                    self.tree.insert("", 0, text = nombre, values = (telefono, correo))
        def _clean_inbox():
            # Delete from first position (0) to the last position ('end')
            cuadro_nombre.delete(0, 'end')
            cuadro_telefono.delete(0, 'end')
            cuadro_correo.delete(0, 'end')

        def _clean_treeview():
            tree_list = self.tree.get_children()
            for item in tree_list:
                self.tree.delete(item)

        def _save(name, phone, email):
            s_name = name
            s_phone = phone
            s_email = email
            with open('contacts_list.csv', 'a') as f:
                writer = csv.writer(f, lineterminator='\r', delimiter=',')
                writer.writerow((s_name, s_phone, s_email))

        def _search(var_inbox, possition):
            my_list = []
            s_var_inbox = str(var_inbox)
            var_possition = int(possition)
            with open('contacts_list.csv', 'r') as f:
                reader = csv.reader(f)
                for i, row in enumerate(reader):
                    if s_var_inbox == row[var_possition]:
                        my_list = [row[0], row[1], row[2]]
                        break
                    else:
                        continue
            return my_list

        def _check(answer, var_search):
            list_answer = answer
            var_search = var_search
            if list_answer == []:
                NoExiste(var_search)
            else:
                name = str(list_answer[0])
                phone = str(list_answer[1])
                email = str(list_answer[2])
                self.tree.insert("", 0, text="------------------------------",
                                 values=("------------------------------", "------------------------------"))
                self.tree.insert("", 0, text=name, values=(phone, email))
                self.tree.insert("", 0, text="Search result of name",
                                 values=("Search result of phone", "Search result of email"))
                self.tree.insert("", 0, text="------------------------------",
                                 values=("------------------------------", "------------------------------"))

        def _check_1(answer, var_search):
            val_modify = answer
            var = var_search
            if val_modify == []:
                NoExiste(var)
            else:
                TopLevelModify(self.window, val_modify)

        # ----------------- BUTTON FUNCTIONS ------------------
        def add():
            nombre = cuadro_nombre.get()
            telefono = cuadro_telefono.get()
            correo = cuadro_correo.get()
            contact_check = [nombre, telefono, correo]
            if contact_check == ['', '', '']:
                Dialog_AltaContacto()
            else:
                if nombre == '':
                    nombre = '<Default>'
                if telefono == '':
                    telefono = '<Default>'
                if correo == '':
                    correo = '<Default>'
                _save(nombre, telefono, correo)
                self.tree.insert("", 0, text="------------------------------",
                                 values=("------------------------------", "------------------------------"))
                self.tree.insert("", 0, text=str(nombre), values=(str(telefono), str(correo)))
                self.tree.insert("", 0, text="Nombre añadido", values=("Telefono añadido", "Correo añadido"))
                self.tree.insert("", 0, text="------------------------------",
                                 values=("------------------------------", "------------------------------"))

            _clean_inbox()

        def search():

            answer = []
            var_search = str(combo.get())
            if var_search == 'Nombre':
                var_inbox = cuadro_nombre.get()
                possition = 0
                answer = _search(var_inbox, possition)
                _check(answer, var_search)
            elif var_search == 'Telefono':
                var_inbox = cuadro_telefono.get()
                possition = 1
                answer = _search(var_inbox, possition)
                _check(answer, var_search)
            else:
                var_inbox = cuadro_correo.get()
                possition = 2
                answer = _search(var_inbox, possition)
                _check(answer, var_search)
            _clean_inbox()

        def modify():
            answer = []
            var_search = str(combo.get())
            if var_search == 'Nombre':
                var_inbox = cuadro_nombre.get()
                possition = 0
                answer = _search(var_inbox, possition)
                _check_1(answer, var_search)
            elif var_search == 'Telefono':
                var_inbox = cuadro_telefono.get()
                possition = 1
                answer = _search(var_inbox, possition)
                _check_1(answer, var_search)
            else:
                var_inbox = cuadro_correo.get()
                possition = 2
                answer = _search(var_inbox, possition)
                _check_1(answer, var_search)
            _clean_inbox()

        def show_contacts():
            clean()
            self.tree.insert("", 0, text="------------------------------",
                             values=("------------------------------", "------------------------------"))
            _view_csv()
            self.tree.insert("", 0, text = "------------------------------", values = ("------------------------------", "------------------------------"))

        def delete():
            name = str(cuadro_nombre.get())
            a = delete_mesageBox(name)
            if a == True:
                with open('contacts_list.csv', 'r') as f:
                    reader = list(csv.reader(f))
                with open('contacts_list.csv', 'w') as f:
                    writer = csv.writer(f, lineterminator='\r', delimiter=',')
                    for i, row in enumerate(reader):
                        if name != row[0]:
                            writer.writerow(row)
            clean()
            show_contacts()

        def clean():
            _clean_inbox()
            _clean_treeview()


class TopLevelModify():
    def __init__(self, root, val_modify):
        self.root_window = root
        self.val_modify = val_modify
        self.name = str(self.val_modify[0])
        self.phone = str(self.val_modify[1])
        self.email = str(self.val_modify[2])

        window_modify = Toplevel(self.root_window)
        window_modify.title("Modify Contact")
        window_modify.configure(bg="#3a4241")
        window_modify.geometry("+400+100")
        window_modify.resizable(0, 0)

        text_frame = LabelFrame(window_modify, bg="#3a4241")
        text_frame.grid(row=0, column=0)

        button_frame = LabelFrame(window_modify, bg="#3a4241")
        button_frame.grid(row=2, column=0)


        Label(text_frame, text="¿Quieres modificar este contacto?", bg="#3a4241",fg="#f7fffe",
              font=("Comic Sans MS", "11", "normal")).grid(row=0, column=0, columnspan=3)
        Label(text_frame, text=self.name, bg="#3a4241",fg="#f7fffe", font=("Comic Sans MS", "11", "bold")).grid(row=1, column=0)
        Label(text_frame, text=self.phone, bg="#3a4241",fg="#f7fffe", font=("Comic Sans MS", "11", "bold")).grid(row=1, column=1)
        Label(text_frame, text=self.email, bg="#3a4241",fg="#f7fffe", font=("Comic Sans MS", "11", "bold")).grid(row=1, column=2)


        Label(text_frame, text='Nuevo Nombre', bg="#3a4241",fg="#f7fffe", font=("Comic Sans MS", "11", "normal")).grid(row=2,
                                                                                                              column=0)
        n_inbox_name = Entry(text_frame, font=("Comic Sans MS", "11", "normal"), width=28)
        n_inbox_name.grid(row=3, column=0)
        n_inbox_name.focus()

        Label(text_frame, text='Nuevo Telefono', bg="#3a4241",fg="#f7fffe", font=("Comic Sans MS", "11", "normal")).grid(row=2,
                                                                                                               column=1)
        n_inbox_phone = Entry(text_frame, font=("Comic Sans MS", "11", "normal"), width=20)
        n_inbox_phone.grid(row=3, column=1)

        Label(text_frame, text='Nuevo Correo', bg="#3a4241",fg="#f7fffe", font=("Comic Sans MS", "11", "normal")).grid(row=2,
                                                                                                               column=2)
        n_inbox_Email = Entry(text_frame, font=("Comic Sans MS", "11", "normal"), width=30)
        n_inbox_Email.grid(row=3, column=2)

        yes_button = Button(button_frame, command=lambda: yes(), text='Yes', width=20)
        yes_button.configure(bg="#3a4241",fg="#f7fffe", cursor='hand2', font=("Comic Sans MS", "10", "normal"))
        yes_button.grid(row=1, column=0, padx=2, pady=3, sticky=W + E)

        no_button = Button(button_frame, command=window_modify.destroy, text='No', width=20, bg="yellow",
                           cursor='hand2')
        no_button.configure(bg="#3a4241",fg="#f7fffe", cursor='hand2', font=("Comic Sans MS", "10", "normal"))
        no_button.grid(row=1, column=1, padx=2, pady=3, sticky=W + E)

        cancel_button = Button(button_frame, command=window_modify.destroy, text='Cancel', width=20, bg="green",
                               cursor='hand2')
        cancel_button.configure(bg="#3a4241",fg="#f7fffe", cursor='hand2', font=("Comic Sans MS", "10", "normal"))
        cancel_button.grid(row=1, column=2, padx=2, pady=3, sticky=W + E)

        def yes():
            contact = self.val_modify
            new_name = n_inbox_name.get()
            new_phone = n_inbox_phone.get()
            new_email = n_inbox_Email.get()
            a = Dialog_ModificarContacto(contact)
            if a == True:
                _del_old(contact[0])
                _add_new(new_name, new_phone, new_email)
            window_modify.destroy()

        def _add_new(name, phone, email):
            s_name = name
            s_phone = phone
            s_email = email
            with open('contacts_list.csv', 'a') as f:
                writer = csv.writer(f, lineterminator='\r', delimiter=',')
                writer.writerow((s_name, s_phone, s_email))

        def _del_old(old_name):
            name = old_name
            with open('contacts_list.csv', 'r') as f:
                reader = list(csv.reader(f))
            with open('contacts_list.csv', 'w') as f:
                writer = csv.writer(f, lineterminator='\r', delimiter=',')
                for i, row in enumerate(reader):
                    if name != row[0]:
                        writer.writerow(row)