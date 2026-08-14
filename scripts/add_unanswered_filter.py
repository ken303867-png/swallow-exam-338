from pathlib import Path


def replace_once(text, old, new, label):
    count = text.count(old)
    if count != 1:
        raise SystemExit(f'{label}: expected 1 match, found {count}')
    return text.replace(old, new, 1)

p1 = Path('app.part1')
s1 = p1.read_text(encoding='utf-8')

s1 = replace_once(
    s1,
    "const st=view.setup||{group,review,dataset:'all',domain:'all',importance:'all',order:'random',count:isCase?'5':'20'};",
    "const st=view.setup||{group,review,dataset:'all',domain:'all',importance:'all',answerStatus:'all',order:'random',count:isCase?'5':'20'};",
    'setup default answerStatus'
)

old_ui = "   <label class=\"field\"><span>重要度</span><select id=\"importance\"><option value=\"all\">すべて</option>${['S+','S','A','B'].map(x=>`<option value=\"${x}\"${st.importance===x?' selected':''}>${x}</option>`).join('')}</select></label>\n   <label class=\"field\"><span>${st.group==='状況設定・事例問題'&&!st.review?'出題事例数':'出題問題数'}</span><select id=\"count\">"
new_ui = "   <label class=\"field\"><span>重要度</span><select id=\"importance\"><option value=\"all\">すべて</option>${['S+','S','A','B'].map(x=>`<option value=\"${x}\"${st.importance===x?' selected':''}>${x}</option>`).join('')}</select></label>\n   ${!st.review?`<label class=\"field\"><span>回答状況</span><select id=\"answerStatus\"><option value=\"all\"${(st.answerStatus||'all')==='all'?' selected':''}>すべての問題</option><option value=\"unanswered\"${st.answerStatus==='unanswered'?' selected':''}>未回答の問題のみ</option></select></label>`:''}\n   <label class=\"field\"><span>${st.group==='状況設定・事例問題'&&!st.review?'出題事例数':'出題問題数'}</span><select id=\"count\">"
s1 = replace_once(s1, old_ui, new_ui, 'answer status UI')

s1 = replace_once(
    s1,
    " if(st.importance!=='all')arr=arr.filter(q=>q.importance===st.importance);\n if(st.review==='wrong')arr=arr.filter(q=>(existingProg(q.id)?.incorrectCount||0)>0);",
    " if(st.importance!=='all')arr=arr.filter(q=>q.importance===st.importance);\n if(!st.review&&st.answerStatus==='unanswered')arr=arr.filter(q=>(existingProg(q.id)?.attempts||0)===0);\n if(st.review==='wrong')arr=arr.filter(q=>(existingProg(q.id)?.incorrectCount||0)>0);",
    'unanswered filter'
)

p1.write_text(s1, encoding='utf-8')

p2 = Path('app.part2')
s2 = p2.read_text(encoding='utf-8')

s2 = replace_once(
    s2,
    "view={name:'setup',setup:{group:b.dataset.start,review:null,dataset:'all',domain:'all',importance:'all',order:'random',count:b.dataset.start==='状況設定・事例問題'?'5':'20'}};render()",
    "view={name:'setup',setup:{group:b.dataset.start,review:null,dataset:'all',domain:'all',importance:'all',answerStatus:'all',order:'random',count:b.dataset.start==='状況設定・事例問題'?'5':'20'}};render()",
    'home study setup'
)

# There are two review setup constructors with the same structure: home review and result review.
old_review = "setup:{group:'all',review:b.dataset.review,dataset:'all',domain:'all',importance:'all',order:'random',count:'20'}"
new_review = "setup:{group:'all',review:b.dataset.review,dataset:'all',domain:'all',importance:'all',answerStatus:'all',order:'random',count:'20'}"
if s2.count(old_review) != 1:
    raise SystemExit(f'home review setup: expected 1 match, found {s2.count(old_review)}')
s2 = s2.replace(old_review, new_review, 1)

old_update = "view.setup={...old,group,dataset:document.querySelector('#dataset').value,domain:document.querySelector('#domain').value,importance:document.querySelector('#importance').value,count:document.querySelector('#count').value,order:document.querySelector('#order').value};"
new_update = "view.setup={...old,group,dataset:document.querySelector('#dataset').value,domain:document.querySelector('#domain').value,importance:document.querySelector('#importance').value,answerStatus:document.querySelector('#answerStatus')?.value||old.answerStatus||'all',count:document.querySelector('#count').value,order:document.querySelector('#order').value};"
s2 = replace_once(s2, old_update, new_update, 'setup update answerStatus')

s2 = replace_once(
    s2,
    "['group','dataset','domain','importance','count','order'].forEach",
    "['group','dataset','domain','importance','answerStatus','count','order'].forEach",
    'setup change listeners'
)

s2 = replace_once(
    s2,
    "view={name:'setup',setup:{group:'all',review:'wrong',dataset:'all',domain:'all',importance:'all',order:'random',count:'20'}};render()",
    "view={name:'setup',setup:{group:'all',review:'wrong',dataset:'all',domain:'all',importance:'all',answerStatus:'all',order:'random',count:'20'}};render()",
    'result review setup'
)

p2.write_text(s2, encoding='utf-8')

sw = Path('sw.js')
sw_text = sw.read_text(encoding='utf-8')
sw_text = replace_once(
    sw_text,
    "const CACHE='swallow-exam-338-v5-explanation-data';",
    "const CACHE='swallow-exam-338-v6-unanswered-filter';",
    'service worker cache'
)
sw.write_text(sw_text, encoding='utf-8')

print('patched app.part1, app.part2, sw.js')
