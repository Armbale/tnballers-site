import re
s = open('work2.html').read()
P = lambda f: open('parts/'+f).read()
def rep(old, new, count=1):
    global s
    n = s.count(old)
    assert n >= 1, 'MISSING: ' + old[:100]
    if count == 1: assert n == 1, 'NOT UNIQUE (%d): %s' % (n, old[:100])
    s = s.replace(old, new) if count != 1 else s.replace(old, new, 1)
def drop(start, end_incl):
    global s
    i = s.index(start); j = s.index(end_incl, i) + len(end_incl)
    s = s[:i] + s[j:]

# image table first
rep('<script>\n/* PRELOADER */', "<script>\n/* HEADSHOTS (compressed, embedded) */\nvar IMG = {bibishkov:'{{IMG:bibishkov}}',ciccarelli:'{{IMG:ciccarelli}}',tavernier:'{{IMG:tavernier}}',bruno:'{{IMG:bruno}}',olguin:'{{IMG:olguin}}',keshavarz:'{{IMG:keshavarz}}',greco:'{{IMG:greco}}',campagna:'{{IMG:campagna}}',pavela:'{{IMG:pavela}}'};\n\n/* PRELOADER */")

# remove scroll-spy and both old hover blocks + doc loading bar
drop('/* SIDEBAR ACTIVE SECTION */', '})();\n')
drop('/* XI NODE HOVER TOOLTIPS + GLOW */', '  else init();\n})();\n')
drop('/* ═══ XI NODE HOVER - bounce pop on mouseover ═══ */', '  else init();\n})();\n')
drop('/* ═══ DOC UNIT LOADING BAR ═══ */', '  advanceBar();\n})();\n')

# mobile nav focus handling
rep("function openMobileNav(){var n=document.getElementById('mobileNav');n.classList.add('open');n.setAttribute('aria-hidden','false');document.querySelector('.hamburger').setAttribute('aria-expanded','true');}",
    "function openMobileNav(){var n=document.getElementById('mobileNav');n.classList.add('open');document.querySelector('.hamburger').setAttribute('aria-expanded','true');var f=n.querySelector('a');if(f)f.focus();}")
rep("function closeMobileNav(){var n=document.getElementById('mobileNav');n.classList.remove('open');n.setAttribute('aria-hidden','true');document.querySelector('.hamburger').setAttribute('aria-expanded','false');}",
    "function closeMobileNav(){var n=document.getElementById('mobileNav');if(!n.classList.contains('open'))return;n.classList.remove('open');var h=document.querySelector('.hamburger');h.setAttribute('aria-expanded','false');if(n.contains(document.activeElement))h.focus();}")

# cursor hover: delegate so dynamic elements (table, player cards) also enlarge the cursor
rep("""  document.querySelectorAll('a,button,.city-node,.apparel-feature,.partner-card,.countup-block,.social-card,.partner-logo-block,.cs-card,.dossier-panel,.file-drop-zone').forEach(function(el){
    el.addEventListener('mouseenter',function(){ball.classList.add('hovered');aura.classList.add('hovered');});
    el.addEventListener('mouseleave',function(){ball.classList.remove('hovered');aura.classList.remove('hovered');});
  });""",
"""  var HOV='a,button,label,.city-node,.partner-card,.countup-block,.social-card,.cs-card,.dossier-panel,.file-drop-zone,.xi-node,.scout-card,.xi-season div,.ambassador-card-reveal';
  document.addEventListener('mouseover',function(e){var on=!!(e.target.closest&&e.target.closest(HOV));ball.classList.toggle('hovered',on);aura.classList.toggle('hovered',on);},{passive:true});""")

# countups
rep("var configs={'monthly':{from:1,to:20,suffix:'M+'},'reach':{from:50,to:500,suffix:'K+'},'units':{from:0,to:3,suffix:''},'canadian':{from:0,to:100,suffix:'%'},'partners':{from:0,to:4,suffix:''},'year':{from:2020,to:2026,suffix:''}};",
    "var configs={'monthly':{from:1,to:20,suffix:'M+'},'reach':{from:50,to:500,suffix:'K+'},'xi':{from:0,to:8,suffix:''},'canadian':{from:0,to:100,suffix:'%'},'clubs':{from:0,to:5,suffix:''},'year':{from:2020,to:2026,suffix:''}};")
rep("setTimeout(function(){countTo(document.getElementById('credPartners'),0,4,'',1400);},600);",
    "setTimeout(function(){countTo(document.getElementById('credXI'),0,8,'',1400);},600);")

