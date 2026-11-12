from pathlib import Path
import json,subprocess,hashlib,math
P=Path(__file__).parent;ROOT=P.parent
def dump(n,v):(P/'data'/n).write_text(json.dumps(v,ensure_ascii=False,indent=2),encoding='utf-8')
raw=json.loads((P/'data/transcript-raw.json').read_text(encoding='utf-8'))
fix={'这事件好事':'这是一件好事','做的更多':'做得更多','整理文字 调整排版':'整理文字、调整排版','不过 这里还有一个问题':'不过，这里还有一个问题'}
rows=[];changes=[]
for s in raw:
 txt=s['text'].strip()
 for a,b in fix.items():txt=txt.replace(a,b)
 if txt!=s['text']:changes.append({'start':s['start'],'before':s['text'],'after':txt,'reason':'语境/标点校正，非人工全文听写'})
 rows.append({**s,'text':txt})
dump('transcript-corrected.json',rows);dump('corrections.json',changes)
(P/'data/口播稿.txt').write_text('\n'.join(s['text'] for s in rows),encoding='utf-8')
subs=[]
for s in rows:
 if subs and s['start']-subs[-1]['end']<.7 and len(subs[-1]['text'])+len(s['text'])<=22 and s['end']-subs[-1]['start']<4.8:
  subs[-1]['text']+='，'+s['text'];subs[-1]['end']=s['end']
 else:subs.append({k:s[k] for k in ['start','end','text']})
dump('subtitles.json',subs)
D=float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','default=nw=1:nk=1',str(P/'audio/narration.mp3')]))
(P/'data/duration.txt').write_text(str(D))
cue_specs=[('research',9.46,'查资料'),('layout',10.96,'调整'),('ai',14.66,'AI'),('compress',16.22,'半'),('rest',18.54,'休息'),('document',22.48,'修改'),('notes',24.42,'笔记'),('other',25.96,'任务'),('four',29.92,'三四'),('reportfast',51.46,'两个小时'),('three',62.42,'三份'),('assign',64.28,'安排'),('deadline',68.14,'半天'),('email',85.18,'邮件'),('instant',91.30,'秒'),('progress',95.02,'进度'),('details',96.86,'细节'),('requests',97.82,'要求'),('dozens',102.20,'几十'),('widen',121.26,'扩建'),('forty',122.56,'40'),('saved',125.60,'20'),('drivers',129.70,'人'),('cars',133.26,'增加'),('congestion',136.74,'拥堵'),('more',169.64,'任务'),('own',171.10,'自己')]
cues={}
for name,near,keyword in cue_specs:
 row=min(raw,key=lambda s:abs(s['start']-near));joined='';spans=[]
 for w in row['words']:
  a=len(joined);joined+=w['word'];spans.append((a,len(joined),w))
 pos=joined.find(keyword)
 if pos<0:
  # Numeric words may be represented as Chinese characters by the word tokenizer.
  if keyword=='40':pos=joined.find('四十')
  if keyword=='20':pos=joined.find('二十')
 assert pos>=0,(name,joined,keyword)
 w=next(w for a,b,w in spans if a<=pos<b)
 cues[name]={'time':w['start'],'frame':round(w['start']*30),'keyword':keyword,'word':w['word'],'source':'ASR词起点，未经人工强制对齐','offset':0}
