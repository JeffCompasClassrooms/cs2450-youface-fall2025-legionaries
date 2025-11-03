// static/js/graffiti.js
(function(){
  const pid = (window.G && window.G.profileId) || 'anonymous';

  const cv = document.getElementById('c');
  if (!cv) return; // profile page only
  const ctx = cv.getContext('2d');

  const toggle   = document.getElementById('toggle');
  const color    = document.getElementById('color');
  const size     = document.getElementById('size');
  const penBtn   = document.getElementById('pen');
  const eraserBtn= document.getElementById('eraser');
  const pushBtn  = document.getElementById('push');
  const clearBtn = document.getElementById('clear');

  let tool = 'pen';
  penBtn?.addEventListener('click', () => tool = 'pen');
  eraserBtn?.addEventListener('click', () => tool = 'eraser');

  // Resize canvas to match container (and scale for devicePixelRatio)
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
    try {
      const res = await fetch(`/api/graffiti/${encodeURIComponent(pid)}`);
      if (res.ok) strokes = await res.json();
      resize();
    } catch(e) { console.warn('graffiti load failed', e); }
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

  // Off by default; enable when checkbox is checked
  cv.style.pointerEvents = 'none';
  toggle?.addEventListener('change', () => {
    cv.style.pointerEvents = toggle.checked ? 'auto' : 'none';
  });

  let drawing = false;
  let pts = [];

  function getPos(e){
    const r = cv.getBoundingClientRect();
    // For pointer events ensure we use clientX/clientY.
    return {x: e.clientX - r.left, y: e.clientY - r.top};
  }

  cv.addEventListener('pointerdown', e => {
    if (!toggle?.checked) return;
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

  pushBtn?.addEventListener('click', async () => {
    if (!pending.length) { alert('Nothing to push. Draw first.'); return; }
    try {
      const res = await fetch(`/api/graffiti/${encodeURIComponent(pid)}/push`, {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({strokes: pending})
      });
      if (!res.ok) { alert('Push failed'); return; }
      pending = [];
      await load();
      alert('Graffiti saved to profile!');
    } catch(e) { alert('Push failed'); }
  });

  clearBtn?.addEventListener('click', async () => {
    if (!confirm('Clear all?')) return;
    try {
      await fetch(`/api/graffiti/${encodeURIComponent(pid)}/clear`, {method:'POST'});
      strokes = [];
      pending = [];
      redraw();
    } catch(e) { console.warn('clear failed', e); }
  });

  load();
})();
