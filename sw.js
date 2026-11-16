// 網路優先：有網路時永遠抓最新版，離線才用快取
const C='amt-v1';
const PRE=['./','index.html','manifest.webmanifest','icons/icon-192.png','icons/icon-512.png','icons/icon-180.png'];
self.addEventListener('install',e=>{e.waitUntil(caches.open(C).then(c=>Promise.all(PRE.map(u=>fetch(u,{cache:'reload'}).then(r=>{if(r&&r.ok&&r.type==='basic')return c.put(u,r)}).catch(()=>{})))).catch(()=>{}).then(()=>self.skipWaiting()))});
self.addEventListener('activate',e=>{e.waitUntil(caches.keys().then(k=>Promise.all(k.filter(x=>x!==C).map(x=>caches.delete(x)))).then(()=>caches.open(C)).then(c=>c.keys().then(rs=>Promise.all(rs.filter(r=>new URL(r.url).searchParams.has('v')).map(r=>c.delete(r))))).catch(()=>{}).then(()=>self.clients.claim()))});
self.addEventListener('fetch',e=>{
 const r=e.request;if(r.method!=='GET')return;const u=new URL(r.url);
 if(u.origin!==location.origin)return;
 if(u.searchParams.has('v'))return; // 更新檢查：直接連線，不存入快取
 e.respondWith(fetch(r,{cache:'no-store'}).then(res=>{if(res&&res.ok&&res.type==='basic'){const c=res.clone();caches.open(C).then(x=>x.put(r,c)).catch(()=>{})}return res}).catch(()=>caches.match(r).then(m=>m||caches.match('./'))));
});
