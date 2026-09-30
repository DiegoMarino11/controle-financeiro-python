import customtkinter as ctk
import json
import os
from datetime import datetime
from tkinter import messagebox


# ==========================================================
# CONFIGURAÇÕES
# ==========================================================

ARQUIVO = "despesas.json"

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

tema_atual = "dark"


CATEGORIAS = [
    "Alimentação",
    "Moradia",
    "Transporte",
    "Saúde",
    "Educação",
    "Lazer",
    "Eletrônicos",
    "Compras",
    "Assinaturas",
    "Contas",
    "Outros"
]


TIPOS = [
    "Fixo",
    "Variável",
    "Parcelado"
]


# ==========================================================
# DADOS
# ==========================================================

def carregar_despesas():

    if not os.path.exists(ARQUIVO):
        return []

    try:

        with open(
            ARQUIVO,
            "r",
            encoding="utf-8"
        ) as arquivo:

            return json.load(arquivo)

    except (json.JSONDecodeError, FileNotFoundError):

        return []


def salvar_despesas():

    with open(
        ARQUIVO,
        "w",
        encoding="utf-8"
    ) as arquivo:

        json.dump(
            despesas,
            arquivo,
            ensure_ascii=False,
            indent=4
        )


despesas = carregar_despesas()


# ==========================================================
# JANELA PRINCIPAL
# ==========================================================

app = ctk.CTk()

app.title("Controle de Despesas")

app.geometry("1300x750")

app.minsize(1100, 650)


# ==========================================================
# FUNÇÕES AUXILIARES
# ==========================================================

def formatar_moeda(valor):

    return (
        f"R$ {valor:,.2f}"
        .replace(",", "X")
        .replace(".", ",")
        .replace("X", ".")
    )


def limpar_conteudo():

    for widget in conteudo.winfo_children():

        widget.destroy()


# ==========================================================
# VALOR REAL DA DESPESA PARA O USUÁRIO
# ==========================================================

def obter_valor_usuario(despesa):

    dividir = despesa.get(
        "dividir",
        False
    )

    valor = despesa.get(
        "valor",
        0
    )


    # ------------------------------------------------------
    # DESPESA NORMAL
    # ------------------------------------------------------

    if not dividir:

        return valor


    # ------------------------------------------------------
    # DIVISÃO PERSONALIZADA
    # ------------------------------------------------------

    if not despesa.get(
        "divisao_igual",
        True
    ):

        return despesa.get(
            "minha_parte",
            valor
        )


    # ------------------------------------------------------
    # DIVISÃO IGUAL
    # ------------------------------------------------------

    numero_pessoas = despesa.get(
        "numero_pessoas",
        1
    )


    if numero_pessoas <= 0:

        return valor


    return valor / numero_pessoas


# ==========================================================
# TEXTO DA DIVISÃO
# ==========================================================

def obter_texto_divisao(despesa):

    if not despesa.get(
        "dividir",
        False
    ):

        return ""


    numero_pessoas = despesa.get(
        "numero_pessoas",
        1
    )


    minha_parte = obter_valor_usuario(
        despesa
    )


    if despesa.get(
        "divisao_igual",
        True
    ):

        return (
            f"   |   "
            f"👥 {numero_pessoas} pessoas"
            f"   |   "
            f"Sua parte: "
            f"{formatar_moeda(minha_parte)}"
        )


    return (
        f"   |   "
        f"👥 {numero_pessoas} pessoas"
        f"   |   "
        f"Sua parte: "
        f"{formatar_moeda(minha_parte)}"
    )


# ==========================================================
# ALTERAR TEMA
# ==========================================================

def alternar_tema():

    global tema_atual

    if tema_atual == "dark":

        tema_atual = "light"

        ctk.set_appearance_mode("light")

        botao_tema.configure(
            text="🌙  Tema escuro"
        )

    else:

        tema_atual = "dark"

        ctk.set_appearance_mode("dark")

        botao_tema.configure(
            text="☀️  Tema claro"
        )


# ==========================================================
# CAMPOS DE PARCELAMENTO
# ==========================================================

def atualizar_campos_parcelamento():

    if entrada_tipo.get() == "Parcelado":

        frame_parcelamento.grid(
            row=3,
            column=0,
            columnspan=3,
            sticky="w",
            padx=10,
            pady=(0, 10)
        )

    else:

        frame_parcelamento.grid_remove()


# ==========================================================
# CAMPOS DE DIVISÃO
# ==========================================================

def atualizar_campos_divisao():

    if variavel_dividir.get():

        frame_divisao.grid(
            row=5,
            column=0,
            columnspan=3,
            sticky="ew",
            padx=10,
            pady=(0, 10)
        )

        atualizar_tipo_divisao()

    else:

        frame_divisao.grid_remove()


# ==========================================================
# TIPO DE DIVISÃO
# ==========================================================

def atualizar_tipo_divisao():

    if not variavel_dividir.get():

        return


    if variavel_divisao_igual.get():

        frame_minha_parte.grid_remove()

        label_resultado_divisao.configure(
            text="Sua parte será calculada automaticamente."
        )

    else:

        frame_minha_parte.grid(
            row=2,
            column=0,
            columnspan=2,
            sticky="w",
            pady=(10, 0)
        )

        label_resultado_divisao.configure(
            text="Informe quanto será a sua parte."
        )


# ==========================================================
# ATUALIZAR VALOR DA DIVISÃO
# ==========================================================

