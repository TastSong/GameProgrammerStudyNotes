using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class UpdateMethod : MonoBehaviour {
    private World world = new World();


    private void Start() {
        Debug.LogError("完成对更新方法的构建");
    }

    private void Update() {
        //world.GameLoop();
    }
}

class Entity {
    public Entity() {
        x_ = 0;
        y_ = 0;
    }

    public void Update() { }

    public double x() { return x_; }
    public double y() { return y_; }

    public void SetX(double x) { x_ = x; }
    public void SetY(double y) { y_ = y; }

    private double x_;
    private double y_;
}

class World {

    public void GameLoop() {
        for (int i = 0; i < entities.Count; i++) {
            entities[i].Update();
        }
    }

    private List<Entity> entities = new List<Entity>();
};