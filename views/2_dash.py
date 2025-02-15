import altair as alt
import pandas as pd
import plotly.figure_factory as ff
import plotly.graph_objects as go
import streamlit as st

# Cor padrão para os gráficos
COLOR = "#252729"

UF_IMAGES = {
    "Rio de Janeiro": "https://upload.wikimedia.org/wikipedia/commons/thumb/7/73/Bandeira_do_estado_do_Rio_de_Janeiro.svg/800px-Bandeira_do_estado_do_Rio_de_Janeiro.svg.png",
    "Bahia": "https://upload.wikimedia.org/wikipedia/commons/thumb/2/28/Bandeira_da_Bahia.svg/800px-Bandeira_da_Bahia.svg.png",
    "Pernambuco": "https://upload.wikimedia.org/wikipedia/commons/thumb/5/59/Bandeira_de_Pernambuco.svg/540px-Bandeira_de_Pernambuco.svg.png",
    "Geral": "https://upload.wikimedia.org/wikipedia/commons/thumb/0/05/Flag_of_Brazil.svg/800px-Flag_of_Brazil.svg.png",
}


# Recuperando os dados carregados
df_vitimas = st.session_state["vitimas"]
df_ocorrencias = st.session_state["ocorrencias"]

# Botões laterais para filtragem
estados = ["Geral", "Bahia", "Pernambuco", "Rio de Janeiro"]
estado = st.sidebar.selectbox("UF", estados)
st.subheader(f'Dados de {estado if estado != 'Geral' else "Brasil"}')

if estado != "Geral":
    ocorrencias_filtered = df_ocorrencias.query("uf == @estado")
    vitimas_filtered = df_vitimas.query("uf == @estado")
else:
    ocorrencias_filtered = df_ocorrencias
    vitimas_filtered = df_vitimas

st.image(UF_IMAGES[estado], width=50)


tab1, tab2 = st.tabs(["OCORRÊNCIAS", "VÍTIMAS"])


with tab1:
    st.subheader("INFORMAÇÕES SOBRE OCORRÊNCIAS".capitalize())
    zoom = 8 if estado != "Geral" else 3

    # Primeira linha
    t1col11, t1col12, t1col13, t1col14 = st.columns(4)

    with t1col11:
        with st.container(border=True):
            st.metric(
                "**OCORRÊNCIAS** :material/news:", int(ocorrencias_filtered.shape[0])
            )

    with t1col12:
        with st.container(border=True):
            feridos = (
                ocorrencias_filtered["agentes_feridos_ocorrencia"].sum()
                + ocorrencias_filtered["civis_feridos_ocorrencia"].sum()
            )
            st.metric("**FERIDOS :material/earthquake:**", int(feridos))

    with t1col13:
        with st.container(border=True):
            mortos = (
                ocorrencias_filtered["agentes_mortos_ocorrencia"].sum()
                + ocorrencias_filtered["civis_mortos_ocorrencia"].sum()
            )
            st.metric("**MORTOS :material/heart_minus:**", int(mortos))

    with t1col14:
        with st.container(border=True):
            chacinas = (ocorrencias_filtered["chacina_ocorrencia"] == "Sim").sum()
            st.metric("**CHACINAS** :material/skull:", int(chacinas))

    t1col21, t1col22 = st.columns([2, 1])

    with t1col21:
        with st.container(border=True):
            # Contar o número de ocorrências por data
            registros = ocorrencias_filtered["mes"].dropna().value_counts().reset_index()
            registros.columns = ["mes", "registros"]

            ordem_meses = [
                "Janeiro",
                "Fevereiro",
                "Março",
                "Abril",
                "Maio",
                "Junho",
                "Julho",
                "Agosto",
                "Setembro",
                "Outubro",
                "Novembro",
                "Dezembro",
            ]
            registros_ordenados = registros.sort_values(by='mes').copy()
            # Criar o gráfico de linha
            chart = (
                alt.Chart(registros_ordenados)).mark_bar().encode(
                    x="mes:N",  # 'T' indica que a variável é temporal
                    y="registros:Q",
                    color=alt.value(COLOR),  # 'Q' indica que a variável é quantitativa
                ).properties(title="Contagem de Ocorrências por mês")
            st.altair_chart(chart, use_container_width=True)

    with t1col22:
        with st.container(border=True):
            source = (
                ocorrencias_filtered["fonte_ocorrencia"].value_counts().reset_index()
            )
            source.columns = ["Fonte", "Registros"]

            # Criando o gráfico de pizza radial
            base = alt.Chart(source).encode(
                alt.Theta("Registros:Q").stack(True),
                alt.Radius("Registros:Q").scale(type="sqrt", zero=True, rangeMin=20),
                color=alt.Color(
                    "Fonte:N", title="Fonte da Ocorrência"
                ),  # Define legenda correta
            )

            c1 = base.mark_arc(innerRadius=20, stroke="#fff")

            c2 = base.mark_text(radiusOffset=10).encode(text="Registros:Q")

            chart = c1 + c2
            chart = c1 + c2

            st.altair_chart(chart, use_container_width=True)

    # Terceira linha
    t1col31, t1col32 = st.columns(2)

    with t1col31:
        with st.container(border=True, height=383):
            st.map(
                ocorrencias_filtered,
                latitude="latitude",
                longitude="longitude",
                height=320,
                size="civis_mortos_ocorrencia",
                color="color",
                zoom=zoom,
            )
            st.markdown("**🟠 Outros Registros  🔴 Chacinas**")

    with t1col32:
        with st.container(border=True, height=383):
            st.markdown("**Motivos mais frequentes**".upper())

            causa_acidentes = (
                ocorrencias_filtered["motivo_principal"]
                .value_counts()
                .sort_values(ascending=False)
                .head(7)
                .reset_index()
                .rename(columns={"motivo_principal": "Motivo", "count": "Ocorrências"})
            )
            st.dataframe(
                causa_acidentes,
                hide_index=True,
                column_config={
                    "Ocorrências": st.column_config.ProgressColumn(
                        "Registros",
                        format="%d",
                        min_value=0,
                        max_value=int(causa_acidentes["Ocorrências"].max()),
                        width="large",
                    )
                },
                use_container_width=True,
            )

    t1col41, t1col42 = st.columns([2, 1])

    with t1col41:
        with st.container(border=True):
            st.markdown("**Registros por cidade**".upper())
            st.bar_chart(
                ocorrencias_filtered.groupby("cidade")
                .count()["data_ocorrencia"]
                .sort_values(ascending=False)
                .head(10),
                height=283,
                color="#252729",
                use_container_width=True,
            )

    with t1col42:
        with st.container(border=True, height=382):
            labels = ocorrencias_filtered["acao_policial"].value_counts().index
            values = ocorrencias_filtered["acao_policial"].value_counts()
            fig = go.Figure(
                data=[
                    go.Pie(
                        labels=labels,
                        values=values,
                        hole=0.7,
                        textinfo="label+percent",
                    )
                ],
                layout=go.Layout(height=400, width=400),
            )
            fig.update(layout_showlegend=False)
            fig.update_layout(
                title={"text": "PROPORÇÃO DE REGISTROS DE AÇÕES POLICIAIS"}
            )
            st.plotly_chart(fig, use_container_width=True)

