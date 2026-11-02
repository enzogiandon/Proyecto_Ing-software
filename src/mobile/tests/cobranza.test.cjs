const { test } = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');
const ts = require('typescript');

// Ejecuta los módulos reales con HTTP y componentes nativos controlados.
// No requiere Django ni instala dependencias.
function load(file, modules = {}, globals = {}) {
  const source = fs.readFileSync(path.join(__dirname, '../src', file), 'utf8');
  const code = ts.transpileModule(source, {
    compilerOptions: { module: ts.ModuleKind.CommonJS, target: ts.ScriptTarget.ES2020,
      jsx: ts.JsxEmit.React, esModuleInterop: true },
  }).outputText;
  const exports = {};
  vm.runInNewContext(code, { exports, require(name) {
    if (name in modules) return modules[name];
    if (name.endsWith('.png')) return name;
    throw new Error('Importación sin preparar: ' + name);
  }, Error, console, FormData, Blob, ...globals });
  return exports;
}
const money = load('utils/importes.ts');
const tick = () => new Promise(setImmediate);

function serviceHarness() {
  const h = { selectedId: 42, posts: [], gets: [],
    parada: { id: 42, orden: 3, monto_recaudar: '15400.50', estado: 'pendiente',
      comercio: { razon_social: 'Comercio real', domicilio: 'Calle 10' } },
    response: { mensaje: 'OK', cobranza_id: 71, pagos_registrados: 2,
      parada_estado: 'finalizada', itinerario_finalizado: false } };
  h.api = {
    async get(url) { h.gets.push(url); if (h.getError) throw h.getError; return { data: h.parada }; },
    async post(url, data) {
      h.posts.push({ url, data });
      if (h.postError) throw h.postError;
      if (h.pending) return h.pending;
      return { data: h.response };
    },
  };
  h.service = load('services/itinerarios.ts', {
    './api': h.api,
    'react-native': { Platform: { OS: 'web' } },
    '../utils/importes': money,
    './paradaService': { getIdParadaSeleccionadaParaCobro: () => h.selectedId },
    '../data/mockParada': {}, '../data/mockItinerario': {},
  });
  return h;
}
const pagos = [{ medio: 'efectivo', monto: 10000 }, { medio: 'efectivo', monto: 5400.50 }];

function reactHarness() {
  const h = { states: [], refs: [], cursor: 0, refCursor: 0, alerts: [], effects: [], focused: false };
  h.react = {
    createElement: (type, props, ...children) => ({ type, props: props || {}, children }),
    useState(initial) {
      const i = h.cursor++;
      if (!(i in h.states)) h.states[i] = initial;
      return [h.states[i], value => { h.states[i] = typeof value === 'function' ? value(h.states[i]) : value; }];
    },
    useRef(initial) { const i = h.refCursor++; return h.refs[i] ?? (h.refs[i] = { current: initial }); },
    useCallback: fn => fn,
  };
  h.native = { StyleSheet: { create: s => s }, Alert: { alert: (...args) => h.alerts.push(args) } };
  for (const n of ['ActivityIndicator', 'Image', 'Modal', 'ScrollView', 'StatusBar', 'Text', 'TextInput', 'TouchableOpacity', 'View']) h.native[n] = n;
  h.render = (Component, props) => { h.cursor = h.refCursor = 0; return Component(props); };
  return h;
}
function find(node, predicate) {
  if (!node || typeof node !== 'object') return;
  if (predicate(node)) return node;
  for (const child of (node.children || []).flat(Infinity)) { const result = find(child, predicate); if (result) return result; }
}
const confirmButton = tree => find(tree, n => n.props.accessibilityState);

function screenHarness(props = {}) {
  const h = reactHarness();
  h.Component = load('screens/ValidarCobro.tsx', { react: h.react, 'react-native': h.native, '../utils/importes': money }).default;
  h.props = { montoTotalCentavos: 1540050, onConfirmar: async () => {}, ...props };
  h.draw = () => h.render(h.Component, h.props);
  h.add = (text, medio = 'efectivo') => {
    h.draw(); h.states[2] = medio; h.states[3] = text;
    const tree = h.draw();
    find(tree, n => n.type === 'TouchableOpacity' && n.children.some(c => c?.children?.includes('Guardar pago'))).props.onPress();
  };
  return h;
}

test('interpreta centavos, miles argentinos y rechaza entradas inválidas', () => {
  for (const value of ['15400.50', '15400,50', '15.400,50']) assert.equal(money.interpretarImporte(value), 1540050);
  assert.equal(money.interpretarImporte('0,01'), 1);
  assert.equal(money.interpretarImporte('15.400'), 1540000);
  for (const value of ['-100', 'abc100', '1,234', '12.34,50', '1.2.3', 'Infinity', '']) assert.equal(money.interpretarImporte(value), null);
  assert.equal(money.decimalACentavos('15400.50'), 1540050);
  assert.equal(money.decimalACentavos(15400.5), 1540050);
  assert.equal(money.decimalACentavos('15.400,50'), null);
});

