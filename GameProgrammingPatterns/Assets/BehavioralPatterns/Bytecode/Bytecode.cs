using System.Collections;
using System.Collections.Generic;
using UnityEngine;

enum Instruction {
    INST_SET_HEALTH = 0x00,
    INST_SET_WISDOM = 0x01,
    INST_SET_AGILITY = 0x02,
    INST_PLAY_SOUND = 0x03,
    INST_SPAWN_PARTICLES = 0x04
};

public class Bytecode : MonoBehaviour{
    void Interpret(Instruction[] instructions) {
        for (int i = 0; i < instructions.Length; i++) {
            Instruction instruction = instructions[i];
            switch (instruction) {
                case Instruction.INST_SET_HEALTH:
                    //setHealth(0, 100);
                    break;

                case Instruction.INST_SET_WISDOM:
                    //setWisdom(0, 100);
                    break;

                case Instruction.INST_SET_AGILITY:
                    //setAgility(0, 100);
                    break;

                case Instruction.INST_PLAY_SOUND:
                    //playSound(SOUND_BANG);
                    break;

                case Instruction.INST_SPAWN_PARTICLES:
                    //spawnParticles(PARTICLE_FLAME);
                    break;
            }
        }
    }
}
