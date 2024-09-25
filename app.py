from flask import Flask, render_template, request, redirect, url_for, send_file
import pandas as pd
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib import colors
from io import BytesIO
import datetime

app = Flask(__name__)

# Ruta para mostrar el formulario de selección de grado
@app.route('/')
def home():
    df = pd.read_csv('data/estudiantes.csv')
    grados = sorted(df['Grado'].unique())
    return render_template('buscar_estudiantes.html', grados=grados)

# Ruta para mostrar todos los estudiantes de un grado
@app.route('/listar', methods=['POST'])
def listar_estudiantes_por_grado():
    grado = request.form['grado']
    df = pd.read_csv('data/estudiantes.csv')
    
    # Filtrar estudiantes por el grado seleccionado
    estudiantes = df[df['Grado'] == int(grado)].sort_values(by='Nombre').to_dict(orient='records')
 
    if estudiantes:
        return render_template('marcar_asistencia.html', estudiantes=estudiantes, grado=grado)
    else:
        return "No hay estudiantes en este grado", 404

# Ruta para actualizar asistencia de varios estudiantes
@app.route('/marcar_asistencia', methods=['POST'])
def marcar_asistencia():
    df = pd.read_csv('data/estudiantes.csv')

    # Recibir los datos del formulario y actualizar asistencia
    for key, value in request.form.items():
        if key.startswith("Almorzo_"):
            estudiante_id = int(key.split('_')[1])
             # Verificar si el checkbox fue marcado
            df.loc[df['ID'] == estudiante_id, 'Almorzo'] ='Si' if value == 'on' else 'No'

        elif key.startswith("Repitio_"):
            estudiante_id = int(key.split('_')[1])
            df.loc[df['ID'] == estudiante_id, 'Repitio'] = 'Si' if value == 'on' else 'No'

    # Guardar cambios en el CSV
    df.to_csv('data/estudiantes.csv', index=False)
    
    return redirect(url_for('home'))

# Ruta para restablecer la asistencia de todos los estudiantes
@app.route('/iniciar_jornada', methods=['POST'])
def iniciar_jornada():
    df = pd.read_csv('data/estudiantes.csv')

    # Restablecer los valores de 'Almorzo' y 'Repitio' para todos los estudiantes
    df['Almorzo'] = 'No'
    df['Repitio'] = 'No'

    # Guardar los cambios en el CSV
    df.to_csv('data/estudiantes.csv', index=False)

    return redirect(url_for('home'))

# Ruta para imprimir la asistencia del grado en un PDF
@app.route('/imprimir', methods=['POST'])
def imprimir_pdf():
    grado = request.form['grado']
    df = pd.read_csv('data/estudiantes.csv')
    
    # Filtrar estudiantes por grado
    df_grado = df[df['Grado'] == int(grado)]

    # Creamos un buffer en memoria para generar el PDF
    buf = BytesIO()

    # Utilizamos SimpleDocTemplate para crear el documento
    doc = SimpleDocTemplate(buf)

    # Título del PDF y fecha
    titulo = f"Asistencia al comedor - Grado {grado} - {datetime.date.today()}"
    data = [[titulo, '', ''], ['Nombre', 'ID', 'Almorzo', 'Repitio']]

    # Añadimos los datos de los estudiantes a la tabla
    for i, row in df_grado.iterrows():
        data.append([row['Nombre'], str(row['ID']), row['Almorzo'], row['Repitio']])

    # Creamos una tabla a partir de los datos
    table = Table(data)

    # Aplicamos estilos a la tabla
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.gray),  # Fondo gris para la primera fila (título)
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),  # Texto blanco para el título
        ('BACKGROUND', (0, 1), (-1, 1), colors.lightgrey),  # Fondo gris claro para la cabecera
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),  # Alineación al centro para todo el contenido
        ('GRID', (0, 0), (-1, -1), 1, colors.black),  # Líneas de cuadrícula negras
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),  # Fuente en negrita para el título
        ('FONTSIZE', (0, 0), (-1, 0), 14),  # Tamaño de fuente más grande para el título
        ('FONTSIZE', (0, 1), (-1, -1), 12),  # Tamaño de fuente regular para los datos
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),  # Espaciado inferior en el título
    ]))

    # Construimos el PDF
    doc.build([table])

    # Configuramos el buffer para que esté listo para enviar
    buf.seek(0)

    # Enviar el archivo PDF generado como una descarga
    return send_file(buf, as_attachment=True, download_name=f'asistencia_grado_{grado}.pdf', mimetype='application/pdf')

if __name__ == '__main__':
    app.run(debug=True)