test('0,10 + 0,20 coincide con 0,30 y admite varios pagos del mismo medio', () => {
  const h = screenHarness({ montoTotalCentavos: 30 });
  h.add('0,10'); h.add('0.20');
  assert.equal(h.states[0].length, 2);
  assert.equal(h.states[0][0].medio, h.states[0][1].medio);
  assert.equal(h.states[0].reduce((n, m) => n + m.montoCentavos, 0), 30);
  assert.equal(confirmButton(h.draw()).props.disabled, false);
});

test('no confirma sumas insuficientes/excedidas ni un importe de parada ausente', () => {
  const h = screenHarness(); h.add('15400,49');
  assert.equal(confirmButton(h.draw()).props.disabled, true);
  h.add('0,02'); assert.equal(confirmButton(h.draw()).props.disabled, true);
  h.props.montoTotalCentavos = undefined; assert.equal(confirmButton(h.draw()).props.disabled, true);
});

test('espera Django, bloquea doble toque, conserva movimientos y permite reintentar', async () => {
  let resolve, reject, calls = 0;
  const h = screenHarness({ onConfirmar: () => { calls++; return new Promise((a, b) => { resolve = a; reject = b; }); } });
  h.add('10000'); h.add('5.400,50');
  const button = confirmButton(h.draw()); const request = button.props.onPress();
  await button.props.onPress(); assert.equal(calls, 1); assert.equal(h.states[4], false);
  assert.equal(confirmButton(h.draw()).props.disabled, true);
  assert.ok(find(h.draw(), n => n.type === 'ActivityIndicator'));
  reject(new Error('Django rechazó el cobro')); await request;
  assert.equal(h.states[0].length, 2); assert.equal(h.states[4], false);
  assert.match(h.states[6], /rechazó/); assert.equal(confirmButton(h.draw()).props.disabled, false);
  const retry = confirmButton(h.draw()).props.onPress(); resolve(); await retry;
  assert.equal(calls, 2); assert.equal(h.states[4], true); assert.equal(confirmButton(h.draw()).props.disabled, true);
});

test('consulta Django y envía todos los pagos con centavos, sin agruparlos', async () => {
  const h = serviceHarness();
  const result = await h.service.registrarCobranza(42, pagos);
  assert.equal(result.cobranza_id, 71);
  assert.equal(h.gets[0], 'paradas/42/');
  assert.equal(h.posts[0].url, 'paradas/42/registrar-cobranza/');
  assert.equal(h.posts[0].data.length, 2);
  assert.equal(h.posts[0].data[1].monto, 5400.5);
});

test('bloquea parada simulada, ID distinto, importe ausente, pagos inválidos y parada finalizada', async () => {
  const scenarios = [h => h.selectedId = null, h => h.parada.id = 99,
    h => delete h.parada.monto_recaudar, h => h.parada.monto_recaudar = 'inválido',
    h => h.parada.estado = 'finalizada'];
  for (const setup of scenarios) {
    const h = serviceHarness(); setup(h);
    await assert.rejects(h.service.registrarCobranza(42, pagos)); assert.equal(h.posts.length, 0);
  }
  const h = serviceHarness();
  await assert.rejects(h.service.registrarCobranza(42, [{ medio: 'efectivo', monto: -1 }]));
  assert.equal(h.posts.length, 0);
});

test('acepta importe numérico del backend y detecta cambios antes de enviar', async () => {
  const h = serviceHarness(); h.parada.monto_recaudar = 15400.5;
  assert.equal((await h.service.obtenerParadaParaCobro(42)).totalCentavos, 1540050);
  h.parada.monto_recaudar = '15400.51';
  await assert.rejects(h.service.registrarCobranza(42, pagos), e => e instanceof h.service.ImporteParadaActualizadoError && e.totalCentavos === 1540051);
  assert.equal(h.posts.length, 0);
});

test('errores HTTP y red nunca se convierten en éxito y liberan el bloqueo para reintentar', async () => {
  for (const failure of [{ response: { status: 400, data: [{ monto: ['Importe rechazado'] }] } },
    { response: { status: 401 } }, { response: { status: 500 } }, { request: {}, code: 'ERR_NETWORK' }]) {
    const h = serviceHarness(); h.postError = failure;
    await assert.rejects(h.service.registrarCobranza(42, pagos));
    h.postError = null;
    assert.equal((await h.service.registrarCobranza(42, pagos)).cobranza_id, 71);
  }
  const h = serviceHarness(); h.response = { mensaje: 'OK' };
  await assert.rejects(h.service.registrarCobranza(42, pagos), /no confirmó/);
});