# spark trail respects pause
rep("if(Math.random()<0.35) sparks.push(", "if(!document.body.classList.contains('motion-paused') && Math.random()<0.35) sparks.push(")

# ---------- FORM ----------
i = s.index('/* FORM */'); j = s.index('/* ══════════════════════════════════════════\n   STARTING XI - INTERACTIVE LOGIC')
s = s[:i] + r"""/* FORM */
var EMAIL_RE=/^[^@\s]+@[^@\s]+\.[^@\s]+$/;
function fieldErr(el,bad){ if(bad) el.setAttribute('aria-invalid','true'); else el.removeAttribute('aria-invalid'); return bad; }
function showErr(id,msgs){ var box=document.getElementById(id); if(!msgs.length){box.hidden=true;box.textContent='';return;} box.hidden=false; box.textContent='Please fix: '+msgs.join(' · '); }
(function(){
  document.querySelectorAll('input[name="age-group"]').forEach(function(r){
    r.addEventListener('change',function(){ var minor=r.checked && r.value!=='18+'; var w=document.getElementById('guardianWrap'); var g=document.getElementById('guardian-email'); w.hidden=!minor; g.required=minor; if(!minor) g.removeAttribute('aria-invalid'); });
  });
})();
function nextFormStep(){
  var msgs=[], first=null;
  function chk(el,bad,msg){ if(fieldErr(el,bad)){ msgs.push(msg); if(!first) first=el; } }
  chk(document.getElementById('first-name'),!document.getElementById('first-name').value.trim(),'first name');
  chk(document.getElementById('last-name'),!document.getElementById('last-name').value.trim(),'last name');
  chk(document.getElementById('email'),!EMAIL_RE.test(document.getElementById('email').value.trim()),'a valid email');
  chk(document.getElementById('position'),!document.getElementById('position').value,'position');
  var age=document.querySelector('input[name="age-group"]:checked');
  if(!age){ msgs.push('your age'); if(!first) first=document.querySelector('input[name="age-group"]'); }
  if(age && age.value!=='18+'){ var g=document.getElementById('guardian-email'); chk(g,!EMAIL_RE.test(g.value.trim()),'parent or guardian email'); }
  chk(document.getElementById('about'),!document.getElementById('about').value.trim(),'a few words about you');
  showErr('step1Error',msgs);
  if(msgs.length){ first.focus(); return; }
  document.getElementById('formStep1').classList.remove('active');
  document.getElementById('formStep2').classList.add('active');
  document.getElementById('step2-title').focus();
}
function prevFormStep(){document.getElementById('formStep2').classList.remove('active');document.getElementById('formStep1').classList.add('active');document.getElementById('first-name').focus();}
function updateFileName(input){
  var ft=document.getElementById('fileText');
  if(input.files&&input.files.length>0){
    var f=input.files[0];
    if(f.size>8*1024*1024){ input.value=''; ft.textContent='That file is over 8MB. Paste a link instead.'; ft.style.color='var(--c-red)'; return; }
    ft.textContent=f.name; ft.style.color='var(--c-red)';
  } else { ft.textContent='Drag & Drop MP4/MOV'; ft.style.color=''; }
}
(function(){
  var dropZone=document.getElementById('dropZone');if(!dropZone)return;
  ['dragenter','dragover'].forEach(function(ev){dropZone.addEventListener(ev,function(){dropZone.classList.add('dragover');},false);});
  ['dragleave','drop'].forEach(function(ev){dropZone.addEventListener(ev,function(){dropZone.classList.remove('dragover');},false);});
})();
(function(){
  var form=document.getElementById('recruitForm'); if(!form) return;
  form.addEventListener('submit',function(e){
    e.preventDefault();
    var msgs=[], first=null;
    var file=document.getElementById('raw-footage'), link=document.getElementById('footage-link'), consent=document.getElementById('consent');
    var hasFile=file.files&&file.files.length>0, linkVal=link.value.trim();
    if(!hasFile && !linkVal){ msgs.push('add a clip or a link'); fieldErr(link,true); first=link; }
    else if(linkVal && !/^https?:\/\/\S+\.\S+/.test(linkVal)){ msgs.push('a full link starting with https://'); fieldErr(link,true); first=link; }
    else fieldErr(link,false);
    if(!consent.checked){ msgs.push('tick the consent box'); if(!first) first=consent; }
    showErr('step2Error',msgs);
    if(msgs.length){ first.focus(); return; }
    var btn=document.getElementById('submitBtn'); btn.disabled=true; btn.textContent='Sending…';
    fetch('/',{method:'POST',body:new FormData(form)})
      .then(function(r){ if(!r.ok) throw new Error(r.status);
        btn.textContent='Profile Submitted ✓'; btn.style.background='#16703A';
        var ok=document.getElementById('formSuccess'); ok.hidden=false; ok.textContent='Thanks, your profile is in. We review every submission personally and will be in touch if it\'s a fit.'; })
      .catch(function(){ btn.disabled=false; btn.textContent='Submit Profile';
        showErr('step2Error',['something went wrong sending it. Try again or email contact@tnballers.com']); });
  });
})();

""" + s[j:]

