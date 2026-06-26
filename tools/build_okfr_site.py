#!/usr/bin/env python3
"""Build the static OKFR publication site."""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import sys
import tempfile
from pathlib import Path
from typing import Any

from build_okfr_seelinks_pack import PACK_PATH, build_pack, intro_markdown, readme_markdown, write_outputs
from okf_lib import ROOT, add_check_arg, repo_rel


SITE_DIR = ROOT / "_site"
PACK_SITE_DIR = Path("data/code-agent-harness-okfr")
GENERATED_AT = "2026-06-26T00:00:00Z"


def ensure_pack_current() -> None:
    pack = build_pack()
    write_outputs(pack)


def should_skip(path: Path) -> bool:
    name = path.name
    if name in {".DS_Store"} or name.startswith("~$"):
        return True
    if name in {"__pycache__", ".pytest_cache", ".mypy_cache", ".ruff_cache"}:
        return True
    if path.suffix in {".pyc", ".tmp", ".log"}:
        return True
    return False


def copy_public_tree(source: Path, dest: Path) -> None:
    for path in sorted(source.rglob("*")):
        rel = path.relative_to(source)
        if any(should_skip(part) for part in path.parents) or should_skip(path):
            continue
        target = dest / rel
        if path.is_dir():
            target.mkdir(parents=True, exist_ok=True)
        else:
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(path, target)


def copy_if_exists(source: Path, dest: Path) -> None:
    if source.is_file():
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, dest)


def remove_tree(path: Path) -> None:
    for _ in range(3):
        if not path.exists():
            return
        shutil.rmtree(path, ignore_errors=True)
        if not path.exists():
            return
        for child in sorted(path.rglob("*"), key=lambda item: len(item.parts), reverse=True):
            try:
                if child.is_file() or child.is_symlink():
                    child.unlink()
                elif child.is_dir():
                    child.rmdir()
            except OSError:
                pass
        try:
            path.rmdir()
        except OSError:
            pass
    if path.exists():
        raise OSError(f"could not remove generated site directory: {path}")


def viewer_html() -> str:
    return r'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Code Agent Harness OKFR</title>
