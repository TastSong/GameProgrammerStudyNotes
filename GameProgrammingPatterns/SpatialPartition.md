## 空间分区

### 定义

将对象根据它们的位置存储在数据结构中，来高效地定位对象

### 场景

* 这是存储活跃的、移动的游戏对象的常用模式，也可用于静态美术和世界地理。 复杂的游戏中，不同的内容有不同的空间分区。

* 这个模式的基本要求是一系列有位置的对象，而你做了太多的通过位置寻找对象的查询，导致性能下降。

### 案例

### 实现方式

* 对于一系列**对象**，每个对象都有**空间上的位置**。 
* 将它们存储在根据位置组织对象的**空间数据结构**中，让你**有效查询在某处或者某处附近的对象**。 
* 当对象的位置改变时，**更新空间数据结构**，这样它可以继续找到对象。

### 优缺点

以空间换时间

### 与其他设计模式的关系