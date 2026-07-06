# CLAUDE.md — misDadosW40K

Guia de referencia para agentes de IA y colaboradores que trabajen sobre este repositorio.

---

## Resumen de la arquitectura

El proyecto implementa **dos versiones independientes** de la misma aplicacion: un lanzador de dados con tematica Warhammer 40K. Ambas versiones replican **exactamente la misma arquitectura en capas** y los mismos modelos de dominio, cada una en su propio lenguaje.

```
Capa de Dominio   →  Dado · Tirada · Historico
Capa de Servicio  →  Lanzador
Capa de Vista     →  VentanaPrincipal (Python) / Animacion + VistaResultados + VistaHistorico + Aplicacion (Web)
```

**Flujo de datos:**
1. La vista recoge la configuracion del usuario (cantidad de dados, lados).
2. Llama a `Lanzador.lanzar(cantidad, lados)`.
3. `Lanzador` crea una `Tirada`, la ejecuta y la almacena en `Historico`.
4. La vista muestra la animacion de 3 s y, al terminar, renderiza el resultado.

El calculo de la tirada se realiza **antes** de que comience la animacion; la animacion es puramente cosmética.

---

## Tecnologias utilizadas

| Version | Tecnologia | Notas |
|---------|-----------|-------|
| Python  | Python 3.8+ | Sin dependencias externas |
| Python  | tkinter + ttk | Incluido en la instalacion estandar de Python |
| Web     | HTML5 | Sin framework, sin preprocesador |
| Web     | CSS3 | Custom properties (`--var`), Flexbox |
| Web     | JavaScript ES6+ | Clases, arrow functions, `'use strict'` |

**Sin dependencias de terceros en ninguna de las dos versiones.**  
No existe `requirements.txt`, `package.json`, ni ningun gestor de paquetes.

---

## Comandos para ejecutar

### Version Python

```bash
# Modo ventana (interfaz grafica tkinter)
python python/main.py

# Modo consola (imprime resultado y termina)
python python/main.py <cantidad> <lados>

# Ejemplos:
python python/main.py 3 6    # 3d6
python python/main.py 2 20   # 2d20
```

### Version Web

```bash
# Abrir directamente en el navegador (sin servidor necesario)
start web/index.html          # Windows
open web/index.html           # macOS
xdg-open web/index.html       # Linux
```

### Pruebas

No existe un framework de tests automatizados. Las pruebas se realizan manualmente ejecutando la aplicacion. Si se añaden tests en el futuro, deben residir en `python/tests/` y seguir el modulo `unittest` de la biblioteca estandar.

### Compilacion / Build

No hay paso de compilacion ni build. Ambas versiones se ejecutan directamente desde los fuentes.

---

## Convenciones de codigo

### Python

- **Cabecera obligatoria** en todos los modulos: `# -*- coding: utf-8 -*-`
- **Idioma**: nombres de variables, metodos, clases y docstrings en **espanol** (sin tildes en los identificadores, con tildes en docstrings y comentarios).
- **Tipado**: type annotations en todos los metodos publicos (`-> None`, `-> int`, `List[int]`, etc.).
- **Docstrings**: formato Google (seccion `Args:` y `Returns:` cuando aplica).
- **Atributos privados**: prefijo `_` (convencion, no name mangling con `__`).
- **Propiedades**: usar `@property` en lugar de getters explicitos. Propiedades de solo lectura; sin setters salvo necesidad justificada.
- **Validacion**: en `__init__` de modelos, lanzar `ValueError` con mensaje descriptivo si los parametros son invalidos.
- **Imports**: primero stdlib, luego imports relativos del propio paquete (con `.`).
- **Constantes de modulo**: `MAYUSCULAS_CON_GUION_BAJO` al principio del fichero.
- **tkinter**: estilos en `_configurar_estilos()`, construccion de widgets en metodos `_crear_frame_*()`, manejadores de eventos con prefijo `_on_`.

### JavaScript

- **`'use strict';`** al inicio del fichero.
- **Sin tildes ni acentos** en codigo ni comentarios (convencion documentada en el propio fichero).
- **Clases ES6** para todos los componentes: `Dado`, `Tirada`, `Historico`, `Lanzador`, `Animacion`, `VistaResultados`, `VistaHistorico`, `Aplicacion`.
- **Atributos privados**: prefijo `_` (misma convencion que Python).
- **Propiedades**: `get` accessors, sin setters salvo necesidad.
- **JSDoc**: en constructores y metodos publicos.
- **Nomenclatura**: `camelCase` para metodos y variables, `PascalCase` para clases, `MAYUSCULAS` para constantes de modulo.
- **DOM**: toda la manipulacion del DOM esta en las clases de Vista (`Animacion`, `VistaResultados`, `VistaHistorico`). La clase `Aplicacion` orquesta y registra eventos.
- **Inicializacion**: `document.addEventListener('DOMContentLoaded', () => { new Aplicacion(); });` al final del fichero.

### CSS

- **Variables CSS** (custom properties) definidas en `:root` para toda la paleta de colores y valores reutilizables.
- Nomenclatura de clases en `kebab-case`.
- Selectores de ID (`#`) solo para elementos unicos de la UI referenciados desde JS.
- **Sin frameworks CSS**; todo escrito a mano.

### Paleta de colores (tema W40K oscuro)

Ambas versiones usan los mismos valores cromaticos:

