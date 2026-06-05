import chess
import chess.svg
import pandas as pd
import numpy as np
from datetime import date

df = pd.read_csv("AI_SCORING.csv", sep=";", decimal=",")
companies = df["company"].tolist()
dims = ["material","mobility","king_safety","center_control","passed_pawns","piece_coordination"]

chess_weights    = {"material":0.05,"mobility":0.25,"king_safety":0.10,"center_control":0.25,"passed_pawns":0.20,"piece_coordination":0.15}
business_weights = {"material":0.25,"mobility":0.10,"king_safety":0.20,"center_control":0.20,"passed_pawns":0.05,"piece_coordination":0.20}

def get_scores(name):
    if name.lower() == "market":
        return df[dims].mean().values.astype(float)
    m = df[df["company"].str.lower() == name.lower()]
    if m.empty:
        raise ValueError(f"'{name}' not found. Options: {companies + ['market']}")
    return m[dims].values[0].astype(float)

def apply_weights(scores, weights):
    w = np.array([weights[d] for d in dims])
    return np.clip(scores * (w / w.max()), 0, 10)

def rank_w(s): return max(0, min(6, round(s * 0.6)))
def rank_b(s): return max(1, min(7, round(7 - s * 0.6)))

def safe_set(board, sq, piece):
    if board.piece_at(sq) is None:
        board.set_piece_at(sq, piece)
    else:
        r, f = chess.square_rank(sq), chess.square_file(sq)
        for dr in [-1, 1, -2, 2]:
            nr = r + dr
            if 0 <= nr <= 7:
                alt = chess.square(f, nr)
                if board.piece_at(alt) is None:
                    board.set_piece_at(alt, piece)
                    return

def fix_board(board):
    wk = board.king(chess.WHITE)
    bk = board.king(chess.BLACK)
    if wk and bk:
        wr, wf = chess.square_rank(wk), chess.square_file(wk)
        br, bf = chess.square_rank(bk), chess.square_file(bk)
        if abs(wr - br) <= 1 and abs(wf - bf) <= 1:
            board.remove_piece_at(wk)
            for sq in [chess.H1, chess.A1, chess.H2, chess.A2]:
                if board.piece_at(sq) is None:
                    board.set_piece_at(sq, chess.Piece(chess.KING, chess.WHITE))
                    wk = sq; break
    wk = board.king(chess.WHITE)
    if wk and board.is_attacked_by(chess.BLACK, wk):
        board.remove_piece_at(wk)
        for sq in [chess.square(f,r) for r in range(3) for f in range(8)]:
            if board.piece_at(sq) is None:
                board.set_piece_at(sq, chess.Piece(chess.KING, chess.WHITE))
                if not board.is_attacked_by(chess.BLACK, sq): break
                board.remove_piece_at(sq)
    bk = board.king(chess.BLACK)
    if bk and board.is_attacked_by(chess.WHITE, bk):
        board.remove_piece_at(bk)
        for sq in [chess.square(f,r) for r in range(7,4,-1) for f in range(8)]:
            if board.piece_at(sq) is None:
                board.set_piece_at(sq, chess.Piece(chess.KING, chess.BLACK))
                if not board.is_attacked_by(chess.WHITE, sq): break
                board.remove_piece_at(sq)

