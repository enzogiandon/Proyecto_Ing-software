const { test } = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs'), path = require('node:path'), vm = require('node:vm');
const ts = require('typescript');

// Se prueban los módulos reales con respuestas HTTP controladas, sin Django.
function load(file, modules = {}) {
  const code = ts.transpileModule(fs.readFileSync(path.join(__dirname, '../src', file), 'utf8'), {
    compilerOptions: { module: ts.ModuleKind.CommonJS, target: ts.ScriptTarget.ES2020,
      jsx: ts.JsxEmit.React, esModuleInterop: true },
  }).outputText;
  const exports = {};
  vm.runInNewContext(code, { exports, Error, console, FormData, Blob,
    require(name) {
      if (name in modules) return modules[name];
      if (name.endsWith('.png')) return name;
      throw new Error('Importación sin preparar: ' + name);
    },
  });
  return exports;
}
const money = load('utils/importes.ts');
const tipos = load('types/inconveniente.ts');
const tick = () => new Promise(setImmediate);
const payload = { tipo: 'local_cerrado', descripcion: 'Comercio cerrado', impide_entrega: true };

function serviceHarness() {
  const h = { selectedId: 42, stop: { id: 42, orden: 3,
    comercio: { razonSocial: 'Comercio original', domicilio: 'Calle 10' } }, calls: [],
    response: { mensaje: 'OK', problema: { id: 71, parada: 42, ...payload },
      parada_estado: 'error', itinerario_finalizado: false } };
  h.api = { async post(url, data) {
    h.calls.push({ url, data });
    if (h.failure) throw h.failure;
    if (h.pending) return h.pending;
    return { data: h.response };
  } };
  h.service = load('services/itinerarios.ts', {
    './api': h.api, 'react-native': { Platform: { OS: 'web' } },
    '../utils/importes': money,
    './paradaService': { getIdParadaSeleccionadaParaCobro: () => h.selectedId,
      getParadaSeleccionada: () => h.stop },
    '../data/mockParada': {}, '../data/mockItinerario': {},
  });
  return h;
}
function find(node, predicate) {
  if (!node || typeof node !== 'object') return;
  if (predicate(node)) return node;
  for (const child of (node.children || []).flat(Infinity)) {
    const result = find(child, predicate); if (result) return result;
  }
}
function text(node) {
  if (typeof node === 'string' || typeof node === 'number') return String(node);
  return node?.children?.flat(Infinity).map(text).join(' ') || '';
}
function screenHarness(service = serviceHarness()) {
  const h = { service, states: [], refs: [], i: 0, r: 0, routes: [], alerts: [], params: {}, focused: false };
  const react = {
    createElement: (type, props, ...children) => ({ type, props: props || {}, children }),
    useState(initial) {
      const i = h.i++;
      if (!(i in h.states)) h.states[i] = typeof initial === 'function' ? initial() : initial;
      return [h.states[i], value => h.states[i] = typeof value === 'function' ? value(h.states[i]) : value];
    },
    useRef(initial) { const i = h.r++; return h.refs[i] ?? (h.refs[i] = { current: initial }); },
    useCallback: fn => fn,
  };
  const native = { StyleSheet: { create: s => s }, Platform: { OS: 'android' },
    Alert: { alert: (...args) => h.alerts.push(args) } };
  for (const key of ['ActivityIndicator', 'Image', 'KeyboardAvoidingView', 'ScrollView', 'Text', 'TextInput', 'TouchableOpacity', 'View']) native[key] = key;
  h.modules = { react, 'react-native': native,
    'expo-router': { useRouter: () => ({ replace: route => h.routes.push(route) }),
      useLocalSearchParams: () => h.params, Redirect: 'Redirect',
      useFocusEffect: effect => { if (!h.focused) { h.focused = true; h.cleanup = effect(); } } },
    'react-native-safe-area-context': { useSafeAreaInsets: () => ({ top: 0, bottom: 0 }) },
    '../constants/theme': { RepartoYA: { blanco: '#fff', azulRuta: '#123C6B' } },
    '../types/inconveniente': tipos,
    '../services/paradaService': { getParadaSeleccionada: () => service.stop,
      getIdParadaSeleccionadaParaCobro: () => service.selectedId },
    '../services/itinerarios': service.service,
  };
  h.Form = load('screens/RegistrarInconveniente.tsx', h.modules).default;
  h.Confirm = load('screens/InconvenienteRegistrado.tsx', h.modules).default;
  h.draw = (Component = h.Form) => { h.i = h.r = 0; return Component(); };
  h.fill = () => {
    let tree = h.draw();
    find(tree, n => n.props.accessibilityRole === 'radio' && text(n).includes('Local cerrado')).props.onPress();
    tree = h.draw();
    find(tree, n => n.type === 'TextInput').props.onChangeText('  Comercio cerrado  ');
    find(tree, n => n.props.accessibilityRole === 'checkbox').props.onPress();
  };
  h.submit = () => find(h.draw(), n => n.props.accessibilityState && 'busy' in n.props.accessibilityState);
  return h;
}

