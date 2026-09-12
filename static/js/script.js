// ---- companion presentation data (colors, images, character names) ----
// the actual algorithm logic and concept notes come from the backend, not from here
const companions = [
  { id: "bfs", color: "#5C8B6E", img: "/static/images/BFS.png", my: "ကိုသေချာ", en: "BFS · Careful Scout", myTag: "သေချာစူးစမ်းတဲ့သူ", desc: "checks every nearby city first, one ring at a time", descMy: "အနီးအနားကို သေချာစစ်ပြီးမှ ဆက်သွားသူ" },
  { id: "dfs", color: "#B5533C", img: "/static/images/DFS.png", my: "ကိုစွန့်စား", en: "DFS · Bold Wanderer", myTag: "ရဲရဲဝံ့ဝံ့ သွားသူ", desc: "commits to one road until it hits a dead end", descMy: "လမ်းတစ်လမ်းကို ရဲရဲဝံ့ဝံ့နဲ့ အဆုံးထိသွားသူ" },
  { id: "ucs", color: "#4A7A8C", img: "/static/images/UCS.png", my: "ကိုချွေတာ", en: "UCS · Budget Trader", myTag: "ချွေတာတဲ့ခရီးသွားသူ", desc: "always follows the cheapest total distance so far", descMy: "အကုန်ကျဆုံးလမ်းကိုသာ အမြဲရွေးချယ်သူ" },
  { id: "ids", color: "#8B6BAE", img: "/static/images/IDS.png", my: "ကိုစူးစမ်း", en: "IDS · Patient Scout", myTag: "စိတ်ရှည်တဲ့စူးစမ်းသူ", desc: "retries with a longer leash each round", descMy: "တဖြည်းဖြည်းနဲ့ နေရာတွေကို ထပ်ခါထပ်ခါရှာသူ" },
  { id: "greedy", color: "#C9A227", img: "/static/images/Greedy.png", my: "ကိုစိတ်မြန်", en: "Greedy · Quick Guess", myTag: "အလျင်အမြန်ဆုံးဖြတ်ချက်ချသူ", desc: "always heads toward what looks closest", descMy: "အခုမြင်ရတဲ့ အကောင်းဆုံးလမ်းကို ချက်ချင်းရွေးသူ" },
  { id: "astar", color: "#14243C", img: "/static/images/A.png", my: "ကိုဉာဏ်ကြီး", en: "A* · Wise Guide", myTag: "ညဏ်ကောင်းတဲ့ ခရီးသွားသူ", desc: "balances distance travelled with distance left", descMy: "သွားပြီးသားခရီးနဲ့ ကျန်တဲ့ခရီးကို နှစ်ခုလုံးတွက်သူ" },
];

let cities = {};
let cityMarkers = {};
let map, routeLine = null;
let selectedId = null;

const fromSel = document.getElementById('fromSel');
const toSel = document.getElementById('toSel');
const grid = document.getElementById('cardGrid');

// ---- render companion cards (static, doesn't need backend data) ----
companions.forEach(c => {
  const el = document.createElement('div');
  el.className = 'card';
  el.dataset.id = c.id;
  el.innerHTML = `
    <div class="portrait" style="background:${c.color}22; border-color:${c.color}55">
      <img src="${c.img}" alt="${c.my}"
           onerror="this.style.display='none'; this.nextElementSibling.style.display='flex';">
      <div class="portrait-fallback" style="background:${c.color}">${c.my[1]}</div>
    </div>
    <div class="my-name">${c.my}</div>
    <div class="my-tag">${c.myTag}</div>
    <div class="en-name">${c.en}</div>
    <div class="desc">${c.desc}</div>
    <div class="desc-my">${c.descMy}</div>
  `;
  el.addEventListener('click', () => runSearch(c));
  grid.appendChild(el);
});

