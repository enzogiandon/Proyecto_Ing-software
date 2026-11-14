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
      assert.ok(Object.hasOwn(modules, name), name);
      return modules[name];
    },
  });
  return exports;
}

function pantalla(api, itinerarioService = {}, router = {}) {
  const { eliminarRutaGuardada, getRutasGuardadas, ordenarPorRuta } = load('services/itinerarios.ts', {
    './api': api, 'react-native': {}, '../utils/importes': {}, './paradaService': {},
    '../data/mockParada': {}, '../data/mockItinerario': {},
  });
  const estados = [];
  let cursor = 0;
  let efectos = [];
  const React = {
    Fragment: 'Fragment',
    createElement: (tipo, props, ...hijos) => ({ tipo, props, hijos }),
    useCallback: (fn) => fn,
    useRef: (current) => React.useState({ current })[0],
    useState(inicial) {
      const i = cursor++;
      if (!(i in estados)) estados[i] = inicial;
      return [estados[i], (valor) => {
        estados[i] = typeof valor === 'function' ? valor(estados[i]) : valor;
      }];
    },
  };
  const Screen = load('app/recorridos-guardados.tsx', {
    react: React,
    'react-native': {
      ActivityIndicator: 'ActivityIndicator', Image: 'Image', Modal: 'Modal', Pressable: 'Pressable',
      ScrollView: 'ScrollView', Text: 'Text', View: 'View', StyleSheet: { create: (styles) => styles },
    },
    'expo-router': { useRouter: () => router, useFocusEffect: (fn) => { efectos.push(fn); } },
    'react-native-safe-area-context': { SafeAreaView: 'SafeAreaView' },
    '../constants/theme': { RepartoYA: {} },
    '../services/itinerarios': { eliminarRutaGuardada, getRutasGuardadas, ordenarPorRuta },
    '../services/itinerarioService': {
      obtenerItinerarioJornada: async () => ({ itinerario: null }),
      ...itinerarioService,
    },
  }).default;

  function render() {
    cursor = 0;
    efectos = [];
    return Screen();
  }
  render();
  let [limpiar] = efectos.map((efecto) => efecto());
  return {
    render,
    async reintentar() {
      const boton = nodos(render()).find((nodo) => nodo.props?.onPress && textos(nodo).includes('Reintentar'));
      assert.ok(boton);
      boton.props.onPress();
      limpiar();
      render();
      limpiar = efectos[0]();
      await asentar();
    },
  };
}

function nodos(elemento) {
  if (Array.isArray(elemento)) return elemento.flatMap(nodos);
  if (!elemento || typeof elemento !== 'object') return [];
  if (typeof elemento.tipo === 'function') return nodos(elemento.tipo(elemento.props));
  return [elemento, ...nodos(elemento.hijos)];
}

function textos(elemento) {
  return nodos(elemento).filter((nodo) => nodo.tipo === 'Text').map((nodo) => nodo.hijos.join(''));
}

const asentar = () => new Promise((resolve) => setImmediate(resolve));

test('muestra carga mientras Django responde', async () => {
  let resolver;
  const app = pantalla({ get: () => new Promise((resolve) => { resolver = resolve; }) });
  assert.ok(nodos(app.render()).some((nodo) => nodo.tipo === 'ActivityIndicator'));
  assert.ok(!textos(app.render()).includes('No hay recorridos guardados'));
  resolver({ data: [] });
  await asentar();
  assert.ok(!nodos(app.render()).some((nodo) => nodo.tipo === 'ActivityIndicator'));
});

test('muestra los nombres de Django y calcula el contador sin metadatos', async () => {
  const llamadas = [];
  const app = pantalla({ async get(url) {
    llamadas.push(url);
    return { data: [{ id: 1, nombre: 'Centro' }, { id: 2, nombre: 'Norte' }] };
  } });
  await asentar();
  assert.deepEqual(llamadas, ['itinerarios/rutas-guardadas/']);
  const vista = app.render();
  for (const texto of ['2 recorridos guardados', 'Centro', 'Norte', 'Cargar', 'Eliminar recorrido']) {
    assert.ok(textos(vista).includes(texto));
  }
  assert.equal(nodos(vista).filter((nodo) => nodo.props?.disabled).length, 2);
});