| Token | Valor | Uso |
|-------|-------|-----|
| Fondo principal | `#1a1a2e` | Fondo de ventana / body |
| Acento dorado | `#c0a060` | Titulos, bordes decorativos |
| Texto principal | `#e0e0e0` | Texto general |
| Boton primario | `#8b0000` | Boton "Lanzar dados" |
| Boton secundario | `#2a2a5e` | Botones de reset |
| Fondo dado | `#f5e6c8` | Cara del dado (animacion) |
| Punto dado | `#2c1810` | Puntos del dado (animacion) |

---

## Estructura de carpetas

```
misDadosW40K/
├── CLAUDE.md               <- Este fichero
├── README.md
├── LICENSE
│
├── python/                 <- Version Python
│   ├── main.py             <- Punto de entrada; detecta modo (consola/ventana)
│   └── app/
│       ├── __init__.py
│       ├── dado.py         <- Modelo: Dado (lanza un dado de N lados)
│       ├── tirada.py       <- Modelo: Tirada (conjunto de dados, fecha, resultados)
│       ├── historico.py    <- Modelo: Historico (lista de Tiradas)
│       ├── lanzador.py     <- Servicio: Lanzador (crea tiradas, gestiona historico)
│       └── ventana.py      <- Vista: VentanaPrincipal (tkinter GUI)
│
└── web/                    <- Version Web
    ├── index.html          <- Estructura HTML; carga estilos y script
    ├── css/
    │   └── estilos.css     <- Tema oscuro W40K con custom properties
    └── js/
        └── app.js          <- Modelos + Servicio + Vistas + Aplicacion (todo en un fichero)
```

---

## Flujo de desarrollo

1. **Cambio en la logica de negocio** (reglas de lanzamiento, validaciones, historico):
   - Modificar el modelo/servicio en Python (`dado.py`, `tirada.py`, `historico.py`, `lanzador.py`).
   - Replicar el cambio en las clases equivalentes de `web/js/app.js`.
   - Ambas implementaciones deben permanecer **sincronizadas y funcionalmente identicas**.

2. **Cambio en la interfaz de usuario**:
   - Python: modificar `ventana.py` (metodos `_crear_frame_*`, `_on_*`, animacion).
   - Web: modificar `index.html`, `estilos.css` y/o la clase `Aplicacion` / vistas en `app.js`.
   - Los cambios de UI no requieren sincronizacion entre versiones (cada una tiene su propia capa de presentacion).

3. **Cambio en la animacion**:
   - Las constantes `DURACION_ANIMACION_MS = 3000` e `INTERVALO_ANIMACION_MS = 500` existen en ambos ficheros (`ventana.py` y `app.js`) y deben mantenerse iguales.
   - La animacion muestra un maximo de 6 dados visibles independientemente de la cantidad configurada.
   - Para dados con mas de 6 lados, se muestra el numero en lugar de puntos.

4. **Limites de configuracion**: cantidad de dados 1–100, lados por dado 2–100 (validados en modelo y en vista).

---

## Reglas para agentes de IA

### Reglas obligatorias

1. **Sincronizacion de versiones**: cualquier cambio en la logica de dominio o de servicio debe aplicarse en **ambas versiones** (Python y Web) salvo que el cambio sea exclusivo de una tecnologia concreta. Nunca dejar las versiones en estado inconsistente.

2. **Sin dependencias externas**: no añadir librerias de terceros, frameworks, ni gestores de paquetes sin solicitud explicita del usuario. La ausencia de dependencias es una decision de diseno deliberada.

3. **Respetar el idioma**: los identificadores (variables, funciones, clases, parametros) se nombran en **espanol**. Los comentarios en Python pueden llevar tildes; los comentarios en JavaScript no deben llevar tildes (convencion ya establecida en el fichero).

4. **Cabecera UTF-8 en Python**: todo fichero `.py` nuevo o modificado debe comenzar con `# -*- coding: utf-8 -*-`.

5. **Mantener type annotations en Python**: no eliminar ni relajar las anotaciones de tipo existentes. Los metodos nuevos deben incluirlas.

6. **No romper la separacion de capas**: la logica de negocio (modelos y servicio) no debe contener referencias a tkinter, al DOM ni a ningun elemento de UI. La vista no debe realizar calculos de negocio.

7. **Validacion en modelos**: las reglas de validacion de parametros (`ValueError` si `lados < 2`, etc.) deben estar en los constructores de los modelos, no en la vista.

8. **Atributos privados**: usar el prefijo `_` para todos los atributos de instancia que no formen parte de la API publica. No usar `__` (name mangling) salvo razon justificada.

9. **No añadir servidor ni build step**: la version web debe seguir siendo abrible directamente en el navegador con `file://`. No introducir bundlers, transpiladores ni servidores de desarrollo sin solicitud explicita.

10. **Paleta de colores**: respetar los tokens de color del tema W40K en ambas versiones. No introducir nuevos colores hardcodeados; usar las constantes (`COLOR_*` en Python) o las variables CSS (`--color-*` en Web).

### Buenas practicas recomendadas

- Leer el fichero completo antes de modificarlo; el contexto de la clase o modulo es relevante.
- Al añadir un metodo a `VentanaPrincipal`, seguir la convencion de seccion (configuracion / construccion / manejadores / animacion) separada por bloques de comentario `# ---`.
- Al añadir una clase a `app.js`, respetar el orden existente: constantes → modelos → servicio → vistas → aplicacion principal.
- Las animaciones usan `tkinter.after()` (Python) o `setInterval`/`setTimeout` (JS); no usar `time.sleep()` ni bucles bloqueantes.
- El boton "Lanzar" debe deshabilitarse durante la animacion y re-habilitarse al terminar, en ambas versiones.
