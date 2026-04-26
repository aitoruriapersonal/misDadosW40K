// app.js - Lanzador de Dados Warhammer 40K (version web)
// Codificacion: UTF-8
// Convencion: sin tildes ni acentos en codigo ni comentarios

'use strict';

// ============================================================
// Posiciones de puntos para cada cara del dado d6 (en %)
// ============================================================
const POSICIONES_PUNTOS = {
  1: [[50, 50]],
  2: [[25, 75], [75, 25]],
  3: [[25, 75], [50, 50], [75, 25]],
  4: [[25, 25], [75, 25], [25, 75], [75, 75]],
  5: [[25, 25], [75, 25], [50, 50], [25, 75], [75, 75]],
  6: [[25, 25], [75, 25], [25, 50], [75, 50], [25, 75], [75, 75]],
};

const DURACION_ANIMACION_MS = 3000;
const INTERVALO_ANIMACION_MS = 500;

// ============================================================
// Modelo: Dado
// ============================================================
class Dado {
  /**
   * Representa un dado con un numero de lados configurable.
   * @param {number} lados - Numero de lados del dado (minimo 2).
   */
  constructor(lados) {
    if (lados < 2) throw new Error('Un dado debe tener al menos 2 lados');
    this._lados = lados;
  }

  get lados() {
    return this._lados;
  }

  /** Lanza el dado y devuelve un entero aleatorio entre 1 y lados. */
  lanzar() {
    return Math.floor(Math.random() * this._lados) + 1;
  }
}

// ============================================================
// Modelo: Tirada
// ============================================================
class Tirada {
  /**
   * Representa una tirada de un conjunto de dados del mismo tipo.
   * @param {number} cantidad - Numero de dados a lanzar.
   * @param {number} lados    - Numero de lados de cada dado.
   */
  constructor(cantidad, lados) {
    if (cantidad < 1) throw new Error('La cantidad de dados debe ser al menos 1');
    if (lados < 2) throw new Error('Los dados deben tener al menos 2 lados');
    this._cantidad = cantidad;
    this._lados = lados;
    this._resultados = [];
    this._fecha = null;
  }

  get cantidad() { return this._cantidad; }
  get lados()    { return this._lados; }
  get resultados() { return [...this._resultados]; }
  get total() { return this._resultados.reduce((a, b) => a + b, 0); }
  get fecha()  { return this._fecha; }

  /** Lanza todos los dados y almacena los resultados. */
  lanzar() {
    this._fecha = new Date();
    const dado = new Dado(this._lados);
    this._resultados = Array.from({ length: this._cantidad }, () => dado.lanzar());
    return [...this._resultados];
  }

  toString() {
    if (this._resultados.length === 0) return `${this._cantidad}d${this._lados}: sin tirar`;
    const res = this._resultados.join(', ');
    return `${this._cantidad}d${this._lados}: [${res}] = ${this.total}`;
  }
}

// ============================================================
// Modelo: Historico
// ============================================================
class Historico {
  constructor() {
    /** @type {Tirada[]} */
    this._entradas = [];
  }

  /** Agrega una tirada al historico. */
  agregar(tirada) {
    this._entradas.push(tirada);
  }

  /** Elimina todas las entradas del historico. */
  resetear() {
    this._entradas = [];
  }

  get entradas() { return [...this._entradas]; }
  get longitud()  { return this._entradas.length; }
}

// ============================================================
// Servicio: Lanzador
// ============================================================
class Lanzador {
  constructor() {
    this._historico = new Historico();
  }

  get historico() { return this._historico; }

  /**
   * Crea, lanza y almacena una tirada en el historico.
   * @param {number} cantidad
   * @param {number} lados
   * @returns {Tirada}
   */
  lanzar(cantidad, lados) {
    const tirada = new Tirada(cantidad, lados);
    tirada.lanzar();
    this._historico.agregar(tirada);
    return tirada;
  }

  resetearHistorico() {
    this._historico.resetear();
  }

  resetearTodo() {
    /**
     * Resetea todos los datos gestionados por el servicio (actualmente el historico).
     * La configuracion de la tirada (cantidad y lados) es responsabilidad de la
     * capa de vista y se resetea desde ahi. Este metodo centraliza el reseteo de
     * la capa de datos para el caso del reseteo global.
     */
    this._historico.resetear();
  }
}

