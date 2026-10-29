const { test } = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs'), path = require('node:path'), vm = require('node:vm');
const ts = require('typescript');
function load(file, modules = {}, globals = {}) {
  const code = ts.transpileModule(fs.readFileSync(path.join(__dirname, '../src', file), 'utf8'), {
    compilerOptions: { module: ts.ModuleKind.CommonJS, target: ts.ScriptTarget.ES2020,
      jsx: ts.JsxEmit.React, esModuleInterop: true },
  }).outputText;
  const exports = {};
  vm.runInNewContext(code, { exports, Error, console, FormData, Blob, ...globals,
    require(name) {
      if (name in modules) return modules[name];
      if (name.endsWith('.png')) return name;
      throw new Error('Importación sin preparar: ' + name);
    },
  });
  return exports;
}
const money = load('utils/importes.ts');
class NativeForm { constructor() { this.parts = []; } append(...args) { this.parts.push(args); } }
function serviceHarness() {
  const h = { verifiedId: 42, calls: [], platform: { OS: 'web' },
    response: { mensaje: 'OK', evidencia: { id: 71, parada: 42, archivo: 'http://test/media/archivo.pdf', fecha: '2026-10-28' } } };
  h.selection = { getIdParadaSeleccionadaParaCobro: () => h.verifiedId };
  h.api = { async post(...args) {
    h.calls.push(args); if (h.failure) throw h.failure;
    if (h.pending) return h.pending;
    return { data: h.response };
  } };
  h.modules = { './api': h.api, 'react-native': { Platform: h.platform },
    '../utils/importes': money, './paradaService': h.selection,
    '../data/mockParada': {}, '../data/mockItinerario': {} };
  h.service = load('services/itinerarios.ts', h.modules);
  return h;
}
const pdf = () => new Blob(['%PDF-1.4 documento de prueba'], { type: 'application/pdf' });

test('el servicio bloquea IDs de mocks o de otra parada sin enviar HTTP', async () => {
  for (const verifiedId of [null, 99]) {
    const h = serviceHarness(); h.verifiedId = verifiedId;
    await assert.rejects(h.service.subirEvidenciaParada(42, 'blob:pdf', 'archivo.pdf', 'application/pdf', pdf()), /no está verificada/);
    assert.equal(h.calls.length, 0);
  }
  const h = serviceHarness();
  for (const id of [0, -1, NaN, 1.5, Number.MAX_SAFE_INTEGER + 1]) await assert.rejects(h.service.subirEvidenciaParada(id, 'blob:pdf'), /no está verificada/);
  assert.equal(h.calls.length, 0);
});

test('un ID positivo solo habilita la subida después de obtener la parada real de Django', async () => {
  const mock = { id: 42, orden: 3, comercio: { razonSocial: 'Mock' }, remitos: [] };
  const selection = load('services/paradaService.ts', {
    './authService': { API_BASE_URL: 'http://test', getAuthToken: () => 'token-prueba' },
    '../data/mockParada': { MOCK_PARADA_SELECCIONADA: mock },
    '../data/mockItinerario': { MOCK_ITINERARIO_ASIGNADO: { paradas: [] } },
  }, { AbortController, setTimeout, clearTimeout,
    fetch: async () => ({ ok: true, json: async () => ({ id: 42, orden: 3,
      monto_recaudar: '15400.50', estado: 'pendiente', comercio: { razon_social: 'Real' } }) }) });
  const h = serviceHarness(); h.modules['./paradaService'] = selection;
  const service = load('services/itinerarios.ts', h.modules);
  await assert.rejects(service.subirEvidenciaParada(42, 'blob:pdf', 'archivo.pdf', 'application/pdf', pdf()));
  assert.equal(h.calls.length, 0);
  await selection.obtenerDetalleParada(42);
  assert.equal((await service.subirEvidenciaParada(42, 'blob:pdf', 'archivo.pdf', 'application/pdf', pdf())).evidencia.id, 71);
  assert.equal(h.calls.length, 1);
});

test('la subida verificada conserva los bytes, el nombre y el tipo PDF en web', async () => {
  const h = serviceHarness();
  await h.service.subirEvidenciaParada(42, 'blob:pdf', 'archivo.pdf', 'application/pdf', pdf());
  const [url, form, config] = h.calls[0];
  assert.equal(url, 'paradas/42/subir-evidencia/');
  const file = form.get('archivo');
  assert.equal(file.name, 'archivo.pdf'); assert.equal(file.type, 'application/pdf');
  assert.equal(await file.text(), '%PDF-1.4 documento de prueba');
  assert.equal(config.headers['Content-Type'], undefined);
});

test('las fotos y los PDF nativos conservan la URI y el MIME al subir', async () => {
  const h = serviceHarness(); h.platform.OS = 'android';
  const service = load('services/itinerarios.ts', h.modules, { FormData: NativeForm });
  for (const [name, mime] of [['camara.jpg', 'image/jpeg'], ['imagen.png', 'image/png'], ['remito.pdf', 'application/pdf']]) {
    await service.subirEvidenciaParada(42, 'file:///' + name, name, mime);
    const parts = h.calls.at(-1)[1].parts;
    assert.equal(parts[0][0], 'archivo'); assert.equal(parts[0][1].type, mime);
    assert.equal(parts[0][1].uri, 'file:///' + name);
  }
});

