#!/usr/bin/env python

import asyncio

from metagpt.roles.researcher import RESEARCH_PATH, Researcher


async def main():
    topic = "中国的代运营商（帮助实体商家在tiktok等平台上运营）如何在当下的tiktok电商中找到爆发的机会"
    role = Researcher(language="zh-cn")
    await role.run(topic)
    print(f"save report to {RESEARCH_PATH / f'{topic}.md'}.")


if __name__ == "__main__":
    asyncio.run(main())