test('envía los tres campos al endpoint real y conserva una confirmación de la parada enviada', async () => {
  const h = serviceHarness();
  const response = await h.service.reportarProblemaParada(42, { ...payload, descripcion: '  Comercio cerrado  ' });
  assert.equal(response.problema.id, 71);
  assert.equal(h.calls[0].url, 'paradas/42/reportar-problema/');
  assert.deepEqual(JSON.parse(JSON.stringify(h.calls[0].data)), payload);
  const receipt = h.service.getConfirmacionInconveniente(71, 42);
  assert.equal(receipt.parada.razonSocial, 'Comercio original');
  assert.equal(receipt.problema.impide_entrega, true);
  assert.equal(h.service.getConfirmacionInconveniente(71, 99), null);
  assert.equal(h.service.getConfirmacionInconveniente(NaN, 42), null);
});

test('envía también false y descripción vacía sin inventar valores', async () => {
  const h = serviceHarness();
  h.response.problema = { id: 71, parada: 42, tipo: 'local_cerrado', descripcion: '', impide_entrega: false };
  h.response.parada_estado = 'pendiente';
  await h.service.reportarProblemaParada(42, { tipo: 'local_cerrado', impide_entrega: false });
  assert.equal(h.calls[0].data.descripcion, ''); assert.equal(h.calls[0].data.impide_entrega, false);
});

test('bloquea IDs inválidos, selección simulada y datos inválidos antes del HTTP', async () => {
  for (const id of [0, -1, NaN, 1.5]) {
    const h = serviceHarness(); await assert.rejects(h.service.reportarProblemaParada(id, payload)); assert.equal(h.calls.length, 0);
  }
  for (const setup of [h => h.selectedId = null, h => h.stop.id = 99]) {
    const h = serviceHarness(); setup(h); await assert.rejects(h.service.reportarProblemaParada(42, payload)); assert.equal(h.calls.length, 0);
  }
  for (const data of [{ ...payload, tipo: '' }, { ...payload, impide_entrega: 'true' },
    { ...payload, descripcion: 'x'.repeat(256) }, { ...payload, tipo: 'otro', descripcion: ' ' }]) {
    const h = serviceHarness(); await assert.rejects(h.service.reportarProblemaParada(42, data)); assert.equal(h.calls.length, 0);
  }
});

test('HTTP 400/401/403/404/500, red y timeout rechazan el registro y permiten reintentar', async () => {
  for (const failure of [{ response: { status: 400, data: { descripcion: ['Texto rechazado'] } } },
    ...[401, 403, 404, 500].map(status => ({ response: { status } })),
    { request: {}, code: 'ERR_NETWORK' }, { request: {}, code: 'ECONNABORTED' }]) {
    const h = serviceHarness(); h.failure = failure;
    await assert.rejects(h.service.reportarProblemaParada(42, payload));
    assert.equal(h.service.getConfirmacionInconveniente(71, 42), null);
    h.failure = null; assert.equal((await h.service.reportarProblemaParada(42, payload)).problema.id, 71);
  }
});

