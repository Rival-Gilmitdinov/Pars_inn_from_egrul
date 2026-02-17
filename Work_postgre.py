from Parser_pdf import data_value
from Work_excel import sp
import psycopg2
from sqlalchemy import create_engine, inspect
from config import user, password, host, db, port
from sqlalchemy.orm import declarative_base, Mapped, mapped_column, Session

engine = create_engine(f'postgresql+psycopg2://{user}:{password}@{host}:{port}/{db}')
Base = declarative_base()

class Inn(Base):
    __tablename__ = 'data_on_inn'
    id : Mapped[int] = mapped_column(primary_key=True)
    inn_company : Mapped[str | None]
    name : Mapped[str | None]
    capital : Mapped[str | None]
    activity : Mapped[str | None]

inspector = inspect(engine)
if not inspector.has_table('data_on_inn'):
    Base.metadata.create_all(bind=engine)

class Append_table_postrge():
    def app(self, spisok, list_inn, error_type, error_data):
        with Session(engine) as session:
            session.query(Inn).delete()
            session.commit()
            for value in spisok:
                n = 0
                data = Inn(inn_company=f'{list_inn[n]}', name=f'{value["Полное наименование на русском языке"]}', capital=f'{value["Сведения об уставном капитале / складочном капитале / уставном фонде / паевом фонде"]}',
                           activity=f'{value["Сведения об основном виде деятельности"]}')
                n += 1
                session.add(data)
                session.commit()
            if error_type:
                for key_error, value_error, in error_type.items():
                    data_error = Inn(inn_company=f'{key_error}', name=f'{value_error}')
                    session.add(data_error)
                    session.commit()
            if error_data:
                for key_error_2, value_error_2, in error_data.items():
                    data_error_2 = Inn(inn_company=f'{key_error_2}', name=f'{value_error_2}')
                    session.add(data_error_2)
                    session.commit()


app = Append_table_postrge()

# app.app(data_value, sp[0], sp[1], sp[2])