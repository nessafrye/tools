#!/usr/bin/env python3
"""
Build script: reads SVG + fonts, outputs productboard-thumbnail-generator.html.
Uses placeholder substitution instead of f-strings to avoid escaping issues.
"""
import base64
import pathlib

ROOT          = pathlib.Path(__file__).parent
ARTIFACTS     = ROOT / "Artifacts"
FONT_PATH     = ARTIFACTS / "Aeonik+Aeonik Mono WOFF2" / "AeonikVF-Regular.woff2"
FONT_MONO_PATH= ARTIFACTS / "Aeonik+Aeonik Mono WOFF2" / "AeonikMonoVF-Regular.woff2"
SVG_PATH      = ARTIFACTS / "Streamline Productboard Thumbnail.svg"
OUT_PATH      = ROOT / "productboard-thumbnail-generator.html"

font_b64      = base64.b64encode(FONT_PATH.read_bytes()).decode("ascii")
font_mono_b64 = base64.b64encode(FONT_MONO_PATH.read_bytes()).decode("ascii")
svg_raw       = SVG_PATH.read_text(encoding="utf-8")

# Inject id onto root <svg> so JS can reference it
svg_inline = svg_raw.replace('<svg ', '<svg id="thumbnail-svg" ', 1)

# ── HTML template ───────────────────────────────────────────────────────────
# Placeholders: @@FONT_B64@@, @@FONT_MONO_B64@@, @@SVG_INLINE@@
HTML = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Productboard Thumbnail Generator</title>
<style>
/* ── Brand tokens ───────────────────────────────────────────────────────── */
:root {
  --rosa-1:#FEF2FF; --rosa-2:#F9C5FF; --rosa-3:#F49AFF;
  --rosa-4:#E23EF7; --rosa-5:#8D1395; --rosa-6:#65366B;
  --banana-1:#FEFAEC; --banana-2:#F6E591; --banana-3:#F1D053;
  --banana-4:#E79F19; --banana-5:#CC7B13; --banana-6:#8A4516;
  --blue-1:#EFF8FF; --blue-2:#B8E2FF; --blue-3:#26ACFF;
  --blue-4:#0077CE; --blue-5:#02508A; --blue-6:#062A4B;
  --carrot-1:#FFF8ED; --carrot-2:#FFDCA8; --carrot-3:#FF982E;
  --carrot-4:#EF6407; --carrot-5:#9D3B0F; --carrot-6:#441706;
  --emerald-1:#F1FCF8; --emerald-2:#C7F5E7; --emerald-3:#89E1C9;
  --emerald-4:#27A588; --emerald-5:#1B6A5B; --emerald-6:#1A473F;
  --pomegranate-1:#FEF4F2; --pomegranate-2:#FDD3CB; --pomegranate-3:#EB5639;
  --pomegranate-4:#D94629; --pomegranate-5:#97311D; --pomegranate-6:#44140B;
  --black-1:#F8F8F8; --black-2:#ECECEC; --black-3:#BDBDBD;
  --black-4:#7C7C7C; --black-5:#464646; --black-6:#000000;

  /* Page-level semantics */
  --bg:             #0d0d0d;
  --panel-bg:       #1a1a1a;
  --border:         rgba(255,255,255,0.10);
  --border-hover:   rgba(255,255,255,0.22);
  --text-primary:   #f0f0f0;
  --text-secondary: rgba(240,240,240,0.45);
  --accent:         var(--banana-3);
  --accent-dark:    var(--banana-4);
  --eyebrow:        var(--blue-3);
}

/* ── Fonts ──────────────────────────────────────────────────────────────── */
@font-face {
  font-family: 'Aeonik VF';
  src: url('data:font/woff2;base64,@@FONT_B64@@') format('woff2');
  font-weight: 100 900;
  font-style: normal;
}
@font-face {
  font-family: 'Aeonik';
  src: url('data:font/woff2;base64,@@FONT_B64@@') format('woff2');
  font-weight: 100 900;
  font-style: normal;
}
@font-face {
  font-family: 'Aeonik Mono';
  src: url('data:font/woff2;base64,@@FONT_MONO_B64@@') format('woff2');
  font-weight: 100 900;
  font-style: normal;
}