// ---- fetch real city list + coordinates from the backend, then build map and dropdowns ----
async function init() {
  const res = await fetch('/cities');
  const cityList = await res.json();

  cityList.forEach(c => { cities[c.name] = { lat: c.lat, lon: c.lon }; });

  const sortedNames = cityList.map(c => c.name).sort();
  sortedNames.forEach(name => {
    fromSel.innerHTML += `<option ${name === 'Yangon' ? 'selected' : ''}>${name}</option>`;
    toSel.innerHTML += `<option ${name === 'Mandalay' ? 'selected' : ''}>${name}</option>`;
  });

  // Myanmar's real national boundary (low-resolution, official-source polygon, [lon, lat] pairs)
  const myanmarBoundaryLonLat = [
    [99.543309,20.186598],[98.959676,19.752981],[98.253724,19.708203],[97.797783,18.62708],
    [97.375896,18.445438],[97.859123,17.567946],[98.493761,16.837836],[98.903348,16.177824],
    [98.537376,15.308497],[98.192074,15.123703],[98.430819,14.622028],[99.097755,13.827503],
    [99.212012,13.269294],[99.196354,12.804748],[99.587286,11.892763],[99.038121,10.960546],
    [98.553551,9.93296],[98.457174,10.675266],[98.764546,11.441292],[98.428339,12.032987],
    [98.509574,13.122378],[98.103604,13.64046],[97.777732,14.837286],[97.597072,16.100568],
    [97.16454,16.928734],[96.505769,16.427241],[95.369352,15.71439],[94.808405,15.803454],
    [94.188804,16.037936],[94.533486,17.27724],[94.324817,18.213514],[93.540988,19.366493],
    [93.663255,19.726962],[93.078278,19.855145],[92.368554,20.670883],[92.303234,21.475485],
    [92.652257,21.324048],[92.672721,22.041239],[93.166128,22.27846],[93.060294,22.703111],
    [93.286327,23.043658],[93.325188,24.078556],[94.106742,23.850741],[94.552658,24.675238],
    [94.603249,25.162495],[95.155153,26.001307],[95.124768,26.573572],[96.419366,27.264589],
    [97.133999,27.083774],[97.051989,27.699059],[97.402561,27.882536],[97.327114,28.261583],
    [97.911988,28.335945],[98.246231,27.747221],[98.68269,27.508812],[98.712094,26.743536],
    [98.671838,25.918703],[97.724609,25.083637],[97.60472,23.897405],[98.660262,24.063286],
    [98.898749,23.142722],[99.531992,22.949039],[99.240899,22.118314],[99.983489,21.742937],
    [100.416538,21.558839],[101.150033,21.849984],[101.180005,21.436573],[100.329101,20.786122],
    [100.115988,20.41785],[99.543309,20.186598],
  ];
  const myanmarBoundary = myanmarBoundaryLonLat.map(([lon, lat]) => [lat, lon]);
  const boundaryLayer = L.polygon(myanmarBoundary);
  const boundaryBounds = boundaryLayer.getBounds();
  const panBounds = boundaryBounds.pad(0.25);

  map = L.map('leafletMap', {
    zoomControl: true,
    attributionControl: false,
    maxBounds: panBounds,
    maxBoundsViscosity: 1.0,
    minZoom: 6,
    maxZoom: 11,
  });

  L.control.zoom({ position: 'topright' }).addTo(map);
  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    minZoom: 6,
    maxZoom: 11,
  }).addTo(map);

  // crisp gold outline right on the real border, to highlight Myanmar against its neighbours
  L.polygon(myanmarBoundary, {
    fill: false,
    color: '#C9A227',
    weight: 2,
  }).addTo(map);

  L.control.attribution({ position: 'bottomright', prefix: false }).addAttribution('© OpenStreetMap contributors').addTo(map);

  map.fitBounds(boundaryBounds, { padding: [16, 16] });

  cityList.forEach(c => {
    const marker = L.circleMarker([c.lat, c.lon], { radius: 4, weight: 1 }).addTo(map).bindPopup(c.name);
    cityMarkers[c.name] = marker;
  });

  // Leaflet sometimes measures its container before the page layout has fully settled,
  // which can leave the map looking blank/blank-tiled. Force a re-check shortly after.
  setTimeout(() => { map.invalidateSize(); map.fitBounds(boundaryLayer.getBounds(), { padding: [16, 16] }); }, 200);
  window.addEventListener('resize', () => { map.invalidateSize(); map.fitBounds(boundaryLayer.getBounds(), { padding: [16, 16] }); });
}
init();

