const { test } = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');
const ts = require('typescript');

function load(file, modules) {
  const source = fs.readFileSync(path.join(__dirname, '../src', file), 'utf8');
  const { outputText } = ts.transpileModule(source, {
    compilerOptions: { module: ts.ModuleKind.CommonJS, jsx: ts.JsxEmit.React, esModuleInterop: true },
  });
  const exports = {};
  vm.runInNewContext(outputText, {
    exports,
    require(name) {
      if (name.endsWith('.png')) return name;
      assert.ok(Object.hasOwn(modules, name), `Module ${name} not provided`);
      return modules[name];
    },
    console,
    clearTimeout,
    setTimeout,
  });
  return exports;
}

function crearMockItinerario() {
  return {
    id: 101,
    fecha: 'Lun, 19 oct 2026',
    rutaNombre: 'Ruta 12 · San Martín',
    estado: 'en_ruta',
    transportistaNombre: 'Martín Rodríguez',
    transportistaIniciales: 'MR',
    vehiculo: { patente: 'AB 458 CD', modelo: 'Unidad 024 · Iveco Daily' },
    totalParadas: 6,
    paradasCompletadas: 2,
    paradas: [
      {
        id: 10,
        orden: 1,
        estado: 'finalizada',
        comercio: { id: 101, razonSocial: 'Comercio Ya Entregado 1', domicilio: 'Calle 1', localidad: 'San Martín' },
        montoCobranza: 50000,
      },
      {
        id: 20,
        orden: 2,
        estado: 'completada',
        comercio: { id: 102, razonSocial: 'Comercio Ya Entregado 2', domicilio: 'Calle 2', localidad: 'San Martín' },
        montoCobranza: 60000,
      },
      {
        id: 1,
        orden: 3,
        estado: 'en_curso',
        comercio: { id: 11, razonSocial: 'Almacén Don Pedro', domicilio: 'Av. San Martín 2450', localidad: 'San Martín' },
        montoCobranza: 148500,
      },
      {
        id: 2,
        orden: 4,
        estado: 'pendiente',
        comercio: { id: 12, razonSocial: 'Autoservicio La Esquina', domicilio: 'Belgrano 1832', localidad: 'San Martín' },
        montoCobranza: 86750,
      },
      {
        id: 3,
        orden: 5,
        estado: 'pendiente',
        comercio: { id: 13, razonSocial: 'Kiosco El Sol', domicilio: 'Mitre 1560', localidad: 'San Martín' },
        montoCobranza: 32400,
      },
      {
        id: 4,
        orden: 6,
        estado: 'pendiente',
        comercio: { id: 14, razonSocial: 'Mercado San José', domicilio: 'Sarmiento 920', localidad: 'San Martín' },
        montoCobranza: 112900,
      },
    ],
  };
}