/* ── Base ───────────────────────────────────────────────────────────────── */
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
html, body { height: 100%; }
body {
  font-family: 'Aeonik VF', 'Aeonik', system-ui, sans-serif;
  background: var(--bg);
  color: var(--text-primary);
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

/* ── App shell ──────────────────────────────────────────────────────────── */
.app {
  display: flex;
  flex: 1;
  min-height: 100vh;
}

/* ────────────────────────────────────────────────────────────────────────
   SIDEBAR
──────────────────────────────────────────────────────────────────────── */
.sidebar {
  width: 300px;
  flex-shrink: 0;
  background: var(--panel-bg);
  border-right: 1px solid var(--border);
  display: flex;
  flex-direction: column;
  padding: 28px 24px 24px;
  gap: 0;
}

/* Header */
.sidebar-header {
  padding-bottom: 24px;
}
.sidebar-eyebrow {
  font-size: 11px;
  font-weight: 600;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  color: var(--eyebrow);
  margin-bottom: 6px;
}
.sidebar-title {
  font-size: 22px;
  font-weight: 600;
  color: var(--text-primary);
  line-height: 1.2;
  letter-spacing: -0.01em;
}

.sidebar-divider {
  height: 1px;
  background: var(--border);
  margin: 0 -24px;
}

/* Field sections */
.sidebar-body {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 24px;
  padding-top: 24px;
}

.field-block {
  display: flex;
  flex-direction: column;
  gap: 0;
}

.field-label {
  font-size: 13px;
  font-weight: 500;
  color: var(--text-primary);
  margin-bottom: 10px;
}

/* Textarea */
.field-block textarea {
  font-family: 'Aeonik VF', 'Aeonik', system-ui, sans-serif;
  font-size: 15px;
  line-height: 1.55;
  color: var(--text-primary);
  background: rgba(255,255,255,0.06);
  border: 1px solid var(--border);
  border-radius: 10px;
  padding: 12px 14px;
  resize: none;
  width: 100%;
  min-height: 120px;
  outline: none;
  transition: border-color 0.15s, background 0.15s;
  caret-color: var(--accent);
}
.field-block textarea:focus {
  border-color: var(--border-hover);
  background: rgba(255,255,255,0.09);
}

/* Mono helper text */
.field-hint {
  font-family: 'Aeonik Mono', 'Courier New', monospace;
  font-size: 11.5px;
  color: var(--text-secondary);
  margin-top: 10px;
  letter-spacing: 0.01em;
}

/* Font size row */
.fontsize-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
}
.fontsize-label {
  font-size: 13px;
  font-weight: 500;
  color: var(--text-primary);
}
.fontsize-pill {
  font-family: 'Aeonik Mono', 'Courier New', monospace;
  font-size: 12px;
  font-weight: 500;
  background: rgba(255,255,255,0.08);
  color: var(--text-primary);
  border: 1px solid var(--border);
  border-radius: 99px;
  padding: 4px 12px;
  transition: background 0.2s, color 0.2s, border-color 0.2s;
}
.fontsize-pill.shrunk {
  background: rgba(255,152,46,0.12);
  color: var(--carrot-3);
  border-color: rgba(255,152,46,0.30);
}

/* Sidebar footer */
.sidebar-footer {
  padding-top: 20px;
}
.btn-reset {
  font-family: 'Aeonik VF', 'Aeonik', system-ui, sans-serif;
  font-size: 13.5px;
  font-weight: 500;
  width: 100%;
  padding: 11px 20px;
  border-radius: 10px;
  border: 1px solid var(--border);
  background: transparent;
  color: var(--text-secondary);
  cursor: pointer;
  transition: background 0.15s, border-color 0.15s, color 0.15s;
}
.btn-reset:hover {
  background: rgba(255,255,255,0.06);
  border-color: var(--border-hover);
  color: var(--text-primary);
}

/* ────────────────────────────────────────────────────────────────────────
   MAIN / PREVIEW
──────────────────────────────────────────────────────────────────────── */
.main {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 40px 48px 80px;  /* extra bottom padding clears the fixed download btn */
  background: var(--bg);
}
.preview-outer {
  width: 100%;
  max-width: 880px;
}
.preview-eyebrow {
  font-size: 11px;
  font-weight: 600;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  color: var(--text-secondary);
  margin-bottom: 14px;
}
.preview-frame {
  width: 100%;
  aspect-ratio: 1600 / 697;
  border: 1.5px dashed rgba(255,255,255,0.18);
  border-radius: 14px;
  overflow: hidden;
  background: #000;
  transition: border-color 0.2s;
}
.preview-frame:hover {
  border-color: rgba(255,255,255,0.28);
}
.preview-frame svg {
  display: block;
  width: 100%;
  height: 100%;
  border-radius: 12px;
}
.preview-meta {
  font-family: 'Aeonik Mono', 'Courier New', monospace;
  font-size: 11.5px;
  color: var(--text-secondary);
  margin-top: 12px;
  letter-spacing: 0.01em;
}