// ---- run a real search against the Flask backend ----
async function runSearch(c) {
  document.querySelectorAll('.card').forEach(el => el.classList.remove('selected'));
  document.querySelector(`.card[data-id="${c.id}"]`).classList.add('selected');
  selectedId = c.id;

  const start = fromSel.value;
  const goal = toSel.value;

  Object.values(cityMarkers).forEach(marker => {
    marker.setStyle({ radius: 4, fillColor: null, color: null });
  });
  if (routeLine) { map.removeLayer(routeLine); routeLine = null; }

  document.getElementById('journeyLabel').textContent = `JOURNEY — ${start.toUpperCase()} TO ${goal.toUpperCase()}`;
  document.getElementById('routeStatus').innerHTML = `<b>${c.my}</b> is searching for a way from ${start} to ${goal}…`;
  document.getElementById('stepsList').innerHTML = '';
  document.getElementById('legendPathDot').style.background = c.color;

  if (start === goal) {
    document.getElementById('routeStatus').textContent = 'Pick two different cities to find a route.';
    return;
  }

  let result;
  try {
    const res = await fetch(`/search?start=${encodeURIComponent(start)}&goal=${encodeURIComponent(goal)}&algorithm=${c.id}`);
    result = await res.json();
  } catch (err) {
    document.getElementById('routeStatus').textContent = 'Something went wrong reaching the server.';
    return;
  }

  if (result.error) {
    document.getElementById('routeStatus').textContent = result.error;
    return;
  }

  const note = document.getElementById('conceptNote');
  note.style.display = 'block';
  document.getElementById('cnMainIdea').textContent = result.concept_note.main_idea;
  document.getElementById('cnNodeSelection').textContent = result.concept_note.node_selection;
  document.getElementById('cnInfoUsed').textContent = result.concept_note.info_used;

  if (!result.path) {
    document.getElementById('routeStatus').textContent = `${c.my} couldn't find a way from ${start} to ${goal}.`;
    return;
  }

  // Phase 1: show every city the algorithm actually checked, in the order it checked them
  document.getElementById('routeStatus').innerHTML = `<b>${c.my}</b> is exploring cities…`;
  for (const name of result.visited_order) {
    const marker = cityMarkers[name];
    if (!marker) continue;
    marker.setStyle({ fillColor: '#999999', color: '#999999', fillOpacity: 0.6 });
    marker.setRadius(5);
    await new Promise(r => setTimeout(r, 60));
  }

  document.getElementById('routeStatus').innerHTML = `<b>${c.my}</b> found the way. Tracing the route…`;
  await new Promise(r => setTimeout(r, 400));

  // Phase 2: highlight the final chosen path on top of the explored cities
  const trail = [];
  for (let i = 0; i < result.path.length; i++) {
    const name = result.path[i];
    const marker = cityMarkers[name];
    marker.setStyle({ fillColor: c.color, color: c.color, fillOpacity: 1 });
    marker.setRadius(7);

    trail.push([cities[name].lat, cities[name].lon]);
    if (trail.length > 1) {
      if (routeLine) map.removeLayer(routeLine);
      routeLine = L.polyline(trail, { color: c.color, weight: 3 }).addTo(map);
    }

    const stepRow = document.createElement('div');
    stepRow.className = 'step';
    stepRow.innerHTML = `<span class="n">${i + 1}</span><span>${name}</span>`;
    document.getElementById('stepsList').appendChild(stepRow);

    await new Promise(r => setTimeout(r, 320));
  }

  document.getElementById('routeStatus').innerHTML =
    `<b>${c.my}</b> reached ${goal} — ${result.path.length - 1} stops, ${result.visited_order.length} cities checked, ${Math.round(result.cost)} km total.`;
}

// ---- language toggle (UI chrome only — concept notes come from backend in English) ----
document.getElementById('langBtn').addEventListener('click', function() {
  const dict = {
    en: { heading: "Pick a companion. Watch them find the way across Myanmar.", sub: "25 cities, real road distances — six ways to search for a route", from: "From", to: "To", btn: "မြန်မာ" },
    my: { heading: "အဖော်တစ်ယောက်ရွေးပါ — မြန်မာနိုင်ငံတစ်ဝှမ်း လမ်းကြောင်းရှာဖွေပုံကို ကြည့်ပါ", sub: "မြို့ ၂၅ မြို့၊ တကယ့်လမ်းအကွာအဝေး — နည်းလမ်း ၆ မျိုးနဲ့ လမ်းရှာခြင်း", from: "မှ", to: "သို့", btn: "English" },
  };
  this.dataset.lang = this.dataset.lang === 'my' ? 'en' : 'my';
  const t = dict[this.dataset.lang];
  document.getElementById('pageHeading').textContent = t.heading;
  document.getElementById('pageSub').textContent = t.sub;
  document.getElementById('fromLbl').textContent = t.from;
  document.getElementById('toLbl').textContent = t.to;
  this.textContent = t.btn;
});