test('muestra estado vacío y el acceso previsto a HU 26', async () => {
  const app = pantalla({ async get() { return { data: [] }; } });
  await asentar();
  const contenido = textos(app.render());
  for (const texto of ['0 recorridos guardados', 'No hay recorridos guardados', '+ Guardar orden actual']) {
    assert.ok(contenido.includes(texto));
  }
});

test('muestra error de conexión sin inventar datos y permite reintentar', async () => {
  let intentos = 0;
  const app = pantalla({ async get() {
    if (++intentos === 1) throw new Error('Sin conexión');
    return { data: [{ id: 7, nombre: 'Sur' }] };
  } });
  await asentar();
  assert.ok(textos(app.render()).includes('No se pudieron cargar los recorridos'));
  assert.ok(!textos(app.render()).includes('No hay recorridos guardados'));
  await app.reintentar();
  assert.equal(intentos, 2);
  assert.ok(textos(app.render()).includes('1 recorrido guardado'));
  assert.ok(textos(app.render()).includes('Sur'));
});

test('trata una respuesta inválida como error', async () => {
  const app = pantalla({ async get() { return { data: [{ id: 4 }] }; } });
  await asentar();
  assert.ok(textos(app.render()).includes('No se pudieron cargar los recorridos'));
});

function boton(app, texto) {
  const encontrado = nodos(app.render()).find((nodo) =>
    nodo.tipo === 'Pressable' && (nodo.props?.accessibilityLabel === texto || textos(nodo).includes(texto)));
  assert.ok(encontrado, texto);
  return encontrado.props;
}

async function cargaPreparada() {
  const escenario = { posts: [], consultas: 0, actualizaciones: [], atras: 0 };
  const actualizado = { paradas: [{ id: 31 }, { id: 12 }] };
  const app = pantalla({
    async get() { return { data: [{ id: 17, nombre: 'Norte' }] }; },
    async post(url, body) {
      escenario.posts.push([url, body.ruta_id]);
      return escenario.enviar ? escenario.enviar() : { data: [31, 12] };
    },
  }, {
    async obtenerItinerarioJornada(opciones) {
      assert.equal(opciones.soloDjango, true);
      if (++escenario.consultas === 1) return { itinerario: { paradas: [{ id: 12 }, { id: 31 }] } };
      return escenario.consultar ? escenario.consultar() : { itinerario: actualizado };
    },
    entregarItinerarioActualizado: (valor) => escenario.actualizaciones.push(valor),
  }, {
    canGoBack: () => true,
    back: () => { escenario.atras++; },
  });
  await asentar();
  boton(app, 'Cargar Norte').onPress();
  return { app, escenario, actualizado };
}

test('el modal advierte del reemplazo y cancelar conserva el itinerario', async () => {
  const { app, escenario } = await cargaPreparada();
  assert.ok(nodos(app.render()).some((nodo) => nodo.tipo === 'Modal'));
  assert.ok(textos(app.render()).some((texto) => texto.includes('Se reemplazará el orden actual')));
  boton(app, 'Cancelar').onPress();
  assert.ok(!nodos(app.render()).some((nodo) => nodo.tipo === 'Modal'));
  assert.deepEqual(escenario.posts, []);
  assert.deepEqual(escenario.actualizaciones, []);
});

test('confirma una sola vez, actualiza las paradas y vuelve al itinerario', async () => {
  const { app, escenario, actualizado } = await cargaPreparada();
  let resolver;
  escenario.enviar = () => new Promise((resolve) => { resolver = resolve; });
  const confirmar = boton(app, 'Cargar recorrido Norte').onPress;
  confirmar();
  confirmar();
  assert.ok(textos(app.render()).includes('Cargando recorrido…'));
  assert.ok(!textos(app.render()).includes('Recorrido Norte cargado'));
  resolver({ data: [31, 12] });
  await asentar();
  assert.deepEqual(escenario.posts, [['itinerarios/ordenar-por-ruta/', 17]]);
  assert.deepEqual(escenario.actualizaciones, [actualizado]);
  assert.ok(textos(app.render()).includes('Recorrido Norte cargado'));
  boton(app, 'Ver itinerario').onPress();
  assert.equal(escenario.atras, 1);
});