/* ────────────────────────────────────────────────────────────────────────
   FIXED DOWNLOAD BUTTON (bottom-right)
──────────────────────────────────────────────────────────────────────── */
.btn-download-fixed {
  position: fixed;
  bottom: 28px;
  right: 28px;
  z-index: 100;
  font-family: 'Aeonik VF', 'Aeonik', system-ui, sans-serif;
  font-size: 14px;
  font-weight: 600;
  padding: 13px 20px 13px 24px;
  border-radius: 12px;
  border: none;
  background: var(--accent);
  color: #000;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 10px;
  box-shadow: 0 4px 20px rgba(241,208,83,0.30);
  transition: background 0.15s, box-shadow 0.15s, transform 0.1s;
  letter-spacing: 0.01em;
}
.btn-download-fixed:hover {
  background: var(--accent-dark);
  box-shadow: 0 6px 28px rgba(241,208,83,0.40);
  transform: translateY(-1px);
}
.btn-download-fixed:active {
  transform: translateY(0);
}
.btn-download-fixed:disabled {
  opacity: 0.50;
  cursor: not-allowed;
  transform: none;
}
.btn-download-fixed .dl-arrow {
  width: 26px;
  height: 26px;
  background: rgba(0,0,0,0.15);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}
.btn-download-fixed .dl-arrow svg {
  width: 13px;
  height: 13px;
}
</style>
</head>
<body>
<div class="app">

  <!-- ── Sidebar ─────────────────────────────────────────────────────── -->
  <aside class="sidebar">

    <div class="sidebar-header">
      <p class="sidebar-eyebrow">Design</p>
      <h1 class="sidebar-title">Productboard Thumbnail</h1>
    </div>

    <div class="sidebar-divider"></div>

    <div class="sidebar-body">

      <!-- Title field -->
      <div class="field-block">
        <p class="field-label">Title</p>
        <textarea id="title-input" rows="4" spellcheck="false"></textarea>
        <p class="field-hint">Press "Enter" to add a line break.</p>
      </div>

      <!-- Font size indicator -->
      <div class="fontsize-row">
        <p class="fontsize-label">Font Size</p>
        <span class="fontsize-pill" id="size-pill">112px</span>
      </div>

    </div>

    <div class="sidebar-footer">
      <button class="btn-reset" id="reset-btn">Reset to defaults</button>
    </div>

  </aside>

  <!-- ── Preview pane ────────────────────────────────────────────────── -->
  <main class="main">
    <div class="preview-outer">
      <p class="preview-eyebrow">Preview</p>
      <div class="preview-frame">
        @@SVG_INLINE@@
      </div>
      <p class="preview-meta">1600 &times; 697 px &nbsp;&middot;&nbsp; PNG</p>
    </div>
  </main>

</div>

<!-- ── Fixed download button ──────────────────────────────────────────── -->
<button class="btn-download-fixed" id="download-btn">
  <span id="download-label">Download thumbnail</span>
  <span class="dl-arrow">
    <svg viewBox="0 0 13 13" fill="none" xmlns="http://www.w3.org/2000/svg">
      <path d="M6.5 1.5v7M3.5 6 6.5 9l3-3M1.5 11.5h10" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
    </svg>
  </span>
</button>

