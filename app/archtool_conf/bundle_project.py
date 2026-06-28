import pathlib
from inspect import isclass

from fastapi import FastAPI
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession, AsyncEngine

from archtool.dependency_injector import DependencyInjector
from web_fractal.building_utils import import_all_models
from web_fractal.http.interfaces import HttpControllerABC
from web_fractal.db import Base

from app.config import DATABASE_URL
from app.archtool_conf.custom_layers import APPS, app_layers

BACKEND_ROOT = pathlib.Path(__file__).parent.parent.parent  # todo_app/


def bundle(app: FastAPI) -> tuple[DependencyInjector, AsyncEngine]:
    """
    Wire the full DI graph and attach all HTTP controllers to the FastAPI app.

    Returns the injector and the async engine (so the caller can run create_all
    on the same engine that the session_maker will use).
    """
    # 1. Create injector
    injector = DependencyInjector(
        modules_list=APPS,
        layers=app_layers,
        project_root=BACKEND_ROOT,
    )

    # 2. Register async resources BEFORE inject()
    engine = create_async_engine(DATABASE_URL, echo=False)
    session_maker = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)
    injector.register(key=async_sessionmaker, value=session_maker, inject_into=False)

    # 3. Import all ORM models so Base.metadata is complete
    import_all_models(Base=Base)

    # 4. Run DI (layer validation happens between Pass 1 and Pass 2)
    injector.inject()

    # 5. Register FastAPI routers from all found controllers.
    # web_fractal.building_utils.initialize_controllers_api uses the legacy
    # injector._dependencies attribute (v0.x); archtool v2.x uses the public
    # injector.dependencies dict — we replicate the same logic here.
    for instance in injector.dependencies.values():
        if isclass(type(instance)) and isinstance(instance, HttpControllerABC):
            instance.init_http_routes()
            app.include_router(instance.router)

    return injector, engine
