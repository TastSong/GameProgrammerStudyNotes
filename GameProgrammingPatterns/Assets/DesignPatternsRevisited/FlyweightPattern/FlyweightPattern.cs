using UnityEngine;
using System.Collections;
using System.Collections.Generic;

namespace FlyweightPattern
{
    public class FlyweightPattern : MonoBehaviour
    {
        void Start()
        {
            string document = "AAZZBBZB";
            char[] chars = document.ToCharArray();

            CharacterFactory factory = new CharacterFactory();

            // 外在状态
            int pointSize = 10;

            foreach (char c in chars)
            {
                pointSize++;
                Character character = factory.GetCharacter(c);
                character.Display(pointSize);
            }
        }
    }

    class CharacterFactory
    {
        private Dictionary<char, Character> _characters =
          new Dictionary<char, Character>();

        public Character GetCharacter(char key)
        {
            Character character = null;
            if (_characters.ContainsKey(key))
            {
                character = _characters[key];
            }
            else
            {
                switch (key)
                {
                    case 'A': character = new CharacterA(); break;
                    case 'B': character = new CharacterB(); break;
                    //...
                    case 'Z': character = new CharacterZ(); break;
                }
                _characters.Add(key, character);
            }
            return character;
        }
    }

    // Character类型所有的数据(外在 + 内在)
    abstract class Character
    {
        protected char symbol;
        protected int width;
        protected int height;
        protected int ascent;
        protected int descent;
        protected int pointSize;

        public abstract void Display(int pointSize);
    }

    class CharacterA : Character
    {
        public CharacterA()
        {
            // CharacterA 共享的类型
            this.symbol = 'A';
            this.height = 100;
            this.width = 120;
            this.ascent = 70;
            this.descent = 0;
        }

        public override void Display(int pointSize)
        {
            this.pointSize = pointSize;
            Debug.Log(this.symbol +
              " (pointsize " + this.pointSize + ")");
        }
    }

    class CharacterB : Character
    {
        public CharacterB()
        {
            // CharacterB 共享的类型
            this.symbol = 'B';
            this.height = 100;
            this.width = 140;
            this.ascent = 72;
            this.descent = 0;
        }

        public override void Display(int pointSize)
        {
            this.pointSize = pointSize;
            Debug.Log(this.symbol +
              " (pointsize " + this.pointSize + ")");
        }

    }

    // ... C, D, E, etc.

    class CharacterZ : Character
    {
        public CharacterZ()
        {
            // CharacterZ 共享的类型
            this.symbol = 'Z';
            this.height = 100;
            this.width = 100;
            this.ascent = 68;
            this.descent = 0;
        }

        public override void Display(int pointSize)
        {
            this.pointSize = pointSize;
            Debug.Log(this.symbol + " (pointsize " + this.pointSize + ")");
        }
    }
}