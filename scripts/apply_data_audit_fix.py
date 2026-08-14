#!/usr/bin/env python3
import json, hashlib
from copy import deepcopy
from pathlib import Path

PATH=Path("data.json")
FIXES={'GEN-2018-Q02': '摂食嚥下に関する筋群ならびに脳・神経のしくみについて、正しい組み合わせはどれか。\na．後輪状披裂筋 ― 嚥下時の声門閉鎖\nb．口蓋帆張筋 ― 鼻咽腔閉鎖\nc．皮質延髄路 ― 顔面・咽喉頭・頸部の運動\nd．上行性網様体賦活系 ― 筋緊張の調節', 'GEN-2018-Q05': '摂食嚥下機能の検査について、正しい組み合わせはどれか。\na．嚥下内視鏡検査は、口蓋帆の左右差を評価することができる。\nb．嚥下造影の正面像は、咽頭残留の左右差を評価することができる。\nc．超音波検査の前額断面画像は、舌の前方から後方にかけての動きを評価することができる。\nd．嚥下造影での嚥下反射の開始は、食塊の先端が第 3 頸椎を超えてからの時間で判断する。', 'GEN-2018-Q14': '成人のフィジカル・アセスメントについて、正しい組み合わせはどれか。\na．鼻声や嗄声の症状があったことから、迷走神経麻痺を疑った。\nb．嘔吐反射がなかったことから、舌咽神経麻痺を疑った。\nc．舌に萎縮があったことから、核上性の舌下神経麻痺を疑った。\nd．舌の右側に味覚障害があったことから、右側の三叉神経麻痺を疑った。', 'GEN-2018-Q08': '摂食嚥下障害に関連する高次脳機能障害とその責任病巣について、正しい組み合わせはどれか。\na．感覚性失語 ― 左前頭葉下部\nb．左半側空間失認 ― 右頭頂葉\nc．観念失行 ― 左頭頂葉\nd．記憶障害 ― 後頭葉', 'GEN-2018-Q17': '摂食訓練（直接訓練）について、正しい組み合わせはどれか。\na．キサンタンガム系のとろみ調整食品は、少量でとろみをつけられるが、においに変化が生じる。\nb．嚥下前頸部回旋は、嚥下前に回旋することで非回旋側の梨状窩（梨状陥凹）に食塊を誘導し誤嚥を防止する。\nc．嚥下の意識化は、嚥下を意識することで嚥下運動を確実にし、誤嚥や咽頭残留を防止する。\nd．息こらえ嚥下（Supraglottic swallow）は、意識的に息こらえをすることで嚥下後誤嚥を防止する。', 'GEN-2018-Q19': '呼吸のアセスメントと呼吸管理について、正しい組み合わせはどれか。\na．正常な肺胞呼吸音は、呼気相・吸気相が同等の大きさで聴取できる。\nb．粗い断続性ラ音が吸気・呼気で聴取された場合、気道内分泌物の貯留が疑われる。\nc．酸素解離曲線より、ヘモグロビンとの結合率が 90%の時の動脈血酸素分圧は、約 60mmHg である。\nd．左外側肺底区（S9）に分泌物の貯留がある場合、腹臥位のドレナージを行う。', 'GEN-2018-Q10': '神経筋疾患による摂食嚥下障害について、正しい組み合わせはどれか。\na．デュシェンヌ型筋ジストロフィーでは、初期に誤嚥を伴う咽頭期の嚥下障害がみられる。\nb．ギラン・バレー症候群では、口腔・咽頭の痙性麻痺による嚥下障害がみられる。\nc．筋萎縮性側索硬化症（ALS）では、嚥下関連筋群の筋疲労により嚥下障害がみられる。\nd．重症筋無力症では、クリーゼを認める場合に誤嚥のリスクが高い。', 'GEN-2018-Q11': '口腔・咽頭・喉頭癌術後の摂食嚥下障害について、正しい組み合わせはどれか。\na．拡大中咽頭切除術（後口蓋弓・舌根部切除）および遊離皮弁による再建術後は、咽頭期惹起が遅延する。\nb．Pull through 法で舌半側切除術が行われた場合、喉頭挙上運動が阻害される。\nc．下顎骨を切除した場合、再建術を行うことにより咬合のズレや咀嚼障害は回避できる。\nd．喉頭がんで喉頭半側切除を行った場合には、声門閉鎖不全が起こる。', 'GEN-2018-Q12': '高齢者の摂食嚥下障害について、正しい組み合わせはどれか。\na．嚥下後の呼吸は加齢に伴い呼気から始まる頻度が増加する。\nb．加齢に伴う臼歯の多数喪失は、舌による食塊を咽頭に送り込む力を弱くする。\nc．加齢に伴うサルコペニアでは、舌骨上筋群の速筋線維に選択的な萎縮を認める。\nd．高齢者では円背・亀背により腹部が圧迫され、胃食道逆流が起きやすい。', 'GEN-2018-Q13': '小児の摂食嚥下障害について、正しい組み合わせはどれか。\na．ダウン症候群では、筋の低緊張や高口蓋、乳歯の萌出遅延による水分誤嚥がみられる。\nb．重度の脳性麻痺では、むせを伴わない誤嚥や喉頭蓋谷、梨状窩（梨状陥凹）への食塊残留による誤嚥がみられる。\nc．先天性ミオパチーの重症乳児型では、重度の嚥下障害による誤嚥性肺炎、胃食道逆流および栄養障害がみられる。\nd．自閉・行動障害を伴う広汎性発達障害児は、成長・発育障害に至るほどの強い好き嫌い（偏食）がみられる。', 'GEN-2018-Q18': '小児における基礎訓練（間接訓練）・摂食訓練（直接訓練）について、正しい組み合わせはどれか。\na．ラッパやティッシュペーパーなどを吹く遊びは、鼻咽腔閉鎖の効果が期待できる。\nb．かんきつ類の果汁などを下唇の内側に塗る訓練は、嚥下促通効果が期待できる。\nc．指先で軽く触る刺激を繰り返す脱感作は、触覚過敏改善の効果が期待できる。\nd．液体の一回量をコントロールする練習は、コップ飲みから開始する。'}

