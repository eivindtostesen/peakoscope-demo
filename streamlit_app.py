# -*- coding: utf-8 -*-
# Copyright (C) 2025  Eivind Tøstesen
# SPDX-License-Identifier: GPL-3.0-or-later
import matplotlib.pyplot as plt
import streamlit as st
import peakoscope
import peakoscope.interface_matplotlib
import peakoscope.interface_pandas

st.title("🎈 My new app")

st.radio(
    "The algorithm finds:",
    ["Peaks", "Valleys"],
    key="radio",
    label_visibility="visible",
    horizontal=True,
)

bounding_boxes_visible = st.checkbox(
    "Plot bounding boxes", value=True, disabled=False, label_visibility="visible"
)
crowns_visible = st.checkbox(
    "Plot crowns", value=False, disabled=False, label_visibility="visible"
)

st.slider(
    "Upper limit on vertical size:",
    min_value=0.0,
    max_value=40.0,
    value=5.0,
    step=0.1,
    format="%0.1f",
    key="maxsize",
    disabled=False,
    label_visibility="visible",
)

if st.session_state.radio == "Peaks":
    valleys = False
    facecolor = "gold"
    edgecolor = "C4"
elif st.session_state.radio == "Valleys":
    valleys = True
    facecolor = "C9"
    edgecolor = "C1"

X, Y = peakoscope.example_2()
tree = peakoscope.tree(Y, valleys=valleys)
peakoscope.interface_matplotlib.TreeMatPlotLib(
    tree,
    X=X,
    Y=Y,
    slice_of_x={n: n.subarray(X) for n in tree},
    slice_of_y={n: n.subarray(Y) for n in tree},
)
peakoscope.interface_pandas.TreePandas(
    tree,
    attrname="pd",
    X=X,
)
filtered_output = list(tree.size_filter(maxsize=st.session_state.maxsize))
fig, tree.plot.ax = plt.subplots()
tree.plot.ax.set_title(st.session_state.radio)
tree.plot.ax.plot(X, Y)
if crowns_visible:
    tree.plot.crowns(filtered_output, facecolor=facecolor)
if bounding_boxes_visible:
    tree.plot.bounding_boxes(filtered_output, edgecolor=edgecolor)

st.pyplot(fig)

st.dataframe(
    tree.pd.dataframe(
        columns="node x_start x_end min max size",
        filter=filtered_output,
    )
    .pipe(tree.pd.sort, "start")
    .drop(columns="node"),
    use_container_width=False,
    hide_index=True,
)
