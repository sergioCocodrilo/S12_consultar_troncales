# Troncales por posici'on

Programa para ayudar en revisar el estado de las troncales.
Est'a pensado para usarse de la siguiente manera:
1. Revisar en la sala de Tx los enlaces del S12.
2. Se hace un archivo CSV de los m'odulos (H') y su estado (abierto|conectado|loop)
	La lista debe guardar en la carpeta data/input/ y debe tener extensi'on .txt
3. El programa lee la lista generada y consulta el estado de la troncal con la siguiente instrucci'on:
	`DISPLAY-TRUNK:NA1=H'____,TSLIST1=1&&5.`
4. El resultado de la consulta ayuda a determinar si el estado f'isico (abierto|conectado|loop) concuerda con el estado l'ogico.
