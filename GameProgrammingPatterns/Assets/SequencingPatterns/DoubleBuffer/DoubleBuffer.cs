using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class DoubleBuffer : MonoBehaviour {
    private Framebuffer temp = new Framebuffer();
    private Framebuffer current = new Framebuffer();
    private Framebuffer next = new Framebuffer();

    private void Start() {
        Draw();

        for (int i = 0; i < current.pixels.Length; i++) {
            Debug.Log(current.pixels[i]);
        }
    }

    private void Draw() {
        next.Clear();
        next.Draw(1, 1);
        next.Draw(4, 1);
        next.Draw(1, 3);
        next.Draw(2, 4);
        next.Draw(3, 4);
        next.Draw(4, 3);
        Swap();
    }

    private void Swap() {
        temp = current;
        current = next;
        next = temp;
    }
}

class Framebuffer {
    private const int WIDTH = 6;
    private const int HEIGHT = 6;

    public Color[] pixels = new Color[WIDTH * HEIGHT];

    public Framebuffer() {
        Clear();
    }

    public void Clear() {
        for (int i = 0; i < WIDTH * HEIGHT; i++) {
            pixels[i] = Color.white;
        }
    }

    public void Draw(int x, int y) {
        pixels[(WIDTH * y) + x] = Color.black;
    }

    public Color[] GetPixels() {
        return pixels;
    }
}
