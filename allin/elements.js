/* brand elements: replay on tap, play all when the kit comes into view */
const elg = document.getElementById('elgrid');
if (elg) {
  const odoSet = (el, on) => el.querySelectorAll('.x-odo i').forEach((c, k) => { const d = on ? [3, 7][k] : 0; c.style.transform = `translateY(-${d * 82}px)`; });
  const confBurst = el => { const c = el.querySelector('.x-conf'); if (!c || reduce) return; c.innerHTML = Array.from({ length: 34 }, (_, i) => `<i style="left:${Math.random() * 100}%;background:${['#016A6D','#fff','#E16A3D','#10262E'][i % 4]};animation-delay:${Math.random() * .35}s"></i>`).join(''); setTimeout(() => c.innerHTML = '', 2300); };
  const play = el => { el.classList.remove('go'); odoSet(el, false); void el.offsetWidth; el.classList.add('go');
    if (el.dataset.a === 'odo') setTimeout(() => odoSet(el, true), reduce ? 0 : 120);
    if (el.dataset.a === 'conf') confBurst(el); };
  const els = [...elg.querySelectorAll('.el')];
  els.forEach(el => el.addEventListener('click', () => play(el)));
  const playAll = () => els.forEach((el, i) => setTimeout(() => play(el), reduce ? 0 : i * 140));
  document.getElementById('elplay').onclick = playAll;
  const eio = new IntersectionObserver(es => es.forEach(e => { if (e.isIntersecting) { playAll(); eio.disconnect(); } }), { threshold: .2 });
  eio.observe(elg);
  els.forEach(el => { if (el.dataset.a === 'odo') odoSet(el, true); });
}
