import matplotlib.pyplot as plt
import streamlit as st
import peakoscope
import peakoscope.interface_matplotlib

st.title("🎈 My new app")

X, Y = peakoscope.example_2()
peaks = peakoscope.tree(Y)
peakoscope.interface_matplotlib.TreeMatPlotLib(
    peaks,
    X=X,
    Y=Y,
    slice_of_x={n: n.subarray(X) for n in peaks},
    slice_of_y={n: n.subarray(Y) for n in peaks},
)
fig, peaks.plot.ax = plt.subplots()
peaks.plot.ax.plot(X, Y)
peaks.plot.crowns(peaks.size_filter())
peaks.plot.bounding_boxes(peaks.size_filter())

st.pyplot(fig)
