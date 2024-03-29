import time

from ray import serve
from ray.serve.handle import RayServeHandle, DeploymentHandle


@serve.deployment
class LightLoad:
    async def __call__(self) -> str:
        start = time.time()
        while time.time() - start < 0.1:
            pass

        return "light"


@serve.deployment
class HeavyLoad:
    async def __call__(self) -> str:
        start = time.time()
        while time.time() - start < 0.2:
            pass

        return "heavy"


@serve.deployment
class Driver:
    def __init__(self, a_handle: RayServeHandle, b_handle: RayServeHandle):
        self.a_handle: DeploymentHandle = a_handle.options(use_new_handle_api=True)
        self.b_handle: DeploymentHandle = b_handle.options(use_new_handle_api=True)

    async def __call__(self) -> str:
        a_future = self.a_handle.remote()
        b_future = self.b_handle.remote()

        return (await a_future), (await b_future)


app = Driver.bind(HeavyLoad.bind(), LightLoad.bind())

