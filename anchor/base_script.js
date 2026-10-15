
(() => {
  const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;

  // Headline: letters rise in, like the portfolio
  const h1 = document.querySelector('[data-split]');
  let i = 0;
  const split = node => {
    [...node.childNodes].forEach(n => {
      if (n.nodeType === 3) {
        const frag = document.createDocumentFragment();
        n.textContent.split(/(\s+)/).forEach(part => {
          if (!part) return;
          if (/^\s+$/.test(part)) { frag.appendChild(document.createTextNode(' ')); return; }
          const w = document.createElement('span'); w.className = 'w'; w.setAttribute('aria-hidden', 'true');
          [...part].forEach(c => { const s = document.createElement('span'); s.className = 'ch'; s.textContent = c; s.style.setProperty('--i', i++); w.appendChild(s); });
          frag.appendChild(w);
        });
        n.replaceWith(frag);
      } else split(n);
    });
  };
  h1.setAttribute('aria-label', h1.textContent.replace(/\s+/g, ' ').trim());
  split(h1);
  requestAnimationFrame(() => setTimeout(() => document.getElementById('hero').classList.add('go'), 80));

  // Reveal on scroll
  const io = new IntersectionObserver(es => es.forEach(e => { if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); } }), { rootMargin: matchMedia('(max-width: 760px)').matches ? '0px 0px 12% 0px' : '0px 0px -8% 0px' });
  document.querySelectorAll('.rv').forEach(el => reduce ? el.classList.add('in') : io.observe(el));

  // Screens: once the page has loaded, fetch the remaining images in the background so they're ready before you scroll to them
  addEventListener('load', () => setTimeout(() => document.querySelectorAll('img[loading="lazy"]').forEach(i => { i.loading = 'eager'; }), 300));

  // Top bar: shadow + reading progress
  const top = document.getElementById('top'), prog = document.getElementById('progress');
  const onScroll = () => {
    top.classList.toggle('scrolled', scrollY > 8);
    prog.style.transform = `scaleX(${Math.min(1, scrollY / ((document.documentElement.scrollHeight - innerHeight) || 1))})`;
  };
  addEventListener('scroll', onScroll, { passive: true }); onScroll();

  // Finding index highlights the section in view
  const links = [...document.querySelectorAll('#index a')];
  const targets = links.map(a => document.querySelector(a.getAttribute('href')));
  const idx = document.getElementById('index');
  const io2 = new IntersectionObserver(es => es.forEach(e => {
    if (!e.isIntersecting) return;
    const k = targets.indexOf(e.target);
    links.forEach((a, j) => a.classList.toggle('on', j === k));
    const a = links[k]; idx.scrollTo({ left: a.offsetLeft - 16, behavior: reduce ? 'auto' : 'smooth' });
  }), { rootMargin: '-45% 0px -50% 0px' });
  targets.forEach(t => io2.observe(t));

  // Lightbox
  const lb = document.getElementById('lb'), lbImg = document.getElementById('lbImg'), lbCap = document.getElementById('lbCap');
  let opener = null;
  const close = () => { lb.classList.remove('on'); opener && opener.focus(); };
  document.querySelectorAll('.shot').forEach(b => b.addEventListener('click', () => {
    const img = b.querySelector('img'); opener = b;
    lbImg.src = img.src; lbImg.alt = img.alt; lbCap.textContent = b.dataset.cap || '';
    lb.classList.add('on'); document.getElementById('lbClose').focus();
  }));
  document.getElementById('lbClose').addEventListener('click', close);
  lb.addEventListener('click', e => { if (e.target === lb || e.target.tagName === 'FIGURE') close(); });
  addEventListener('keydown', e => { if (e.key === 'Escape' && lb.classList.contains('on')) close(); });

  // When this page is shown inside the portfolio, hand navigation back to the portfolio
  if (window.parent !== window) {
    document.addEventListener('click', e => {
      const a = e.target.closest('a[href]'); if (!a) return;
      const href = a.getAttribute('href');
      if (href.startsWith('portfolio-hero.html')) { e.preventDefault(); parent.postMessage({ pd: 'nav', hash: href.split('#')[1] || 'home' }, '*'); }
      else if (href === 'amin-prototype.html') { e.preventDefault(); parent.postMessage({ pd: 'proto' }, '*'); }
    });
    addEventListener('keydown', e => { if (e.key === 'Escape' && !lb.classList.contains('on')) parent.postMessage({ pd: 'nav', hash: 'work' }, '*'); });
  }
})();
