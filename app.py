from google.colab import drive
import os
import pandas as pd
import matplotlib.pyplot as plt

# 1) Cargar los datos de los archivos
drive.mount('/content/drive')

ruta_principal = '/content/drive/MyDrive/BANCOS'

resultados = []

for ruta_subcarpeta in os.scandir(ruta_principal):
    if ruta_subcarpeta.is_dir():
        archivos_especificos = ['1C201112002.xls', '1N60001122020n.xls']
        
        for archivo_especifico in archivos_especificos:
            ruta_archivo = os.path.join(ruta_subcarpeta.path, archivo_especifico)
            
            if os.path.exists(ruta_archivo):
                df = pd.read_excel(ruta_archivo, header=None)  # 1)
                
                df = df.dropna()

                # 2) Calcular el beneficio neto
                ingresos_filas = df[df.iloc[:, 1].str.contains('INGRESOS', na=False)] 
                gastos_filas = df[df.iloc[:, 1].str.contains('GASTOS', na=False)]
                
                total_ingresos = ingresos_filas.iloc[:, -1].sum()
                total_gastos = gastos_filas.iloc[:, -1].sum()
                beneficio_neto = total_ingresos - total_gastos  # 2)

                # 3) Calcular el capital total
                activos_filas = df[df.iloc[:, 1].str.contains('ACTIVOS', na=False)]
                pasivos_filas = df[df.iloc[:, 1].str.contains('PASIVOS', na=False)]

                total_activos = activos_filas.iloc[:, -1].sum()
                total_pasivos = pasivos_filas.iloc[:, -1].sum()
                capital_total = total_activos - total_pasivos  # 3)

                # 4) Calcular el índice de rentabilidad
                indice_rentabilidad = (beneficio_neto / capital_total) * 100 # 4)

                resultados.append({
                    'Archivo': archivo_especifico,
                    'Beneficio Neto': beneficio_neto,
                    'Capital Total': capital_total,
                    'Índice de Rentabilidad': indice_rentabilidad
                })

                print(f"\n1) Archivo cargado: {archivo_especifico}")
                print(f"Total de ingresos: {total_ingresos:,.2f}")
                print(f"Total de gastos: {total_gastos:,.2f}")
                print(f"2) Beneficio neto: {beneficio_neto:,.2f}")
                print(f"Total de activos: {total_activos:,.2f}")
                print(f"Total de pasivos: {total_pasivos:,.2f}")
                print(f"3) Capital total: {capital_total:,.2f}")
                print(f"4) Índice de Rentabilidad: {indice_rentabilidad:,.2f}%")

df_resultados = pd.DataFrame(resultados)

print("\nResultados recopilados:")
print(df_resultados)

# 5) Análisis exploratorio de los índices de rentabilidad
print("\n5) Análisis Exploratorio de los Índices de Rentabilidad:")

rango_rentabilidad = df_resultados['Índice de Rentabilidad'].min(), df_resultados['Índice de Rentabilidad'].max()
print(f"Rango de los índices de rentabilidad: Desde {rango_rentabilidad[0]:.2f}% hasta {rango_rentabilidad[1]:.2f}%")

promedio_rentabilidad = df_resultados['Índice de Rentabilidad'].mean()
desviacion_rentabilidad = df_resultados['Índice de Rentabilidad'].std()
print(f"Promedio de los índices de rentabilidad: {promedio_rentabilidad:,.2f}%")
print(f"Desviación estándar de los índices de rentabilidad: {desviacion_rentabilidad:,.2f}%")

tendencia = "Tendencia creciente" if df_resultados['Índice de Rentabilidad'].iloc[-1] > df_resultados['Índice de Rentabilidad'].iloc[0] else "Tendencia decreciente"
print(f"Análisis de tendencias: {tendencia}")  # 5)

# 6) Visualizar los resultados usando gráficos
print("\n6) Gráficos:")
plt.figure(figsize=(10, 6))
plt.plot(df_resultados['Archivo'], df_resultados['Índice de Rentabilidad'], marker='o', color='b', linestyle='-', label='Rentabilidad')
plt.title('Evolución de la Rentabilidad a lo largo del tiempo')
plt.xlabel('Archivos (BANCO)')
plt.ylabel('Índice de Rentabilidad (%)')
plt.xticks(rotation=45, ha='right')
plt.grid(True)
plt.tight_layout()
plt.legend()
plt.show()

print("\n")
plt.figure(figsize=(10, 6))
plt.scatter(df_resultados['Beneficio Neto'], df_resultados['Capital Total'], color='g', alpha=0.6)
plt.title('Relación entre Beneficio Neto y Capital Total')
plt.xlabel('Beneficio Neto')
plt.ylabel('Capital Total')
plt.grid(True)
plt.tight_layout()
plt.show() # 6)