with tab2:
    st.subheader("INFORMAÇÕES SOBRE VÍTIMAS".capitalize())

    t2col11, t2col12, t2col13 = st.columns([1, 2, 1])

    with t2col11:
        with st.container(border=True, height=380):
            st.markdown("**Vítimas por faixa etária**".upper())
            faixa_etaria = (
                vitimas_filtered["faixa_etaria"]
                .value_counts()
                .sort_values(ascending=False)
                .reset_index()
                .rename(columns={"faixa_etaria": "Faixa Etária", "count": "Vítimas"})
            )
            st.dataframe(
                faixa_etaria,
                hide_index=True,
                column_config={
                    "Vítimas": st.column_config.ProgressColumn(
                        "Registros",
                        format="%d",
                        min_value=0,
                        max_value=int(faixa_etaria["Vítimas"].max()),
                        width="small",
                    )
                },
                use_container_width=True,
            )

    with t2col12:
        with st.container(border=True, height=382):
            st.markdown("**Vítimas por gênero**".upper())
            st.bar_chart(
                vitimas_filtered.groupby("genero")
                .count()["uf"]
                .sort_values(ascending=False),
                height=300,
                color=COLOR,
                horizontal=True,
            )

    with t2col13:
        with st.container(border=True, height=382):
            labels = vitimas_filtered["raca"].value_counts().index
            values = vitimas_filtered["raca"].value_counts()
            fig = go.Figure(
                data=[
                    go.Pie(
                        labels=labels,
                        values=values,
                        hole=0.7,
                        textinfo="label+percent",
                    )
                ],
                layout=go.Layout(height=400, width=400),
            )
            fig.update(layout_showlegend=False)
            fig.update_layout(title={"text": "Distribuição de Raça".upper()})
            st.plotly_chart(fig, use_container_width=True)

    t2col21, t2col22 = st.columns([3, 1])

    with t2col21:
        with st.container(border=True, height=500):
            st.markdown("**DISTRIBUIÇÃO DAS IDADES**")
            fig = ff.create_distplot(
                [vitimas_filtered["idade"].dropna()],
                group_labels=["Idade"],
                show_rug=False,
                colors=["#252729"],
            )
            st.plotly_chart(fig, use_container_width=True)

    with t2col22:
        with st.container(border=True, height=500):
            st.markdown("**Local onde a vítima foi alvejada**".upper())
            faixa_etaria = (
                vitimas_filtered["local"]
                .value_counts()
                .sort_values(ascending=False)
                .reset_index()
                .rename(columns={"local": "local", "count": "Vítimas"})
            )
            st.dataframe(
                faixa_etaria,
                hide_index=True,
                column_config={
                    "Vítimas": st.column_config.ProgressColumn(
                        "Registros",
                        format="%d",
                        min_value=0,
                        max_value=int(faixa_etaria["Vítimas"].max()),
                        width="small",
                    )
                },
                use_container_width=True,
            )
    categorias = df_vitimas["tipo_pessoa"].unique()

    choice = st.selectbox("Tipo de pessoa", categorias)

    st.markdown("**Tabela de contingência Gênero x Raça**")
    st.table(
        pd.crosstab(
            vitimas_filtered.query("tipo_pessoa == @choice")["genero"],
            vitimas_filtered.query("tipo_pessoa == @choice")["raca"],
        )
    )
