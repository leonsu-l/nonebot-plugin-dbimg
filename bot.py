import nonebot
from nonebot.adapters.onebot.v11 import Adapter as ONEBOT_V11Adapter

from nonebot.adapters.qq import Adapter as QQAdapter



nonebot.init()

driver = nonebot.get_driver()
driver.register_adapter(ONEBOT_V11Adapter)

driver.register_adapter(QQAdapter)


nonebot.load_from_toml("pyproject.toml")

if __name__ == "__main__":
    nonebot.run()