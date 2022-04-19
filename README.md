# Game Programmer Study Notes 游戏编程学习笔记 

# Game Programming Patterns 游戏编程模式

![](./Pictures/GameProgrammingPatterns.png)

[代码示例](./GameProgrammingPatterns)	

- 重访设计模式
  - [命令模式](./GameProgrammingPatterns/Command.md)：*将“请求〞封装成对象，以便使用不同的清求，队列或者日志来参数化其他对象，同时支持可撤消的操作*
  - [享元模式](./GameProgrammingPatterns/Flyweight.md)：*以共享的方式高效地支持大量的细粒度的对象。通过复用内存中已存在的对象，降低系络创建对象实例的性能消耗*
  - [观察者模式](./GameProgrammingPatterns/Observer.md)：*定义对象间的一种一对多的依赖关系，当一个对象的状态发生改变时，所有依赖于它的对象都得到通知并被白动更新*
  - [原型模式](./GameProgrammingPatterns/Prototype.md)：*用原型实例指定创建对象的种类，并且通过拷贝这些原型创建新的对象*
  - [单例模式](./GameProgrammingPatterns/Singleton.md)：*保证一个类只有一个实例，并且提供了访问该实例的全局访问点*
  - [状态模式](./GameProgrammingPatterns/State.md)：*允许对象在当内部状态改交时改交其行为，就好像此对象改变了自己的类一样*
- 序列模式
  - [双缓冲模式](./GameProgrammingPatterns/DoubleBuffer.md)：*使用序列操作来模拟瞬间或者同时发生的事情*
  - [游戏循环](./GameProgrammingPatterns/Assets/SequencingPatterns/GameLoop)：*实现游戏运行过程中对用户输入处理和时间处理的解耦*
  - [更新方法](./GameProgrammingPatterns/UpdateMethod.md)：*通过每次处理一帧的行为来模拟一系列独立对象*
- 行为模式
  - [字节码](./GameProgrammingPatterns/Bytecode.md)：*将行为编码为虚拟机器上的指令，来赋予其数据的灵活性。从而让数据易于修改，易手加载，并与其他可执行部分相隔离*
  - [子类沙箱](./GameProgrammingPatterns/SubclassSandbox.md)：*用一系列由基类提供的操作定义子类中的行为*
  - [类型对象](./GameProgrammingPatterns/TypeObject.md)：*创造一个类A来允许灵活的创造新的类，而类A的每个实例都代表了不同类型的对象*
- 解耦模式
  - [组件模式](./GameProgrammingPatterns/Component.md)：*允许单一的实体跨越多个领域，无需这些领域彼此耦合*
  - [事件队列](./GameProgrammingPatterns/EventQueue.md)：*事件队列模式，对消息或事件的发送与处理进行时间上的解耦*
  - [服务定位器](./GameProgrammingPatterns/ServiceLocator.md)：*提供服务的全局接入点，而不心让用户和实现它的具体类解耦*
- 优化模式
  - [数据局部性](./GameProgrammingPatterns/DataLocality.md)：*合理组织数据，充分使用CPU的级存来加速内行读取*
  - [脏标识模式](./GameProgrammingPatterns/DirtyFlag.md)：*将工作延期至需要其结果时才去执行，以避免不心要的工作*
  - [对象池模式](./GameProgrammingPatterns/ObjectPool.md)：*放弃单独地分配和释放对象，从固定的池中重用对象，以提高性能和内存使用率*
  - [空间分区](./GameProgrammingPatterns/SpatialPartition.md)：*将对条存储在基于位置组织的数据结构中，来有效的定位对象*

**重访设计模式的六种设计方法为经典23种设计模式的之六，这六种设计模式也是游戏中常用的设计模式；序列模式、行为模式和优化模式适用与游戏引擎设计；解耦模式适用于游戏UI部分的设计-------自定义组件和消息机制的设计**

# QFramework Unity框架

![](./Pictures/QFormwork.png)

[详细文档](./QFramework/README.md)

- 架构目的：使用框架的目的与意义
- 设计原则：SOLID设计模式的六大原则
- 总体架构：框架的分层以及层级之间的规则
- 代码示例：如何使用此框架
- 实现细节：框架实现过程中的技术要点

