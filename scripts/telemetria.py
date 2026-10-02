#!/usr/bin/env python3
"""Telemetria do GitHub — gera assets/telemetria.svg com dados reais.

Variáveis de ambiente (a Action passa sozinha):
  GH_USER       login do GitHub (ErickLarssen)
  ES_TOKEN      token pessoal clássico (opcional, recomendado):
                  read:user -> conta contribuições privadas
                  repo      -> lê os acessos ao perfil (tráfego) e linguagens de repositórios privados
  GITHUB_TOKEN  fallback: só dados públicos (sem acessos ao perfil)
Uso local sem rede:  python3 telemetria.py --demo
"""
import os, sys, json, random, datetime, urllib.request
from base import *

try:
    from zoneinfo import ZoneInfo
    AGORA = datetime.datetime.now(ZoneInfo("America/Sao_Paulo"))
except Exception:
    AGORA = datetime.datetime.utcnow() - datetime.timedelta(hours=3)

USER = os.environ.get("GH_USER", "ErickLarssen")
TOKEN = os.environ.get("ES_TOKEN") or os.environ.get("GITHUB_TOKEN")
AQUI_S = os.path.dirname(os.path.abspath(__file__))
ACESSOS = os.path.join(AQUI_S, "acessos.json")


# ═══════════════════════ DADOS ═══════════════════════
def _req(url, corpo=None, token=TOKEN):
    h = {"User-Agent": "es-telemetria", "Accept": "application/vnd.github+json"}
    if token:
        h["Authorization"] = f"bearer {token}"
    data = json.dumps(corpo).encode() if corpo else None
    with urllib.request.urlopen(urllib.request.Request(url, data, h), timeout=30) as r:
        return json.loads(r.read())


GQL = """query($login:String!,$de:DateTime!,$ate:DateTime!){
  user(login:$login){
    followers{totalCount}
    repositories(ownerAffiliations:OWNER,first:100,isFork:false){
      totalCount
      nodes{ languages(first:10,orderBy:{field:SIZE,direction:DESC}){ edges{ size node{ name } } } }
    }
    ano: contributionsCollection(from:$de,to:$ate){ totalCommitContributions restrictedContributionsCount }
    cal: contributionsCollection{ contributionCalendar{ totalContributions weeks{ contributionDays{ date contributionCount } } } }
  }
}"""


def dados_reais():
    inicio = datetime.datetime(AGORA.year, 1, 1).strftime("%Y-%m-%dT00:00:00Z")
    fim = AGORA.strftime("%Y-%m-%dT23:59:59Z")
    r = _req("https://api.github.com/graphql", {"query": GQL, "variables": {"login": USER, "de": inicio, "ate": fim}})
    if "errors" in r:
        raise RuntimeError(r["errors"])
    u = r["data"]["user"]
    dias = [(d["date"], d["contributionCount"]) for w in u["cal"]["contributionCalendar"]["weeks"] for d in w["contributionDays"]]
    langs = {}
    for repo in u["repositories"]["nodes"]:
        for e in repo["languages"]["edges"]:
            langs[e["node"]["name"]] = langs.get(e["node"]["name"], 0) + e["size"]
    return dict(
        dias=dias,
        total=u["cal"]["contributionCalendar"]["totalContributions"],
        commits=u["ano"]["totalCommitContributions"] + u["ano"]["restrictedContributionsCount"],
        seguidores=u["followers"]["totalCount"],
        repos=u["repositories"]["totalCount"],
        langs=langs,
        acessos=acessos_perfil(),
    )


def acessos_perfil():
    """Soma os acessos dos últimos 14 dias. A API só guarda 14 dias, então gravamos o histórico em acessos.json."""
    tok = os.environ.get("ES_TOKEN")
    if not tok:
        return None
    try:
        t = _req(f"https://api.github.com/repos/{USER}/{USER}/traffic/views", token=tok)
    except Exception as e:
        print("tráfego indisponível:", e)
        return None
    hist = json.load(open(ACESSOS)) if os.path.exists(ACESSOS) else {"dias": {}}
    for v in t.get("views", []):
        hist["dias"][v["timestamp"][:10]] = v["count"]
    json.dump(hist, open(ACESSOS, "w"), indent=2, sort_keys=True)
    corte = (AGORA.date() - datetime.timedelta(days=13)).isoformat()
    return sum(c for d, c in hist["dias"].items() if d >= corte)


