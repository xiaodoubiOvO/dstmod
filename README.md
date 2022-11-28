# dstmod

#### 介绍
自用 提取饥荒modoverrides.lua模组ID

支持一键输出`dedicated_server_mods_setup.lua`

#### 软件架构
1. 正则提取modoverrides.lua模组ID
2. aiohttp异步请求mod页面获取信息
3. PrettyTable打印表格

#### 安装教程
Windows可以在 [releases](https://gitee.com/xiaodoubiOvO/dstmod/releases) 下载exe
1. 安装Python3
2. 安装依赖`pip install aiohttp prettytable`
3. 下载dstmod.py

#### 使用说明
1. 运行程序
    - python dstmod.py modoverrides.lua路径
    - 或者把modoverrides.lua拖到exe打开
2. 等待解析完成
3. 最后输入"y"可以输出`dedicated_server_mods_setup.lua`
4. 执行完毕

#### 关于'dedicated_server_mods_setup.lua'
服务器模组不自动下载、不生效和不自动更新可能就是没把模组id加到这个文件里，需要手动添加：ServerModSetup("模组ID")
