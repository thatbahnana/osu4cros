# 🥁 osu4cros

*Probably* the only installer for osu!(lazer) on **ChromeOS**.
Install osu!(lazer) easily and quickly on your compatible device with a simple, automated script designed specifically for ChromeOS!

## 💡 Please Note

**osu4cros** is designed to work **exclusively** within **Borealis**, the Steam environment for ChromeOS.
The Linux development environment, **Crostini**, does not provide the necessary performance or compatibility for osu!(lazer) — especially in terms of touch input, audio, GPU acceleration, and overall responsiveness.

### Installing osu!(lazer) in Crostini often leads to:

* Poor performance: unstable framerate, broken audio, game running at ×1.25 speed
* Hardware incompatibilities: no support for touch, stylus, or graphics tablet, unstable mouse behavior

<sup>\*These observations are based on my own testing using an Asus Chromebook Flip CX5500.</sup>

### In contrast, installing osu!(lazer) through Borealis generally provides:

* Full compatibility with touch, controllers, mouse, and graphics tablets\*
* Smooth and stable performance thanks to GPU acceleration inside Borealis

<sup>\*Graphics tablets work partially when applying the [recommended ChromeOS settings](/CONFIGURATION.md)</sup>

💡 **osu4cros makes the installation process clean, optimized, and effortless — it automates everything and avoids complex, tedious steps.**

## 🧩 Requirements

* A **ChromeOS device compatible with Steam**
  → [See the list of supported devices](https://support.google.com/chromebook/answer/14220699#zippy=%2Csupported-devices)

* An **up-to-date version of ChromeOS**

* A **stable internet connection**
  (Required to download osu!(lazer) and its dependencies)


## 📦 Installation

1. Open the **crosh** terminal by pressing:
   `Ctrl` + `Alt` + `T`

2. If Steam (Borealis) is **already installed**, launch the Borealis environment:

```crosh
vmc launch borealis
```

Otherwise, follow [Google’s official instructions](https://support.google.com/chromebook/answer/14220699?hl=en#zippy=%2Csupported-devices) to install it.

3. Once inside Borealis, start the installation by running:

```bash
curl -sS -o install.py https://raw.githubusercontent.com/thatbahnana/osu4cros/refs/heads/main/install.py
python3 install.py
```

4. Follow the on-screen instructions to complete the installation.
Don’t forget to check the [recommended ChromeOS settings](/CONFIGURATION.md) for the best experience.


## 🐞 Known Issues

* **Audio issues on first launch**
  See the [recommended configuration](/CONFIGURATION.md) to resolve audio problems.

* **Incompatibility with Crostini**
    osu4cros **does not work** in the Linux development environment (Crostini).

* **External devices** (controller, graphics tablet, stylus, etc.)
    Work well in Borealis if properly configured. See the [recommended configuration](/CONFIGURATION.md).