def atualizar_preview_divisao():

    if not variavel_dividir.get():

        return


    valor_texto = (
        entrada_valor
        .get()
        .strip()
        .replace(",", ".")
    )


    try:

        valor = float(valor_texto)

    except ValueError:

        label_resultado_divisao.configure(
            text="Digite um valor válido."
        )

        return


    if valor <= 0:

        label_resultado_divisao.configure(
            text="Digite um valor maior que zero."
        )

        return


    if variavel_divisao_igual.get():

        try:

            pessoas = int(
                entrada_numero_pessoas.get()
            )

            if pessoas <= 0:

                raise ValueError

        except ValueError:

            label_resultado_divisao.configure(
                text="Informe o número de pessoas."
            )

            return


        minha_parte = valor / pessoas


        label_resultado_divisao.configure(
            text=(
                f"Sua parte: "
                f"{formatar_moeda(minha_parte)}"
            )
        )

    else:

        minha_parte_texto = (
            entrada_minha_parte
            .get()
            .strip()
            .replace(",", ".")
        )


        try:

            minha_parte = float(
                minha_parte_texto
            )

        except ValueError:

            label_resultado_divisao.configure(
                text="Informe sua parte."
            )

            return


        if minha_parte < 0:

            label_resultado_divisao.configure(
                text="Sua parte não pode ser negativa."
            )

            return


        if minha_parte > valor:

            label_resultado_divisao.configure(
                text=(
                    "Sua parte não pode ser "
                    "maior que o valor total."
                )
            )

            return


        label_resultado_divisao.configure(
            text=(
                f"Sua parte: "
                f"{formatar_moeda(minha_parte)}"
            )
        )


# ==========================================================
# ADICIONAR DESPESA
# ==========================================================

def adicionar_despesa():

    descricao = (
        entrada_descricao
        .get()
        .strip()
    )


    valor_texto = (
        entrada_valor
        .get()
        .strip()
        .replace(",", ".")
    )


    tipo = entrada_tipo.get()

    categoria = entrada_categoria.get()


    # ------------------------------------------------------
    # DESCRIÇÃO
    # ------------------------------------------------------

    if not descricao:

        messagebox.showwarning(
            "Atenção",
            "Digite uma descrição."
        )

        return


    # ------------------------------------------------------
    # VALOR
    # ------------------------------------------------------

    try:

        valor = float(
            valor_texto
        )

        if valor <= 0:

            raise ValueError

    except ValueError:

        messagebox.showwarning(
            "Atenção",
            "Digite um valor válido."
        )

        return


    # ------------------------------------------------------
    # CATEGORIA
    # ------------------------------------------------------

    if not categoria:

        messagebox.showwarning(
            "Atenção",
            "Selecione uma categoria."
        )

        return


    # ------------------------------------------------------
    # PARCELAMENTO
    # ------------------------------------------------------

    total_parcelas = None

    parcelas_pagas = None


    if tipo == "Parcelado":

        try:

            total_parcelas = int(
                entrada_total_parcelas
                .get()
            )

            parcelas_pagas = int(
                entrada_parcelas_pagas
                .get()
            )

            if total_parcelas <= 0:

                raise ValueError

            if parcelas_pagas < 0:

                raise ValueError

            if parcelas_pagas > total_parcelas:

                raise ValueError

        except ValueError:

            messagebox.showwarning(
                "Atenção",
                (
                    "Informe corretamente o total "
                    "de parcelas e as parcelas já pagas."
                )
            )

            return


    # ------------------------------------------------------
    # DIVISÃO
    # ------------------------------------------------------

    dividir = variavel_dividir.get()

    numero_pessoas = 1

    divisao_igual = True

    minha_parte = valor


    if dividir:

        try:

            numero_pessoas = int(
                entrada_numero_pessoas
                .get()
            )

            if numero_pessoas < 2:

                raise ValueError

        except ValueError:

            messagebox.showwarning(
                "Atenção",
                "Informe pelo menos 2 pessoas."
            )

            return


        divisao_igual = (
            variavel_divisao_igual.get()
        )


        # ----------------------------------------------
        # DIVISÃO IGUAL
        # ----------------------------------------------

        if divisao_igual:

            minha_parte = (
                valor / numero_pessoas
            )


        # ----------------------------------------------
        # VALOR PERSONALIZADO
        # ----------------------------------------------

        else:

            minha_parte_texto = (
                entrada_minha_parte
                .get()
                .strip()
                .replace(",", ".")
            )


            try:

                minha_parte = float(
                    minha_parte_texto
                )

            except ValueError:

                messagebox.showwarning(
                    "Atenção",
                    "Informe sua parte."
                )

                return


            if minha_parte < 0:

                messagebox.showwarning(
                    "Atenção",
                    "Sua parte não pode ser negativa."
                )

                return


            if minha_parte > valor:

                messagebox.showwarning(
                    "Atenção",
                    "Sua parte não pode ser maior que o valor total."
                )

                return


    # ------------------------------------------------------
    # CRIAR DESPESA
    # ------------------------------------------------------

    nova_despesa = {

        "descricao": descricao,

        "valor": valor,

        "tipo": tipo,

        "categoria": categoria,

        "total_parcelas": total_parcelas,

        "parcelas_pagas": parcelas_pagas,

        "dividir": dividir,

        "numero_pessoas": numero_pessoas,

        "divisao_igual": divisao_igual,

        "minha_parte": minha_parte,

        "data": datetime.now().strftime(
            "%d/%m/%Y"
        )
    }


    despesas.append(
        nova_despesa
    )

    salvar_despesas()


    # ------------------------------------------------------
    # LIMPAR CAMPOS
    # ------------------------------------------------------

    entrada_descricao.delete(
        0,
        "end"
    )

    entrada_valor.delete(
        0,
        "end"
    )

    entrada_tipo.set(
        "Variável"
    )

    entrada_categoria.set(
        "Alimentação"
    )

    entrada_total_parcelas.delete(
        0,
        "end"
    )

    entrada_parcelas_pagas.delete(
        0,
        "end"
    )

    entrada_numero_pessoas.delete(
        0,
        "end"
    )

    entrada_minha_parte.delete(
        0,
        "end"
    )

    variavel_dividir.set(
        False
    )

    variavel_divisao_igual.set(
        True
    )


    atualizar_campos_parcelamento()

    atualizar_campos_divisao()


    messagebox.showinfo(
        "Sucesso",
        "Despesa adicionada com sucesso!"
    )


    mostrar_inicio()


# ==========================================================
# EDITAR DESPESA
# ==========================================================