with PATH.open(encoding="utf-8") as f:
    data=json.load(f)
before=deepcopy(data)
qmap={q["id"]:q for q in data["questions"]}
if len(data["questions"]) != 338 or len(qmap) != 338:
    raise SystemExit("invalid question count or duplicate IDs")
if set(FIXES) - set(qmap):
    raise SystemExit("missing target IDs")
for qid,new_text in FIXES.items():
    q=qmap[qid]
    if q.get("question_format") != "combination_4":
        raise SystemExit(f"{qid} is not combination_4")
    if [q.get("option_"+x) for x in "ABCD"] != ["a・b","a・d","b・c","c・d"]:
        raise SystemExit(f"{qid} combination choices changed unexpectedly")
    q["question_text"]=new_text

data["meta"]["dataVersion"]="2026-08-14-r2"

if sum(q.get("question_group")=="一般問題" for q in data["questions"]) != 178:
    raise SystemExit("general count mismatch")
if sum(q.get("question_group")=="状況設定・事例問題" for q in data["questions"]) != 160:
    raise SystemExit("case count mismatch")
for q in data["questions"]:
    if any(not q.get("option_"+x) for x in "ABCD"):
        raise SystemExit(f"missing choice: {q['id']}")
    if q.get("correct_answer") not in "ABCD":
        raise SystemExit(f"invalid correct_answer: {q['id']}")
for qid,new_text in FIXES.items():
    if qmap[qid]["question_text"] != new_text:
        raise SystemExit(f"fix failed: {qid}")

bmap={q["id"]:q for q in before["questions"]}
unchanged=sum(bmap[qid]==qmap[qid] for qid in bmap if qid not in FIXES)
if unchanged != 327:
    raise SystemExit(f"unexpected non-target change count: {unchanged}")

with PATH.open("w",encoding="utf-8") as f:
    json.dump(data,f,ensure_ascii=False,indent=2)
    f.write("\n")
raw=PATH.read_bytes()
print("validated=338")
print("general=178 case=160")
print("fixed=11 unchanged=327")
print("dataVersion="+data["meta"]["dataVersion"])
print("sha256="+hashlib.sha256(raw).hexdigest())
