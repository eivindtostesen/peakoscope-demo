# -*- coding: utf-8 -*-
# Copyright (C) 2025  Eivind Tøstesen
# SPDX-License-Identifier: GPL-3.0-or-later
import matplotlib.pyplot as plt
import streamlit as st
import peakoscope
import peakoscope.interface_matplotlib

st.title("🎈 My new app")

st.radio(
    "Choose algorithm:",
    ["Find peaks", "Find valleys"],
    key="radio",
    label_visibility="visible",
    horizontal=True,
)

bb = st.checkbox(
    "Plot bounding boxes", value=True, disabled=False, label_visibility="visible"
)
crowns = st.checkbox(
    "Plot crowns", value=False, disabled=False, label_visibility="visible"
)

st.slider(
    "Filter by maximum vertical size:",
    min_value=0.0,
    max_value=40.0,
    value=5.0,
    step=0.1,
    format="%0.1f",
    key="maxsize",
    disabled=False,
    label_visibility="visible",
)

if st.session_state.radio == "Find peaks":
    valleys = False
    facecolor = "gold"
    edgecolor = "C4"
elif st.session_state.radio == "Find valleys":
    valleys = True
    facecolor = "C9"
    edgecolor = "C1"

X, Y = peakoscope.example_2()
peaks = peakoscope.tree(Y, valleys=valleys)
peakoscope.interface_matplotlib.TreeMatPlotLib(
    peaks,
    X=X,
    Y=Y,
    slice_of_x={n: n.subarray(X) for n in peaks},
    slice_of_y={n: n.subarray(Y) for n in peaks},
)
fig, peaks.plot.ax = plt.subplots()
peaks.plot.ax.plot(X, Y)
if crowns:
    peaks.plot.crowns(
        peaks.size_filter(maxsize=st.session_state.maxsize), facecolor=facecolor
    )
if bb:
    peaks.plot.bounding_boxes(
        peaks.size_filter(maxsize=st.session_state.maxsize), edgecolor=edgecolor
    )

st.pyplot(fig)