def editar_despesa(indice):

    despesa = despesas[indice]


    janela = ctk.CTkToplevel(
        app
    )

    janela.title(
        "Editar despesa"
    )

    janela.geometry(
        "550x700"
    )

    janela.resizable(
        False,
        False
    )

    janela.grab_set()


    # ------------------------------------------------------
    # TÍTULO
    # ------------------------------------------------------

    ctk.CTkLabel(
        janela,
        text="✏️ Editar despesa",
        font=ctk.CTkFont(
            size=24,
            weight="bold"
        )
    ).pack(
        pady=(25, 20)
    )


    # ------------------------------------------------------
    # DESCRIÇÃO
    # ------------------------------------------------------

    ctk.CTkLabel(
        janela,
        text="Descrição",
        anchor="w"
    ).pack(
        fill="x",
        padx=40
    )


    campo_descricao = ctk.CTkEntry(
        janela
    )

    campo_descricao.pack(
        fill="x",
        padx=40,
        pady=(5, 15)
    )

    campo_descricao.insert(
        0,
        despesa.get(
            "descricao",
            ""
        )
    )


    # ------------------------------------------------------
    # VALOR
    # ------------------------------------------------------

    ctk.CTkLabel(
        janela,
        text="Valor total / valor da parcela",
        anchor="w"
    ).pack(
        fill="x",
        padx=40
    )


    campo_valor = ctk.CTkEntry(
        janela
    )

    campo_valor.pack(
        fill="x",
        padx=40,
        pady=(5, 15)
    )

    campo_valor.insert(
        0,
        str(
            despesa.get(
                "valor",
                0
            )
        ).replace(
            ".",
            ","
        )
    )


    # ------------------------------------------------------
    # TIPO
    # ------------------------------------------------------

    ctk.CTkLabel(
        janela,
        text="Tipo",
        anchor="w"
    ).pack(
        fill="x",
        padx=40
    )


    campo_tipo = ctk.CTkComboBox(
        janela,
        values=TIPOS
    )

    campo_tipo.pack(
        fill="x",
        padx=40,
        pady=(5, 15)
    )

    campo_tipo.set(
        despesa.get(
            "tipo",
            "Variável"
        )
    )


    # ------------------------------------------------------
    # CATEGORIA
    # ------------------------------------------------------

    ctk.CTkLabel(
        janela,
        text="Categoria",
        anchor="w"
    ).pack(
        fill="x",
        padx=40
    )


    campo_categoria = ctk.CTkComboBox(
        janela,
        values=CATEGORIAS
    )

    campo_categoria.pack(
        fill="x",
        padx=40,
        pady=(5, 15)
    )

    campo_categoria.set(
        despesa.get(
            "categoria",
            "Outros"
        )
    )


    # ------------------------------------------------------
    # PARCELAMENTO
    # ------------------------------------------------------

    frame_edicao_parcelamento = ctk.CTkFrame(
        janela,
        fg_color="transparent"
    )


    ctk.CTkLabel(
        frame_edicao_parcelamento,
        text="Total"
    ).grid(
        row=0,
        column=0,
        padx=(0, 5)
    )


    campo_total_parcelas = ctk.CTkEntry(
        frame_edicao_parcelamento,
        width=80
    )

    campo_total_parcelas.grid(
        row=0,
        column=1,
        padx=5
    )


    ctk.CTkLabel(
        frame_edicao_parcelamento,
        text="Já pagas"
    ).grid(
        row=0,
        column=2,
        padx=(20, 5)
    )


    campo_parcelas_pagas = ctk.CTkEntry(
        frame_edicao_parcelamento,
        width=80
    )

    campo_parcelas_pagas.grid(
        row=0,
        column=3,
        padx=5
    )


    campo_total_parcelas.insert(
        0,
        str(
            despesa.get(
                "total_parcelas",
                ""
            )
            or ""
        )
    )


    campo_parcelas_pagas.insert(
        0,
        str(
            despesa.get(
                "parcelas_pagas",
                ""
            )
            if despesa.get(
                "parcelas_pagas"
            ) is not None
            else ""
        )
    )


    # ------------------------------------------------------
    # DIVISÃO
    # ------------------------------------------------------

    variavel_editar_dividir = ctk.BooleanVar(
        value=despesa.get(
            "dividir",
            False
        )
    )


    ctk.CTkCheckBox(
        janela,
        text="👥 Dividir esta despesa",
        variable=variavel_editar_dividir
    ).pack(
        anchor="w",
        padx=40,
        pady=(15, 10)
    )


    frame_edicao_divisao = ctk.CTkFrame(
        janela,
        fg_color="transparent"
    )


    ctk.CTkLabel(
        frame_edicao_divisao,
        text="Número de pessoas:"
    ).grid(
        row=0,
        column=0,
        padx=(0, 10)
    )


    campo_numero_pessoas = ctk.CTkEntry(
        frame_edicao_divisao,
        width=80
    )

    campo_numero_pessoas.grid(
        row=0,
        column=1
    )


    campo_numero_pessoas.insert(
        0,
        str(
            despesa.get(
                "numero_pessoas",
                2
            )
        )
    )


    variavel_editar_divisao_igual = ctk.BooleanVar(
        value=despesa.get(
            "divisao_igual",
            True
        )
    )


    ctk.CTkRadioButton(
        frame_edicao_divisao,
        text="Dividir igualmente",
        variable=variavel_editar_divisao_igual,
        value=True
    ).grid(
        row=1,
        column=0,
        columnspan=2,
        sticky="w",
        pady=(15, 5)
    )


    ctk.CTkRadioButton(
        frame_edicao_divisao,
        text="Definir minha parte",
        variable=variavel_editar_divisao_igual,
        value=False
    ).grid(
        row=2,
        column=0,
        columnspan=2,
        sticky="w",
        pady=5
    )


    ctk.CTkLabel(
        frame_edicao_divisao,
        text="Minha parte:"
    ).grid(
        row=3,
        column=0,
        sticky="w",
        pady=(10, 0)
    )


    campo_minha_parte = ctk.CTkEntry(
        frame_edicao_divisao,
        width=100
    )

    campo_minha_parte.grid(
        row=3,
        column=1,
        padx=10,
        pady=(10, 0)
    )


    valor_inicial_minha_parte = despesa.get(
        "minha_parte",
        despesa.get(
            "valor",
            0
        )
    )


    campo_minha_parte.insert(
        0,
        str(
            valor_inicial_minha_parte
        ).replace(
            ".",
            ","
        )
    )


    # ------------------------------------------------------
    # ATUALIZAR VISIBILIDADE
    # ------------------------------------------------------

    def atualizar_edicao():

        if campo_tipo.get() == "Parcelado":

            frame_edicao_parcelamento.pack(
                fill="x",
                padx=40,
                pady=(0, 10)
            )

        else:

            frame_edicao_parcelamento.pack_forget()


        if variavel_editar_dividir.get():

            frame_edicao_divisao.pack(
                fill="x",
                padx=40,
                pady=(0, 10)
            )

        else:

            frame_edicao_divisao.pack_forget()


        if variavel_editar_divisao_igual.get():

            campo_minha_parte.configure(
                state="disabled"
            )

        else:

            campo_minha_parte.configure(
                state="normal"
            )


    campo_tipo.configure(
        command=lambda _: atualizar_edicao()
    )


    variavel_editar_dividir.trace_add(
        "write",
        lambda *args: atualizar_edicao()
    )


    variavel_editar_divisao_igual.trace_add(
        "write",
        lambda *args: atualizar_edicao()
    )


    atualizar_edicao()


    # ------------------------------------------------------
    # SALVAR ALTERAÇÕES
    # ------------------------------------------------------

    def salvar_edicao():

        nova_descricao = (
            campo_descricao
            .get()
            .strip()
        )


        novo_valor_texto = (
            campo_valor
            .get()
            .strip()
            .replace(",", ".")
        )


        novo_tipo = campo_tipo.get()

        nova_categoria = campo_categoria.get()


        # ----------------------------------------------
        # DESCRIÇÃO
        # ----------------------------------------------

        if not nova_descricao:

            messagebox.showwarning(
                "Atenção",
                "Digite uma descrição.",
                parent=janela
            )

            return


        # ----------------------------------------------
        # VALOR
        # ----------------------------------------------

        try:

            novo_valor = float(
                novo_valor_texto
            )

            if novo_valor <= 0:

                raise ValueError

        except ValueError:

            messagebox.showwarning(
                "Atenção",
                "Digite um valor válido.",
                parent=janela
            )

            return


        # ----------------------------------------------
        # CATEGORIA
        # ----------------------------------------------

        if not nova_categoria:

            messagebox.showwarning(
                "Atenção",
                "Selecione uma categoria.",
                parent=janela
            )

            return


        # ----------------------------------------------
        # PARCELAMENTO
        # ----------------------------------------------

        novo_total_parcelas = None

        novas_parcelas_pagas = None


        if novo_tipo == "Parcelado":

            try:

                novo_total_parcelas = int(
                    campo_total_parcelas
                    .get()
                )

                novas_parcelas_pagas = int(
                    campo_parcelas_pagas
                    .get()
                )

                if novo_total_parcelas <= 0:

                    raise ValueError

                if novas_parcelas_pagas < 0:

                    raise ValueError

                if novas_parcelas_pagas > novo_total_parcelas:

                    raise ValueError

            except ValueError:

                messagebox.showwarning(
                    "Atenção",
                    (
                        "Informe corretamente o total "
                        "de parcelas e as parcelas já pagas."
                    ),
                    parent=janela
                )

                return


        # ----------------------------------------------
        # DIVISÃO
        # ----------------------------------------------

        dividir = (
            variavel_editar_dividir.get()
        )

        numero_pessoas = 1

        divisao_igual = True

        nova_minha_parte = novo_valor


        if dividir:

            try:

                numero_pessoas = int(
                    campo_numero_pessoas
                    .get()
                )

                if numero_pessoas < 2:

                    raise ValueError

            except ValueError:

                messagebox.showwarning(
                    "Atenção",
                    "Informe pelo menos 2 pessoas.",
                    parent=janela
                )

                return


            divisao_igual = (
                variavel_editar_divisao_igual.get()
            )


            if divisao_igual:

                nova_minha_parte = (
                    novo_valor
                    / numero_pessoas
                )

            else:

                minha_parte_texto = (
                    campo_minha_parte
                    .get()
                    .strip()
                    .replace(",", ".")
                )


                try:

                    nova_minha_parte = float(
                        minha_parte_texto
                    )

                except ValueError:

                    messagebox.showwarning(
                        "Atenção",
                        "Informe sua parte.",
                        parent=janela
                    )

                    return


                if nova_minha_parte < 0:

                    messagebox.showwarning(
                        "Atenção",
                        "Sua parte não pode ser negativa.",
                        parent=janela
                    )

                    return


                if nova_minha_parte > novo_valor:

                    messagebox.showwarning(
                        "Atenção",
                        "Sua parte não pode ser maior que o valor total.",
                        parent=janela
                    )

                    return


        # ----------------------------------------------
        # ATUALIZAR
        # ----------------------------------------------

        despesas[indice]["descricao"] = (
            nova_descricao
        )

        despesas[indice]["valor"] = (
            novo_valor
        )

        despesas[indice]["tipo"] = (
            novo_tipo
        )

        despesas[indice]["categoria"] = (
            nova_categoria
        )

        despesas[indice]["total_parcelas"] = (
            novo_total_parcelas
        )

        despesas[indice]["parcelas_pagas"] = (
            novas_parcelas_pagas
        )

        despesas[indice]["dividir"] = (
            dividir
        )

        despesas[indice]["numero_pessoas"] = (
            numero_pessoas
        )

        despesas[indice]["divisao_igual"] = (
            divisao_igual
        )

        despesas[indice]["minha_parte"] = (
            nova_minha_parte
        )


        salvar_despesas()


        janela.destroy()


        mostrar_despesas()


    # ------------------------------------------------------
    # BOTÕES
    # ------------------------------------------------------

    ctk.CTkButton(
        janela,
        text="💾 Salvar alterações",
        height=42,
        command=salvar_edicao
    ).pack(
        fill="x",
        padx=40,
        pady=(15, 10)
    )


    ctk.CTkButton(
        janela,
        text="Cancelar",
        height=38,
        fg_color="transparent",
        border_width=1,
        command=janela.destroy
    ).pack(
        fill="x",
        padx=40
    )


