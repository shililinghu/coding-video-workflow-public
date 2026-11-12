from pathlib import Path
import json, shutil
from faster_whisper import WhisperModel
p=Path(__file__).parent
(p/'audio').mkdir(exist_ok=True)
(p/'data').mkdir(exist_ok=True)
src=Path('C:/ExampleWorkspace/example.mp3')
shutil.copy2(src,p/'audio/narration.mp3')
m=WhisperModel('small',device='cpu',compute_type='int8',local_files_only=True,cpu_threads=8)
segs,info=m.transcribe(str(src),language='zh',word_timestamps=True,vad_filter=True,beam_size=5)
rows=[]
for s in segs:
 rows.append({'start':s.start,'end':s.end,'text':s.text,'words':[{'start':w.start,'end':w.end,'word':w.word,'probability':w.probability} for w in s.words]})
 print(f'{s.start:.2f} {s.end:.2f} {s.text}',flush=True)
(p/'data/transcript-raw.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding='utf-8')


