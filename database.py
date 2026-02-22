import os
from sqlalchemy import create_engine, inspect, text
from sqlalchemy.orm import sessionmaker, DeclarativeBase

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data.db")
DATABASE_URL = f"sqlite:///{DB_PATH}"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine, expire_on_commit=False)


class Base(DeclarativeBase):
    pass


_initialized = False


def init_db():
    """Create tables and default admin. Safe to call multiple times."""
    global _initialized
    if _initialized:
        return
    _initialized = True

    # Import here to avoid circular imports
    from models import User
    from auth import hash_password

    Base.metadata.create_all(bind=engine)

    # Migrate: add enunciado column if missing (for existing databases)
    inspector = inspect(engine)
    columns = [c["name"] for c in inspector.get_columns("questoes")]
    if "enunciado" not in columns:
        with engine.connect() as conn:
            conn.execute(text("ALTER TABLE questoes ADD COLUMN enunciado TEXT DEFAULT ''"))
            conn.commit()

    # Migrate: remove FK constraint on juiz_id in tentativas (for existing databases)
    if "tentativas" in inspector.get_table_names():
        fks = inspector.get_foreign_keys("tentativas")
        has_juiz_fk = any(
            fk.get("referred_table") == "users" for fk in fks
        )
        if has_juiz_fk:
            with engine.connect() as conn:
                conn.execute(text(
                    "CREATE TABLE tentativas_new ("
                    "id INTEGER PRIMARY KEY AUTOINCREMENT, "
                    "equipe_id INTEGER NOT NULL REFERENCES equipes(id), "
                    "questao_id INTEGER NOT NULL REFERENCES questoes(id), "
                    "numero INTEGER NOT NULL, "
                    "acertou BOOLEAN NOT NULL, "
                    "pontos INTEGER NOT NULL DEFAULT 0, "
                    "juiz_id INTEGER NOT NULL, "
                    "created_at DATETIME)"
                ))
                conn.execute(text(
                    "INSERT INTO tentativas_new SELECT * FROM tentativas"
                ))
                conn.execute(text("DROP TABLE tentativas"))
                conn.execute(text("ALTER TABLE tentativas_new RENAME TO tentativas"))
                conn.commit()

    # Seed: limpar dados e recriar admin, juízes, regatas e questões
    from seed_data import ADMIN_PASSWORD, JUIZES, REGATAS
    from models import Tentativa, Questao, Regata, Equipe

    db = SessionLocal()
    try:
        # Limpar tudo na ordem correta (FKs)
        db.query(Tentativa).delete()
        db.query(Questao).delete()
        db.query(Regata).delete()
        db.query(Equipe).delete()
        db.query(User).delete()
        db.flush()

        # Admin
        db.add(User(
            username="admin",
            password_hash=hash_password(ADMIN_PASSWORD),
            role="admin",
        ))

        # Juízes
        for username, password in JUIZES:
            db.add(User(
                username=username,
                password_hash=hash_password(password),
                role="juiz",
            ))

        # Regatas e questões (15 regatas: 5 por dia × 3 dias)
        img_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                               "assets", "images", "questoes")
        first = True
        for dia, dia_data in REGATAS.items():
            nivel = dia_data["nivel"]
            for regata_num, questoes_list in dia_data["questoes"].items():
                nome = f"Regata {regata_num} - Dia {dia}"
                regata = Regata(nome=nome, ativa=first)
                first = False
                db.add(regata)
                db.flush()

                for enunciado, img_filename in questoes_list:
                    img_data = None
                    if img_filename:
                        img_path = os.path.join(img_dir, img_filename)
                        if os.path.exists(img_path):
                            with open(img_path, "rb") as f:
                                img_data = f.read()
                    db.add(Questao(
                        regata_id=regata.id,
                        nivel=nivel,
                        enunciado=enunciado,
                        imagem=img_data,
                        imagem_filename=img_filename,
                    ))

        db.commit()
    finally:
        db.close()


def get_db():
    """Create a fresh session. Ensures DB is initialized first."""
    init_db()
    db = SessionLocal()
    return db
