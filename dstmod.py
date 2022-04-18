#!/usr/bin/python3
import re, os, time, sys
import aiohttp
import asyncio
from prettytable import PrettyTable
from urllib.request import getproxies

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.74 Safari/537.36 Edg/99.0.1150.55',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
}
print('=== 解析modoverrides.lua提取modID v0.5 ===')
try:
    path = os.path.join(sys.argv[1])
except:
    path = os.path.join(input('modoverrides.lua路径：'))
proxy = getproxies().get('http')


async def fetch(session, modid):
    url = f'https://steamcommunity.com/sharedfiles/filedetails/?id={modid}'
    try:
        # print(modid)
        async with session.get(url=url, headers=headers, timeout=5, proxy=proxy) as req:
            if req.status == 200:
                html = await req.text()
                name = re.search(r'<div class="workshopItemTitle">(.+)</div>', html).group(1)
                return modid, name
            return modid, '获取失败'
    except:
        return modid, '获取失败'


async def get_mod_name(mods):
    conn = aiohttp.TCPConnector(ssl=False)
    # semaphore = asyncio.Semaphore(6)
    async with aiohttp.ClientSession(connector=conn) as session:
        tasks = [asyncio.create_task(fetch(session, mod)) for mod in mods]
        result = await asyncio.gather(*tasks)
        return result


def main():
    if os.path.exists(path):
        with open(path, encoding='utf-8') as f:
            data = f.read()

        modid = re.findall(r'"workshop-(\d+)"', data)
        print(f'检测到 {len(modid)} 个MOD...')
        result = []
        print('正在异步请求mod主页获取信息(需要网络)...')
        s_t = time.time()
        loop = asyncio.get_event_loop()
        result = loop.run_until_complete(get_mod_name(modid))
        e_t = time.time()
        if result:
            table = PrettyTable(['ID', 'NAME'])
            for i in result:
                table.add_row([i[0], i[1]])
            print(table)
        print(f'请求耗时：{e_t-s_t}')

        # print('modID: {}\n'.format(','.join(modid)))
        mods = ['ServerModSetup("{}")'.format(i) for i in modid]
        out = input('是否要输出到"dedicated_server_mods_setup.lua"[y/N]：') or 'n'
        if out in ['y', 'Y']:
            out_path = os.path.abspath('dedicated_server_mods_setup.lua')
            with open(out_path, 'w', encoding='utf-8') as f:
                f.write('\n'.join(mods))
                f.write('\n')
            print('输出完毕：{}'.format(out_path))
    else:
        print('错误：找不到modoverrides.lua文件，请确认路径是否正确')
    input('执行完毕！')


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        pass
