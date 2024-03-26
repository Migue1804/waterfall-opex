import streamlit as st
import plotly.graph_objects as go
import pandas as pd

def main():
    st.image("Waterfall.jpg", width=720) 
    st.sidebar.header("Registro de OPEX")

    num_categories = st.sidebar.number_input('Número de Categorías de Costos', min_value=1, step=1, value=1, format='%d')

    if num_categories < 1:
        st.sidebar.warning("Debe ingresar al menos una categoría de costos.")
        return

    # Crear una lista para almacenar los datos de OPEX
    data = []

    for i in range(num_categories):
        st.sidebar.markdown(f"**Categoría de Costos {i+1}**")
        category_name = st.sidebar.text_input(f'Nombre de la Categoría {i+1}', key=f'category_name_{i}')
        budget = st.sidebar.number_input(f'Presupuesto - Categoría {i+1} (USD)', min_value=0.0, step=1.0, key=f'budget_{i}')
        actual = st.sidebar.number_input(f'Costo Real - Categoría {i+1} (USD)', min_value=0.0, step=1.0, key=f'actual_{i}')

        data.append({'Categoría de Costos': category_name,
                     'Presupuesto (USD)': budget,
                     'Costo Real (USD)': actual})

    df = pd.DataFrame(data)

    plot_waterfall_chart(df)

    # Mostrar los datos ingresados en la aplicación
    st.write(df)

def plot_waterfall_chart(df):
    # Calcular las diferencias entre el presupuesto y el costo real
    df['Diferencia'] = df['Costo Real (USD)'] - df['Presupuesto (USD)']

    # Calcular el total del presupuesto y el total real
    total_budget = df['Presupuesto (USD)'].sum()
    total_actual = df['Costo Real (USD)'].sum()

    # Crear una lista para las categorías de costos
    categories = ["Presupuesto"] + df['Categoría de Costos'].tolist() + ["Ejecutado"]

    # Crear una lista para los valores de la diferencia
    differences = [total_budget] + df['Diferencia'].tolist() + [total_actual]

    # Crear una lista para los tipos de medida (entrada, salida, total)
    measures = ["absolute"] + ["relative"] * len(df) + ["absolute"]

    # Crear una lista para el texto que se muestra en el gráfico
    texts = df['Presupuesto (USD)'].tolist() + [""] * len(df) + df['Costo Real (USD)'].tolist()

    # Crear la figura del Waterfall Chart
    fig = go.Figure(go.Waterfall(
        name = "OPEX",
        orientation = "v",
        measure = measures,
        x = categories,
        textposition = "outside",
        text = texts,
        y = differences,
        connector = {"line":{"color":"rgb(63, 63, 63)"}}, # Conector en negro
        increasing = {"marker":{"color":"red"}},  # Color rojo para valores mayores al presupuesto
        decreasing = {"marker":{"color":"green"}}, # Color verde para valores menores al presupuesto
        totals = {"marker":{"color":"blue"}} # Color azul para el total
    ))

    # Configurar el diseño y el título del gráfico
    fig.update_layout(
        title = 'Bridge Chart: Presupuesto vs. Costo Real por Categoría de Costos',
        xaxis_title = "Categoría de Costos",
        yaxis_title = "Diferencia (USD)",
        showlegend = True,
        height = 600,
        width = 800
    )

    # Mostrar el gráfico en la aplicación
    st.plotly_chart(fig)

if __name__ == "__main__":
    main()
