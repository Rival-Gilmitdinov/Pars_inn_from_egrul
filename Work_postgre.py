from Parser_pdf import data_value
import psycopg2
from sqlalchemy import create_engine, inspect
from config import user, password, host, db, port
from sqlalchemy.orm import declarative_base, Mapped, mapped_column, Session

engine = create_engine(f'postgresql+psycopg2://{user}:{password}@{host}:{port}/{db}')
Base = declarative_base()

class Inn(Base):
    __tablename__ = 'data_on_inn'
    id : Mapped[int] = mapped_column(primary_key=True)
    name : Mapped[str]
    capital : Mapped[str]
    activity : Mapped[str]

inspector = inspect(engine)
if not inspector.has_table('data_of_html'):
    Base.metadata.create_all(bind=engine)

class Append_table_postrge():
    def app(self, spisok):
        with Session(engine) as session:
            for value in spisok:
                data = Inn(name=f'{value["Полное наименование на русском языке"]}', capital=f'{value["Сведения об уставном капитале / складочном капитале / уставном фонде / паевом фонде"]}',
                           activity=f'{value["Сведения об основном виде деятельности"]}')
                session.add(data)
                session.commit()

