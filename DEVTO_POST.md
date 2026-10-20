---
title: "Infant sharks do, do, do support prints well: shark-fin supports for long tilted overhangs"
published: false
tags: 3dprinting, python, opensource, cura
---

Tilt a long box onto one edge and its walls get strong along their length. Its base, though, turns into a long 55° overhang: right around where slicers start adding support, and over 150 mm it tends to curl.

Normal supports fill the whole space under it and weld to every layer. So I tried something leaner: **shark fins**.

**The short version**

- A row of thin plates runs *downhill* under the face and follows its slope.
- They touch the part only at **teeth every 3 mm**. The first two teeth really touch, to hold the start of the overhang where curling begins. The rest stop 0.15 mm short.
- They **stop at 85 %** of the height with a **blunt 5 mm flat top**, because a sharp tip means tiny, slow layers.
- A crossbar foot and a one-layer brim pad keep them standing.
- On the test box: five fins, 1.68 m of filament, about 40 minutes (slicer estimate).

In Cura it's a **toolbar button**: click the face you want supported, or press Auto.

**The mistakes, for free:** the first version had a lovely round "shark" back. It was a strip of plastic doing nothing. The sloped back I sketched next cost *more* than a straight drop once measured. The paper lists all of them.

**Why a paper?** It's a defensive publication: a published method is prior art, which makes it much harder for anyone to patent it later. The fins and a long list of variations are dedicated to the public, so they stay free for hobbyists.

**The honest bit:** nothing's been printed yet. Section 8 has a test plan. If you have a printer and an evening, please break some boxes and tell me who wins.

📄 Paper: https://github.com/The-Dorkknight/fin-ally-supported
🔧 Plugin: https://github.com/The-Dorkknight/cura-shark-support
🔖 DOI: *(add after Zenodo)*
