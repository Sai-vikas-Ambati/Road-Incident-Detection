import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm

def detect_anomalies(data):
    mu, std = np.mean(data), np.std(data)
    anomalies = [x for x in data if abs(x - mu) > 2*std]
    return anomalies

if __name__ == "__main__":
    traffic_flow = np.random.normal(50, 10, 100)
    anomalies = detect_anomalies(traffic_flow)
    print("Detected anomalies:", anomalies)
