# Exclusão de Tentativas — Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Allow judges to delete erroneously registered attempts, with automatic renumbering and score recalculation.

**Architecture:** Add `excluir_tentativa()` to `scoring.py` that deletes a record and renumbers/recalculates remaining attempts. Add a "Excluir" button in the attempt history section of `pages/2_Juiz.py` with same permission rules as "Corrigir".

**Tech Stack:** Python, SQLAlchemy, Streamlit

---

### Task 1: Write failing tests for `excluir_tentativa`

**Files:**
- Modify: `tests/test_scoring.py`

**Step 1: Write the failing tests**

Add these tests at the end of `tests/test_scoring.py`:

```python
from scoring import excluir_tentativa


def test_excluir_unica_tentativa(db):
    equipe = db.query(Equipe).filter_by(nome="Equipe A").first()
    questao = db.query(Questao).first()
    juiz = db.query(User).first()

    registrar_tentativa(db, equipe.id, questao.id, False, juiz.id)
    tentativa = db.query(Tentativa).first()

    excluir_tentativa(db, tentativa.id)

    restantes = db.query(Tentativa).filter_by(equipe_id=equipe.id, questao_id=questao.id).all()
    assert len(restantes) == 0


def test_excluir_primeira_renumera_seguintes(db):
    equipe = db.query(Equipe).filter_by(nome="Equipe A").first()
    questao = db.query(Questao).first()
    juiz = db.query(User).first()

    registrar_tentativa(db, equipe.id, questao.id, False, juiz.id)
    registrar_tentativa(db, equipe.id, questao.id, False, juiz.id)
    registrar_tentativa(db, equipe.id, questao.id, True, juiz.id)

    # Delete the first attempt
    primeira = db.query(Tentativa).filter_by(equipe_id=equipe.id, questao_id=questao.id, numero=1).first()
    excluir_tentativa(db, primeira.id)

    restantes = (
        db.query(Tentativa)
        .filter_by(equipe_id=equipe.id, questao_id=questao.id)
        .order_by(Tentativa.numero)
        .all()
    )
    assert len(restantes) == 2
    # Old attempt 2 (errou) is now attempt 1
    assert restantes[0].numero == 1
    assert restantes[0].acertou is False
    assert restantes[0].pontos == 0
    # Old attempt 3 (acertou) is now attempt 2 → 80 pts instead of 50
    assert restantes[1].numero == 2
    assert restantes[1].acertou is True
    assert restantes[1].pontos == 80


def test_excluir_do_meio_renumera(db):
    equipe = db.query(Equipe).filter_by(nome="Equipe A").first()
    questao = db.query(Questao).first()
    juiz = db.query(User).first()

    registrar_tentativa(db, equipe.id, questao.id, False, juiz.id)
    registrar_tentativa(db, equipe.id, questao.id, False, juiz.id)
    registrar_tentativa(db, equipe.id, questao.id, True, juiz.id)

    # Delete the middle attempt
    segunda = db.query(Tentativa).filter_by(equipe_id=equipe.id, questao_id=questao.id, numero=2).first()
    excluir_tentativa(db, segunda.id)

    restantes = (
        db.query(Tentativa)
        .filter_by(equipe_id=equipe.id, questao_id=questao.id)
        .order_by(Tentativa.numero)
        .all()
    )
    assert len(restantes) == 2
    # First attempt stays as 1
    assert restantes[0].numero == 1
    assert restantes[0].acertou is False
    assert restantes[0].pontos == 0
    # Old attempt 3 (acertou) is now attempt 2 → 80 pts
    assert restantes[1].numero == 2
    assert restantes[1].acertou is True
    assert restantes[1].pontos == 80


def test_excluir_afeta_leaderboard(db):
    equipe_a = db.query(Equipe).filter_by(nome="Equipe A").first()
    questao = db.query(Questao).first()
    juiz = db.query(User).first()

    # Equipe A: misses first, hits second (80 pts)
    registrar_tentativa(db, equipe_a.id, questao.id, False, juiz.id)
    registrar_tentativa(db, equipe_a.id, questao.id, True, juiz.id)

    ranking = calcular_leaderboard(db)
    equipe_a_pts = next(r for r in ranking if r["equipe"] == "Equipe A")
    assert equipe_a_pts["pontos"] == 80

    # Delete the wrong first attempt → acerto becomes attempt 1 → 100 pts
    primeira = db.query(Tentativa).filter_by(equipe_id=equipe_a.id, questao_id=questao.id, numero=1).first()
    excluir_tentativa(db, primeira.id)

    ranking = calcular_leaderboard(db)
    equipe_a_pts = next(r for r in ranking if r["equipe"] == "Equipe A")
    assert equipe_a_pts["pontos"] == 100
```

