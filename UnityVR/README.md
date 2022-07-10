# Unity VR虚拟现实完全自学教程

# 第 1 章 VR 行业概述

VR 行业目前处于发展早期阶段，在大众市场普及方面面临着挑战，行业生态尚需完善，硬件先发展还是内容先丰富，貌似是一个悖论，但我们应该看到，硬件技术正在飞速发展，硬件产业链上的厂家也在还渐提高产品性能，同时深度学习、SG 等技术也逐渐显露，随着Unity 等内容制作引擎的版本升级，使得开发者制作高品质 VR 应用程序的门槛也越来越低。我们有理由相信，VR 技术会在未来蓬勃发展。

# 第 2 章 Unity VR 概述

Unity 是当前业界领先的 VR/AR 内容制作工具，是大多数 VR/AR 创作者首选的开发工具，世界上超过 60%的 VR/AR 内容是用 Unity 制作完成的。Unity 为制作优质的 VR 应用程序提供了一系列先进的解决方案，无论是 VR、AR 还是MR，都可以依靠 Unity 高度优化的渲染流水线以及编辑器的快速迭代功能，使需求得以完美实现。基于跨平台的优势，Unity 支持市面上绝大多数的硬件平台，原生支持 Oculus Rift、 Steam VR/VIVE、 Play Station VR、Gear VR、Microsoft HoloLens 以及Google 的 Daydream View。

# 第 3 章 当前主流 VR 硬件

HTC VIVE （HTC 使用Value公司的Steam VR技术）、Oculus Rift（被Facebook收购前期版本使用SteamVR）、Gear VR（三星使用Oculus技术）、Cardboard（谷歌的开源初级VR方案）、Daydream 平台（第二代谷歌VR解决方案）

# 第 4 章 VR 应用程序开发工作流程

资源准备->模型优化及重拓扑->展 UV 的过程->材质贴图制作->将资源导入 Unity->导入开发工具包->场景搭建->设置光照环境->交互开发->测试优化->发布应用程序

# 第 5 章 VR 交互设计原则

1. 设计必要的新手引导
2. 使用十字线（准星）
3. 避免界面深度引起的疲劳感
4. 使用恒定的速度 
5. 保持用户在地面上
6. 保持头部的跟踪
7. 用光来引导用户的注意力
8. 借助比例
9. 使用空间音频
10. 充分使用反馈

# 第 6 章 HTC VIVE 硬件

1. HTC VIVE 定位原理

   HTC VIVE 基于 Valve 公司的 SteamVR 技术，SteamVR 定位由 Valve 自主研发，SteamVR定位器（即 Lighthouse）使用多重同步脉沖与激光线扫描房间，覆盖大约5 米的范围。SteamVR使用简单的三角学找到每个感应器的精确到毫米以内的位置，借助组合多个感应器 2个定位器，以及添加高速IMU（惯性测量单元）。SteamVR 也以 1000Hz 的刷新率计算被定位物品的方向、速度、角速度。

