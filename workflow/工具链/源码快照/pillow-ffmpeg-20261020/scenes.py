from PIL import Image,ImageDraw
import math
CUES={}
def ease(t,a,d=.8):
 k=max(0,min(1,(t-a)/d));return 1-(1-k)**3
def cue(n):return CUES[n]['time']
def render_scene(im,d,s,t,h):
 text,panel,arrow,check,fox,INK,RED,BLUE,GREEN,PALE=h
 def tx(x,y,v,z=46,c=INK,b=False):text(d,(x,y),v,z,c,b)
 def center(x,y,v,z=46,c=INK):text(d,(x,y),v,z,c,True,anchor='mm')
 def heading(v):tx(115,117,v,44,BLUE,True);tx(1630,125,'情境示意',28,BLUE)
 def doc(x,y,w=100,h=126,label='',c=BLUE):
  d.rounded_rectangle((x,y,x+w,y+h),radius=8,fill=PALE,outline=c,width=4)
  d.polygon([(x+w-26,y),(x+w-26,y+26),(x+w,y+26)],fill=c)
  for j in range(3):d.line((x+15,y+44+j*20,x+w-15,y+44+j*20),fill=c,width=4)
  if label:center(x+w/2,y+h-14,label,24,c)
 def envelope(x,y,w=100,c=BLUE):
  d.rounded_rectangle((x,y,x+w,y+w*.64),radius=6,fill=PALE,outline=c,width=4)
  d.line([(x+4,y+3),(x+w/2,y+w*.36),(x+w-4,y+3)],fill=c,width=4)
 def bubble(x,y,w=120,c=BLUE):
  d.rounded_rectangle((x,y,x+w,y+70),radius=17,fill=c)
  d.polygon([(x+20,y+60),(x+15,y+85),(x+48,y+65)],fill=c)
  for i in range(3):d.ellipse((x+24+i*28,y+29,x+33+i*28,y+38),fill=PALE)
 def clock(x,y,r=65,angle=.75):
  d.ellipse((x-r,y-r,x+r,y+r),fill=PALE,outline=BLUE,width=5)
  for i in range(12):
   a=i*math.pi/6;d.line((x+math.sin(a)*(r-8),y-math.cos(a)*(r-8),x+math.sin(a)*(r-16),y-math.cos(a)*(r-16)),fill=BLUE,width=3)
  d.line((x,y,x+math.sin(angle)*r*.6,y-math.cos(angle)*r*.6),fill=RED,width=5)
  d.line((x,y,x-r*.35,y-r*.15),fill=INK,width=6)
 def room():
  # Window, plant, lamp and desktop anchor the same space across task changes.
  d.rounded_rectangle((120,230,410,510),radius=8,fill='#d4e2df',outline='#b5beb3',width=4)
  d.rectangle((145,375,205,495),fill='#b7c8c5');d.rectangle((220,325,290,495),fill='#acbfbc');d.rectangle((305,395,385,495),fill='#b7c8c5')
  d.line((265,230,265,510),fill=PALE,width=9);d.line((120,365,410,365),fill=PALE,width=9)
  d.line((430,660,1780,660),fill='#9c8061',width=18)
  d.rectangle((490,670,515,835),fill='#ad9477');d.rectangle((1675,670,1700,835),fill='#ad9477')
  d.line([(490,640),(490,450),(545,410)],fill=BLUE,width=10)
  d.polygon([(515,390),(585,420),(550,464),(493,430)],fill=BLUE)
  d.line((390,605,390,550),fill=GREEN,width=5)
  d.ellipse((358,537,390,576),fill=GREEN);d.ellipse((390,516,420,557),fill=GREEN)
  d.polygon([(350,600),(430,600),(417,652),(363,652)],fill=RED)
 def monitor(mode='ppt',done=False):
  panel(d,(605,220,1350,595),INK)
  d.rounded_rectangle((625,240,1330,575),radius=10,fill=PALE)
  d.rectangle((625,240,1330,292),fill='#d8dfd9')
  for i,c in enumerate([RED,'#d9aa5e',GREEN]):d.ellipse((644+i*26,258,656+i*26,270),fill=c)
  tx(750,249,'演示文稿' if mode=='ppt' else '工作报告',30,BLUE,True)
  d.rectangle((910,595,1035,632),fill=BLUE)
  d.polygon([(860,632),(1085,632),(1115,650),(830,650)],fill=BLUE)
  if mode=='ppt':
   d.rectangle((645,310,780,555),fill='#e8e1d2')
   for i in range(3):
    d.rectangle((662,326+i*72,757,381+i*72),fill=PALE,outline=BLUE,width=2)
    d.rectangle((673,337+i*72,737,343+i*72),fill=BLUE)
   d.rectangle((810,325,1295,548),fill='#ecddbd',outline='#d2c5a9',width=2)
   tx(840,347,'PPT',62,BLUE,True)
   for j,v in enumerate([.45,.72,1]):d.rectangle((1040+j*62,488-v*110,1080+j*62,488),fill=[BLUE,GREEN,RED][j])
   d.line((842,444,982,444),fill=BLUE,width=8);d.line((842,472,960,472),fill=BLUE,width=7)
  else:
   doc(675,320,140,180,c=BLUE)
   tx(865,332,'报告',52,BLUE,True)
   for j in range(4):d.line((865,420+j*30,1250-j%2*90,420+j*30),fill='#b9c6c0',width=9)
  if done:
   d.ellipse((1220,310,1295,385),fill=GREEN);check(d,1238,330,40,color=PALE)
 def tray(labels):
  panel(d,(1430,235,1770,620),'#ded8c8');tx(1465,255,'待办',38,BLUE,True)
  for i,(lab,c) in enumerate(labels):
   panel(d,(1460,327+i*86,1740,395+i*86));tx(1490,340+i*86,lab,36,c,True)
 def fox_at(x=300,pose=1,ht=380):fox(im,x,840,ht,pose)
 def timeband(k,showrest=True,fill=0,small=False):
  x,y,w=550,725,1210
  tx(x,675,'同样的 2 小时',36,BLUE,True)
  d.rounded_rectangle((x,y,x+w,y+100),radius=12,fill='#d5d0c1')
  pptw=w*(1-.75*k)
  d.rounded_rectangle((x,y,x+pptw,y+100),radius=12,fill=BLUE)
  if k>.1 and showrest:
   d.rounded_rectangle((x+pptw+5,y,x+w,y+100),radius=12,fill='#d8e6d4')
  center(x+pptw/2,y+50,'PPT',39,PALE)
  for i,(lab,c) in enumerate([('文档',RED),('笔记',BLUE),('其他',RED)]):
   a=[cue('document'),cue('notes'),cue('other')][i]
   if fill and t>=a:
    q=ease(t,a,.7);xx=x+w/4*(i+1)
    yy=y-185*(1-q)
    d.rounded_rectangle((xx+5,yy,xx+w/4-4,yy+100),radius=10,fill=c)
    center(xx+w/8,yy+50,lab,36,PALE)
  if k>.96 and showrest and not fill and (t>=cue('rest') or kind=='end'):center(x+w*.625,y+50,'1.5 小时',44,GREEN)
 kind=s['kind']
 if kind in ['desk','question']:
  heading('工作台 / 省下来的时间')
  room();k=ease(t,cue('compress'),1.1)
  monitor(done=t>=cue('compress'))
  pose=0 if t<cue('ai') else 1
  fx=300+45*ease(t,cue('ai'),.8)
  fox_at(fx,pose)
  if t<cue('ai'):
   tray([('查资料',BLUE),('整理文字',BLUE),('调整排版',BLUE)])
   if t>=cue('research'):check(d,1690,342,30)
   if t>=cue('layout'):check(d,1690,510,30)
  else:
   tray([('文档',RED),('笔记',BLUE),('其他任务',RED)])
   panel(d,(1025,135,1320,208),GREEN);center(1172,171,'AI',42,PALE)
  timeband(k,True,fill=t>=cue('document') and kind=='desk')
  if t>=cue('compress'):
   tx(610,164,'2 小时 → 0.5 小时',44,GREEN,True)
  if t>=cue('four') and kind=='desk':tx(1460,163,'1 件 → 4 件',42,RED,True)
  if kind=='question':
   # New scenario keeps the original task and potential free time visible.
   panel(d,(1425,235,1770,620));tx(1470,270,'外部安排',43,RED,True)
   envelope(1510,380,155,RED);center(1600,545,'？',62,RED)
 elif kind=='office':
  heading('公司 / 效率与交付要求')
  room();monitor('report',t>=cue('reportfast'));fox_at(325,1)
  panel(d,(1430,235,1770,620));tx(1470,260,'任务架',40,BLUE,True)
  doc(1480,345,100,145,c=BLUE)
  k=ease(t,cue('three'),.9)
  if k>0:
   for i in range(2):doc(1500+(i+1)*55*k,345-35*k,100,145,c=RED)
  tx(1465,530,'3 份报告' if k>.9 else '1 份报告',45,RED if k>.9 else BLUE,True)
  tx(615,150,'一整天 → 2 小时' if t>=cue('reportfast') else '耗时：一整天',46,GREEN if t>=cue('reportfast') else BLUE,True)
  tx(555,680,'交付期限',37,BLUE,True)
  x,y,w=555,735,1205
  d.rounded_rectangle((x,y,x+w,y+84),radius=12,fill='#d3d0c4')
  shrink=ease(t,cue('deadline'),.9)
  width=w*(1-.5*shrink)
  d.rounded_rectangle((x,y,x+width,y+84),radius=12,fill=RED if shrink>0 else BLUE)
  center(x+width/2,y+42,'半天' if shrink>.8 else '一天',44,PALE)
  if t>=cue('assign'):
   panel(d,(1070,125,1350,200),RED);center(1210,162,'新安排',42,PALE)
  if shrink>.95:tx(1210,750,'一天 → 半天',46,RED,True)
 elif kind=='messages':
  heading('沟通 / 同一个话题的往返')
  fox_at(285,1,420)
  panel(d,(555,230,1415,660),INK)
  d.rectangle((575,250,1395,640),fill=PALE)
  d.rectangle((575,250,1395,325),fill='#d7ded7');tx(615,263,'项目沟通',42,BLUE,True)
  instant=t>=cue('instant')
  if not instant:
   envelope(690,390,180,BLUE);arrow(d,(920,450),(1100,450),BLUE,7);clock(1225,450,65)
   tx(720,565,'邮件',40,BLUE,True);tx(1125,565,'等待回复',40,BLUE,True)
   if t>=cue('email'):d.line((690,550,875,550),fill=RED,width=5)
  else:
   bubble(640,370,190,BLUE);bubble(1130,470,190,GREEN)
   if t>=cue('progress'):tx(890,355,'确认进度',36,BLUE,True)
   if t>=cue('details'):tx(890,425,'讨论细节',36,BLUE,True)
   if t>=cue('requests'):tx(890,495,'新增要求',36,RED,True)
   q=ease(t,cue('instant'),.6);xx=850+260*q
   d.ellipse((xx,425,xx+20,445),fill=RED)
   tx(780,575,'几秒送达',40,GREEN,True)
  panel(d,(1460,230,1770,660),'#e3dccd');tx(1490,260,'往返',40,BLUE,True)
  n=3 if t<cue('progress') else min(24,3+int(max(0,t-cue('progress'))*2.7))
  for i in range(n):
   x=1490+(i%3)*82;y=345+(i//3)*32
   d.rounded_rectangle((x,y,x+61,y+21),radius=7,fill=BLUE if i<3 else RED)
  tx(1490,600,'数十次' if t>=cue('dozens') else '几次',43,RED if t>=cue('dozens') else BLUE,True)
  tx(555,680,'沟通占用',37,BLUE,True)
  count=3 if not instant else min(24,3+int(max(0,t-cue('progress'))*2.7))
  for i in range(24):
   x=555+i*50
   d.rounded_rectangle((x,740,x+43,815),radius=6,fill=(BLUE if i<3 else RED) if i<count else '#d5d0c1')
 elif kind=='road':
  heading('道路 / 同一条通勤路线')
  # House and office remain fixed while lanes expand and cars enter.
  d.polygon([(160,380),(290,260),(420,380)],fill=RED)
  d.rectangle((190,380,390,545),fill=PALE,outline=INK,width=4)
  d.rectangle((260,445,315,545),fill=BLUE);tx(230,570,'家',44,BLUE,True)
  for i,(x,hh) in enumerate([(1520,230),(1630,320),(1750,190)]):
   d.rectangle((x,535-hh,x+85,535),fill=BLUE if i==1 else '#91a7a4')
   for j in range(2):
    for k in range(int(hh/55)-1):d.rectangle((x+16+j*35,555-hh+k*48,x+32+j*35,574-hh+k*48),fill=PALE)
  tx(1580,570,'公司',44,BLUE,True)
  p=ease(t,cue('widen'),1.2);top=360-75*p;bottom=530+75*p
  d.rounded_rectangle((450,top,1460,bottom),radius=25,fill='#707a76')
  for edge in [top+12,bottom-12]:d.line((475,edge,1435,edge),fill=PALE,width=4)
  lanes=4 if p>.6 else 2
  for j in range(1,lanes):
   yy=top+(bottom-top)*j/lanes
   for xx in range(480,1430,95):d.line((xx,yy,xx+52,yy),fill='#e8dfbd',width=3)
  density=ease(t,cue('drivers'),6.4)
  n=5+int(density*19)
  # Accumulated path distance slows continuously as traffic thickens.
  elapsed=max(0,t-116.6);speedphase=elapsed*55-40*max(0,t-cue('drivers'))*density
  for i in range(n):
   lane=i%lanes;col=i//lanes
   x=490+(col*151+speedphase)%880
   y=top+(bottom-top)*(lane+.5)/lanes
   c=RED if i>=5 and t>=cue('cars') else '#e9cb8e'
   d.rounded_rectangle((x,y-17,x+62,y+17),radius=8,fill=c,outline=INK,width=2)
   d.rectangle((x+17,y-12,x+40,y+12),fill=PALE)
  # A feeder route visibly adds users instead of spontaneous congestion.
  if t>=127.72:
   d.line([(780,650),(915,bottom)],fill='#8f9690',width=40)
   arrow(d,(786,645),(894,bottom+8),RED,6)
  fox_at(270,1,250)
  panel(d,(600,690,1745,825));tx(640,705,'60 分钟',55,BLUE,True)
  if t>=cue('forty'):
   tx(1000,705,'→ 40 分钟',55,GREEN,True)
  if t>=cue('saved'):
   tx(640,772,'原先节省 20 分钟' if t>=cue('congestion') else '节省 20 分钟',36,GREEN,True)
   x,y,w=1060,780,600
   d.rounded_rectangle((x,y,x+w,y+26),radius=8,fill=GREEN)
   k=ease(t,cue('congestion'),1.5)
   if k>0:d.rounded_rectangle((x+w*(1-k*.68),y,x+w,y+26),radius=8,fill=RED)
   if k>.8:tx(1090,640,'新增拥堵',34,RED,True)
 elif kind=='mechanism':
  heading('同一种变化 / 时间收益的去向')
  fox_at(310,1,430)
  for i,(lab,c) in enumerate([('单次成本',BLUE),('发生次数',RED),('总占用',RED)]):
   x=560+i*410;panel(d,(x,270,x+340,590));center(x+170,345,lab,45,c)
   center(x+170,465,'↓' if i==0 else '↑',105,c)
   if i<2:arrow(d,(x+350,430),(x+392,430),GREEN,7)
  tx(565,650,'省下的时间',43,GREEN,True)
  d.rounded_rectangle((565,725,1750,815),radius=12,fill=GREEN)
  q=ease(t,145.56,2)
  if q>0:
   d.rounded_rectangle((1750-790*q,725,1750,815),radius=12,fill=RED)
   if q>.7:center(1340,770,'新增行为',46,PALE)
 elif kind=='recap':
  heading('从工具速度 / 到任务总量')
  fox_at(300,1,410)
  labels=['PPT','报告','消息','道路']
  for i,lab in enumerate(labels):
   x=550+i*310;panel(d,(x,270,x+260,665));center(x+130,325,lab,42,BLUE)
   if i<2:
    doc(x+40,385,90,120,c=BLUE);doc(x+100,415,90,120,c=RED)
   elif i==2:
    bubble(x+35,395,110,BLUE);bubble(x+90,505,110,RED)
   else:
    d.rectangle((x+40,385,x+220,570),fill='#747e77')
    for j in range(4):d.rounded_rectangle((x+65+(j%2)*90,405+(j//2)*85,x+105+(j%2)*90,459+(j//2)*85),radius=5,fill=RED if j>1 else PALE)
  if t>=156:
   tx(580,735,'单次更快',52,GREEN,True);arrow(d,(940,775),(1110,775),BLUE,7);tx(1200,735,'总量可能增加',52,RED,True)
 elif kind=='end':
  heading('回到工作台 / 时间如何分配')
  room();monitor(done=True);fox_at(335,1,400)
  tx(680,168,'2 小时 → 0.5 小时',40,GREEN,True)
  if t<166.64:
   tray([('文档',RED),('笔记',BLUE),('其他任务',RED)])
   timeband(1,True,0)
  else:
   panel(d,(1430,235,1770,620));tx(1470,270,'剩余时间',39,BLUE,True);center(1600,405,'1.5 h',67,GREEN);center(1600,535,'？',75,GREEN)
   tx(555,680,'省下的 1.5 小时',38,GREEN,True)
   for i,(lab,c) in enumerate([('更多产出',BLUE),('自主时间',GREEN)]):
    x=600+i*600;panel(d,(x,735,x+480,835),'#d8e6d4' if i else '#dde3e1')
    if t>=cue('own' if i else 'more'):center(x+240,785,lab,45,c)
    else:center(x+240,785,'？',45,c)
   # Both options stay open; the film does not choose on the viewer's behalf.
   arrow(d,(1100,690),(850,723),BLUE,5);arrow(d,(1100,690),(1410,723),GREEN,5)
 return im

def covers(ROOT,text,panel,fox,font):
 O=ROOT/'02_项目成片/efficiency-after/封面';O.mkdir(exist_ok=True)
 for vert,size in [(True,(1200,1600)),(False,(1600,1200))]:
  w,h=size;im=Image.new('RGB',size,'#e9e1cf');d=ImageDraw.Draw(im)
  d.rectangle((42,42,w-42,h-42),outline='#c6bea9',width=3)
  text(d,(80,100),'效率提高了',104,'#24343f',True)
  text(d,(80,245),'怎么还更忙？',108,'#b9513d',True)
  if vert:
   x,y,bw=110,660,980
   fox(im,340,1420,395,1)
   text(d,(660,1120),'空档呢？',66,'#b9513d',True)
  else:
   x,y,bw=530,600,960
   fox(im,300,1060,450,1)
  text(d,(x,y-135),'2 小时 → 0.5 小时',62,'#31596b',True)
  panel(d,(x,y-35,x+bw,y+270),'#faf4e8')
  # One smaller completed job, then three extra tasks occupy the saved area.
  labels=['PPT','文档','笔记','其他']
  for i,lab in enumerate(labels):
   xx=x+20+i*(bw-40)/4;ww=(bw-40)/4-10
   c='#31596b' if i==0 else '#b9513d'
   d.rounded_rectangle((xx,y+45,xx+ww,y+205),radius=10,fill=c)
   text(d,(xx+ww/2,y+125),lab,49,'#faf4e8',True,anchor='mm')
  if not vert:text(d,(740,1010),'省下的时间，又被填满',55,'#b9513d',True)
  text(d,(80,h-115),'效率提高之后',44,'#31596b',True)
  im.save(O/('效率提高之后_封面_3比4.png' if vert else '效率提高之后_封面_4比3.png'))
 (O/'制作记录.md').write_text('# 封面制作记录\n1200×1600（3:4）及1600×1200（4:3）分别排版。主意象为PPT占用压缩后，文档、笔记及其他任务填满时间带；复用指定白狐观察空档去向。图形与版式为程序原创，无新增AI生成图片，无生成提示词。数字来自口播假设案例；平台裁切与传播效果未验证。',encoding='utf-8')
