<div align="center">

  # League Wizard
  An async python framework to implement plugins in League of Legends

</div>

## <del>不打联盟了，暂停维护了。</del> 继续维护

### 环境要求

1. python >= 3.10
2. 见 requirements.txt

### 使用方法

1. 基于本项目[创建模板](https://github.com/ninthseason/LeagueWizard/generate)
2. 将创建好的仓库克隆至本地
3. 修改`main.py`中`GlobalConfig.set_config_file_path("<你期望的配置文件路径>")`
4. 命令行进入项目文件夹，运行`python main.py`

### 插件的安装

LeagueWizard仅是一个插件框架，任何实际性的功能需要通过插件实现。

项目中自带两个样例插件:

- ApplyPerk - 符文库（保存/应用符文）
- AutoPick - 选人阶段自动选择英雄

更多的插件请通过其他渠道获取，或者自行编写

> 本项目没有任何官方的插件平台、qq群，不包含在本仓库内的插件均为第三方插件。
>
> 任何采用本框架的插件禁止闭源与收费。

1. 插件目录: `./plugins/`
2. 将插件放入插件目录即可
3. 插件是一个文件夹（python package），请不要将插件以外的任何文件/文件夹放入插件目录

**警告：插件加载器会自动运行插件，第三方插件中可能存在恶意代码，请不要使用任何不信任的插件**

### 更多

> 原理：
>
> 1. LOL客户端提供了通讯端口，在请求头添加 Authorization(由auth-token得来) 后可以通过https请求向客户端发送指令
> 2. 通讯端口及 auth-token 可以通过查询`LeagueClientUx.exe`的启动参数获得
> 3. 可以通过通讯端口和 auth-token 与客户端建立wss连接，以监听一些事件



> 插件的开发：
>
> 一个插件应由以下部分组成
>
> - 逻辑代码
>   - 事件监听器
>   - 事件回调函数
> - 主菜单选项
>   - 显示文本
>   - 回调函数
> - 配置条目
>
> 详细使用方法见样例插件`AutoPick.__init__.py`代码注释



> 可能有帮助的参考:
>
> - https://github.com/matsjla/league-connect
> - [Official League Client API Documentation](https://developer.riotgames.com/docs/lol#league-client-api)
> - [Unofficial League Client API Documentation (HextechDocs)](https://www.hextechdocs.dev/lol/lcuapi)
