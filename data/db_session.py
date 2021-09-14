from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import NullPool

DbBase = declarative_base()
__factory = None


def global_init(db_data: str, db_type: str = 'postgresql'):
    global __factory
    if __factory:
        return
    db_data = db_data.strip()
    if not db_data:
        raise Exception('Не удалось подключиться к %s' % db_data)
    if db_type == 'postgresql':
        db_data = db_data.split()
        try:
            dbname_idx = db_data.index(list(filter(lambda x: 'dbname' in x, db_data))[0])
            assert dbname_idx != -1
            dbname = db_data.pop(dbname_idx).split('=')[-1]
        except (IndexError, AssertionError):
            raise Exception('Не указано название БД')
        conn_str = f'postgresql:///{dbname}?{db_data[0]}&%s' % '&'.join(db_data[1:])
        print(f'conn_str: {conn_str}')
    else:
        conn_str = f'{db_type}:///{db_data}'
    engine = create_engine(conn_str, echo=False, poolclass=NullPool)
    __factory = sessionmaker(bind=engine)
    from . import __all_models
    DbBase.metadata.create_all(engine)


def create_session() -> Session:
    global __factory
    return __factory()