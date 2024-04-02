#!/usr/bin/env python

import asyncio

from metagpt.roles.researcher import RESEARCH_PATH, Researcher


async def main():
    topic = "阿里巴巴股价走势"
    role = Researcher(language="zh-cn")
    await role.run(topic)
    print(f"save report to {RESEARCH_PATH / f'{topic}.md'}.")


if __name__ == "__main__":
    asyncio.run(main())
