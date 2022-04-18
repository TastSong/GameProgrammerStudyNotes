# 第一章 网络游戏的开端

1. HTTP
2. Socket
3. TCP
4. UDP

# 第二章 分身有术：异步和多路复用

1. 异步
2. 状态检测Poll
3. 多路复用Select
4. Select服务端、Select客户端

# 第三章 实践出真知：大乱斗游戏

1. 搭建场景：角色类Human、类结构设计、 BaseHuman、角色预设、CtrlHuman、SyncHuman
2. 网络模块 ：委托、 通信协议、消息队列、NetManager类、测试网络模块
3. 进入游戏：Enter协议、创建角色、接收Enter协议、测试Enter协议
4. 服务端如何处理消息：反射机制、消息处理函数、 事件处理、玩家数据、处理Enter协议
5. 玩家列表：List协议、客户端处理、服务端处理、测试
6. 移动同步：Move协议、客户端处理、 服务端处理、测试
7. 玩家离开：Leave协议、客户端处理、服务端处理、测试
8. 攻击动作：Attack协议、播放攻击动作、客户端处理、服务端处理、测试
9. 攻击伤害：Hit协议、客户端处理、服务端处理
10. 角色死亡：Die协议、客户端处理、测试

# 第四章 正确收发数据流

1. TCP数据流：系统缓冲区、粘包半包现象、人工重现粘包现象
2. 解决粘包问题的方法：长度信息法、固定长度法、结束符号法
3. 大端小端问题
4. 完整发送数据
5. 不完整发送示例、 如何解决发送不完整问题、ByteArray和Queue、解决线程冲突、为什么要使用队列
6. 高效的接收数据、不足之处、完整的ByteArray、将ByteArray应用到异步程序

# 第五章 深入了解TCP，解决暗藏问题

1. 从TCP到铜线：应用层、传输层、网络层、网络接口
2. 数据传输流程：TCP连接的建立、TCP的数据传输、TCP连接的终止
3. 常用TCP参数：ReceiveBufferSize、SendBufferSize、 NoDelay、TTL、ReuseAddress、LingerState
4. Close的恰当时机
5. 异常处理
6. 心跳机制

# 第六章 通用客户端网络模块

1. 网络模块设计

   对外接口

   内部设计

2. 网络事件

   事件类型

   监听列表

   分发事件

3. 连接服务端

   Connect

   ConnectCallback

   测试程序

4. 关闭连接

   isClosing

   Close

   测试

5. Json协议

   为什么会有协议类

   使用JsonUtility

   协议格式

   协议文件

   协议体的编码解码

   协议名的编码解码

6. 发送数据

   Send

   SendCallback

   测试

7. 消息事件

8. 接收数据

   新的成员

   ConnectCallback

   ReceiveCallback

   OnReceiveData

   Update

   测试

9. 心跳机制

   PING和PONG协议

   成员变量

   发送PING协议

   监听PONG协议

   测试

10. Protobuf协议

    什么是Protobuf

    编写proto文件

    生成协议类

    导入protobuf-net.dll

    编码解码

# 第七章  通用服务端框架

1. 服务端架构

   总体架构

   模块划分

   游戏流程

2. Json编码解码

   添加协议文件

   引用System.web.Extensions

   修改MsgBase类

   测试

3. 网络模块

   整体结构

   ClientState

   开启监听和多路复用

   处理监听消息

   处理客户端消息

   关闭连接

   处理协议

   Time

   发送协议

   测试

4. 心跳机制

   lastPingTime

   时间戳

   回应MsgPing协议

   超时处理

   测试程序

5. 玩家的数据结构

   完整的ClientState

   PlayerData

   Player

   PlayerManager

6. 配置MySQL数据库

   安装并启动MySQL数据库

   安装Navicat for MySQL

   配置数据表

   安装connector

   MySQL基础知识

7. 数据库模块

   连接数据库

   防止SQL注入

   IsAccountExist

   Register

   CreatePlayer

   CheckPassword

   GetPlayerData

   UpdatePlayerData

8. 登录注册功能

   注册登录协议

   记事本协议

   注册功能

   登录功能

   退出功能

   获取文本功能

   保存文本功能

   客户端界面

   客户端监听

   客户端注册功能

   客户端登录功能

   客户端记事本功能

   测试

# 第八章 完整大项目《坦克大战》

1. 《坦克大战》游戏功能

    登录注册

   房间系统

   战斗系统

2. 坦克模型

   导入模型

   模型结构

3. 资源管理器

   设计构想

   代码实现

   测试

4. 坦克类

   设计构想

   代码实现

   测试

5. 行走控制

   速度参数

   移动控制

   测试

   走在地形上