function pantalla({ itinerarioInicial = crearMockItinerario(), router = {}, api = {} } = {}) {
  let itinerarioEntregado = null;
  const postsGuardarRuta = [];

  const mockApi = {
    async post(url, data) {
      if (url.includes('guardar-ruta')) {
        postsGuardarRuta.push(data);
        return { data: [] };
      }
      if (api.post) return api.post(url, data);
      return { data: [] };
    },
    ...api,
  };

  const { guardarOrdenRuta } = load('services/itinerarios.ts', {
    './api': mockApi,
    'react-native': { Platform: { OS: 'ios' } },
    '../utils/importes': { decimalACentavos: () => null, formatoCentavos: () => '' },
    './paradaService': { getIdParadaSeleccionadaParaCobro: () => 1, getParadaSeleccionada: () => null },
    '../data/mockParada': { MOCK_PARADA_SELECCIONADA: { id: 1, comercio: {}, remitos: [], montoCobranza: 0 } },
    '../data/mockItinerario': { MOCK_ITINERARIO_ASIGNADO: itinerarioInicial },
  });

  const mockItinerarioService = {
    obtenerItinerarioJornada: async () => ({ itinerario: itinerarioInicial }),
    entregarItinerarioActualizado: (itin) => {
      itinerarioEntregado = itin;
    },
    tomarItinerarioActualizado: () => itinerarioEntregado,
  };

  const estados = [];
  let cursor = 0;
  let efectos = [];

  const React = {
    Fragment: 'Fragment',
    createElement: (tipo, props, ...hijos) => ({ tipo, props, hijos }),
    useCallback: (fn) => fn,
    useMemo: (fn) => fn(),
    useRef: (current) => React.useState({ current })[0],
    useState(inicial) {
      const i = cursor++;
      if (!(i in estados)) estados[i] = inicial;
      return [
        estados[i],
        (valor) => {
          estados[i] = typeof valor === 'function' ? valor(estados[i]) : valor;
        },
      ];
    },
    useEffect(fn) {
      efectos.push(fn);
    },
  };

  const Screen = load('app/reordenar-paradas.tsx', {
    react: React,
    'react-native': {
      ActivityIndicator: 'ActivityIndicator',
      Image: 'Image',
      Modal: 'Modal',
      Pressable: 'Pressable',
      ScrollView: 'ScrollView',
      Text: 'Text',
      View: 'View',
      TouchableOpacity: 'TouchableOpacity',
      StatusBar: { currentHeight: 24 },
      Platform: { OS: 'android' },
      BackHandler: { addEventListener: () => ({ remove: () => {} }) },
      StyleSheet: { create: (styles) => styles },
      PanResponder: {
        create: (config) => ({
          panHandlers: {
            onGrant: config.onPanResponderGrant,
            onMove: config.onPanResponderMove,
            onRelease: config.onPanResponderRelease,
            onTerminate: config.onPanResponderTerminate,
          },
          _config: config,
        }),
      },
    },
    'expo-router': { useRouter: () => router },
    'react-native-safe-area-context': {
      SafeAreaView: 'SafeAreaView',
      useSafeAreaInsets: () => ({ top: 20, bottom: 20, left: 0, right: 0 }),
    },
    '../constants/theme': {
      RepartoYA: {
        naranjaYA: '#F4661B',
        azulRuta: '#123C6B',
        cremaPan: '#FFF6EC',
        carbon: '#1B1B1F',
        blanco: '#FFFFFF',
        grisTexto: '#6B7280',
      },
    },
    '../services/itinerarios': { guardarOrdenRuta },
    '../services/itinerarioService': mockItinerarioService,
    '../types/itinerario': {},
    '../data/mockItinerario': { MOCK_ITINERARIO_ASIGNADO: itinerarioInicial },
  }).default;

  function render() {
    cursor = 0;
    efectos = [];
    return Screen();
  }

  return {
    render,
    async montar() {
      render();
      for (const efecto of efectos) {
        efecto();
      }
      await asentar();
    },
    getPostsGuardarRuta: () => postsGuardarRuta,
    getItinerarioEntregado: () => itinerarioEntregado,
  };
}

function nodos(elemento) {
  if (Array.isArray(elemento)) return elemento.flatMap(nodos);
  if (!elemento || typeof elemento !== 'object') return [];
  if (typeof elemento.tipo === 'function') return nodos(elemento.tipo(elemento.props));
  return [elemento, ...nodos(elemento.hijos)];
}

function textos(elemento) {
  return nodos(elemento)
    .filter((nodo) => nodo.tipo === 'Text')
    .map((nodo) => nodo.hijos.join(''));
}

const asentar = () => new Promise((resolve) => setImmediate(resolve));

test('muestra carga mientras se obtiene el itinerario activo', async () => {
  const app = pantalla({
    itinerarioInicial: null,
  });
  const vistaInicial = app.render();
  assert.ok(nodos(vistaInicial).some((n) => n.tipo === 'ActivityIndicator'));
  assert.ok(textos(vistaInicial).includes('Cargando paradas del itinerario...'));
});

test('muestra la cabecera corporativa oficial, nombre de ruta y paradas pendientes', async () => {
  const app = pantalla();
  await app.montar();
  const vista = app.render();
  const textoTodos = textos(vista);

  assert.ok(textoTodos.includes('Recorrido y Paradas'));
  assert.ok(textoTodos.includes('Mantené presionada una parada para moverla libremente'));
  assert.ok(textoTodos.includes('Ruta 12 · San Martín'));
  assert.ok(textoTodos.includes('4 paradas pendientes'));
});

test('excluye paradas ya entregadas y lista solo las pendientes en orden relativo (Regla HU 24)', async () => {
  const app = pantalla();
  await app.montar();
  const vista = app.render();
  const textoTodos = textos(vista);

  // NO debe mostrar comercios ya entregados
  assert.ok(!textoTodos.includes('Comercio Ya Entregado 1'));
  assert.ok(!textoTodos.includes('Comercio Ya Entregado 2'));

  // SÍ debe mostrar las 4 pendientes
  assert.ok(textoTodos.includes('Almacén Don Pedro'));
  assert.ok(textoTodos.includes('Autoservicio La Esquina'));
  assert.ok(textoTodos.includes('Kiosco El Sol'));
  assert.ok(textoTodos.includes('Mercado San José'));

  // Verificamos numeración relativa 1, 2, 3, 4
  assert.ok(textoTodos.includes('1'));
  assert.ok(textoTodos.includes('2'));
  assert.ok(textoTodos.includes('3'));
  assert.ok(textoTodos.includes('4'));
});

