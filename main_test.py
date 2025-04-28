import tkinter as tk
import sqlite3

# Configurando o banco de dados
def configurar_banco():
    conexao = sqlite3.connect("clubes.db")
    cursor = conexao.cursor()

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

# Função para salvar clube
def salvar_clube_no_banco(nome, pais, estado, cores, estadio):
    conexao = sqlite3.connect("clubes.db")
    cursor = conexao.cursor()
    cursor.execute("""
        INSERT INTO clubes (nome, pais, estado, cores, estadio)
        VALUES (?, ?, ?, ?, ?)
    """, (nome, pais, estado, cores, estadio))
    conexao.commit()
    conexao.close()
    atualizar_lista()
    print("Clube salvo no banco de dados!")

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

# Função para abrir a janela de cadastro
def abrir_janela_cadastro():
    janela_cadastro = tk.Toplevel()
    janela_cadastro.title("Cadastro de Clube de Futebol")
    janela_cadastro.geometry("400x400")

    # Campos para cadastro
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
            nome_entry.get(), pais_entry.get(), estado_entry.get(), cores_entry.get(), estadio_entry.get()
        )
    ).pack()

# Janela principal
def main():
    configurar_banco()

    global lista_clubes

    janela_principal = tk.Tk()
    janela_principal.title("App de Futebol")
    janela_principal.geometry("500x400")

    # Lista de clubes
    lista_clubes = tk.Listbox(janela_principal, width=50, height=15)
    lista_clubes.pack()

    # Botões de ação
    tk.Button(janela_principal, text="Cadastrar Clube", command=abrir_janela_cadastro).pack()
    tk.Button(janela_principal, text="Excluir Clube", command=excluir_clube).pack()
    tk.Button(janela_principal, text="Editar Clube", command=editar_clube).pack()

    atualizar_lista()  # Atualiza a lista ao iniciar o app
    janela_principal.mainloop()

if __name__ == "__main__":
    main()