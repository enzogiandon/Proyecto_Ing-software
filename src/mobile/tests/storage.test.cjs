const { test } = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');
const ts = require('typescript');

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
    async clear() {
      store.clear();
    },
  };
}

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
      if (name.endsWith('.png')) return name;
      throw new Error('Importación sin preparar: ' + name);
    },
    console,
    Error,
    JSON,
    setTimeout,
    clearTimeout,
    ...globals,
  };
  vm.runInNewContext(code, context);
  return exports;
}

test('HU-storage: saveTokens persiste en AsyncStorage en entorno nativo móvil sin window', async () => {
  const asyncStorageMock = createAsyncStorageMock();
  // Simulamos entorno React Native / Expo nativo donde window es undefined
  const storage = loadModule('services/storage.ts', {
    '@react-native-async-storage/async-storage': { __esModule: true, default: asyncStorageMock, ...asyncStorageMock },
  }, { window: undefined });

  await storage.saveTokens('token-acceso-123', 'token-refresh-456');

  assert.equal(asyncStorageMock._store.get('repartoya_access_token'), 'token-acceso-123');
  assert.equal(asyncStorageMock._store.get('repartoya_refresh_token'), 'token-refresh-456');

  const access = await storage.getAccessToken();
  const refresh = await storage.getRefreshToken();

  assert.equal(access, 'token-acceso-123');
  assert.equal(refresh, 'token-refresh-456');
});

test('HU-storage: simulación de cierre y reapertura de app recupera tokens desde AsyncStorage', async () => {
  const asyncStorageMock = createAsyncStorageMock();
  asyncStorageMock._store.set('repartoya_access_token', 'token-persistido-789');
  asyncStorageMock._store.set('repartoya_refresh_token', 'refresh-persistido-789');

  // Nueva instancia limpia simulando inicio desde cero de la app sin memoria previa y sin window
  const storageReinicio = loadModule('services/storage.ts', {
    '@react-native-async-storage/async-storage': { __esModule: true, default: asyncStorageMock, ...asyncStorageMock },
  }, { window: undefined });

  const tokenRecuperado = await storageReinicio.getAccessToken();
  const refreshRecuperado = await storageReinicio.getRefreshToken();

  assert.equal(tokenRecuperado, 'token-persistido-789');
  assert.equal(refreshRecuperado, 'refresh-persistido-789');
});

test('HU-storage: clearTokens elimina credenciales de memoria y AsyncStorage', async () => {
  const asyncStorageMock = createAsyncStorageMock();
  const storage = loadModule('services/storage.ts', {
    '@react-native-async-storage/async-storage': { __esModule: true, default: asyncStorageMock, ...asyncStorageMock },
  }, { window: undefined });

  await storage.saveTokens('access-temporal', 'refresh-temporal');
  assert.equal(asyncStorageMock._store.size, 2);

  await storage.clearTokens();

  assert.equal(asyncStorageMock._store.get('repartoya_access_token'), undefined);
  assert.equal(asyncStorageMock._store.get('repartoya_refresh_token'), undefined);

  const token = await storage.getAccessToken();
  assert.equal(token, null);
});

test('HU-storage: saveUserSession y getUserSession persisten y recuperan datos del transportista', async () => {
  const asyncStorageMock = createAsyncStorageMock();
  const storage = loadModule('services/storage.ts', {
    '@react-native-async-storage/async-storage': { __esModule: true, default: asyncStorageMock, ...asyncStorageMock },
  }, { window: undefined });

  const usuarioPrueba = {
    dni: '12345678',
    first_name: 'Martín',
    last_name: 'Rodríguez',
    vehiculo: { patente: 'AB 458 CD' },
  };

  await storage.saveUserSession(usuarioPrueba);

  assert.ok(asyncStorageMock._store.has('repartoya_transportista_session'));

  // Nueva instancia simulando reinicio
  const storageReinicio = loadModule('services/storage.ts', {
    '@react-native-async-storage/async-storage': { __esModule: true, default: asyncStorageMock, ...asyncStorageMock },
  }, { window: undefined });

  const usuarioRecuperado = await storageReinicio.getUserSession();
  assert.deepEqual(usuarioRecuperado, usuarioPrueba);

  await storageReinicio.clearUserSession();
  assert.equal(await storageReinicio.getUserSession(), null);
});

test('HU-storage: authService restaura sesión automáticamente tras reinicio de la aplicación', async () => {
  const asyncStorageMock = createAsyncStorageMock();
  asyncStorageMock._store.set('repartoya_access_token', 'token-chofer-autenticado');
  asyncStorageMock._store.set(
    'repartoya_transportista_session',
    JSON.stringify({ dni: '12345678', first_name: 'Martín', last_name: 'Rodríguez' })
  );

  const storageMock = loadModule('services/storage.ts', {
    '@react-native-async-storage/async-storage': { __esModule: true, default: asyncStorageMock, ...asyncStorageMock },
  }, { window: undefined });

  const authService = loadModule('services/authService.ts', {
    './storage': storageMock,
    './config': { BACKEND_URL: 'http://test' },
    '../data/mockData': {
      CHOFERES_PRUEBA: [],
      MOCK_CHOFER_ACTUAL: { dni: '12345678', first_name: 'Martín', last_name: 'Rodríguez' },
    },
  }, { window: undefined, fetch: () => Promise.reject(new Error('offline')) });

  // Antes de restaurar, la sesión en memoria está vacía
  assert.equal(authService.estaAutenticado(), false);

  // Al restaurar sesión desde AsyncStorage
  const restaurado = await authService.restaurarSesion();
  assert.equal(restaurado, true);
  assert.equal(authService.estaAutenticado(), true);
  assert.equal(authService.getAuthToken(), 'token-chofer-autenticado');
  assert.equal(authService.getUsuarioActual()?.first_name, 'Martín');

  // Al cerrar sesión, limpia el almacenamiento y el estado
  authService.cerrarSesion();
  assert.equal(authService.estaAutenticado(), false);
  assert.equal(authService.getAuthToken(), null);
});
