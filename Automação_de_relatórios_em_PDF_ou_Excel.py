"""
=====================================================================
 GERADOR DE RELATÓRIO PDF A PARTIR DE PLANILHA EXCEL
=====================================================================

O que este script faz:
    1. Abre uma janela (tkinter) para o usuário escolher um arquivo .xlsx
    2. Lê os dados da planilha com pandas
    3. Identifica automaticamente quais colunas são numéricas
    4. Gera um gráfico (barras se houver poucas linhas, linha se houver
       muitas linhas) com os dados numéricos encontrados
    5. Monta um relatório em PDF contendo:
         - Nome do arquivo de origem
         - Tabela resumo (média, total, mínimo e máximo) de cada
           coluna numérica
         - O gráfico gerado
    6. Salva o PDF na mesma pasta do Excel original, com o mesmo nome
       (apenas troca a extensão .xlsx por .pdf)

Como instalar as dependências (rode no terminal antes de executar):
    pip install pandas matplotlib fpdf2 openpyxl

Observações importantes:
    - Use "fpdf2" (e não o pacote "fpdf" antigo/clássico, que está
      desatualizado desde 2017). O fpdf2 é importado da mesma forma
      (import fpdf / from fpdf import FPDF), então o código abaixo
      funciona normalmente.
    - "openpyxl" é exigido pelo pandas internamente para ler
      arquivos .xlsx — sem ele o pd.read_excel falha.
    - O tkinter já vem instalado por padrão no Python do Windows e
      do macOS. No Linux, caso não esteja disponível, instale com:
      sudo apt-get install python3-tk
=====================================================================
"""

import os
import tkinter as tk
from tkinter import filedialog, messagebox

import pandas as pd
import matplotlib
matplotlib.use("Agg")  # backend sem interface gráfica (evita conflito com tkinter)
import matplotlib.pyplot as plt

from fpdf import FPDF


def selecionar_arquivo() -> str:
    """Abre uma janela para o usuário escolher um arquivo Excel (.xlsx).

    Retorna o caminho completo do arquivo escolhido, ou uma string
    vazia caso o usuário cancele a seleção.
    """
    janela = tk.Tk()
    janela.withdraw()  # esconde a janela principal, mostra só o diálogo de seleção
    janela.attributes("-topmost", True)  # garante que o diálogo apareça na frente

    caminho = filedialog.askopenfilename(
        title="Selecione um arquivo Excel (.xlsx)",
        filetypes=[("Arquivos Excel", "*.xlsx")],
    )

    janela.destroy()
    return caminho


def identificar_colunas_numericas(df: pd.DataFrame) -> list:
    """Retorna a lista de colunas do DataFrame que são numéricas."""
    return df.select_dtypes(include="number").columns.tolist()


def gerar_grafico(df: pd.DataFrame, colunas_numericas: list, caminho_imagem: str) -> None:
    """Gera um gráfico com as colunas numéricas e salva como imagem PNG.

    Regra usada: se a planilha tiver poucas linhas (<=15), um gráfico
    de barras facilita a comparação direta entre categorias. Se tiver
    muitas linhas, um gráfico de linha representa melhor a tendência
    dos dados ao longo do tempo/índice.
    """
    plt.figure(figsize=(8, 4.5))

    if len(df) <= 15:
        df[colunas_numericas].plot(kind="bar", ax=plt.gca())
    else:
        df[colunas_numericas].plot(kind="line", ax=plt.gca())

    plt.title("Dados Numéricos da Planilha")
    plt.xlabel("Índice (linha da planilha)")
    plt.ylabel("Valor")
    plt.legend(loc="best")
    plt.tight_layout()
    plt.savefig(caminho_imagem, dpi=150)
    plt.close()


def calcular_resumo(df: pd.DataFrame, colunas_numericas: list) -> pd.DataFrame:
    """Calcula média, total (soma), mínimo e máximo de cada coluna numérica."""
    resumo = pd.DataFrame({
        "Media": df[colunas_numericas].mean(),
        "Total": df[colunas_numericas].sum(),
        "Minimo": df[colunas_numericas].min(),
        "Maximo": df[colunas_numericas].max(),
    })
    return resumo.round(2)


