(()=>{'use strict';
let selected=null;
let passThrough=false;
let syncing=false;

function currentQuestionText(){
  return document.querySelector('.q-text')?.textContent?.trim()||'';
}

function addStyle(){
  if(document.getElementById('answer-confirm-style'))return;
  const s=document.createElement('style');
  s.id='answer-confirm-style';
  s.textContent='.answer-confirm-wrap{margin:12px 0}.answer-confirm-wrap .btn:disabled{opacity:.45;cursor:not-allowed}';
  document.head.appendChild(s);
}

function ensureConfirm(){
  const options=document.querySelector('.options');
  const choiceButtons=[...document.querySelectorAll('.option[data-choice]')];
  if(!options||!choiceButtons.length)return;
  if(choiceButtons.some(b=>b.disabled)||document.querySelector('.feedback')){
    document.querySelector('.answer-confirm-wrap')?.remove();
    return;
  }

  const qText=currentQuestionText();
  if(selected&&selected.questionText!==qText)selected=null;

  choiceButtons.forEach(b=>b.classList.toggle('selected',!!selected&&b.dataset.choice===selected.choice));

  let wrap=document.querySelector('.answer-confirm-wrap');
  if(!wrap){
    wrap=document.createElement('div');
    wrap.className='answer-confirm-wrap';
    wrap.innerHTML='<button class="btn primary block" id="answerConfirm" type="button" disabled>解答確定</button>';
    options.insertAdjacentElement('afterend',wrap);
  }
  const confirmBtn=wrap.querySelector('#answerConfirm');
  confirmBtn.disabled=!selected;
  confirmBtn.onclick=()=>{
    if(!selected)return;
    const target=[...document.querySelectorAll('.option[data-choice]')].find(b=>b.dataset.choice===selected.choice&&!b.disabled);
    if(!target)return;
    selected=null;
    passThrough=true;
    try{target.click();}finally{passThrough=false;}
  };
}

function scheduleSync(){
  if(syncing)return;
  syncing=true;
  requestAnimationFrame(()=>{syncing=false;ensureConfirm();});
}

document.addEventListener('click',e=>{
  const btn=e.target.closest?.('.option[data-choice]');
  if(!btn||passThrough||btn.disabled)return;
  e.preventDefault();
  e.stopImmediatePropagation();
  selected={questionText:currentQuestionText(),choice:btn.dataset.choice};
  ensureConfirm();
},true);

addStyle();
new MutationObserver(scheduleSync).observe(document.getElementById('app')||document.body,{childList:true,subtree:true});
scheduleSync();
})();
