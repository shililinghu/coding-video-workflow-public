from pathlib import Path
P=Path(__file__).parent
s=(P.parent/'cheap-more/render.py').read_text(encoding='utf-8').replace('random.seed(1019)','random.seed(1020)')
s=s.replace("min(34,duration)","min(38,duration)")
s=s.replace("im=scene_image(s,t);d=ImageDraw.Draw(im)","""im=scene_image(s,t)
 if i>0 and scenes[i-1]['kind']!=s['kind'] and t-s['start']<.3:
  k=(t-s['start'])/.3;k=k*k*(3-2*k)
  im=Image.blend(scene_image(scenes[i-1],s['start']-1/30),im,k)
 d=ImageDraw.Draw(im)""")
(P/'render.py').write_text(s,encoding='utf-8')
s=(P.parent/'cheap-more/finish.py').read_text(encoding='utf-8').replace('02_项目成片/cheap-more','02_项目成片/efficiency-after').replace('越便宜反而花得越多_完整版.mp4','效率提高之后_完整版.mp4')
(P/'finish.py').write_text(s,encoding='utf-8')
s=(P.parent/'cheap-more/final_stills.py').read_text(encoding='utf-8').replace('for j in range(3):','for j in range(math.ceil(len(ims)/24)):')
(P/'final_stills.py').write_text(s,encoding='utf-8')