def build_board(sc_a, sc_b):
    board = chess.Board(fen=None)
    mat_a,mob_a,ks_a,cc_a,pp_a,pc_a = sc_a
    mat_b,mob_b,ks_b,cc_b,pp_b,pc_b = sc_b
    safe_set(board, chess.square(0, rank_w(mat_a)), chess.Piece(chess.ROOK,   chess.WHITE))
    safe_set(board, chess.square(1, rank_w(mob_a)), chess.Piece(chess.KNIGHT, chess.WHITE))
    safe_set(board, chess.square(2, rank_w(cc_a)),  chess.Piece(chess.BISHOP, chess.WHITE))
    safe_set(board, chess.square(3, rank_w(pc_a)),  chess.Piece(chess.QUEEN,  chess.WHITE))
    king_r_a = 0 if ks_a >= 7 else min(3, round((10-ks_a)*0.3))
    safe_set(board, chess.square(4, king_r_a), chess.Piece(chess.KING, chess.WHITE))
    np_a = max(1, round(pp_a/10*3))
    for f in [5,6][:np_a]:
        safe_set(board, chess.square(f, rank_w(pp_a)), chess.Piece(chess.PAWN, chess.WHITE))
    safe_set(board, chess.square(7, rank_b(mat_b)), chess.Piece(chess.ROOK,   chess.BLACK))
    safe_set(board, chess.square(6, rank_b(mob_b)), chess.Piece(chess.KNIGHT, chess.BLACK))
    safe_set(board, chess.square(5, rank_b(cc_b)),  chess.Piece(chess.BISHOP, chess.BLACK))
    safe_set(board, chess.square(4, rank_b(pc_b)),  chess.Piece(chess.QUEEN,  chess.BLACK))
    king_r_b = 7 if ks_b >= 7 else max(4, round(7-(10-ks_b)*0.3))
    safe_set(board, chess.square(3, king_r_b), chess.Piece(chess.KING, chess.BLACK))
    np_b = max(1, round(pp_b/10*3))
    for f in [2,1][:np_b]:
        safe_set(board, chess.square(f, rank_b(pp_b)), chess.Piece(chess.PAWN, chess.BLACK))
    fix_board(board)
    return board

def captured_html(board, color):
    full = {chess.QUEEN:1, chess.ROOK:2, chess.BISHOP:2, chess.KNIGHT:2, chess.PAWN:8}
    on_board = {pt:0 for pt in full}
    for sq in chess.SQUARES:
        p = board.piece_at(sq)
        if p and p.color == color and p.piece_type in on_board:
            on_board[p.piece_type] += 1
    syms_w = {chess.QUEEN:"♕",chess.ROOK:"♖",chess.BISHOP:"♗",chess.KNIGHT:"♘",chess.PAWN:"♙"}
    syms_b = {chess.QUEEN:"♛",chess.ROOK:"♜",chess.BISHOP:"♝",chess.KNIGHT:"♞",chess.PAWN:"♟"}
    syms = syms_w if color == chess.WHITE else syms_b
    col  = "#ffffff" if color == chess.WHITE else "#aaaaaa"
    out = []
    for pt in [chess.QUEEN, chess.ROOK, chess.BISHOP, chess.KNIGHT, chess.PAWN]:
        for _ in range(full[pt] - on_board[pt]):
            out.append(f'<span style="color:{col};font-size:16px;text-shadow:0 1px 3px #000">{syms[pt]}</span>')
    return "".join(out) if out else '<span style="color:#444;font-size:11px">all pieces active</span>'

def advantage_bar(ta, tb, name_a, name_b):
    total = ta + tb
    pct = round(ta/total*100) if total > 0 else 50
    diff = abs(round(ta-tb,2))
    lead = name_a if ta>tb+0.3 else (name_b if tb>ta+0.3 else None)
    label = f"{lead}  +{diff}" if lead else "Equal"
    return f"""
    <div style="margin:10px 0 4px;display:flex;justify-content:space-between;font-size:11px">
      <span style="color:#fff;font-weight:500">{name_a} {round(ta,2)}</span>
      <span style="color:#666">{label}</span>
      <span style="color:#888">{round(tb,2)} {name_b}</span>
    </div>
    <div style="height:8px;border-radius:4px;overflow:hidden;display:flex">
      <div style="width:{pct}%;background:#e0d9c8"></div>
      <div style="width:{100-pct}%;background:#3a3a3a"></div>
    </div>"""

def description(name_a, name_b, sc_a, sc_b, persp):
    ta = float(np.mean(sc_a)); tb = float(np.mean(sc_b))
    diff = ta - tb
    adv = f"<strong>{name_a}</strong> has a clear advantage" if diff>2 else \
          f"<strong>{name_a}</strong> has a slight edge" if diff>0.5 else \
          f"<strong>{name_b}</strong> has a clear advantage" if diff<-2 else \
          f"<strong>{name_b}</strong> has a slight edge" if diff<-0.5 else "Position is <strong>equal</strong>"
    key = [1,3] if persp=="chess" else [0,5]
    kname = "mobility & center control" if persp=="chess" else "material & ecosystem"
    sa_k = round(float(np.mean([sc_a[i] for i in key])),1)
    sb_k = round(float(np.mean([sc_b[i] for i in key])),1)
    dom = f"{name_a} leads on {kname} ({sa_k} vs {sb_k})" if sa_k>sb_k+1 else \
          f"{name_b} leads on {kname} ({sb_k} vs {sa_k})" if sb_k>sa_k+1 else \
          f"Both competitive on {kname}"
    ks_a = round(float(sc_a[2]),1); ks_b = round(float(sc_b[2]),1)
    risk = f"{name_a} king is exposed (safety {ks_a}/10)" if ks_a<5 else \
           f"{name_b} king is exposed (safety {ks_b}/10)" if ks_b<5 else "Both kings are safe"
    return f"{adv}. {dom}. {risk}."

