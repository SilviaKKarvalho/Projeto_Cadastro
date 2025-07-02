import sqlite3 # banco de dados
import tkinter as tk # interface basica
from tkinter import messagebox # caixas de mensagens
from tkinter import ttk # interface grafica tb

def conectar():
    return sqlite3.connect('cadastro.db')

#Informações importantes: Nome Prestador, e-mail, telefone, atividades agendada e Setor resposável pelo serviço.

# colunas do banco de dados
def criar_tabela():
    conn = conectar()
    c= conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS usuarios(
        tel INTERGER NOT NULL,
        nome TEXT NOT NULL,
        email TEXT NOT NULL,
        ativ TEXT NOT NULL,
        setor TEXT NOT NULL
                            
        )       
    ''')
    conn.commit()
    conn.close()
  


# CREATE
def inserir_usuario():
    nome = entry_nome.get()
    email = entry_email.get()
    tel =   entry_tel.get()
    ativ =  entry_ativ.get()
    setor = entry_setor.get()
   
    if nome and email and tel and ativ and setor:
        conn = conectar()
        c = conn.cursor()
        c.execute('INSERT INTO usuarios(tel,nome,email,ativ,setor) VALUES(?,?,?,?,?)', (tel, nome, email, ativ, setor))
        conn.commit()
        conn.close()
        messagebox.showinfo('AVISO', 'DADOS INSERIDOS COM SUCESSO!') 
        mostrar_usuario()

        # entry_cpf.delete(0,)
        entry_tel.delete(0, tk.END)
        entry_email.delete(0, tk.END)
        entry_nome.delete(0, tk.END)
        entry_ativ.delete(0, tk.END)
        entry_setor.delete(0, tk.END)



    else:
        messagebox.showwarning('ATENÇÃO!', 'INSIRA OS DADOS CORRETAMENTE') 

# READ
def mostrar_usuario():
    for row in tree.get_children():   
        tree.delete(row)
    conn = conectar()
    c = conn.cursor()    
    c.execute('SELECT * FROM usuarios')
    usuarios = c.fetchall()
    for usuario in usuarios:
        tree.insert("", "end", values=(usuario[0], usuario[1],usuario[2], usuario[3], usuario[4]))
    conn.close()    


# DELETE
def delete_usuario():
    dado_del = tree.selection()
    if dado_del:
       user_tel = tree.item(dado_del)['values'][0]
       conn = conectar()
       c = conn.cursor()    
       c.execute('DELETE FROM usuarios WHERE tel = ? ',(user_tel,))
       conn.commit()
       conn.close()
       messagebox.showinfo('', 'DADO DELETADO')
       mostrar_usuario()

    else:
       messagebox.showerror('', 'SELECIONE UM DADO')  

# UPDATE 
       
def editar():
     selecao = tree.selection()
     if selecao:
         user_tel = tree.item(selecao)['values'][0]
         
         novo_nome = entry_nome.get()
         novo_email = entry_email.get()
         novo_ativ = entry_ativ.get()
         novo_setor = entry_setor.get()
         

         if novo_nome and novo_email:
            conn = conectar()
            c = conn.cursor()    
            c.execute('UPDATE usuarios SET nome = ? , email = ?, ativ= ?, setor= ? WHERE tel = ? ',(novo_nome, novo_email, novo_ativ, novo_setor, user_tel))
            conn.commit()
            conn.close()  
            messagebox.showinfo('', 'DADOS ATUALIZADOS')
            mostrar_usuario()

         else:
             messagebox.showwarning('', 'PREENCHA TODOS OS CAMPOS')

     else:
            messagebox.showerror('','SELECIONE A LINHA PARA EDITAR')


janela = tk.Tk()
janela.title('CRUD')
janela.geometry('1920x1080')
janela.configure(bg = 'gray')

titulo = tk.Label(janela, text='Cadastro de Acesso', font=('arial',16))
titulo.grid(row= 0, column=2)

label_nome = tk.Label(janela, text='Nome:', font=('roboto',15))
label_nome.grid(row=1, column=0, padx=10, pady=10, )

entry_nome = tk.Entry(janela, font=('roboto',15))
entry_nome.grid(row=1, column=1, padx=10, pady=10)

label_email = tk.Label(janela, text = 'E-mail:', font=('roboto',15))
label_email.grid(row=2, column=0, padx=10, pady=10)

entry_email = tk.Entry(janela, text = 'E-mail:', font=('roboto',15))
entry_email.grid(row=2, column=1, padx=10, pady=10)



label_tel = tk.Label(janela, text = 'TEL:', font=('roboto',15))
label_tel.grid(row=3, column=0, padx=10, pady=10)

entry_tel = tk.Entry(janela, text = 'TEL:', font=('roboto',15))
entry_tel.grid(row=3, column=1,   pady=10)


label_ativ = tk.Label(janela, text = 'Ativ:', font=('roboto',15))
label_ativ.grid(row=4, column=0, padx=10, pady=10)

entry_ativ = tk.Entry(janela, text = 'Ativ:', font=('roboto',15))
entry_ativ.grid(row=4, column=1,   pady=10)


label_setor = tk.Label(janela, text = 'Setor:', font=('roboto',15))
label_setor.grid(row=5, column=0, padx=10, pady=10)

entry_setor = tk.Entry(janela, text = 'Setor:', font=('roboto',15))
entry_setor.grid(row=5, column=1,   pady=10)


btn_salvar = tk.Button(janela, text='Salvar', command=inserir_usuario,  width=15)
btn_salvar.grid(row= 6, column=1,  pady=10)

btn_deletar = tk.Button(janela, text='deletar', command=delete_usuario , width=15)
btn_deletar.grid(row=6, column=2,  pady=10)

btn_atualizar = tk.Button(janela, text='atualizar', command=editar,  width=15)
btn_atualizar.grid(row=6, column=3,  pady=10)

columns = ('TELEFONE', 'NOME', 'E-MAIL','ATIVIDADE AGENDADA', 'SETOR RESPONSAVEL')
tree = ttk.Treeview(janela, columns=columns, show='headings',)
tree.grid(row = 7, column=0, columnspan= 10, padx=5, pady=10)

for col in columns:
    tree.heading(col, text=col)

criar_tabela()
mostrar_usuario()


janela.mainloop()






# CREATE  -  CRIAR UM NOVO DADO PARA UMA APLICAÇÃO
# READ    -  SISTEMA LE ESSE DADO
# UPDATE  -  SISTEMA ATUALIZAR O DADO
# DELETE  -  DELETAR O DADOS QUE FOI CRIADO