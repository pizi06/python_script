# -*- coding:utf8 -*-

import asyncio
async def my_task(seconds):
    print("start sleeping for {} seconds".format(seconds))
    await asyncio.sleep(seconds)
    print("end sleeping for {} seconds".format(seconds))

all_tasks = asyncio.gather(my_task(4), my_task(2))
loop = asyncio.get_event_loop()
loop.run_until_complete(all_tasks)
loop.close()
