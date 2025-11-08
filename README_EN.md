- zh_CN [简体中文](README.md)

# Outer Stepped Polygon Extraction Algorithm 

An algorithm to extract the **minimum outer stepped polygon (contour)** from **Polygon (counterclockwise order)**.

![Example Result](Figure_1.png)

> **Left**: Original point set (counterclockwise order, no outer polygon)  
> **Right**: Translated point set + recomputed outer stepped polygon (CCW)

---

## Features

- Based on **four corner extremal points + recursive edge construction**
- Accurately handles **concavities, collinear points, and boundary cases**
- Outputs a **closed**, **counterclockwise** polygon vertex sequence
- Includes `matplotlib` visualization example (`test_points.py`)
- Pure Python + optional `matplotlib` (for visualization only)

---
