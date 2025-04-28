import tkinter as tk
import sqlite3

# Configurando o banco de dados
def configurar_banco():
    conexao = sqlite3.connect("clubes.db")  # Cria ou conecta ao banco de dados
    cursor = conexao.cursor()
    # Cria a tabela se não existir
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS clubes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            pais TEXT NOT NULL,
            estado TEXT NOT NULL,
            cores TEXT NOT NULL,
            estadio TEXT NOT NULL
        )
    """)
    conexao.commit()
    conexao.close()

def salvar_clube_no_banco(nome, pais, estado, cores, estadio):
    conexao = sqlite3.connect("clubes.db")
    cursor = conexao.cursor()
    # Insere os dados no banco
    cursor.execute("""
        INSERT INTO clubes (nome, pais, estado, cores, estadio)
        VALUES (?, ?, ?, ?, ?)
    """, (nome, pais, estado, cores, estadio))
    conexao.commit()
    conexao.close()
    print("Clube salvo no banco de dados!")

# Função para abrir a janela de cadastro
def abrir_janela_cadastro():
    janela_cadastro = tk.Toplevel()
    janela_cadastro.title("Cadastro de Clube de Futebol")
    janela_cadastro.geometry("400x400")

    # Labels e campos de entrada
    tk.Label(janela_cadastro, text="Nome:").pack()
    nome_entry = tk.Entry(janela_cadastro)
    nome_entry.pack()

    tk.Label(janela_cadastro, text="País:").pack()
    pais_entry = tk.Entry(janela_cadastro)
    pais_entry.pack()

    tk.Label(janela_cadastro, text="Estado:").pack()
    estado_entry = tk.Entry(janela_cadastro)
    estado_entry.pack()

    tk.Label(janela_cadastro, text="Principais cores:").pack()
    cores_entry = tk.Entry(janela_cadastro)
    cores_entry.pack()

    tk.Label(janela_cadastro, text="Estádio:").pack()
    estadio_entry = tk.Entry(janela_cadastro)
    estadio_entry.pack()

    tk.Button(
        janela_cadastro,
        text="Salvar",
        command=lambda: salvar_clube_no_banco(
            nome_entry.get(),
            pais_entry.get(),
            estado_entry.get(),
            cores_entry.get(),
            estadio_entry.get()
        )
    ).pack()

# Janela principal
def main():
    configurar_banco()  # Configura o banco antes de iniciar o app

    janela_principal = tk.Tk()
    janela_principal.title("App de Futebol")
    janela_principal.geometry("300x200")

    tk.Label(janela_principal, text="Bem-vindo ao app!").pack()
    tk.Button(janela_principal, text="Cadastrar Clube", command=abrir_janela_cadastro).pack()

    janela_principal.mainloop()

if __name__ == "__main__":
    main()