'use strict';
const controls = ['search', 'topic', 'type', 'failure', 'cost'].map(id => document.getElementById(id));
const collection = document.getElementById('collection');
const cards = Array.from(document.querySelectorAll('.card'));
document.querySelector('.filters').hidden = false;
function filter() {
  const [search, topic, type, failure, cost] = controls.map(el => el.value.trim());
  const words = search.toLowerCase().split(/\s+/).filter(Boolean);
  let visible = 0;
  for (const card of cards) {
    const match = words.every(word => card.dataset.search.includes(word)) &&
      (!topic || card.dataset.topics.split('|').includes(topic)) &&
      (!type || card.dataset.type === type) && (!failure || card.dataset.modes.split('|').includes(failure)) &&
      (collection.value === 'all' || card.dataset.collection === collection.value) &&
      (!cost || card.dataset.cost === cost);
    card.hidden = !match;
    visible += Number(match);
  }
  document.getElementById('results').textContent = `Showing ${visible} of ${cards.length} resources`;
  document.getElementById('empty').hidden = visible !== 0;
}
collection.addEventListener('change', () => {
  controls.forEach(el => { el.value = ''; });
  document.getElementById('collection-note').textContent = {agents: 'Start with labs and tools, then deepen your understanding through guidance and research.', foundations: 'Supporting AI and engineering foundations. Original relevance labels remain visible.', credentials: 'Credentials (verify claims): check syllabus, prerequisites, assessment, availability and cost with the provider. Inclusion is not endorsement.', all: 'The complete catalog, including foundations and credentials.'}[collection.value];
  filter();
});
controls.forEach(el => el.addEventListener('input', filter));
function resetFilters() {
  controls.forEach(el => { el.value = ''; });
  filter();
  controls[0].focus({ preventScroll: true });
}
document.getElementById('reset').addEventListener('click', resetFilters);
document.getElementById('empty-reset').addEventListener('click', resetFilters);

filter();
