# -*- coding: utf-8 -*-
"""
ADITYA GUNE
Infinite Horizon Value Iteration
"""
import numpy as np
from mdp import MDP
import sys
from valueiter import *
from parking import Parking_MDP
from simulator import Simulator
from qlearning import Qlearning
from policygen import *
#Set up environment
beta = 0.9
epsilon = 0.00001
numrows = 11

"""
SETTINGS:
createMDP = 1 FOR CREATING A PARKING MDP
valiter = 1 FOR VALUE ITERATION
sim = 1 FOR RUNNING A SIMULATION
qlearn = 1 FOR QLEARNING
"""
createMDP = 1
valiter = 0
sim = 1
qlearn = 0

#Write an MDP to a file
if createMDP == 1:
    mdp1 = Parking_MDP(rows=10, R_handicap=-100, R_coll=-10000)
    parkingfile = open('ParkingMDP1.txt', 'w')
    (states1, actions1, T1, R1) = mdp1.getMDP()
    mdp1.writeMDP(parkingfile)
    parkingfile.close()
    mdp2 = Parking_MDP(rows=11, R_handicap=-100, R_coll=-10000)
    parkingfile = open('ParkingMDP2.txt', 'w')
    (states2, actions2, T2, R2) = mdp2.getMDP()
    mdp2.writeMDP(parkingfile)
    parkingfile.close()

if sim == 1:
    
    if mdp1 is None or mdp2 is None:
        print("Please run again with section set to 1")
    else:
        
        #option=1 for random,
        #option=2 for avoid collisions,
        #option=3 for greedy 
        policy1 = generate_policy(numrows, option=1)
        
    
        simulator = Simulator((states1, actions1, R1, T1))
        (R_tot, actions_taken, states_visited) = simulator.runPolicy(policy1)
        print("Reward: ", R_tot)
        print('Actions Taken: \n', actions_taken)
        print('States Visited: \n', states_visited)

R_avg = []

if qlearn == 1:
    for eps in [.1, .25, .33, .5, .66, .75, .99]:
        ql = Qlearning((states, actions, R, T), epsilon = eps)
        for trial in range(100):
            ql.learn()
        ra = 0
        for trial in range(1000):
            (R_tot, actions_taken, states_visited) = ql.run_iteration()
            ra =+ R_tot
        ra /= 1000
        print(ra)



if valiter == 1:
    #Read in an MDP from a file    
    k = mdp.read_MDP_from_file('ParkingMDP1.txt')    
    (states, actions, R, T) = mdp.process_MDP(k)
    t = open('output.txt', 'w+')
    (V, pi) = value_iter(states, actions, R, T, t, beta, epsilon)
    print("Optimal Value Function:")
    t.write("Optimal Value Function:\n")
    for x in V:
        print(x)
        t.write(str(x)+'\n')
    print
    t.write('\n')
    print("Optimal Policy:")
    t.write("Optimal Policy:\n")
    for x in pi:
        print(x)
        t.write(str(x)+'\n')
    t.close()
