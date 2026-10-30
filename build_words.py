from pathlib import Path
import json,re,collections
source=Path('/opt/pyvenv/lib/python3.13/site-packages/textblob/en/en-spelling.txt')
lexsource=Path('/opt/pyvenv/lib/python3.13/site-packages/textblob/en/en-lexicon.txt')
freq={}
for line in source.read_text().splitlines():
 s=line.split()
 if len(s)==2 and s[0].isalpha() and s[0].islower() and s[0].isascii():
  try:freq[s[0]]=int(s[1])
  except ValueError:pass
lex={}
for line in lexsource.read_text().splitlines():
 s=line.split()
 if len(s)>=2 and s[0].isalpha() and s[0].islower():lex[s[0]]=s[1]
# Restrict daily ANSWERS to relatively common, dictionary-listed words, never proper nouns.
# A small school-safety exclusion list removes unsuitable themes and some historical place/names.
block=set('fuck shit damn hell crap cunt dick cock tits boobs slut bitch whore arse asses rape raped rapes rapist naked nude sex sexy sexual penis vagina genital orgasm condom murder murders killed killing killer suicide suicidal drugs heroin cocaine meth racist racism nazi nazism hitler syphilis gangrene hemorrhage pneumonia plague corpse corpses torture hostage hostages hostage gunshot shotgun firearm warfare russian french american napoleon princess colonel carcass cancer cancers tumor tumors lymphoid osteoma puritan november december illinois arkansas nicholas maryland thursday thomas william mary jane auntie jesus satan devil papal pope godly holmes pierre rostov sonya anatole natasha kutuzov denisov moscow vyazma balaga murat daniel hannah aaron simon iowa utah syphilis aneurysm'.split())
block.update('thou thee hath doth unto whence midst shalt ye yeas saith bonaparte footman footmen serf serfs'.split())
# Remove over-specialized scientific terms that show up frequently in the books used to build this corpus.
block.update('dorsum plexus venous sciatic trophic varicose iodoform abscess arterial neuralgia vascular'.split())
# Avoid potentially distracting / sensitive daily classroom answer words.
block.update('breast breasts virgin drunk drunken poison hatred weapon pistol abuse abuses slaves slavery insult terror death dying hate stupid blood disease diseases lesions violent violence'.split())
# Exclude variants of strongly inappropriate words from answers and accepted guesses.
profanity_roots=('fuck','shit','bitch','cunt','nigg','fagg','pussy','whore','rape','slut','dick','cock')
def school_safe(word):
 return word not in block and not any(root in word for root in profanity_roots)
# Add everyday school vocabulary that is less frequent in 19th-century books, when vetted.
extra = '''
cat dog fox pig cow hen ant bat bee owl pup cub duck frog lion bear goat horse sheep mouse fish bird pony yak
sun sky rain wind snow cold warm cool hot star moon cloud light dark blue pink gold teal gray grey red
book read write poem quiz word math art music sing song play game team jump run hop skip spin swim dive
food cake milk rice soup corn eggs egg pear plum lime apple grape peach berry toast pasta pizza bread beans
chef cook bake boil chop stir pour heat roast slice plate bowl spoon fork knife cup mug jar tray pan pot
bike bus boat train car taxi cart truck road path lane park yard farm barn home room door gate roof wall
sand beach ocean river lake pond hill peak rock stone grass tree leaf leaves flower bloom seed soil dirt
kind nice glad calm brave proud fair share help care give gift smile laugh happy cheer peace
frog kite sock shoe coat shirt hat cap scarf glove boots pants chair desk clock phone lamp
face hand head nose eyes ears arm leg foot feet hair tooth teeth
class learn school pencil paper eraser marker folder study lesson teacher student notebook homework
heart loved hugs hug love friend friends family cheer joy hope dream brave
candy ghost spooky pumpkin costume costumes spider web bats mask candy treat trick night scare
planet earth nature weather wildlife forest garden recycle conserve climate science system habitat
sunny solar summer sunrise sunset sunshine sunlight
winter frosty snowman snowball
harvest feast turkey thankful grateful gather
year fresh future restart progress grow growth
ratio radius circle circles formula geometry polygon angles
'''.lower().split()
# include only alphabetic words; for scoring choose enough known daily answers for each grade.
for w in extra:
 if re.fullmatch(r'[a-z]{4,8}',w) and school_safe(w) and w not in freq:freq[w]=28
