document.addEventListener('DOMContentLoaded',()=>{
  const display = document.getElementById('display');
  const keys = document.querySelectorAll('.keys button');
  const clearBtn = document.getElementById('clear');
  const backBtn = document.getElementById('back');
  const equalsBtn = document.getElementById('equals');

  function update(v){
    display.value = v;
  }

  keys.forEach(k=>{
    k.addEventListener('click',()=>{
      const v = k.dataset.value;
      if(!v) return;
      display.value = (display.value==='0' || display.value==='') ? v : (display.value + v);
    });
  });

  clearBtn.addEventListener('click',()=>{ display.value = '' });
  backBtn.addEventListener('click',()=>{ display.value = display.value.slice(0,-1) });

  async function evaluate(){
    let expr = display.value || '';
    expr = expr.replace(/÷/g,'/').replace(/×/g,'*').replace(/\^/g,'**');
    try{
      const res = await fetch('/api/calc',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({expression:expr})});
      const data = await res.json();
      if(!res.ok) throw data;
      update(String(data.result));
    }catch(err){
      const msg = (err && err.detail) ? err.detail : 'Invalid expression';
      alert(msg);
    }
  }

  equalsBtn.addEventListener('click',evaluate);
  document.addEventListener('keydown',(e)=>{
    if(e.key==='Enter'){ e.preventDefault(); evaluate(); }
    else if(e.key==='Backspace'){ display.value = display.value.slice(0,-1) }
    else if(e.key==='Escape'){ display.value = '' }
    else if(/^[0-9+\-*/().%]$/.test(e.key)){ display.value += e.key }
    else if(e.key==='^'){ display.value += '^' }
  });
});
