(function(){
    const pid = window.G.profileId;
    const cv = document.getElementById('c');
    const ctx = cv.getContext('2d');
  
    const toggle = document.getElementById('toggle');
    const color = document.getElementById('color');
    const size = document.getElementById('size');
    const penBtn = document.getElementById('pen');
    const eraserBtn = document.getElementById('eraser');
    const pushBtn = document.getElementById('push');
    const clearBtn = document.getElementById('clear');
  
    let tool = 'pen';
    penBtn.onclick = () => tool = 'pen';
    eraserBtn.onclick = () => tool = 'eraser';
  
    // Resize canvas to match container
    function resize(){
      const r = cv.getBoundingClientRect();
      const d = window.devicePixelRatio || 1;
      cv.width = r.width * d;
      cv.height = r.height * d;
      ctx.setTransform(d,0,0,d,0,0);
      redraw();
    }
    window.addEventListener('resize', resize);
  
    let strokes = [];
    let pending = [];
  
    async function load(){
      const res = await fetch(`/api/graffiti/${pid}`);
      strokes = await res.json();
      resize();
    }
  
    function drawStroke(s){
      ctx.lineJoin = 'round';
      ctx.lineCap = 'round';
      ctx.lineWidth = s.size;
      if (s.tool === 'eraser') {
        ctx.globalCompositeOperation = 'destination-out';
        ctx.strokeStyle = 'rgba(0,0,0,1)';
      } else {
        ctx.globalCompositeOperation = 'source-over';
        ctx.strokeStyle = s.color;
      }
      ctx.beginPath();
      s.points.forEach((p, i) => i ? ctx.lineTo(p.x, p.y) : ctx.moveTo(p.x, p.y));
      ctx.stroke();
      ctx.globalCompositeOperation = 'source-over';
    }
  
    function redraw(){
      const r = cv.getBoundingClientRect();
      ctx.clearRect(0, 0, r.width, r.height);
      strokes.forEach(drawStroke);
    }
  
    cv.style.pointerEvents = 'none';
    toggle.addEventListener('change', () => {
      cv.style.pointerEvents = toggle.checked ? 'auto' : 'none';
    });
  
    let drawing = false;
    let pts = [];
  
    function getPos(e){
      const r = cv.getBoundingClientRect();
      return {x: e.clientX - r.left, y: e.clientY - r.top};
    }
  
    cv.addEventListener('pointerdown', e => {
      if (!toggle.checked) return;
      drawing = true;
      pts = [getPos(e)];
    });
  
    cv.addEventListener('pointermove', e => {
      if (!drawing) return;
      pts.push(getPos(e));
      redraw();
      drawStroke({points: pts, color: color.value, size: +size.value, tool});
    });
  
    function endDraw(){
      if (!drawing || pts.length < 2) {
        drawing = false;
        return;
      }
      drawing = false;
      const stroke = {points: pts, color: color.value, size: +size.value, tool};
      strokes.push(stroke);
      pending.push(stroke);
      redraw();
      pts = [];
    }
  
    cv.addEventListener('pointerup', endDraw);
    cv.addEventListener('pointerleave', endDraw);
  
    pushBtn.addEventListener('click', async () => {
      if (!pending.length) {
        alert('Nothing to push.');
        return;
      }
      const res = await fetch(`/api/graffiti/${pid}/push`, {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({strokes: pending})
      });
      if (!res.ok) {
        alert('Push failed');
        return;
      }
      pending = [];
      await load();
    });
  
    clearBtn.addEventListener('click', async () => {
      if (!confirm('Clear all?')) return;
      await fetch(`/api/graffiti/${pid}/clear`, {method:'POST'});
      strokes = [];
      pending = [];
      redraw();
    });
  
    load();
  })();
  