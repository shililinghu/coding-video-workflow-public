from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import json, math, random, subprocess, sys, bisect, hashlib
P=Path(__file__).parent
ROOT=P.parent
W,H=1920,1080
FPS=30
BG='#e9e1cf'; INK='#24343f'; RED='#b9513d'; BLUE='#31596b'; GREEN='#4a7562'; PALE='#faf4e8'
fonts={}
def font(n,bold=False):
 key=(n,bold)
 if key not in fonts: fonts[key]=ImageFont.truetype('C:/Windows/Fonts/msyhbd.ttc' if bold else 'C:/Windows/Fonts/msyh.ttc',n)
 return fonts[key]
def text(d,xy,s,size=56,fill=INK,bold=False,anchor=None): d.text(xy,s,font=font(size,bold),fill=fill,anchor=anchor)
def panel(d,box,fill=PALE,outline=None,width=3):
 x,y,x2,y2=box
 d.rounded_rectangle((x+10,y+12,x2+10,y2+12),radius=16,fill='#c6bead')
 d.rounded_rectangle(box,radius=16,fill=fill,outline=outline,width=width)
def arrow(d,a,b,color=RED,width=8):
 d.line([a,b],fill=color,width=width)
 ang=math.atan2(b[1]-a[1],b[0]-a[0]);x,y=b
 d.polygon([(x,y),(x-25*math.cos(ang-.5),y-25*math.sin(ang-.5)),(x-25*math.cos(ang+.5),y-25*math.sin(ang+.5))],fill=color)
def check(d,x,y,s=55,color=GREEN):d.line([(x,y+s*.45),(x+s*.32,y+s*.8),(x+s,y)],fill=color,width=12)
def bowl(d,x,y,s=1,color=RED):
 d.ellipse((x-110*s,y-26*s,x+110*s,y+34*s),fill='#f5ead3',outline=INK,width=4)
 d.pieslice((x-105*s,y-80*s,x+105*s,y+95*s),0,180,fill=color,outline=INK,width=4)
 for dx in [-50,0,50]:d.arc((x+dx*s-18*s,y-100*s,x+dx*s+18*s,y-36*s),100,270,fill=INK,width=5)
def phone(d,x=740,y=120,w=600,h=690):
 panel(d,(x,y,x+w,y+h),INK)
 d.rounded_rectangle((x+18,y+30,x+w-18,y+h-20),radius=16,fill=PALE)
 text(d,(x+55,y+65),'午饭',54,bold=True)
 d.rounded_rectangle((x+50,y+140,x+w-50,y+205),radius=22,fill='#ddd8c9')
 text(d,(x+85,y+150),'搜索附近餐厅',36)
 return x,y,w,h
def mealcard(d,x,y,label,price='¥25',detail='4.8  ·  25分钟',selected=False,w=450,h=140):
 panel(d,(x,y,x+w,y+h), '#e4efdf' if selected else PALE,GREEN if selected else None,5)
 bowl(d,x+85,y+70,.45,GREEN if selected else RED)
 text(d,(x+158,y+17),label,38,bold=True)
 text(d,(x+158,y+63),price,42,RED,True)
 text(d,(x+260,y+77),detail,25)
def clock(d,x,y,minutes):
 d.ellipse((x-75,y-75,x+75,y+75),fill=PALE,outline=INK,width=6)
 a=minutes/60*2*math.pi-math.pi/2
 d.line([(x,y),(x+55*math.cos(a),y+55*math.sin(a))],fill=RED,width=7)
 d.line([(x,y),(x,y-40)],fill=INK,width=8)
 text(d,(x,y+100),f'{minutes}分钟',48,anchor='mm')

