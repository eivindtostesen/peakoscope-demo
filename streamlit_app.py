# -*- coding: utf-8 -*-
# Copyright (C) 2025  Eivind Tøstesen
# SPDX-License-Identifier: GPL-3.0-or-later
import matplotlib.pyplot as plt
import streamlit as st
import peakoscope
import peakoscope.interface_matplotlib
import peakoscope.interface_pandas

st.title("Peakoscope demo")

with st.echo(code_location="below"):
    with st.sidebar:
        st.header("Generate data set")
        if "seeds_list" not in st.session_state:
            st.session_state.seeds_list = ["It's...", "The fjords"]
            st.session_state.input_seed = None

        # choose data set (random seed) from list:
        st.selectbox(
            "Select random seed value:",
            st.session_state.seeds_list,
            key="selected_seed",
        )

        # add new random seed to list:
        def insert_new_seed():
            new = st.session_state.input_seed
            if new and new not in st.session_state.seeds_list:
                st.session_state.seeds_list.insert(0, new)
                st.session_state.input_seed = None

        st.text_input(
            "Or enter a new random seed:",
            placeholder="Something completely different",
            max_chars=25,
            on_change=insert_new_seed,
            key="input_seed",
        )

        # choose window:
        st.slider(
            "Choose range of data set (x-axis):",
            min_value=1900,
            max_value=3000,
            value=(1900, 2100),
            key="range",
        )

    # generate data set:
    range_start, range_end = st.session_state.range
    data_X, data_Y = peakoscope.example_2(
        length=range_end - 1900 + 1, randomseed=st.session_state.selected_seed
    )
    data_X = data_X[range_start - 1900 :]
    data_Y = data_Y[range_start - 1900 :]

    # columns with input widgets:
    radio_col, check_col, slider_col = st.columns([1, 1, 2])

    # choose algorithm:
    with radio_col:
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
    with check_col:
        bounding_boxes_visible = st.checkbox(
            "Plot bounding boxes",
            value=True,
        )
        crowns_visible = st.checkbox(
            "Plot crowns",
            value=False,
        )

    # choose input parameter:
    with slider_col:
        st.slider(
            "Upper limit on vertical size:",
            min_value=0,
            max_value=int(max(data_Y) - min(data_Y) + 1),
            value=int(0.2 * (max(data_Y) - min(data_Y))),
            key="maxsize",
        )

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
    tree.plot.ax.set_title(f"{st.session_state.radio} in data")
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
    fig_col, df_col = st.columns([6, 4])

    # show the matplotlib figure:
    with fig_col:
        st.pyplot(fig)

    # show the pandas dataframe:
    with df_col:
        st.dataframe(
            df,
            use_container_width=False,
            hide_index=True,
        )

    st.subheader("Code")
