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

function pantalla(api) {
  const { getRutasGuardadas } = load('services/itinerarios.ts', {
    './api': api, 'react-native': {}, '../utils/importes': {}, './paradaService': {},
    '../data/mockParada': {}, '../data/mockItinerario': {},
  });
  const estados = [];
  let cursor = 0;
  let efecto;
  const React = {
    Fragment: 'Fragment',
    createElement: (tipo, props, ...hijos) => ({ tipo, props, hijos }),
    useCallback: (fn) => fn,
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
      ActivityIndicator: 'ActivityIndicator', Image: 'Image', Pressable: 'Pressable',
      ScrollView: 'ScrollView', Text: 'Text', View: 'View', StyleSheet: { create: (styles) => styles },
    },
    'expo-router': { useRouter: () => ({}), useFocusEffect: (fn) => { efecto = fn; } },
    'react-native-safe-area-context': { SafeAreaView: 'SafeAreaView' },
    '../constants/theme': { RepartoYA: {} },
    '../services/itinerarios': { getRutasGuardadas },
  }).default;

  function render() {
    cursor = 0;
    return Screen();
  }
  render();
  let limpiar = efecto();
  return {
    render,
    async reintentar() {
      const boton = nodos(render()).find((nodo) => nodo.props?.onPress && textos(nodo).includes('Reintentar'));
      assert.ok(boton);
      boton.props.onPress();
      limpiar();
      render();
      limpiar = efecto();
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
  assert.equal(nodos(vista).filter((nodo) => nodo.props?.disabled).length, 4);
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