# ==========================================================
# MARCAR PARCELA COMO PAGA
# ==========================================================

def marcar_parcela_paga(indice):

    despesa = despesas[indice]


    total_parcelas = despesa.get(
        "total_parcelas"
    )

    parcelas_pagas = despesa.get(
        "parcelas_pagas",
        0
    )


    if not total_parcelas:

        return


    if parcelas_pagas >= total_parcelas:

        messagebox.showinfo(
            "Compra quitada",
            "Todas as parcelas já foram pagas."
        )

        return


    proxima_parcela = (
        parcelas_pagas + 1
    )


    confirmar = messagebox.askyesno(
        "Confirmar pagamento",
        (
            f"Marcar a parcela "
            f"{proxima_parcela}/{total_parcelas} "
            f"como paga?"
        )
    )


    if not confirmar:

        return


    despesas[indice]["parcelas_pagas"] = (
        parcelas_pagas + 1
    )


    salvar_despesas()


    if (
        despesas[indice]["parcelas_pagas"]
        == total_parcelas
    ):

        messagebox.showinfo(
            "Compra quitada",
            "Todas as parcelas foram pagas!"
        )


    mostrar_despesas()


# ==========================================================
# EXCLUIR DESPESA
# ==========================================================

def excluir_despesa(indice):

    despesa = despesas[indice]


    confirmar = messagebox.askyesno(
        "Excluir despesa",
        (
            f"Deseja excluir "
            f"'{despesa['descricao']}'?"
        )
    )


    if confirmar:

        despesas.pop(
            indice
        )

        salvar_despesas()

        mostrar_despesas()


