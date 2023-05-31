<div align="center">

  # League Wizard
  An async python framework to implement plugins in League of Legends

</div>

## <del>不打联盟了，暂停维护了。</del> 继续维护

### 环境要求

1. python >= 3.10
2. 见 requirements.txt

### 使用方法

1. 下载本仓库
2. 命令行运行`python main.py`

### 安装插件

LeagueWizard仅是一个插件框架，任何实际性的功能需要通过插件实现。

项目中自带三个样例插件（目前也仅有这三个插件）:

- ApplyPerk - 符文库（保存/应用符文）
- AutoPick - 选人阶段自动选择英雄
- Statistic - 统计一局游戏中你角色的属性值


1. 插件存放在`plugins`目录中
2. 请不要将不是插件的文件放入插件目录

**警告：插件加载器会自动运行插件，第三方插件中可能存在恶意代码，请不要使用任何不信任的插件**


### 插件额外说明

ApplyPerk一目了然，无需多言。

---

AutoPick需要知道英雄id，可以从[这里](https://ddragon.leagueoflegends.com/cdn/13.10.1/data/zh_CN/champion.json)获取。

`Ctrl+f`搜索你要找的英雄，以`瑟提`为例，可以找到以下内容：

```
"Sett":{"version":"13.10.1","id":"Sett","key":"875","name":"腕豪","title":"瑟提","blurb":"在与诺克萨斯的战争结束之后，艾欧尼亚的地下王国日渐兴起，瑟提在其中脱颖而出，成为了一方霸主。虽然他一开始只是纳沃利的搏击场里的无名小卒，但他有着一身蛮力，而且极其耐打，很快就名声鹊起。等到当地的搏击手尽数被他击败之后，瑟提靠着一腔勇武，掌控了自己曾经浴血奋战的搏击场。","info":{"attack":8,"defense":5,"magic":1,"difficulty":2},"image":{"full":"Sett.png","sprite":"champion3.png","group":"champion","x":96,"y":96,"w":48,"h":48},"tags":["Fighter","Tank"],"partype":"豪意","stats":{"hp":670,"hpperlevel":114,"mp":0,"mpperlevel":0,"movespeed":340,"armor":33,"armorperlevel":5.2,"spellblock":28,"spellblockperlevel":2.05,"attackrange":125,"hpregen":7,"hpregenperlevel":0.5,"mpregen":0,"mpregenperlevel":0,"crit":0,"critperlevel":0,"attackdamage":60,"attackdamageperlevel":4,"attackspeedperlevel":1.75,"attackspeed":0.625}}
```

注意看`"name":"腕豪"`前面的`"key":"875"`，875即是腕豪的id。

---

Statistic插件比较复杂，分为两个步骤1. 录制数据 2. 生成图表

开启`开启/关闭数据统计`（绿色表示开启）即可自动录制每局数据。

选择`生成统计文件`，选择录制好的数据文件，即可生成tensorboard图表数据，数据生成在`plugins/Statistic/tensorboard_data`目录下。

命令行执行`tensorboard --logdir <LeagueWizard路径>/plugins/Statistic/tensorboard_data`即可启动tensorboard服务端。

浏览器访问[http://localhost:6006/](http://localhost:6006/)即可查看数据图表。

### 其他

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
> 详细使用方法参考示例插件



> 可能有帮助的参考:
>
> - https://github.com/matsjla/league-connect
> - [Official League Client API Documentation](https://developer.riotgames.com/docs/lol#league-client-api)
> - [Unofficial League Client API Documentation (HextechDocs)](https://www.hextechdocs.dev/lol/lcuapi)
