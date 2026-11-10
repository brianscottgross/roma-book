import re,os,hashlib,io,subprocess
from PIL import Image
h=open('out/book.html').read()
os.makedirs('out/small',exist_ok=True)
def rep(m):
    src=m.group(1)
    if not src.startswith(('data/','photos/')): return m.group(0)
    w=820 if '/sv/' in src else 520
    out='out/small/'+src.replace('/','_')
    if not os.path.exists(out) or os.path.getmtime(out)<os.path.getmtime(src):
        im=Image.open(src).convert('RGB'); im.thumbnail((w,w*2)); im.save(out,quality=58)
    return f'<img src="{out[4:]}"'
h=re.sub(r'<img src="([^"]+)"',rep,h)
open('out/book_small.html','w').write(h)
subprocess.run(['node','-e',open('build/pdf4.js').read()],check=True)
from pypdf import PdfReader,PdfWriter
from reportlab.pdfgen import canvas
d3=PdfReader('sources/draft3.pdf'); body=PdfReader('out/body.pdf')
w=PdfWriter()
for i in range(9): w.add_page(d3.pages[i])
for p in body.pages: w.add_page(p)
n=9+len(body.pages)
for k,i in enumerate(range(319,329)):
    pg=d3.pages[i]
    b=io.BytesIO(); c=canvas.Canvas(b,pagesize=(612,792))
    c.setFillColorRGB(1,1,1); c.rect(280,792-779,52,12,stroke=0,fill=1)
    c.setFillColorRGB(.2,.2,.2); c.setFont('Helvetica',8); c.drawCentredString(306,792-775,str(n+k+1))
    c.save(); b.seek(0); pg.merge_page(PdfReader(b).pages[0]); w.add_page(pg)
import sys
out=sys.argv[1] if len(sys.argv)>1 else 'out/Roma Norte Building by Building.pdf'
w.write(out); print(len(w.pages),os.path.getsize(out)//1e6,'MB')
