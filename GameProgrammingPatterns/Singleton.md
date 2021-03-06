## 单例模式

[代码示例](.\Assets\DesignPatternsRevisited\SingletonPattern)

### 定义

确保一个类只有一个实例，并为其提供一个全局访问入口

### 场景

1. 程序中的某个类对于所有客户端只有一个可用的实例
2. 你需要更加严格地控制全局变量

### 案例

[单例](./Assets/DesignPatternsRevisited/SingletonPattern)

### 实现方式

1. 在类中添加一个私有静态成员变量用于保存单例实例。
2. 声明一个公有静态构建方法用于获取单例实例。
3. 在静态方法中实现"延迟初始化"。 该方法会在首次被调用时创建一个新对象， 并将其存储在静态成员变量中。 此后该方法每次被调用时都返回该实例。
4. 将类的构造函数设为私有。 类的静态方法仍能调用构造函数， 但是其他对象不能调用。
5. 检查客户端代码， 将对单例的构造函数的调用替换为对其静态构建方法的调用。

### 优缺点

**优点**

-  你可以保证一个类只有一个实例。
-  你获得了一个指向该实例的全局访问节点。
-  仅在首次请求单例对象时对其进行初始化。

**缺点**

-  违反了_单一职责原则_。 该模式同时解决了两个问题*(在一个方法中进行了创建类和提供类对象的操作)*。
-  单例模式可能掩盖不良设计， 比如程序各组件之间相互了解过多等。
-  该模式在多线程环境下需要进行特殊处理， 避免多个线程多次创建单例对象。
-  单例的客户端代码单元测试可能会比较困难， 因为许多测试框架以基于继承的方式创建模拟对象。 由于单例类的构造函数是私有的， 而且绝大部分语言无法重写静态方法， 所以你需要想出仔细考虑模拟单例的方法。 要么干脆不编写测试代码， 或者不使用单例模式。

### 与其他设计模式的关系

- **外观模式** *(GOF)*类通常可以转换为单例模式类， 因为在大部分情况下一个**外观对象** *(GOF)*就足够了。
- 如果你能将对象的所有共享状态简化为一个享元对象， 那么**享元模式**就和单例类似了。 但这两个模式有两个根本性的不同。
  1. 只会有一个单例实体， 但是*享元*类可以有多个实体， 各实体的内在状态也可以不同。
  2. *单例*对象可以是可变的。 享元对象是不可变的。
- **抽象工厂模式** *(GOF)*、 **生成器模式** *(GOF)*和**原型模式**都可以用单例来实现。