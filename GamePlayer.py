# coding: utf-8
import sys
import time
import cv2
import numpy as np
from BrainDQN_mx import BrainDQN

from GrabReader import *

label = "FlappyBird"

# preprocess raw image to 80*80 gray image
def preprocess(observation):
    observation = cv2.cvtColor(cv2.resize(observation, (80, 80)), cv2.COLOR_BGR2GRAY)
    ret, observation = cv2.threshold(observation,1,255,cv2.THRESH_BINARY)
    return np.reshape(observation,(80,80,1))

def play():
    # Step 1: init BrainDQN
    actions = 2
    if len(sys.argv) > 1: 
        brain = BrainDQN(actions, 'saved_networks/network-dqn_mx%04s.params'%
                sys.argv[1])
    else:
        brain = BrainDQN(actions)
    # Step 2: init Flappy Bird Game
    game = GrabReader(label)
    action0 = np.array([0, 1])
    ob, rew, ter = game.state(action0)

    ob = cv2.cvtColor(cv2.resize(ob, (80, 80)), cv2.COLOR_BGR2GRAY)
    ret, ob = cv2.threshold(ob,1,255,cv2.THRESH_BINARY)
    brain.setInitState(ob)

    c = 0
    tc = 0
    t = []
    old = False
    while True:
        action = brain.getAction()
        if old:
            ob, rew, ter = game.state(action)
            ob = cv2.cvtColor(cv2.resize(ob, (80, 80)), cv2.COLOR_BGR2GRAY)
            ret, ob = cv2.threshold(ob,1,255,cv2.THRESH_BINARY)
            brain.setInitState(ob)
            old = False
        else:
            print int(action[1]),
            ob, rew, ter = game.state(action)
            print rew, ter,
            sys.stdout.flush()
            ob = preprocess(ob)
            brain.setPerception(ob, action, rew, ter)
            old = ter
        

if __name__ == "__main__":
    import sys
    play()