def dados_demo():
    random.seed(42)
    hoje = AGORA.date()
    ini = hoje - datetime.timedelta(days=hoje.weekday() + 1 + 52 * 7)
    dias = []
    d = ini
    while d <= hoje:
        p = 0.55 if d.weekday() < 5 else 0.25
        dias.append((d.isoformat(), random.choice([1, 2, 3, 4, 6, 9, 13]) if random.random() < p else 0))
        d += datetime.timedelta(days=1)
    for k in range(9):
        dias[-1 - k] = (dias[-1 - k][0], random.randint(2, 8))
    return dict(dias=dias, total=sum(c for _, c in dias), commits=742, seguidores=48, repos=21,
                langs={"JavaScript": 61000, "HTML": 38000, "CSS": 29000, "Python": 14000, "Java": 9000, "PHP": 5000},
                acessos=None)


def sequencias(dias):
    cont = [c for _, c in dias]
    atual = 0
    i = len(cont) - 1
    if cont and cont[i] == 0:
        i -= 1   # hoje ainda sem contribuição não quebra a sequência
    while i >= 0 and cont[i] > 0:
        atual += 1; i -= 1
    recorde = corrida = 0
    for c in cont:
        corrida = corrida + 1 if c > 0 else 0
        recorde = max(recorde, corrida)
    return atual, recorde


def n(v):
    return f"{v/1000:.1f}k".replace(".0k", "k") if v >= 1000 else str(v)