<script>
(function () {
  'use strict';

  /* ── Constants ──────────────────────────────────────────────────────── */
  var DEFAULT_TITLE = 'This will be the title of the\nProductboard article';
  var STORAGE_KEY   = 'intellistack.productboard-thumbnail.title';
  var DEFAULT_SIZE  = 112;
  var MIN_SIZE      = 88;
  var MAX_WIDTH     = 1508;
  var FIRST_Y       = 141.2;
  var FONT_B64      = '@@FONT_B64@@';

  /* ── DOM refs ───────────────────────────────────────────────────────── */
  var svgEl         = document.getElementById('thumbnail-svg');
  var textEl        = document.getElementById('data-editable');
  var textarea      = document.getElementById('title-input');
  var resetBtn      = document.getElementById('reset-btn');
  var downloadBtn   = document.getElementById('download-btn');
  var downloadLabel = document.getElementById('download-label');
  var sizePill      = document.getElementById('size-pill');

  /* ── Measurement canvas ─────────────────────────────────────────────── */
  var mCanvas = document.createElement('canvas');
  var mCtx    = mCanvas.getContext('2d');

  function measureLine(text, size) {
    mCtx.font = size + 'px "Aeonik VF"';
    return mCtx.measureText(text).width;
  }

  function calcFontSize(lines) {
    var size = DEFAULT_SIZE;
    while (size > MIN_SIZE) {
      var maxW = 0;
      for (var i = 0; i < lines.length; i++) {
        var w = measureLine(lines[i], size);
        if (w > maxW) maxW = w;
      }
      if (maxW <= MAX_WIDTH) break;
      size -= 2;
    }
    return Math.max(size, MIN_SIZE);
  }

  /* ── SVG updater ────────────────────────────────────────────────────── */
  function updateSVG(rawText) {
    var lines = rawText.split('\n');
    var size  = calcFontSize(lines);

    textEl.setAttribute('font-size', size);

    while (textEl.firstChild) { textEl.removeChild(textEl.firstChild); }

    var ns = 'http://www.w3.org/2000/svg';
    for (var i = 0; i < lines.length; i++) {
      var tspan = document.createElementNS(ns, 'tspan');
      tspan.setAttribute('x', '46');
      tspan.setAttribute('y', String(FIRST_Y + i * size));
      tspan.textContent = lines[i];
      textEl.appendChild(tspan);
    }

    sizePill.textContent = size + 'px';
    if (size < DEFAULT_SIZE) {
      sizePill.classList.add('shrunk');
    } else {
      sizePill.classList.remove('shrunk');
    }
  }

  /* ── localStorage ───────────────────────────────────────────────────── */
  var saveTimer = null;
  function schedSave(val) {
    clearTimeout(saveTimer);
    saveTimer = setTimeout(function () {
      try { localStorage.setItem(STORAGE_KEY, val); } catch (e) {}
    }, 250);
  }

  /* ── Handlers ───────────────────────────────────────────────────────── */
  textarea.addEventListener('input', function () {
    updateSVG(textarea.value);
    schedSave(textarea.value);
  });

  resetBtn.addEventListener('click', function () {
    textarea.value = DEFAULT_TITLE;
    updateSVG(DEFAULT_TITLE);
    try { localStorage.removeItem(STORAGE_KEY); } catch (e) {}
  });

  /* ── Export ─────────────────────────────────────────────────────────── */
  function slugify(str) {
    return str.toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/^-+|-+$/g, '').slice(0, 60);
  }

  function fontFaceBlock() {
    var src = 'url(data:font/woff2;base64,' + FONT_B64 + ') format(\'woff2\')';
    return (
      '@font-face { font-family: \'Aeonik VF\'; src: ' + src + '; font-weight: 100 900; font-style: normal; }' +
      '@font-face { font-family: \'Aeonik\';    src: ' + src + '; font-weight: 100 900; font-style: normal; }'
    );
  }

  downloadBtn.addEventListener('click', function () {
    downloadBtn.disabled     = true;
    downloadLabel.textContent = 'Exporting…';

    var lines    = textarea.value.split('\n');
    var date     = new Date().toISOString().slice(0, 10);
    var filename = 'productboard-thumbnail-' + slugify(lines[0] || 'thumbnail') + '-' + date + '.png';

    var serializer = new XMLSerializer();
    var svgStr     = serializer.serializeToString(svgEl);

    if (svgStr.indexOf('xmlns=') === -1) {
      svgStr = svgStr.replace('<svg', '<svg xmlns="http://www.w3.org/2000/svg"');
    }

    var fontDefs = '<defs><style type="text/css">' + fontFaceBlock() + '</style></defs>';
    svgStr = svgStr.replace(/<\/svg>\s*$/, fontDefs + '</svg>');

    var blob = new Blob([svgStr], { type: 'image/svg+xml;charset=utf-8' });
    var url  = URL.createObjectURL(blob);
    var img  = new Image();

    img.onload = function () {
      var canvas    = document.createElement('canvas');
      canvas.width  = 1600;
      canvas.height = 697;
      canvas.getContext('2d').drawImage(img, 0, 0, 1600, 697);
      URL.revokeObjectURL(url);

      canvas.toBlob(function (pngBlob) {
        var a      = document.createElement('a');
        a.href     = URL.createObjectURL(pngBlob);
        a.download = filename;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        setTimeout(function () { URL.revokeObjectURL(a.href); }, 1000);

        downloadBtn.disabled      = false;
        downloadLabel.textContent = 'Download thumbnail';
      }, 'image/png');
    };

    img.onerror = function () {
      URL.revokeObjectURL(url);
      downloadBtn.disabled      = false;
      downloadLabel.textContent = 'Download thumbnail';
      alert('Export failed — see browser console for details.');
    };

    img.src = url;
  });

  /* ── Init ───────────────────────────────────────────────────────────── */
  document.fonts.ready.then(function () {
    var saved = null;
    try { saved = localStorage.getItem(STORAGE_KEY); } catch (e) {}
    var initial = (saved !== null) ? saved : DEFAULT_TITLE;
    textarea.value = initial;
    updateSVG(initial);
  });

}());
</script>
</body>
</html>
"""

html = (HTML
  .replace('@@FONT_B64@@',      font_b64)
  .replace('@@FONT_MONO_B64@@', font_mono_b64)
  .replace('@@SVG_INLINE@@',    svg_inline))

OUT_PATH.write_text(html, encoding='utf-8')
print(f"Written: {OUT_PATH}")
print(f"File size: {OUT_PATH.stat().st_size / 1024:.1f} KB")