def board_card(title, subtitle, icon, name_a, name_b, sc_a_w, sc_b_w, sc_a_raw, sc_b_raw, persp, weights):
    board = build_board(sc_a_w, sc_b_w)
    svg = chess.svg.board(board, size=340, colors={"square light":"#F0D9B5","square dark":"#B58863"})
    w = np.array([weights[d] for d in dims])
    ta = round(float(w @ sc_a_raw),2)
    tb = round(float(w @ sc_b_raw),2)
    cap_b = captured_html(board, chess.BLACK)
    cap_w = captured_html(board, chess.WHITE)
    adv = advantage_bar(ta, tb, name_a, name_b)
    desc = description(name_a, name_b, sc_a_w, sc_b_w, persp)
    return f"""
    <div style="background:#1e1c1a;border:1px solid #333;border-radius:12px;padding:16px;width:380px;flex-shrink:0">
      <div style="display:flex;align-items:center;gap:8px;margin-bottom:2px">
        <span style="font-size:18px">{icon}</span>
        <span style="font-size:14px;font-weight:700;color:#fff">{title}</span>
      </div>
      <div style="font-size:10px;color:#555;margin-bottom:14px;padding-left:26px">{subtitle}</div>

      <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:3px">
        <div style="display:flex;align-items:center;gap:6px">
          <div style="width:10px;height:10px;border-radius:50%;background:#444;border:1px solid #666"></div>
          <span style="font-size:12px;color:#bbb;font-weight:500">{name_b}</span>
          <span style="font-size:10px;color:#555">Black</span>
        </div>
        <span style="font-size:12px;color:#666;font-weight:500">{tb}</span>
      </div>
      <div style="min-height:22px;margin-bottom:6px;letter-spacing:1px">{cap_b}</div>

      <div style="border-radius:8px;overflow:hidden;line-height:0;border:1px solid #333">{svg}</div>

      <div style="min-height:22px;margin-top:6px;letter-spacing:1px">{cap_w}</div>
      <div style="display:flex;justify-content:space-between;align-items:center;margin-top:3px">
        <div style="display:flex;align-items:center;gap:6px">
          <div style="width:10px;height:10px;border-radius:50%;background:#e0d9c8;border:1px solid #aaa"></div>
          <span style="font-size:12px;color:#fff;font-weight:500">{name_a}</span>
          <span style="font-size:10px;color:#666">White</span>
        </div>
        <span style="font-size:12px;color:#aaa;font-weight:500">{ta}</span>
      </div>

      {adv}
      <div style="margin-top:12px;font-size:10px;color:#777;line-height:1.6;border-top:1px solid #2a2a2a;padding-top:10px">{desc}</div>
    </div>"""

