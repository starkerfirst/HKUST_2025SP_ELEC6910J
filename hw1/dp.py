# coding: utf-8
import time
import numpy as np
import gymnasium as gym
from gymnasium.wrappers import TimeLimit
from gymnasium.envs.registration import register


register(id='SlipperyFrozenLake-v1',
    entry_point='gymnasium.envs.toy_text.frozen_lake:FrozenLakeEnv',
    kwargs={'map_name': '4x4', 'is_slippery': True})
register(id='FrozenLake-v1',
    entry_point='gymnasium.envs.toy_text.frozen_lake:FrozenLakeEnv',
    kwargs={'map_name': '4x4', 'is_slippery': False})


"""
For policy_evaluation, policy_improvement, policy_iteration and value_iteration,
the parameters P, nS, nA, gamma are defined as follows:

	P: nested dictionary
		From gym.core.Environment
		For each pair of states in [1, nS] and actions in [1, nA], P[state][action] is a list of
		tuple of the form (p_trans, next_state, reward, terminal) where
			- p_trans: float
				the transition probability of transitioning from "state" to "next_state" with "action"
			- next_state: int
				denotes the state we transition to (in range [0, nS - 1])
			- reward: int
				either 0 or 1, the reward for transitioning from "state" to
				"next_state" with "action"
			- terminal: bool
			  True when "next_state" is a terminal state (hole or goal), False otherwise
	nS: int
		number of states in the environment
	nA: int
		number of actions in the environment
	gamma: float
		Discount factor. Number in range [0, 1)
"""


def policy_evaluation(P, nS, nA, policy, gamma=0.9, eps=1e-3):
    """Evaluate the value function from a given policy.

    Parameters
    ----------
    P, nS, nA, gamma:
      defined at beginning of file
    policy: np.array[nS]
      The policy to evaluate. Maps states to actions.
    eps: float
      Terminate policy evaluation when
        max |value_function(s) - prev_value_function(s)| < eps
    Returns
    -------
    value_function: np.ndarray[nS]
      The value function of the given policy, where value_function[s] is
      the value of state s
    """

    value_function = np.zeros(nS)

    ############################
    # YOUR IMPLEMENTATION HERE #
    
    while True:
      old_value_function = value_function.copy()
      for state in range(nS):
        value_s = 0
        for p, next_s, r, done in P[state][policy[state]]: # reward is given during transition from 14 to 15
          if done:
            value_s += p * r
            continue
          value_s += p * (r + gamma * old_value_function[next_s])
        value_function[state] = value_s
      
      # exit condition
      if np.max(np.abs(value_function - old_value_function)) < eps:
        break


    ############################
    return value_function


def policy_improvement(P, nS, nA, value_from_policy, policy, gamma=0.9):
    """Given the value function from policy, improve the policy.

    Parameters
    ----------
    P, nS, nA, gamma:
      defined at beginning of file
    value_from_policy: np.ndarray
      The value calculated from evaluating the policy
    policy: np.array
      The previous policy.

    Returns
    -------
    new_policy: np.ndarray[nS]
      An array of integers. Each integer is the optimal action to take
      in that state according to the environment dynamics and the
      given value function.
    """

    new_policy = np.zeros(nS, dtype=int)

    ############################
    # YOUR IMPLEMENTATION HERE #
    
    for state in range(nS):
      max_value = -np.inf
      for action in range(nA):
        value = 0
        for p, next_s, r, done in P[state][action]:
          if done:
            value += p * r
            continue
          value += p * (r + gamma * value_from_policy[next_s])
        if value > max_value:
          max_value = value
          new_policy[state] = action

    ############################
    return new_policy


