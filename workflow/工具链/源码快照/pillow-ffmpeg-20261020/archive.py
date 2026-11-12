from pathlib import Path
import json,shutil,hashlib,math
P=Path(__file__).parent;ROOT=P.parent;R=P/'render';O=ROOT/'02_项目成片/efficiency-after';A=ROOT/'01_项目复盘/项目/efficiency-after';A.mkdir(parents=True,exist_ok=True)
C=json.loads((R/'check.json').read_text(encoding='utf-8'));V=json.loads((R/'content-audit.json').read_text(encoding='utf-8'));S=json.loads((R/'sync-check.json').read_text(encoding='utf-8'));proj=json.loads((P/'data/project.json').read_text(encoding='utf-8'))
assert C['decodeErrors']==0 and C['frames']==proj['frames'] and C['longSilences']==0
assert all(abs(s['offsetMs'])<=1 for s in S)
E=A/'验收证据';E.mkdir(exist_ok=True)
for name in ['check.json','content-audit.json','determinism.json','final-probe.json','decode.log','loudness-first.txt','loudness-final.txt','silence.txt','sync-check.json','final-contact.jpg','mobile-final.jpg']:
 shutil.copy2(R/name,E/name)
for p in [*R.glob('motion-cuts-*.jpg'),*R.glob('final-review-*.jpg'),*R.glob('thumb-*.png')]:shutil.copy2(p,E/p.name)
shutil.copy2(P/'分镜.md',A/'分镜.md')
for name in ['project.json','transcript-raw.json','transcript-corrected.json','subtitles.json','corrections.json','cues.json','口播稿.txt']:shutil.copy2(P/'data'/name,A/name)
src=ROOT/'03_有价值素材/原始口播/efficiency-after';src.mkdir(exist_ok=True)
shutil.copy2(P/'audio/narration.mp3',src/proj['source'])
assert hashlib.sha256((src/proj['source']).read_bytes()).hexdigest()==proj['sourceSha256']
lu=C['loudness']['input_i'];tp=C['loudness']['input_tp'];dur=C['duration'];frames=C['frames']
doc=f'''# 效率提高之后

2026-10-20本地制作完成，待用户反馈，未发布。采用用户提供的《效率提高之后_口播_爽朗少年_1.18x_20261020.mp3》，输入181.296秒；完整保留原句、停顿与输入速度，未再次变速、重录或删改原声。独立新工程efficiency-after，复用当前仍存在的Pillow/FFmpeg工具并重写内容，未运行归档中的失效历史命令。

交付：{dur:.3f}秒，{frames}帧，1920×1080、30fps、H.264/AAC；38个内部时间段、52条字幕、27个取自原ASR的词级动作点。无独立怪手、无成片分镜计数、无顶部进度条；完整句子仅字幕。封面1200×1600（3:4）及1600×1200（4:3）分别排版。另附540p15全长有声预览、SRT及配乐署名。

主问题：工具使单件事情更快完成后，为什么总占用不一定下降？贯穿对象为可分配的时间带和待办托盘。PPT从两小时压缩到半小时，绿色空档出现后被文档、笔记与其他任务依次填入；报告任务架从一份变三份，交付期限从一天变半天；同一沟通窗口由邮件等待转为即时消息，往返次数与占用同时增长；道路原路线保留，车道扩建后支路车流汇入，新增拥堵占用原先节省的时间。片尾回到已完成的PPT及1.5小时空档，更多产出与自主时间依原声先后呈现，两个选项保持开放。

数字均来自原声中的假设案例，不是AI效率实测、真实企业或道路调查。一天不擅自换算成固定工时，道路拥堵后不编造新的最终通勤数字；图形数量、时间片和收益条用于示意变化，不冒充测量比例。主画面保留“情境示意”短标识。未新增科学术语或普遍必然结论。

实际流程：读取当前归档入口、指南、参考catalog、风格/白狐规范、两次最新流程迭代→实际重看白狐和纸层参考→复制源音频、本地small词级转写→4处文本/标点校正留痕→策划/分镜/27词级点→76幅初期末期源码抽帧、38秒有声连续样片→检查压缩/填入/期限/消息/车流和切点→修正道路“新增拥堵”标签压数字、片尾计时标签与标题间距→重新生成相应抽帧→1080p30全片与540p15全长预览→新口播独立混音和测量→最终封装、完整解码、原声波形同步抽查→76幅最终初期/末期帧、16幅390宽图与双封面/240宽缩略实际复核。

表达与时序验证：源文件、副本及归档副本SHA-256一致；校正转写全部进入字幕，范围、顺序和连续镜头覆盖通过；66px字幕最大宽{V['maxSubtitleWidthAt66px']:.0f}px，设计宽1690px内；76个主画面采样未发现与当时字幕相同的至少八字长句。65个包含全部内部时间段起点与27动作点的帧，乱序重复绘制相同。动作和切点共54帧检查；跨案例有0.3秒平滑交叉淡化，同场景内部保持对象与结果，不将这称为全片无切点。

声音与封装验证：最终{lu} LUFS、{tp} dBTP；完整解码0错误；低于−45dB且超过2秒的长静音0段。视频设计差{dur-proj['duration']:.6f}秒。原始MP3与最终AAC在5/45/85/125/175秒做3秒波形相关性检查，五处偏移均在1ms内；证明这些采样位置保持同步，不能代替全文人工听审。新混音使用已有Reverie / Scott Buckley（CC BY 4.0）低音量音乐床、淡入淡出与实测后的双遍响度处理，署名随交付。没有直接沿用上一条成片音轨。

参考与资产：ref-3b1370f955be借鉴米白纸层、阴影与限色；ref-beeabc60c2a1为用户指定白狐，保留白毛蓝眼深蓝连帽衫；ref-23566852e0c3借鉴贯穿对象、状态延续、可见因果与自然转场。参考人物、文案和原图均未直接入片。桌面、电脑、待办、报告、沟通窗口、房屋、道路、车流和时间带均为程序原创示意。白狐复用已有抱书/思考姿态与短距离平移，无新增骨骼、眨眼、耳尾或专用操作动作。两张封面均代码绘制，无新增AI生成图或生成提示词。

已修正：道路段“新增拥堵”短标签从通勤数字区移到收益条上方；拥堵后标签改为“原先节省20分钟”，避免把初始节省值误当当前保留值；片尾计时与长标题拉开间距，两个选择按“任务/自己”的ASR时标依次出现。修正后渲染的是当前交付版本。

限制：未连续全文人工听审、逐秒通看或真实手机/平台测试。ASR词起点不是人工强制对齐，字幕合并可能提前显示句内后半句；“这事件→这是一件”“做的更多→做得更多”为语境校正，非人工听写。八字文本比对不排除同义重复，静态缩略不证明移动端动态可读性；往返与车流数量是示意。角色专用动作能力仍有限。后续优先根据用户播放反馈复核字幕句界、节奏和角色操作感；如小屏内容过密，再减次要界面信息。以上改进待验证，无用户审美认可、发布或传播效果数据。

最终文件位于02_项目成片/efficiency-after；复盘及证据见本目录；原口播归档至03_有价值素材/原始口播/efficiency-after。

制作入口：transcribe.py→prepare.py→bootstrap.py→render.py（stills/sample/preview/full/covers）→finish.py（audio/preview/full）→audit.py（默认内容检查，sync原声同步）→final_stills.py→archive.py。bootstrap重建render/finish工具；内容在scenes.py与prepare.py。新工程保留在独立目录，旧作品未修改。
'''
(A/'README.md').write_text(doc,encoding='utf-8');(P/'README.md').write_text(doc,encoding='utf-8')
(O/'README.md').write_text('# 效率提高之后\n\n2026-10-20本地完成待反馈，未发布；181.3秒/1080p30，完整保留20261020版输入口播与语速。\n\n- [完整版](效率提高之后_完整版.mp4)\n- [全长有声预览](全长有声预览_540p.mp4)\n- [字幕](字幕.srt)\n- [两种比例封面](封面/)\n- [复盘及验收](../../01_项目复盘/项目/efficiency-after/README.md)\n\n配乐：Reverie / Scott Buckley，署名见音乐署名.txt。数字为原声假设案例；字幕使用自动词时间与语境校正，未全文人工听审。',encoding='utf-8')
proj['status']='本地完成待用户反馈，未发布';proj['finalFile']=str(O/'效率提高之后_完整版.mp4');proj['finalSha256']=C['finalSha256']
(P/'data/project.json').write_text(json.dumps(proj,ensure_ascii=False,indent=2),encoding='utf-8');shutil.copy2(P/'data/project.json',A/'project.json')
cat=ROOT/'03_有价值素材/视觉参考/catalog.json';data=json.loads(cat.read_text(encoding='utf-8'))
for item in data['items']:
 if item['id'] in proj['references'] and 'efficiency-after' not in item.setdefault('usedIn',[]):item['usedIn'].append('efficiency-after')