**此框架相较于流行的框架[ET](https://github.com/egametang/ET)、[JEngine](https://github.com/JasonXuDeveloper/JEngine)等框架，QFormwork更专注于逻辑层的架构，在工具层实现组件化做到即用即安装，更佳纯粹；此教程在Unity学堂可以学习，重点不应该放在框架的使用，而是放在框架的搭建过程**

# Unity 3D高级编程

![](./Pictures/ProfessionalNotes.png)

* [第一章 架构](./ProfessionalUnity3D/第一章架构.md)：架构的意义、架构的原理以及如何实现架构
* [第二章 C#技术要点](./ProfessionalUnity3D/第二章技术要点.md)：C# 技术的基础知识
* [第三章 数据表与程序](./ProfessionalUnity3D/第三章数据表.md)：针对客户端中的表格数据、程序的协作与应用
* [第四章 用户界面](./ProfessionalUnity3D/第四章用户界面.md)：用户界面（UI）的工作原理与优化手段
* [第五章 3D模型与动画](./ProfessionalUnity3D/第五章3D模型与动画.md)：3D 模型的原理、动画的原理以及两者的优化
* [第六章 网络通信](./ProfessionalUnity3D/第六章网络层.md)：网络层的业务与底层原理
* [第七章 游戏中的AI](./ProfessionalUnity3D/第七章游戏中的AI.md) : 各种 AI 类型
* [第八章 地图与寻路](./ProfessionalUnity3D/第八章地图与寻路.md) ：场景构建与优化、地图构建以及寻路算法优化
* [第九章 渲染管线与图形学](./ProfessionalUnity3D/第九章渲染管线与图形学.md) ：图形数学、图形学常用算法、渲染管线的相关知识
* [第十章 渲染原理与知识](./ProfessionalUnity3D/第十章渲染原理与知识.md) ：客户端各类渲染技术的渲染原理

**整本书讲解的为Unity的底层原理，核心思想是优化游戏性能，主要的围绕提高游戏运行速度与降低内存消耗展开，优化的本质其实就是减少GC和降低drewcall，进而分别从C#技术要点、UI、模型等模块进行讲解**

# Clean Code 

![](./Pictures/CleanCode.png)

[详细文档](./CleanCode/CleanCode.md)

* 目的
* 命名法则
* 函数
* 注释
* 格式准则
* 对象和数据结构
* 错误处理
* 边界
* 单元测试
* 类

**本书主要讲解功能实现的时候代码的规范，如果你阅读的时候发现你都做到了，那你写的代码一定十分简洁，当然大多数的人应该或多或少都会有些点没有做到，那这就是你代码的提高点，此书可以多次阅读，每次尽可能都有一点改善就好，如果对书中的优化点你存在异议，请相信“Bob大叔”**

# 游戏感

![](./Pictures/GameFell.png)



[详细文档](./GameFell/GameFell.md)

* 游戏感的三大基础构件
  * 实时控制
  * 模拟空间
  * 润色 (Polish)
* 游戏感的体验
  * 操作的美感
  * 学习、练习和掌握一项技能的榆
  * 悦感
  * 感觉的延伸
  * 个体的延伸
  * 与游戏里一个独特的物理实体的
  * 交互感
* 创造游戏感
* 游戏感测量维度
  * 输入
  * 响应
  * 情景
  * 润色
  * 隐喻
  * 规则

**本书主要讲解游戏感的定义、游戏感的三大基础构件以及度量游戏感的六个维度，使得我们可以从数据上对游戏好坏进行评判，评判游戏变得可以量化**

# Java 游戏服务器架构实战

![](./Pictures/JavaGameServer.png)



[详细文档](./Java游戏服务器架构实战/README.md)

* 模块零概论
  * 第1章 游戏服务器架构总体设计
  * 第2章 服务器项目管理一Maven
  * 第3章 数据库选择与安装

* 模块二 游戏服务中心架构设计
  * 第4章 游戏服务中心开发
  * 第5章 Web服务器网关开发

* 模块三 游戏网关架构设计
  * 第6章 游戏服务器网关开发

* 模块四 业务服务架构设计
  * 第7章 游戏服务器网关与游戏业务服务数据通信
  * 第8章 游戏业务处理框架开发
  * 第9章 游戏用户数据管理

* 模块五 RPC通信架构设计
  * 第10章 RPC 通信设计与实现
  * 第11章 事件系统的设计与实现
  * 第12章 游戏服务器自动化测试

* 模块六 实例
  * 第13章 服务器开发实例一一世界聊天系统

**本书主要从游戏服务中心、游戏网关、RPC通信和业务服务四个模块，展开介绍游戏的短链接和长链接的网关设计、以及微服务通信以及业务服务设计实现，其中主要是用的框架为Spring Cloud**

# Unity 人工智能实战

![](./Pictures/UnityAI.png)

[详细文档](./UnityAI/README.md)

* 第1章 行为一一智能移动
* 第2章 导航
* 第3章 决策制定
* 第4章 新的NavMesh API
* 第5章 协作和战术
* 第6章 agent感知
* 第7章 棋类游戏和应用的搜索AI
* 第8章 机器学习
* 第9章 程序化内容生成
* 第10章 其他

**本书主要讲解如何实现各类游戏AI，在实现Agent寻路时重点讲解了NavMesh使用，并在最后两章讲解了主流的几个智能体的实现**

# Unity引擎HDRP高清渲染管线实战

![](./Pictures/UnityHDRP.png)



# Unity网络游戏实战

![](./Pictures/UnityNetwork.png)

[详细文档](./UnityNetworkGame/README.md)

* 第一章 网络游戏的开端
* 第二章 分身有术：异步和安路复用
* 第三章 文践出真知：大乱斗游戏
* 第四章 正砷收发数据流
* 第五章 深入了解TCP，解决暗藏问题
* 第六章 通用客户端网络模块
* 第七章 通用服务端框架
* 第八章 完整大项目《坦克克大战》
* 第九章 UI界面模块
* 第十章 游戏大厅和房间
* 第十一章 战斗和胜负判定
* 第十二章 同步战斗信息

**第一部分“扎基础”主要介绍TCP网络游戏开发的必备知识，包括TCP异步连接、多路复用的处理，以及怎样处理粘包分包、怎样发送完整的网络数据、怎样设置正确的网络参数。第3章介绍了一款简单 网络游戏开发的全过程，在后续章节中会逐步完善这个游戏。** 

**第二部分“搭框架”主要介绍商业级客户端网络框架的实现方 法。这套框架具有较高的通用性，解决了网络游戏开发中常遇到的问 题，且达到极致的性能要求，可以运用在多款游戏上。书中还介绍了 一套单进程服务端框架的实现，服务端框架使用select多路复用，做到底层与逻辑分离，设有消息分发、事件处理等模块。 第**

**三部分“做游戏”通过一个完整的实例讲解网络游戏的设计思路，包括游戏实体的类设计、怎样组织代码、怎样实现游戏大厅（房间系统）、怎样实现角色的同步。这一部分会使用第二部分搭好的框架，一步步地做出完整的游戏项目。**

# Unity Shader入门精要

![](./Pictures/UnityShader.png)



# Unity VR虚拟现实完全自学教程

![](./Pictures/UnityVR.png)













 



