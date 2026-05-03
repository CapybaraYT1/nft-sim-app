<!DOCTYPE html>
<html lang="ru">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Gift Store</title>
  <script src="https://telegram.org/js/telegram-web-app.js"></script>
  <style>
    * { margin: 0; padding: 0; box-sizing: border-box; }
    body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; background: #1a1a2e; color: #ffffff; min-height: 100vh; display: flex; flex-direction: column; }
    .header { padding: 16px 16px 12px; display: flex; align-items: center; justify-content: space-between; background: #1a1a2e; flex-shrink: 0; }
    .header h1 { font-size: 20px; font-weight: 700; }
    .stars-badge { background: #16213e; border: 1px solid #0f3460; color: #a78bfa; padding: 6px 14px; border-radius: 20px; font-size: 14px; font-weight: 700; }
    .page { display: none; flex: 1; overflow-y: auto; padding-bottom: 84px; }
    .page.active { display: block; }
    .section-title { padding: 16px 16px 10px; font-size: 12px; text-transform: uppercase; letter-spacing: 0.07em; color: #7878a0; font-weight: 700; }
    .gifts-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 12px; padding: 0 16px; }
    .gift-card { background: #16213e; border: 1px solid #0f3460; border-radius: 16px; padding: 18px 12px; display: flex; flex-direction: column; align-items: center; gap: 8px; cursor: pointer; transition: transform 0.12s; position: relative; }
    .gift-card:active { transform: scale(0.95); }
    .gift-card.sold-out { opacity: 0.4; pointer-events: none; }
    .gift-emoji { font-size: 50px; line-height: 1; }
    .gift-name { font-size: 13px; font-weight: 600; text-align: center; color: #e0e0ff; }
    .gift-supply { font-size: 11px; color: #7878a0; }
    .gift-price { font-size: 15px; font-weight: 700; color: #a78bfa; }
    .badge { position: absolute; top: 8px; right: 8px; font-size: 10px; font-weight: 700; padding: 2px 7px; border-radius: 8px; }
    .badge-sold { background: #ff3b30; color: #fff; }
    .task-list { padding: 0 16px; display: flex; flex-direction: column; gap: 10px; }
    .task-item { background: #16213e; border: 1px solid #0f3460; border-radius: 14px; padding: 16px; display: flex; align-items: center; gap: 14px; }
    .task-item.done { opacity: 0.5; }
    .task-icon { font-size: 32px; flex-shrink: 0; }
    .task-body { flex: 1; }
    .task-title { font-size: 15px; font-weight: 600; color: #e0e0ff; margin-bottom: 4px; }
    .task-desc { font-size: 12px; color: #7878a0; }
    .task-reward { font-size: 14px; font-weight: 700; color: #a78bfa; flex-shrink: 0; text-align: right; }
    .task-check { font-size: 22px; flex-shrink: 0; }
    .btn-task { flex-shrink: 0; background: #a78bfa; color: #1a1a2e; border: none; border-radius: 10px; padding: 8px 14px; font-size: 13px; font-weight: 700; cursor: pointer; }
    .btn-task:disabled { opacity: 0.4; cursor: not-allowed; }
    .profile-card { margin: 16px; background: #16213e; border: 1px solid #0f3460; border-radius: 18px; padding: 24px 20px; display: flex; flex-direction: column; align-items: center; gap: 10px; }
    .profile-photo { width: 72px; height: 72px; border-radius: 50%; object-fit: cover; }
    .profile-avatar-fallback { width: 72px; height: 72px; border-radius: 50%; background: linear-gradient(135deg, #a78bfa, #0f3460); display: flex; align-items: center; justify-content: center; font-size: 32px; }
    .profile-name { font-size: 20px; font-weight: 700; color: #e0e0ff; }
    .profile-username { font-size: 13px; color: #7878a0; }
    .owned-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 10px; padding: 0 16px 16px; }
    .owned-card { background: #16213e; border: 1px solid #0f3460; border-radius: 16px; aspect-ratio: 1; display: flex; align-items: center; justify-content: center; position: relative; overflow: hidden; cursor: pointer; }
    .owned-card-emoji { font-size: 40px; }
    .owned-serial { position: absolute; top: 6px; right: -10px; font-size: 9px; color: #7878a0; font-weight: 700; transform: rotate(45deg); white-space: nowrap; }
    .owned-upgraded { position: absolute; bottom: 4px; left: 4px; font-size: 8px; color: #a78bfa; font-weight: 700; }
    .market-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 12px; padding: 0 16px; }
    .market-card { background: #16213e; border: 1px solid #0f3460; border-radius: 16px; padding: 16px 12px 14px; display: flex; flex-direction: column; align-items: center; gap: 7px; position: relative; }
    .btn-upgrade { width: 100%; background: transparent; border: 1px solid #a78bfa; color: #a78bfa; border-radius: 10px; padding: 7px; font-size: 12px; font-weight: 700; cursor: pointer; margin-top: 4px; }
    .state-msg { text-align: center; padding: 60px 20px; color: #7878a0; font-size: 15px; line-height: 1.6; }
    .state-msg.error { color: #ff6b6b; }
    .tab-bar { position: fixed; bottom: 0; left: 0; right: 0; background: #16213e; border-top: 1px solid #0f3460; display: flex; z-index: 50; padding-bottom: env(safe-area-inset-bottom, 0px); }
    .tab-item { flex: 1; display: flex; flex-direction: column; align-items: center; justify-content: center; padding: 10px 0 8px; cursor: pointer; gap: 3px; color: #555580; border: none; background: transparent; transition: color 0.15s; }
    .tab-item.active { color: #a78bfa; }
    .tab-icon { font-size: 22px; }
    .tab-label { font-size: 10px; font-weight: 600; }
    .modal-overlay { display: none; position: fixed; inset: 0; background: rgba(0,0,0,0.65); z-index: 100; align-items: flex-end; }
    .modal-overlay.open { display: flex; }
    .modal { background: #16213e; border-top: 1px solid #0f3460; border-radius: 24px 24px 0 0; padding: 28px 20px 44px; width: 100%; }
    .modal-emoji { font-size: 64px; text-align: center; margin-bottom: 14px; }
    .modal h2 { font-size: 21px; font-weight: 700; color: #e0e0ff; margin-bottom: 4px; }
    .modal-sub { color: #7878a0; font-size: 13px; margin-bottom: 20px; }
    .modal-price { font-size: 30px; font-weight: 800; color: #a78bfa; text-align: center; margin-bottom: 24px; }
    .btn-primary { width: 100%; padding: 16px; border: none; border-radius: 14px; font-size: 17px; font-weight: 700; cursor: pointer; background: #a78bfa; color: #1a1a2e; }
    .btn-primary:disabled { opacity: 0.45; cursor: not-allowed; }
    .btn-secondary { width: 100%; padding: 14px; border: none; border-radius: 14px; font-size: 15px; font-weight: 600; cursor: pointer; background: transparent; color: #7878a0; margin-top: 8px; }
  </style>
</head>
<body>
  <div class="header"><h1>🎁 Gift Store</h1><div class="stars-badge" id="stars-badge">⭐ —</div></div>

  <div class="page active" id="page-gifts">
    <div class="section-title">Доступные подарки</div>
    <div id="gifts-container" class="state-msg">Загрузка…</div>
  </div>

  <div class="page" id="page-tasks">
    <div class="section-title">Выполняй задания — получай звёзды</div>
    <div id="tasks-container" class="state-msg">Загрузка…</div>
  </div>

  <div class="page" id="page-market">
    <div class="section-title">Мои подарки</div>
    <div id="market-container" class="state-msg">Загрузка…</div>
  </div>

  <div class="page" id="page-profile">
    <div class="profile-card" id="profile-card">
      <img id="profile-photo" class="profile-photo" src="" style="display:none" onerror="this.style.display='none';document.getElementById('profile-fallback').style.display='flex'"/>
      <div class="profile-avatar-fallback" id="profile-fallback">👤</div>
      <div class="profile-name" id="profile-name">—</div>
      <div class="profile-username" id="profile-username"></div>
    </div>
    <div class="section-title">Все подарки</div>
    <div id="profile-gifts"></div>
  </div>

  <nav class="tab-bar">
    <button class="tab-item active" onclick="switchTab('gifts',this)"><span class="tab-icon">🎁</span><span class="tab-label">Подарки</span></button>
    <button class="tab-item" onclick="switchTab('tasks',this)"><span class="tab-icon">✅</span><span class="tab-label">Задания</span></button>
    <button class="tab-item" onclick="switchTab('market',this)"><span class="tab-icon">🛒</span><span class="tab-label">Маркет</span></button>
    <button class="tab-item" onclick="switchTab('profile',this)"><span class="tab-icon">👤</span><span class="tab-label">Профиль</span></button>
  </nav>

  <div class="modal-overlay" id="modal-buy" onclick="closeBuyModal(event)">
    <div class="modal">
      <div class="modal-emoji" id="buy-emoji"></div>
      <h2 id="buy-name"></h2>
      <div class="modal-sub" id="buy-supply"></div>
      <div class="modal-price" id="buy-price"></div>
      <button class="btn-primary" id="btn-buy" onclick="confirmBuy()">Купить</button>
      <button class="btn-secondary" onclick="closeBuyModal()">Отмена</button>
    </div>
  </div>

  <div class="modal-overlay" id="modal-upgrade" onclick="closeUpgradeModal(event)">
    <div class="modal">
      <div class="modal-emoji" id="upg-emoji"></div>
      <h2 id="upg-name"></h2>
      <div class="modal-sub">Улучшение сделает подарок уникальным</div>
      <div class="modal-price">⭐ 25</div>
      <button class="btn-primary" id="btn-upgrade" onclick="confirmUpgrade()">Улучшить за ⭐ 25</button>
      <button class="btn-secondary" onclick="closeUpgradeModal()">Отмена</button>
    </div>
  </div>

  <script>
    const tg = window.Telegram.WebApp;
    tg.ready();
    tg.expand();

    let currentUser = null, selectedGift = null, selectedUserGift = null;
    const tgUser = tg.initDataUnsafe?.user;
    const loaded = {};

    function switchTab(name, el) {
      document.querySelectorAll('.page').forEach(p => p.classList.remove('active'));
      document.querySelectorAll('.tab-item').forEach(t => t.classList.remove('active'));
      document.getElementById('page-' + name).classList.add('active');
      el.classList.add('active');
      if (!loaded[name]) { loaded[name] = true; loadTab(name); }
    }

    function loadTab(name) {
      if (name === 'tasks') loadTasks();
      if (name === 'market') loadMarket();
      if (name === 'profile') loadProfile();
    }

    async function fetchJSON(url) {
      const r = await fetch(url);
      return r.json();
    }

    async function postJSON(url, body) {
      const r = await fetch(url, { method: 'POST', headers: {'Content-Type':'application/json'}, body: JSON.stringify(body) });
      return r.json();
    }

    function esc(s) { return String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;'); }
    function enc(g) { return encodeURIComponent(JSON.stringify(g)); }

    function setStars(n) {
      if (currentUser) currentUser.stars = n;
      document.getElementById('stars-badge').textContent = '⭐ ' + n;
    }

    async function init() {
      if (tgUser) {
        try {
          const startParam = tg.initDataUnsafe?.start_param || '';
          const referrer_id = startParam.startsWith('ref_') ? Number(startParam.replace('ref_', '')) : null;
          const res = await fetch('/user', { method: 'POST', headers: {'Content-Type':'application/json'}, body: JSON.stringify({ id: tgUser.id, username: tgUser.username || tgUser.first_name, referrer_id }) });
          currentUser = await res.json();
          setStars(currentUser.stars ?? 0);
        } catch(e) { console.error('User init:', e); }
      } else {
        document.getElementById('stars-badge').textContent = '⭐ Гость';
      }
      loadGifts();
    }

    async function loadGifts() {
      const c = document.getElementById('gifts-container');
      c.className = 'state-msg'; c.textContent = 'Загрузка…';
      try {
        const gifts = await fetchJSON('/gifts');
        if (!gifts.length) { c.textContent = 'Подарки пока недоступны.'; return; }
        c.className = 'gifts-grid';
        c.innerHTML = gifts.map(g => {
          const remaining = g.total_supply - g.sold;
          const out = remaining <= 0;
          return `<div class="gift-card${out?' sold-out':''}" onclick="openBuyModal('${enc(g)}')">${out?'<span class="badge badge-sold">Нет</span>':''}<div class="gift-emoji">${g.emoji||'🎁'}</div><div class="gift-name">${esc(g.name)}</div><div class="gift-supply">${remaining}/${g.total_supply}</div><div class="gift-price">⭐ ${g.price}</div></div>`;
        }).join('');
      } catch(e) { c.className = 'state-msg error'; c.textContent = 'Ошибка загрузки.'; }
    }

    function openBuyModal(encoded) {
      selectedGift = JSON.parse(decodeURIComponent(encoded));
      document.getElementById('buy-emoji').textContent = selectedGift.emoji || '🎁';
      document.getElementById('buy-name').textContent = selectedGift.name;
      document.getElementById('buy-supply').textContent = `Осталось: ${selectedGift.total_supply - selectedGift.sold} шт.`;
      document.getElementById('buy-price').textContent = '⭐ ' + selectedGift.price;
      document.getElementById('modal-buy').classList.add('open');
    }

    function closeBuyModal(e) {
      if (!e || e.target === document.getElementById('modal-buy')) {
        document.getElementById('modal-buy').classList.remove('open');
        selectedGift = null;
      }
    }

    async function confirmBuy() {
      if (!selectedGift || !currentUser) { tg.showAlert('Войдите через Telegram.'); return; }
      const btn = document.getElementById('btn-buy');
      btn.disabled = true; btn.textContent = 'Обработка…';
      try {
        const data = await postJSON('/buy_gift', { user_id: currentUser.id, gift_id: selectedGift.id });
        if (data.error) { tg.showAlert(data.error); }
        else { setStars(data.stars_left); closeBuyModal(); tg.showAlert('Подарок куплен! 🎉'); loadGifts(); loaded.market = false; loaded.profile = false; }
      } catch(e) { tg.showAlert('Ошибка. Попробуйте снова.'); }
      finally { btn.disabled = false; btn.textContent = 'Купить'; }
    }

    async function loadTasks() {
      const c = document.getElementById('tasks-container');
      c.className = 'state-msg'; c.textContent = 'Загрузка…';
      if (!currentUser) { c.textContent = 'Войдите через Telegram.'; return; }
      try {
        const tasks = await fetchJSON(`/tasks/${currentUser.id}`);
        if (!tasks.length) { c.textContent = 'Задания скоро появятся!'; return; }
        c.className = 'task-list';
        c.innerHTML = tasks.map(t => `<div class="task-item${t.done?' done':''}" id="task-${t.id}"><div class="task-icon">${t.emoji||'⭐'}</div><div class="task-body"><div class="task-title">${esc(t.title)}</div><div class="task-desc">${esc(t.description||'')}</div></div><div class="task-reward">+⭐${t.reward}</div>${t.done?'<div class="task-check">✅</div>':`<button class="btn-task" onclick="doTask(${t.id},${t.reward},this)">Выполнить</button>`}</div>`).join('');
      } catch(e) { c.className = 'state-msg error'; c.textContent = 'Ошибка загрузки заданий.'; }
    }

    async function doTask(taskId, reward, btn) {
      const row = document.getElementById('task-' + taskId);
      const title = row?.querySelector('.task-title')?.textContent || '';
      if (title === 'Подписаться на канал') {
        window.open('https://t.me/cat_zz', '_blank', 'noopener,noreferrer');
        btn.disabled = true; btn.textContent = 'Проверяем…';
        setTimeout(async () => {
          try {
            const data = await postJSON('/complete_task', { user_id: currentUser.id, task_id: taskId });
            if (data.error) { tg.showAlert(data.error); btn.disabled = false; btn.textContent = 'Выполнить'; return; }
            setStars(data.stars);
            row.classList.add('done');
            row.querySelector('.btn-task')?.remove();
            const chk = document.createElement('div'); chk.className = 'task-check'; chk.textContent = '✅'; row.appendChild(chk);
            tg.showAlert(`+⭐${reward} начислено!`);
            loaded.profile = false;
          } catch(e) { tg.showAlert('Ошибка.'); btn.disabled = false; btn.textContent = 'Выполнить'; }
        }, 3000);
        return;
      }
      if (title === 'Пригласить друга') {
        window.open('https://t.me/share/url?url=https://t.me/nftsim_bot?start=ref_' + currentUser.id + '&text=Присоединяйся к NFT Gift симулятору!');
        btn.disabled = true; btn.textContent = 'Ждём друга…';
        return;
      }
      btn.disabled = true; btn.textContent = '…';
      try {
        const data = await postJSON('/complete_task', { user_id: currentUser.id, task_id: taskId });
        if (data.error) { tg.showAlert(data.error); btn.disabled = false; btn.textContent = 'Выполнить'; return; }
        setStars(data.stars);
        row.classList.add('done');
        row.querySelector('.btn-task')?.remove();
        const chk = document.createElement('div'); chk.className = 'task-check'; chk.textContent = '✅'; row.appendChild(chk);
        tg.showAlert(`+⭐${reward} начислено!`);
        loaded.profile = false;
      } catch(e) { tg.showAlert('Ошибка.'); btn.disabled = false; btn.textContent = 'Выполнить'; }
    }

    async function loadMarket() {
      const c = document.getElementById('market-container');
      c.className = 'state-msg'; c.textContent = 'Загрузка…';
      if (!currentUser) { c.textContent = 'Войдите через Telegram.'; return; }
      try {
        const gifts = await fetchJSON('/user_gifts/' + currentUser.id);
        if (!gifts.length) { c.textContent = 'У вас пока нет подарков.'; return; }
        c.className = 'market-grid';
        c.innerHTML = gifts.map(g => `<div class="market-card"><div class="gift-emoji">${g.gifts?.emoji||'🎁'}</div><div class="gift-name">${esc(g.gifts?.name||'')}</div><div class="market-number">#${g.number_in_collection}</div>${g.is_upgraded?'<div style="color:#a78bfa;font-size:11px;font-weight:700">✨ Улучшен</div>':`<button class="btn-upgrade" onclick="openUpgradeModal('${enc(g)}')">✨ Улучшить ⭐25</button>`}</div>`).join('');
      } catch(e) { c.className = 'state-msg error'; c.textContent = 'Ошибка загрузки.'; }
    }

    function openUpgradeModal(encoded) {
      selectedUserGift = JSON.parse(decodeURIComponent(encoded));
      document.getElementById('upg-emoji').textContent = selectedUserGift.gifts?.emoji || '🎁';
      document.getElementById('upg-name').textContent = selectedUserGift.gifts?.name || '';
      document.getElementById('modal-upgrade').classList.add('open');
    }

    function closeUpgradeModal(e) {
      if (!e || e.target === document.getElementById('modal-upgrade')) {
        document.getElementById('modal-upgrade').classList.remove('open');
        selectedUserGift = null;
      }
    }

    async function confirmUpgrade() {
      if (!selectedUserGift || !currentUser) return;
      const btn = document.getElementById('btn-upgrade');
      btn.disabled = true; btn.textContent = 'Обработка…';
      try {
        const data = await postJSON('/upgrade_gift', { user_id: currentUser.id, user_gift_id: selectedUserGift.id });
        if (data.error) { tg.showAlert(data.error); }
        else { setStars(currentUser.stars - 25); closeUpgradeModal(); tg.showAlert('✨ Подарок улучшен!'); loaded.market = false; loaded.profile = false; }
      } catch(e) { tg.showAlert('Ошибка.'); }
      finally { btn.disabled = false; btn.textContent = 'Улучшить за ⭐ 25'; }
    }

    async function loadProfile() {
      if (!currentUser) return;
      if (tgUser?.photo_url) {
        const img = document.getElementById('profile-photo');
        img.src = tgUser.photo_url;
        img.style.display = 'block';
        document.getElementById('profile-fallback').style.display = 'none';
      }
      document.getElementById('profile-name').textContent = tgUser?.first_name || currentUser.username || '—';
      document.getElementById('profile-username').textContent = tgUser?.username ? '@' + tgUser.username : '';
      const c = document.getElementById('profile-gifts');
      try {
        const gifts = await fetchJSON('/user_gifts/' + currentUser.id);
        if (!gifts.length) { c.innerHTML = ''; return; }
        c.className = 'owned-grid';
        c.innerHTML = gifts.map(g => `<div class="owned-card"><div class="owned-serial">#${g.number_in_collection}</div><div class="owned-card-emoji">${g.gifts?.emoji||'🎁'}</div>${g.is_upgraded?'<div class="owned-upgraded">✨</div>':''}</div>`).join('');
      } catch(e) { c.innerHTML = ''; }
    }

    init();
  </script>
</body>
</html>