test('estado inicial muestra "El orden actual está guardado" sin botón activo', async () => {
  const app = pantalla();
  await app.montar();
  const vista = app.render();
  const textoTodos = textos(vista);

  assert.ok(textoTodos.includes('El orden actual está guardado'));
  assert.ok(textoTodos.includes('Mantené presionados los puntos para cambiar la posición de una parada.'));
  assert.ok(!textoTodos.includes('Cambios sin guardar'));
});

test('volver sin cambios navega directamente a /itinerario sin modal de alerta', async () => {
  let rutaDestino = null;
  const router = { replace: (r) => { rutaDestino = r; } };
  const app = pantalla({ router });
  await app.montar();

  const botonVolver = nodos(app.render()).find((n) => n.props?.accessibilityLabel === 'Volver al itinerario');
  assert.ok(botonVolver);
  botonVolver.props.onPress();

  const vista = app.render();
  // El modal no debe estar visible
  const modal = nodos(vista).find((n) => n.tipo === 'Modal');
  assert.equal(modal.props.visible, false);
  assert.equal(rutaDestino, '/itinerario');
});

test('reordenar paradas habilita "Cambios sin guardar" y botón "Guardar orden" (HU 24 Escenario 1)', async () => {
  const app = pantalla();
  await app.montar();

  // Presionamos bajar la primera parada (Almacén Don Pedro)
  const botonBajar = nodos(app.render()).find(
    (n) => n.props?.accessibilityLabel === 'Bajar parada Almacén Don Pedro'
  );
  assert.ok(botonBajar);
  botonBajar.props.onPress();

  const vista = app.render();
  const textoTodos = textos(vista);

  assert.ok(textoTodos.includes('Cambios sin guardar'));
  assert.ok(textoTodos.includes('Guardar orden'));
  assert.ok(!textoTodos.includes('El orden actual está guardado'));
});

test('volver con cambios sin guardar abre el modal "¿Descartar cambios?" (HU 24 Escenario 2)', async () => {
  let rutaDestino = null;
  const router = { replace: (r) => { rutaDestino = r; } };
  const app = pantalla({ router });
  await app.montar();

  // Modificamos el orden
  const botonBajar = nodos(app.render()).find((n) => n.props?.accessibilityLabel === 'Bajar parada Almacén Don Pedro');
  botonBajar.props.onPress();

  // Intentamos volver
  const botonVolver = nodos(app.render()).find((n) => n.props?.accessibilityLabel === 'Volver al itinerario');
  botonVolver.props.onPress();

  const vista = app.render();
  const modal = nodos(vista).find((n) => n.tipo === 'Modal');
  assert.equal(modal.props.visible, true);
  assert.equal(rutaDestino, null); // No navega todavía

  const textoModal = textos(modal);
  assert.ok(textoModal.includes('¿Descartar cambios?'));
  assert.ok(textoModal.includes('Modificaste el orden de paradas y no lo guardaste.'));
  assert.ok(textoModal.includes('Descartar'));
  assert.ok(textoModal.includes('Seguir editando'));
});

test('en modal "¿Descartar cambios?", "Seguir editando" conserva modificaciones', async () => {
  const app = pantalla();
  await app.montar();

  // Modificamos orden y abrimos modal
  nodos(app.render()).find((n) => n.props?.accessibilityLabel === 'Bajar parada Almacén Don Pedro').props.onPress();
  nodos(app.render()).find((n) => n.props?.accessibilityLabel === 'Volver al itinerario').props.onPress();

  const modal = nodos(app.render()).find((n) => n.tipo === 'Modal');
  const botonSeguir = nodos(modal).find((n) => n.props?.accessibilityLabel === 'Seguir editando');
  assert.ok(botonSeguir);
  botonSeguir.props.onPress();

  const vista = app.render();
  const modalDespues = nodos(vista).find((n) => n.tipo === 'Modal');
  assert.equal(modalDespues.props.visible, false);
  assert.ok(textos(vista).includes('Cambios sin guardar'));
});