test('fallos de red, rechazo HTTP y respuestas incompletas siguen sin simular éxito', async () => {
  for (const failure of [{ request: {}, code: 'ERR_NETWORK' }, { response: { status: 400, data: { archivo: ['Formato rechazado'] } } },
    { response: { status: 401 } }, { response: { status: 413 } }, { response: { status: 500 } }]) {
    const h = serviceHarness(); h.failure = failure;
    await assert.rejects(h.service.subirEvidenciaParada(42, 'blob:pdf', 'archivo.pdf', 'application/pdf', pdf()));
  }
  const h = serviceHarness(); h.response = { mensaje: 'OK' };
  await assert.rejects(h.service.subirEvidenciaParada(42, 'blob:pdf', 'archivo.pdf', 'application/pdf', pdf()), /no confirmó/);
});

function screenHarness(service = serviceHarness()) {
  const h = { service, states: [], refs: [], i: 0, r: 0, routes: [], alerts: [],
    stop: { id: 42, orden: 3, montoCobranza: 15400.50, comercio: { razonSocial: 'Comercio', domicilio: 'Calle 10' } } };
  const react = {
    createElement: (type, props, ...children) => ({ type, props: props || {}, children }),
    useState(initial) { const i = h.i++; if (!(i in h.states)) h.states[i] = initial;
      return [h.states[i], value => h.states[i] = typeof value === 'function' ? value(h.states[i]) : value]; },
    useRef(initial) { const i = h.r++; return h.refs[i] ?? (h.refs[i] = { current: initial }); },
  };
  const native = { StyleSheet: { create: s => s }, Platform: { OS: 'web' }, Alert: { alert: (...a) => h.alerts.push(a) } };
  for (const n of ['ActivityIndicator', 'Image', 'ScrollView', 'StatusBar', 'Text', 'TouchableOpacity', 'View']) native[n] = n;
  h.Component = load('screens/AdjuntarDocumento.tsx', {
    react, 'react-native': native, 'expo-router': { router: { replace: route => h.routes.push(route) } },
    'expo-image-picker': {}, 'expo-document-picker': {},
    '../services/paradaService': { getParadaSeleccionada: () => h.stop,
      getIdParadaSeleccionadaParaCobro: () => service.verifiedId },
    '../services/itinerarios': service.service,
  }).default;
  h.draw = () => { h.i = h.r = 0; return h.Component(); };
  h.draw(); h.file = { name: 'archivo.pdf', uri: 'blob:pdf', mimeType: 'application/pdf', webFile: pdf() };
  h.states[0] = h.file;
  h.button = () => find(h.draw(), n => n.props.accessibilityState && 'busy' in n.props.accessibilityState);
  return h;
}
function find(node, predicate) {
  if (!node || typeof node !== 'object') return;
  if (predicate(node)) return node;
  for (const c of (node.children || []).flat(Infinity)) { const result = find(c, predicate); if (result) return result; }
}

test('la pantalla conserva el archivo al bloquear una parada no verificada y permite reintentar', async () => {
  const service = serviceHarness(); service.verifiedId = null;
  const h = screenHarness(service); await h.button().props.onPress();
  assert.equal(h.states[0], h.file); assert.equal(h.states[1], false);
  assert.match(h.states[2], /no está verificada/); assert.equal(service.calls.length, 0); assert.equal(h.routes.length, 0);
  service.verifiedId = 42; await h.button().props.onPress();
  assert.equal(service.calls.length, 1); assert.equal(h.routes[0].params.paradaId, '42');
  assert.equal(h.routes[0].params.evidenciaId, '71');
});

test('una selección diferente bloquea el envío sin perder el documento', async () => {
  const service = serviceHarness(), h = screenHarness(service);
  service.verifiedId = 99;
  await h.button().props.onPress();
  assert.equal(service.calls.length, 0); assert.equal(h.states[0], h.file);
  assert.match(h.states[2], /cambió la selección/);
});

test('se conservan indicador, bloqueo de doble toque y reintento después de un error HTTP', async () => {
  const service = serviceHarness(); let reject;
  service.pending = new Promise((_, r) => reject = r);
  const h = screenHarness(service), button = h.button();
  const first = button.props.onPress(); await button.props.onPress();
  assert.equal(service.calls.length, 1); assert.equal(h.routes.length, 0);
  assert.equal(h.button().props.disabled, true); assert.ok(find(h.draw(), n => n.type === 'ActivityIndicator'));
  reject({ response: { status: 400, data: { archivo: ['Archivo rechazado'] } } }); await first;
  assert.equal(h.states[0], h.file); assert.match(h.states[2], /Archivo rechazado/); assert.equal(h.button().props.disabled, false);
  service.pending = null; await h.button().props.onPress();
  assert.equal(h.routes.length, 1); assert.equal(h.states[0], null);
});