// ============================================================
// Vista: Animacion de dados
// ============================================================
class Animacion {
  /**
   * Gestiona la animacion de los dados durante el lanzamiento.
   * @param {HTMLElement} contenedor - Contenedor de los dados.
   * @param {HTMLElement} textoTirando - Elemento de texto animado.
   */
  constructor(contenedor, textoTirando) {
    this._contenedor = contenedor;
    this._textoTirando = textoTirando;
    this._intervaloId = null;
    this._timeoutId = null;
    this._frame = 0;
  }

  /**
   * Inicia la animacion.
   * @param {number} cantidad - Numero de dados.
   * @param {number} lados    - Lados de cada dado.
   * @param {Function} alTerminar - Callback ejecutado al finalizar.
   */
  iniciar(cantidad, lados, alTerminar) {
    this._frame = 0;
    this._actualizarFrame(cantidad, lados);

    this._intervaloId = setInterval(() => {
      this._frame++;
      this._actualizarFrame(cantidad, lados);
    }, INTERVALO_ANIMACION_MS);

    this._timeoutId = setTimeout(() => {
      this._detener();
      alTerminar();
    }, DURACION_ANIMACION_MS);
  }

  _detener() {
    clearInterval(this._intervaloId);
    clearTimeout(this._timeoutId);
  }

  _actualizarFrame(cantidad, lados) {
    this._dibujarDados(cantidad, lados);
    const puntos = '.'.repeat((this._frame % 4) + 1);
    this._textoTirando.textContent = `Tirando${puntos}`;
  }

  _dibujarDados(cantidad, lados) {
    const numVisibles = Math.min(cantidad, 6);
    this._contenedor.innerHTML = '';

    for (let i = 0; i < numVisibles; i++) {
      const valor = Math.floor(Math.random() * Math.min(lados, 6)) + 1;
      const elemDado = this._crearElementoDado(valor, lados);
      this._contenedor.appendChild(elemDado);

      // Pequeña demora para que el efecto de sacudida se aplique correctamente
      setTimeout(() => elemDado.classList.add('animando'), 10);
    }
  }

  /**
   * Crea un elemento DOM representando la cara de un dado.
   * @param {number} valor - Valor a mostrar (1-6 con puntos, otros con numero).
   * @param {number} lados - Lados totales del dado (para decidir representacion).
   * @returns {HTMLElement}
   */
  _crearElementoDado(valor, lados) {
    const dado = document.createElement('div');
    dado.className = 'dado';

    const posiciones = POSICIONES_PUNTOS[valor];
    if (posiciones && lados <= 6) {
      // Mostrar puntos para dados d6 o menores
      posiciones.forEach(([px, py]) => {
        const punto = document.createElement('div');
        punto.className = 'punto';
        punto.style.left = `${px}%`;
        punto.style.top = `${py}%`;
        dado.appendChild(punto);
      });
    } else {
      // Mostrar numero para dados con mas de 6 lados
      dado.classList.add('dado-numero');
      dado.textContent = valor;
    }

    return dado;
  }
}

// ============================================================
// Vista: Resultados
// ============================================================
class VistaResultados {
  /**
   * @param {HTMLElement} elemTotal   - Elemento para mostrar el total.
   * @param {HTMLElement} elemDetalle - Elemento para mostrar el detalle.
   */
  constructor(elemTotal, elemDetalle) {
    this._elemTotal = elemTotal;
    this._elemDetalle = elemDetalle;
  }

  mostrar(tirada) {
    const resStr = tirada.resultados.join(', ');
    this._elemTotal.textContent = `Total: ${tirada.total}`;
    this._elemDetalle.textContent = `${tirada.cantidad}d${tirada.lados}  \u2192  [${resStr}]`;
  }

  limpiar() {
    this._elemTotal.textContent = 'Sin tirar';
    this._elemDetalle.textContent = '';
  }
}

// ============================================================
// Vista: Historico
// ============================================================
class VistaHistorico {
  /** @param {HTMLElement} contenedor */
  constructor(contenedor) {
    this._contenedor = contenedor;
  }

