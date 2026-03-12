"""
plot.py - Renders a temperature forecast chart using matplotlib.
"""

import matplotlib.pyplot as plt


def plot_forecast(location: dict, daily: dict) -> None:
    """
    Display a line chart of the 7-day min/max temperature forecast.
    """
    dates = daily["time"]
    highs = daily["temperature_2m_max"]
    lows  = daily["temperature_2m_min"]

    # Use short date labels (e.g. "Mar 11") for readability
    labels = [f"{d[5:7]}/{d[8:]}" for d in dates]  # "YYYY-MM-DD" → "MM/DD"

    fig, ax = plt.subplots(figsize=(9, 4))

    ax.plot(labels, highs, marker="o", color="tomato",  label="High °C")
    ax.plot(labels, lows,  marker="o", color="steelblue", label="Low °C")

    # Shade the area between high and low
    ax.fill_between(labels, lows, highs, alpha=0.15, color="orange")

    # Annotate each point with its value
    for i, (h, l) in enumerate(zip(highs, lows)):
        ax.annotate(f"{h}°", (labels[i], h), textcoords="offset points",
                    xytext=(0, 6), ha="center", fontsize=8, color="tomato")
        ax.annotate(f"{l}°", (labels[i], l), textcoords="offset points",
                    xytext=(0, -12), ha="center", fontsize=8, color="steelblue")

    ax.set_title(f"7-Day Temperature Forecast — {location['name']}, {location['country']}")
    ax.set_ylabel("Temperature (°C)")
    ax.set_xlabel("Date")
    ax.legend()
    ax.grid(axis="y", linestyle="--", alpha=0.5)

    plt.tight_layout()
    plt.show()
