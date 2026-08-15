"""
Generate publication-ready versions of the paper's data figures.

Reuses the exact analysis code from the tutorials (02_erp_analysis,
04_tfr_advanced, 06_bdm_advanced, 07_ctf_analysis / 08_ctf_advanced), with
one deliberate deviation: Figure 5's broadband CTF slope panel is computed
across all 7 subjects (not just sj=2 as in 07_ctf_analysis.ipynb), since a
significant-time-window claim requires more than one subject to test.

Most of the underlying per-subject analyses (ERP target-lateralized, TFR
display-density, BDM loc_vs_main) are assumed already computed and cached
on disk by having run the corresponding tutorials at least once -- this
script only re-runs the one analysis that doesn't already exist in any
tutorial (the group-level broadband CTF for Figure 5) plus the two
single-subject BDM analyses for Figure 4's GAT/TFR panels (cheap, ~1 min
combined). If a read_* call below fails with a "no files found" style
error, run the referenced tutorial notebook first.

Usage
-----
    python paper_figures/generate_figures.py            # all figures
    python paper_figures/generate_figures.py --figure 2 # just Figure 2
"""

import argparse
import os

import matplotlib.pyplot as plt
from matplotlib import gridspec

from open_dvm.analysis import BDM, CTF, ERP
from open_dvm.support.datasets import fetch_processed_data
from open_dvm.support.FolderStructure import FolderStructure
from open_dvm.visualization.plot import (
    plot_bdm_timecourse,
    plot_ctf_timecourse,
    plot_erp_timecourse,
    plot_tfr_timecourse,
)

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "output")

# Standard eye-tracking QC, identical across all tutorials
EYE_DICT = {
    "use_tracker": True,
    "window_oi": (0, 0.3),
    "angle_thresh": 1,
    "viewing_dist": 70,
    "screen_res": (1920, 1080),
    "screen_h": 29,
    "drift_correct": (-0.2, 0),
}


def setup_publication_style():
    """Journal-typical vector-PDF settings: editable (non-outlined) text,
    a widely-available sans-serif fallback chain, and a small base font
    size appropriate for a double-column figure viewed at final size."""
    plt.rcParams.update(
        {
            "pdf.fonttype": 42,  # embed as real (editable) text, not outlined paths
            "ps.fonttype": 42,
            "font.family": "sans-serif",
            "font.sans-serif": ["Arial", "Helvetica", "DejaVu Sans"],
            "font.size": 8,
            "axes.linewidth": 0.8,
            "axes.titlesize": 9,
            "axes.labelsize": 8,
            "legend.fontsize": 7,
            "xtick.labelsize": 7,
            "ytick.labelsize": 7,
            "savefig.dpi": 300,
        }
    )


# Double-column journal width; height chosen per figure
DOUBLE_COL_WIDTH = 7.2  # inches (~183 mm)


def add_panel_label(ax, label, x=-0.10, y=1.08):
    ax.text(
        x,
        y,
        label,
        transform=ax.transAxes,
        fontsize=11,
        fontweight="bold",
        va="top",
        ha="left",
    )


def save_figure(fig, name):
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    path = os.path.join(OUTPUT_DIR, f"{name}.pdf")
    fig.savefig(path, bbox_inches="tight")
    print(f"  saved {path}")


def load_project_data():
    """Fetch (if needed) and switch into the cached tutorial dataset --
    identical fast-path used at the top of every tutorial notebook."""
    project_folder = fetch_processed_data()
    os.chdir(project_folder)