2. Inside-Out 与 Out-Inside 位置跟踪技

   VR技术中比较重要的技术是获取到头显、手柄等设备的位置信息，即位置追踪技术，目前存在两种实现方式，分别为由内而外的位置追踪(Inside-Out）和由外而内(Outside-In）的位置追踪。

   * Outside-In 跟踪技术

     Ouside-In跟踪技术借助外部设备 （比如 HITC VIVE 中的 Liehthouse 基站），实现对头显、控制器等设备在场景中的位置跟踪。外部设各通常为摄像机、红外传感器等，它们被放在静止位置，朝向被跟踪物体。在外部设备所能感应的范国内，系统获得被跟踪设备的位置和朝向信息。使用这种跟踪技术的 VR 平台以 Oculus Rifi、 HTC VIVE、PS VR为代表，通过外部跟踪器实现硬件设备的位置追踪，其优势是跟踪精度较高，适合小范围跟踪：其劣势是需要使用外部设备进行跟踪，用户移动范围有限。

   * Inside-Out 跟踪技术

     Inside-Out 位置跟踪技术采用额外摄像机，通过光学或者计算机视觉的方法实现空问定位功能，可以实现较大空间内的定位。该定位技术中比较重要的是 SLAM (Simultaneous Localization and Mapping）算法，此算法也多应用在 AR 技术中。这种跟踪技术的优势是不受空间约束，能够显著提高 VR 设备的移动性，越来越被广泛应用在提供6自由度运动跟踪的 VR一体机中；其劣势是该技术受光照因素影响较大，在光照强烈的室外场景、光照较暗的室内场景，以及缺少足够特征(比如几乎没有任何特征的地面)的场景中，跟踪精度会降低，容易出现画面漂移的现象。

# 第 7 章 VR 中的 UI

一、将 UI 容器转换为世界空间坐标

1. 新建一个 Canvas 游戏对象，在其 Canvas 组件中，将Render Mode 属性修改为 World Space。
2. 此时 Canvas 便具有了世界空间坐标，Rect Trasform 组件为可修改状态，可以像3D物体一样在场景中设置位置、旋转、缩放等参数。我们一般需要根据 VR 场景的大小，修改Canvas 容器的外观，使其适应场景比例。有两种方式实现：一种方式是修改 RectTransform 组件的缩放 Scale 值，比如将其修改为 0.001;另外-一种方式是保持缩放不变，修改 Rect Transform 的Width 和 Height 属性。需要注意的是，对于修改比例的操作，尽量在 Canvas（即 UI 元素的容器）上完成，而不要修改容器的子物体。
3. 为了能够在 VR 场景中比较清晰地观看 UI 元素，需要修改 Canvas 容器上 Canvas Scaler组件的 Dynamic Pixels Per Unit 属性值，一般为 2~5 之间的数值。下图左右侧文字分别在不同的 Canvas 中，左侧文字是 Dynamic Pixels Per Unit 属性值为默认时的表现，右侧文字是该值为3时的表现。

二、VR 中的 UI 交互 

Unity 的 UI 系统主要由以下部分组成，它们互相配合，实现了从用户输入（例如点击、悬停等）到事件发送的过程。

* Event System：事件系统。
* Input Module： 输入模块。
* Raycaster：射线投射器。
* Graphic Components： 图形组件，如按钮、列表等。

不同的 VR 硬件平台和SDK，与UI交互的实现机制不同，但它们都基于 Unity Ur 的事什系统流程，或者继示站文介绍的组件，或者模找相关的事件，例如在 Oculus Utilities 中，使用 OVR Physics Raycaster 类通过集成Unity 的 Basc Raycaster 类来实现Physics Raycaster的角色。

# 第 9 章 SteamVR

一、 SteamVR

SteamVR 是由 Valve 公司推出的一套 VR 软硬件解决方案，由 Valve 提供软件支持和硬件标淮，授权技术给硬件生产伙伴，其中包括 HTC VIVE、OSVR、微软 Windows MR 等。我们谈到 SteamVR，在不同的情境下，所指代的对象不同。当运行一个 VR 程序时，需要打开 SteamVR。进行房型设置、硬件配对时，这里指的是 SteamVR Runtime (SteamVR 运行时）如果在使用 Unity 进行 VR 内容开发时，需要导入 SteamVR，这里所指的是 SteamVR Plugin。

二、 SteamVR Plugin 

SteamVR Plugin 是针对Unity 的SteamVR 开发工具包，以插件的形式存在，可以从 Unity Asset Store 中进行下载，导入到 Unity 项目中。该插件是开发基于 SteamVR 应用程序的必备工具，包括附带的交互开发工具 Interaction System,以及第三方开发的 VRTK，都是基于该工具包延伸而来的.

三、 InteractionSystem

InteractionSystem 脱胎于 The Lab，抽取了这个应用中关于交互的关键部分，包括一系列的脚本、预制体和一些游戏资源，InteractionSystem 内置于 SteamVR Unity Plugin 中，将 SteamvR Plugin 导入Unity 后，即可在SteamVR 目录下找到 InteractionSystem。

通过InteractionSystem可以快速实现传送、与物体的交互、UI 的交互等。

# 第 10 章 使用 VRTK 进行交互开发

## 10.1 VRTK 简介

### 10.1.1 什么是 VRTK

### 10.1.2 VRTK 能做什么

### 10.1.3 为什么选择 VRTK

### 10.1.4 未来版本

## 10.2 SteamVR Plugin、InteractionSystem 与 VRTK 的关系

## 10.3 配置 VRTK

### 10.3.1 一般配置过程

### 10.3.2 快速配置 VRTK

## 10.4 VRTK 中的指针

### 10.4.1 指针

### 10.4.2 指针渲染器 

## 10.5 在 VRTK 中实现传送

### 10.5.1 VRTK 中的传送类型

### 10.5.2 限定传送区域

### 10.5.3 在 VR 场景中实现传送 

## 10.6 使用 VRTK 实现与物体的交互

### 10.6.1 概述 

### 10.6.2 配置方法 

### 10.6.3 VRTK 的抓取机制

## 10.7 VRTK 中的控制器高亮和振动

### 10.7.1 控制器高亮

### 10.7.2 控制器振动

## 10.8 VRTK 中与 UI 的交互

## 10.9 实例：开枪射击效果

## 10.10 实例：攀爬效果

## 10.11 实例：实现释放自动吸附功能

# 第 11 章 将基于 PC 平台的应用移植到 VR 平台

## 11.1 项目移植分析

## 11.2 初始化 VR 交互

## 11.3 Player 的移植

## 11.4 设置道具为可交互对象

## 11.5 实现控制器与道具的交互逻辑

## 11.6 修改 UI 渲染模式为 World Space

## 11.7 玩家伤害闪屏效果

## 11.8 根据报错信息调整代码

## 11.9 游戏结束及重新开始

# 第 12 章 Leap Motion for VR

## 12.1 概述

## 12.2 硬件准备

## 12.3 软件环境

## 12.4 Leap Motion VR 初始开发环境

## 12.5 替换 Leap Motion 在 VR 环境中的手部模型

## 12.6 实现与 3D 物体的交互

## 12.7 实例：使用 Leap Motion 实现枪械的组装

# 第 13 章 VIVE Tracker 的使用

## 13.1 外观结构

## 13.2 使用场景

## 13.3 初次使用 Tracker 

## 13.4 使用 Tracker 作为控制器

## 13.5 使用 Tracker 与现实世界物体进行绑定

## 13.6 小结

# 第 14 章 Unity VR 游戏案例——《水果忍者 VR》原型开发

## 14.1 项目简介

## 14.2 初始化项目

## 14.3 配置武士刀

## 14.4 编写水果生成逻辑 

## 14.5 实现切割水果的效果

## 14.6 制作分数和游戏结束 UI

## 14.7 编写计分、计时和游戏结束等逻辑

# 第 15 章 Unity VR 案例—— Tilt Brush 原型开发

## 15.1 项目分析

## 15.2 初始化项目并编写脚本

## 15.3 实现修改笔刷颜色功能

## 15.4 扩展内容：将绘制交互修改为 VRTK 版本

## 15.5 异常处理

# 第16 章 Unity VR 性能优化工具和方法

# 16.1 Unity Profiler 

## 16.2 Memory Profiler

## 16.3 Frame Debugger

## 16.4 优化原则和措施

### 16.4.1 LOD 技术

### 16.4.2 较少 Draw Call 数量

### 16.4.3 使用单通道立体渲染

### 16.4.4 使用 The Lab Renderer

## 16.4.5 小结