# ==========================================================
# CRIAR CARD
# ==========================================================

def criar_card(
    parent,
    titulo,
    valor
):

    frame = ctk.CTkFrame(
        parent,
        height=105,
        corner_radius=15
    )

    frame.pack(
        side="left",
        fill="both",
        expand=True,
        padx=5
    )


    ctk.CTkLabel(
        frame,
        text=titulo,
        font=ctk.CTkFont(
            size=13
        )
    ).pack(
        anchor="w",
        padx=18,
        pady=(18, 2)
    )


    ctk.CTkLabel(
        frame,
        text=valor,
        font=ctk.CTkFont(
            size=23,
            weight="bold"
        )
    ).pack(
        anchor="w",
        padx=18
    )


# ==========================================================
# TEXTO DO PARCELAMENTO
# ==========================================================

def obter_texto_parcelamento(
    despesa
):

    total_parcelas = despesa.get(
        "total_parcelas"
    )

    parcelas_pagas = despesa.get(
        "parcelas_pagas",
        0
    )


    if not total_parcelas:

        return ""


    if parcelas_pagas >= total_parcelas:

        return (
            f"   |   "
            f"{total_parcelas}/"
            f"{total_parcelas}"
            f"   |   "
            f"✅ Quitado"
        )


    proxima_parcela = (
        parcelas_pagas + 1
    )

    restantes = (
        total_parcelas
        - parcelas_pagas
    )


    return (
        f"   |   "
        f"{proxima_parcela}/"
        f"{total_parcelas}"
        f"   |   "
        f"{parcelas_pagas} pagas"
        f"   |   "
        f"{restantes} restantes"
    )


# ==========================================================
# TELA INÍCIO
# ==========================================================

