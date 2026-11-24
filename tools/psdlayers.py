import struct,sys,re
def parse(path):
    f=open(path,'rb');b=f.read()
    assert b[:4]==b'8BPS';ver=struct.unpack('>H',b[4:6])[0];L=8 if ver==2 else 4
    p=26;cm=struct.unpack('>I',b[p:p+4])[0];p+=4+cm
    ir=struct.unpack('>I',b[p:p+4])[0];p+=4+ir
    lm=struct.unpack('>Q' if L==8 else '>I',b[p:p+L])[0];p+=L
    li=struct.unpack('>Q' if L==8 else '>I',b[p:p+L])[0];p+=L
    n=struct.unpack('>h',b[p:p+2])[0];p+=2;n=abs(n)
    out=[]
    for i in range(n):
        t,l,bt,r=struct.unpack('>4i',b[p:p+16]);p+=16
        nc=struct.unpack('>H',b[p:p+2])[0];p+=2;p+=nc*(2+L)
        p+=4;blend=b[p:p+4];p+=4;op=b[p];p+=4
        el=struct.unpack('>I',b[p:p+4])[0];p+=4;e=p;end=p+el
        ml=struct.unpack('>I',b[e:e+4])[0];e+=4+ml
        bl=struct.unpack('>I',b[e:e+4])[0];e+=4+bl
        nl=b[e];name=b[e+1:e+1+nl].decode('latin1');e+=((1+nl+3)//4)*4
        info={}
        while e<end-12:
            sig=b[e:e+4];key=b[e+4:e+8].decode('latin1');e+=8
            big=key in('LMsk','Lr16','Lr32','Layr','Mt16','Mt32','Mtrn','Alph','FMsk','lnk2','FEid','FXid','PxSD') and L==8
            ln=struct.unpack('>Q' if big else '>I',b[e:e+(8 if big else 4)])[0];e+=(8 if big else 4)
            info[key]=b[e:e+ln];e+=ln
            if ln%2 and False:e+=1
        if 'luni' in info:
            d=info['luni'];k=struct.unpack('>I',d[:4])[0];name=d[4:4+2*k].decode('utf-16-be')
        rec={'name':name,'rect':(l,t,r,bt),'op':op,'blend':blend.decode('latin1'),'keys':list(info)}
        if 'lsct' in info:rec['group']=struct.unpack('>I',info['lsct'][:4])[0]
        if 'TySh' in info:
            d=info['TySh'];rec['xf']=struct.unpack('>6d',d[2:50])
            txt=re.search(rb'Txt TEXT(....)',d)
            if txt:
                k=struct.unpack('>I',txt.group(1))[0];s=txt.end();rec['text']=d[s:s+2*k].decode('utf-16-be',errors='replace').rstrip('\x00')
            ed=d[d.find(b'EngineData'):]
            rec['sizes']=re.findall(rb'/FontSize ([\d.]+)',ed)[:4]
            rec['fonts']=re.findall(rb'/Name \(\xfe\xff((?:[^)]|\\\))*)\)',ed)[:6]
            rec['fonts']=[x.replace(b'\\',b'').decode('utf-16-be','replace') for x in rec['fonts']]
            rec['tracking']=re.findall(rb'/Tracking ([-\d.]+)',ed)[:2]
            rec['fill']=re.findall(rb'/FillColor << /Type 1 /Values \[ ([\d. ]+)\]',ed)[:2]
        out.append(rec);p=end
    return out
if __name__=='__main__':
    for r in parse(sys.argv[1]):
        print({k:v for k,v in r.items() if k!='keys'}, ''.join('' for _ in []))
