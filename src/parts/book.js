
/* ══════════════════════════════════════════
   BOOK A SHOOT form (Netlify Forms)
   ══════════════════════════════════════════ */
(function(){
  var f=document.getElementById('bookForm'); if(!f) return;
  var err=document.getElementById('bookError'), ok=document.getElementById('bookSuccess'), btn=document.getElementById('bookSubmit');
  var RE=/^[^@\s]+@[^@\s]+\.[^@\s]+$/;
  function mark(el,bad){ if(bad) el.setAttribute('aria-invalid','true'); else el.removeAttribute('aria-invalid'); return bad; }
  f.addEventListener('submit', function(e){
    e.preventDefault();
    var miss=[], first=null;
    function need(id,label,test){ var el=document.getElementById(id); var bad=mark(el,!test(el)); if(bad){ miss.push(label); if(!first) first=el; } }
    need('b-name','your name',function(el){return el.value.trim().length>1;});
    need('b-email','a valid email',function(el){return RE.test(el.value.trim());});
    need('b-who','who you are',function(el){return !!el.value;});
    need('b-loc','a location',function(el){return el.value.trim().length>1;});
    need('b-details','a few details',function(el){return el.value.trim().length>4;});
    var svc=f.querySelectorAll('input[name="service"]:checked').length;
    if(!svc){ miss.push('what you need'); if(!first) first=f.querySelector('input[name="service"]'); }
    var c=document.getElementById('b-consent'); if(!c.checked){ miss.push('privacy consent'); if(!first) first=c; }
    if(miss.length){ err.hidden=false; err.textContent='Please add: '+miss.join(' · '); ok.hidden=true; if(first) first.focus(); return; }
    err.hidden=true; btn.disabled=true; btn.textContent='Sending...';
    var data=new URLSearchParams(new FormData(f)).toString();
    fetch('/', {method:'POST', headers:{'Content-Type':'application/x-www-form-urlencoded'}, body:data})
      .then(function(r){ if(!r.ok) throw new Error(r.status); ok.hidden=false; ok.textContent='Thanks! Your request is in. We\'ll reply within two working days.'; f.reset(); })
      .catch(function(){ err.hidden=false; err.innerHTML='That didn\'t send. Please email <a href="mailto:contact@tnballers.com?subject=Videography%20enquiry">contact@tnballers.com</a> instead.'; })
      .then(function(){ btn.disabled=false; btn.textContent='Send Request'; });
  });
})();
