// Hodl my b page-turn: arrows, swipe, buttons, #p<n>. No JS or reduced motion = pages stacked.
(function(){
  var mag=document.querySelector('.mag');if(!mag)return;
  if(matchMedia('(prefers-reduced-motion: reduce)').matches)return;
  var pages=[].slice.call(mag.querySelectorAll('.pg')),bar=document.querySelector('.mag-bar');
  var prev=bar.querySelector('.prev'),next=bar.querySelector('.next'),cnt=bar.querySelector('.cnt'),i=0,busy=false;
  var m=/^#p(\d+)$/.exec(location.hash);if(m)i=Math.min(pages.length-1,Math.max(0,m[1]-1));
  mag.classList.add('on');bar.hidden=false;
  function ui(){pages.forEach(function(p,k){p.classList.toggle('cur',k===i);p.setAttribute('aria-hidden',k===i?'false':'true')});
    cnt.textContent='Page '+(i+1)+' / '+pages.length;prev.disabled=i===0;next.disabled=i===pages.length-1;
    history.replaceState(null,'','#p'+(i+1));}
  function go(d){var n=i+d;if(busy||n<0||n>=pages.length)return;busy=true;
    var o=pages[i],nw=pages[n],oc=d>0?'outN':'outP',ic=d>0?'inN':'inP';
    o.classList.add(oc);setTimeout(function(){o.classList.remove(oc);i=n;ui();nw.classList.add(ic);
      var t=bar.getBoundingClientRect().top;if(t<0)bar.scrollIntoView();
      setTimeout(function(){nw.classList.remove(ic);busy=false},400)},380);}
  prev.onclick=function(){go(-1)};next.onclick=function(){go(1)};
  addEventListener('keydown',function(e){if(e.target.closest&&e.target.closest('input,textarea'))return;
    if(e.key==='ArrowRight')go(1);else if(e.key==='ArrowLeft')go(-1)});
  var x0=null,y0=0;mag.addEventListener('touchstart',function(e){x0=e.touches[0].clientX;y0=e.touches[0].clientY},{passive:true});
  mag.addEventListener('touchend',function(e){if(x0===null)return;var dx=e.changedTouches[0].clientX-x0,dy=e.changedTouches[0].clientY-y0;x0=null;
    if(Math.abs(dx)>50&&Math.abs(dx)>Math.abs(dy)*1.5)go(dx<0?1:-1)},{passive:true});
  ui();
})();
