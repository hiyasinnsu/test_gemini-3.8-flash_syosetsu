const fs = require('fs');
const vm = require('vm');

const html = fs.readFileSync('index.html', 'utf8');

const match = html.match(/<script>([\s\S]*?)<\/script>/);
if (!match) {
  console.error('No script tag found!');
  process.exit(1);
}

const context = {
  window: {
    location: { search: '', hash: '' },
    onload: null
  },
  document: {
    documentElement: { style: { setProperty: () => {} } },
    body: { classList: { add: () => {}, remove: () => {}, contains: () => false } },
    getElementById: () => ({ textContent: '', value: '', disabled: false, classList: { add: () => {}, remove: () => {} } }),
    querySelectorAll: () => []
  },
  localStorage: {
    getItem: () => null,
    setItem: () => {}
  },
  history: {
    replaceState: () => {}
  },
  console: console
};

try {
  vm.createContext(context);
  vm.runInContext(match[1] + '; console.log("Novel 1 chapters:", novels["1"].chapters.length); console.log("Novel 2 chapters:", novels["2"].chapters.length);', context);
  console.log('JS validation: SUCCESS!');
} catch (e) {
  console.error('Error executing script:', e);
  process.exit(1);
}
