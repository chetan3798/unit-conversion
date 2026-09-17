document.addEventListener('DOMContentLoaded', () => {
  const dataEl = document.getElementById('categories-data');
  let CATEGORIES = {};
  try {
    CATEGORIES = dataEl ? JSON.parse(dataEl.textContent) : {};
  } catch (err) {
    console.error('Could not parse category data -- is this page being served by Flask (python app.py), not opened as a raw file?', err);
  }

  const categoryKeys = Object.keys(CATEGORIES);

  const UNIT_LABELS = {
    ton: 'metric ton', gal: 'gal (US)', gal_uk: 'gal (UK)', floz: 'fl oz',
    barrel: 'oil barrel', short_ton: 'short ton (US)', long_ton: 'long ton (UK)',
    troy_oz: 'troy oz', acre_ft: 'acre-ft', board_ft: 'board ft', sqmile: 'sq mile',
    mm2: 'mm²', cm2: 'cm²', m2: 'm²', km2: 'km²', ft2: 'ft²', yd2: 'yd²',
    kmh: 'km/h', ms: 'm/s', BTU_hr: 'BTU/hr', ton_ref: 'ton (refrigeration)',

    // Electrical & Electronics
    V: 'Volt (V)', mV: 'Millivolt (mV)', kV: 'Kilovolt (kV)',
    A: 'Ampere (A)', mA: 'Milliampere (mA)', uA: 'Microampere (µA)',
    ohm: 'Ohm (Ω)', kohm: 'Kilohm (kΩ)', Mohm: 'Megohm (MΩ)',
    Hz: 'Hertz (Hz)', kHz: 'Kilohertz (kHz)', MHz: 'Megahertz (MHz)', GHz: 'Gigahertz (GHz)',

    // Fluid Dynamics & HVAC
    cfm: 'CFM (ft³/min)', gpm: 'GPM (gal/min)', Ls: 'Liters/sec (L/s)', m3hr: 'm³/hour',
    cP: 'Centipoise (cP)', cSt: 'Centistokes (cSt)', Pas: 'Pascal-second (Pa·s)',

    // Mechanical & Structural
    N: 'Newton (N)', kN: 'Kilonewton (kN)', lbf: 'Pound-force (lbf)',
    Nm: 'Newton-meter (N·m)', lbft: 'Foot-pound (ft·lbf)',
    kgm3: 'kg/m³', gcm3: 'g/cm³', lbft3: 'lb/ft³',
    ms2: 'm/s²', g: 'Standard gravity (g)',
    deg: 'Degrees (°)', rad: 'Radians (rad)', rpm: 'RPM (rev/min)',

    // Data & Telecommunications
    Mbps: 'Megabits/sec (Mbps)', Gbps: 'Gigabits/sec (Gbps)', MBs: 'Megabytes/sec (MB/s)',
    dB: 'Decibels (dB)', dBA: 'A-weighted (dBA)', dBm: 'Decibel-milliwatts (dBm)',

    // Lighting & Optics
    lx: 'Lux (lx)', fc: 'Foot-candles (fc)', nit: 'Nits (cd/m²)', lm: 'Lumens (lm)',

    // Automotive & Environmental
    mpg_us: 'Miles/gal US (MPG)', mpg_uk: 'Miles/gal UK (MPG)', l_per_100km: 'Liters/100km (L/100km)', km_per_l: 'Kilometers/liter (km/L)',
    Sv: 'Sievert (Sv)', Gy: 'Gray (Gy)', rem: 'Rem',
  };
  const labelFor = (unit) => UNIT_LABELS[unit] || unit;

  const boxWrapper = document.getElementById('boxWrapper');
  const categorySelect = document.getElementById('categorySelect');
  const catIcon = document.getElementById('catIcon');
  const formulaNote = document.getElementById('formulaNote');
  const resetBtn = document.getElementById('resetBtn');

  const precisionSelect = document.getElementById('precisionSelect');
  const themeToggleBtn = document.getElementById('themeToggleBtn');
  const themeIcon = themeToggleBtn ? themeToggleBtn.querySelector('.theme-icon') : null;
  const toastNotification = document.getElementById('toastNotification');

  let currentKey = categoryKeys[0];
  const debounceTimers = {};
  let currentPrecision = 'auto';

  if (!currentKey) {
    formulaNote.textContent = 'No categories configured.';
    return;
  }

  function applyTheme(theme) {
    document.documentElement.setAttribute('data-theme', theme);
    if (themeIcon) {
      themeIcon.className = theme === 'dark' ? 'fa-solid fa-sun theme-icon' : 'fa-solid fa-moon theme-icon';
    }
  }

  const savedTheme = localStorage.getItem('theme') || 'light';
  applyTheme(savedTheme);

  if (themeToggleBtn) {
    themeToggleBtn.addEventListener('click', () => {
      const cTheme = document.documentElement.getAttribute('data-theme') || 'light';
      const nTheme = cTheme === 'light' ? 'dark' : 'light';
      applyTheme(nTheme);
      localStorage.setItem('theme', nTheme);
    });
  }

  function showToast(msg) {
    if (!toastNotification) return;
    toastNotification.textContent = msg;
    toastNotification.classList.add('show');
    setTimeout(() => toastNotification.classList.remove('show'), 2000);
  }

  function copyToClipboard(text) {
    if (!text) return;
    navigator.clipboard.writeText(text).then(() => showToast('Copied!')).catch(() => showToast('Failed to copy'));
  }

  if (precisionSelect) {
    precisionSelect.addEventListener('change', (e) => {
      currentPrecision = e.target.value;
      const box = document.querySelector(`.cat-box[data-key="${currentKey}"]`);
      if (box) {
         if (box._getMode && box._getMode() === 'all') {
           box._convertAllBox(box, currentKey);
         } else {
           const activeInput = getActiveSourceInput(box);
           convertPair(box, activeInput);
         }
      }
    });
  }

  function formatInputNumber(value) {
    const num = Number(value);
    if (!Number.isFinite(num)) {
      return '';
    }

    if (currentPrecision === 'sci') return num.toExponential(4);
    if (currentPrecision !== 'auto') return num.toFixed(parseInt(currentPrecision, 10));

    const normalized = num.toString();
    if (!normalized.includes('e')) {
      return normalized.replace(/(\.\d*?)0+$/, '$1').replace(/\.$/, '');
    }

    return num.toFixed(12).replace(/(\.\d*?)0+$/, '$1').replace(/\.$/, '');
  }

  // Format a number for read-only display: up to 8 significant digits,
  // no trailing zeros, graceful dash for non-finite values.
  function formatDisplayNumber(value) {
    const num = Number(value);
    if (!Number.isFinite(num)) return '\u2014';
    if (num === 0) return '0';
    if (currentPrecision === 'sci') return num.toExponential(4);
    if (currentPrecision !== 'auto') return num.toFixed(parseInt(currentPrecision, 10));
    return parseFloat(num.toPrecision(8)).toString();
  }

  function setEditState(box, fieldName) {
    box.dataset.lastEdited = fieldName;
  }

  function getActiveSourceInput(box) {
    const bottom = box.querySelector('.bottomInput');
    const top = box.querySelector('.topInput');
    if (box.dataset.lastEdited === 'bottom' && bottom && bottom.value !== '') {
      return bottom;
    }
    return top;
  }

  async function convertPair(boxEl, sourceField) {
    if (!boxEl) return;
    const key = boxEl.dataset.key;
    const fromSel = boxEl.querySelector('.fromUnit');
    const toSel = boxEl.querySelector('.toUnit');
    const topInput = boxEl.querySelector('.topInput');
    const bottomInput = boxEl.querySelector('.bottomInput');
    if (!topInput || !bottomInput || !fromSel || !toSel) return;

    const isTop = sourceField ? (sourceField === topInput) : (boxEl.dataset.lastEdited !== 'bottom');
    const sourceInput = isTop ? topInput : bottomInput;
    const targetInput = isTop ? bottomInput : topInput;
    const fromUnit = isTop ? fromSel.value : toSel.value;
    const toUnit = isTop ? toSel.value : fromSel.value;

    const valStr = (sourceInput.value || '').trim();
    if (valStr === '' || Number.isNaN(Number(valStr))) {
      targetInput.value = '';
      return;
    }

    try {
      const response = await fetch('/api/convert', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          category: key,
          from_unit: fromUnit,
          to_unit: toUnit,
          value: Number(valStr),
        }),
      });
      const data = await response.json();
      if (data.error) {
        return;
      }
      targetInput.value = formatInputNumber(data.result);
      if (isTop) {
        const allFromInput = boxEl.querySelector('.allFromInput');
        if (allFromInput && allFromInput.value !== topInput.value) {
          allFromInput.value = topInput.value;
        }
      }
    } catch (err) {
      console.error('convertPair error:', err);
    }
  }

  const debounceConvertPair = (boxEl, sourceField) => {
    const key = boxEl.dataset.key;
    clearTimeout(debounceTimers[key + '-pair']);
    debounceTimers[key + '-pair'] = setTimeout(() => convertPair(boxEl, sourceField), 150);
  };

  const CATEGORY_GROUPS = {
    'Common': ['length', 'weight', 'temperature', 'volume', 'area', 'time'],
    'Engineering & Mechanics': ['speed', 'acceleration', 'force', 'torque', 'density', 'angle_rotation', 'pressure', 'energy', 'power'],
    'Electronics & Data': ['voltage', 'current', 'resistance', 'frequency', 'digital_storage', 'data_transfer_rate'],
    'Fluids & HVAC': ['flow_rate', 'viscosity'],
    'Environmental & Misc': ['sound_level', 'illuminance_luminance', 'fuel_efficiency', 'radiation_dose']
  };

  function renderCategoryOptions(filter = '') {
    const f = filter.toLowerCase();
    categorySelect.innerHTML = Object.keys(CATEGORY_GROUPS).map(group => {
      const options = CATEGORY_GROUPS[group].filter(key => {
         if (!CATEGORIES[key]) return false;
         return CATEGORIES[key].label.toLowerCase().includes(f) || key.includes(f);
      }).map(key => `<option value="${key}">${CATEGORIES[key].label}</option>`);
      
      if (options.length === 0) return '';
      return `<optgroup label="${group}">${options.join('')}</optgroup>`;
    }).join('');
  }
  
  renderCategoryOptions();

  const categorySearchInput = document.getElementById('categorySearchInput');
  const clearSearchBtn = document.getElementById('clearSearchBtn');
  
  if (categorySearchInput) {
    categorySearchInput.addEventListener('input', (e) => {
      renderCategoryOptions(e.target.value);
      if (clearSearchBtn) clearSearchBtn.style.display = e.target.value ? '' : 'none';
    });
  }
  
  if (clearSearchBtn) {
    clearSearchBtn.addEventListener('click', () => {
      if (categorySearchInput) categorySearchInput.value = '';
      renderCategoryOptions();
      clearSearchBtn.style.display = 'none';
    });
  }

  categoryKeys.forEach((key, i) => {
    const cat = CATEGORIES[key];
    const box = document.createElement('div');
    box.className = 'cat-box';
    box.dataset.key = key;
    if (i !== 0) box.style.display = 'none';

    const opts = cat.units.map((u) => `<option value="${u}">${labelFor(u)}</option>`).join('');
    box.innerHTML = `
      <div class="mode-toggle">
        <button class="modeBtn active" type="button" data-mode="one">Single Conversion</button>
        <button class="modeBtn" type="button" data-mode="all">Multi-Unit View</button>
      </div>

      <div class="single-mode">
        <div class="conversion-stack">
          <div class="conversion-card">
            <span class="input-meta">From</span>
            <div class="field-row">
              <input type="number" inputmode="decimal" step="any" class="topInput" placeholder="0" aria-label="Value to convert from" />
              <select class="fromUnit" aria-label="From unit">${opts}</select>
            </div>
          </div>

          <button class="swapTrigger" type="button" aria-label="Swap units" title="Swap units">
            <i class="fa-solid fa-arrows-up-down" aria-hidden="true"></i>
          </button>

          <div class="conversion-card">
            <span class="input-meta">To</span>
            <div class="field-row">
              <input type="number" inputmode="decimal" step="any" class="bottomInput" placeholder="0" aria-label="Converted value" />
              <select class="toUnit" aria-label="To unit">${opts}</select>
              <button class="copyBtn" type="button" aria-label="Copy result" title="Copy (C)"><i class="fa-regular fa-copy"></i></button>
            </div>
          </div>
        </div>
      </div>

      <div class="all-mode" style="display:none;">
        <div class="conversion-card all-from-control">
          <span class="input-meta">From</span>
          <div class="field-row">
            <input type="number" inputmode="decimal" step="any" class="allFromInput" placeholder="0" aria-label="Value to convert from" />
            <select class="allFromUnit" aria-label="From unit">${opts}</select>
          </div>
        </div>
        <div class="all-list"></div>
      </div>`;

    const fromSel = box.querySelector('.fromUnit');
    const toSel = box.querySelector('.toUnit');
    const topInput = box.querySelector('.topInput');
    const bottomInput = box.querySelector('.bottomInput');

    const allModeEl = box.querySelector('.all-mode');
    const oneModeEl = box.querySelector('.single-mode');
    const allListEl = box.querySelector('.all-list');
    const allFromInput = box.querySelector('.allFromInput');
    const allFromUnit = box.querySelector('.allFromUnit');
    let mode = 'one';

    fromSel.value = cat.default[0];
    toSel.value = cat.default[1];
    topInput.value = '1';
    allFromInput.value = '1';
    allFromUnit.value = cat.default[0];
    setEditState(box, 'top');

    boxWrapper.appendChild(box);

    async function convertAllBox(boxEl, categoryKey) {
      const value = topInput.value;
      if (value === '' || Number.isNaN(parseFloat(value))) {
        allListEl.innerHTML = '<p class="all-list-error">Enter a value above</p>';
        return;
      }

      try {
        const response = await fetch('/api/convert-all', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ category: categoryKey, from_unit: fromSel.value, value }),
        });
        const data = await response.json();
        if (data.error) {
          allListEl.innerHTML = `<p class="all-list-error">${data.error}</p>`;
          return;
        }

        // Render each unit as a read-only display row
        allListEl.innerHTML = data.results
          .map((row) => {
            const isActive = row.unit === fromSel.value;
            return `
              <div class="all-row ${isActive ? 'active' : ''}">
                <span class="unit-label">
                  ${labelFor(row.unit)}
                  ${isActive ? '<span class="from-badge">FROM</span>' : ''}
                </span>
                <span class="unit-value-display">${formatDisplayNumber(row.result)}</span>
                <button class="copyBtn listCopyBtn" data-value="${row.result}" type="button" aria-label="Copy" title="Copy"><i class="fa-regular fa-copy"></i></button>
              </div>`;
          })
          .join('');
      } catch (err) {
        allListEl.innerHTML = '<p class="all-list-error">Connection error</p>';
      }
    }

    const debounceConvertAll = (boxEl, categoryKey) => {
      clearTimeout(debounceTimers[categoryKey + '-all']);
      debounceTimers[categoryKey + '-all'] = setTimeout(() => convertAllBox(boxEl, categoryKey), 200);
    };

    topInput.addEventListener('input', () => {
      setEditState(box, 'top');
      allFromInput.value = topInput.value;
      debounceConvertPair(box, topInput);
      debounceConvertAll(box, key);
    });

    bottomInput.addEventListener('input', () => {
      setEditState(box, 'bottom');
      debounceConvertPair(box, bottomInput);
    });

    // Multi-unit From value: sync to topInput then debounce recalc.
    allFromInput.addEventListener('input', () => {
      topInput.value = allFromInput.value;
      setEditState(box, 'top');
      debounceConvertPair(box, topInput);
      debounceConvertAll(box, key);
    });

    // Multi-unit From unit: sync to fromSel then recalc immediately.
    allFromUnit.addEventListener('change', () => {
      fromSel.value = allFromUnit.value;
      updateFormula(key, fromSel.value, toSel.value);
      convertPair(box, topInput);
      convertAllBox(box, key);
    });

    fromSel.addEventListener('change', () => {
      allFromUnit.value = fromSel.value;
      const activeInput = getActiveSourceInput(box);
      updateFormula(key, fromSel.value, toSel.value);
      if (mode === 'one') {
        convertPair(box, activeInput);
      } else {
        convertAllBox(box, key);
      }
    });

    toSel.addEventListener('change', () => {
      const activeInput = getActiveSourceInput(box);
      updateFormula(key, fromSel.value, toSel.value);
      if (mode === 'one') {
        convertPair(box, activeInput);
      } else {
        convertAllBox(box, key);
      }
    });

    box.querySelector('.swapTrigger').addEventListener('click', () => {
      const tempUnit = fromSel.value;
      fromSel.value = toSel.value;
      toSel.value = tempUnit;
      allFromUnit.value = fromSel.value;

      setEditState(box, 'top');
      updateFormula(key, fromSel.value, toSel.value);
      if (mode === 'one') {
        convertPair(box, topInput);
      } else {
        convertAllBox(box, key);
      }
    });

    box.querySelectorAll('.modeBtn').forEach((btn) => {
      btn.addEventListener('click', () => {
        mode = btn.dataset.mode;
        box.querySelectorAll('.modeBtn').forEach((b) => b.classList.toggle('active', b === btn));
        if (mode === 'one') {
          // Sync multi-unit controls back into single-mode fields.
          topInput.value = allFromInput.value;
          fromSel.value = allFromUnit.value;
          oneModeEl.style.display = '';
          allModeEl.style.display = 'none';
          formulaNote.style.display = '';
          setEditState(box, 'top');
          updateFormula(key, fromSel.value, toSel.value);
          convertPair(box, topInput);
        } else {
          // Sync single-mode fields into multi-unit controls.
          allFromInput.value = topInput.value;
          allFromUnit.value = fromSel.value;
          oneModeEl.style.display = 'none';
          allModeEl.style.display = '';
          formulaNote.style.display = 'none';
          convertAllBox(box, key);
        }
      });
    });

    box.addEventListener('click', (e) => {
      const copyBtn = e.target.closest('.copyBtn');
      if (copyBtn) {
        if (copyBtn.classList.contains('listCopyBtn')) {
          copyToClipboard(copyBtn.dataset.value);
        } else {
          copyToClipboard(bottomInput.value);
        }
      }
    });

    box._getMode = () => mode;
    box._convertPair = convertPair;
    box._convertAllBox = convertAllBox;
  });

  async function updateFormula(key, fromUnit, toUnit) {
    if (key === 'temperature') {
      formulaNote.textContent = 'Temperature uses an offset formula, not a fixed multiplier.';
      return;
    }
    if (key === 'fuel_efficiency' && ((fromUnit === 'l_per_100km') !== (toUnit === 'l_per_100km'))) {
      formulaNote.textContent = 'Fuel economy uses an inverse formula (e.g., L/100km = 235.215 / MPG US).';
      return;
    }

    try {
      const response = await fetch('/api/convert', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ category: key, from_unit: fromUnit, to_unit: toUnit, value: 1 }),
      });
      const data = await response.json();
      if (data.error) {
        formulaNote.textContent = '';
        return;
      }
      const ratio = Number(data.result).toLocaleString(undefined, { maximumFractionDigits: 6 });
      formulaNote.textContent = `1 ${labelFor(fromUnit)} = ${ratio} ${labelFor(toUnit)}`;
    } catch (err) {
      formulaNote.textContent = '';
    }
  }

  function switchCategory(key) {
    const oldBox = document.querySelector(`.cat-box[data-key="${currentKey}"]`);
    const newBox = document.querySelector(`.cat-box[data-key="${key}"]`);
    if (!oldBox || !newBox) return;

    oldBox.classList.add('fade-out');
    setTimeout(() => {
      oldBox.style.display = 'none';
      oldBox.classList.remove('fade-out');
      currentKey = key;
      catIcon.className = `fa-solid fa-${CATEGORIES[key].icon}`;
      newBox.style.display = '';
      newBox.classList.add('fade-in');

      const topInput = newBox.querySelector('.topInput');
      const fromSel = newBox.querySelector('.fromUnit');
      const toSel = newBox.querySelector('.toUnit');
      const boxMode = newBox._getMode && newBox._getMode();

      if (boxMode === 'all') {
        newBox._convertAllBox(newBox, key);
      } else {
        topInput.value = topInput.value || '1';
        setEditState(newBox, 'top');
        updateFormula(key, fromSel.value, toSel.value);
        convertPair(newBox, topInput);
      }

      requestAnimationFrame(() => {
        requestAnimationFrame(() => newBox.classList.remove('fade-in'));
      });
    }, 150);
  }

  categorySelect.addEventListener('change', (e) => switchCategory(e.target.value));

  resetBtn.addEventListener('click', () => {
    const box = document.querySelector(`.cat-box[data-key="${currentKey}"]`);
    const cat = CATEGORIES[currentKey];
    const topInput = box.querySelector('.topInput');
    const fromSel = box.querySelector('.fromUnit');
    const toSel = box.querySelector('.toUnit');
    const allFromInput = box.querySelector('.allFromInput');
    const allFromUnit = box.querySelector('.allFromUnit');

    topInput.value = '1';
    fromSel.value = cat.default[0];
    toSel.value = cat.default[1];
    if (allFromInput) allFromInput.value = '1';
    if (allFromUnit) allFromUnit.value = cat.default[0];
    setEditState(box, 'top');

    if (box._getMode && box._getMode() === 'all') {
      box._convertAllBox(box, currentKey);
    } else {
      updateFormula(currentKey, cat.default[0], cat.default[1]);
      convertPair(box, topInput);
    }
  });

  catIcon.className = `fa-solid fa-${CATEGORIES[currentKey].icon}`;
  const firstBox = document.querySelector(`.cat-box[data-key="${currentKey}"]`);
  const firstTopInput = firstBox.querySelector('.topInput');
  firstTopInput.value = '1';
  setEditState(firstBox, 'top');
  updateFormula(currentKey, CATEGORIES[currentKey].default[0], CATEGORIES[currentKey].default[1]);
  convertPair(firstBox, firstTopInput);

  // About Modal Controller
  const aboutLink = document.getElementById('aboutLink');
  const aboutModal = document.getElementById('aboutModal');
  const closeAboutBtn = document.getElementById('closeAboutBtn');
  const modalDoneBtn = document.getElementById('modalDoneBtn');

  function openAboutModal() {
    if (!aboutModal) return;
    aboutModal.classList.add('active');
    aboutModal.setAttribute('aria-hidden', 'false');
    document.body.style.overflow = 'hidden';
  }

  function closeAboutModal() {
    if (!aboutModal) return;
    aboutModal.classList.remove('active');
    aboutModal.setAttribute('aria-hidden', 'true');
    document.body.style.overflow = '';
  }

  if (aboutLink) {
    aboutLink.addEventListener('click', (e) => {
      e.preventDefault();
      openAboutModal();
    });
  }

  if (closeAboutBtn) {
    closeAboutBtn.addEventListener('click', closeAboutModal);
  }

  if (modalDoneBtn) {
    modalDoneBtn.addEventListener('click', closeAboutModal);
  }

  if (aboutModal) {
    aboutModal.addEventListener('click', (e) => {
      if (e.target === aboutModal) {
        closeAboutModal();
      }
    });
  }

  window.addEventListener('keydown', (e) => {
    // Only trigger shortcuts if not typing in an input
    const isInput = e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA';
    
    if (e.key === 'Escape') {
      if (aboutModal && aboutModal.classList.contains('active')) {
        closeAboutModal();
      } else {
        if (resetBtn) resetBtn.click();
      }
    }
    
    if (!isInput) {
      if (e.key.toLowerCase() === 's') {
        const box = document.querySelector(`.cat-box[data-key="${currentKey}"]`);
        if (box) {
          const swapBtn = box.querySelector('.swapTrigger');
          if (swapBtn && swapBtn.offsetParent !== null) swapBtn.click();
        }
      }
      
      if (e.key.toLowerCase() === 'c') {
         const box = document.querySelector(`.cat-box[data-key="${currentKey}"]`);
         if (box) {
            const bottomInput = box.querySelector('.bottomInput');
            if (bottomInput && bottomInput.offsetParent !== null) copyToClipboard(bottomInput.value);
         }
      }
    }
  });
});