test('no confirma respuestas incompletas o de otro motivo, descripción, indicador o parada', async () => {
  const changes = [h => h.response = { mensaje: 'OK' }, h => h.response.problema.id = 0,
    h => h.response.problema.parada = 99, h => h.response.problema.tipo = 'otro',
    h => h.response.problema.descripcion = 'Otro texto', h => h.response.problema.impide_entrega = false,
    h => h.response.parada_estado = 'pendiente', h => delete h.response.itinerario_finalizado];
  for (const change of changes) {
    const h = serviceHarness(); change(h);
    await assert.rejects(h.service.reportarProblemaParada(42, payload), /no confirmó/);
    assert.equal(h.service.getConfirmacionInconveniente(71, 42), null);
  }
});

test('el servicio bloquea solicitudes concurrentes para la misma parada', async () => {
  const h = serviceHarness(); let resolve;
  h.pending = new Promise(r => resolve = r);
  const first = h.service.reportarProblemaParada(42, payload); await tick();
  await assert.rejects(h.service.reportarProblemaParada(42, payload), /enviando/);
  assert.equal(h.calls.length, 1); resolve({ data: h.response }); await first;
});

test('formulario espera Django, muestra indicador y bloquea doble toque y edición', async () => {
  const service = serviceHarness(); let resolve;
  service.pending = new Promise(r => resolve = r);
  const h = screenHarness(service); h.fill();
  const button = h.submit(); const pending = button.props.onPress(); await button.props.onPress();
  assert.equal(service.calls.length, 1); assert.equal(h.routes.length, 0);
  const tree = h.draw(); assert.equal(h.submit().props.disabled, true);
  assert.ok(find(tree, n => n.type === 'ActivityIndicator'));
  assert.equal(find(tree, n => n.type === 'TextInput').props.editable, false);
  assert.equal(find(tree, n => n.props.accessibilityRole === 'radio').props.disabled, true);
  resolve({ data: service.response }); await pending;
  assert.equal(h.routes.length, 1); assert.equal(h.routes[0].params.problemaId, '71'); assert.equal(h.routes[0].params.paradaId, '42');
  assert.equal(h.states[0], null); assert.equal(h.states[1], '');
});

test('formulario envía con el mismo botón aun si falla la API y navega a confirmación', async () => {
  const service = serviceHarness(); service.failure = { response: { status: 500 } };
  const h = screenHarness(service); h.fill(); await h.submit().props.onPress();
  assert.equal(h.routes.length, 1);
  assert.equal(h.routes[0].params.paradaId, '42');
  assert.equal(h.routes[0].params.modoDemo, 'true');
});

test('pantalla permite enviar paradas sin conexión al back y conserva las nueve opciones aprobadas', async () => {
  const service = serviceHarness(); service.selectedId = null;
  const h = screenHarness(service); const tree = h.draw();
  assert.equal(h.submit().props.disabled, false); assert.doesNotMatch(text(tree), /Falta una parada verificada/);
  assert.equal(tipos.TIPOS_INCONVENIENTE.length, 9);
  assert.equal(find(tree, n => n.type === 'TextInput').props.maxLength, 255);
  h.fill();
  await h.submit().props.onPress();
  assert.equal(h.routes.length, 1);
  assert.equal(h.routes[0].params.modoDemo, 'true');
});

test('confirmación usa el registro real y la parada original aunque cambie la selección', async () => {
  const service = serviceHarness(), h = screenHarness(service);
  h.params = { problemaId: '71', paradaId: '42', descripcion: 'Texto inventado' };
  assert.equal(h.draw(h.Confirm).type, 'Redirect');
  await service.service.reportarProblemaParada(42, payload);
  service.stop = { id: 99, orden: 9, comercio: { razonSocial: 'Otro comercio' } };
  const tree = h.draw(h.Confirm);
  assert.notEqual(tree.type, 'Redirect'); assert.match(text(tree), /Comercio original/);
  assert.match(text(tree), /Comercio cerrado/); assert.doesNotMatch(text(tree), /Texto inventado|Otro comercio|demostración/);
  find(tree, n => n.props.onPress && text(n).includes('Volver a la parada')).props.onPress();
  assert.equal(h.routes[0].params.paradaId, '42'); assert.equal(h.routes[0].params.inconvenienteId, '71'); assert.equal(h.routes[0].params.cobranzaId, '');
  h.params.paradaId = '99'; assert.equal(h.draw(h.Confirm).type, 'Redirect');
});
