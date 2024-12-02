from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dependency_injector import containers, providers
from opentelemetry.instrumentation.sqlalchemy import SQLAlchemyInstrumentor

from src.app.configurator import config
from src.app.adapters.use_cases.tutoring_session import TutoringSessionService
from src.app.adapters.units_of_work.tutoring_session import TutoringSessionDatabaseUnitOfWork

URL = config.get_database_uri()
print(f"URL: {URL}")
ENGINE = create_engine(url=URL)


def get_default_session_factory():
    return sessionmaker(bind=ENGINE)


class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(
        packages=[
            "src.app.adapters.entrypoints.api.v1",
        ]
    )

    SQLAlchemyInstrumentor().instrument(
        engine=ENGINE, enable_commenter=True, commenter_options={}
    )
    DEFAULT_SESSION_FACTORY = get_default_session_factory

    tutoring_session_uow = providers.Singleton(
        TutoringSessionDatabaseUnitOfWork, session_factory=DEFAULT_SESSION_FACTORY
    )

    tutoring_session_service = providers.Factory(
        TutoringSessionService,
        uow=tutoring_session_uow,
    )

