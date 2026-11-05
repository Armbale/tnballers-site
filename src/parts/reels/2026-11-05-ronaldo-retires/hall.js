// Shared "hall of fame" scene: perspective corridor, framed photos, skylight beam, gold dust. k = seconds into scene.
function hall(k,H,IMG,{push=0,hero='ronaldo.png',heroH=1150,heroTop=null,dim=1}={}){
  const cl=(x,a=0,b=1)=>Math.max(a,Math.min(b,x));
  const P=['cr_154.jpg','cr_097.jpg','cr_087.jpg','cr_070.jpg','cr_097.jpg','cr_154.jpg'];
  const z=1+push;let h=`<div style="position:absolute;inset:0;overflow:hidden;background:radial-gradient(ellipse 60% 45% at 50% 30%,#3a2a12 0%,#120c06 55%,#050403 100%);transform:scale(${z});transform-origin:50% 40%">`;
  // floor reflection + walls
  h+=`<div style="position:absolute;left:0;right:0;bottom:0;height:${H*0.36}px;background:linear-gradient(#1a130b,#050403);"></div>`;
  h+=`<div style="position:absolute;left:0;right:0;bottom:${H*0.36-4}px;height:4px;background:linear-gradient(90deg,transparent,#c9a24a55,transparent)"></div>`;
  [[-1,'left'],[1,'right']].forEach(([s,side])=>{
    h+=`<div style="position:absolute;top:0;${side}:0;width:380px;height:${H}px;perspective:900px"><div style="position:absolute;inset:0;transform-origin:${side==='left'?'left':'right'} center;transform:rotateY(${s*-58}deg);background:linear-gradient(${side==='left'?90:270}deg,#2a1d0e,#100b06);">`;
    for(let i=0;i<3;i++){const src=P[(side==='left'?0:3)+i];const y=H*0.16+i*H*0.22;
      h+=`<div style="position:absolute;${side}:${40+i*10}px;top:${y}px;width:300px;height:${H*0.17}px;border:10px solid #b8913f;outline:3px solid #6b4f1c;box-shadow:0 0 30px #000,inset 0 0 20px #000;overflow:hidden"><img src="${IMG}${src}" style="width:100%;height:100%;object-fit:cover;filter:sepia(.25) brightness(.85)"></div>`;
      h+=`<div style="position:absolute;${side}:${120+i*10}px;top:${y-16}px;width:140px;height:14px;background:radial-gradient(#ffe7a0,transparent 70%)"></div>`}
    h+=`</div></div>`});
  // back wall arch + skylight beam
  h+=`<div style="position:absolute;left:300px;right:300px;top:${H*0.08}px;height:${H*0.56}px;background:linear-gradient(#2c2010,#16100a);border:6px solid #6b4f1c;border-radius:240px 240px 0 0;box-shadow:inset 0 0 80px #000"></div>`;
  h+=`<div style="position:absolute;left:390px;width:300px;top:-100px;height:${H*0.9}px;background:linear-gradient(#fff4d0cc,#ffd98a33 60%,transparent);filter:blur(28px);opacity:${0.75+0.1*Math.sin(k*2)}"></div>`;
  h+=`<div style="position:absolute;left:0;right:0;top:${H*0.1}px;text-align:center;font-family:Tanker;font-size:${H*0.45}px;line-height:1;color:#d8b25a22;-webkit-text-stroke:3px #d8b25a55">7</div>`;
  // dust
  for(let i=0;i<50;i++){const r=((i*9301+49297)%233280)/233280,r2=((i*4241+1013)%9973)/9973;const x=380+r*320+Math.sin(k*.6+i)*30;const y=(H*0.9)-((k*(20+r2*40)+i*97)%(H*0.85));h+=`<div style="position:absolute;left:${x}px;top:${y}px;width:${2+r*4}px;height:${2+r*4}px;border-radius:50%;background:#ffe9b0;opacity:${.3+.6*r2};box-shadow:0 0 8px #ffd98a"></div>`}
  // hero
  if(hero){const top=heroTop??(H-heroH);h+=`<img src="${IMG}${hero}" style="position:absolute;left:50%;top:${top}px;height:${heroH}px;transform:translateX(-50%);filter:drop-shadow(0 0 40px #ffd98a55) drop-shadow(0 40px 60px #000) brightness(${dim});-webkit-mask-image:linear-gradient(#000 80%,transparent 99%)">`;
    h+=`<div style="position:absolute;left:50%;top:${top}px;height:${heroH}px;width:900px;transform:translateX(-50%);background:radial-gradient(ellipse 40% 30% at 50% 10%,#ffe7a033,transparent 70%);mix-blend-mode:screen"></div>`}
  return h+`<div style="position:absolute;inset:0;background:radial-gradient(ellipse 80% 70% at 50% 45%,transparent 50%,#000c 100%)"></div></div>`;
}
