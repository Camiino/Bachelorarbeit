import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from glob import glob
from scipy.signal import savgol_filter

# --- CONFIG ---
INPUT_DIR = "Exports/Final_Cleaned"
OUTPUT_DIR = "Exports/Plots"
DELIMITER = ";"
MARKERS = [1, 2, 3, 4, 5]
AXES = ["X", "Y", "Z"]

# --- Setup ---
os.makedirs(OUTPUT_DIR, exist_ok=True)
files = glob(f"{INPUT_DIR}/*_final_clean.csv")

def compute_scalar_velocity_and_acceleration(df, marker_id):
    # Compute v = ||(vx, vy, vz)|| and a = ||(ax, ay, az)|| for a given marker
    vs = []
    accs = []
    for axis in AXES:
        col = f"{marker_id}_{axis}"
        if col in df.columns:
            pos = df[col].astype(float).values
            v = np.gradient(pos)
            a = np.gradient(v)
            vs.append(v)
            accs.append(a)
    if len(vs) == 3:
        vel_norm = np.sqrt(vs[0]**2 + vs[1]**2 + vs[2]**2)
        acc_norm = np.sqrt(accs[0]**2 + accs[1]**2 + accs[2]**2)

        # Smooth the results using Savitzky-Golay filter
        window_v = 9 if len(vel_norm) >= 9 else len(vel_norm) // 2 * 2 + 1
        window_a = 15 if len(acc_norm) >= 15 else len(acc_norm) // 2 * 2 + 1

        vel_smooth = savgol_filter(vel_norm, window_length=window_v, polyorder=3)
        acc_smooth = savgol_filter(acc_norm, window_length=window_a, polyorder=3)

        return vel_smooth, acc_smooth
    else:
        return None, None

# --- Plotting ---
for path in files:
    name = os.path.basename(path).replace("_final_clean.csv", "")
    print(f"\n📈 Plotting scalar curves for: {name}")

    try:
        df = pd.read_csv(path, delimiter=DELIMITER)
        time = df["Frame"].values  # 0–100 (% of motion)

        fig, (ax_v, ax_a) = plt.subplots(2, 1, figsize=(10, 6), sharex=True)
        fig.suptitle(f"{name} – Betrag von Geschwindigkeit und Beschleunigung", fontsize=14)

        for marker_id in MARKERS:
            v, a = compute_scalar_velocity_and_acceleration(df, marker_id)
            if v is not None and a is not None:
                ax_v.plot(time, v, label=f"Marker {marker_id}")
                ax_a.plot(time, a, label=f"Marker {marker_id}")

        ax_v.set_title("Geschwindigkeit (||v||)")
        ax_a.set_title("Beschleunigung (||a||)")
        ax_a.set_xlabel("Bewegungsfortschritt (%)")
        ax_v.set_ylabel("||v||")
        ax_a.set_ylabel("||a||")
        ax_v.legend()
        ax_a.legend()
        fig.tight_layout(rect=[0, 0, 1, 0.95])

        out_path = os.path.join(OUTPUT_DIR, f"{name}_velocity_acc_scalar.png")
        fig.savefig(out_path)
        plt.close(fig)
        print(f"✅ Saved plot: {out_path}")

    except Exception as e:
        print(f"❌ Failed for {name}: {e}")
