// Render every SVG in ../svg to a PNG in ../png (transparent, width = argv[2] px)
const {chromium}=require('/opt/node22/lib/node_modules/playwright');
const fs=require('fs'),path=require('path');
const src=path.join(__dirname,'..','svg'), out=path.join(__dirname,'..','png');
const W=+(process.argv[2]||3000);
(async()=>{fs.mkdirSync(out,{recursive:true});const b=await chromium.launch();
for(const f of fs.readdirSync(src).filter(f=>f.endsWith('.svg'))){
  const svg=fs.readFileSync(path.join(src,f),'utf8');
  const [,vw,vh]=svg.match(/viewBox="0 0 ([\d.]+) ([\d.]+)"/).map(Number);
  const w=f.includes('icon')?1024:W, h=Math.round(w*vh/vw);
  const p=await b.newPage({viewport:{width:w,height:h}});
  await p.setContent(`<style>html,body{margin:0;background:transparent}svg{display:block;width:${w}px;height:${h}px}</style>${svg}`);
  await p.screenshot({path:path.join(out,f.replace('.svg','.png')),omitBackground:true});await p.close();console.log('png',f);}
await b.close();})();
