from archtool.global_types import AppModule
from archtool.layers.default_layers import (
    default_layers,
    InfrastructureLayer,
    DomainLayer,
    ApplicationLayer,
    PresentationLayer,
)

# Standard 4-layer list (order: outermost → innermost)
app_layers = default_layers  # [PresentationLayer, ApplicationLayer, DomainLayer, InfrastructureLayer]

APPS: list[AppModule] = [
    AppModule("app.users"),
    AppModule("app.todos"),
]
