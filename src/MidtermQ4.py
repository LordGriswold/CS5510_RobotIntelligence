from typing import Dict
import gym
import numpy as np
import os
import random
import matplotlib.pyplot as plt
import collections
import matplotlib.animation as animation
from array2gif import  write_gif
import math

from cartpole import CartPoleEnv

GRAV_ACC = 9.8

def plot_environment(env, figsize=(5,4)):
    plt.figure(figsize=figsize)
    img = env.render()
    plt.imshow(img)
    plt.axis("off")
    return img

def test_policy(env, policy_func, n_scenario = 1000, max_actions = 500, verbose=False):
    final_rewards = []
    for episode in range(n_scenario):
        if verbose and episode % 50 == 0:
            print(episode)
        episode_rewards = 0
        obs, x = env.reset()  # reset to a random position
        if max_actions == None:
            while True:
                action = policy_func(obs)
                obs, reward, done, info, x = env.step(action)
                episode_rewards += reward
                if done:
                    break
        else:
            for step in range(max_actions):
                action = policy_func(obs)
                obs, reward, done, info, x = env.step(action)
                episode_rewards += reward
                if done:
                    break
        final_rewards.append(episode_rewards)
    return final_rewards

def plot_policy(final_rewards, policy_name:str=''):
    fig = plt.plot(range(len(final_rewards)), final_rewards)
    plt.grid()
    plt.title(policy_name + "\n Mean Reward {:.2f}, Min Reward {:.2f}".format(np.mean(final_rewards), np.min(final_rewards)))
    plt.ylabel('Cumulative Reward')
    plt.xlabel('Iteration')
    plt.ylim(0, max(final_rewards)*1.1)
    return fig

'''
Test the max angle (radians) the pole can fall before the cart cannot recover 
(solves part C)
Note that the length parameter actually represents half the length of the pole
'''
def testMaxTheta(env, start = 0.1, step = 0.1):
    curr_theta = start
    max_theta = curr_theta
    env.theta_threshold_radians = math.pi / 2
    env.reset()
    while True:
        env.reset()
        env.state = (0, 0, curr_theta, 0)
        env.steps_beyond_terminated = None
        for i in range(20):
            obs, reward, done, info, x = env.step(1)
        if obs[2] <= curr_theta and not done:
            # pole recovered a little or didn't go up
            max_theta = curr_theta
            curr_theta += step
        else:
            # pole continued to fall after applying a force
            return max_theta if not done else None

# Policies

def policy(obs):
    theta, omega = obs[2:4] # Get current theta and omega
    if abs(theta) < 0.03: # theta is very small
        return 0 if omega < 0 else 1 # move left if the angular acceleration is negative
    else:
        return 0 if theta < 0 else 1 # move left if the angle is negative

if __name__ == '__main__':
    env = CartPoleEnv()
    env.masscart = 4.0
    env.masspole = 0.2
    env.length = 0.5
    env.force_mag = 6.0
    env.reset()
    # rewards = test_policy(env, policy, max_actions=1000)
    # fig = plot_policy(rewards, policy_name="Policy")
    # plt.show()
    maxTheta = testMaxTheta(env, step=0.001)
    if maxTheta is None:
        print(f"There is no maximum theta (as long as the pole starts by not moving)")
    else: 
        print(f"Maximum Theta is {round(maxTheta, 4)} radians.")