def policy_iteration(P, nS, nA, gamma=0.9, eps=10e-3):
    """Runs policy iteration.

    You should call the policy_evaluation() and policy_improvement() methods to
    implement this method.

    Parameters
    ----------
    P, nS, nA, gamma:
      defined at beginning of file
    eps: float
      eps parameter used in policy_evaluation()
    Returns:
    ----------
    value_function: np.ndarray[nS]
    policy: np.ndarray[nS]
    """

    value_function = np.zeros(nS)
    policy = np.zeros(nS, dtype=int)

    ############################
    # YOUR IMPLEMENTATION HERE #
    # 0: left
    # 1: down
    # 2: right
    # 3: up
    while True:
      old_policy = policy.copy()
      value_function = policy_evaluation(P, nS, nA, policy)
      policy = policy_improvement(P, nS, nA, value_function, policy)
      
      if np.array_equal(policy, old_policy):
        break

    ############################
    return value_function, policy


def value_iteration(P, nS, nA, gamma=0.9, eps=1e-3):
    """Learn value function and policy using value iteration method for a given
    gamma and environment.

    Parameters:
    ----------
    P, nS, nA, gamma:
      defined at beginning of file
    eps: float
      Terminate value iteration when
        max |value_function(s) - prev_value_function(s)| < eps
    Returns:
    ----------
    value_function: np.ndarray[nS]
    policy: np.ndarray[nS]
    """

    value_function = np.zeros(nS)
    policy = np.zeros(nS, dtype=int)
    ############################
    # YOUR IMPLEMENTATION HERE #

    while True:
      old_value_function = value_function.copy()
      for state in range(nS):
        max_value = -np.inf
        for action in range(nA):
          value_s = 0
          for p, next_s, r, done in P[state][action]: # reward is given during transition from 14 to 15
            if done:
              value_s += p * r
              continue
            value_s += p * (r + gamma * old_value_function[next_s])
          if value_s > max_value:
            max_value = value_s
        value_function[state] = max_value
      
      # exit condition
      if np.max(np.abs(value_function - old_value_function)) < eps:
        break

    # output policy
    for state in range(nS):
      max_value = -np.inf
      max_action = 0
      for action in range(nA):
        value_s = 0
        for p, next_s, r, done in P[state][action]: # reward is given during transition from 14 to 15
          if done:
            value_s += p * r
            continue
          value_s += p * (r + gamma * value_function[next_s])
        if value_s > max_value:
          max_value = value_s
          max_action = action
      policy[state] = max_action

    ############################
    return value_function, policy


def render_single(env, policy, max_steps=100):
    """This function does not need to be modified.
    Renders policy once on environment. Watch your agent play!

    Parameters
    ----------
    env: gym.core.Environment
      Environment to play on. Must have nS, nA, and P as attributes.
    policy: np.array of shape [env.nS]
      The action to take at a given state
    """

    episode_reward = 0
    state, _ = env.reset()
    while True:
        env.render()
        time.sleep(0.25)
        action = policy[state]
        state, reward, terminal, truncated, _ = env.step(action)
        episode_reward += reward
        if terminal or truncated:
            break
    env.render()
    if not terminal:
        print("The agent didn't reach a terminal state in {} steps.".format(max_steps))
    else:
        print("Episode reward: %f" % episode_reward)


# Edit below to run policy and value iteration on different environments and
# visualize the resulting policies in action!
# You may change the parameters in the functions below
if __name__ == "__main__":
    # comment/uncomment these lines to switch between deterministic/stochastic environments
    # human render mode for the animation
    # env = gym.make("FrozenLake-v1", render_mode="human")
    env = gym.make("SlipperyFrozenLake-v1", render_mode="human")

    env = TimeLimit(env, max_episode_steps=100)
    P = env.P
    nS, nA = env.observation_space.n, env.action_space.n

    print("\n" + "-" * 25 + "\nBeginning Policy Iteration\n" + "-" * 25)
    V_pi, p_pi = policy_iteration(P, nS, nA, gamma=0.9, eps=1e-3)
    print(f"finish policy iteration: {V_pi} {p_pi}")
    render_single(env, p_pi, 100)
    print(p_pi)

    print("\n" + "-" * 25 + "\nBeginning Value Iteration\n" + "-" * 25)
    V_vi, p_vi = value_iteration(P, nS, nA, gamma=0.9, eps=1e-3)
    print(f"finish policy iteration: {V_vi} {p_vi}")
    render_single(env, p_vi, 100)
    print(p_vi)
