(async()=>{
 try{
  const names=['./app.part1','./app.part2'];
  const parts=await Promise.all(names.map(async n=>{const r=await fetch(n,{cache:'no-store'});if(!r.ok)throw new Error(n+' を取得できませんでした（HTTP '+r.status+'）');return r.text();}));
  (0,eval)(parts.join(''));
 }catch(e){console.error(e);const root=document.getElementById('app');if(root)root.innerHTML='<div class="boot"><div><strong>アプリを読み込めませんでした</strong><p>'+String(e.message||e)+'</p></div></div>';}
})();
