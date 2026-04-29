import time
import json
import os
import subprocess


class TapizSensor:
    def __init__(self):
        self.state = {
            "K": 1.0,
            "Phi": 1.0,
            "Delta": 0.0,
            "step": 0
        }
        self.last_commit_signal = 0.0

    def signal(self):
        return (self.state["K"] * self.state["Phi"]) - self.state["Delta"]

    def update(self):
        s = self.signal()

        self.state["K"] = 0.9 * self.state["K"] + 0.1 * abs(s)
        self.state["Phi"] = 0.95 * self.state["Phi"] + 0.05 * (1 + s * 0.01)
        self.state["Delta"] = 0.5 * self.state["Delta"] + 0.5 * (s * 0.1)

        self.state["step"] += 1
        return s

    def save(self, path="estado.json"):
        with open(path, "w") as f:
            json.dump(self.state, f, indent=2)


# -------------------------
# GIT CONTROL LAYER
# -------------------------

def git_commit(signal, state):
    msg = f"tapiz sync | s={signal:.4f} | K={state['K']:.3f}"

    subprocess.run(["git", "add", "."], stdout=subprocess.DEVNULL)
    subprocess.run(["git", "commit", "-m", msg], stdout=subprocess.DEVNULL)
    subprocess.run(["git", "push"], stdout=subprocess.DEVNULL)


def run():
    sensor = TapizSensor()

    print("\n--- TAPIZ SENSOR + GIT ACTIVE ---\n")

    while True:
        s = sensor.update()
        sensor.save()

        print(
            f"step={sensor.state['step']} "
            f"| s={s:.5f} "
            f"| K={sensor.state['K']:.5f} "
            f"| Phi={sensor.state['Phi']:.5f} "
            f"| Delta={sensor.state['Delta']:.5f}"
        )

        # -------------------------
        # CONDICIÓN DE COMMIT
        # -------------------------
        delta_signal = abs(s - sensor.last_commit_signal)

        if delta_signal > 0.5:
            git_commit(s, sensor.state)
            sensor.last_commit_signal = s

        time.sleep(1)


if __name__ == "__main__":
    run()
