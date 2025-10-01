"""
TEMPLATE PARA GOOGLE DOCS

Este archivo contiene el contenido que debería tener el template de Google Docs
para ser usado con la función generateDocuments del app.gs.

Para crear el template:
1. Crear un nuevo documento de Google Docs
2. Copiar y pegar el contenido de abajo
3. Formatear según sea necesario
4. Obtener el ID del documento
5. Configurar TEMPLATE_DOC_ID en el archivo .env

Los placeholders [[CAMPO]] serán reemplazados automáticamente por los datos del formulario.

PLACEHOLDERS DISPONIBLES:
- [[TITULO_ACTIVIDAD]] - Título de la actividad
- [[DOCENTE_RESPONSABLE]] - Nombre del docente responsable
- [[DEPARTAMENTO]] - Departamento/Instituto de pertenencia
- [[EQUIPO]] - Lista de integrantes (incluye nombre, DNI, correo y claustro)
- [[FUNDAMENTACION]] - Fundamentación de la actividad
- [[OBJETIVOS]] - Objetivos y propósitos
- [[METODOLOGIA]] - Metodología a utilizar
- [[GRADOS]] - Grados/ciclos incluidos
- [[MATERIALES_PRESUPUESTO]] - Materiales e insumos
- [[PERIODOS]] - Períodos propuestos (formato: "2025: Marzo, Abril | 2026: Mayo")
- [[FECHA_GENERACION]] - Fecha de generación del documento
- [[CUADRO_FIRMA]] - Espacio para firma

NOTA SOBRE [[EQUIPO]]:
El placeholder [[EQUIPO]] será reemplazado por una lista formateada que incluye:
- Apellido y Nombre
- DNI
- Correo electrónico
- Claustro (Docente, Nodocente, Estudiante, Graduado/a, Investigador/a, etc.)

Ejemplo de formato:
  • García, María Elena
    DNI: 12345678
    Correo: garcia@uncoma.edu.ar
    Claustro: Docente
"""

TEMPLATE_CONTENT = """
FORMULARIO DE ACTIVIDAD EDUCATIVA

Convocatoria [[AÑO_CONVOCATORIA]]



Título de la Actividad

[[TITULO_ACTIVIDAD]]

Docente Responsable: [[DOCENTE_RESPONSABLE]]

Departamento/Instituto de pertenencia: [[DEPARTAMENTO]]

Equipo

[[EQUIPO]]

Fundamentación

[[FUNDAMENTACION]]

Objetivos o Propósitos

[[OBJETIVOS]]

Metodología

[[METODOLOGIA]]

Grados incluidos en la actividad

[[GRADOS]]

Materiales e insumos / Presupuesto

[[MATERIALES_PRESUPUESTO]]

Períodos propuestos para la realización de la actividad

[[PERIODOS]]

Firma del Docente Responsable

[[CUADRO_FIRMA]]

Documento generado automáticamente el [[FECHA_GENERACION]]
"""

if __name__ == "__main__":
    print("=== TEMPLATE PARA GOOGLE DOCS ===")
    print()
    print("Copie el siguiente contenido en un nuevo documento de Google Docs:")
    print()
    print("=" * 60)
    print(TEMPLATE_CONTENT)
    print("=" * 60)
    print()
    print("Instrucciones:")
    print("1. Crear nuevo documento en Google Docs")
    print("2. Pegar el contenido de arriba")
    print("3. Formatear según necesidades")
    print("4. Obtener el ID del documento de la URL")
    print("5. Configurar TEMPLATE_DOC_ID en .env")