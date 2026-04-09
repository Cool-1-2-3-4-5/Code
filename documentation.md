Post-Reimage Recovery

Use this whenever you flash/reimage the OS and GPIO behavior changes.

Quick start
1. Open a terminal in this project folder.
2. Run:
   bash post-reimage-setup.sh
3. Test:
   python3 newptests.py

What this script restores
- gpiozero and lgpio runtime packages
- pigpio built from local source at pigpio-master/pigpio-master
- pigpiod service at boot (systemd)
- verification that Python can import gpiozero + pigpio

Why this is needed
- New Raspberry Pi OS images can be Debian trixie-based.
- On trixie, pigpio apt packages may be unavailable.
- Without pigpio daemon, gpiozero falls back to software PWM, which causes servo jitter.

Optional hardening
- Keep this whole project in git and push to remote before reimaging.
- Keep a copy of your working SD card image once everything is stable.
- After first boot from a fresh image, run only this script before testing servos.
