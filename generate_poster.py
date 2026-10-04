import os

with open('qr_code.svg', 'r', encoding='utf-8') as f:
    qr_svg = f.read().strip()

qr_svg_clean = qr_svg.replace('width="39mm" height="39mm"', 'class="qr-code-svg" viewBox="0 0 39 39"')

html_content = f'''<!doctype html>
<html lang="kk">
<head>
<meta charset="utf-8">
<title>Постер · ЕББҚ бар балаларды ерте жастан сапалы білім алу жағдайын қамту</title>
<link rel="stylesheet" href="css/fonts.css">
<link rel="stylesheet" href="css/tokens.css">
<link rel="stylesheet" href="css/base.css">
<style>
  @page {{
    size: 210mm 297mm;
    margin: 0;
  }}

  body {{
    margin: 0;
    padding: 0;
    background: var(--c-ink);
  }}

  .poster-sheet {{
    width: 210mm;
    height: 297mm;
    position: relative;
    overflow: hidden;
    background: var(--c-ink);
    color: var(--c-paper);
    padding: 16mm 16mm 14mm 16mm;
    box-sizing: border-box;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
  }}

  /* Подложка SVG */
  .poster-sheet > .art {{
    position: absolute;
    left: 0; top: 0;
    width: 210mm; height: 297mm;
    z-index: 0;
    overflow: visible;
  }}

  .art path, .art line, .art circle {{
    vector-effect: non-scaling-stroke;
    fill: none;
  }}

  .art .ax-grid {{
    stroke: var(--c-grid-dark);
    stroke-width: 0.2mm;
  }}

  .art .traj-line {{
    stroke: var(--c-amber);
    stroke-width: calc(var(--line) * 1.5);
  }}

  .art .traj-dash {{
    stroke: var(--c-amber);
    stroke-width: var(--line);
    stroke-dasharray: 2mm 1.5mm;
  }}

  .art .head-amber {{
    fill: var(--c-amber);
    stroke: none;
  }}

  .art .tick-amber {{
    stroke: var(--c-amber);
    stroke-width: var(--line);
  }}

  /* Общие элементы */
  .z-content {{
    position: relative;
    z-index: 1;
  }}

  .ref {{
    font-size: var(--fs-note);
    white-space: nowrap;
    opacity: 0.75;
    font-weight: 400;
  }}

  /* ==================== ВЕРХНИЙ БЛОК: ЗАГОЛОВОК, СЛОГАН, ПРИЗЫВ ==================== */
  .header-block {{
    display: flex;
    flex-direction: column;
    gap: var(--sp-2);
  }}

  .slogan-tag {{
    display: inline-flex;
    align-items: center;
    gap: var(--sp-2);
    font-family: var(--f-display);
    font-size: 11pt;
    font-weight: 700;
    color: var(--c-amber);
    letter-spacing: 0.8pt;
    text-transform: uppercase;
  }}

  .slogan-tag::before {{
    content: '';
    width: 6mm;
    height: calc(var(--line) * 1.5);
    background: var(--c-amber);
  }}

  .poster-title {{
    font-family: var(--f-display);
    font-size: 26pt;
    font-weight: 800;
    line-height: 1.15;
    color: var(--c-paper);
    margin: 0;
    letter-spacing: -0.3pt;
  }}

  .call-banner {{
    margin-top: var(--sp-1);
    padding: 3mm 4mm;
    background: rgba(242, 168, 29, 0.12);
    border-left: calc(var(--line) * 2.5) solid var(--c-amber);
    font-family: var(--f-display);
    font-size: 14.5pt;
    font-weight: 700;
    color: var(--c-paper);
    line-height: 1.25;
  }}

  /* ==================== ЦЕНТРАЛЬНЫЙ БЛОК: ТРАЕКТОРИЯ 4 ОТМЕТКИ ==================== */
  .trajectory-block {{
    position: relative;
    margin: var(--sp-2) 0;
    padding-left: 18mm;
    display: flex;
    flex-direction: column;
    gap: 5.5mm;
  }}

  .milestone-card {{
    position: relative;
    background: rgba(245, 240, 230, 0.04);
    border: var(--line) solid rgba(245, 240, 230, 0.15);
    border-radius: 1.5mm;
    padding: 3mm 4.5mm;
    display: flex;
    flex-direction: column;
    gap: 1.2mm;
  }}

  .milestone-card.featured {{
    background: rgba(242, 168, 29, 0.08);
    border-color: rgba(242, 168, 29, 0.35);
  }}

  .milestone-head {{
    display: flex;
    align-items: baseline;
    gap: var(--sp-2);
  }}

  .milestone-badge {{
    font-family: var(--f-display);
    font-weight: 800;
    font-size: 11pt;
    line-height: 1;
    color: var(--c-amber);
    letter-spacing: 0.2pt;
  }}

  .milestone-title {{
    font-family: var(--f-display);
    font-weight: 700;
    font-size: 12pt;
    line-height: 1.15;
    color: var(--c-paper);
  }}

  .milestone-text {{
    margin: 0;
    font-family: var(--f-text);
    font-size: 10.2pt;
    line-height: 1.35;
    color: var(--c-paper);
    opacity: 0.92;
  }}

  /* ==================== НИЖНЯЯ ПЛАШКА: ФАКТЫ, QR, ИСТОЧНИКИ ==================== */
  .bottom-plate {{
    background: rgba(245, 240, 230, 0.06);
    border: var(--line) solid rgba(245, 240, 230, 0.2);
    border-radius: 2mm;
    padding: 4mm 5.5mm;
    display: grid;
    grid-template-columns: 1fr 34mm;
    column-gap: 5mm;
    align-items: center;
  }}

  .facts-col {{
    display: flex;
    flex-direction: column;
    gap: 2.5mm;
  }}

  .fact-item {{
    display: grid;
    grid-template-columns: 4mm 1fr;
    align-items: baseline;
    column-gap: 2mm;
  }}

  .fact-marker {{
    width: 2.2mm;
    height: 2.2mm;
    background: var(--c-amber);
    border-radius: 50%;
    margin-top: 1.5mm;
  }}

  .fact-text {{
    margin: 0;
    font-family: var(--f-text);
    font-size: 10pt;
    line-height: 1.35;
    color: var(--c-paper);
  }}

  .sources-note {{
    margin-top: 1mm;
    font-size: 8pt;
    line-height: 1.3;
    color: var(--c-paper);
    opacity: 0.75;
    border-top: var(--line) solid rgba(245, 240, 230, 0.12);
    padding-top: 2mm;
  }}

  .qr-col {{
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 1.5mm;
  }}

  .qr-card {{
    background: #FFFFFF;
    padding: 1.8mm;
    border-radius: 1.5mm;
    width: 26mm;
    height: 26mm;
    box-sizing: border-box;
    display: flex;
    align-items: center;
    justify-content: center;
  }}

  .qr-code-svg {{
    width: 100%;
    height: 100%;
    display: block;
  }}

  .qr-caption {{
    font-family: var(--f-display);
    font-size: 7.5pt;
    font-weight: 700;
    line-height: 1.2;
    text-align: center;
    color: var(--c-paper);
    opacity: 0.9;
  }}
</style>
</head>
<body>
<div class="poster-sheet mm-grid on-dark">

  <!-- ===== Единый рисунок SVG на весь лист 210×297 мм ===== -->
  <svg class="art" viewBox="0 0 210 297" aria-hidden="true">
    <!-- Вертикальная траектория в янтарном цвете (снизу вверх к школе) -->
    <path class="traj-line" d="M25 210 V100"/>
    <path class="head-amber" d="M25 94 L22.5 101 L27.5 101 Z"/>

    <!-- Горизонтальная опорная ось внизу траектории -->
    <path class="ax-grid" d="M16 210 H194"/>
    <path class="head-amber" d="M196 210 L192 208.5 L192 211.5 Z" style="fill: var(--c-grid-dark);"/>

    <!-- 4 отметки-коннектора точно по центру карточек этапов (к x=34 мм) -->
    <path class="tick-amber" d="
      M22 117.4 H34
      M22 140.9 H34
      M22 164.3 H34
      M22 187.8 H34
    "/>
  </svg>

  <!-- Янтарная точка-ребёнок на начальной отметке траектории (0 жас · Скрининг) -->
  <span class="dot" style="position:absolute; z-index:2; left: calc(25mm - var(--dot-r)); top: calc(187.8mm - var(--dot-r)); background: var(--c-amber); box-shadow: 0 0 5mm rgba(242, 168, 29, 0.7);"></span>

  <!-- ==================== ВЕРХНИЙ БЛОК: ЗАГОЛОВОК, СЛОГАН, ПРИЗЫВ ==================== -->
  <div class="header-block z-content">
    <div class="slogan-tag">Ерте басталған бағыт</div>
    <h1 class="poster-title">ЕББҚ бар балаларды ерте жастан<br>сапалы білім алу жағдайын қамту</h1>
    <div class="call-banner">
      Неғұрлым ерте, соғұрлым көп мүмкіндік. <span class="ref">[ТЕКСЕРУ]</span>
    </div>
  </div>

  <!-- ==================== ЦЕНТРАЛЬНЫЙ БЛОК: ТРАЕКТОРИЯ 4 ОТМЕТКИ (СНИЗУ ВВЕРХ) ==================== -->
  <div class="trajectory-block z-content">
    <!-- Отметка 4 (Мектеп, верхушка траектории) -->
    <div class="milestone-card">
      <div class="milestone-head">
        <span class="milestone-badge">Мектеп</span>
        <span class="milestone-title">Сабақтастық</span>
      </div>
      <p class="milestone-text">Қолдау балабақшадан мектепке дейін үзілмейді.</p>
    </div>

    <!-- Отметка 3 (1-3 жас) -->
    <div class="milestone-card">
      <div class="milestone-head">
        <span class="milestone-badge">1 жастан · 3 жастан</span>
        <span class="milestone-title">Арнайы бөбекжай-бақша және балабақша</span>
      </div>
      <p class="milestone-text">1 жастан · Арнайы бөбекжай-бақша. 3 жастан · арнайы балабақша.</p>
    </div>

    <!-- Отметка 2 (0-18 жас) -->
    <div class="milestone-card">
      <div class="milestone-head">
        <span class="milestone-badge">0–18 жас</span>
        <span class="milestone-title">ПМПК</span>
      </div>
      <p class="milestone-text">Баланың ерекше білім беру қажеттіліктері бағаланады.</p>
    </div>

    <!-- Отметка 1 (0 жас, начало пути) -->
    <div class="milestone-card featured">
      <div class="milestone-head">
        <span class="milestone-badge">0 жас</span>
        <span class="milestone-title">Скрининг</span>
      </div>
      <p class="milestone-text">Емханада баланың психофизикалық дамуы тексеріледі. <span class="ref">[ТЕКСЕРУ]</span></p>
    </div>
  </div>

  <!-- ==================== НИЖНЯЯ ПЛАШКА: ФАКТЫ, QR, ИСТОЧНИКИ ==================== -->
  <div class="bottom-plate z-content">
    <div class="facts-col">
      <div class="fact-item">
        <span class="fact-marker"></span>
        <p class="fact-text">Инклюзивті топта ЕББҚ бар балалар саны үшеуден аспайды.</p>
      </div>
      <div class="fact-item">
        <span class="fact-marker"></span>
        <p class="fact-text">Үйдегі даму бағдарламасы: отбасы да команданың мүшесі.</p>
      </div>
      <div class="sources-note">
        Дереккөздер: Дәріс 5; ННПЦ РСИО, 2023; adilet.zan.kz
      </div>
    </div>

    <div class="qr-col">
      <div class="qr-card">
        {qr_svg_clean}
      </div>
      <div class="qr-caption">ННПЦ РСИО әдістемелік ұсынымы</div>
    </div>
  </div>

</div>
</body>
</html>'''

with open('poster.html', 'w', encoding='utf-8') as f:
    f.write(html_content)

print('Generated poster.html successfully! Length:', len(html_content))