6. 坦克爬坡

   Unity的物理系统

   添加物理组件

   测试

7. 相机跟随

   功能需求

   数学原理

   编写代码

   测试

8. 旋转炮塔

   炮塔元素

   旋转控制

   测试

9. 发射炮

   制作炮弹预设

   制作爆炸效果

   炮弹组件

   坦克开炮

   测试

10. 摧毁敌人

    坦克的生命值

    焚烧特效

    坦克被击中处理

    炮弹的攻击处理

    测试

# 第九章 UI界面模块

1. 界面模块的设计

   简单的界面调用

   通用界面模块

2. 场景结构

3. 面板基类BasePanel

   设计要点

   代码实现

   知识点

4. 界面管理器PanelManager

   层级管理

   打开面板

   关闭面板

5. 登录面板LoginPanel

   导入资源

   UI组件

   制作面板预设

   登录面板类

   打开面板

   引用UI组件

   网络监听

   登录和注册按钮

   收到登录协议

6. 注册面板RegisterPanel

   制作面板预设

   注册面板类

   按钮事件

   收到注册协议

7. 提示面板TipPanel

   制作面板预设

   提示面板类

   测试面板

8. 游戏入口GameMain

   设计要点

   代码实现

   缓存用户名

9. 功能测试

   登录

   注册

   下线

# 第十章 游戏大厅和房间

1. 列表面板预设

   整体结构

   个人信息栏

   操作栏

   房间列表栏

   Scroll View

   列表项Room

2. 房间面板预设

   整体结构

   列表栏

   列表项Player

   控制栏

3. 协议设计

   查询战绩MsgGetAchieve协议

   查询房间列表MsgGetRoomList协议

   创建房间MsgCreateRoom协议

   进入房间MsgEnterRoom协议

   查询房间信息MsgGetRoomInfo协议

   退出房间MsgLeaveRoom协议

   开始战斗MsgStartBattle协议

4. 列表面板逻辑

   面板类

   获取部件

   网络监听

   刷新战绩

   刷新房间列表

   加入房间

   创建房间

   刷新按钮

5. 房间面板逻辑

   面板类

   获取部件

   网络监听

   刷新玩家列表

   退出房间

   开始战斗

6. 打开列表面板

7. 服务端玩家数据

   存储数据

   临时数据

8. 服务端房间类

   管理器和房间类的关系

   房间类的设计要点

   添加玩家

   选择阵营

   删除玩家

   选择新房主

   广播消息

    生成房间信息

9. 服务端房间管理器

   数据结构

   获取房间

   添加房间

   删除房间

   生成列表信息

10. 服务端消息处理

    查询战绩MsgGetAchieve

    查询房间列表MsgGetRoomList

    创建房间MsgCreateRoom

    进入房间MsgEnterRoom

    查询房间信息MsgGetRoomInfo

    离开房间MsgLeaveRoom

11. 玩家事件处理

12. 测试

# 第十一章 战斗和胜负判定

1. 协议设计

   进入战斗MsgEnterBattle

   战斗结果MsgBattleResult

   退出战斗MsgLeaveBattle

2. 坦克

   不同阵营的坦克预设

   战斗模块

   同步坦克SyncTank

   坦克的属性

3. 战斗管理器

   设计要点

   管理器类

   坦克管理

   重置战场

   开始战斗

   产生坦克

   战斗结束

   玩家离开

4. 战斗结果面板

   面板预设

   面板逻辑

5. 服务端开启战斗

   能否开始战斗

   定义出生点

   坦克信息

   开启战斗

   消息处理

6. 服务端胜负判断

   是否死亡

   胜负决断函数

   定时器

   Room::Update

7. 服务端断线处理

8. 测试

   进入战场

   离开战场

# 第十二章 同步战斗信息

1. 同步理论

   同步的过程

   同步的难题

2. 状态同步

   直接状态同步

   跟随算法

   预测算法

3. 帧同步

   指令同步

   从Update说起

   什么是同步帧

   指令

   指令的执行

4. 协议设计

   位置同步MsgSyncTank

   开火MsgFire

   击中MsgHit

5. 发送同步信息

   发送位置信息

   发送开火信息

   发送击中信息

6. 处理同步信息

   协议监听

   OnMsgSyncTank

   OnMsgFire

   OnMsgHit

7. 同步坦克SyncTank

   预测算法的成员变量

   移动到预测位置

   初始化

   更新预测位置

   炮弹同步

8. 服务端消息处理

   位置同步MsgSyncTank

   开火MsgFire

   击中MsgHit

   调试

9. 完善细节

   滚动的轮子和履带

   灵活操作

   准心

   自动瞄准

   界面和场景优化

   战斗面板

   击杀提示