**Step 2: Run tests to verify they fail**

Run: `python3 -m pytest tests/test_scoring.py -v -k "excluir"`
Expected: FAIL — `ImportError: cannot import name 'excluir_tentativa' from 'scoring'`

---

### Task 2: Implement `excluir_tentativa` in scoring.py

**Files:**
- Modify: `scoring.py`

**Step 1: Add the function**

Add at the end of `scoring.py`:

```python
def excluir_tentativa(db: Session, tentativa_id: int) -> None:
    """Delete an attempt and renumber/recalculate remaining attempts for the same team+question."""
    tentativa = db.query(Tentativa).get(tentativa_id)
    if not tentativa:
        return

    equipe_id = tentativa.equipe_id
    questao_id = tentativa.questao_id

    db.delete(tentativa)
    db.flush()

    # Renumber and recalculate remaining attempts
    restantes = (
        db.query(Tentativa)
        .filter_by(equipe_id=equipe_id, questao_id=questao_id)
        .order_by(Tentativa.created_at)
        .all()
    )

    for i, t in enumerate(restantes, start=1):
        t.numero = i
        if t.acertou:
            t.pontos = PONTOS_POR_TENTATIVA.get(i, 0)
        else:
            t.pontos = 0

    db.commit()
```

**Step 2: Run tests to verify they pass**

Run: `python3 -m pytest tests/test_scoring.py -v -k "excluir"`
Expected: All 4 new tests PASS

**Step 3: Run full test suite**

Run: `python3 -m pytest tests/ -v`
Expected: All 16 tests PASS (12 existing + 4 new)

**Step 4: Commit**

```bash
git add scoring.py tests/test_scoring.py
git commit -m "feat: add excluir_tentativa with renumbering and score recalculation"
```

---

### Task 3: Add "Excluir" button to Juiz page

**Files:**
- Modify: `pages/2_Juiz.py`

**Step 1: Add import**

In `pages/2_Juiz.py` line 5, add `excluir_tentativa` to the import:

```python
from scoring import registrar_tentativa, excluir_tentativa, PONTOS_POR_TENTATIVA
```

**Step 2: Add Excluir button in the attempt history**

Replace the history section (lines 312-332) with:

```python
# --- Attempt history & correction ---
if tentativas_anteriores:
    st.divider()
    st.markdown("#### Historico de tentativas")
    for t in tentativas_anteriores:
        with st.container(border=True):
            status_icon = "✅" if t.acertou else "❌"
            c1, c2, c3 = st.columns([5, 1, 1])
            c1.markdown(
                f"**Tentativa {t.numero}** — {status_icon} {'Acertou' if t.acertou else 'Errou'} — **{t.pontos} pts**"
            )
            can_modify = (t.juiz_id == user["id"]) or (user["role"] == "admin")
            if can_modify:
                if c2.button("Corrigir", key=f"corrigir_{t.id}"):
                    t.acertou = not t.acertou
                    if t.acertou:
                        t.pontos = PONTOS_POR_TENTATIVA.get(t.numero, 0)
                    else:
                        t.pontos = 0
                    db.commit()
                    st.rerun()
                if c3.button("Excluir", key=f"excluir_{t.id}", type="primary"):
                    excluir_tentativa(db, t.id)
                    st.rerun()
```

Key changes:
- `st.columns([5, 1])` → `st.columns([5, 1, 1])` to add third column
- Renamed `can_correct` → `can_modify` (same logic applies to both buttons)
- Added `c3.button("Excluir")` with `type="primary"` for visual distinction
- Calls `excluir_tentativa(db, t.id)` then `st.rerun()`

**Step 3: Run full test suite**

Run: `python3 -m pytest tests/ -v`
Expected: All 16 tests PASS

**Step 4: Manual verification**

Run: `streamlit run app.py`
- Navigate to Juiz page, log in
- Select a team and question with existing attempts
- Verify "Excluir" button appears next to "Corrigir"
- Click Excluir → attempt removed, remaining renumbered, points updated
- Check Leaderboard → scores reflect the change

**Step 5: Commit**

```bash
git add pages/2_Juiz.py
git commit -m "feat: add delete button for attempts in judge page"
```
