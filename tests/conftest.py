import pathlib
from typing import Generator
import pytest
from harvesters import core

TRANSPORT_LAYER_FILE = pathlib.Path(
    "/opt/mvIMPACT_Acquire/lib/x86_64/mvGenTLProducer.cti"
)


class GigEVisionClient:
    def __init__(self, transport_layer_file: pathlib.Path):
        self._transport_layer_file = transport_layer_file
        self._harvester = None

    @property
    def harvester(self):
        if not self._harvester:
            self._harvester = core.Harvester()
            self._harvester.add_cti_file(self._transport_layer_file)
        return self._harvester

    def connect(self) -> None: ...

    def disconnect(self) -> None: ...

    def find_cameras(self) -> list[str]: ...


@pytest.fixture
def gigevision_client() -> Generator[GigEVisionClient, None, None]:
    yield GigEVisionClient(TRANSPORT_LAYER_FILE)
