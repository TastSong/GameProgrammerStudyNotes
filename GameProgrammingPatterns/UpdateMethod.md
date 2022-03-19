## 更新方法

[代码示例](.\Assets\SequencingPatterns\UpdateMethod)	

### 定义

* 通过每次处理一帧的行为模拟一系列独立对象；

### 场景

- 你的游戏有很多对象或系统需要同时运行。
- 每个对象的行为都与其他的大部分独立。
- 对象需要跟着时间进行模拟。

### 案例

[对象的更新行为](./Assets/SequencingPatterns/UpdateMethod)

### 实现方式

* **游戏世界**管理**对象集合**。 

* 每个对象实现一个**更新方法**模拟对象在**一帧**内的行为。

* 每一帧，游戏循环更新集合中的每一个对象。

### 优缺点

**优点**

* 对象行为独立于游戏世界

**缺点**

* 增加系统复杂度

### 与其他设计模式的关系

- 这个模式，以及**游戏循环**模式和**组件模式**，是构建游戏引擎核心的三位一体。
- 当你关注在每帧中更新实体或组件的缓存性能时，**数据局部性模式**可以让它跑到更快。
- [Unity](http://unity3d.com/)框架在多个类中使用了这个模式，包括 [`MonoBehaviour`](http://docs.unity3d.com/Documentation/ScriptReference/MonoBehaviour.Update.html)。