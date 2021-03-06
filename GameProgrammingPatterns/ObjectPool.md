## 对象池模式

[代码示例](.\Assets\OptimizationPatterns\ObjectPool)	

### 定义

放弃单独地分配和释放对象，从固定的池中重用对象，以提高性能和内存使用率

### 场景

- 需要频繁创建和销毁对象。
- 对象大小相仿。
- 在堆上进行对象内存分配十分缓慢或者会导致内存碎片。
- 每个对象都封装了像数据库或者网络连接这样很昂贵又可以重用的资源。

### 案例

[对象池](./Assets/OptimizationPatterns/ObjectPool)

### 实现方式

* 定义一个**池**对象，其包含了一组**可重用对象**。
* 其中每个可重用对象都支持**查询“使用中”状态**，说明它是不是“正在使用”。
* 池被初始化时，它就创建了整个对象集合（通常使用一次连续的分配），然后初始化所有对象到“不在使用中”状态。
* 当你需要新对象，向池子要一个。 
* 它找到一个可用对象，初始化为“使用中”然后返回。
* 当对象不再被需要，它被设置回“不在使用中”。 
* 通过这种方式，可以轻易地创建和销毁对象而不必分配内存或其他资源。

### 优缺点

以空间换时间

### 与其他设计模式的关系

- 这看上去很像是**享元模式**。 两者都控制了一系列可重用的对象。不同在于“重用”的含义。 享元对象分享实例间*同时*拥有的相同部分。享元模式在不同上下文中使用相同对象避免了*重复*内存使用。

  对象池中的对象也被重用了，但是是在不同的时间点上被重用的。 “重用”在对象池中意味着对象在原先的对象用完*之后*分配内存。 对象池没有期待对象会在它的生命周期中分享什么。

- 将内存中同样类型的对象进行整合，能确保在遍历对象时CPU缓存总是满的。 **数据局部性模式**介绍了这一点。