sheet=Image.open(ROOT/'03_有价值素材/角色/pixel-fox/sprites-v2.png')
actors=[]
for i in range(4):
 tile=sheet.crop(((i%2)*768,(i//2)*512,(i%2+1)*768,(i//2+1)*512))
 tile=tile.crop(tile.getbbox())
 actors.append(tile)
actor_cache={}
def fox(im,x,y,height=470,pose=1,flip=False):
 key=(height,pose,flip)
 if key not in actor_cache:
  a=actors[pose];a=a.resize((round(a.width*height/a.height),height),Image.Resampling.NEAREST)
  if flip:a=a.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
  actor_cache[key]=a
 a=actor_cache[key];im.paste(a,(int(x-a.width/2),int(y-height)),a)

random.seed(1020)
base=Image.new('RGB',(W,H),BG);bd=ImageDraw.Draw(base)
for i in range(14000):
 x=random.randrange(W);y=random.randrange(H);v=random.randrange(205,239)
 bd.point((x,y),fill=(v,min(240,v-4),max(0,v-18)))
bd.rectangle((64,55,1855,875),outline='#c6bea9',width=2)
bd.rectangle((90,77,190,90),fill=RED)

scenes=json.loads((P/'data/scenes.json').read_text(encoding='utf-8'))
subs=json.loads((P/'data/subtitles.json').read_text(encoding='utf-8'))
substarts=[s['start'] for s in subs]
scene_starts=[s['start'] for s in scenes]
duration=float((P/'data/duration.txt').read_text())
TOTAL=math.ceil(duration*FPS)

import scenes as scene_module
scene_module.CUES=json.loads((P/'data/cues.json').read_text(encoding='utf-8'))
def scene_image(s,t):
 im=base.copy();d=ImageDraw.Draw(im)
 return scene_module.render_scene(im,d,s,t,(text,panel,arrow,check,fox,INK,RED,BLUE,GREEN,PALE))
def frame(f):
 t=f/FPS;i=max(0,bisect.bisect_right(scene_starts,t)-1);s=scenes[i]
 im=scene_image(s,t)
 if i>0 and scenes[i-1]['kind']!=s['kind'] and t-s['start']<.3:
  k=(t-s['start'])/.3;k=k*k*(3-2*k)
  im=Image.blend(scene_image(scenes[i-1],s['start']-1/30),im,k)
 d=ImageDraw.Draw(im)
 j=bisect.bisect_right(substarts,t)-1
 if j>=0 and t<subs[j]['end']:
  line=subs[j]['text'];sz=66
  while d.textbbox((0,0),line,font=font(sz))[2]>1690:sz-=2
  d.rounded_rectangle((80,905,1840,1035),radius=16,fill=INK)
  text(d,(960,965),line,sz,PALE,anchor='mm')
 return im

def encode(path,fps=30,size=(1920,1080),start=0,end=None):
 end=TOTAL if end is None else end
 cmd=['ffmpeg','-y','-v','error','-f','rawvideo','-pix_fmt','rgb24','-s',f'{size[0]}x{size[1]}','-r',str(fps),'-i','-','-an','-c:v','libx264','-preset','veryfast','-crf','20','-pix_fmt','yuv420p',str(path)]
 proc=subprocess.Popen(cmd,stdin=subprocess.PIPE)
 for f in range(start,end,30//fps):
  im=frame(f)
  if size!=(W,H):im=im.resize(size,Image.Resampling.BILINEAR)
  proc.stdin.write(im.tobytes())
  if f%900==0:print(f'{f}/{TOTAL}',flush=True)
 proc.stdin.close()
 if proc.wait()!=0:raise RuntimeError('encoding failed')

def covers():
 scene_module.covers(ROOT,text,panel,fox,font)
if __name__=='__main__':
 (P/'render').mkdir(exist_ok=True)
 mode=sys.argv[1] if len(sys.argv)>1 else 'stills'
 if mode=='stills':
  ims=[]
  for i,s in enumerate(scenes):
   for k,t in enumerate([s['start']+min(.9,(s['end']-s['start'])/3),s['end']-.35]):
    im=frame(round(t*30));im.save(P/f'render/scene-{i:02d}-{k}.jpg',quality=88)
    th=im.resize((480,270));dd=ImageDraw.Draw(th);dd.rectangle((0,0,100,28),fill=INK);dd.text((4,2),f'{i+1} / {t:.1f}s',font=font(20),fill=PALE);ims.append(th)
  out=Image.new('RGB',(1920,math.ceil(len(ims)/4)*270),BG)
  for j,im in enumerate(ims):out.paste(im,((j%4)*480,(j//4)*270))
  out.save(P/'render/contact.jpg',quality=90)
  # Repeat frames in a different order to check stateless rendering.
  ids=[0,TOTAL//2,TOTAL-1,600,1200]
  hashes={f:hashlib.sha256(frame(f).tobytes()).hexdigest() for f in ids}
  assert all(hashlib.sha256(frame(f).tobytes()).hexdigest()==hashes[f] for f in reversed(ids))
  (P/'render/determinism.json').write_text(json.dumps(hashes,indent=2))
 elif mode=='preview':encode(P/'render/preview-silent.mp4',15,(960,540))
 elif mode=='sample':encode(P/'render/sample-silent.mp4',30,(1920,1080),0,round(min(38,duration)*30))
 elif mode=='full':encode(P/'render/silent.mp4')
 elif mode=='covers':covers()
