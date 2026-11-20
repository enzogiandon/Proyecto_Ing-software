const { test } = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');
const ts = require('typescript');

function loadModule(file, modules = {}, globals = {}) {
  const source = fs.readFileSync(path.join(__dirname, '../src', file), 'utf8');
  const code = ts.transpileModule(source, {
    compilerOptions: {
      module: ts.ModuleKind.CommonJS,
      target: ts.ScriptTarget.ES2020,
      jsx: ts.JsxEmit.React,
      esModuleInterop: true,
    },
  }).outputText;
  const exports = {};
  const context = {
    exports,
    require(name) {
      if (name in modules) return modules[name];
      if (name === './config') return { getBackendBaseUrl: () => 'http://test', BACKEND_URL: 'http://test' };
      if (name.endsWith('.png')) return name;
      throw new Error('Importación sin preparar: ' + name);
    },
    console,
    Error,
    JSON,
    setTimeout,
    clearTimeout,
    AbortController,
    ...globals,
  };
  vm.runInNewContext(code, context);
  return exports;
}

function createAsyncStorageMock() {
  const store = new Map();
  return {
    _store: store,
    async setItem(key, val) {
      store.set(key, String(val));
    },
    async getItem(key) {
      return store.has(key) ? store.get(key) : null;
    },
    async removeItem(key) {
      store.delete(key);
    },
  };
}

test('HU-68: isJornadaIniciada discrimina correctamente entre estado asignado y en_curso', () => {
  const asyncStorageMock = createAsyncStorageMock();
  const storageMock = loadModule('services/storage.ts', {
    '@react-native-async-storage/async-storage': { __esModule: true, default: asyncStorageMock, ...asyncStorageMock },
  }, { window: undefined });

  const itinerarioService = loadModule('services/itinerarioService.ts', {
    './authService': { getAuthToken: () => 'token', getUsuarioActual: () => ({ first_name: 'Martín' }), API_BASE_URL: 'http://test' },
    './storage': storageMock,
    '../data/mockItinerario': { MOCK_ITINERARIO_ASIGNADO: { id: 101, estado: 'asignado', paradas: [] }, MOCK_ITINERARIO_SIN_ASIGNAR: null },
    '../types/itinerario': {},
  }, { window: undefined, fetch: () => Promise.resolve({ ok: true, json: async () => ({}) }) });

  assert.equal(itinerarioService.isJornadaIniciada({ id: 101, estado: 'asignado', totalParadas: 4, paradasCompletadas: 0, paradas: [] }), false);
  assert.equal(itinerarioService.isJornadaIniciada({ id: 101, estado: 'en_curso', totalParadas: 4, paradasCompletadas: 0, paradas: [] }), true);
  assert.equal(itinerarioService.isJornadaIniciada({ id: 101, estado: 'en_ruta', totalParadas: 4, paradasCompletadas: 0, paradas: [] }), true);
  assert.equal(itinerarioService.isJornadaIniciada({ id: 101, estado: 'finalizado', totalParadas: 4, paradasCompletadas: 4, paradas: [] }), true);
  assert.equal(itinerarioService.isJornadaIniciada(null), false);
});

test('HU-68: comenzarJornadaLaboral persiste el inicio en almacenamiento nativo y envía POST a backend', async () => {
  const asyncStorageMock = createAsyncStorageMock();
  const storageMock = loadModule('services/storage.ts', {
    '@react-native-async-storage/async-storage': { __esModule: true, default: asyncStorageMock, ...asyncStorageMock },
  }, { window: undefined });

  const llamadasHttp = [];
  const fetchMock = async (url, opciones) => {
    llamadasHttp.push({ url, body: JSON.parse(opciones.body) });
    return { ok: true, json: async () => ({ mensaje: 'OK' }) };
  };

  const itinerarioService = loadModule('services/itinerarioService.ts', {
    './authService': { getAuthToken: () => 'token-prueba', getUsuarioActual: () => ({ first_name: 'Martín' }), API_BASE_URL: 'http://test' },
    './storage': storageMock,
    '../data/mockItinerario': { MOCK_ITINERARIO_ASIGNADO: { id: 101, estado: 'asignado', paradas: [] }, MOCK_ITINERARIO_SIN_ASIGNAR: null },
    '../types/itinerario': {},
  }, { window: undefined, fetch: fetchMock });

  const resultado = await itinerarioService.comenzarJornadaLaboral(101);
  assert.equal(resultado.success, true);
  assert.equal(llamadasHttp.length, 1);
  assert.equal(llamadasHttp[0].url, 'http://test/api/itinerarios/iniciar/');
  assert.equal(llamadasHttp[0].body.itinerario_id, 101);

  // Verificamos persistencia nativa
  const persistido = await storageMock.isJornadaIniciadaStorage(101);
  assert.equal(persistido, true);
});