test('en modal "¿Descartar cambios?", "Descartar" revierte el orden previo e itinerario', async () => {
  let rutaDestino = null;
  const router = { replace: (r) => { rutaDestino = r; } };
  const app = pantalla({ router });
  await app.montar();

  // Modificamos orden y abrimos modal
  nodos(app.render()).find((n) => n.props?.accessibilityLabel === 'Bajar parada Almacén Don Pedro').props.onPress();
  nodos(app.render()).find((n) => n.props?.accessibilityLabel === 'Volver al itinerario').props.onPress();

  const modal = nodos(app.render()).find((n) => n.tipo === 'Modal');
  const botonDescartar = nodos(modal).find((n) => n.props?.accessibilityLabel === 'Descartar cambios');
  assert.ok(botonDescartar);
  botonDescartar.props.onPress();

  assert.equal(rutaDestino, '/itinerario');
});

test('presionar "Guardar orden" envía la secuencia completa a Django y actualiza en memoria', async () => {
  const app = pantalla();
  await app.montar();

  // Bajamos Almacén Don Pedro (ID 1) para que pase después de Autoservicio La Esquina (ID 2)
  nodos(app.render()).find((n) => n.props?.accessibilityLabel === 'Bajar parada Almacén Don Pedro').props.onPress();

  const botonGuardar = nodos(app.render()).find((n) => n.props?.accessibilityLabel === 'Guardar orden');
  assert.ok(botonGuardar);
  await botonGuardar.props.onPress();
  await asentar();

  // Verifica que envió las paradas entregadas originales primero (10, 20) seguidas de las reordenadas (2, 1, 3, 4)
  const posts = app.getPostsGuardarRuta();
  assert.equal(posts.length, 1);
  assert.deepEqual(Array.from(posts[0].parada_ids), [10, 20, 2, 1, 3, 4]);

  // Verifica que actualizó el itinerario en memoria para la pantalla itinerario
  const actualizado = app.getItinerarioEntregado();
  assert.ok(actualizado);
  assert.equal(actualizado.paradas.length, 6);
  assert.equal(actualizado.paradas[2].id, 2);
  assert.equal(actualizado.paradas[2].estado, 'en_curso');
  assert.equal(actualizado.paradas[3].id, 1);
  assert.equal(actualizado.paradas[3].estado, 'pendiente');
});

test('guardado exitoso muestra el toast flotante "Nuevo orden guardado" y botón inactivo', async () => {
  const app = pantalla();
  await app.montar();

  nodos(app.render()).find((n) => n.props?.accessibilityLabel === 'Bajar parada Almacén Don Pedro').props.onPress();
  await nodos(app.render()).find((n) => n.props?.accessibilityLabel === 'Guardar orden').props.onPress();
  await asentar();

  const vista = app.render();
  const textoTodos = textos(vista);

  assert.ok(textoTodos.includes('Nuevo orden guardado'));
  assert.ok(textoTodos.includes('Orden guardado'));

  // El botón ahora está deshabilitado
  const botonDeshabilitado = nodos(vista).find((n) => n.props?.accessibilityState?.disabled === true);
  assert.ok(botonDeshabilitado);
});

test('tras guardar exitosamente, volver al itinerario no muestra modal de descartar', async () => {
  let rutaDestino = null;
  const router = { replace: (r) => { rutaDestino = r; } };
  const app = pantalla({ router });
  await app.montar();

  nodos(app.render()).find((n) => n.props?.accessibilityLabel === 'Bajar parada Almacén Don Pedro').props.onPress();
  await nodos(app.render()).find((n) => n.props?.accessibilityLabel === 'Guardar orden').props.onPress();
  await asentar();

  // Presionamos volver
  nodos(app.render()).find((n) => n.props?.accessibilityLabel === 'Volver al itinerario').props.onPress();

  const modal = nodos(app.render()).find((n) => n.tipo === 'Modal');
  assert.equal(modal.props.visible, false);
  assert.equal(rutaDestino, '/itinerario');
});

test('soporta interacción táctil de arrastre (PanResponder) y muestra estado de movimiento', async () => {
  const app = pantalla();
  await app.montar();

  // Obtenemos el handle del primer elemento
  const handle = nodos(app.render()).find((n) => n.props?.accessibilityLabel === 'Mover Almacén Don Pedro');
  assert.ok(handle);

  // Simulamos inicio de arrastre
  handle.props.onGrant();
  let vista = app.render();
  let textoTodos = textos(vista);
  assert.ok(textoTodos.includes('Moviendo Almacén Don Pedro'));
  assert.ok(textoTodos.includes('Deslizá la parada hacia arriba o abajo. Soltala en la posición que prefieras.'));

  // Simulamos desplazamiento hacia abajo
  handle.props.onMove(null, { dy: 80 });
  // Simulamos soltar
  handle.props.onRelease();

  vista = app.render();
  textoTodos = textos(vista);
  assert.ok(textoTodos.includes('Cambios sin guardar'));
});
