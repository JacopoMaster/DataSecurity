from TimingAttackModule import *
import numpy as np


def compute_variance_from_observations(exp,ta):
    obs_0 = []
    obs_1 = []
    for _ in range(3000):
        ct = np.random.randint(1, 2**31) + np.random.randint(0, 2**31)  # Genero un numero random a 64 bit
        t_tot = ta.victimdevice(ct)
        # Test con bit 0
        exp.append(0)
        obs = t_tot - ta.attackerdevice(ct,exp)
        del exp[-1]
        obs_0.append(obs)
        # Test con bit 1
        exp.append(1)
        obs = t_tot - ta.attackerdevice(ct,exp)
        del exp[-1]
        obs_1.append(obs)

    var_0 = np.var(obs_0)
    var_1 = np.var(obs_1)   
    return var_0, var_1



def perform_timing_attack():
    ta = TimingAttack()
    exp = [1]
    for i in range(1,64):
        var_0, var_1 = compute_variance_from_observations(exp,ta)
        if var_0 < var_1:
            exp.append(0)
        else:
            exp.append(1)
        print(f"Dopo {i} iterazioni, l'esponente parziale è: {exp}")
    print("L'esponente segreto recuperato è:", exp)
    ta.test(exp)


#Eseguo l'attacco    
perform_timing_attack()