cat.write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')
entry=f'''\n\n### 2026-10-20｜效率提高之后｜独立新片交付

- 用户要求：“跟之前一样的要求”，采用本轮20261020版1.18x口播。当前工作区为F盘目录；独立efficiency-after，完整保留原句与输入语速，未重录/删句/再次变速，旧片未改。
- 实际流程：读项目梳理/指南/风格/白狐/catalog与最新两次流程迭代→实际看素材→本地词级转写与语境/标点校正→38内部时间段/52字幕/27个ASR动作点→76源码初期末期抽帧、38秒有声连续样片→54动作/切点帧复核→修正道路标签压数字、片尾标题计时距离与选择出现点→1080p30全片/540p15预览、新终混→最终机检/原声同步/76最终抽帧与16幅390宽复核→双封面及240宽缩略检查。
- 已实现：{dur:.3f}秒、{frames}帧；PPT压缩后新增任务填入同一时间带；报告架从1份变3份、交付期限一天变半天；同话题消息往返增加；原通勤路线扩建后新增车流与拥堵；结尾回到工作台，更多产出/自主时间两项开放。完整句子仅字幕，无独立怪手/分镜计数。白狐沿用抱书、思考与平移，未新增骨骼/专用操作动作。
- 验证：源副本与归档副本一致；校正稿字幕覆盖/顺序/范围、场景连续通过；65关键帧乱序确定性相等；76主画面采样无至少八字精确字幕重复，最大字幕宽1518px；完整解码0错误，{lu}LUFS/{tp}dBTP，0段低于−45dB且超过2秒长静音；原始MP3对最终AAC五处波形偏移在1ms内。证据01_项目复盘/项目/efficiency-after/验收证据。
- 封面与交付：1200×1600（3:4）、1600×1200（4:3）独立排版，以PPT缩短而任务填满时间为主意象；实际看全尺寸与240宽缩略。02_项目成片/efficiency-after含完整版、全长预览、SRT、双封面与Reverie署名。原声归档03_有价值素材/原始口播/efficiency-after。ref-3b1370f955be/ref-beeabc60c2a1/ref-23566852e0c3已登记usedIn，未复制参考人物文案，无新增AI生成图片。
- 边界与建议：数字来自原声假设案例，未视为AI或道路实测；一天不换算固定工时，未编造拥堵后的新通勤数值。未全文人工听审/逐秒通看/真实手机测试；27重点ASR词点非人工强制对齐，字幕句内可能提前显示，八字检查不能排除同义重复。后续优先按播放反馈复核句界、节奏、角色操作感及小屏密度，建议待验证。状态本地完成待反馈，未发布，无传播数据。
'''
def append_once(path,marker,content):
 if marker not in path.read_text(encoding='utf-8'):
  with path.open('a',encoding='utf-8') as f:f.write(content)
append_once(ROOT/'Coding Video 项目指南.md','### 2026-10-20｜效率提高之后｜独立新片交付',entry)
append_once(ROOT/'项目梳理.md','## 2026-10-20 新片补记','\n\n## 2026-10-20 新片补记\n\n《效率提高之后》独立efficiency-after本地完成，181.3秒；[完整版与双封面](02_项目成片/efficiency-after/README.md)、[复盘与验收](01_项目复盘/项目/efficiency-after/README.md)。采用20261020版1.18x口播并保持输入速度；待用户反馈，未发布。\n')
append_once(ROOT/'02_项目成片/README.md','efficiency-after/README.md','\n- [效率提高之后](efficiency-after/README.md)：2026-10-20，181.3秒完整片、全长预览、字幕和双封面；待反馈，未发布。\n')
print('Archived',frames,lu,tp)
