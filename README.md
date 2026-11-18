Taller 3 - Informatica 1- Grupo 3 

Miguel Santamaria Restrepo 

Taller desarrollado en Python integrando MongoDB Atlas y manejo de archivos locales. El programa comienza generando 50 registros de pacientes de forma aleatoria, validando estrictamente mediante expresiones regulares (Regex) que los identificadores, la edad, la frecuencia cardiaca y la saturación de oxígeno (SpO2) cumplan con los formatos exigidos. Tras ordenar los datos de menor a mayor según la frecuencia cardiaca de los pacientes, el sistema crea automáticamente los directorios necesarios y exporta la información en formatos TXT, CSV y JSON, dejando además un registro de auditoría de cada paso en un archivo `log.txt`. Finalmente, el algoritmo se conecta a un clúster de MongoDB Atlas para insertar todos los datos en la nube y ejecutar consultas analíticas, calculando el promedio de la frecuencia cardiaca general y detectando cuántos pacientes presentan una saturación riesgosa menor al 94%.

Para hacer funcionar el sistema, se emplearon librerías nativas de Python como `os`, `json`, `csv` y `re` para la gestión local y las validaciones de texto, integrando adicionalmente la librería externa `pymongo` para establecer la conexión remota con la base de datos

