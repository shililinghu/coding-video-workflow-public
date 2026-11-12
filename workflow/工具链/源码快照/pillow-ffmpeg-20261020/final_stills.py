from pathlib import Path
from PIL import Image,ImageDraw
import math
P=Path(__file__).parent;R=P/'render'
ims=[]
for p in sorted(R.glob('final-??-?.jpg')):
 im=Image.open(p).resize((480,270));ims.append(im)
for j in range(math.ceil(len(ims)/24)):
 batch=ims[j*24:(j+1)*24]
 if not batch:continue
 out=Image.new('RGB',(1920,math.ceil(len(batch)/4)*270),'#e9e1cf')
 for i,im in enumerate(batch):out.paste(im,((i%4)*480,(i//4)*270))
 out.save(R/f'final-review-{j}.jpg')
files=sorted(R.glob('final-??-1.jpg'))
chosen=[files[round(i*(len(files)-1)/15)] for i in range(16)]
out=Image.new('RGB',(1560,880),'#e9e1cf')
for i,p in enumerate(chosen):
 im=Image.open(p).resize((390,219));out.paste(im,((i%4)*390,(i//4)*220))
out.save(R/'mobile-final.jpg')