# ----------------------------------------------------------------------
# Figure 2 -- N2pc waveforms (source: 02_erp_analysis.ipynb, Section 5)
# ----------------------------------------------------------------------
def figure_2():
    print("Figure 2: N2pc waveforms (target-lateralized ERP)")

    erp_data, times = FolderStructure().read_erps(
        erp_name="target_lateralized", cnds=["absent", "present"], sjs="all"
    )

    # the data-driven N2pc window used for panel B's highlight (Listing 6)
    window_oi = ERP.select_erp_window(
        erp_data,
        elec_oi=[["PO3"], ["PO4"]],
        method="cnd_avg",
        window_oi=(0.15, 0.35),
        polarity="neg",
    )
    window_oi_ms = (window_oi[0] * 1000, window_oi[1] * 1000, window_oi[2])

    fig, axes = plt.subplots(1, 2, figsize=(DOUBLE_COL_WIDTH, 3.2))

    # Panel A: separate contra/ipsi waveforms per condition
    plt.sca(axes[0])
    plot_erp_timecourse(
        erp_data,
        times=times * 1000,
        elec_oi=[["PO3"], ["PO4"]],
        lateralized=False,
        cnds=["absent", "present"],
        colors=["navy", "royalblue", "darkred", "salmon"],
        show_SE=True,
        show_legend=True,
    )

    # Panel B: lateralized difference, highlighting the data-driven window
    # (Listing 7) -- not the broader 150-350 ms search range from Listing 6
    plt.sca(axes[1])
    plot_erp_timecourse(
        erp_data,
        times=times * 1000,
        elec_oi=[["PO3"], ["PO4"]],
        lateralized=True,
        cnds=["absent", "present"],
        colors=["blue", "red"],
        show_SE=True,
        window_oi=window_oi_ms,
        show_legend=True,
    )

    for ax, label in zip(axes, "AB"):
        add_panel_label(ax, label)

    fig.tight_layout()
    save_figure(fig, "figure2_n2pc")
    plt.close(fig)


# ----------------------------------------------------------------------
# Figure 3 -- TFR display-density dynamics (source: 04_tfr_advanced.ipynb,
# Section 4)
# ----------------------------------------------------------------------
def figure_3():
    print("Figure 3: Time-frequency dynamics (T+D+ vs T-D-)")

    tfr_data = FolderStructure().read_tfr(
        tfr_folder_path=["wavelet"],
        tfr_name="display_density",
        cnds=["T+D+", "T-D-"],
        sjs="all",
    )

    fig = plt.figure(figsize=(DOUBLE_COL_WIDTH, 5.2))
    gs = gridspec.GridSpec(2, 2, height_ratios=[1, 0.7], hspace=0.4, wspace=0.3)
    axes = [fig.add_subplot(gs[0, 0]), fig.add_subplot(gs[0, 1]), fig.add_subplot(gs[1, :])]

    conditions = ["T+D+", "T-D-"]
    for idx, cnd in enumerate(conditions):
        plt.sca(axes[idx])
        plot_tfr_timecourse(
            tfr=tfr_data,
            cnds=[cnd],
            elec_oi="all",
            timecourse="2d",
            contour=True,
            levels=20,
            cmap="viridis",
            vmin=None,
            vmax=None,
            onset_times=[0],
        )
        axes[idx].set_title(cnd, fontsize=9, fontweight="bold")
        axes[idx].axhline(8, color="red", linestyle="--", linewidth=1, alpha=0.6)
        axes[idx].axhline(12, color="red", linestyle="--", linewidth=1, alpha=0.6)

    plt.sca(axes[2])
    plot_tfr_timecourse(
        tfr=tfr_data,
        cnds=conditions,
        elec_oi="all",
        freq_oi=(8, 12),
        timecourse="1d",
        stats="fdr",
        cnd_diff=("T+D+", "T-D-"),
        onset_times=[0],
    )

    add_panel_label(axes[0], "A")
    add_panel_label(axes[2], "B")

    fig.tight_layout()
    save_figure(fig, "figure3_tfr_density")
    plt.close(fig)


