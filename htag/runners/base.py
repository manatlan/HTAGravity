from typing import TYPE_CHECKING, Union, Type
if TYPE_CHECKING:
    from ..server import App

class BaseRunner:
    """Base class for all runners that execute an App."""
    def __init__(self, app: Union[Type["App"], "App"]):
        self.app = app

    def run(self, host: str = "127.0.0.1", port: int = 8000) -> None:
        """Must be implemented by subclasses to start the server/UI."""
        raise NotImplementedError()
