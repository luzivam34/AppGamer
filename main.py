import tkinter as tk
import sqlite3

#configuração do banco de dados
def config_bd():
    conexao = sqlite3.connect("clubes.db")  # Criar ou conactar ao Banco de dados
    cursor = conexao.cursor()

    # Criar uma tabela se não existir
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

# Função para atualizar a lista de clubes no app
def atualizar_lista():
    conexao = sqlite3.connect("clubes.db")
    cursor = conexao.cursor()
    cursor.execute("SELECT * FROM clubes")
    clubes = cursor.fetchall()
    conexao.close()

    lista_clubes.delete(0, tk.END)  # Limpa a lista atual
    for clube in clubes:
        lista_clubes.insert(tk.END, f"{clube[0]} - {clube[1]}")  # Exibe ID e nome


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

# Função para excluir clube
def excluir_clube():
    selecao = lista_clubes.get(tk.ACTIVE)
    if not selecao:
        return
    clube_id = selecao.split(" - ")[0]  # Obtém o ID do clube
    conexao = sqlite3.connect("clubes.db")
    cursor = conexao.cursor()
    cursor.execute("DELETE FROM clubes WHERE id = ?", (clube_id,))
    conexao.commit()
    conexao.close()
    atualizar_lista()
    print(f"Clube {clube_id} excluído!")

# Função para editar um clube
def editar_clube():
    selecao = lista_clubes.get(tk.ACTIVE)
    if not selecao:
        return
    clube_id = selecao.split(" - ")[0]  # Obtém o ID do clube

    # Janela de edição
    janela_edicao = tk.Toplevel()
    janela_edicao.title("Editar Clube")
    janela_edicao.geometry("400x400")

    # Obtém os dados do clube
    conexao = sqlite3.connect("clubes.db")
    cursor = conexao.cursor()
    cursor.execute("SELECT * FROM clubes WHERE id = ?", (clube_id,))
    clube = cursor.fetchone()
    conexao.close()

    # Campos para edição
    tk.Label(janela_edicao, text="Nome:").pack()
    nome_entry = tk.Entry(janela_edicao)
    nome_entry.insert(0, clube[1])
    nome_entry.pack()

    tk.Label(janela_edicao, text="País:").pack()
    pais_entry = tk.Entry(janela_edicao)
    pais_entry.insert(0, clube[2])
    pais_entry.pack()

    tk.Label(janela_edicao, text="Estado:").pack()
    estado_entry = tk.Entry(janela_edicao)
    estado_entry.insert(0, clube[3])
    estado_entry.pack()

    tk.Label(janela_edicao, text="Principais cores:").pack()
    cores_entry = tk.Entry(janela_edicao)
    cores_entry.insert(0, clube[4])
    cores_entry.pack()

    tk.Label(janela_edicao, text="Estádio:").pack()
    estadio_entry = tk.Entry(janela_edicao)
    estadio_entry.insert(0, clube[5])
    estadio_entry.pack()

    tk.Button(
        janela_edicao,
        text="Salvar Alterações",
        command=lambda: salvar_edicoes(clube_id, nome_entry.get(), pais_entry.get(), estado_entry.get(), cores_entry.get(), estadio_entry.get())
    ).pack()

def salvar_edicoes(clube_id, nome, pais, estado, cores, estadio):
    conexao = sqlite3.connect("clubes.db")
    cursor = conexao.cursor()
    cursor.execute("""
        UPDATE clubes
        SET nome = ?, pais = ?, estado = ?, cores = ?, estadio = ?
        WHERE id = ?
    """, (nome, pais, estado, cores, estadio, clube_id))
    conexao.commit()
    conexao.close()
    atualizar_lista()
    print(f"Clube {clube_id} atualizado!")


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

    global lista_clubes

    janela  = tk.Tk()
    janela.title("Meu app de Futball")
    janela.geometry("500x400") #DEfine o tamanha da Janela

    # Lista de clubes
    lista_clubes = tk.Listbox(janela, width=50, height=15)
    lista_clubes.pack()


    tk.Label(janela, text="Bem vindo").pack()
    tk.Button(janela, text="Cadastrar", command=cadastro).pack()
    tk.Button(janela, text="Excluir Clube", command=excluir_clube).pack()
    tk.Button(janela, text="Editar Clube", command=editar_clube).pack()


    janela.mainloop() #Mantém a janela aberta

if __name__ == "__main__":
    main()