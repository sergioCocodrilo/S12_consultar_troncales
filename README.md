# Troncales por posición

Programa para ayuda al crear un inventario de troncales / servicios en BDTD.

Está pensado para usarse de la siguiente manera:

1. Revisar en la sala de Tx los enlaces del S12.

2. Crear un archivo CSV con información de los módulos (H'). El archivo debe guardarse como ".csv" en la carpeta data/input/ e incluir las siguientes columnas:
		- MÓDULO (H'nnnn)
		- SALA 
		- BASTIDOR (ej. 101B46)
		- TABLILLA (ej. 0102)
		- PAR (1 - 19)
		- ESTADO (abierto|conectado|loop)

3. El programa lee el archivo y por cada módulo, agrega la información obtenida de la instrucción:
	`DISPLAY-TRUNK:NA1=H'____,TSLIST1=1&&5.`

4. El resultado de la consulta se almacena en un archivo CSV con el mismo nombre que el archivo de entrada pero en data/output. Este procedimiento ayuda a determinar si el estado físico (abierto|conectado|loop) concuerda con el estado lógico (resultado de la consulta al sistema).
