import pandas as pd
import streamlit as st
from faker import Faker

df2 = pd.read_csv(r'dados_teste_lingo4.csv')
dataframe_completo = pd.read_csv(r'Base Embraer.csv')


def main():
    # Definir cores personalizadas
    color_gray = '##204782'
    color_white = '#ffffff'
    gradient_color1 = '#204782'  # Deep Blue
    gradient_color2 = '#2f5694'  # Light Sky Blue

    st.image(r'logo-embraer.png', use_column_width=True)

    st.title('Assiduidade e Progresso')

    st.sidebar.image('logo-lingopass-azul.png', use_column_width=True)
    analysis_type = st.sidebar.selectbox('Escolha o tipo de análise', ['Tabela Resumitiva','Geral', 'Individual'])

    # Filtro para Resultado de Nivelamento
    unique_results = ['A1', 'A2', 'B1', 'B2', 'C1', 'C2']

    # Filtro para Leva
    unique_levas = df2['Leva'].unique()

    # Filtro para Área
    unique_areas = df2[df2['Área'] != '-']['Área'].unique()

    # Filtro para Modelo de Aula
    unique_modelos = df2['Modelo de aula'].unique()
    
    # Excluir a coluna "Unnamed: 0"
    df2.drop('Unnamed: 0', axis=1, inplace=True)
    
    df_selected = df2.copy()

    

    def ajustar_tempo(valor):
        # se a parte decimal for maior que zero, multiplica por 1000
        if valor % 1 > 0:
            return valor * 1000
        else:
            return valor

    if analysis_type == 'Tabela Resumitiva':

        # Remover o símbolo de percentagem e converter para float
        df_selected['Média de progresso'] = df_selected['total progresso'].str.rstrip('%').astype('float')

        # Ajustar os tempos e converter para horas
        df_selected['Média tempo AOV horas'] = df_selected['tempo AOV minutos'].apply(ajustar_tempo) / 60
        df_selected['Média tempo plataforma horas'] = df_selected['tempo plataforma minutos'].apply(ajustar_tempo) / 60

        # Tabela agrupada por Idioma de Interesse
        df_grouped_language = df_selected.groupby('Idioma de interesse').agg(
            {'Média tempo AOV horas': 'mean', 'Média tempo plataforma horas': 'mean',
             'Média de progresso': 'mean'}).reset_index()
        df_grouped_language['Média de progresso'] = df_grouped_language['Média de progresso'].apply(
            lambda x: f'{x:.2f}%')



        # Tabela agrupada por Resultado nivelamento
        df_grouped_result = df_selected.groupby('Resultado nivelamento').agg(
            {'Média tempo AOV horas': 'mean', 'Média tempo plataforma horas': 'mean',
             'Média de progresso': 'mean'}).reset_index()
        df_grouped_result = df_grouped_result[
            df_grouped_result['Resultado nivelamento'].isin(['A1', 'A2', 'B1', 'B2', 'C1', 'C2'])]
        df_grouped_result['Média de progresso'] = df_grouped_result['Média de progresso'].apply(lambda x: f'{x:.2f}%')

        # Tabela agrupada por Leva
        df_grouped_leva = df_selected.groupby('Leva').agg(
            {'Média tempo AOV horas': 'mean', 'Média tempo plataforma horas': 'mean',
             'Média de progresso': 'mean'}).reset_index()
        df_grouped_leva['Média de progresso'] = df_grouped_leva['Média de progresso'].apply(lambda x: f'{x:.2f}%')

        # Tabela agrupada por Área
        df_grouped_area = df_selected.groupby('Área').agg(
            {'Média tempo AOV horas': 'mean', 'Média tempo plataforma horas': 'mean',
             'Média de progresso': 'mean'}).reset_index()
        df_grouped_area = df_grouped_area[df_grouped_area['Área'] != '-']
        df_grouped_area['Média de progresso'] = df_grouped_area['Média de progresso'].apply(lambda x: f'{x:.2f}%')


        table_option = st.selectbox(
            'Escolha a tabela para visualizar',
            ('Idioma de interesse', 'Resultado Nivelamento', 'Leva', 'Área')
        )

        if table_option == 'Idioma de interesse':
            st.subheader('Tabela por Idioma de interesse')
            st.write(df_grouped_language)
        elif table_option == 'Resultado Nivelamento':
            st.subheader('Tabela por Resultado Nivelamento')
            st.write(df_grouped_result)
        elif table_option == 'Leva':
            st.subheader('Tabela por Leva')
            st.write(df_grouped_leva)
        elif table_option == 'Área':
            st.subheader('Tabela por Área')
            st.write(df_grouped_area)

    if analysis_type == 'Individual':
        st.subheader('Análise Individual')


        # Use selectbox for name input and show suggestions
        unique_names = df2['Nome completo'].unique()
        selected_name = st.selectbox('Nome completo', options=unique_names)

        if selected_name:
            df_individual = df2[df2['Nome completo'] == selected_name]
            st.write(df_individual)

            # Apply the function to the specific columns
            df_individual['tempo plataforma minutos'] = df_individual['tempo plataforma minutos'].apply(ajustar_tempo)
            df_individual['tempo AOV minutos'] = df_individual['tempo AOV minutos'].apply(ajustar_tempo)

            # Show progress and time data in cards
            progress = df_individual['total progresso'].values[0]
            platform_time = df_individual['tempo plataforma minutos'].values[0] / 60  # convert to hours
            aov_time = df_individual['tempo AOV minutos'].values[0] / 60  # convert to hours
            total_time = platform_time + aov_time

            

            # Estilo CSS inline
            container_style = f"""
                background: linear-gradient(135deg, {gradient_color1}, {gradient_color2});
                padding: 1rem;
                border-radius: 0.5rem;
                border:0.5px solid {color_gray};
                border-width: 2px;
                box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19);
                color: {color_white};
            """

            label_style = f"""
                color: {color_white};
            """

            value_style = f"""
                color: {color_white};
                font-weight: bold;
            """

            # Criando os cartões métricos
            col1, col2 = st.columns(2)

            with col1:
                with st.container():
                    st.markdown(
                        f'<div style="{container_style}"><span style="{label_style}">Progresso total:</span> <span style="{value_style}">{progress}</span></div>',
                        unsafe_allow_html=True)
                    st.markdown("<br>", unsafe_allow_html=True)
                    st.markdown(
                        f'<div style="{container_style}"><span style="{label_style}">Tempo na plataforma:</span> <span style="{value_style}">{platform_time:.2f} horas</span></div>',
                        unsafe_allow_html=True)

            with col2:
                with st.container():
                    st.markdown(
                        f'<div style="{container_style}"><span style="{label_style}">Tempo em AoV:</span> <span style="{value_style}">{aov_time:.2f} horas</span></div>',
                        unsafe_allow_html=True)
                    st.markdown("<br>", unsafe_allow_html=True)
                    st.markdown(
                        f'<div style="{container_style}"><span style="{label_style}">Tempo total:</span> <span style="{value_style}">{total_time:.2f} horas</span></div>',
                        unsafe_allow_html=True)



    if analysis_type == 'Geral':  # Análise Geral

        with st.expander("Filtro", expanded=True):

            unique_languages = df_selected['Idioma de interesse'].unique()

            selected_language = st.sidebar.multiselect('Idioma de interesse', unique_languages, unique_languages)

            selected_result = st.sidebar.multiselect('Resultado nivelamento', unique_results, unique_results)

            selected_leva = st.sidebar.multiselect('Leva', unique_levas, unique_levas)

            selected_area = st.sidebar.multiselect('Área', unique_areas, unique_areas)

            selected_modelo = st.sidebar.multiselect('Modelo de aula', unique_modelos, unique_modelos)

            df_selected = df_selected[df_selected['Resultado nivelamento'].isin(selected_result)]
            df_selected = df_selected[df_selected['Leva'].isin(selected_leva)]
            df_selected = df_selected[df_selected['Área'].isin(selected_area)]
            df_selected = df_selected[df_selected['Modelo de aula'].isin(selected_modelo)]
            df_selected = df_selected[df_selected['Idioma de interesse'].isin(selected_language)]

            # Apply the function to the specific columns
            df_selected['tempo plataforma minutos'] = df_selected['tempo plataforma minutos'].apply(ajustar_tempo)
            df_selected['tempo AOV minutos'] = df_selected['tempo AOV minutos'].apply(ajustar_tempo)
            df_selected['tempo total'] = df_selected['tempo total'].apply(ajustar_tempo)



            # Convert to hours
            df_selected['tempo plataforma minutos'] /= 60
            df_selected['tempo AOV minutos'] /= 60
            df_selected['tempo total'] /= 60



            slider_cols1 = st.columns(2)

            slider_cols2 = st.columns(2)

            slider_cols3 = st.columns(2)

            # Tempo na plataforma (minutos)

        try:

            with slider_cols1[0]:

                min_platform_time, max_platform_time = df_selected['tempo plataforma minutos'].min(), df_selected[
                    'tempo plataforma minutos'].max()

                platform_time_value = st.slider('Tempo na plataforma (horas)', min_value=int(min_platform_time),
                                                max_value=int(max_platform_time))

            with slider_cols1[1]:

                platform_radio = st.radio("Filtrar tempo na plataforma por", ('Maior ou igual a', 'Menor ou igual a'))

            if platform_radio == 'Maior ou igual a':

                df_selected = df_selected[df_selected['tempo plataforma minutos'] >= platform_time_value]

            else:

                df_selected = df_selected[df_selected['tempo plataforma minutos'] <= platform_time_value]

            # Tempo AOV minutos

            with slider_cols2[0]:

                min_aov_time, max_aov_time = df_selected['tempo AOV minutos'].min(), df_selected['tempo AOV minutos'].max()

                aov_time_value = st.slider('Tempo AOV (horas)', min_value=int(min_aov_time), max_value=int(max_aov_time))

            with slider_cols2[1]:

                aov_radio = st.radio("Filtrar tempo AOV por", ('Maior ou igual a', 'Menor ou igual a'))

            if aov_radio == 'Maior ou igual a':

                df_selected = df_selected[df_selected['tempo AOV minutos'] >= aov_time_value]

            else:

                df_selected = df_selected[df_selected['tempo AOV minutos'] <= aov_time_value]

            # Tempo total

            with slider_cols3[0]:

                min_total_time, max_total_time = df_selected['tempo total'].min(), df_selected['tempo total'].max()

                total_time_value = st.slider('Tempo total (horas)', min_value=int(min_total_time),
                                             max_value=int(max_total_time))

            with slider_cols3[1]:

                total_radio = st.radio("Filtrar tempo total por", ('Maior ou igual a', 'Menor ou igual a'))

            if total_radio == 'Maior ou igual a':

                df_selected = df_selected[df_selected['tempo total'] >= total_time_value]

            else:

                df_selected = df_selected[df_selected['tempo total'] <= total_time_value]

            st.write(df_selected)

            st.divider()  #  Draws a horizontal rule

            with st.expander("Resultado de Nivelamento", expanded=True):

                st.write("Quantidade de Aluno por Nivelamento")
                
                
                level_counts = df_selected['Resultado nivelamento'].value_counts()
                columns = []
                values = []
                for i,j in level_counts.items():
                    columns.append(i)
                    values.append(j)
                newDf = pd.DataFrame({"type":columns,"Quantidade de Alunos":values})
                newDf = newDf.set_index("type")
                st.bar_chart(newDf)

            with st.expander("Relação de Tempo por Quantidade de Alunos", expanded=True):
                # Calcular a média para cada coluna de tempo
                avg_platform_time = df_selected['tempo plataforma minutos'].mean() / 60  # Convert to hours
                avg_aov_time = df_selected['tempo AOV minutos'].mean() / 60  # Convert to hours
                avg_total_time = df_selected['tempo total'].mean() / 60  # Convert to hours

                # Definir cores personalizadas
                gradient_color1 = '#204782'  # Deep Blue
                gradient_color2 = '#2f5694'  # Light Sky Blue

                # Estilo CSS inline
                container_style = f"""
                    background: linear-gradient(135deg, {gradient_color1}, {gradient_color2});
                    padding: 1rem;
                    border-radius: 0.5rem;
                    border:0.5px solid {color_gray};
                    border-width: 2px;
                    box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19);
                    color: {color_white};
                """

                label_style = f"""
                    color: {color_white};
                """

                value_style = f"""
                    color: {color_white};
                    font-weight: bold;
                """

                # Exibir os resultados como métricas (cards)
                col1, col2, col3 = st.columns(3)

                with col1:
                    with st.container():
                        st.markdown(
                            f'<div style="{container_style}"><span style="{label_style}">Média de Tempo Plataforma:</span> <span style="{value_style}">{avg_platform_time:.2f} horas</span></div>',
                            unsafe_allow_html=True)

                with col2:
                    with st.container():
                        st.markdown(
                            f'<div style="{container_style}"><span style="{label_style}">Média de Tempo AOV:</span> <span style="{value_style}">{avg_aov_time:.2f} horas</span></div>',
                            unsafe_allow_html=True)

                with col3:
                    with st.container():
                        st.markdown(
                            f'<div style="{container_style}"><span style="{label_style}">Média de Tempo Total:</span> <span style="{value_style}">{avg_total_time:.2f} horas</span></div>',
                            unsafe_allow_html=True)

                # Calcular as médias de tempo para cada aluno
                student_time_data = df_selected.groupby('Nome completo')[
                    ['tempo plataforma minutos', 'tempo AOV minutos', 'tempo total']].mean()
                st.markdown("<br>", unsafe_allow_html=True)

          
            with st.expander("Relação de Progresso por Aluno", expanded=True):

                df_selected['total progresso'] = df_selected['total progresso'].str.rstrip('%').astype('float')

                # Calcular a média do progresso
                avg_progress = df_selected['total progresso'].mean()


                # Estilo CSS inline
                container_style = f"""
                        background: linear-gradient(135deg, {gradient_color1}, {gradient_color2});
                        padding: 1rem;
                        border-radius: 0.5rem;
                        border:0.5px solid {color_gray};
                        border-width: 2px;
                        box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19);
                        color: {color_white};
                    """

                label_style = f"""
                        color: {color_white};
                    """

                value_style = f"""
                        color: {color_white};
                        font-weight: bold;
                    """

                # Exibir o resultado como métrica (card)
                with st.container():
                    st.markdown(
                        f'<div style="{container_style}"><span style="{label_style}">Progresso Médio por Aluno:</span> <span style="{value_style}">{avg_progress:.2f}%</span></div>',
                        unsafe_allow_html=True)
                st.markdown("<br>", unsafe_allow_html=True)

                student_progress_data = df_selected.groupby('Nome completo')['total progresso'].mean()
                
                # Criar um dicionário mapeando gestores para cada aluno
                gestor_df = dataframe_completo.groupby('Nome completo')[
                    'Gestor'].agg('first')

                # Juntar os DataFrames usando a coluna 'Nome' como chave de junção
                student_progress_data = pd.merge(
                    student_progress_data, gestor_df, on='Nome completo')

                # Converter o DataFrame para ter um formato adequado para st.line_chart
                student_progress_data = student_progress_data.reset_index()
                student_progress_data.columns = ['Aluno', 'Progresso Médio','Gestor']
                student_progress_data = student_progress_data.set_index('Aluno')


                # Inserir um controle deslizante para definir o número de alunos com maior progresso
                num_top_students = st.slider('Selecione o número de alunos com maior progresso', min_value=1,
                                             max_value=50, value=10)

                # Obter os 'num_top_students' alunos com maior progresso
                top_students = student_progress_data.nlargest(num_top_students, 'Progresso Médio')
                
                top_students['Progresso Médio'] = top_students['Progresso Médio'].apply(lambda x: f'{x}%')
                
                # Exibir os 'num_top_students' alunos com maior progresso
                st.subheader(f'Top {num_top_students} Alunos com maior progresso')
                st.write(top_students)

                # Inserir um controle deslizante para definir o número de alunos com menor progresso
                num_bottom_students = st.slider('Selecione o número de alunos com menor progresso', min_value=1,
                                                max_value=50, value=10)

                # Obter os 'num_bottom_students' alunos com menor progresso
                bottom_students = student_progress_data.nsmallest(num_bottom_students, 'Progresso Médio')
                bottom_students['Progresso Médio'] = bottom_students['Progresso Médio'].apply(lambda x: f'{x}%')

                # Exibir os 'num_bottom_students' alunos com menor progresso
                st.subheader(f'Top {num_bottom_students} Alunos com menor progresso')
                st.write(bottom_students)

        except ValueError:
            st.error("Não há dados o suficiente")
        except Exception as error:
            print(error)
            st.error("Erro em algum filtro")


if __name__ == "__main__":
    main()