test('el servicio también bloquea solicitudes simultáneas de la misma parada', async () => {
  const h = serviceHarness(); let resolve;
  h.pending = new Promise(r => resolve = r);
  const first = h.service.registrarCobranza(42, pagos); await tick();
  await assert.rejects(h.service.registrarCobranza(42, pagos), /procesando/);
  assert.equal(h.posts.length, 1);
  resolve({ data: h.response }); await first;
});

test('la procedencia de la parada excluye los mocks y conserva la verificación al actualizar el cobro', async () => {
  const mock = { id: 1 }, mockItem = { id: 5, comercio: {} };
  const modules = { './authService': { API_BASE_URL: 'http://test', getAuthToken: () => 'token' },
    '../data/mockParada': { MOCK_PARADA_SELECCIONADA: mock },
    '../data/mockItinerario': { MOCK_ITINERARIO_ASIGNADO: { paradas: [mockItem] } } };
  let data = { id: 42, orden: 3, monto_recaudar: '15400.50', estado: 'pendiente' };
  const h = load('services/paradaService.ts', modules, { AbortController,
    setTimeout, clearTimeout, fetch: async () => ({ ok: true, json: async () => data }) });
  assert.equal(h.getIdParadaSeleccionadaParaCobro(), null);
  await h.obtenerDetalleParada(42); assert.equal(h.getIdParadaSeleccionadaParaCobro(), 42);
  h.actualizarEstadoCobroParada('validado', 'finalizada'); assert.equal(h.getIdParadaSeleccionadaParaCobro(), 42);
  assert.equal(h.getParadaSeleccionada().estado, 'finalizada');
  h.seleccionarParadaItem(mockItem); assert.equal(h.getIdParadaSeleccionadaParaCobro(), null);
  data = { monto_recaudar: '15400.50' }; await h.obtenerDetalleParada(42);
  assert.equal(h.getIdParadaSeleccionadaParaCobro(), null);
});

test('la ruta solo muestra el formulario tras verificar Django y convierte centavos al enviar', async () => {
  const h = reactHarness(), svc = serviceHarness();
  let updated = 0;
  const routes = [];
  const Route = load('app/validar-cobro.tsx', {
    react: h.react, 'react-native': h.native,
    'expo-router': { useRouter: () => ({ replace: r => routes.push(r) }),
      useFocusEffect: fn => { if (!h.focused) { h.focused = true; h.effects.push(fn()); } } },
    '../screens/ValidarCobro': 'ValidarCobro',
    '../services/paradaService': { getIdParadaSeleccionadaParaCobro: () => 42, actualizarEstadoCobroParada: () => updated++ },
    '../services/itinerarios': svc.service,
  }).default;
  assert.notEqual(h.render(Route).type, 'ValidarCobro'); await tick();
  const screen = h.render(Route); assert.equal(screen.type, 'ValidarCobro'); assert.equal(screen.props.montoTotalCentavos, 1540050);
  await screen.props.onConfirmar({ movimientos: [{ medio: 'efectivo', montoCentavos: 1000000 }, { medio: 'efectivo', montoCentavos: 540050 }], totalCentavos: 1540050 });
  assert.equal(updated, 1); assert.equal(svc.posts[0].data[1].monto, 5400.5);
  h.alerts[0][2][0].onPress(); assert.equal(routes[0].params.paradaId, '42'); assert.equal(routes[0].params.cobranzaId, '71');
});

test('en modo fallback conserva los datos de la parada seleccionada y su retorno', async () => {
  const h = reactHarness(), svc = serviceHarness();
  const routes = [];
  const quilmesStop = {
    id: 21,
    orden: 3,
    montoCobranza: 98000.0,
    comercio: { razonSocial: 'Distribuidora Quilmes', domicilio: 'Lavalle 450', localidad: 'Quilmes' },
  };
  const Route = load('app/validar-cobro.tsx', {
    react: h.react, 'react-native': h.native,
    'expo-router': {
      useRouter: () => ({ replace: r => routes.push(r) }),
      useFocusEffect: fn => { if (!h.focused) { h.focused = true; h.effects.push(fn()); } },
      useLocalSearchParams: () => ({ paradaId: '21' }),
    },
    '../screens/ValidarCobro': 'ValidarCobro',
    '../services/paradaService': {
      getIdParadaSeleccionadaParaCobro: () => null,
      actualizarEstadoCobroParada: () => {},
      getParadaSeleccionada: () => quilmesStop,
      obtenerParadaSeleccionadaOId: () => quilmesStop,
    },
    '../services/itinerarios': svc.service,
  }, { setTimeout, clearTimeout }).default;

  h.render(Route);
  await new Promise(resolve => setTimeout(resolve, 1300));
  const screen = h.render(Route);
  assert.equal(screen.type, 'ValidarCobro');
  assert.equal(screen.props.nombreComercio, 'Distribuidora Quilmes');
  assert.equal(screen.props.montoTotalCentavos, 9800000);
  assert.equal(screen.props.ordenParada, 3);
  screen.props.onVolver();
  assert.equal(routes[0].params.paradaId, '21');
});