def mostrar_inicio():

    limpar_conteudo()


    # ------------------------------------------------------
    # TÍTULO
    # ------------------------------------------------------

    ctk.CTkLabel(
        conteudo,
        text="Olá! 👋",
        font=ctk.CTkFont(
            size=28,
            weight="bold"
        )
    ).pack(
        anchor="w"
    )


    ctk.CTkLabel(
        conteudo,
        text="Aqui está o resumo das suas despesas.",
        font=ctk.CTkFont(
            size=14
        )
    ).pack(
        anchor="w",
        pady=(0, 20)
    )


    # ------------------------------------------------------
    # TOTAL REAL DO USUÁRIO
    # ------------------------------------------------------

    total = sum(
        obter_valor_usuario(
            despesa
        )
        for despesa in despesas
    )


    quantidade = len(
        despesas
    )


    total_fixos = sum(
        obter_valor_usuario(
            despesa
        )
        for despesa in despesas
        if despesa.get(
            "tipo"
        ) == "Fixo"
    )


    total_variaveis = sum(
        obter_valor_usuario(
            despesa
        )
        for despesa in despesas
        if despesa.get(
            "tipo"
        ) == "Variável"
    )


    total_parcelados = sum(
        obter_valor_usuario(
            despesa
        )
        for despesa in despesas
        if despesa.get(
            "tipo"
        ) == "Parcelado"
    )


    # ------------------------------------------------------
    # CARDS PRINCIPAIS
    # ------------------------------------------------------

    frame_cards = ctk.CTkFrame(
        conteudo,
        fg_color="transparent"
    )

    frame_cards.pack(
        fill="x",
        pady=(0, 10)
    )


    criar_card(
        frame_cards,
        "TOTAL GASTO",
        formatar_moeda(total)
    )


    criar_card(
        frame_cards,
        "DESPESAS",
        str(quantidade)
    )


    criar_card(
        frame_cards,
        "FIXOS",
        formatar_moeda(total_fixos)
    )


    # ------------------------------------------------------
    # TIPOS
    # ------------------------------------------------------

    frame_tipos = ctk.CTkFrame(
        conteudo,
        fg_color="transparent"
    )

    frame_tipos.pack(
        fill="x",
        pady=(0, 20)
    )


    criar_card(
        frame_tipos,
        "VARIÁVEIS",
        formatar_moeda(
            total_variaveis
        )
    )


    criar_card(
        frame_tipos,
        "PARCELADOS",
        formatar_moeda(
            total_parcelados
        )
    )


    # ------------------------------------------------------
    # ADICIONAR DESPESA
    # ------------------------------------------------------

    frame_adicionar = ctk.CTkFrame(
        conteudo,
        corner_radius=15
    )

    frame_adicionar.pack(
        fill="x",
        pady=(0, 20)
    )


    ctk.CTkLabel(
        frame_adicionar,
        text="Adicionar despesa",
        font=ctk.CTkFont(
            size=18,
            weight="bold"
        )
    ).grid(
        row=0,
        column=0,
        columnspan=3,
        sticky="w",
        padx=20,
        pady=(15, 10)
    )


    global entrada_descricao
    global entrada_valor
    global entrada_tipo
    global entrada_categoria
    global entrada_total_parcelas
    global entrada_parcelas_pagas
    global frame_parcelamento
    global variavel_dividir
    global frame_divisao
    global variavel_divisao_igual
    global frame_minha_parte
    global entrada_numero_pessoas
    global entrada_minha_parte
    global label_resultado_divisao


    # ------------------------------------------------------
    # DESCRIÇÃO
    # ------------------------------------------------------

    entrada_descricao = ctk.CTkEntry(
        frame_adicionar,
        placeholder_text="Descrição"
    )

    entrada_descricao.grid(
        row=1,
        column=0,
        padx=10,
        pady=(0, 10),
        sticky="ew"
    )


    # ------------------------------------------------------
    # VALOR
    # ------------------------------------------------------

    entrada_valor = ctk.CTkEntry(
        frame_adicionar,
        placeholder_text="Valor total / parcela"
    )

    entrada_valor.grid(
        row=1,
        column=1,
        padx=10,
        pady=(0, 10),
        sticky="ew"
    )


    # ------------------------------------------------------
    # TIPO
    # ------------------------------------------------------

    entrada_tipo = ctk.CTkComboBox(
        frame_adicionar,
        values=TIPOS,
        command=lambda _: atualizar_campos_parcelamento()
    )

    entrada_tipo.set(
        "Variável"
    )

    entrada_tipo.grid(
        row=1,
        column=2,
        padx=10,
        pady=(0, 10),
        sticky="ew"
    )


    # ------------------------------------------------------
    # CATEGORIA
    # ------------------------------------------------------

    entrada_categoria = ctk.CTkComboBox(
        frame_adicionar,
        values=CATEGORIAS
    )

    entrada_categoria.set(
        "Alimentação"
    )

    entrada_categoria.grid(
        row=2,
        column=0,
        padx=10,
        pady=(0, 10),
        sticky="ew"
    )


    # ------------------------------------------------------
    # PARCELAMENTO
    # ------------------------------------------------------

    frame_parcelamento = ctk.CTkFrame(
        frame_adicionar,
        fg_color="transparent"
    )


    ctk.CTkLabel(
        frame_parcelamento,
        text="Total de parcelas:"
    ).pack(
        side="left",
        padx=(0, 5)
    )


    entrada_total_parcelas = ctk.CTkEntry(
        frame_parcelamento,
        width=90,
        placeholder_text="Ex: 12"
    )

    entrada_total_parcelas.pack(
        side="left",
        padx=5
    )


    ctk.CTkLabel(
        frame_parcelamento,
        text="Já pagas:"
    ).pack(
        side="left",
        padx=(15, 5)
    )


    entrada_parcelas_pagas = ctk.CTkEntry(
        frame_parcelamento,
        width=90,
        placeholder_text="Ex: 6"
    )

    entrada_parcelas_pagas.pack(
        side="left",
        padx=5
    )


    frame_parcelamento.grid_remove()


    # ------------------------------------------------------
    # DIVIDIR DESPESA
    # ------------------------------------------------------

    variavel_dividir = ctk.BooleanVar(
        value=False
    )


    ctk.CTkCheckBox(
        frame_adicionar,
        text="👥 Dividir esta despesa",
        variable=variavel_dividir,
        command=atualizar_campos_divisao
    ).grid(
        row=4,
        column=0,
        columnspan=3,
        sticky="w",
        padx=10,
        pady=(5, 10)
    )


    # ------------------------------------------------------
    # FRAME DIVISÃO
    # ------------------------------------------------------

    frame_divisao = ctk.CTkFrame(
        frame_adicionar,
        fg_color="transparent"
    )


    ctk.CTkLabel(
        frame_divisao,
        text="Número de pessoas:"
    ).grid(
        row=0,
        column=0,
        sticky="w"
    )


    entrada_numero_pessoas = ctk.CTkEntry(
        frame_divisao,
        width=80,
        placeholder_text="Ex: 3"
    )

    entrada_numero_pessoas.grid(
        row=0,
        column=1,
        padx=10
    )


    variavel_divisao_igual = ctk.BooleanVar(
        value=True
    )


    ctk.CTkRadioButton(
        frame_divisao,
        text="Dividir igualmente",
        variable=variavel_divisao_igual,
        value=True,
        command=atualizar_tipo_divisao
    ).grid(
        row=1,
        column=0,
        columnspan=2,
        sticky="w",
        pady=(10, 5)
    )


    ctk.CTkRadioButton(
        frame_divisao,
        text="Definir minha parte",
        variable=variavel_divisao_igual,
        value=False,
        command=atualizar_tipo_divisao
    ).grid(
        row=2,
        column=0,
        columnspan=2,
        sticky="w"
    )


    frame_minha_parte = ctk.CTkFrame(
        frame_divisao,
        fg_color="transparent"
    )


    ctk.CTkLabel(
        frame_minha_parte,
        text="Minha parte:"
    ).pack(
        side="left"
    )


    entrada_minha_parte = ctk.CTkEntry(
        frame_minha_parte,
        width=100,
        placeholder_text="Ex: 150"
    )

    entrada_minha_parte.pack(
        side="left",
        padx=10
    )


    label_resultado_divisao = ctk.CTkLabel(
        frame_divisao,
        text="Sua parte será calculada automaticamente."
    )

    label_resultado_divisao.grid(
        row=4,
        column=0,
        columnspan=2,
        sticky="w",
        pady=(10, 0)
    )


    frame_divisao.grid_remove()


    # ------------------------------------------------------
    # BOTÃO ADICIONAR
    # ------------------------------------------------------

    ctk.CTkButton(
        frame_adicionar,
        text="+ Adicionar",
        height=38,
        command=adicionar_despesa
    ).grid(
        row=6,
        column=0,
        columnspan=3,
        padx=10,
        pady=(10, 15),
        sticky="ew"
    )


    # ------------------------------------------------------
    # COLUNAS
    # ------------------------------------------------------

    frame_adicionar.columnconfigure(
        0,
        weight=1
    )

    frame_adicionar.columnconfigure(
        1,
        weight=1
    )

    frame_adicionar.columnconfigure(
        2,
        weight=1
    )


    # ------------------------------------------------------
    # ÚLTIMAS DESPESAS
    # ------------------------------------------------------

    ctk.CTkLabel(
        conteudo,
        text="Últimas despesas",
        font=ctk.CTkFont(
            size=18,
            weight="bold"
        )
    ).pack(
        anchor="w",
        pady=(0, 8)
    )


    lista = ctk.CTkScrollableFrame(
        conteudo,
        corner_radius=15
    )

    lista.pack(
        fill="both",
        expand=True
    )


    if not despesas:

        ctk.CTkLabel(
            lista,
            text="Nenhuma despesa cadastrada.",
            font=ctk.CTkFont(
                size=15
            )
        ).pack(
            pady=30
        )

    else:

        for despesa in reversed(
            despesas[-8:]
        ):

            criar_item_despesa(
                lista,
                despesa
            )


