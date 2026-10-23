
/* ══════════════════════════════════════════
   TABS / VIEWS  (click-driven, works inside previews and on Netlify)
   ══════════════════════════════════════════ */
(function(){
  var VIEWS = {home:'Home', nine:'The Players', canada:'Canada & Legends', book:'Book a Shoot', studios:'Studios', scouted:'Get Scouted', about:'About', privacy:'Privacy Policy', terms:'Terms of Use', cookies:'Cookie Statement', accessibility:'Accessibility'};
  var ALIAS = {hero:'home', metrics:'home', services:'home', main:'home', xi:'nine', 'starting-xi':'nine', players:'nine', culture:'home', sponsors:'home', booking:'book', legends:'canada', 'media-engine':'studios', 'social-metrics':'studios', recruit:'scouted'};
  var current = null;
  function resolve(id){ return VIEWS[id] ? id : (ALIAS[id] || null); }
  window.tnbGo = function(v, opts){
    opts = opts || {};
    if(!VIEWS[v]) v = 'home';
    var views = document.querySelectorAll('.view');
    for(var i=0;i<views.length;i++){
      var on = views[i].getAttribute('data-view') === v;
      views[i].hidden = !on;
      if(on){ views[i].classList.remove('view-enter'); void views[i].offsetWidth; views[i].classList.add('view-enter'); }
    }
    document.querySelectorAll('[data-view-link]').forEach(function(a){
      var on = a.getAttribute('data-view-link') === v;
      a.classList.toggle('active', on);
      if(on) a.setAttribute('aria-current','page'); else a.removeAttribute('aria-current');
    });
    document.title = (v==='home' ? 'True North Ballers: Canada\'s Soccer Culture, Documented' : VIEWS[v] + ' | True North Ballers');
    if(typeof closeMobileNav === 'function') closeMobileNav();
    try { window.scrollTo({top:0, behavior:'instant'}); } catch(e){ window.scrollTo(0,0); }
    try { if(location.hash.slice(1) !== v) history.replaceState(null, '', '#'+v); } catch(e){}
    if(!opts.initial){
      var h = document.querySelector('.view[data-view="'+v+'"] .view-title');
      if(h) h.focus({preventScroll:true});
    }
    current = v;
  };
  document.addEventListener('click', function(e){
    var a = e.target.closest && e.target.closest('a[href^="#"]');
    if(!a) return;
    var id = a.getAttribute('href').slice(1);
    var v = resolve(id);
    if(!v) return;
    e.preventDefault();
    window.tnbGo(v);
  });
  var start = resolve(location.hash.slice(1)) || 'home';
  window.tnbGo(start, {initial:true});
})();

/* Escape closes the mobile menu */
document.addEventListener('keydown', function(e){
  if(e.key !== 'Escape') return;
  var nav = document.getElementById('mobileNav');
  if(nav && nav.classList.contains('open')) closeMobileNav();
});

/* ══════════════════════════════════════════
   MOTION TOGGLE (pause tickers, particles, sparks)
   ══════════════════════════════════════════ */
(function(){
  var btn = document.getElementById('motionToggle');
  if(!btn) return;
  function set(paused){
    document.body.classList.toggle('motion-paused', paused);
    btn.setAttribute('aria-pressed', String(paused));
    btn.setAttribute('aria-label', paused ? 'Play animations' : 'Pause animations');
    btn.textContent = paused ? '▶' : '❚❚';
  }
  if(window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches) set(true);
  btn.addEventListener('click', function(){ set(!document.body.classList.contains('motion-paused')); });
})();