holiday={
'halloween':{4:['bats','mask'],5:['ghost','treat'],6:['spooky','spider'],7:['pumpkin','haunted'],8:['costumes','skeleton']},
'earth':{4:['tree','soil'],5:['earth','green'],6:['planet','forest'],7:['weather','habitat'],8:['wildlife','recycled']},
'kindness':{4:['love','kind'],5:['heart','smile'],6:['caring','friend'],7:['friends','helpful'],8:['kindness','friendly']},
'newyear':{4:['year','hope'],5:['fresh','dream'],6:['future','change'],7:['restart','promise'],8:['progress','newfound']},
'summer':{4:['warm','heat'],5:['beach','sunny'],6:['summer','sunset'],7:['sunrise','sunbeam'],8:['sunlight','sunshine']},
'harvest':{4:['food','farm'],5:['feast','gravy'],6:['turkey','family'],7:['harvest','sharing'],8:['grateful','thankful']},
'school':{4:['book','read'],5:['learn','study'],6:['pencil','lesson'],7:['teacher','library'],8:['notebook','learning']},
'winter':{4:['snow','cold'],5:['frost','chill'],6:['winter','frozen'],7:['snowman','mittens'],8:['snowball','snowfall']},
'pi':{4:['math','sums'],5:['ratio','angle'],6:['radius','circle'],7:['formula','numbers'],8:['geometry','triangle']}
}
# Every holiday override is excluded from ordinary daily answers, removing calendar collisions.
reserved=set()
for group in holiday.values():
 for lst in group.values():reserved.update(lst)
# Keep at least 366 answers per grade for leap years with deterministic nonrepetition.
configs={3:(4,38),4:(4,15),5:(5,33),6:(5,16),7:(6,40),8:(6,17),9:(7,40),10:(7,19),11:(8,34),12:(8,17)}
answer={}
for grade,(length,low) in configs.items():
 words=[w for w,n in freq.items() if len(w)==length and n>=low and w in lex and lex[w] not in ('NNP','NNPS') and school_safe(w) and w not in reserved]
 # Don't allow extra frequency low words with poor meaning; tie in lex grammatical tags.
 words=sorted(words,key=lambda w:(-freq[w],w))
 print('Grade',grade,'length',length,'size',len(words),'examples',words[:18], 'tail',words[-10:])
 if len(words)<366:raise RuntimeError(f'Grade {grade} insufficient words')
 answer[grade]=words
# Valid guesses across grades include common spellings and more rare words in CMU pronouncing dictionary.
import cmudict
valid=collections.defaultdict(set)
for w in cmudict.words():
 w=w.lower()
 if w.isascii() and w.isalpha() and 4<=len(w)<=8 and school_safe(w):valid[len(w)].add(w)
for w in freq:
 if 4<=len(w)<=8 and school_safe(w):valid[len(w)].add(w)
for words in answer.values():
 for w in words: valid[len(w)].add(w)
for words in holiday.values():
 for l, ws in words.items():valid[l].update(ws)
# Separate answer and guesses to make manual updates easy.
raw={'answers':answer,'holidays':holiday,'valid':{l:sorted(ws) for l,ws in valid.items()},'version':'1.0'}
(dest:=Path('/mnt/data/valley_word_quest/word-bank.js')).write_text('/* Daily answer banks, shared by everyone selecting the same grade/date. See README for source acknowledgements. */\nwindow.VWQ_WORDS='+json.dumps(raw,separators=(',',':'),ensure_ascii=True)+';\n')
print('total answers',sum(map(len,answer.values())),'unique',len(set(sum(list(answer.values()),[]))),'valid guesses',sum(map(len,valid.values())),'file KB',round(dest.stat().st_size/1024,1))
