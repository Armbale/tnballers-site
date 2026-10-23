
/* ══════════════════════════════════════════
   THE NINE: card slider, player pop-up, stats table
   ══════════════════════════════════════════ */
(function(){
  var P = window.ninePlayers || [];
  if(!P.length) return;
  var N = P.length;
  var AB = {Finishing:'FIN',Strength:'STR',Aerial:'AER',Dribbling:'DRI',Pace:'PAC',Stamina:'STA',Crossing:'CRO',Passing:'PAS',Tackling:'TAC',Vision:'VIS',Shooting:'SHO',Defending:'DEF',Positioning:'POS',Distribution:'DIS',Reflexes:'REF',Command:'COM'};
  function esc(s){ return String(s).replace(/[&<>"']/g, function(c){ return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]; }); }
  function pad(n){ return (n<10?'0':'')+n; }
  function tot(p){
    var t={apps:0,starts:0,mins:0,g:0,a:0,sp:false,mp:false};
    p.comps.forEach(function(c){
      t.apps+=c.apps; t.g+=c.g; t.a+=c.a;
      if(c.starts==null) t.sp=true; else t.starts+=c.starts;
      if(c.mins==null) t.mp=true; else t.mins+=c.mins;
    });
    return t;
  }
  function fmt(n, partial){ return (n==null?'–':n.toLocaleString('en-CA')) + (partial?'+':''); }
  function ovr(p){ var s=0; p.stats.forEach(function(x){ s+=x.v; }); return Math.round(s/p.stats.length); }
  P.forEach(function(p){ p._t = tot(p); p._o = ovr(p); });
  var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  function motionOff(){ return reduce || document.body.classList.contains('motion-paused'); }

  function cardHTML(p, big){
    var attrs = p.stats.map(function(x){ return '<div class="fut-attr"><b>'+x.v+'</b><span>'+(AB[x.l]||x.l.slice(0,3).toUpperCase())+'</span></div>'; }).join('');
    attrs += '<div class="fut-attr fut-attr-season"><b>'+p._t.apps+'</b><span>APP</span></div>';
    var photo = p.photo ? '<img src="'+p.photo+'" alt="" loading="lazy" draggable="false">' : '<span class="fut-initials">'+esc(p.first[0]+p.last[0])+'</span>';
    return '<div class="fut-card'+(big?' fut-big':'')+'" aria-hidden="true"><div class="fut-in">'+
      '<div class="fut-sash"></div><div class="fut-shine"></div>'+
      '<div class="fut-top">'+
        '<div class="fut-meta"><span class="fut-ovr">'+p._o+'</span><span class="fut-pos">'+p.short+'</span><span class="fut-leaf">🍁</span><span class="fut-club">'+esc(p.clubCode)+'</span></div>'+
        '<div class="fut-photo">'+photo+'</div>'+
      '</div>'+
      '<div class="fut-name">'+esc(p.last)+'</div>'+
      '<div class="fut-attrs">'+attrs+'</div>'+
      '<div class="fut-foot"><span>TNB · 2026</span><span>#'+esc(p.jersey)+'</span></div>'+
      (p.news ? '<div class="fut-news">NEW</div>' : '')+
    '</div></div>';
  }

  /* ---------- pop-up ---------- */
  var modal = document.createElement('div');
  modal.className = 'nine-modal'; modal.hidden = true;
  modal.innerHTML = '<div class="nine-backdrop" data-close></div>'+
    '<div class="nine-dialog" role="dialog" aria-modal="true" aria-labelledby="nineMTitle" tabindex="-1">'+
      '<div class="nine-mtop"><span class="nine-mcount" id="nineMCount"></span>'+
        '<div class="nine-mnav"><button type="button" class="nine-arrow" data-step="-1" aria-label="Previous player">←</button><button type="button" class="nine-arrow" data-step="1" aria-label="Next player">→</button>'+
        '<button type="button" class="nine-close" data-close aria-label="Close player stats">✕</button></div></div>'+
      '<div class="nine-mbody" id="nineMBody"></div>'+
    '</div>';
  document.body.appendChild(modal);
  var mBody = modal.querySelector('#nineMBody'), mCount = modal.querySelector('#nineMCount'), dialog = modal.querySelector('.nine-dialog');
  var cur = -1, returnFocus = null;

  function tiles(p){
    var t=p._t, list;
    if(p.gk) list=[['Apps',fmt(t.apps)],['Mins',fmt(t.mins,t.mp)],['Saves',fmt(p.gk.saves)],['Conceded',fmt(p.gk.ga)],['Clean sheets',fmt(p.gk.cs)]];
    else list=[['Apps',fmt(t.apps)],['Starts',(t.sp&&!t.starts)?'–':fmt(t.starts,t.sp)],['Mins',fmt(t.mins,t.mp)],['Goals',fmt(t.g)],['Assists',fmt(t.a)]];
    return list.map(function(x){ return '<div class="nine-tile"><b>'+x[1]+'</b><span>'+x[0]+'</span></div>'; }).join('');
  }
  function render(i){
    var p=P[i], t=p._t;
    var rows = p.comps.map(function(c){
      return '<tr><th scope="row">'+esc(c.c)+'</th><td>'+fmt(c.apps)+'</td><td>'+fmt(c.starts)+'</td><td>'+fmt(c.mins)+'</td><td>'+fmt(c.g)+'</td><td>'+fmt(c.a)+'</td></tr>';
    }).join('');
    var bars = p.stats.map(function(x){ return '<div class="nine-bar-row"><span>'+esc(x.l)+'</span><div class="nine-bar-track"><i style="width:'+x.v+'%"></i></div><b>'+x.v+'</b></div>'; }).join('');
    var hl = p.highlights.map(function(h){ return '<li>'+esc(h)+'</li>'; }).join('');
    mBody.innerHTML =
      '<div class="nine-mcard">'+cardHTML(p,true)+'</div>'+
      '<div class="nine-minfo">'+
        (p.news ? '<p class="nine-news"><span>Latest</span>'+esc(p.news)+'</p>' : '')+
        '<h3 class="nine-mname" id="nineMTitle">'+esc(p.name)+'</h3>'+
        '<p class="nine-msub">'+esc(p.pos)+' · '+esc(p.club)+' · #'+esc(p.jersey)+'</p>'+
        '<div class="nine-chips">'+
          (p.ig ? '<a class="nine-chip nine-ig" href="'+p.ig+'" target="_blank" rel="noopener noreferrer">'+esc(p.igHandle)+'<span class="visually-hidden"> on Instagram (opens in a new tab)</span></a>' : '')+
          (p.agency ? '<span class="nine-chip">🤝 '+esc(p.agency)+'</span>' : '')+
          (p.from ? '<span class="nine-chip">🍁 '+esc(p.from)+'</span>' : '')+
        '</div>'+
        '<h4 class="nine-h4">2026 season · all competitions</h4>'+
        '<div class="nine-tiles'+(p.gk?' gk':'')+'">'+tiles(p)+'</div>'+
        '<div class="nine-comps"><table><caption class="visually-hidden">'+esc(p.name)+' 2026 statistics by competition</caption><thead><tr><th scope="col">Competition</th><th scope="col">Apps</th><th scope="col">Starts</th><th scope="col">Mins</th><th scope="col">G</th><th scope="col">A</th></tr></thead><tbody>'+rows+'</tbody></table></div>'+
        '<p class="nine-src">Source: '+(p.src||[]).map(function(x){ return '<a href="'+x.u+'" target="_blank" rel="noopener noreferrer">'+esc(x.t)+'<span class="visually-hidden"> (opens in a new tab)</span></a>'; }).join(', ')+' · as of '+STATS_ASOF+'</p>'+
        '<h4 class="nine-h4">TNB scout ratings</h4><div class="nine-bars">'+bars+'</div>'+
        '<h4 class="nine-h4">Highlights</h4><ul class="nine-hl">'+hl+'</ul>'+
        '<p class="nine-asof">Stats as of '+STATS_ASOF+'. "–" means not published.</p>'+
      '</div>';
    mCount.textContent = 'Player '+pad(i+1)+' of '+pad(N);
    cur = i;
  }
  function open(i, from){
    returnFocus = from || document.activeElement;
    render(i);
    modal.hidden = false;
    document.documentElement.classList.add('nine-lock');
    requestAnimationFrame(function(){ modal.classList.add('on'); });
    dialog.focus({preventScroll:true});
  }
  function close(){
    if(modal.hidden) return;
    modal.classList.remove('on'); modal.hidden = true; cur = -1;
    document.documentElement.classList.remove('nine-lock');
    if(returnFocus && returnFocus.focus) returnFocus.focus({preventScroll:true});
  }
  function step(d){ if(cur<0) return; render((cur+d+N)%N); sliders.forEach(function(s){ s.go(cur,true); }); }
  window.nineOpen = function(i){ open(i); };
  window.nineClose = close;
  window.nineCurrent = function(){ return cur; };
  modal.addEventListener('click', function(e){
    if(e.target.closest('[data-close]')) close();
    var a = e.target.closest('[data-step]'); if(a) step(+a.getAttribute('data-step'));
  });
  document.addEventListener('keydown', function(e){
    if(modal.hidden) return;
    if(e.key==='Escape'){ e.preventDefault(); e.stopPropagation(); close(); }
    else if(e.key==='ArrowRight'){ step(1); }
    else if(e.key==='ArrowLeft'){ step(-1); }
    else if(e.key==='Tab'){
      var f = modal.querySelectorAll('button, a[href]'); if(!f.length) return;
      var first=f[0], last=f[f.length-1];
      if(e.shiftKey && (document.activeElement===first || document.activeElement===dialog)){ e.preventDefault(); last.focus(); }
      else if(!e.shiftKey && document.activeElement===last){ e.preventDefault(); first.focus(); }
    }
  }, true);

  /* ---------- sliders ---------- */
  var sliders = [];
  function Slider(root){
    var self=this, active=0, hover=false, focusIn=false, visible=false, holdUntil=0, ticking=false;
    root.innerHTML =
      '<div class="nine-head"><div class="nine-count" aria-live="polite"><b>01</b><span>/ '+pad(N)+'</span></div>'+
      '<div class="nine-name-live" aria-hidden="true"></div>'+
      '<div class="nine-ctrls"><button type="button" class="nine-arrow" data-dir="-1" aria-label="Previous player">←</button><button type="button" class="nine-arrow" data-dir="1" aria-label="Next player">→</button></div></div>'+
      '<ul class="nine-track" aria-label="TNB partner players">'+
        P.map(function(p,i){
          return '<li class="nine-slide" data-i="'+i+'"><button type="button" class="nine-open" data-i="'+i+'" aria-label="'+esc(p.name)+', '+esc(p.pos)+', '+esc(p.club)+'. Open stats">'+cardHTML(p,false)+'</button>'+
            '<div class="nine-cap"><span class="nine-cap-num">'+pad(i+1)+'</span><b>'+esc(p.name)+'</b><span>'+esc(p.club)+'</span></div></li>';
        }).join('')+
      '</ul>'+
      '<div class="nine-dots">'+P.map(function(p,i){ return '<button type="button" class="nine-dot" data-i="'+i+'" aria-label="Show player '+(i+1)+': '+esc(p.name)+'"><span>'+(i+1)+'</span></button>'; }).join('')+'</div>'+
      '<div class="nine-progress" aria-hidden="true"><i></i></div>';
    var track=root.querySelector('.nine-track'), slides=[].slice.call(root.querySelectorAll('.nine-slide')),
        dots=[].slice.call(root.querySelectorAll('.nine-dot')), countB=root.querySelector('.nine-count b'),
        bar=root.querySelector('.nine-progress i');
    function setActive(i){
      active=i;
      slides.forEach(function(s,k){ s.classList.toggle('is-active',k===i); s.classList.toggle('is-near',Math.abs(k-i)===1); });
      dots.forEach(function(d,k){ d.classList.toggle('on',k===i); if(k===i) d.setAttribute('aria-current','true'); else d.removeAttribute('aria-current'); });
      countB.textContent = pad(i+1);
      bar.style.width = ((i+1)/N*100)+'%';
    }
    this.go = function(i, instant){
      i=(i+N)%N; var s=slides[i];
      var left = s.offsetLeft - (track.clientWidth - s.offsetWidth)/2;
      try { track.scrollTo({left:left, behavior:(instant||motionOff())?'auto':'smooth'}); } catch(e){ track.scrollLeft=left; }
      setActive(i);
    };
    function nearest(){
      var c = track.scrollLeft + track.clientWidth/2, best=0, bd=1e9;
      slides.forEach(function(s,k){ var d=Math.abs(s.offsetLeft+s.offsetWidth/2-c); if(d<bd){bd=d;best=k;} });
      return best;
    }
    track.addEventListener('scroll', function(){
      if(ticking) return; ticking=true;
      requestAnimationFrame(function(){ ticking=false; var n=nearest(); if(n!==active) setActive(n); });
    }, {passive:true});
    root.addEventListener('click', function(e){
      var d=e.target.closest('[data-dir]'); if(d){ holdUntil=Date.now()+9000; self.go(active + +d.getAttribute('data-dir')); return; }
      var dot=e.target.closest('.nine-dot'); if(dot){ holdUntil=Date.now()+9000; self.go(+dot.getAttribute('data-i')); return; }
      var o=e.target.closest('.nine-open'); if(o){
        var i=+o.getAttribute('data-i');
        if(i!==active){ holdUntil=Date.now()+9000; self.go(i); return; }
        open(i, o);
      }
    });
    track.addEventListener('keydown', function(e){
      if(e.key!=='ArrowRight' && e.key!=='ArrowLeft') return;
      e.preventDefault(); holdUntil=Date.now()+9000;
      self.go(active + (e.key==='ArrowRight'?1:-1));
      var b=slides[active].querySelector('.nine-open'); if(b) b.focus({preventScroll:true});
    });
    track.addEventListener('focusin', function(e){
      var o=e.target.closest('.nine-open'); if(o){ var i=+o.getAttribute('data-i'); if(i!==active) self.go(i); }
    });
    root.addEventListener('mouseenter', function(){ hover=true; });
    root.addEventListener('mouseleave', function(){ hover=false; });
    root.addEventListener('focusin', function(){ focusIn=true; });
    root.addEventListener('focusout', function(){ focusIn=false; });
    track.addEventListener('pointerdown', function(){ holdUntil=Date.now()+9000; });
    if('IntersectionObserver' in window){
      new IntersectionObserver(function(en){ visible = en[0].isIntersecting; }, {threshold:.35}).observe(root);
    }
    setInterval(function(){
      if(!visible || hover || focusIn || !modal.hidden || motionOff() || Date.now()<holdUntil) return;
      self.go(active+1);
    }, 3600);
    setActive(0);
    // re-centre once the view becomes visible / on resize
    var ro = window.ResizeObserver ? new ResizeObserver(function(){ self.go(active,true); }) : null;
    if(ro) ro.observe(track);
  }
  document.querySelectorAll('[data-nine-slider]').forEach(function(el){ sliders.push(new Slider(el)); });

  /* ---------- stats table ---------- */
  var body = document.getElementById('statsBody');
  if(body){
    var sortKey='g', sortDir=-1, NUM=['apps','starts','mins','g','a'];
    var val=function(p,k){ return NUM.indexOf(k)>-1 ? p._t[k] : String(p[k]).toLowerCase(); };
    var draw=function(){
      var rows=P.map(function(p,i){return {p:p,i:i};}).sort(function(A,B){
        var a=val(A.p,sortKey), b=val(B.p,sortKey);
        if(a<b) return -sortDir; if(a>b) return sortDir;
        return A.p._t.apps > B.p._t.apps ? -1 : 1;
      });
      body.innerHTML=rows.map(function(r){
        var p=r.p,t=p._t;
        var face=p.photo?'<img src="'+p.photo+'" alt="" width="40" height="50">':'';
        return '<tr><th scope="row"><button type="button" class="st-player" data-open="'+r.i+'">'+face+'<span><span class="st-name">'+esc(p.name)+'</span><span class="st-sub">#'+esc(p.jersey)+' · '+esc(p.pos)+'</span></span></button></th>'+
          '<td><span class="st-pos">'+p.short+'</span></td><td>'+esc(p.club)+'</td>'+
          '<td class="num">'+t.apps+'</td><td class="num">'+((t.sp&&!t.starts)?'–':fmt(t.starts,t.sp))+'</td><td class="num">'+fmt(t.mins,t.mp)+'</td>'+
          '<td class="num'+(t.g>0?' st-g':'')+'">'+t.g+'</td><td class="num">'+t.a+'</td></tr>';
      }).join('');
      document.querySelectorAll('#statsTable thead th').forEach(function(th){
        if(th.getAttribute('data-key')===sortKey) th.setAttribute('aria-sort', sortDir>0?'ascending':'descending'); else th.removeAttribute('aria-sort');
      });
    };
    document.querySelectorAll('#statsTable thead th button').forEach(function(b){
      b.addEventListener('click', function(){
        var k=b.parentNode.getAttribute('data-key');
        if(k===sortKey) sortDir=-sortDir; else { sortKey=k; sortDir=NUM.indexOf(k)>-1?-1:1; }
        draw();
      });
    });
    body.addEventListener('click', function(e){ var b=e.target.closest('[data-open]'); if(b) open(+b.getAttribute('data-open'), b); });
    draw();
  }

  /* ---------- collab counter ---------- */
  document.querySelectorAll('.collab-count').forEach(function(el){
    var to=+el.getAttribute('data-to'), done=false;
    if(!('IntersectionObserver' in window)) return;
    new IntersectionObserver(function(en){
      if(done || !en[0].isIntersecting) return; done=true;
      if(motionOff()) return;
      var t0=performance.now();
      (function f(now){ var k=Math.min(1,(now-t0)/1600); el.textContent=Math.round(to*(1-Math.pow(1-k,3))); if(k<1) requestAnimationFrame(f); })(t0);
    }, {threshold:.5}).observe(el);
  });
})();