# ----------------------------------------------------------------------
# Figure 4 -- BDM visualization modes (source: 06_bdm_advanced.ipynb)
# ----------------------------------------------------------------------
def figure_4():
    print("Figure 4: BDM visualization modes")

    # Panel A: group-level (7 subjects) loc_vs_main decoding, already
    # computed by 06_bdm_advanced.ipynb's Section 5 loop
    bdm_perm_data = FolderStructure().read_bdm(
        bdm_folder_path=["dist_img", "all_elecs"], bdm_name="loc_vs_main", sjs="all"
    )

    # Panels B/C: single-subject demonstrations (sj=2), matching
    # 06_bdm_advanced.ipynb Sections 2 and 4 -- cheap enough to recompute
    sj = 2
    df, epochs = FolderStructure().load_processed_epochs(
        sj=sj, fname="ses_01_main", preproc_name="main", eye_dict=EYE_DICT
    )

    bdm_gat = BDM(
        sj=sj,
        epochs=epochs,
        df=df,
        to_decode="dist_img",
        baseline=(-0.2, 0),
        nr_folds=10,
        elec_oi="all",
        data_type="broadband",
        downsample=64,
    )
    output_gat, _ = bdm_gat.classify(
        cnds=dict(block_type=["localizer"]),
        window_oi=(-0.1, 0.4),
        labels_oi="all",
        GAT=True,
    )

    bdm_tfr = BDM(
        sj=sj,
        epochs=epochs,
        df=df,
        to_decode="dist_img",
        baseline=(-0.2, 0),
        nr_folds=10,
        elec_oi="all",
        data_type="tfr",
        min_freq=4,
        max_freq=40,
        downsample=128,
    )
    output_tfr, _ = bdm_tfr.classify(
        cnds=dict(block_type=["localizer"]),
        window_oi=(-0.2, 0.5),
        labels_oi="all",
        GAT=False,
        excl_factor=dict(img_loc=[8]),
    )

    fig = plt.figure(figsize=(DOUBLE_COL_WIDTH, 6.4))
    gs = gridspec.GridSpec(2, 2, width_ratios=[1, 1.2], height_ratios=[1, 0.8], wspace=0.35, hspace=0.55)

    # Panel A: GAT matrix
    ax_a = fig.add_subplot(gs[0, 0])
    plt.sca(ax_a)
    plot_bdm_timecourse(
        output_gat,
        timecourse="2d_GAT",
        diverging_cmap=False,
        chance_level=0.5,
        mask_nonsig=False,
        stats=False,  # single subject -- no group-level test to run
    )

    # Panel B: time-frequency decoding heatmap
    ax_b = fig.add_subplot(gs[0, 1])
    plt.sca(ax_b)
    plot_bdm_timecourse(
        output_tfr,
        timecourse="2d_tfr",
        diverging_cmap=False,
        chance_level=0.5,
        mask_nonsig=False,
        stats=False,  # single subject -- no group-level test to run
    )

    # Panel C: 1D decoding timecourse, group-level, spanning the full width
    ax_c = fig.add_subplot(gs[1, :])
    plt.sca(ax_c)
    plot_bdm_timecourse(
        bdm_perm_data,
        cnds=["localizer", "main"],
        timecourse="1d",
        colors=["red", "blue"],
        stats="perm",
        cnd_diff=("localizer", "main"),
    )

    for ax, label in zip((ax_a, ax_b, ax_c), "ABC"):
        add_panel_label(ax, label)

    fig.tight_layout()
    save_figure(fig, "figure4_bdm_modes")
    plt.close(fig)


