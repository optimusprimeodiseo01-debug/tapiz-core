import time
import json
import os
import subprocess

# =====================================
# CONFIG
# =====================================

TAPIZ_REMOTE = "https://github.com/optimusprimeodiseo01-debug/tapiz-state.git"
TAPIZ_DIR = "tapiz-state"


# =====================================
# TAPIZ STRUCT
# =====================================

def es_irreductible(n):
    if n < 2:
        return False
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False
    return True


def descomponer(n):
    factores = {}
    d = 2
    while d * d <= n:
        while n % d == 0:
            factores[d] = factores.get(d, 0) + 1
            n //= d
        d += 1
    if n > 1:
        factores[n] = 1
    return factores


# =====================================
# DIRECCIONAMIENTO TAPIZ
# =====================================

def firma_a_ruta(firma):
    if not firma:
        return "tapiz/base"
    primos = sorted(firma.keys())
    return "tapiz/" + "/".join(str(p) for p in primos)


def asegurar_repo_tapiz():
    if not os.path.exists(TAPIZ_DIR):
        subprocess.run(["git", "clone", TAPIZ_REMOTE])
    else:
        subprocess.run(["git", "-C", TAPIZ_DIR, "pull"])


def publicar_estado(state):
    asegurar_repo_tapiz()

    ruta_rel = firma_a_ruta(state["firma"])
    ruta_abs = os.path.join(TAPIZ_DIR, ruta_rel)

    os.makedirs(ruta_abs, exist_ok=True)

    archivo = os.path.join(ruta_abs, f"state_{state['step']}.json")

    with open(archivo, "w") as f:
        json.dump(state, f, indent=2)

    subprocess.run(["git", "-C", TAPIZ_DIR, "add", "."])
    subprocess.run([
        "git", "-C", TAPIZ_DIR,
        "commit", "-m",
        f"tapiz publish step={state['step']} firma={state['firma']}"
    ])
    subprocess.run(["git", "-C", TAPIZ_DIR, "push"])


def leer_estados_relacionados(firma):
    asegurar_repo_tapiz()

    rutas = []

    # misma firma
    rutas.append(firma_a_ruta(firma))

    # subestructuras
    for p in firma.keys():
        rutas.append(f"tapiz/{p}")

    estados = []

    for r in rutas:
        path = os.path.join(TAPIZ_DIR, r)
        if os.path.exists(path):
            for f in os.listdir(path):
                if f.endswith(".json"):
                    try:
                        with open(os.path.join(path, f)) as file:
                            estados.append(json.load(file))
                    except:
                        pass

    return estados


# =====================================
# SENSOR
# =====================================

class TapizSensor:
    def __init__(self):
        self.state = {
            "K": 1.0,
            "Phi": 1.0,
            "Delta": 0.0,
            "step": 0,
            "firma": {}
        }
        self.last_signature = None

    def signal(self):
        return self.state["K"] * self.state["Phi"]

    def update(self):
        s = self.signal()

        # dinámica
        self.state["K"] *= 0.99
        self.state["Phi"] *= 1.0005
        self.state["Delta"] = abs(self.state["K"] - self.state["Phi"])
        self.state["step"] += 1

        # firma estructural
        n = int((self.state["step"] + 1) * (self.state["K"] * 50 + self.state["Phi"] * 50))
        self.state["firma"] = descomponer(max(2, n))

        return s

    def save(self, path="estado.json"):
        with open(path, "w") as f:
            json.dump(self.state, f, indent=2)


# =====================================
# RUNNER
# =====================================

def run():
    sensor = TapizSensor()

    print("\n--- TAPIZ DISTRIBUTED ACTIVE ---\n")

    while True:
        s = sensor.update()
        sensor.save()

        print(
            f"step={sensor.state['step']} "
            f"| s={s:.5f} "
            f"| K={sensor.state['K']:.5f} "
            f"| Phi={sensor.state['Phi']:.5f} "
            f"| Delta={sensor.state['Delta']:.5f} "
            f"| firma={sensor.state['firma']}"
        )

        # ---------------------------------
        # EVENTO ESTRUCTURAL
        # ---------------------------------

        firma_actual = sensor.state["firma"]

        if firma_actual != sensor.last_signature:

            # publicar en red
            if sensor.state["step"] % 5 == 0:
                publicar_estado(sensor.state)

            # leer vecinos
            relacionados = leer_estados_relacionados(firma_actual)

            print(f"[tapiz-net] estados relacionados: {len(relacionados)}")

            sensor.last_signature = firma_actual

        time.sleep(1)


if __name__ == "__main__":
    run()