# ---------- XI DATA ----------
i = s.index('  var xiPlayers = ['); j = s.index('  var xiCoords = [')
s = s[:i] + P('xi_data.js') + s[j:]
rep("    [230,545]\n  ];", "    [230,545]\n  ];\n  window.xiPlayers = xiPlayers;\n\n  function seasonHTML(p){\n    var s=p.season; if(!s) return '';\n    var gk=p.short==='GK';\n    var cells = gk ? [['Apps',s.apps],['Mins',s.mins.toLocaleString('en-CA')],['Saves',s.saves,1],['Conceded',s.ga],['Clean Sh.',s.cs]]\n                   : [['Apps',s.apps],['Starts',s.starts],['Mins',s.mins.toLocaleString('en-CA')],['Goals',s.g,1],['Assists',s.a,1]];\n    return '<div class=\"xi-info-club-label\">2026 Season · '+s.comp+'</div>'+\n      '<div class=\"xi-season\">'+cells.map(function(c){return '<div><b'+(c[2]&&c[1]>0?' class=\"hl\"':'')+'>'+c[1]+'</b><span>'+c[0]+'</span></div>';}).join('')+'</div>'+\n      (p.extra?'<p class=\"xi-season-extra\">'+p.extra+'</p>':'')+\n      '<p class=\"xi-season-src\">As of 15 Oct 2026</p><div class=\"xi-info-divider\"></div>';\n  }")

# entrance animation: short, and cleared afterwards so hover can take over
i = s.index('  // Cinematic staggered entrance'); j = s.index('    io.observe(shell);\n  })();', i) + len('    io.observe(shell);\n  })();')
s = s[:i] + """  // Staggered entrance when the pitch appears. Animation is cleared afterwards
  // so it can't lock the node's transform/filter (this is what blocked hover before).
  (function(){
    var shell = document.querySelector('.xi-shell');
    if(!shell) return;
    var nodes = document.querySelectorAll('#xiSvg .xi-node');
    if(window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;
    var fired = false;
    nodes.forEach(function(n){ n.style.opacity = '0'; });
    var io = new IntersectionObserver(function(entries){
      entries.forEach(function(e){
        if(e.isIntersecting && !fired){
          fired = true; io.disconnect();
          nodes.forEach(function(node, i){
            setTimeout(function(){
              node.style.opacity = '';
              node.style.animation = 'xiNodeIn 0.6s cubic-bezier(0.34,1.56,0.64,1) both';
              node.addEventListener('animationend', function done(){ node.style.animation=''; node.removeEventListener('animationend', done); });
            }, 250 + i * 90);
          });
        }
      });
    }, {threshold: 0.15});
    io.observe(shell);
  })();"""  + s[j:]

# expose helpers
rep("  var xiCurrent = -1;\n  var xiLinesOn = true;", "  var xiCurrent = -1;\n  var xiLinesOn = true;\n  window.xiCurrentIdx = function(){ return xiCurrent; };\n  window.xiOpen = function(i){ if(xiCurrent !== i) window.xiSelect(i); };")
rep("    btn.classList.toggle('on', xiLinesOn);\n  };", "    btn.classList.toggle('on', xiLinesOn);\n    btn.setAttribute('aria-pressed', String(xiLinesOn));\n  };")
# closing returns focus to the node
rep("""      ring.setAttribute('opacity','0');
      xiCurrent = -1;
      return;""", """      ring.setAttribute('opacity','0');
      if(panel.contains(document.activeElement)){ var nd=document.querySelector('#xiSvg .xi-node[data-idx="'+idx+'"]'); if(nd) nd.focus(); }
      xiCurrent = -1;
      return;""")
rep("""'<button class="xi-info-close" onclick="xiSelect('+idx+')">✕</button>'""", """'<button class="xi-info-close" type="button" aria-label="Close player card" onclick="xiSelect('+idx+')">✕</button>'""", count=0)