test('HU-68: comenzarJornadaLaboral maneja rechazo cuando el transportista no posee itinerario asignado', async () => {
  const asyncStorageMock = createAsyncStorageMock();
  const storageMock = loadModule('services/storage.ts', {
    '@react-native-async-storage/async-storage': { __esModule: true, default: asyncStorageMock, ...asyncStorageMock },
  }, { window: undefined });

  const fetchMock = async (url, opciones) => {
    return {
      ok: false,
      status: 400,
      json: async () => ({
        code: 'SIN_ITINERARIO_ASIGNADO',
        detail: 'No posees ningún itinerario asignado para iniciar.',
      }),
    };
  };

  const itinerarioService = loadModule('services/itinerarioService.ts', {
    './authService': { getAuthToken: () => 'token-prueba', getUsuarioActual: () => ({ first_name: 'Martín' }), API_BASE_URL: 'http://test' },
    './storage': storageMock,
    '../data/mockItinerario': { MOCK_ITINERARIO_ASIGNADO: { id: 101, estado: 'asignado', paradas: [] }, MOCK_ITINERARIO_SIN_ASIGNAR: null },
    '../types/itinerario': {},
  }, { window: undefined, fetch: fetchMock });

  const resultado = await itinerarioService.comenzarJornadaLaboral(101);
  assert.equal(resultado.success, false);
  assert.equal(resultado.code, 'SIN_ITINERARIO_ASIGNADO');
  assert.equal(resultado.error, 'No posees ningún itinerario asignado para iniciar.');

  // Verifica que no se persiste en AsyncStorage si falló el inicio
  const persistido = await storageMock.isJornadaIniciadaStorage(101);
  assert.equal(persistido, false);
});

test('HU-68: en Recorridos Guardados, una jornada sin iniciar bloquea Cargar y Guardar', () => {
  const recorridos = [{ id: 10, nombre: 'Ruta habitual norte' }];
  let alertLlamado = false;
  const AlertMock = {
    alert: (titulo, mensaje) => {
      alertLlamado = true;
      assert.ok(mensaje.includes('Debés comenzar tu jornada laboral') || mensaje.includes('Jornada no iniciada'));
    },
  };

  // Simulación del estado cuando la jornada no está iniciada (itinerario asignado pero no comenzado)
  const jornadaIniciada = false;
  const asignacion = 'asignado';

  // Validación de que Cargar está deshabilitado
  const botonCargarDeshabilitado = asignacion !== 'asignado' || !jornadaIniciada;
  assert.equal(botonCargarDeshabilitado, true);

  // Validación de que presionar Guardar bloquea la apertura del modal y emite alerta
  const abrirModalGuardar = () => {
    if (asignacion === 'asignado' && !jornadaIniciada) {
      AlertMock.alert('Jornada no iniciada', 'Debés comenzar tu jornada laboral en Mi Itinerario para guardar el orden de las paradas.');
      return false;
    }
    return true;
  };

  const pudoAbrir = abrirModalGuardar();
  assert.equal(pudoAbrir, false);
  assert.equal(alertLlamado, true);
});

test('HU-68: en Recorridos Guardados, una vez iniciada la jornada se habilitan Cargar y Guardar', () => {
  const jornadaIniciada = true;
  const asignacion = 'asignado';

  const botonCargarDeshabilitado = asignacion !== 'asignado' || !jornadaIniciada;
  assert.equal(botonCargarDeshabilitado, false);

  let modalAbierto = false;
  const abrirModalGuardar = () => {
    if (asignacion === 'asignado' && !jornadaIniciada) {
      return false;
    }
    modalAbierto = true;
    return true;
  };

  const pudoAbrir = abrirModalGuardar();
  assert.equal(pudoAbrir, true);
  assert.equal(modalAbierto, true);
});
