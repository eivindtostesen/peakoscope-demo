# -*- coding: utf-8 -*-
# Copyright (C) 2025  Eivind Tøstesen
# SPDX-License-Identifier: GPL-3.0-or-later
import matplotlib.pyplot as plt
import streamlit as st
import peakoscope
import peakoscope.interface_matplotlib
import peakoscope.interface_pandas

st.title("🎈 My new app")

with st.echo(code_location="below"):
    # input widget columns:
    col1, col2, col3 = st.columns([1, 1, 2])

    # choose peaks or valleys:
    with col1:
        st.radio(
            "Let Peakoscope find:",
            ["Peaks", "Valleys"],
            key="radio",
        )
    if st.session_state.radio == "Peaks":
        find_valleys = False
        facecolor = "gold"
        edgecolor = "C4"
    elif st.session_state.radio == "Valleys":
        find_valleys = True
        facecolor = "C9"
        edgecolor = "C1"

    # choose plot types:
    with col2:
        bounding_boxes_visible = st.checkbox(
            "Plot bounding boxes",
            value=True,
        )
        crowns_visible = st.checkbox(
            "Plot crowns",
            value=False,
        )

    # choose input parameter:
    with col3:
        st.slider(
            "Upper limit on vertical size:",
            min_value=0.0,
            max_value=40.0,
            value=5.0,
            step=0.1,
            format="%0.1f",
            key="maxsize",
        )

    # get data set:
    data_X, data_Y = peakoscope.example_2()

    # process data set:
    tree = peakoscope.tree(data_Y, valleys=find_valleys)
    filtered_output = list(tree.size_filter(maxsize=st.session_state.maxsize))

    # generate matplotlib figure:
    peakoscope.interface_matplotlib.TreeMatPlotLib(
        tree,
        X=data_X,
        Y=data_Y,
        slice_of_x={n: n.subarray(data_X) for n in tree},
        slice_of_y={n: n.subarray(data_Y) for n in tree},
    )
    fig, tree.plot.ax = plt.subplots()
    tree.plot.ax.set_title(st.session_state.radio)
    tree.plot.ax.plot(data_X, data_Y)
    if crowns_visible:
        tree.plot.crowns(filtered_output, facecolor=facecolor)
    if bounding_boxes_visible:
        tree.plot.bounding_boxes(filtered_output, edgecolor=edgecolor)

    # generate pandas dataframe:
    peakoscope.interface_pandas.TreePandas(
        tree,
        attrname="pd",
        X=data_X,
    )
    df = (
        tree.pd.dataframe(
            columns="node x_start x_end min max size",
            filter=filtered_output,
        )
        .pipe(tree.pd.sort, "start")
        .drop(columns="node")
    )

    # columns with output:
    col1, col2 = st.columns([6, 4])

    # show the matplotlib figure:
    with col1:
        st.pyplot(fig)

    # show the pandas dataframe:
    with col2:
        st.dataframe(
            df,
            use_container_width=False,
            hide_index=True,
        )