# ----------------------------------------------------------------------
# Figure 5 -- CTF slope reconstructions
#
# Panel A (multi-frequency heatmap) and panel B (single-subject broadband
# slope timecourse) are both sj=2, unchanged from 07_ctf_analysis.ipynb
# Sections 5 and 2. Panel C (group-level ping-decoding timecourse, with a
# real across-subject t-test) is from 08_ctf_advanced.ipynb's cross-task
# "ping" analysis -- already computed and cached on disk by that notebook.
# ----------------------------------------------------------------------
def figure_5():
    print("Figure 5: CTF slope reconstructions")

    sj = 2
    df, epochs = FolderStructure().load_processed_epochs(
        sj=sj, fname="ses_01_main", preproc_name="main", eye_dict=EYE_DICT
    )

    # Panel A: single-subject multi-frequency sweep (07, Section 5)
    ctf_tfr = CTF(
        sj=sj,
        epochs=epochs,
        df=df,
        to_decode="img_loc",
        nr_bins=8,
        nr_chans=8,
        elec_oi="all",
        filter=8,
        avg_ch=True,
        baseline=(-0.2, 0),
        downsample=128,
        min_freq=2,
        max_freq=30,
        num_frex=10,
        freq_scaling="linear",
    )
    _, ctf_params_tfr, _ = ctf_tfr.spatial_ctf(
        pos_labels="all",
        cnds=dict(block_type=["localizer"]),
        window_oi=(-0.2, 0.5),
        freqs="main_param",
    )

    # Panel B: single-subject broadband voltage slope timecourse (07, Section 2)
    ctf_localizer = CTF(
        sj=sj,
        epochs=epochs,
        df=df,
        to_decode="img_loc",
        nr_bins=8,
        nr_chans=8,
        elec_oi="all",
        filter=8,
        avg_ch=True,
        baseline=(-0.2, 0),
        downsample=128,
    )
    _, ctf_params, _ = ctf_localizer.spatial_ctf(
        pos_labels="all",
        cnds=dict(block_type=["localizer"]),
        window_oi=(-0.2, 0.5),
        freqs="broadband",
    )

    # Panel C: group-level ping-decoding timecourse (08, cached on disk)
    ctfs_ping = FolderStructure().read_ctfs(
        ctf_folder_path=["img_loc"], output_type="param", ctf_name="ctf_ping", sjs="all"
    )

    fig = plt.figure(figsize=(DOUBLE_COL_WIDTH, 6.0))
    gs = gridspec.GridSpec(2, 2, height_ratios=[1.3, 1], hspace=0.55, wspace=0.4)

    # Panel A: full-width top row -- this heatmap is naturally wide (time x
    # frequency), so it stays badly squashed in a narrow tall column
    ax_a = fig.add_subplot(gs[0, :])
    plt.sca(ax_a)
    plot_ctf_timecourse(
        ctf_params_tfr, cnds=["localizer"], colors=["black"], output="E_slopes",
        timecourse="2d_tfr", smooth=True,
    )
    ax_a.set_ylabel("Frequency (Hz)")

    ax_b = fig.add_subplot(gs[1, 0])
    plt.sca(ax_b)
    plot_ctf_timecourse(
        ctf_params, cnds=["localizer"], colors=["steelblue"],
        output="voltage_slopes", smooth=True, show_legend=False,
    )
    ax_b.axhline(0, color="k", linestyle="--", alpha=0.3)
    ax_b.axvline(0, color="k", linestyle="--", alpha=0.3)

    ax_c = fig.add_subplot(gs[1, 1])
    plt.sca(ax_c)
    plot_ctf_timecourse(
        ctfs_ping, cnds=["localizer_main"], colors=["red"],
        output="voltage_amps", timecourse="1d", stats="ttest", show_legend=False,
    )

    for ax, label in zip((ax_a, ax_b, ax_c), "ABC"):
        add_panel_label(ax, label)

    save_figure(fig, "figure5_ctf_slopes")
    plt.close(fig)


FIGURES = {2: figure_2, 3: figure_3, 4: figure_4, 5: figure_5}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--figure", type=int, choices=sorted(FIGURES), default=None,
        help="Generate only this figure (default: all)",
    )
    args = parser.parse_args()

    setup_publication_style()
    load_project_data()

    targets = [args.figure] if args.figure else sorted(FIGURES)
    for n in targets:
        FIGURES[n]()


if __name__ == "__main__":
    main()
