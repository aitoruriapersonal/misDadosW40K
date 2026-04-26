# misDadosW40K

Repositorio que contiene un programa de tirada de dados de Warhammer 40K.
El repositorio contiene varias versiones del mismo programa (web, python).

## Estructura

```
/
├── python/          -> Version Python (tkinter GUI + modo consola)
│   ├── main.py      -> Punto de entrada
│   └── app/
│       ├── dado.py      -> Modelo: dado
│       ├── tirada.py    -> Modelo: tirada
│       ├── historico.py -> Modelo: historico
│       ├── lanzador.py  -> Servicio: lanzador
│       └── ventana.py   -> Vista: ventana principal (tkinter)
└── web/             -> Version Web (HTML/CSS/JS vanilla)
    ├── index.html
    ├── css/
    │   └── estilos.css
    └── js/
        └── app.js
```

## Version Python

### Requisitos
- Python 3.8+
- tkinter (incluido en la instalacion estandar de Python)

### Uso

**Modo ventana** (doble click o sin argumentos):
```bash
python python/main.py
```

**Modo consola** (con argumentos `<cantidad> <lados>`):
```bash
python python/main.py 3 6    # lanza 3 dados de 6 caras
python python/main.py 2 20   # lanza 2 dados de 20 caras
```

## Version Web

Abrir `web/index.html` en cualquier navegador moderno. No requiere servidor ni dependencias externas.

## Funcionalidades

- Configuracion de cantidad de dados y numero de lados por dado
- Animacion de 3 segundos al lanzar (caras del dado cambiando cada 0,5 s)
- Visualizacion del resultado total y detalle de cada dado
- Historico de tiradas con hora
- Boton para resetear el historico
- Boton de reseteo global (configuracion + historico)
- Boton de cierre de la aplicacion
