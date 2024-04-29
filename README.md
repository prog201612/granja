# Estructura de dades

## CONSTANTS
- `TIPUS DE CAPACITAT`: Corral, Aliment, Rebuig

## TAULES i/o (LLISTATS)

### GLOBAL GRANJA
- `TIPUS PRODUCTES`: El tipus de producte defineix un nom i el TIPUS DE CAPACITAT on pot anar el producte. Un ESTOC d'una CAPACITAT requireix un TIPUS PRODUCTES.
- `PERSONA LEGAL`: Nom, DNI i altres dades  d'una persona física. Aquesta posteriorment pot ser Proveïdor, Client, Treballador, Banc, etc., o una combinació d'aquests.

### EXPLOTACIÓ
- `PROVEÏDORS`: Cal tenir algú que ens proveeix algun bé físic o servei. Aquest tindrà una PERSONA LEGAL assignada.
- `ARTICLES DEL PROVEÏDOR`: Cal estar assignat a un proveïdor i que tingui assignat un TIPUS PRODUCTES (GLOBAL GRANJA). Áixò defineix a quin TIPUS DE CAPACITAT pot estar magatzemat el producte, a part del tipus de producte com per exemple la seva qualitat. Cal entendre que els ESTOCS d'una CAPACITAT guarden productes d'un TIPUS PRODUCTE. 
- `COMANDES DEL PROVEÏDOR`: Es pot definir la caçalera i línies d'una comanda d'ARTICLES DEL PROVEÏDOR. Les línies de la comanda es creen aquí. EXEMPLE: Xais (diferentes qualitats), Pinso (diferentes qualitats), Rebuig (?). En aquest últim cas tenim que el proveïdor de Rebuig pot ser la mateixa Granja, així la granja la crearem com a proveïdor de la granja.
- `DETALLS DE LA COMANDA DEL PROVEÏDOR`: (igual a les línies d'una comanda). Aquí no creem les línies. L'objectiu d'aquest llistat és consultar els productes que estan sol·licitats però que encara no els hem entrat de manera digitalitzada a la granja digital (Processada). Disposa de la ACCIÓ: "Crear Entrades de Material". Ens permet enviar els productes sol·licitats a ENTRADES DE MATERIAL. EXEMPLE: demanem un camió de xais, hem encarregat pinso, o ens volem recordar que tenim rebuig per desar.
- `ENTRADES DE MATERIAL`: Zona intermitja on hi ha els productes que ja han arribat físicament a la granja però que encara no s'han magatzemat a cap ESTOC d'una CAPACITAT. Disposa de la ACCIÓ: "Enviar material al estoc". Ens permet seleccionar una CAPACITAT del mateix TIPUS DE CAPACITAT que té l'ARTICLE DEL PROVEÏDOR on guardar el material. El sistema hauria de ser prou inteligent com per detectar si ja hi ha un ESTOC dins la CAPACITAT amb el mateix TIPUS PRODUCTE (qualitat). Si existeix incrementa i si no es crea un nou ESTOC dins la CAPACITAT. EXEMPLE: ens ha arribat un camió de xais, ens ha arribat el pinso, o senzillament ja volem moure Rebuig cap a alguna CAPACITATS.
- `CAPACITATS`: és una abstracció que engloba zones físiques dins la granja. Les zones físiques reals son CAPACITATS ESTOC que penjen d'una CAPACITAT. Una capacitat té TIPUS DE CAPACITAT actualment amb els valors Corral, Aliment, Rebuig.
- `CAPACITATS ESTOC`: Zona física dins la granja que pertany a una CAPACITAT, això defineix que en aquell estoc només hi poden anar productes d'un TIPUS DE PRODUCTE que engloba un TIPUS DE CAPACITAT i una qualitat del producte. Disposa de la ACCIÓ: "Moure estoc entre capacitats del mateix tipus" que ens permet moure el producte magatzemat entre estocs sempre iquant aquests siguin del mateix tipus. EXEMPLE: volem moure xais a un altre corral, volem moure pinso a una altre zona o volem moure rebuig.

### CLIENTS
- `CLIENTS`: no hi ha molt a dir.
- `VENDES`: les vendes tenen DETALL VENDA amb els articles (XAIS) que poden sortir d'un CAPACITAT STOC de tipus Corral.
    - `ACCIONS`:
        - `"Afegir articles de l'estoc a la venda"`: parmet agafar articles (xais) dels CAPACITATS ESTOC de tipus Corral i vendre'ls a un CLIENTS.
        - `"Defuncions..."`: Permet generar defuncions que a posteriori haurem d'anar a DEFUNCIONS per modificar el tipus de defunció i adjuntar-hi la documentació (imatge).
- `DEFUNCIONS`: Animals d'una venda que han mort.

<br/>

## CIRQÜITS

### ENTRADA DE MATERIAL
- `COMANDES DEL PROVEÏDOR`: Creem la comanda i les línies de la comanda.
- `DETALLS DE LA COMANDA DEL PROVEÏDOR`: Podem enviar els items de la comanda a ENTRADES DE MATERIAL "Crear Entrades de Material" o directament a CAPACITATS ESTOC "Enviar material al estoc".

### MOURE MATERIAL ENTRE ESTOCS
- `CAPACITATS ESTOC`: Tenim la acció "Moure estoc entre capacitats del mateix tipus".

### VENTES DE MATERIAL
- `VENTES`: Afegim una venta i utilitzem l'acció "Afegir articles de l'estoc a la venda" per poder moure articles d'un CAPACITATS ESTOC a DETALL VENDA.