# ═══════════════════════ DESENHO ═══════════════════════
def gerar(D):
    T = Texto("t")
    W, H = 1000, 432
    a = []
    atual, recorde = sequencias(D["dias"])

    # ── indicadores ──
    tiles = [
        ("CONTRIBUIÇÕES", n(D["total"]), "NOS ÚLTIMOS 12 MESES", OURO_C),
        ("SEQUÊNCIA ATUAL", str(atual), f"DIAS · RECORDE {recorde}", ACO),
        (f"COMMITS EM {AGORA.year}", n(D["commits"]), "PÚBLICOS + PRIVADOS", OURO_C),
        (("ACESSOS AO PERFIL", n(D["acessos"]), "NOS ÚLTIMOS 14 DIAS", ACO) if D.get("acessos") is not None
         else ("REPOSITÓRIOS", n(D["repos"]), f"{n(D['seguidores'])} SEGUIDORES", ACO)),
    ]
    tw, tx0, ty = 222, 32, 30
    for i, (rot, val, rodape, cor) in enumerate(tiles):
        x = tx0 + i * (tw + 16)
        a.append(f'<g class="sobe" style="animation-delay:{0.1*i:.1f}s">')
        a.append(f'<rect x="{x}" y="{ty}" width="{tw}" height="92" rx="14" fill="#141319" stroke="{cor}" stroke-opacity=".25"/>')
        a.append(f'<rect x="{x+24}" y="{ty}" width="{tw-48}" height="1" fill="url(#fioTopo)"/>')
        a.append(f'<circle cx="{x+20}" cy="{ty+22}" r="2.8" fill="{cor}"/>')
        a.append(T(rot, MONO, 9, x + 30, ty + 25.5, 2.2, fill=cor))
        a.append(em_ouro(T(val, SERIF, 32, x + 18, ty + 66, 0.5), x + 14, ty + 36, 120, 38, p="t"))
        a.append(T(rodape, MONO_R, 7.5, x + tw - 16, ty + 64, 1.2, "end", fill=SUAVE, extra=' fill-opacity=".8"'))
        a.append("</g>")

    # ── calendário ──
    CX, CY, P, Q = 80, 186, 16.6, 13
    dias = D["dias"][-371:]
    primeiro = datetime.date.fromisoformat(dias[0][0])
    col0 = (primeiro.weekday() + 1) % 7   # domingo = 0
    nz = sorted(c for _, c in dias if c > 0) or [1]
    limites = [nz[int(len(nz) * f)] for f in (.25, .5, .75)]
    niveis = ["#18171D", "#3B2D14", "#6E4C19", "#B5822F", "#E8B866"]
    a.append(T("CALENDÁRIO DE CONTRIBUIÇÕES", MONO, 9, 32, 156, 2.4, fill=SUAVE))
    a.append(T(f"SEQUÊNCIA {atual}D  ·  RECORDE {recorde}D", MONO, 9, 968, 156, 2, "end", fill=OURO_C))
    celulas, destaque, mes_ant, ult_x = [], [], None, -99
    for k, (data, c) in enumerate(dias):
        pos = k + col0
        sem, dia = pos // 7, pos % 7
        x, y = round(CX + sem * P, 1), round(CY + dia * P, 1)
        nivel = 0 if c == 0 else 1 + sum(c > l for l in limites)
        celulas.append(f'<rect x="{x}" y="{y}" width="{Q}" height="{Q}" rx="3" fill="{niveis[nivel]}"/>')
        dt = datetime.date.fromisoformat(data)
        if dia == 0 and dt.month != mes_ant and sem < 52:
            mes_ant = dt.month
            if x - ult_x < 34:
                pular_rotulo = True
            else:
                pular_rotulo = False
                ult_x = x
        else:
            pular_rotulo = True
        if not pular_rotulo:
            nome = ["jan", "fev", "mar", "abr", "mai", "jun", "jul", "ago", "set", "out", "nov", "dez"][dt.month - 1]
            a.append(T(nome, MONO_R, 8, x, CY - 6, 0.5, fill=SUAVE, extra=' fill-opacity=".7"'))
        if k >= len(dias) - atual and atual:
            destaque.append(f'<rect x="{x-1.5}" y="{y-1.5}" width="{Q+3}" height="{Q+3}" rx="4" fill="none" stroke="{LUZ}" stroke-opacity=".65"/>')
    for i, nome in [(1, "seg"), (3, "qua"), (5, "sex")]:
        a.append(T(nome, MONO_R, 8, CX - 10, CY + i * P + 9.5, 0.5, "end", fill=SUAVE, extra=' fill-opacity=".6"'))
    ultima = len(dias) - 1 + col0
    hx, hy = round(CX + (ultima // 7) * P, 1), round(CY + (ultima % 7) * P, 1)
    cal_w = (ultima // 7 + 1) * P
    a.append(f'<g class="surge" style="animation-delay:.4s"><g id="cel">{"".join(celulas)}</g></g>')
    a.append(f'<g mask="url(#mCel)"><rect class="onda" x="{CX-160}" y="{CY}" width="160" height="{7*P}" fill="url(#tOnda)"/></g>')
    a.append(f'<g class="surge" style="animation-delay:1.2s">{"".join(destaque)}</g>')
    a.append(f'<rect class="hoje" x="{hx-3}" y="{hy-3}" width="{Q+6}" height="{Q+6}" rx="5" fill="none" stroke="{LUZ}" stroke-width="1.5"/>')
    # legenda de intensidade
    lx = 968 - 5 * 14 - 34
    a.append(T("menos", MONO_R, 8, lx - 6, CY + 7 * P + 18, 0.4, "end", fill=SUAVE, extra=' fill-opacity=".7"'))
    for i, cor in enumerate(niveis):
        a.append(f'<rect x="{lx + i*14}" y="{CY + 7*P + 9}" width="11" height="11" rx="2.5" fill="{cor}"/>')
    a.append(T("mais", MONO_R, 8, lx + 5 * 14 + 4, CY + 7 * P + 18, 0.4, fill=SUAVE, extra=' fill-opacity=".7"'))

    # ── linguagens ──
    LY = 352
    tot = sum(D["langs"].values()) or 1
    top = sorted(D["langs"].items(), key=lambda kv: -kv[1])[:6]
    cores = [OURO_C, ACO, LUZ, ACO_E, OURO_E, "#CFC9BC"]
    a.append(T("MISTURA DE LINGUAGENS", MONO, 9, 32, LY - 14, 2.4, fill=SUAVE))
    bx, bw = 32, 936
    segs, x = [], bx
    soma_top = sum(v for _, v in top)
    for i, (nome, v) in enumerate(top):
        w = bw * v / soma_top
        segs.append(f'<rect x="{x:.1f}" y="{LY}" width="{max(w-3,2):.1f}" height="10" rx="5" fill="{cores[i]}"/>')
        x += w
    a.append(f'<g mask="url(#mBarra)">{"".join(segs)}</g>')
    lx = 32
    for i, (nome, v) in enumerate(top):
        pct = f"{100*v/tot:.0f}%"
        a.append(f'<circle cx="{lx+4}" cy="{LY+30}" r="4" fill="{cores[i]}"/>')
        a.append(T(nome, SANS_M, 12, lx + 14, LY + 34, 0.2, fill=MARFIM, extra=' fill-opacity=".85"'))
        w = T.medir(nome, SANS_M, 12, 0.2)
        a.append(T(pct, MONO_R, 9.5, lx + 20 + w, LY + 34, 0.4, fill=SUAVE))
        lx += 20 + w + T.medir(pct, MONO_R, 9.5, 0.4) + 28

    # ── rodapé ──
    a.append(f'<circle class="pisca" cx="35" cy="{H-21}" r="2.4" fill="{OURO_C}"/>')
    a.append(T(f"ATUALIZADO EM {AGORA.strftime('%d.%m.%Y')}  ·  {AGORA.strftime('%Hh%M')}", MONO_R, 8.5, 46, H - 18, 1.8, fill=SUAVE, extra=' fill-opacity=".75"'))
    a.append(T("VIA GITHUB API  ·  GRAPHQL", MONO_R, 8.5, 968, H - 18, 1.8, "end", fill=ACO, extra=' fill-opacity=".7"'))

    defs = defs_vidro(W, H) + f'''
    <linearGradient id="tOnda" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="{LUZ}" stop-opacity="0"/><stop offset=".5" stop-color="{LUZ}" stop-opacity=".55"/><stop offset="1" stop-color="{LUZ}" stop-opacity="0"/>
    </linearGradient>
    <mask id="mCel" maskUnits="userSpaceOnUse" x="0" y="0" width="{W}" height="{H}"><use href="#cel" fill="#fff"/></mask>
    <mask id="mBarra" maskUnits="userSpaceOnUse" x="0" y="0" width="{W}" height="{H}"><rect class="barra" x="32" y="{LY-2}" width="936" height="14" fill="#fff"/></mask>'''
    css = f"""
      .onda {{ animation: onda 9s cubic-bezier(.45,0,.55,1) 2s infinite }}
      @keyframes onda {{ 0%{{transform:translateX(0)}} 40%,100%{{transform:translateX({cal_w+320}px)}} }}
      .hoje {{ animation: pisca 2.4s ease-in-out infinite }}
      .barra {{ transform-box:fill-box; transform-origin:left; animation: barra 1.6s cubic-bezier(.2,.7,.3,1) .8s both }}
      @keyframes barra {{ from{{transform:scaleX(0)}} to{{transform:scaleX(1)}} }}"""
    corpo = f'''<g clip-path="url(#card)">
  {fundo_vidro(W, H, grade=.08, luz=(500, 230, 460, 170))}
  {"".join(a)}
  {borda_vidro(W, H)}
</g>'''
    label = (f"Atividade no GitHub: {D['total']} contribuições nos últimos 12 meses, sequência atual de {atual} dias "
             f"(recorde {recorde}), {D['commits']} commits em {AGORA.year}. Linguagens: "
             + ", ".join(f"{k} {100*v/tot:.0f}%" for k, v in top) + ".")
    return svg(W, H, label, defs + T.defs(), corpo, css)


if __name__ == "__main__":
    if "--demo" in sys.argv:
        D = dados_demo()
    else:
        try:
            D = dados_reais()
        except Exception as e:
            print("falha ao ler a API do GitHub:", e)
            sys.exit(1)   # mantém o SVG anterior em vez de publicar dados vazios
    gravar("telemetria.svg", gerar(D))