  actualizar(tiradas) {
    this._contenedor.innerHTML = '';

    if (tiradas.length === 0) {
      const p = document.createElement('p');
      p.className = 'historico-vacio';
      p.textContent = 'Aun no se han realizado tiradas.';
      this._contenedor.appendChild(p);
      return;
    }

    tiradas.forEach((tirada, indice) => {
      const hora = tirada.fecha
        ? tirada.fecha.toLocaleTimeString('es-ES')
        : '??:??:??';
      const div = document.createElement('div');
      div.className = 'entrada-historico';
      div.textContent = `[${hora}] #${String(indice + 1).padStart(3, '\u00a0')}  ${tirada}`;
      this._contenedor.prepend(div);
    });
  }
}

// ============================================================
// Aplicacion principal
// ============================================================
class Aplicacion {
  constructor() {
    this._lanzador = new Lanzador();

    // Elementos de la UI
    this._inputCantidad    = document.getElementById('cantidad');
    this._inputLados       = document.getElementById('lados');
    this._labelTipoDado    = document.getElementById('tipo-dado');
    this._panelAnimacion   = document.getElementById('panel-animacion');
    this._contenedorDados  = document.getElementById('contenedor-dados');
    this._textoTirando     = document.getElementById('texto-tirando');
    this._btnLanzar        = document.getElementById('btn-lanzar');

    // Sub-vistas
    this._animacion = new Animacion(this._contenedorDados, this._textoTirando);
    this._vistaResultados = new VistaResultados(
      document.getElementById('resultado-total'),
      document.getElementById('resultado-detalle')
    );
    this._vistaHistorico = new VistaHistorico(
      document.getElementById('lista-historico')
    );

    this._registrarEventos();
  }

  _registrarEventos() {
    this._btnLanzar.addEventListener('click', () => this._onLanzar());

    document.getElementById('btn-reset-historico')
      .addEventListener('click', () => this._onResetHistorico());

    document.getElementById('btn-reset-global')
      .addEventListener('click', () => this._onResetGlobal());

    document.getElementById('btn-cerrar')
      .addEventListener('click', () => this._onCerrar());

    this._inputCantidad.addEventListener('input', () => this._onCambioConfig());
    this._inputLados.addEventListener('input', () => this._onCambioConfig());
  }

  _onCambioConfig() {
    const cantidad = parseInt(this._inputCantidad.value, 10) || 1;
    const lados    = parseInt(this._inputLados.value, 10) || 6;
    this._labelTipoDado.textContent = `${cantidad}d${lados}`;
  }

  _onLanzar() {
    const cantidad = parseInt(this._inputCantidad.value, 10);
    const lados    = parseInt(this._inputLados.value, 10);

    if (!Number.isInteger(cantidad) || cantidad < 1) {
      alert('La cantidad minima de dados es 1.');
      return;
    }
    if (!Number.isInteger(lados) || lados < 2) {
      alert('El numero minimo de lados es 2.');
      return;
    }

    // Realizar el lanzamiento (calculo inmediato, animacion despues)
    const tirada = this._lanzador.lanzar(cantidad, lados);

    // Mostrar animacion
    this._btnLanzar.disabled = true;
    this._panelAnimacion.classList.remove('oculto');

    this._animacion.iniciar(cantidad, lados, () => {
      this._panelAnimacion.classList.add('oculto');
      this._btnLanzar.disabled = false;
      this._vistaResultados.mostrar(tirada);
      this._vistaHistorico.actualizar(this._lanzador.historico.entradas);
    });
  }

  _onResetHistorico() {
    this._lanzador.resetearHistorico();
    this._vistaResultados.limpiar();
    this._vistaHistorico.actualizar([]);
  }

  _onResetGlobal() {
    this._lanzador.resetearTodo();
    this._inputCantidad.value = 1;
    this._inputLados.value = 6;
    this._labelTipoDado.textContent = '1d6';
    this._vistaResultados.limpiar();
    this._vistaHistorico.actualizar([]);
  }

  _onCerrar() {
    // Intentar cerrar la pestana del navegador
    window.close();
    // Fallback: mostrar mensaje si window.close() no tuvo efecto
    setTimeout(() => {
      alert('Puedes cerrar esta pestana del navegador manualmente.');
    }, 300);
  }
}

// Iniciar la aplicacion cuando el DOM este listo
document.addEventListener('DOMContentLoaded', () => {
  new Aplicacion();
});