test('un POST fallido o inválido permite reintentar sin mostrar éxito prematuro', async () => {
  const { app, escenario } = await cargaPreparada();
  escenario.enviar = () => { throw new Error('Sin conexión'); };
  await boton(app, 'Cargar recorrido Norte').onPress();
  assert.equal(escenario.consultas, 1);
  escenario.enviar = () => ({ data: [31, 31] });
  await boton(app, 'Reintentar carga').onPress();
  assert.equal(escenario.consultas, 1);
  assert.ok(!textos(app.render()).includes('Recorrido Norte cargado'));
  escenario.enviar = undefined;
  await boton(app, 'Reintentar carga').onPress();
  assert.ok(textos(app.render()).includes('Recorrido Norte cargado'));
});

test('si falla la actualización visual, reconsulta sin repetir el POST', async () => {
  const { app, escenario, actualizado } = await cargaPreparada();
  escenario.consultar = () => ({ itinerario: { paradas: [{ id: 12 }, { id: 31 }] } });
  await boton(app, 'Cargar recorrido Norte').onPress();
  assert.deepEqual(escenario.actualizaciones, []);
  assert.ok(textos(app.render()).some((texto) => texto.includes('Django confirmó la carga')));
  escenario.consultar = undefined;
  await boton(app, 'Reconsultar itinerario').onPress();
  assert.equal(escenario.posts.length, 1);
  assert.deepEqual(escenario.actualizaciones, [actualizado]);
});

test('si la reconsulta sigue fallando, permite cerrar y deja visible el aviso sin repetir el POST', async () => {
  const { app, escenario } = await cargaPreparada();
  escenario.consultar = () => { throw new Error('Sin conexión'); };
  await boton(app, 'Cargar recorrido Norte').onPress();
  await boton(app, 'Reconsultar itinerario').onPress();
  assert.equal(escenario.consultas, 3);
  boton(app, 'Cerrar').onPress();
  assert.ok(!nodos(app.render()).some((nodo) => nodo.tipo === 'Modal'));
  assert.ok(textos(app.render()).includes(
    'Django aplicó el recorrido Norte, pero la pantalla de Itinerario no pudo actualizarse.',
  ));
  assert.equal(escenario.posts.length, 1);
  assert.deepEqual(escenario.actualizaciones, []);
});

test('sin itinerario asignado, la carga queda deshabilitada y se explica el motivo', async () => {
  const app = pantalla({ async get() { return { data: [{ id: 17, nombre: 'Norte' }] }; } });
  await asentar();
  assert.equal(boton(app, 'Cargar Norte').disabled, true);
  assert.ok(textos(app.render()).includes('Necesitás un itinerario asignado para cargar un recorrido.'));
});

async function eliminacionPreparada(recorridos = [{ id: 17, nombre: 'Norte' }]) {
  const escenario = { posts: [], consultasItinerario: 0, actualizaciones: [] };
  const app = pantalla({
    async get() { return escenario.listar ? escenario.listar() : { data: recorridos }; },
    async post(url, body) {
      escenario.posts.push([url, body.ruta_id, Object.keys(body)]);
      return escenario.enviar ? escenario.enviar() : { data: { id: 17, mensaje: 'Ruta eliminada' } };
    },
  }, {
    async obtenerItinerarioJornada() {
      escenario.consultasItinerario++;
      return { itinerario: null };
    },
    entregarItinerarioActualizado: (valor) => escenario.actualizaciones.push(valor),
  });
  await asentar();
  boton(app, 'Eliminar recorrido Norte').onPress();
  return { app, escenario };
}

test('el modal identifica el recorrido y cancelar conserva la lista sin enviar un POST', async () => {
  const { app, escenario } = await eliminacionPreparada();
  const modal = nodos(app.render()).find((nodo) => nodo.tipo === 'Modal');
  assert.ok(textos(modal).includes('Norte'));
  assert.ok(textos(modal).includes('¿Estás seguro de que querés eliminar este recorrido?'));
  boton(app, 'Cancelar').onPress();
  assert.ok(!nodos(app.render()).some((nodo) => nodo.tipo === 'Modal'));
  assert.deepEqual(escenario.posts, []);
  assert.ok(textos(app.render()).includes('1 recorrido guardado'));
});