def dim_table(name_a, name_b, sc_a, sc_b):
    labels = [("♖","Rook","Material","material"),
              ("♘","Knight","Mobility","mobility"),
              ("♗","Bishop","Center control","center_control"),
              ("♕","Queen","Piece coordination","piece_coordination"),
              ("♔","King","King safety","king_safety"),
              ("♙","Pawn","Passed pawns","passed_pawns")]
    rows = ""
    for sym, piece, label, dim in labels:
        i = dims.index(dim)
        sa = round(float(sc_a[i]),1); sb = round(float(sc_b[i]),1)
        wa = round(sa/10*100); wb = round(sb/10*100)
        winner_a = sa > sb + 0.9; winner_b = sb > sa + 0.9
        col_a = "#7fa650" if winner_a else "#555"
        col_b = "#7fa650" if winner_b else "#444"
        badge_a = f'<span style="font-size:9px;background:#7fa650;color:#fff;padding:1px 5px;border-radius:3px;margin-left:4px">+{round(sa-sb,1)}</span>' if winner_a else ""
        badge_b = f'<span style="font-size:9px;background:#7fa650;color:#fff;padding:1px 5px;border-radius:3px;margin-left:4px">+{round(sb-sa,1)}</span>' if winner_b else ""
        rows += f"""
        <tr style="border-bottom:1px solid #2a2a2a">
          <td style="padding:8px 10px;white-space:nowrap">
            <span style="font-size:14px;margin-right:6px">{sym}</span>
            <span style="font-size:11px;color:#777">{label}</span>
          </td>
          <td style="padding:8px 10px">
            <div style="display:flex;align-items:center;gap:8px">
              <div style="width:90px;height:4px;background:#2a2a2a;border-radius:2px;flex-shrink:0">
                <div style="width:{wa}%;height:4px;background:{col_a};border-radius:2px"></div></div>
              <span style="font-size:12px;color:#ddd;min-width:28px">{sa}{badge_a}</span>
            </div>
          </td>
          <td style="padding:8px 10px">
            <div style="display:flex;align-items:center;gap:8px">
              <div style="width:90px;height:4px;background:#2a2a2a;border-radius:2px;flex-shrink:0">
                <div style="width:{wb}%;height:4px;background:{col_b};border-radius:2px"></div></div>
              <span style="font-size:12px;color:#999;min-width:28px">{sb}{badge_b}</span>
            </div>
          </td>
        </tr>"""
    return f"""
    <div style="background:#1e1c1a;border:1px solid #333;border-radius:12px;padding:16px;margin-top:20px">
      <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:12px">
        <span style="font-size:13px;font-weight:600;color:#fff">Dimension breakdown</span>
        <span style="font-size:10px;color:#555">scores 0 – 10</span>
      </div>
      <table style="width:100%;border-collapse:collapse">
        <tr style="border-bottom:1px solid #2a2a2a">
          <th style="padding:6px 10px;color:#444;font-size:10px;font-weight:400;text-align:left">Piece / Dimension</th>
          <th style="padding:6px 10px;font-size:10px;font-weight:500;text-align:left;color:#ddd">
            <span style="display:inline-block;width:8px;height:8px;border-radius:50%;background:#e0d9c8;margin-right:4px;vertical-align:middle"></span>{name_a}
          </th>
          <th style="padding:6px 10px;font-size:10px;font-weight:500;text-align:left;color:#888">
            <span style="display:inline-block;width:8px;height:8px;border-radius:50%;background:#444;border:1px solid #666;margin-right:4px;vertical-align:middle"></span>{name_b}
          </th>
        </tr>
        {rows}
      </table>
    </div>"""

def how_to_read():
    return """
    <div style="background:#1e1c1a;border:1px solid #2a2a2a;border-radius:12px;padding:14px 16px;margin-bottom:20px">
      <div style="font-size:11px;font-weight:600;color:#aaa;margin-bottom:8px;letter-spacing:.05em;text-transform:uppercase">How to read this</div>
      <div style="display:flex;flex-wrap:wrap;gap:12px">
        <span style="font-size:11px;color:#ccc">♖ Rook = Material (funding)</span>
        <span style="font-size:11px;color:#ccc">♘ Knight = Mobility (models + APIs)</span>
        <span style="font-size:11px;color:#ccc">♗ Bishop = Center control (LMSYS + enterprise)</span>
        <span style="font-size:11px;color:#ccc">♕ Queen = Piece coordination (ecosystem)</span>
        <span style="font-size:11px;color:#ccc">♔ King = King safety (regulatory + runway)</span>
        <span style="font-size:11px;color:#ccc">♙ Pawn = Passed pawns (unique models)</span>
        <span style="font-size:11px;color:#aaa">— Piece advanced = higher score on that dimension</span>
        <span style="font-size:11px;color:#aaa">— Captured pieces = missing from standard set</span>
      </div>
    </div>"""

