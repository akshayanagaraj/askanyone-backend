from contextlib import contextmanager
from sqlalchemy import create_engine
from sqlalchemy.orm import Session as SaSession
from sqlalchemy.orm import scoped_session, sessionmaker
from flask import current_app
import os

SQLALCHEMY_ENGINE_OPTIONS = {
    'pool_size': int(os.environ.get('SQL_POOL_SIZE', 5)),
    'max_overflow': int(os.environ.get('SQL_POOL_MAX_OVERFLOW', 7)),
    'pool_recycle': int(os.environ.get('SQL_POOL_RECYCLE_MINS', 15)) * 60,
    'connect_args': {
        'application_name': os.environ.get('POD_NAME') or 'dm_backend',
    }
}


class TenantSession(SaSession):
    """
    Multi-Tenant database session, enables multi db session based on tenant id.
    """
    _tenant_id = None

    def get_bind(self, mapper=None, clause=None):
        # print(os.environ)
        # print(os.environ, os.environ.get('DATABASE_URL'),'env variables')
        return create_engine('postgresql+psycopg2://postgres:postgres@127.0.0.1:5432/askanyone', **SQLALCHEMY_ENGINE_OPTIONS)

    def using_bind(self, tenant_id):
        """
        :param tenant_id: tenant_id for the db session
        :return: sqlalchemy session
        """
        _session = TenantSession()
        vars(_session).update(vars(self))
        _session._tenant_id = tenant_id
        return _session


Session = scoped_session(
    sessionmaker(class_=TenantSession, autocommit=False, autoflush=False))


@contextmanager
def db_session():
    session = Session()
    try:
        yield session
        session.commit()
        current_app.logger.debug('session commit')
    except Exception as e:
        current_app.logger.exception(e)
        current_app.logger.debug('session rollback')
        session.rollback()
        raise
    finally:
        current_app.logger.debug('session close')
        session.close()
