<div align="center">

<a href="https://wisemandenny.github.io/hxtra/web/"><img src="docs/assets/banner.svg" alt="HXtra: custom firmware for the Line 6 HX Stomp" width="100%"></a>

[![Release](https://img.shields.io/github/v/release/wisemandenny/hxtra?style=flat-square&color=ff2e93&label=release)](https://github.com/wisemandenny/hxtra/releases/latest)
[![License: GPL-3.0](https://img.shields.io/github/license/wisemandenny/hxtra?style=flat-square&color=blue)](LICENSE)
[![Stars](https://img.shields.io/github/stars/wisemandenny/hxtra?style=flat-square&color=yellow)](https://github.com/wisemandenny/hxtra/stargazers)
[![Last commit](https://img.shields.io/github/last-commit/wisemandenny/hxtra?style=flat-square)](https://github.com/wisemandenny/hxtra/commits/main)

<!-- demo: tour, a short loop of the virtual HX Stomp from tools/hx_mirror.py -->
<p><img src="https://github.com/user-attachments/assets/b804955a-3275-40b6-932b-d1ccf10c4d95" width="480" alt="A tour of HXtra on the HX Stomp: the BPM and tap colours, DSP usage in the Edit view and model browser, and six snapshots"></p>

</div>

<a href="https://wisemandenny.github.io/hxtra/web/#recovery"><img src="docs/assets/safe.svg" alt="100% safe for your HX Stomp: HXtra never touches the bootloader, so the stock firmware can always go back on." width="100%"></a>

<table>
<tr>
<td width="33%" valign="top">

&nbsp;

<img src="docs/assets/icons/try.svg" width="40" height="40" align="absmiddle" alt=""> **[Try before you install](https://wisemandenny.github.io/hxtra/web/#try-without-installing)**

Run HXtra from the HX Stomp's memory for one session. Nothing is written to the unit, and a power-cycle brings back what you had.

&nbsp;

</td>
<td width="33%" valign="top">

&nbsp;

<img src="docs/assets/icons/recover.svg" width="40" height="40" align="absmiddle" alt=""> **[Always recoverable](https://wisemandenny.github.io/hxtra/web/#recovery)**

If an install ever stops at the splash screen, hold Page Right while powering on and reinstall stock with Line 6 Updater. Every feature ran on a real HX Stomp before release.

&nbsp;

</td>
<td width="33%" valign="top">

&nbsp;

<img src="docs/assets/icons/install.svg" width="40" height="40" align="absmiddle" alt=""> **[Install from your browser](https://wisemandenny.github.io/hxtra/web/)**

The setup page builds HXtra locally from your own firmware file, right in your browser. Nothing is uploaded, and there's no software to set up on your computer.

&nbsp;

</td>
</tr>
</table>

## Installation

<p align="center"><a href="https://wisemandenny.github.io/hxtra/web/"><img src="docs/assets/install-hxtra.svg" alt="Install HXtra" width="60%"></a></p>

## Features

<sub>*Demos were recorded from a real HX Stomp's screen, along with its audio and button presses, then overlaid on a simulated HX Stomp.*</sub>

### <img src="docs/assets/icons/tuner.svg" width="28" height="28" align="top" alt=""> Tuner settings

*On the tuner's own third page*

- **Tuner button** (Hold, Press): "Hold" opens the tuner when you hold TAP (stock behavior); "Press" opens it with a press, and TAP no longer taps the tempo.
- **Tuner lock** (Off, On): On locks the tuner's other settings (Output, Reference, Type, Trails, Offsets).

<!-- demo: tuner -->
<details>
<summary>Demo</summary>

<img src="https://github.com/user-attachments/assets/7decba81-b026-4fb5-95f9-6c8899b2e47c" width="100%" alt="The tuner: Activate set to Press, so one press opens it, then Lock On and its knobs no longer change">

</details>

### <img src="docs/assets/icons/bpm.svg" width="40" height="28" align="top" alt=""> BPM display

*Global Settings › BPM Display*

- **Font size** (XL, L, M, S, Off): the size of the tempo text at the top left of the Home screen. Off hides it.
- **Color** (White, Gray, Red, Orange, Yellow, Green, Cyan, Blue, Purple, Tempo): the tempo text's and the beat dot's colour. Tempo follows the TAP footswitch's colour (Tap LED Color).
- **Dot position** (Left, Right, Both, Off): where the beat dot blinks with TAP, beside the preset number. Off hides it; with both Off the BPM display is off.

<!-- demo: bpm -->
<details>
<summary>Tap demo</summary>

<img src="https://github.com/user-attachments/assets/62783af2-506f-4878-80ed-e2705acba51c" width="100%" alt="Tapping TAP: the tempo and its beat dot follow">

</details>

<details>
<summary>Settings demo</summary>

<img src="https://github.com/user-attachments/assets/4579e864-8a7d-46fd-a764-ec5cd102b6e9" width="100%" alt="Global Settings, BPM Display: Font Size, Color and Dot Position">

</details>

### <img src="docs/assets/icons/breathing-line.svg" width="28" height="28" align="top" alt=""> Breathing line

*Global Settings › Breathing Line*

- **Color** (White, Red, Green, Blue, Fire, Ice, Sunset, Ocean, Aurora, Neon, Rainbow): the colour or gradient of the line across the middle of the Home screen.
- **Type** (Off, Steady, Breathe, Cylon, Comet, Heart, Sparkle): how it moves; Off gives back the stock line.
- **Speed** (1–10, Tempo): the speed of the animation. 1 = 8s/cycle, 10 = 0.8s/cycle; Tempo follows the tempo.

<!-- demo: breathing-line -->
<details>
<summary>Unit demo</summary>

<img src="https://github.com/user-attachments/assets/d492b0aa-1151-42c6-b84a-27f6fd36e5d8" width="100%" alt="Breathing Line types, colours and speeds on the Home screen, on the unit">

</details>

<details>
<summary>Screen-only demo</summary>

<img src="https://github.com/user-attachments/assets/dd1085e1-c51d-4377-8dee-26b8ce5e1423" width="100%" alt="The same, the screen alone: Steady, Breathe, Cylon, Heart, Sparkle, then Aurora, Ice, Fire and Tempo">

</details>

### <img src="docs/assets/icons/dsp-usage.svg" width="32" height="32" align="top" alt=""> DSP meter

- Each block shows its share of the DSP, and the top right corner the total, in the Edit view and in the model browser.

<!-- demo: dsp-usage -->
<details>
<summary>Demo</summary>

<img src="https://github.com/user-attachments/assets/fb8644f3-b5ab-4803-b3be-fefcfb23c7b3" width="100%" alt="Browsing bass amps: the DSP total previews each model, then the added block shows its share">

</details>

### <img src="docs/assets/icons/gr-meter.svg" width="28" height="28" align="top" alt=""> Gain reduction meter

*New settings on all compressors except 3-Band Compressor*

- **Mtr Size** (Off, S, M, L, XL): the meter's thickness. Each size is an additional 5px; off disables the meter.
- **Mtr Pos** (Middle, Top, Left, Bottom, Right): Location of the meter on the Home screen. Middle takes the place of the line across the middle, and disables breathing line.
- **Mtr Dir** (Normal, Reverse): Normal fills left to right or top to bottom; Reverse the other way. Useful for Left/Right position settings.

<!-- demo: gr-meter -->
<details>
<summary>Demo</summary>

https://github.com/user-attachments/assets/50b5cd91-f578-4252-a1df-4b73d8ca1995

</details>

### <img src="docs/assets/icons/long-press.svg" width="28" height="28" align="top" alt=""> Virtual footswitches

*Global Settings › Footswitches*

- **Assign a block**: in the block's Bypass Assign, press Page › once to see MIDI In, then turn MIDI In up from Off: FS6 is one click up, FS10 five
- **Parameters**: assign one to the same FS in Controller Assign, and it follows the footswitch too.
- **MIDI**: **underneath, FS6 … FS10 are MIDI CC 20 … 24.** HX Edit shows them that way, and a MIDI controller sending those CCs switches them as well.

<details>
<summary>Demo</summary>

<img src="https://github.com/user-attachments/assets/f0261c29-ef31-4527-8d96-21ef176b67aa" width="100%" alt="A block's Bypass Assign: MIDI In set to the virtual footswitch FS6, then holding FS2 toggles it">

</details>

### <img src="docs/assets/icons/long-press.svg" width="28" height="28" align="top" alt=""> Footswitch long press

*Global Settings › Footswitches*

- **FS1 … FS5 Hold** (Off, Tuner, FS4, FS5, FS6 … FS10): what holding that footswitch for a second does in Stomp mode. FS6 … FS10 are virtual footswitches: assign blocks to them in Bypass Assign.
- **FS6 … FS10 Function** (Tuner, Stomp, Bank Up, Bank Dn, PresetUp, PresetDn, SnpshtUp, SnpshtDn, FS Mode&gt;, &lt;FS Mode, AllBypas, TogglEXP): what that virtual footswitch does, as FS3 … FS5 Function do for the real ones. Stomp, the default, toggles its blocks.
- **Switch a virtual footswitch**: hold the footswitch whose Hold is set to that FS. By default, holding FS1 switches FS6, and so on up to FS5 and FS10.

<!-- demo: long-press -->
<details>
<summary>Demo</summary>

<img src="https://github.com/user-attachments/assets/50a6ecf0-6d87-4556-8ffd-035e4b40987b" width="100%" alt="Tapping and holding FS2, holding FS1 for the tuner, then the Hold and FS6 to FS10 Function settings">

</details>

### <img src="docs/assets/icons/snapshots.svg" width="104" height="32" align="top" alt=""> More snapshots

- Six snapshots per preset: press the lit snapshot footswitch again to flip between snapshots 1–3 and 4–6.
- Once a preset has snapshots 4–6, next and previous snapshot (SnpshtUp, SnpshtDn, MIDI CC 69) step through all six: next on 3 goes to 4, and next on 6 back to 1.
- MIDI CC 69 selects any of the six directly: values 0–2 for snapshots 1–3, 3–5 for 4–6.

<!-- demo: snapshots -->
<details>
<summary>Demo</summary>

<img src="https://github.com/user-attachments/assets/8ce9d86c-cffb-491e-9c47-0430a02a4af7" width="100%" alt="Snapshots 1 to 3, the lit footswitch again for 4 to 6, and again back to 1 to 3">

</details>

### <img src="docs/assets/icons/tap-color.svg" width="28" height="28" align="top" alt=""> Tap LED color

*Global Settings › Displays*

- **Tap LED Color** (Red, DkOrange, LtOrange, Yellow, Green, Teal, Blue, Violet, Pink, White, Rainbow, Random): the colour of the TAP footswitch's blinking LED ring, and the icon and label of TAP/TUNER on the Home screen. Rainbow fades the ring a small step through the rainbow on each beat; Random picks a new colour at each beat. Both keep the label white.

<!-- demo: tap-color -->
<details>
<summary>Demo</summary>

<img src="https://github.com/user-attachments/assets/29f1b0a3-fa13-4d40-bfb0-cb426b15079d" width="100%" alt="Tap LED Color: red, green, blue, then Rainbow walking the colour wheel, and BPM Display Color Tempo following it">

</details>

### <img src="docs/assets/icons/metronome.svg" width="35" height="28" align="top" alt=""> Metronome

*New block: Looper › Metronome*

- **Time** (a note value, synced to the tempo): the beat, as a delay's Time.
- **Level** (−60 … +6 dB): the click's volume.
- **Accent** (Off, 2 … 12): every nth beat is a downbeat, a higher click.
- **Thru** (Off, On): On plays your signal with the click under it; Off plays the click alone.

<!-- demo: metronome -->
<details>
<summary>Demo</summary>

https://github.com/user-attachments/assets/f25be41c-3ab0-45a1-87fa-99cd50194933

</details>

### <img src="docs/assets/icons/real-names.svg" width="28" height="28" align="top" alt=""> Real block names (optional, off unless you tick it on the setup page)

*No settings*

- Renames all blocks to match the gear they were based on: e.g. Deez One Mod becomes Boss DS-1 Mod.

<!-- demo: real-names -->
<details>
<summary>Demo</summary>

<img src="https://github.com/user-attachments/assets/607728e6-773b-41ae-9619-5a30ca2f50ad" width="100%" alt="The model browser's Distortion list by real names: Xotic EP Booster, Klon Centaur, Ibanez TS808">

</details>

### <img src="docs/assets/icons/nam.svg" width="28" height="28" align="top" alt=""> NAM A2 Lite

- [Neural Amp Modeler](https://www.neuralampmodeler.com) captures on the HX Stomp's own DSP, from [hx-stomp-nam-lite](https://github.com/nocaseguy/hx-stomp-nam-lite). The setup page converts your `.nam` files.

<div align="center">

<a href="docs/features.md"><img src="docs/assets/feature-guide.svg" alt="Read the feature guide" width="45%"></a>

</div>

## Engineering

<table>
<tr>
<td width="50%" valign="top">

### <img src="docs/assets/icons/dev-module.svg" width="28" height="28" align="top" alt=""> Feature modules
Each feature is one Python module in `tools/features/` with its Cortex-M4 code in `src/m4/`, and the build automatically finds it.

&nbsp;

</td>
<td width="50%" valign="top">

### <img src="docs/assets/icons/dev-hooks.svg" width="28" height="28" align="top" alt=""> Hook layer
Features reach the firmware only through hooks that the patcher, `tools/patch_menu.py`, lets them share, and every write checks the stock bytes first, so a clash fails the build, not the unit.

&nbsp;

</td>
</tr>
<tr>
<td valign="top">

### <img src="docs/assets/icons/dev-settings.svg" width="28" height="28" align="top" alt=""> Virtual global settings
The patcher makes up its own setting IDs and packs their values into unused records the HX Stomp already saves, increasing the capacity from 10 settings to 46.

&nbsp;

</td>
<td valign="top">

### <img src="docs/assets/icons/dev-pipeline.svg" width="28" height="28" align="top" alt=""> From Python to HX Stomp
`tools/m4asm.py` assembles each feature's code with `clang`, the patcher places it in free space in the firmware and points the hooked stock calls at it, and `tools/hxf.py` packs the result into a new `.hxf`.

&nbsp;

</td>
</tr>
<tr>
<td valign="top">

### <img src="docs/assets/icons/dev-tested.svg" width="28" height="28" align="top" alt=""> Emulated first
Every feature's M4 code runs on an emulated Cortex-M4 ([unicorn](https://www.unicorn-engine.org), `tests/m4emu.py`) before it runs on a unit, and a pinned MD5 of the whole build catches any byte that changes by accident.

&nbsp;

</td>
<td valign="top">

### <img src="docs/assets/icons/dev-mirror.svg" width="28" height="28" align="top" alt=""> Screen mirror and demo videos
A developer build streams the HX Stomp's screen over USB, and `tools/hx_mirror.py` records it with every control event and renders the demo videos in this README.

&nbsp;

</td>
</tr>
</table>

<div align="center">

<a href="docs/architecture.md"><img src="docs/assets/engineering-guide.svg" alt="Read the engineering guide" width="51%"></a>

</div>

## Why use AI?

<table>
<tr>
<td width="50%" valign="top">

### 100% reverse engineered
The HX Stomp has no SDK, no documentation, no source code and no debug symbols. Everything HXtra changes had to be found first by reading raw disassembly of a stripped binary that runs on two processors: the Cortex-M4 that runs the screen and footswitches, and the SHARC DSP that processes the audio.

&nbsp;

</td>
<td valign="top">

### AI only writes code
One person chose every feature and decided how each should look, feel and behave, and shelved ideas that were unsafe or not worth the risk. I loaded every test build onto my own HX Stomp, played through it and watched the screen, which is where most bugs were caught, and tuned animation speeds, colours and the click's volume by eye and ear. All AI did is write the code.

&nbsp;

</td>
</tr>
</table>

## FAQ

<table>
<tr>
<td width="50%" valign="top">

### <img src="docs/assets/icons/faq-stock.svg" width="28" height="28" align="top" alt=""> How do I go back to stock firmware?
[See the recovery guide on the setup page](https://wisemandenny.github.io/hxtra/web/#recovery)

&nbsp;

</td>
<td width="50%" valign="top">

### <img src="docs/assets/icons/faq-presets.svg" width="28" height="28" align="top" alt=""> Will this break my presets?
- **No.** Presets made on stock firmware open in HXtra.
- A preset saved with snapshots 4–6 still loads on stock firmware, as snapshots 1–3.
- HX Edit opens, exports and imports HXtra presets, but its exports (`.hlx`) and backups (`.hxb`) hold snapshots 1–3 only.
- Presets made with an older release of [hx-stomp-nam-lite](https://github.com/nocaseguy/hx-stomp-nam-lite) won't load their NAM blocks in HXtra, so add NAM to those presets again. Presets from its current release open as they are.

&nbsp;

</td>
</tr>
<tr>
<td valign="top">

### <img src="docs/assets/icons/faq-dsp.svg" width="28" height="28" align="top" alt=""> Does HXtra use up extra DSP?
**No.** DSP usage is only marginally affected by the compressor gain reduction meter and the metronome block. If you notice any audio crackling, disable those features.

&nbsp;

</td>
<td valign="top">

### <img src="docs/assets/icons/faq-choose.svg" width="28" height="28" align="top" alt=""> Can I choose which features I get?
The setup page builds every feature, plus Real block names if you tick their box. To leave a feature out of the firmware altogether, [build it yourself](docs/building.md).

&nbsp;

</td>
</tr>
<tr>
<td valign="top">

### <img src="docs/assets/icons/faq-platforms.svg" width="28" height="28" align="top" alt=""> Which operating systems are supported?
*Only macOS and Windows are fully supported.*

- The setup page builds HXtra on Windows, macOS and Linux, in any modern browser.
- Its Run from RAM step needs Chrome or Edge.
- Installing uses Line 6 Updater, which runs on Windows and macOS.
- Building from the command line needs clang to assemble the features' code: Apple's Command Line Tools on a Mac, or clang on Linux and WSL (`apt install clang`). Both give the same build, MD5 included.

&nbsp;

</td>
<td valign="top">

### <img src="docs/assets/icons/faq-legal.svg" width="28" height="28" align="top" alt=""> Is this legal?
*This isn't legal advice, and where you live matters.*

- **No locks are broken.** The firmware isn't encrypted or signed, so HXtra doesn't violate copy protection. That is what anti-circumvention laws such as the US DMCA (§1201) forbid.
- **Reverse engineering for compatible software is protected** in the US (*Sega v. Accolade*), the EU (Software Directive, Articles 5(3) and 6), the UK (CDPA ss. 50B and 50BA) and Canada (Copyright Act s. 30.61).
- **This repo does not contain Line 6 IP** The patcher holds only addresses, table layouts and a few short runs of stock bytes it checks before writing. You bring your own copy of the official firmware, and the build changes it on your computer.
- **Changing the firmware on your own unit** is private use. US law lets the owner of a program's copy adapt it to run it on their machine (17 U.S.C. §117), other countries are less clear, and Line 6's license terms may forbid it: that is a contract matter between you and Line 6.
- **Don't share the built `.hxf`.** It is Line 6's firmware with changes, and passing it on would infringe their copyright.
- No NAM captures are included either; you bring your own.

&nbsp;

</td>
</tr>
</table>

## Known issues

- With the breathing line on, the BPM beat dot sometimes draws half lit.
- Tapping the tempo doesn't yet move the Metronome's beat onto your taps.

Found something else? [Open an issue](https://github.com/wisemandenny/hxtra/issues/new/choose).

## Acknowledgements

- **[Derek Bui (nocaseguy)](https://github.com/nocaseguy)**, for [hx-stomp-nam-lite](https://github.com/nocaseguy/hx-stomp-nam-lite), the foundation HXtra is forked from. It brought the SHARC assembler and simulator, the NAM A2 Lite kernel, the firmware container tools, the RAM loader and the setup page, and it showed that the HX Stomp's firmware can be changed safely.
- **[ghidra-sharc](https://github.com/roblg/ghidra-sharc)**, whose SHARC opcode tables the assembler adapts.
- **[Neural Amp Modeler](https://github.com/sdatkinson/neural-amp-modeler)**, by Steven Atkinson.
- **[Jason Shimmy](https://jasonshimmy.com/)**, for [HelixHelp](https://helixhelp.com/), whose model list gives Real block names the gear each model is based on.

## License

HXtra is [GPL-3.0-or-later](LICENSE). Third-party notices are in [NOTICE](NOTICE). Line 6, Helix, HX Stomp, HX Effects and HX Edit are trademarks of Yamaha Guitar Group, Inc. HXtra is not affiliated with, endorsed by or supported by Line 6 or Yamaha Guitar Group.
