## 数据局部性

[代码示例](.\Assets\OptimizationPatterns\DataLocality)	

### 定义

合理组织数据，充分使用CPU的缓存来加速内存读取

### 场景

1. 性能问题确实由缓存不命中引起

### 案例

[更新大量相同组件](./Assets/OptimizationPatterns/DataLocality)

### 实现方式

* 现代的CPU有**缓存来加速内存读取**。

* 它可以**更快地读取最近访问过的内存的毗邻内存**。 

* 通过**提高内存局部性**来提高性能——保证数据**以处理顺序排列在连续内存上**。

### 优缺点

**优点**

1. 提高缓存利用率
2. 加快数据读写速度

**缺点**

* 系统更加复杂，更加缺乏灵活性

### 与其他设计模式的关系

- 这一模式几乎完全得益于同类对象的连续存储数组。 随着时间的推移，你也许需要向那个数组增加或删除对象。 **对象池模式**正是关于这一点。
- 这一章大部分围绕着**组件模式**。 这种模式的数据结构绝对是为缓存优化的最常见例子。事实上，使用组件模式让这种优化变得容易了。 由于实体是按“领域”（AI，物理，等等）更新的，将它们划出去变成组件，更容易将它们保存为对缓存友好的合适大小。但是这不意味你*只能*为组件使用这个模式！ 任何需要接触很多数据的关键代码，考虑数据局部性都是很重要的。