from pathlib import Path
import json,hashlib,subprocess,math,re
import numpy as np
from PIL import Image,ImageDraw
import render as r
P=Path(__file__).parent;R=P/'render';ROOT=P.parent;O=ROOT/'02_项目成片/efficiency-after'
def dump(n,v):(R/n).write_text(json.dumps(v,ensure_ascii=False,indent=2),encoding='utf-8')
def norm(t):return ''.join(c for c in t if c.isalnum())
def content():
 rows=json.loads((P/'data/transcript-corrected.json').read_text(encoding='utf-8'));subs=r.subs
 assert norm(''.join(s['text'] for s in rows))==norm(''.join(s['text'] for s in subs))
 assert all(a['end']<=b['start'] for a,b in zip(subs,subs[1:]))
 assert all(0<=s['start']<s['end']<=r.duration for s in subs)
 assert all(abs(a['end']-b['start'])<1e-6 for a,b in zip(r.scenes,r.scenes[1:]))
 ids=sorted(set([0,r.TOTAL-1]+[round(s['start']*30) for s in r.scenes]+[v['frame'] for v in r.scene_module.CUES.values()]))
 hashes={i:hashlib.sha256(r.frame(i).tobytes()).hexdigest() for i in ids}
 assert all(hashlib.sha256(r.frame(i).tobytes()).hexdigest()==hashes[i] for i in reversed(ids))
 dump('determinism.json',hashes)
 src=Path('C:/ExampleWorkspace/example.mp3')
 assert src.read_bytes()==(P/'audio/narration.mp3').read_bytes()
 cover={}
 for p in (O/'封面').glob('*.png'):
  im=Image.open(p);cover[p.name]=im.size
  assert im.size in [(1200,1600),(1600,1200)]
  im.resize((240,round(240*im.height/im.width))).save(R/('thumb-'+p.name))
 maxwidth=max(r.font(66).getlength(s['text']) for s in subs)
 assert maxwidth<1690
 # Trace only main-image text, then compare it with the current subtitle.
 original=r.text;duplicate=[];checked=0
 for s in r.scenes:
  for t in [s['start']+.8,s['end']-.35]:
   main=[]
   def traced(d,xy,v,*args,**kwargs):
    main.append(v);return original(d,xy,v,*args,**kwargs)
   r.text=traced
   try:r.scene_image(s,t)
   finally:r.text=original
   caption=next((norm(c['text']) for c in subs if c['start']<=t<c['end']),'')
   for v in main:
    v=norm(v)
    if len(v)>=8 and v in caption:duplicate.append({'time':t,'text':v})
   checked+=1
 assert not duplicate,duplicate
 dump('content-audit.json',{'fullTranscriptCoverage':True,'subtitleOrderAndRange':True,'sceneCoverageContinuous':True,'subtitleCount':len(subs),'sceneBeats':len(r.scenes),'asrActionCues':len(r.scene_module.CUES),'deterministicFrames':len(ids),'sourceCopyIdentical':True,'maxSubtitleWidthAt66px':round(maxwidth,2),'mainTextSamples':checked,'exactLongDuplicates':duplicate,'covers':cover,'limitations':'自动识别与语境校正，非全文人工听写；八字检查不排除同义重复；静态小屏检查不代表真实手机'})
 # Source QA in groups, without requiring one very tall contact sheet.
 files=sorted(R.glob('scene-??-?.jpg'))
 for j in range(math.ceil(len(files)/20)):
  batch=files[j*20:(j+1)*20];out=Image.new('RGB',(1920,math.ceil(len(batch)/4)*270),r.BG)
  for i,p in enumerate(batch):out.paste(Image.open(p).resize((480,270)),((i%4)*480,(i//4)*270))
  out.save(R/f'source-review-{j}.jpg')
 times=[]
 for n in ['compress','document','three','deadline','instant','dozens','widen','congestion','own']:
  t=r.scene_module.CUES[n]['time'];times += [t-.1,t+.2,t+.55,t+1.1]
 for t in [46.18,76.36,116.60,139.06,149.98,162.54]:times += [t-.1,t+.1,t+.4]
 for j in range(math.ceil(len(times)/20)):
  batch=times[j*20:(j+1)*20];out=Image.new('RGB',(1920,math.ceil(len(batch)/4)*270),r.BG)
  for i,t in enumerate(batch):
   im=r.frame(round(t*30)).resize((480,270));d=ImageDraw.Draw(im);d.rectangle((0,0,110,25),fill=r.INK);d.text((3,3),f'{t:.2f}s',fill='white');out.paste(im,((i%4)*480,(i//4)*270))
  out.save(R/f'motion-cuts-{j}.jpg')
 print('Content and determinism passed',len(ids),flush=True)
def sync():
 final=O/'效率提高之后_完整版.mp4';result=[]
 for t in [5,45,85,125,175]:
  arrays=[]
  for path in [P/'audio/narration.mp3',final]:
   a=np.frombuffer(subprocess.check_output(['ffmpeg','-v','error','-ss',str(t),'-i',str(path),'-t','3','-ac','1','-ar','8000','-f','f32le','-']),dtype=np.float32);arrays.append(a)
  a,b=arrays;n=min(len(a),len(b));a=a[:n];b=b[:n];scores=[]
  for lag in range(-160,161):
   aa=a[max(0,-lag):min(n,n-lag)];bb=b[max(0,lag):min(n,n+lag)]
   scores.append(float(np.dot(aa,bb)/max(1e-10,np.linalg.norm(aa)*np.linalg.norm(bb))))
  lag=int(np.argmax(scores))-160;assert abs(lag)<=8 and max(scores)>.9,(t,lag,max(scores))
  result.append({'time':t,'offsetMs':lag/8,'correlation':max(scores),'reference':'原始口播MP3与最终成片AAC'})
 dump('sync-check.json',result);print(result,flush=True)
if __name__=='__main__':
 import sys
 if 'sync' in sys.argv:sync()
 else:content()
