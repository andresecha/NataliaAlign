# Alineamiento Multilingüe de Poesía

Esta es una herramienta fácil de usar diseñada para investigadores y traductores. Utiliza Inteligencia Artificial (LaBSE) para comparar automáticamente versos originales en ruso con sus múltiples traducciones y colocarlos juntos en una tabla limpia y editable.

## ¿Qué necesitas para empezar?

Esta herramienta está diseñada para que cualquier persona pueda usarla, ¡incluso si no tienes experiencia previa programando! Solo necesitas tener **Python** instalado en tu computadora.

### 1. Instalar Python (Si no lo tienes)
- **Usuarios de Windows:** 
  1. Abre la tienda de aplicaciones "Microsoft Store" en tu ordenador, busca "Python 3" e instálalo gratis.
  2. Alternativamente, puedes descargarlo desde [python.org/downloads](https://www.python.org/downloads/). 
  3. **¡IMPORTANTE!** Si lo instalas desde la web, asegúrate de marcar la casilla que dice **"Add python.exe to PATH"** en la primera pantalla del instalador.
- **Usuarios de Mac:**
  1. Descarga el instalador desde [python.org/downloads](https://www.python.org/downloads/) y sigue las instrucciones en pantalla.

---

## ¿Cómo iniciar la herramienta?

¡Es muy sencillo! Una vez que hayas descargado esta carpeta, no tienes que lidiar con comandos complejos.

- **Si usas Windows:**
  Haz doble clic en el archivo llamado `ejecutar_windows.bat` (o simplemente `ejecutar_windows` si no ves la extensión). ¡Eso es todo! La primera vez tardará unos minutos en configurar todo, y luego abrirá automáticamente la aplicación en tu navegador de internet.

- **Si usas Mac o Linux:**
  Abre la terminal, navega hasta esta carpeta y ejecuta el archivo haciendo doble clic en él, o escribiendo `./ejecutar_herramienta.sh`.

---

## ¿Cómo añadir nuevos poemas y traducciones?

El sistema detecta automáticamente cualquier poema nuevo que quieras analizar, siempre y cuando sigas estas sencillas **reglas de nombrado** y guardes los archivos de texto (`.txt`) dentro de la carpeta `data/`:

**1. El poema original (ruso):**
Debe llevar un **"Identificador"** al principio y terminar con la palabra **original**.
*   *Ejemplo:* `105 original.txt` o `poema_amor original.txt`

**2. Las traducciones:**
Deben llevar exactamente el **mismo Identificador** al inicio, seguido de la palabra **trad**.
*   *Ejemplo:* `105 trad 1.txt`, `105 trad 2.txt`, o `poema_amor trad ingles.txt`

¡Y ya está! La próxima vez que abras la aplicación, el identificador (`105` o `poema_amor`) aparecerá automáticamente en el menú desplegable. 

---

## ¿Cómo usar la interfaz gráfica?

1. En el menú desplegable, selecciona el poema que deseas analizar.
2. Si es la primera vez, presiona **"Alinear Versos"**. La IA leerá los textos, comprenderá los significados, cruzará los datos y organizará las traducciones en una tabla fila por fila junto a los versos rusos correspondientes.
3. **Edición Manual:** Verás una tabla con los resultados. La IA está diseñada para hacer el 95% del trabajo pesado. Sin embargo, los traductores a veces invierten el orden poético de las frases. Si notas algún desajuste menor, **puedes hacer doble clic en cualquier celda de la tabla para modificar o mover el texto** a tu gusto.
4. Cuando el poema esté perfecto, selecciona el formato (Excel o CSV) y presiona **"Guardar Cambios"**.

*Nota: El algoritmo inteligente es tolerante; si un traductor unió dos ideas en una frase, la herramienta agrupará el texto. Si una frase no fue traducida en absoluto, la celda en la tabla simplemente quedará en blanco de forma impecable.*