def gerar_pdf(nome_arquivo_original: str, resumo: pd.DataFrame,
              caminho_imagem: str, caminho_pdf: str) -> None:
    """Monta o relatório em PDF: título, nome do arquivo, tabela resumo e gráfico."""
    pdf = FPDF()
    pdf.add_page()

    # --- Título do relatório ---
    pdf.set_font("Helvetica", "B", 16)
    pdf.cell(0, 10, "Relatório de Análise de Dados", new_x="LMARGIN", new_y="NEXT", align="C")
    pdf.ln(4)

    # --- Nome do arquivo de origem ---
    pdf.set_font("Helvetica", "", 11)
    pdf.cell(0, 8, f"Arquivo de origem: {nome_arquivo_original}", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(4)

    # --- Tabela resumo ---
    pdf.set_font("Helvetica", "B", 12)
    pdf.cell(0, 8, "Tabela Resumo", new_x="LMARGIN", new_y="NEXT")

    largura_coluna_nome = 50   # coluna com o nome da variável (mais larga)
    largura_coluna_valor = 35  # colunas de média/total/mínimo/máximo
    altura_linha = 8

    # Cabeçalho da tabela
    pdf.set_font("Helvetica", "B", 10)
    pdf.cell(largura_coluna_nome, altura_linha, "Coluna", border=1)
    for nome_stat in resumo.columns:
        pdf.cell(largura_coluna_valor, altura_linha, nome_stat, border=1, align="C")
    pdf.ln(altura_linha)

    # Linhas da tabela (uma por coluna numérica encontrada)
    pdf.set_font("Helvetica", "", 10)
    for nome_coluna, linha in resumo.iterrows():
        pdf.cell(largura_coluna_nome, altura_linha, str(nome_coluna), border=1)
        for valor in linha:
            pdf.cell(largura_coluna_valor, altura_linha, str(valor), border=1, align="C")
        pdf.ln(altura_linha)

    pdf.ln(8)

    # --- Gráfico ---
    pdf.set_font("Helvetica", "B", 12)
    pdf.cell(0, 8, "Gráfico", new_x="LMARGIN", new_y="NEXT")
    pdf.image(caminho_imagem, x=10, w=190)

    pdf.output(caminho_pdf)


def main() -> None:
    # 1. Seleção do arquivo Excel pelo usuário
    caminho_excel = selecionar_arquivo()
    if not caminho_excel:
        print("Nenhum arquivo selecionado. Encerrando o programa.")
        return

    # 2. Leitura dos dados com pandas
    try:
        df = pd.read_excel(caminho_excel)
    except Exception as erro:
        messagebox.showerror("Erro ao ler o arquivo", f"Não foi possível ler o arquivo:\n{erro}")
        return

    if df.empty:
        messagebox.showwarning("Aviso", "A planilha selecionada está vazia.")
        return

    # 3. Identificação automática das colunas numéricas
    colunas_numericas = identificar_colunas_numericas(df)
    if not colunas_numericas:
        messagebox.showwarning(
            "Aviso", "Nenhuma coluna numérica foi encontrada nesta planilha."
        )
        return

    # Monta os caminhos de saída com o mesmo nome do arquivo original
    pasta = os.path.dirname(caminho_excel) or "."
    nome_base = os.path.splitext(os.path.basename(caminho_excel))[0]
    caminho_imagem_temp = os.path.join(pasta, f"_grafico_temp_{nome_base}.png")
    caminho_pdf = os.path.join(pasta, f"{nome_base}.pdf")

    try:
        # 4. Geração do gráfico
        gerar_grafico(df, colunas_numericas, caminho_imagem_temp)

        # 5. Cálculo do resumo e geração do PDF
        resumo = calcular_resumo(df, colunas_numericas)
        gerar_pdf(os.path.basename(caminho_excel), resumo, caminho_imagem_temp, caminho_pdf)
    except Exception as erro:
        messagebox.showerror("Erro ao gerar relatório", f"Ocorreu um erro:\n{erro}")
        return
    finally:
        # Remove a imagem temporária usada apenas para montar o PDF
        if os.path.exists(caminho_imagem_temp):
            os.remove(caminho_imagem_temp)

    # 6. Avisa o usuário que o PDF foi salvo com sucesso
    print(f"Relatório gerado com sucesso em: {caminho_pdf}")
    messagebox.showinfo("Sucesso", f"Relatório PDF gerado com sucesso:\n{caminho_pdf}")


if __name__ == "__main__":
    main()
