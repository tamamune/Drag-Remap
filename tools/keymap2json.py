import re, json, sys
src=open('tools/keymap.c',encoding='utf-8').read()
kbj=json.load(open('tools/keyboard.json',encoding='utf-8'))
order=[(k['matrix'][0],k['matrix'][1]) for k in kbj['layouts']['LAYOUT']['layout']]
LAYERS=['BASE','ONOFF','OFFON','ONON','LOWER','UPPER','UTIL','MOUSE','BALL_SETTINGS','MISC']
TD=['TD_ESC_GRAVE']+['TD_%d'%i for i in range(1,10)]+['TD_0','TD_COMM_S','TD_DOT_S']
CUSTOM=("CMD_CTL UNDO REDO COPY CUT PASTE SC_UP SC_DOWN SC_RESET CAPTCHA SAVE SAVEAS NEXTTAB PREVTAB CLOSETAB RSTRTAB "
 "L_SPD_I L_SPD_D R_SPD_I R_SPD_D L_ANG_I L_ANG_D L_INV L_CHMOD R_ANG_I R_ANG_D R_INV R_CHMOD INV_SCRL MOD_SCRL AUTO_MOUSE OLED_MOD").split()
B={}
for i,c in enumerate('ABCDEFGHIJKLMNOPQRSTUVWXYZ'): B['KC_'+c]=4+i
for i,c in enumerate('1234567890'): B['KC_'+c]=0x1E+i
for i in range(12): B['KC_F%d'%(i+1)]=0x3A+i
B.update(KC_ENT=0x28,KC_ESC=0x29,KC_BSPC=0x2A,KC_TAB=0x2B,KC_SPACE=0x2C,KC_MINS=0x2D,KC_EQL=0x2E,KC_LBRC=0x2F,KC_RBRC=0x30,
 KC_BSLS=0x31,KC_NUHS=0x32,KC_SCLN=0x33,KC_QUOT=0x34,KC_GRV=0x35,KC_COMM=0x36,KC_DOT=0x37,KC_SLSH=0x38,KC_PSCR=0x46,KC_DEL=0x4C,
 KC_RIGHT=0x4F,KC_LEFT=0x50,KC_DOWN=0x51,KC_UP=0x52,KC_NUM_LOCK=0x53,KC_KP_SLASH=0x54,KC_KP_ASTERISK=0x55,KC_KP_MINUS=0x56,
 KC_KP_PLUS=0x57,KC_KP_ENTER=0x58,KC_KP_0=0x62,KC_LSFT=0xE1,KC_RSFT=0xE5,KC_LALT=0xE2,KC_LWIN=0xE3,KC_VOLU=0xA9,KC_VOLD=0xAA,
 MS_BTN1=0xD1,MS_BTN2=0xD2,MS_BTN3=0xD3,MS_WHLU=0xD9,MS_WHLD=0xDA,_______=1,XXXXXXX=0,MC_CAD=0x7E40,MC_TASK=0x7E41)
for i in range(1,10): B['KC_KP_%d'%i]=0x58+i
for i,n in enumerate(CUSTOM): B[n]=0x7E00+i
for i,n in enumerate(LAYERS): B[n]=i
for i,n in enumerate(TD): B[n]=i
def split(s):
    out=[];d=0;cur=''
    for ch in s:
        if ch=='(':d+=1
        if ch==')':d-=1
        if ch==',' and d==0: out.append(cur.strip());cur=''
        else: cur+=ch
    if cur.strip(): out.append(cur.strip())
    return out
def ev(t):
    t=t.strip()
    m=re.match(r'(\w+)\((.*)\)$',t,re.S)
    if not m:
        m2=re.match(r'QK_USER_(\d+)$',t)
        if m2: return 0x7E40+int(m2.group(1))
        return B[t]
    f,a=m.group(1),[ev(x) for x in split(m.group(2))]
    if f=='S': return 0x200|a[0]
    if f=='C': return 0x100|a[0]
    if f=='LT': return 0x4000|(a[0]<<8)|a[1]
    if f=='LSFT_T': return 0x2000|0x200|a[0]
    if f=='MO': return 0x5220|a[0]
    if f=='TG': return 0x5260|a[0]
    if f=='TO': return 0x5200|a[0]
    if f=='TD': return 0x5700|a[0]
    raise Exception(t)
# strip comments
s=re.sub(r'//.*','',src); s=re.sub(r'/\*.*?\*/','',s,flags=re.S)
i=s.index('keymaps[]'); j=s.index('encoder_map[]')
kmsec=s[i:j]; encsec=s[j:]
ROWS,COLS,NE=14,7,8
km=[[[0]*COLS for _ in range(ROWS+NE)] for l in range(10)]
for l in range(10): km[l]=[[0]*COLS for _ in range(ROWS+NE)]
seen=[]
for m in re.finditer(r'\[(\w+)\]\s*=\s*LAYOUT\(',kmsec):
    name=m.group(1); st=m.end(); d=1; k=st
    while d: 
        d+= (kmsec[k]=='(')-(kmsec[k]==')'); k+=1
    args=split(kmsec[st:k-1]); assert len(args)==len(order),(name,len(args),len(order))
    l=LAYERS.index(name); seen.append(name)
    for (r,c),a in zip(order,args): km[l][r][c]=ev(a)
for m in re.finditer(r'\[('+'|'.join(LAYERS)+r')\]\s*=\s*\{',encsec):
    name=m.group(1); st=m.end(); d=1; k=st
    while d:
        d+=(encsec[k]=='{')-(encsec[k]=='}'); k+=1
    items=re.findall(r'ENCODER_CCW_CW\(((?:[^()]|\([^()]*\))*)\)',encsec[st:k-1])
    assert len(items)==NE,(name,len(items))
    l=LAYERS.index(name)
    for e,it in enumerate(items):
        a,b=split(it); km[l][ROWS+e][0]=ev(a); km[l][ROWS+e][1]=ev(b)
print('layers',seen)
json.dump({'device':'KillerWhale DUO','rows':ROWS+NE,'cols':COLS,'layers':10,'keymap':km},open('keymap-test.json','w'))