# ==========================================================
# ITEM DE DESPESA
# ==========================================================

def criar_item_despesa(
    parent,
    despesa
):

    frame = ctk.CTkFrame(
        parent,
        corner_radius=10
    )

    frame.pack(
        fill="x",
        padx=5,
        pady=5
    )


    tipo = despesa.get(
        "tipo",
        "Variável"
    )


    categoria = despesa.get(
        "categoria",
        "Outros"
    )


    valor_usuario = obter_valor_usuario(
        despesa
    )


    texto = (

        f"{despesa['descricao']}"
        f"   |   "
        f"{formatar_moeda(valor_usuario)}"
        f"   |   "
        f"{tipo}"
        f"   |   "
        f"{categoria}"
    )


    if tipo == "Parcelado":

        texto += obter_texto_parcelamento(
            despesa
        )


    if despesa.get(
        "dividir",
        False
    ):

        texto += obter_texto_divisao(
            despesa
        )


    texto += (
        f"   |   "
        f"{despesa['data']}"
    )


    ctk.CTkLabel(
        frame,
        text=texto,
        anchor="w",
        font=ctk.CTkFont(
            size=14
        )
    ).pack(
        side="left",
        padx=15,
        pady=12
    )


# ==========================================================
# TELA DESPESAS
# ==========================================================

def mostrar_despesas():

    limpar_conteudo()


    ctk.CTkLabel(
        conteudo,
        text="💰 Minhas Despesas",
        font=ctk.CTkFont(
            size=28,
            weight="bold"
        )
    ).pack(
        anchor="w"
    )


    ctk.CTkLabel(
        conteudo,
        text="Aqui estão todas as despesas cadastradas.",
        font=ctk.CTkFont(
            size=14
        )
    ).pack(
        anchor="w",
        pady=(0, 20)
    )


    lista = ctk.CTkScrollableFrame(
        conteudo,
        corner_radius=15
    )

    lista.pack(
        fill="both",
        expand=True
    )


    if not despesas:

        ctk.CTkLabel(
            lista,
            text="Nenhuma despesa cadastrada.",
            font=ctk.CTkFont(
                size=16
            )
        ).pack(
            pady=30
        )

        return


    for indice, despesa in enumerate(
        despesas
    ):

        frame = ctk.CTkFrame(
            lista,
            corner_radius=10
        )

        frame.pack(
            fill="x",
            padx=5,
            pady=5
        )


        tipo = despesa.get(
            "tipo",
            "Variável"
        )


        categoria = despesa.get(
            "categoria",
            "Outros"
        )


        valor_usuario = obter_valor_usuario(
            despesa
        )


        # --------------------------------------------------
        # INFORMAÇÕES
        # --------------------------------------------------

        frame_info = ctk.CTkFrame(
            frame,
            fg_color="transparent"
        )

        frame_info.pack(
            side="left",
            fill="x",
            expand=True
        )


        ctk.CTkLabel(
            frame_info,
            text=despesa["descricao"],
            anchor="w",
            font=ctk.CTkFont(
                size=15,
                weight="bold"
            )
        ).pack(
            anchor="w",
            padx=15,
            pady=(10, 0)
        )


        texto = (

            f"{formatar_moeda(valor_usuario)}"
            f"   |   "
            f"{tipo}"
            f"   |   "
            f"{categoria}"
        )


        if despesa.get(
            "dividir",
            False
        ):

            texto += (
                f"   |   "
                f"👥 "
                f"{despesa.get('numero_pessoas', 1)}"
                f" pessoas"
            )


        if tipo == "Parcelado":

            texto += obter_texto_parcelamento(
                despesa
            )


        texto += (
            f"   |   "
            f"{despesa['data']}"
        )


        ctk.CTkLabel(
            frame_info,
            text=texto,
            anchor="w",
            font=ctk.CTkFont(
                size=13
            )
        ).pack(
            anchor="w",
            padx=15,
            pady=(0, 10)
        )


        # --------------------------------------------------
        # BOTÃO PAGAR
        # --------------------------------------------------

        if (
            tipo == "Parcelado"
            and despesa.get(
                "parcelas_pagas",
                0
            ) < despesa.get(
                "total_parcelas",
                0
            )
        ):

            ctk.CTkButton(
                frame,
                text="✅ Pagar",
                width=85,
                command=lambda i=indice:
                marcar_parcela_paga(i)
            ).pack(
                side="right",
                padx=5
            )


        # --------------------------------------------------
        # BOTÃO EDITAR
        # --------------------------------------------------

        ctk.CTkButton(
            frame,
            text="✏️ Editar",
            width=85,
            command=lambda i=indice:
            editar_despesa(i)
        ).pack(
            side="right",
            padx=5
        )


        # --------------------------------------------------
        # BOTÃO EXCLUIR
        # --------------------------------------------------

        ctk.CTkButton(
            frame,
            text="🗑 Excluir",
            width=85,
            fg_color="#C0392B",
            hover_color="#922B21",
            command=lambda i=indice:
            excluir_despesa(i)
        ).pack(
            side="right",
            padx=10
        )


# ==========================================================
# TELA RELATÓRIOS
# ==========================================================

