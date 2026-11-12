from pathlib import Path
import subprocess,json,re,sys,shutil,hashlib,math
P=Path(__file__).parent;O=P.parent/'02_项目成片/efficiency-after';O.mkdir(exist_ok=True)
R=P/'render';R.mkdir(exist_ok=True)
D=float((P/'data/duration.txt').read_text());TOTAL=math.ceil(D*30)
def run(args,**kw):return subprocess.run(['ffmpeg','-hide_banner','-nostdin','-y',*map(str,args)],capture_output=True,check=True,**kw)
def measurement(path):
 r=run(['-i',path,'-af','loudnorm=I=-16:TP=-1.5:LRA=11:print_format=json','-f','null','NUL'])
 log=r.stderr.decode('utf-8',errors='replace');return json.loads(log[log.rfind('{'):log.rfind('}')+1]),log
def audio():
 music=P.parent/'03_有价值素材/音乐与音效/life-omitted/Reverie.mp3'
 graph=f'[0:a]loudnorm=I=-17:TP=-2:LRA=11,aresample=48000,apad,atrim=duration={D}[n];[1:a]loudnorm=I=-32:TP=-8:LRA=8,aresample=48000,afade=t=in:d=2,afade=t=out:st={D-4}:d=4,atrim=duration={D}[b];[n][b]amix=inputs=2:normalize=0,alimiter=limit=0.89:level=0:latency=1[a]'
 run(['-i',P/'audio/narration.mp3','-stream_loop','-1','-i',music,'-filter_complex',graph,'-map','[a]','-t',D,'-ar','48000','-ac','2','-c:a','pcm_s16le',R/'premix.wav'])
 m,log=measurement(R/'premix.wav');(R/'loudness-first.txt').write_text(log,encoding='utf-8')
 f=f"loudnorm=I=-16:TP=-1.7:LRA=11:measured_I={m['input_i']}:measured_TP={m['input_tp']}:measured_LRA={m['input_lra']}:measured_thresh={m['input_thresh']}:offset={m['target_offset']}:linear=true"
 run(['-i',R/'premix.wav','-af',f+f',aresample=48000,apad,atrim=duration={D}','-t',D,'-ar','48000','-ac','2','-c:a','aac','-b:a','192k',R/'mix.m4a'])
 shutil.copy2(P.parent/'02_项目成片/life-omitted-v4/音乐署名.txt',O/'音乐署名.txt')
def mux(mode):
 src=R/('silent.mp4' if mode=='full' else 'preview-silent.mp4')
 dst=O/('效率提高之后_完整版.mp4' if mode=='full' else '全长有声预览_540p.mp4')
 run(['-i',src,'-i',R/'mix.m4a','-map','0:v:0','-map','1:a:0','-c','copy','-t',TOTAL/30,'-movflags','+faststart',dst])
 return dst
def verify(dst):
 probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-count_frames','-show_streams','-show_format','-of','json',str(dst)]))
 (R/'final-probe.json').write_text(json.dumps(probe,ensure_ascii=False,indent=2),encoding='utf-8')
 video=next(s for s in probe['streams'] if s['codec_type']=='video');a=next(s for s in probe['streams'] if s['codec_type']=='audio')
 assert int(video['nb_read_frames'])==TOTAL
 assert video['width']==1920 and video['height']==1080
 assert abs(float(video['duration'])-TOTAL/30)<.001
 assert abs(float(a['duration'])-D)<.06
 res=run(['-v','error','-i',dst,'-f','null','NUL']);(R/'decode.log').write_bytes(res.stderr)
 m,log=measurement(dst);(R/'loudness-final.txt').write_text(log,encoding='utf-8')
 assert -17<=float(m['input_i'])<=-15
 assert float(m['input_tp'])<=-1.0
 silence=run(['-i',dst,'-af','silencedetect=n=-45dB:d=2','-f','null','NUL']).stderr.decode('utf-8',errors='replace')
 (R/'silence.txt').write_text(silence,encoding='utf-8')
 scenes=json.loads((P/'data/scenes.json').read_text(encoding='utf-8'))
 from PIL import Image,ImageDraw
 ims=[]
 for i,s in enumerate(scenes):
  for k,t in enumerate([s['start']+min(.9,(s['end']-s['start'])/3),s['end']-.35]):
   path=R/f'final-{i:02d}-{k}.jpg'
   run(['-v','error','-ss',t,'-i',dst,'-frames:v','1','-q:v','2',path])
   im=Image.open(path).resize((480,270));d=ImageDraw.Draw(im);d.rectangle((0,0,110,25),fill='#24343f');d.text((5,5),f'{i+1} / {t:.1f}s',fill='white');ims.append(im)
 contact=Image.new('RGB',(1920,math.ceil(len(ims)/4)*270),'#e9e1cf')
 for j,im in enumerate(ims):contact.paste(im,((j%4)*480,(j//4)*270))
 contact.save(R/'final-contact.jpg',quality=90)
 (R/'check.json').write_text(json.dumps({'frames':TOTAL,'duration':float(probe['format']['duration']),'loudness':m,'decodeErrors':len(res.stderr),'longSilences':silence.count('silence_start'),'sourceCopySha256':hashlib.sha256((P/'audio/narration.mp3').read_bytes()).hexdigest(),'finalSha256':hashlib.sha256(dst.read_bytes()).hexdigest()},ensure_ascii=False,indent=2),encoding='utf-8')
 print(json.dumps({'frames':TOTAL,'LUFS':m['input_i'],'dBTP':m['input_tp'],'path':str(dst)},ensure_ascii=False),flush=True)
if __name__=='__main__':
 mode=sys.argv[1]
 if mode=='audio':audio()
 elif mode in ['preview','full']:
  dst=mux(mode)
  if mode=='full':verify(dst)
 elif mode=='verify':verify(O/'效率提高之后_完整版.mp4')
