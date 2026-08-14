(()=>{'use strict';
function expandAllOptionExplanations(){
  document.querySelectorAll('.feedback details').forEach(detail=>{
    detail.open=true;
  });
}

const target=document.getElementById('app')||document.body;
new MutationObserver(expandAllOptionExplanations).observe(target,{childList:true,subtree:true});
expandAllOptionExplanations();
})();