def generate(name_a, name_b, sc_a, sc_b):
    sc_a_chess = apply_weights(sc_a, chess_weights)
    sc_b_chess = apply_weights(sc_b, chess_weights)
    sc_a_biz   = apply_weights(sc_a, business_weights)
    sc_b_biz   = apply_weights(sc_b, business_weights)

    # initials badges
    init_a = "".join(w[0].upper() for w in name_a.split()[:2])
    init_b = "".join(w[0].upper() for w in name_b.split()[:2])

    card_chess = board_card("Chess perspective","Mobility & center control weighted (0.25 each)","♟",
                             name_a,name_b,sc_a_chess,sc_b_chess,sc_a,sc_b,"chess",chess_weights)
    card_biz   = board_card("Business perspective","Material, king safety & coordination weighted (0.20–0.25)","📊",
                             name_a,name_b,sc_a_biz,sc_b_biz,sc_a,sc_b,"business",business_weights)
    table = dim_table(name_a, name_b, sc_a, sc_b)
    legend = how_to_read()
    today = date.today().strftime("%B %d, %Y")

    return f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8">
<title>{name_a} vs {name_b} — Chess Framework</title>
<style>
  *{{box-sizing:border-box;margin:0;padding:0}}
  body{{background:#141412;font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;
       color:#ccc;display:flex;flex-direction:column;align-items:center;padding:32px 16px;min-height:100vh}}
  strong{{color:#fff}}
</style>
</head><body>
<div style="width:100%;max-width:820px">

  <!-- Header -->
  <div style="margin-bottom:28px">
    <div style="font-size:11px;color:#555;letter-spacing:.08em;text-transform:uppercase;margin-bottom:10px">
      AI Competitive Landscape — Chess Framework · {today}
    </div>
    <div style="display:flex;align-items:center;gap:16px;flex-wrap:wrap">
      <div style="display:flex;align-items:center;gap:10px">
        <div style="width:44px;height:44px;border-radius:8px;background:#e0d9c8;display:flex;align-items:center;justify-content:center;font-size:14px;font-weight:700;color:#141412">{init_a}</div>
        <div>
          <div style="font-size:22px;font-weight:700;color:#fff">{name_a}</div>
          <div style="font-size:11px;color:#555">White pieces</div>
        </div>
      </div>
      <div style="font-size:20px;color:#333;font-weight:300;padding:0 8px">vs</div>
      <div style="display:flex;align-items:center;gap:10px">
        <div style="width:44px;height:44px;border-radius:8px;background:#2a2a2a;border:1px solid #444;display:flex;align-items:center;justify-content:center;font-size:14px;font-weight:700;color:#aaa">{init_b}</div>
        <div>
          <div style="font-size:22px;font-weight:700;color:#aaa">{name_b}</div>
          <div style="font-size:11px;color:#555">Black pieces</div>
        </div>
      </div>
    </div>
  </div>

  <!-- How to read -->
  {legend}

  <!-- Boards -->
  <div style="display:flex;gap:20px;flex-wrap:wrap;justify-content:center;margin-bottom:20px">
    {card_chess}
    {card_biz}
  </div>

  <!-- Breakdown table -->
  {table}

  <!-- Footer -->
  <div style="margin-top:28px;padding-top:16px;border-top:1px solid #222;text-align:center">
    <div style="font-size:10px;color:#444;line-height:1.8">
      Scores based on public data: funding (Crunchbase), models (company websites + HuggingFace),
      LMSYS Chatbot Arena rankings, EU AI Act compliance status, estimated runway.<br>
      Chess framework by Mold+Chess · {today}
    </div>
  </div>

</div>
</body></html>"""

def main():
    print("\nAvailable companies:")
    for c in companies: print(f"  - {c}")
    print("  - market")
    print()
    name_a = input("Company A (White): ").strip()
    name_b = input("Company B (Black) or 'market': ").strip()
    try:
        sc_a = get_scores(name_a); sc_b = get_scores(name_b)
    except ValueError as e:
        print(f"Error: {e}"); return
    html = generate(name_a, name_b, sc_a, sc_b)
    fn = f"chess_{name_a.replace(' ','_')}_vs_{name_b.replace(' ','_')}.html"
    with open(fn,"w",encoding="utf-8") as f: f.write(html)
    print(f"\nSaved: {fn}")
    print("Open in your browser.")

if __name__ == "__main__":
    main()