'use strict';
const controls = ['search', 'topic', 'type', 'scope', 'cost'].map(id => document.getElementById(id));
const cards = Array.from(document.querySelectorAll('.card'));
document.querySelector('.filters').hidden = false;
function filter() {
  const [search, topic, type, scope, cost] = controls.map(el => el.value.trim());
  const words = search.toLowerCase().split(/\s+/).filter(Boolean);
  let visible = 0;
  for (const card of cards) {
    const match = words.every(word => card.dataset.search.includes(word)) &&
      (!topic || card.dataset.topics.split('|').includes(topic)) &&
      (!type || card.dataset.type === type) && (!scope || card.dataset.scope === scope) &&
      (!cost || card.dataset.cost === cost);
    card.hidden = !match;
    visible += Number(match);
  }
  document.getElementById('results').textContent = `Showing ${visible} of ${cards.length} resources`;
  document.getElementById('empty').hidden = visible !== 0;
}
controls.forEach(el => el.addEventListener('input', filter));
document.getElementById('reset').addEventListener('click', () => { controls.forEach(el => { el.value = ''; }); filter(); });