dump('cues.json',cues)
spec=[
(0,'desk','同一工作台：任务、时钟与两小时窗口'),(7.68,'desk','屏幕内建立PPT，查资料/文字/排版依语音展开'),(14.66,'desk','AI入口出现，同一PPT完成'),(16.22,'desk','任务占用从两小时平滑压缩为半小时'),(18.54,'desk','余下一个半小时形成绿色空档'),(22.48,'desk','另一份文档从待办托盘进入空档'),(24.42,'desk','笔记进入第三个时间格'),(25.96,'desk','其他任务进入第四格'),(29.92,'desk','同样两小时完成四件，休息空档已填满'),(34.42,'desk','任务总量与单件速度分开看'),
(38.86,'question','保留PPT与空档，外部安排的入口出现'),(46.18,'office','同一办公空间换成报告任务与交付日历'),(50.04,'office','AI使报告完成耗时变为两个小时'),(57.06,'office','负责人观察完成能力，待办增加'),(62.42,'office','同一任务架出现三份报告'),(64.28,'office','新工作安排落入交付日历'),(68.14,'office','交付期限从一天收缩至半天'),(70.86,'office','已完成能力转为当前要求，报告保持三份'),
(76.36,'messages','转入同一沟通窗口，邮件和等待'),(83.78,'messages','半天一次的邮件流'),(90.02,'messages','邮件变为消息，几秒送达'),(95.02,'messages','进度/细节/新要求依次到来'),(99.18,'messages','相同话题的消息队列从几次堆到数十次'),(104.34,'messages','小时间片累积占满时间带'),(109,'messages','单次成本和发生次数对照'),
(116.60,'road','家与公司之间建立原道路，通勤六十分钟'),(121.26,'road','原道路扩建，车道增加'),(122.56,'road','通勤变为四十分钟，显示节省二十分钟'),(127.72,'road','支路上的车辆汇入，路线保持'),(133.26,'road','密度增加，车速变慢'),(136.74,'road','新增拥堵占用原先节省的时间，未设定新通勤数字'),(139.06,'mechanism','时间带连起成本降低、行为增加、收益被消耗'),
(149.98,'recap','PPT/报告/消息/道路依次回看同一种变化'),(156,'recap','单次速度提高与总任务量分别表示'),(162.54,'end','回到开场PPT和一个半小时的时间空档'),(166.64,'end','时间从同一空档连向两个选项'),(169.64,'end','更多任务与自主时间保持并列，不替观众选择'),(173.24,'end','已完成PPT与保留的空档留在桌面收尾')]
scenes=[{'start':a,'end':spec[i+1][0] if i+1<len(spec) else D,'kind':b,'tag':c} for i,(a,b,c) in enumerate(spec)]
dump('scenes.json',scenes)
dump('project.json',{'title':'效率提高之后','source':'效率提高之后_口播_爽朗少年_1.18x_20261020.mp3','duration':D,'fps':30,'frames':math.ceil(D*30),'sourceSha256':hashlib.sha256((P/'audio/narration.mp3').read_bytes()).hexdigest(),'references':['ref-3b1370f955be','ref-beeabc60c2a1','ref-23566852e0c3'],'status':'制作中，未发布'})
O=ROOT/'02_项目成片/efficiency-after';O.mkdir(parents=True,exist_ok=True)
def stamp(t):
 m=round(t*1000);return f'{m//3600000:02}:{m//60000%60:02}:{m//1000%60:02},{m%1000:03}'
(O/'字幕.srt').write_text('\n\n'.join(f"{i+1}\n{stamp(s['start'])} --> {stamp(s['end'])}\n{s['text']}" for i,s in enumerate(subs)),encoding='utf-8')
(P/'分镜.md').write_text('# 效率提高之后 · 策划与分镜\n\n主问题：为什么工具更快了，我们却没有因此更轻松？\n标题候选：效率提高之后 / 效率提高了，怎么还更忙？ / 省下来的时间，去哪了？\n贯穿对象：同一条可分配时间带与待办托盘。先压缩单件任务，再用新增任务、要求、消息及车流展示总量变化。\n封面：PPT从2小时压缩到0.5小时，余下时间被文档/笔记/其他任务填入，白狐观察消失的绿色空档。\n数字与边界：均为原口播假设案例，不表示真实公司、AI模型实测或道路研究。一天不换算成固定小时；道路拥堵段不编造最终通勤时间；无普遍必然结论。\n全部原声与输入速度保留。主画面只有短标签、数字、界面与对象；完整句子只放字幕。\n\n|时间|贯穿空间|变化与结果|\n|---|---|---|\n'+'\n'.join(f"|{s['start']:.2f}–{s['end']:.2f}|{s['kind']}|{s['tag']}|" for s in scenes),encoding='utf-8')
assert all(0<=s['start']<s['end']<=D for s in subs)
assert all(a['end']<=b['start'] for a,b in zip(subs,subs[1:]))
print('duration',D,'scenes',len(scenes),'subtitles',len(subs),'ASR cues',len(cues))