# contention branch: blue accent + club + season
ci = s.index("    // ── IN CONTENTION (amber treatment) ──"); cj = s.index("    // ── POSSIBLE ──", ci)
cont = s[ci:cj]
cont = cont.replace('rgba(201,162,39,0.75)','#3C8BDB').replace('rgba(201,162,39,0.9)','#1C5DA6').replace('var(--c-gold)','#1C5DA6').replace('rgba(201,162,39,0.1)','#E4EEF9').replace('rgba(201,162,39,0.4)','rgba(28,93,166,0.4)').replace('rgba(201,162,39,0.2)','#E4EEF9').replace('rgba(201,162,39,0.35)','rgba(28,93,166,0.35)')
cont = cont.replace("""        '<div class="xi-info-club-label">Stats Profile</div>'+""", """        '<div class="xi-info-club-label">Club</div>'+
        '<div class="xi-info-club">'+p.club+'</div>'+
        '<div class="xi-info-divider"></div>'+
        seasonHTML(p)+
        '<div class="xi-info-club-label">TNB Scout Ratings</div>'+""")
cont = cont.replace("'<div class=\"xi-info-photo\" style=\"background:#E4EEF9;border-color:rgba(28,93,166,0.4);color:#1C5DA6\">'+p.initials+'</div>'", "'<div class=\"xi-info-photo\" style=\"background:#E4EEF9;border-color:rgba(28,93,166,0.4);color:#1C5DA6\">'+p.initials+'</div>'")
cont = cont.replace("'<div class=\"xi-info-name\" style=\"font-size:1.4rem;line-height:0.95;margin-top:4px\">'+nameParts2[0]+'<br>'+nameParts2.slice(1).join(' ')+'</div>'+\n          '</div>'+",
                    "'<div class=\"xi-info-name\" style=\"font-size:1.4rem;line-height:0.95;margin-top:4px\">'+nameParts2[0]+'<br>'+nameParts2.slice(1).join(' ')+'</div>'+\n          '</div>'+\n          '<div class=\"xi-info-jersey\" style=\"margin-bottom:0;flex-shrink:0;background:#E4EEF9;border-color:#1C5DA6;color:#1C5DA6\">'+p.jersey+'</div>'+")
assert 'seasonHTML(p)' in cont
s = s[:ci] + cont + s[cj:]

# confirmed branch: season block + ratings label + alt + agency
rep("""      '<div class="xi-info-club-label">Stats</div>'+""", """      seasonHTML(p)+
      '<div class="xi-info-club-label">TNB Scout Ratings</div>'+""")
rep("""<img src="'+p.photo+'" alt="'+p.name+'" style=""", """<img src="'+p.photo+'" alt="'+(p.alt||p.name)+'" style=""")
rep("""(p.agency ? '<div style="font-family:var(--f-condensed);font-size:.52rem;letter-spacing:2.5px;font-weight:700;color:rgba(18,18,18,0.68);text-transform:uppercase;margin-top:5px">🤝 '+p.agency+'</div>' : '')""",
    """(p.agency ? '<div class="xi-agency">🤝 Agency: '+p.agency+'</div>' : '')""")
rep("""class="xi-info-ig" style="margin-top:10px">'+igSvg+' '+p.igHandle+'</a>'""", """class="xi-info-ig" style="margin-top:10px">'+igSvg+' '+p.igHandle+'<span class="visually-hidden"> on Instagram (opens in new tab)</span></a>'""")
rep("""var igSvg = '<svg viewBox="0 0 24 24" style=""", """var igSvg = '<svg aria-hidden="true" viewBox="0 0 24 24" style=""")

# market value
rep("var kval=Math.round(ease*1428);", "var kval=Math.round(ease*2100);")
rep("else{ el.textContent='€1.4M+'; }", "else{ el.textContent='€2.1M+'; }")

# append new logic
rep('</script>\n</body>', P('extra.js') + '\n</script>\n</body>')

# ---------- THE NINE: drop pitch + radar logic, add cards ----------
a = s.index('/* ══════════════════════════════════════════\n   STARTING XI - INTERACTIVE LOGIC')
b = s.index('/* ═══ AMBASSADOR RADAR CANVAS')
c = s.index('/* ═══ IMMERSIVE: CURSOR TRAIL')
s = s[:a] + P('nine_data.js') + '\n' + P('nine.js') + '\n' + P('book.js') + '\n\n' + s[c:]

open('work3.html','w').write(s)
print('script ok')