test('espera la confirmación, bloquea duplicados y quita solo el recorrido elegido', async () => {
  const { app, escenario } = await eliminacionPreparada([{ id: 17, nombre: 'Norte' }, { id: 21, nombre: 'Sur' }]);
  let resolver;
  escenario.enviar = () => new Promise((resolve) => { resolver = resolve; });
  const confirmar = boton(app, 'Confirmar eliminación del recorrido').onPress;
  const primera = confirmar();
  await confirmar();
  assert.deepEqual(escenario.posts, [['itinerarios/eliminar-ruta/', 17, ['ruta_id']]]);
  assert.ok(textos(app.render()).includes('Eliminando recorrido…'));
  assert.ok(textos(app.render()).includes('2 recorridos guardados'));
  assert.ok(!textos(app.render()).includes('Recorrido eliminado'));
  resolver({ data: { id: 17, mensaje: 'Ruta eliminada' } });
  await primera;
  assert.ok(textos(app.render()).includes('Recorrido eliminado'));
  boton(app, 'Aceptar').onPress();
  assert.ok(textos(app.render()).includes('1 recorrido guardado'));
  assert.ok(textos(app.render()).includes('Sur'));
  assert.ok(!textos(app.render()).includes('Norte'));
  assert.equal(escenario.consultasItinerario, 1);
  assert.deepEqual(escenario.actualizaciones, []);
});

test('conserva el recorrido si falla Django o devuelve otro ID y permite reintentar', async () => {
  const { app, escenario } = await eliminacionPreparada();
  escenario.enviar = () => { throw new Error('Sin conexión'); };
  await boton(app, 'Confirmar eliminación del recorrido').onPress();
  assert.ok(textos(app.render()).some((texto) => texto.includes('No se pudo confirmar la eliminación')));
  escenario.enviar = () => ({ data: { id: 25, mensaje: 'Ruta eliminada' } });
  await boton(app, 'Reintentar eliminación').onPress();
  assert.ok(textos(app.render()).includes('1 recorrido guardado'));
  assert.ok(!textos(app.render()).includes('Recorrido eliminado'));
  escenario.enviar = undefined;
  await boton(app, 'Reintentar eliminación').onPress();
  assert.equal(escenario.posts.length, 3);
  assert.ok(textos(app.render()).includes('Recorrido eliminado'));
});

test('al eliminar el último recorrido vuelve al estado vacío de la HU 63', async () => {
  const { app } = await eliminacionPreparada();
  await boton(app, 'Confirmar eliminación del recorrido').onPress();
  boton(app, 'Aceptar').onPress();
  for (const texto of ['0 recorridos guardados', 'No hay recorridos guardados', '+ Guardar orden actual']) {
    assert.ok(textos(app.render()).includes(texto));
  }
});

test('actualizar el listado refleja si el recorrido sigue guardado sin confirmar la eliminación ni repetir el POST', async () => {
  for (const sigueGuardado of [true, false]) {
    const { app, escenario } = await eliminacionPreparada();
    escenario.enviar = () => { throw new Error('Respuesta perdida'); };
    await boton(app, 'Confirmar eliminación del recorrido').onPress();
    escenario.listar = () => ({ data: sigueGuardado ? [{ id: 17, nombre: 'Norte' }] : [] });
    await boton(app, 'Actualizar listado').onPress();
    const contenido = textos(app.render());
    assert.equal(contenido.includes('Norte'), sigueGuardado);
    assert.equal(contenido.includes('No hay recorridos guardados'), !sigueGuardado);
    assert.ok(!contenido.includes('Recorrido eliminado'));
    assert.equal(escenario.posts.length, 1);
  }
});

test('si actualizar el listado sigue fallando, cancelar conserva la tarjeta sin repetir el POST', async () => {
  const { app, escenario } = await eliminacionPreparada();
  escenario.enviar = () => { throw new Error('Respuesta perdida'); };
  await boton(app, 'Confirmar eliminación del recorrido').onPress();
  let consultas = 0;
  escenario.listar = () => { consultas++; throw new Error('Sin conexión'); };
  await boton(app, 'Actualizar listado').onPress();
  await boton(app, 'Actualizar listado').onPress();
  assert.equal(consultas, 2);
  assert.ok(textos(app.render()).some((texto) => texto.includes('sigue sin verificarse')));
  boton(app, 'Cancelar').onPress();
  assert.ok(!nodos(app.render()).some((nodo) => nodo.tipo === 'Modal'));
  assert.ok(textos(app.render()).includes('1 recorrido guardado'));
  assert.equal(escenario.posts.length, 1);
});