def mostrar_relatorios():

    limpar_conteudo()


    ctk.CTkLabel(
        conteudo,
        text="📊 Relatórios",
        font=ctk.CTkFont(
            size=28,
            weight="bold"
        )
    ).pack(
        anchor="w"
    )


    ctk.CTkLabel(
        conteudo,
        text="Veja como seus gastos estão distribuídos.",
        font=ctk.CTkFont(
            size=14
        )
    ).pack(
        anchor="w",
        pady=(0, 20)
    )


    # ------------------------------------------------------
    # TOTAIS
    # ------------------------------------------------------

    total = sum(
        obter_valor_usuario(
            despesa
        )
        for despesa in despesas
    )


    total_fixos = sum(
        obter_valor_usuario(
            despesa
        )
        for despesa in despesas
        if despesa.get(
            "tipo"
        ) == "Fixo"
    )


    total_variaveis = sum(
        obter_valor_usuario(
            despesa
        )
        for despesa in despesas
        if despesa.get(
            "tipo"
        ) == "Variável"
    )


    total_parcelados = sum(
        obter_valor_usuario(
            despesa
        )
        for despesa in despesas
        if despesa.get(
            "tipo"
        ) == "Parcelado"
    )


    # ------------------------------------------------------
    # CARDS
    # ------------------------------------------------------

    frame_tipos = ctk.CTkFrame(
        conteudo,
        fg_color="transparent"
    )

    frame_tipos.pack(
        fill="x",
        pady=(0, 20)
    )


    criar_card(
        frame_tipos,
        "TOTAL GASTO",
        formatar_moeda(total)
    )


    criar_card(
        frame_tipos,
        "FIXOS",
        formatar_moeda(
            total_fixos
        )
    )


    criar_card(
        frame_tipos,
        "VARIÁVEIS",
        formatar_moeda(
            total_variaveis
        )
    )


    criar_card(
        frame_tipos,
        "PARCELADOS",
        formatar_moeda(
            total_parcelados
        )
    )


    # ------------------------------------------------------
    # CATEGORIAS
    # ------------------------------------------------------

    categorias = {}


    for despesa in despesas:

        categoria = despesa.get(
            "categoria",
            "Outros"
        )


        if categoria not in categorias:

            categorias[categoria] = 0


        categorias[categoria] += (
            obter_valor_usuario(
                despesa
            )
        )


    ctk.CTkLabel(
        conteudo,
        text="Gastos por categoria",
        font=ctk.CTkFont(
            size=18,
            weight="bold"
        )
    ).pack(
        anchor="w",
        pady=(5, 10)
    )


    lista = ctk.CTkScrollableFrame(
        conteudo,
        corner_radius=15
    )

    lista.pack(
        fill="both",
        expand=True
    )


    if not categorias:

        ctk.CTkLabel(
            lista,
            text="Nenhuma informação disponível."
        ).pack(
            pady=30
        )

        return


    categorias_ordenadas = sorted(
        categorias.items(),
        key=lambda item: item[1],
        reverse=True
    )


    for categoria, valor in categorias_ordenadas:

        percentual = (

            valor / total * 100

            if total > 0

            else 0
        )


        frame = ctk.CTkFrame(
            lista,
            corner_radius=10
        )

        frame.pack(
            fill="x",
            padx=5,
            pady=5
        )


        ctk.CTkLabel(
            frame,
            text=categoria,
            font=ctk.CTkFont(
                size=15,
                weight="bold"
            )
        ).pack(
            side="left",
            padx=15,
            pady=12
        )


        ctk.CTkLabel(
            frame,
            text=(
                f"{formatar_moeda(valor)}"
                f"   "
                f"({percentual:.1f}%)"
            ),
            font=ctk.CTkFont(
                size=14
            )
        ).pack(
            side="right",
            padx=15
        )


# ==========================================================
# MENU LATERAL
# ==========================================================

sidebar = ctk.CTkFrame(
    app,
    width=210,
    corner_radius=0
)

sidebar.pack(
    side="left",
    fill="y"
)

sidebar.pack_propagate(False)


# ----------------------------------------------------------
# LOGO
# ----------------------------------------------------------

ctk.CTkLabel(
    sidebar,
    text="💰",
    font=ctk.CTkFont(
        size=42
    )
).pack(
    pady=(35, 5)
)


# ----------------------------------------------------------
# NOME
# ----------------------------------------------------------

ctk.CTkLabel(
    sidebar,
    text="Controle\nFinanceiro",
    font=ctk.CTkFont(
        size=20,
        weight="bold"
    )
).pack(
    pady=(0, 40)
)


# ----------------------------------------------------------
# INÍCIO
# ----------------------------------------------------------

ctk.CTkButton(
    sidebar,
    text="🏠  Início",
    height=42,
    anchor="w",
    command=mostrar_inicio
).pack(
    fill="x",
    padx=15,
    pady=5
)


# ----------------------------------------------------------
# DESPESAS
# ----------------------------------------------------------

ctk.CTkButton(
    sidebar,
    text="💰  Despesas",
    height=42,
    anchor="w",
    command=mostrar_despesas
).pack(
    fill="x",
    padx=15,
    pady=5
)


# ----------------------------------------------------------
# RELATÓRIOS
# ----------------------------------------------------------

ctk.CTkButton(
    sidebar,
    text="📊  Relatórios",
    height=42,
    anchor="w",
    command=mostrar_relatorios
).pack(
    fill="x",
    padx=15,
    pady=5
)


# ----------------------------------------------------------
# TEMA
# ----------------------------------------------------------

botao_tema = ctk.CTkButton(
    sidebar,
    text="☀️  Tema claro",
    height=42,
    anchor="w",
    command=alternar_tema
)

botao_tema.pack(
    fill="x",
    padx=15,
    pady=(30, 5)
)


# ==========================================================
# ÁREA PRINCIPAL
# ==========================================================

conteudo = ctk.CTkFrame(
    app,
    fg_color="transparent"
)

conteudo.pack(
    side="left",
    fill="both",
    expand=True,
    padx=25,
    pady=25
)


# ==========================================================
# INICIAR APLICAÇÃO
# ==========================================================

mostrar_inicio()

app.mainloop()