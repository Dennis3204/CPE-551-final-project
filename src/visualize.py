"""
visualize.py

this script creates Matplotlib charts that turn the analysis module's outputs into pictures.

Three plots live here, one per question the project sets out to answer:

    - "plot_top_n_underserved"
    - "plot_port_mix"
    - "plot_geographic_distribution" 
"""

import matplotlib.pyplot as plt


# color palette for nice formatting
COLOR_GAP_BAR = "#cc3344"
COLOR_LEVEL1 = "#fdd0a2"
COLOR_LEVEL2 = "#fdae6b"
COLOR_DC_FAST = "#e6550d"
COLOR_STANDARD_ONLY = "#888888"
COLOR_FAST_CAPABLE = "#cc3344"


def plot_top_n_underserved(ranked_regions, n=10):
    """
    this outputs a horizontal bar chart of the worst N regions by EV gap score.

    """
    if n <= 0:
        raise ValueError(f"n must be a positive integer, got {n!r}.")

    top = ranked_regions[:n]
    names = [name for name, _ in top]
    scores = [score for _, score in top]

    # make the height grow with row count so the labels never overlap
    fig, ax = plt.subplots(figsize=(8, max(3.0, 0.4 * len(top) + 2.0)))
    ax.barh(names, scores, color=COLOR_GAP_BAR, label="Gap score")

    ax.set_xlabel("Gap score (higher = more underserved)")
    ax.set_ylabel("Region")
    ax.set_title(
        f"Top {len(top)} Underserved Regions by EV Charging Gap Score"
    )

    ax.set_xlim(0.0, 1.0)
    ax.invert_yaxis()
    ax.legend(loc="lower right")

    return fig


def plot_port_mix(regions, n=10):
    """
    Stacked bar chart of Level 1 / Level 2 / DC Fast counts per region.
    """
    if n <= 0:
        raise ValueError(f"n must be a positive integer, got {n!r}.")

    sorted_regions = sorted(
        regions.values(),
        key=lambda r: r.total_stations(),
        reverse=True,
    )
    top = sorted_regions[:n]

    names = [region.region_name for region in top]
    l1_counts = []
    l2_counts = []
    fast_counts = []
    for region in top:
        l1_counts.append(sum(s.level1 for s in region.stations))
        l2_counts.append(sum(s.level2 for s in region.stations))
        fast_counts.append(sum(s.dc_fast for s in region.stations))

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.bar(names, l1_counts, color=COLOR_LEVEL1, label="Level 1")
    ax.bar(
        names,
        l2_counts,
        bottom=l1_counts,
        color=COLOR_LEVEL2,
        label="Level 2",
    )

    fast_bottom = [l1 + l2 for l1, l2 in zip(l1_counts, l2_counts)]
    ax.bar(
        names,
        fast_counts,
        bottom=fast_bottom,
        color=COLOR_DC_FAST,
        label="DC Fast",
    )

    ax.set_xlabel("Region")
    ax.set_ylabel("Total ports")
    ax.set_title(
        f"Port Mix Across Top {len(top)} Regions (by station count)"
    )
    ax.legend(loc="upper right")
    # Long region names rotate so they don't run into each other.
    plt.setp(ax.get_xticklabels(), rotation=45, ha="right")

    return fig


def plot_geographic_distribution(df):
    """
    Scatter plot of station locations colored by DC Fast capability.

    this function uses "longitude" as x and latitude" as y to give a rough,
    GIS-free map of New York that's good enough to see the obvious
    clusters (NYC, Long Island, the Hudson Valley corridor) and the
    obvious places in need of work.
    """
    required = {"latitude", "longitude", "dc_fast"}
    missing = required - set(df.columns)
    if missing:
        raise KeyError(
            f"DataFrame is missing required column(s): {sorted(missing)}."
        )

    fast_mask = df["dc_fast"] > 0
    fast = df[fast_mask]
    standard_only = df[~fast_mask]

    fig, ax = plt.subplots(figsize=(9, 8))
    # show slow chargers first so the DC-Fast layer is on top
    ax.scatter(
        standard_only["longitude"],
        standard_only["latitude"],
        s=12,
        alpha=0.5,
        color=COLOR_STANDARD_ONLY,
        label="Standard only (L1 / L2)",
    )
    ax.scatter(
        fast["longitude"],
        fast["latitude"],
        s=18,
        alpha=0.75,
        color=COLOR_FAST_CAPABLE,
        label="DC Fast capable",
    )

    ax.set_xlabel("Longitude")
    ax.set_ylabel("Latitude")
    ax.set_title("Geographic Distribution of NY EV Charging Stations")
    ax.legend(loc="upper left")
    # this makes the aspect ratio equal
    ax.set_aspect("equal", adjustable="datalim")

    return fig


if __name__ == "__main__":
    # testing to see if it works
    from pathlib import Path

    from src.analysis import build_regions, rank_regions
    from src.data_loader import clean_stations, load_stations

    csv_path = (
        Path(__file__).resolve().parent.parent
        / "data"
        / "alt_fuel_stations.csv"
    )

    print(f"Smoke test: loading {csv_path}")
    df = clean_stations(load_stations(csv_path))
    regions = build_regions(df, region_col="city")
    ranked = rank_regions(regions)
    print(f"  Built {len(regions)} regions, ranking has {len(ranked)} entries.")

    plot_top_n_underserved(ranked, n=10)
    plot_port_mix(regions, n=10)
    plot_geographic_distribution(df)

    print("Three figures generated")
    plt.show()
