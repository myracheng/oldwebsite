import matplotlib.pyplot as plt
import sys
import numpy as np
import pandas as pd
from scipy.signal import savgol_filter

# Takes a list of confessions and sentiment scores
# And smooths all of them

# Optional: Plot the smoothed results against timestamp in matplotlib
PLOT = False

def smooth_score(score_name, df):
    """
    Smooths data along a given sentiment score metric
    """
    smoothed_key = score_name + "_smoothed"
    scores = df[score_name].tolist()
    yhat = savgol_filter(scores, 15, 2) # window size 15, polynomial order 3
    df[smoothed_key] = yhat

    if PLOT:
        timestamps = df["timestamp"].tolist()
        plt.plot(timestamps, yhat)
        plt.title("Sentiment " + score_name + " score vs. Timestamp")
        plt.show()

    return df

if __name__ == '__main__':
    """
    Usage:
        python3 clean.py CollegeName

    Return: Creates an smoothed csv file to be used in the graphical interface
    """
    assert(len(sys.argv) == 2)

    college_name = sys.argv[1]
    filename = college_name + ".csv"
    df = pd.read_csv(filename, header=0, sep=u",", index_col = None, encoding="ISO-8859-1")

    df = smooth_score("compound", df)
    df = smooth_score("positive", df)
    df = smooth_score("negative", df)
    df = smooth_score("neutral", df)

    df.to_csv(college_name + "_smoothed.csv")
