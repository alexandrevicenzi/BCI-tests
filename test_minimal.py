import pytest
from bci_tester.data import MICRO_CONTAINER
from bci_tester.data import MINIMAL_CONTAINER


CONTAINER_IMAGES = [MINIMAL_CONTAINER, MICRO_CONTAINER]

MINIMAL_IMAGE_MAX_SIZE = 40 * 1024 * 1024
MICRO_IMAGE_MAX_SIZE = 25 * 1024 * 1024


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "container,size",
    [
        (MICRO_CONTAINER, MICRO_IMAGE_MAX_SIZE),
        (MINIMAL_CONTAINER, MINIMAL_IMAGE_MAX_SIZE),
    ],
    indirect=["container"],
)
async def test_minimal_image_size(container, size, container_runtime):
    assert (
        await container_runtime.get_image_size(container.image_url_or_id)
        < size
    )


def test_fat_packages_absent(auto_container):
    for pkg in ("zypper", "grep", "diff", "sed", "info", "man"):
        assert not auto_container.connection.exists(pkg)


def test_base_packages_present(auto_container):
    for pkg in ("cat", "sh", "bash"):
        assert auto_container.connection.exists(pkg)


@pytest.mark.parametrize(
    "container", [MICRO_CONTAINER], indirect=["container"]
)
def test_rpm_absent_in_micro(container):
    assert not container.connection.exists(
        "rpm"
    ), "rpm must not be present in the micro container"


@pytest.mark.parametrize(
    "container", [MINIMAL_CONTAINER], indirect=["container"]
)
def test_rpm_present_in_micro(container):
    assert container.connection.exists(
        "rpm"
    ), "rpm must be present in the minimal container"