<style>
:root{--bg:#101522;--panel:#171d2d;--panel2:#20283c;--line:#303a58;--text:#e9eefb;--muted:#9eabc8;--accent:#67a7ff;--accent2:#5ce0c7;--warn:#f5b75d}
*{box-sizing:border-box}html,body{margin:0;height:100%}body{background:var(--bg);color:var(--text);font:14px/1.45 -apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;overflow:hidden}
button,input{font:inherit}button{cursor:pointer}a{color:var(--accent);text-decoration:none}a:hover{text-decoration:underline}
.app{height:100%;display:grid;grid-template-rows:52px 1fr}
header{display:flex;align-items:center;gap:12px;padding:0 14px;border-bottom:1px solid var(--line);background:#0d1220}
.menu{width:34px;height:34px;border:1px solid var(--line);border-radius:8px;background:var(--panel2);color:var(--text);font-size:18px}.title{font-weight:700}.sub{color:var(--muted)}.legend{margin-left:auto;display:flex;gap:10px;flex-wrap:wrap}.legend span{display:flex;align-items:center;gap:5px;color:var(--muted);font-size:12px}.dot{width:10px;height:10px;border-radius:50%;display:inline-block}
.body{position:relative;min-height:0;overflow:hidden}.side{position:absolute;z-index:20;top:0;bottom:0;left:0;width:322px;max-width:86vw;background:var(--panel);border-right:1px solid var(--line);display:flex;flex-direction:column;transform:translateX(-100%);transition:.18s transform ease;box-shadow:8px 0 24px #0006}.side.open{transform:none}.search{margin:12px;padding:9px 11px;border:1px solid var(--line);border-radius:8px;background:var(--panel2);color:var(--text)}.list{overflow:auto;padding:0 10px 16px}.group{margin:12px 6px 4px;color:var(--muted);font-size:11px;text-transform:uppercase;letter-spacing:.06em}.entry{display:grid;grid-template-columns:14px 1fr;gap:8px;padding:7px 8px;border-radius:7px;color:var(--text)}.entry:hover,.entry.active{background:#26314c}.entry small{display:block;color:var(--muted);font-size:11px;margin-top:2px}
.toolbar{position:absolute;z-index:12;top:12px;left:50%;transform:translateX(-50%);display:flex;align-items:center;gap:5px;padding:5px;background:#101522d9;border:1px solid var(--line);border-radius:10px;box-shadow:0 8px 20px #0004}.toolbar button{border:0;background:transparent;color:var(--muted);padding:7px 10px;border-radius:7px}.toolbar button.on{background:var(--accent);color:#06172d;font-weight:700}.toolbar button:disabled{opacity:.4;cursor:default}.toolbar .sep{width:1px;height:22px;background:var(--line)}
.graph{position:absolute;inset:0}.graph svg{width:100%;height:100%;display:block;background-image:radial-gradient(#26314c 1px,transparent 1px);background-size:28px 28px}.edge{stroke:#7380a8;stroke-width:1.2;opacity:.28}.edge.focus{stroke:var(--accent2);opacity:.95;stroke-width:2.4}.edge.dim{opacity:.05}.node circle{stroke:#c7d6ff;stroke-width:1.6}.node text{paint-order:stroke;stroke:#101522;stroke-width:4px;stroke-linejoin:round;fill:var(--text);font-size:12px;pointer-events:none}.node.dim{opacity:.25}.node.active circle{stroke:#fff;stroke-width:3}.node.active text{font-weight:700;font-size:13px}
.hint{position:absolute;left:14px;bottom:12px;color:var(--muted);background:#101522d9;border:1px solid var(--line);border-radius:8px;padding:6px 9px;max-width:58vw}.counts{position:absolute;right:14px;bottom:12px;color:var(--muted);background:#101522d9;border:1px solid var(--line);border-radius:8px;padding:6px 9px}
.detail{position:absolute;z-index:24;top:0;bottom:0;right:0;width:430px;max-width:94vw;background:var(--panel);border-left:1px solid var(--line);transform:translateX(100%);transition:.18s transform ease;box-shadow:-8px 0 24px #0006;overflow:auto;padding:18px 20px 34px}.detail.open{transform:none}.close{position:absolute;right:12px;top:10px;width:30px;height:30px;border:1px solid var(--line);border-radius:8px;background:var(--panel2);color:var(--text)}.badge{display:inline-block;border:1px solid var(--line);border-radius:999px;background:var(--panel2);color:var(--muted);padding:3px 9px;font-size:11px;margin-bottom:8px}.detail h2{font-size:20px;line-height:1.25;margin:3px 36px 8px 0}.summary{color:#c8d3ec;margin:8px 0 12px}.section-title{color:var(--accent);font-weight:700;margin-top:18px}.chips{display:flex;flex-wrap:wrap;gap:6px}.chip{border:1px solid var(--line);border-radius:999px;background:var(--panel2);color:#cfe5ff;padding:4px 9px;font-size:12px;cursor:pointer}.chip:hover{border-color:var(--accent);background:#22375d}.kv{display:grid;grid-template-columns:120px 1fr;gap:7px 12px;margin-top:10px}.kv div:nth-child(odd){color:var(--muted)}.links{padding-left:0;list-style:none}.links li{margin:5px 0}.links .dot{margin-right:6px}.tip{position:absolute;z-index:30;max-width:320px;display:none;pointer-events:none;background:var(--panel);border:1px solid var(--line);border-radius:8px;padding:8px 10px;box-shadow:0 10px 26px #0008}.tip b{display:block}.tip small{color:var(--muted)}
@media(max-width:760px){.legend{display:none}.toolbar{top:8px;max-width:96vw;overflow:auto}.toolbar button{padding:6px 8px}.hint{display:none}.counts{left:12px;right:auto}.detail{width:100vw}}
</style>
</head>
<body>
<div class="app">
<header><button class="menu" id="menu" title="Open timeline and concept list">☰</button><div><div class="title">Code Agent Harness OKFR</div><div class="sub">OKF reader · graph, timeline, sources, Claim Cards</div></div><div class="legend" id="legend"></div></header>
<main class="body" id="body">
<aside class="side open" id="side"><input class="search" id="search" placeholder="Search pages, claims, sources..."><div class="list" id="list"></div></aside>
<div class="toolbar"><button id="back" title="Back">←</button><button id="forward" title="Forward">→</button><span class="sep"></span><button id="home">Home</button><span class="sep"></span><button data-layout="force">Force</button><button data-layout="timeline" class="on">Timeline</button><button data-layout="type">Type</button><button data-layout="narrative">Narrative</button></div>
<section class="graph"><svg id="svg" role="img" aria-label="OKFR graph"><defs><marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M 0 0 L 10 5 L 0 10 z" fill="#7380a8"></path></marker><marker id="arrowFocus" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M 0 0 L 10 5 L 0 10 z" fill="#5ce0c7"></path></marker></defs><g id="edges"></g><g id="nodes"></g></svg></section>
<div class="hint" id="hint">Select from the hamburger list or click a node. Relationship chips highlight matching edges.</div><div class="counts" id="counts"></div><div class="tip" id="tip"></div>
<aside class="detail" id="detail"><button class="close" id="close">×</button><div id="detailBody"></div></aside>
</main>
</div>
<script>
const PACK_URL='data/code-agent-harness-okfr/pack.json';
const COLORS={root:'#8a93ad',topics:'#5ce0c7',papers:'#67a7ff',claims:'#f5b75d',sources:'#8f7bff',reports:'#e57ad8',guidance:'#7bd88f',maps:'#f08d49',architecture:'#c7d6ff',progress:'#9eabc8',templates:'#72809f'};
let pack,items,nodeMap,edges,edgeByNode,selected=null,layout='timeline',history=[],hIndex=-1,relFilter=null;
const svg=document.getElementById('svg'),nodesG=document.getElementById('nodes'),edgesG=document.getElementById('edges'),detail=document.getElementById('detail'),detailBody=document.getElementById('detailBody'),tip=document.getElementById('tip');
function esc(s){return String(s??'').replace(/[&<>"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));}
function prop(item,k){return item?.properties?.[k]??''}
function arr(v){return Array.isArray(v)?v:(v?[v]:[])}
function color(section){return COLORS[section]||'#8a93ad'}
function short(s,n=42){s=String(s||'');return s.length>n?s.slice(0,n-1)+'…':s}
function dateValue(item){const d=String(prop(item,'okfr_date')||prop(item,'okf_timestamp')||'');const m=d.match(/(19|20)\d{2}(?:-\d{2})?/);return m?m[0]:''}
function section(item){return String(prop(item,'okf_section')||'root')}
function byId(id){return items.find(i=>i.id===id)}
function buildAdj(){edgeByNode=new Map();for(const e of edges){for(const id of [e.from,e.to]){if(!edgeByNode.has(id))edgeByNode.set(id,[]);edgeByNode.get(id).push(e)}}}
function outgoing(id){return edges.filter(e=>e.from===id)}function incoming(id){return edges.filter(e=>e.to===id)}
function layoutNodes(){const w=svg.clientWidth||1200,h=svg.clientHeight||800;const pad=90;const nodes=pack.graph.nodes.map(n=>({...n,item:byId(n.id)}));const groups=[...new Set(nodes.map(n=>section(n.item)))].sort();const types=[...new Set(nodes.map(n=>prop(n.item,'okf_type')||n.kind))].sort();const dated=nodes.map(n=>dateValue(n.item)).filter(Boolean).sort();const minYear=dated[0]?parseInt(dated[0].slice(0,4),10):2020,maxYear=dated.at(-1)?parseInt(dated.at(-1).slice(0,4),10):2026;
 nodes.forEach((n,i)=>{let x,y;if(layout==='timeline'){const d=dateValue(n.item),yr=d?parseInt(d.slice(0,4),10):maxYear;const month=d&&d.includes('-')?parseInt(d.slice(5,7),10)-1:5;const t=(yr+month/12-minYear)/Math.max(1,maxYear-minYear+1);x=pad+t*(w-pad*2);y=86+groups.indexOf(section(n.item))*Math.max(34,(h-180)/Math.max(1,groups.length-1));}
 else if(layout==='type'){x=pad+types.indexOf(prop(n.item,'okf_type')||n.kind)*Math.max(90,(w-pad*2)/Math.max(1,types.length-1));y=88+groups.indexOf(section(n.item))*Math.max(44,(h-190)/Math.max(1,groups.length-1));}
 else if(layout==='narrative'){const sec=groups.indexOf(section(n.item));const rank=i%80;x=pad+rank*Math.max(12,(w-pad*2)/80);y=85+sec*Math.max(44,(h-185)/Math.max(1,groups.length-1));}
 else{const a=i/nodes.length*Math.PI*2;const r=Math.min(w,h)*(.18+(i%7)*.035);x=w/2+Math.cos(a)*r;y=h/2+Math.sin(a)*r;}
 n.x=x;n.y=y;});nodeMap=new Map(nodes.map(n=>[n.id,n]));}
function relatedSet(){if(!selected)return null;const set=new Set([selected]);for(const e of edgeByNode.get(selected)||[]){set.add(e.from);set.add(e.to)}return set}
function draw(){layoutNodes();const rel=relatedSet();edgesG.innerHTML='';nodesG.innerHTML='';for(const e of edges){const a=nodeMap.get(e.from),b=nodeMap.get(e.to);if(!a||!b)continue;const focus=selected&&(e.from===selected||e.to===selected);const dim=rel&&(!rel.has(e.from)||!rel.has(e.to));const wrong=relFilter&&e.metadata?.relationship_label!==relFilter&&e.kind!==relFilter;const line=document.createElementNS('http://www.w3.org/2000/svg','line');line.setAttribute('x1',a.x);line.setAttribute('y1',a.y);line.setAttribute('x2',b.x);line.setAttribute('y2',b.y);line.setAttribute('class','edge '+(focus&&!wrong?'focus ':'')+(dim||wrong?'dim':''));line.setAttribute('marker-end',focus&&!wrong?'url(#arrowFocus)':'url(#arrow)');line.onmouseenter=ev=>showTip(ev,`${a.title} -> ${b.title}`,e.metadata?.relationship_label||e.kind);line.onmouseleave=hideTip;line.onclick=()=>select(e.to);edgesG.appendChild(line)}
 for(const n of nodeMap.values()){const relDim=rel&&!rel.has(n.id);const g=document.createElementNS('http://www.w3.org/2000/svg','g');g.setAttribute('class','node '+(n.id===selected?'active ':'')+(relDim?'dim':''));g.setAttribute('transform',`translate(${n.x},${n.y})`);const c=document.createElementNS('http://www.w3.org/2000/svg','circle');c.setAttribute('r',n.id===selected?11:7);c.setAttribute('fill',color(section(n.item)));g.appendChild(c);const sec=section(n.item);const labelOk=n.id===selected||(!selected&&['root','topics','reports','guidance','maps'].includes(sec))||(selected&&rel&&rel.has(n.id)&&!['papers','claims'].includes(sec));if(labelOk){const t=document.createElementNS('http://www.w3.org/2000/svg','text');t.setAttribute('x',14);t.setAttribute('y',4);t.textContent=short(n.title,48);g.appendChild(t)}g.onclick=()=>select(n.id);g.onmouseenter=ev=>showTip(ev,n.title,n.summary||'');g.onmouseleave=hideTip;nodesG.appendChild(g)}document.getElementById('counts').textContent=`${items.length} pages · ${edges.length} links`;}
function showTip(ev,title,summary){tip.innerHTML=`<b>${esc(title)}</b><small>${esc(summary||'')}</small>`;tip.style.display='block';const r=document.getElementById('body').getBoundingClientRect();let x=ev.clientX-r.left+14,y=ev.clientY-r.top+14;if(x+330>r.width)x-=330;if(y+100>r.height)y-=100;tip.style.left=x+'px';tip.style.top=y+'px'}function hideTip(){tip.style.display='none'}
function chip(label,count){return `<span class="chip" data-rel="${esc(label)}">${esc(label)} (${count})</span>`}
function linkList(list,reverse=false){return '<ul class="links">'+list.slice(0,80).map(e=>{const id=reverse?e.from:e.to;const item=byId(id);return item?`<li><span class="dot" style="background:${color(section(item))}"></span><a href="#" data-id="${esc(id)}">${esc(item.name)}</a><small> ${esc(e.metadata?.relationship_label||e.kind)}</small></li>`:''}).join('')+'</ul>'}
function openDetail(id){const item=byId(id);if(!item)return;const outs=outgoing(id),ins=incoming(id);const counts={};[...outs,...ins].forEach(e=>{const k=e.metadata?.relationship_label||e.kind;counts[k]=(counts[k]||0)+1});detailBody.innerHTML=`<span class="badge">${esc(prop(item,'okf_type')||'page')}</span><h2>${esc(item.name)}</h2><div class="summary">${esc(item.info_text||'')}</div><div class="section-title">Relationship chips</div><div class="chips">${Object.entries(counts).map(([k,v])=>chip(k,v)).join('')||'<span class="badge">No graph relationships</span>'}</div><div class="section-title">Key metadata</div><div class="kv"><div>Date</div><div>${esc(dateValue(item)||prop(item,'okf_timestamp'))}</div><div>Section</div><div>${esc(section(item))}</div><div>Path</div><div><a href="${esc(prop(item,'wiki_path'))}">${esc(prop(item,'wiki_path'))}</a></div><div>Evidence tier</div><div>${esc(prop(item,'evidence_tier')||'')}</div><div>Claim type</div><div>${esc(prop(item,'claim_type')||'')}</div><div>Source refs</div><div>${arr(prop(item,'source_ref')).map(esc).join('<br>')}</div></div><div class="section-title">References -> ${outs.length}</div>${linkList(outs)}<div class="section-title">Referenced by <- ${ins.length}</div>${linkList(ins,true)}`;detail.classList.add('open');detailBody.querySelectorAll('[data-id]').forEach(a=>a.onclick=ev=>{ev.preventDefault();select(a.getAttribute('data-id'))});detailBody.querySelectorAll('[data-rel]').forEach(c=>{c.onmouseenter=()=>{relFilter=c.dataset.rel;draw()};c.onmouseleave=()=>{relFilter=null;draw()}})}
function push(id){history=history.slice(0,hIndex+1);history.push(id);hIndex=history.length-1;updateNav()}function select(id,noPush=false){selected=id;if(!noPush)push(id);openDetail(id);draw();buildList(document.getElementById('search').value.toLowerCase())}
function updateNav(){document.getElementById('back').disabled=hIndex<=0;document.getElementById('forward').disabled=hIndex>=history.length-1}
function home(){selected=null;detail.classList.remove('open');push(null);draw();buildList(document.getElementById('search').value.toLowerCase())}
function buildList(q=''){const list=document.getElementById('list');list.innerHTML='';const sorted=[...items].filter(i=>(i.name+' '+i.info_text+' '+prop(i,'wiki_path')).toLowerCase().includes(q)).sort((a,b)=>(dateValue(a)||'9999').localeCompare(dateValue(b)||'9999')||section(a).localeCompare(section(b))||a.name.localeCompare(b.name));let last='';for(const item of sorted.slice(0,600)){const d=dateValue(item),grp=d?`${d} · ${section(item)}`:section(item);if(grp!==last){const h=document.createElement('div');h.className='group';h.textContent=grp;list.appendChild(h);last=grp}const a=document.createElement('a');a.href='#';a.className='entry '+(item.id===selected?'active':'');a.innerHTML=`<span class="dot" style="background:${color(section(item))};margin-top:5px"></span><span>${esc(item.name)}<small>${esc(prop(item,'okf_type'))} · ${esc(prop(item,'wiki_path'))}</small></span>`;a.onclick=ev=>{ev.preventDefault();select(item.id);if(innerWidth<820)document.getElementById('side').classList.remove('open')};list.appendChild(a)}}
function legend(){const secs=[...new Set(items.map(section))].sort();document.getElementById('legend').innerHTML=secs.slice(0,9).map(s=>`<span><i class="dot" style="background:${color(s)}"></i>${esc(s)}</span>`).join('')}
async function init(){pack=await fetch(PACK_URL).then(r=>r.json());items=pack.items;edges=pack.graph.edges;buildAdj();legend();buildList();draw();history=[null];hIndex=0;updateNav();}
document.getElementById('menu').onclick=()=>document.getElementById('side').classList.toggle('open');document.getElementById('search').oninput=e=>buildList(e.target.value.toLowerCase());document.getElementById('close').onclick=()=>{detail.classList.remove('open');selected=null;draw();buildList(document.getElementById('search').value.toLowerCase())};document.getElementById('home').onclick=home;document.getElementById('back').onclick=()=>{if(hIndex>0){hIndex--;selected=history[hIndex];selected?openDetail(selected):detail.classList.remove('open');draw();buildList(document.getElementById('search').value.toLowerCase());updateNav()}};document.getElementById('forward').onclick=()=>{if(hIndex<history.length-1){hIndex++;selected=history[hIndex];selected?openDetail(selected):detail.classList.remove('open');draw();buildList(document.getElementById('search').value.toLowerCase());updateNav()}};document.querySelectorAll('[data-layout]').forEach(b=>b.onclick=()=>{layout=b.dataset.layout;document.querySelectorAll('[data-layout]').forEach(x=>x.classList.toggle('on',x===b));draw()});addEventListener('resize',draw);init().catch(err=>{document.body.innerHTML='<pre style="padding:24px;color:#fff">Could not load OKFR pack: '+esc(err.message)+'</pre>'});
</script>
</body>
</html>
'''


def site_manifest(dest: Path) -> dict[str, Any]:
    files = []
    for path in sorted(dest.rglob("*")):
        if not path.is_file():
            continue
        if should_skip(path):
            continue
        if path.name == "site-manifest.json":
            continue
        rel = path.relative_to(dest).as_posix()
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        files.append({"path": rel, "sha256": digest, "bytes": path.stat().st_size})
    return {"generated_at": GENERATED_AT, "files": files}


def build_site(dest: Path, refresh_pack: bool = True) -> None:
    if dest.exists():
        remove_tree(dest)
    dest.mkdir(parents=True)
    if refresh_pack:
        ensure_pack_current()

    html = viewer_html()
    (dest / "index.html").write_text(html, encoding="utf-8")
    (dest / "viewer.html").write_text(html, encoding="utf-8")

    pack_dest = dest / PACK_SITE_DIR
    pack_dest.mkdir(parents=True, exist_ok=True)
    shutil.copy2(PACK_PATH, pack_dest / "pack.json")
    (pack_dest / "intro.md").write_text(intro_markdown(read_json(PACK_PATH)), encoding="utf-8")
    (pack_dest / "README.md").write_text(readme_markdown(read_json(PACK_PATH)), encoding="utf-8")

    copy_public_tree(ROOT / "wiki", dest / "wiki")
    for rel in ["README.md", "LLM-WIKI.md", "CHANGELOG.md", "PROGRESS.md", "CONTEXT.md", "LICENSE"]:
        copy_if_exists(ROOT / rel, dest / rel)
    redistributable = ROOT / "sources/raw/redistributable"
    if redistributable.is_dir():
        copy_public_tree(redistributable, dest / "sources/raw/redistributable")
    copy_if_exists(ROOT / "sources/README.md", dest / "sources/README.md")

    manifest = site_manifest(dest)
    (dest / "site-manifest.json").write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def compare_dirs(expected: Path, actual: Path) -> list[str]:
    expected_manifest = site_manifest(expected)
    actual_manifest = site_manifest(actual) if actual.exists() else {"files": []}
    expected_files = {entry["path"]: entry for entry in expected_manifest["files"]}
    actual_files = {entry["path"]: entry for entry in actual_manifest["files"]}
    errors: list[str] = []
    for path in sorted(expected_files.keys() - actual_files.keys()):
        errors.append(f"_site missing generated file: {path}")
    for path in sorted(actual_files.keys() - expected_files.keys()):
        errors.append(f"_site has extra generated file: {path}")
    for path in sorted(expected_files.keys() & actual_files.keys()):
        if expected_files[path]["sha256"] != actual_files[path]["sha256"]:
            errors.append(f"_site file out of date: {path}")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    add_check_arg(parser)
    args = parser.parse_args()
    if args.check:
        with tempfile.TemporaryDirectory(prefix="okfr-site-") as tmp:
            expected = Path(tmp) / "_site"
            build_site(expected, refresh_pack=False)
            errors = compare_dirs(expected, SITE_DIR)
        if errors:
            print("OKFR site check failed:")
            for error in errors[:80]:
                print(f"- {error}")
            if len(errors) > 80:
                print(f"- ... {len(errors) - 80} more")
            return 1
        print(f"OKFR site is up to date: {repo_rel(SITE_DIR)}")
        return 0

    build_site(SITE_DIR)
    print(f"Wrote {repo_rel(SITE_DIR)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
