#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PIGPIO_SRC="$ROOT_DIR/pigpio-master/pigpio-master"

echo "[1/5] Updating apt metadata"
sudo apt update

echo "[2/5] Installing runtime/build dependencies"
sudo apt install -y build-essential python3-gpiozero python3-lgpio python3-setuptools

if [[ ! -d "$PIGPIO_SRC" ]]; then
  echo "ERROR: pigpio source not found at: $PIGPIO_SRC"
  echo "Expected folder: pigpio-master/pigpio-master"
  exit 1
fi

echo "[3/5] Building and installing pigpio from source"
make -C "$PIGPIO_SRC"
sudo make -C "$PIGPIO_SRC" install

echo "[4/5] Installing/refreshing pigpiod systemd service"
cat <<'EOF' | sudo tee /etc/systemd/system/pigpiod.service >/dev/null
[Unit]
Description=Pigpio daemon
After=network.target

[Service]
Type=forking
PIDFile=/run/pigpio.pid
ExecStart=/usr/local/bin/pigpiod -l -p 8888
ExecStop=/bin/kill -SIGTERM $MAINPID
Restart=on-failure

[Install]
WantedBy=multi-user.target
EOF

sudo systemctl daemon-reload
sudo systemctl enable --now pigpiod

echo "[5/5] Verifying pigpio + service status"
python3 - <<'PY'
import importlib
for mod in ("gpiozero", "pigpio"):
    try:
        importlib.import_module(mod)
        print(f"{mod}: OK")
    except Exception as exc:
        print(f"{mod}: FAIL -> {exc}")
        raise
PY

systemctl is-enabled pigpiod
systemctl is-active pigpiod

echo
echo "Recovery complete. Next run: python3 newptests.py"
