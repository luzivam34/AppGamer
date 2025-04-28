import tkinter as tk
import sqlite3

#configuração do banco de dados
def config_bd():
    conexao = sqlite3.connect("clubes.db") # Criar ou conactar ao Banco de dados
    cursor = conexao.cursor()
    # Criar uma tabela se não existir
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS clubes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        pais TEXT NOT NULL,
        estado TEXT NOT NULL,
        cores TEXT NOT NULL,
        estadio TEXT NOT NULL,
    )
    """)
    conexao.commit()
    conexao.close()

def salvar_clube(nome, pais, estado, cores, estadio):
    conexao = sqlite3.connect("clubes.db")
    cursor = conexao.cursor()
    # insere os dados no banco de dados
    cursor.execute("""
        INSERT INTO clubes (nome, pais, estado, cores, estadio)
        VALUES (?, ?, ?, ?, ?)
    """, (nome, pais, estado, cores, estadio))
    conexao.commit()
    conexao.close()
    print("Clubes salvos no Banco de Dados!")

def cadastro():
    jan_cadastro = tk.Toplevel() #Cria uma nova janela
    jan_cadastro.title("Cadastro de Clubes")
    jan_cadastro.geometry("400x400")

    #Labels e campos de entrada
    tk.Label(jan_cadastro, text="Nome: ").pack()
    nome_entry = tk.Entry(jan_cadastro)
    nome_entry.pack()

    tk.Label(jan_cadastro, text="País: ").pack()
    pais_entry = tk.Entry(jan_cadastro)
    pais_entry.pack()

    tk.Label(jan_cadastro, text="Estado: ").pack()
    estado_entry = tk.Entry(jan_cadastro)
    estado_entry.pack()

    tk.Label(jan_cadastro, text="Principais Cores: ").pack()
    cores_entry = tk.Entry(jan_cadastro)
    cores_entry.pack()

    tk.Label(jan_cadastro, text="Estádio: ").pack()
    estadio_entry = tk.Entry(jan_cadastro)
    estadio_entry.pack()

    tk.Button(
        jan_cadastro,
        text="Salvar",
        command=lambda: salvar_clube(
            nome_entry.get(),
            pais_entry.get(),
            estado_entry.get(),
            cores_entry.get(),
            estadio_entry.get()
        )
    ).pack()

#Janela principal
def main():
    config_bd() # configurar o banco antes de iniciar o app

    janela  = tk.Tk()
    janela.title("Meu app de Futball")
    janela.geometry("300x200") #DEfine o tamanha da Janela

    tk.Label(janela, text="Bem vindo").pack()
    tk.Button(janela, text="Cadastrar", command=cadastro).pack()

    janela.mainloop() #Mantém a janela aberta

if __name__ == "__main__":
    main()