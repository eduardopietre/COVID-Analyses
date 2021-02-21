import numpy as np
import pickle
import datetime
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib import animation

# SragYearCombiner.py must be runned before this script.
# "data/srag_deaths_by_year.data" must already exist.

def load_deaths_by_year(normalize_years=False, cumulative=False, path="data/srag_deaths_by_year.data"):
    with open(path, "rb") as file:
        years_info = pickle.load(file)

        if normalize_years:
            for info in years_info:
                info[1] = [datetime.date(month=date.month, day=date.day, year=2000) for date in info[1]]

        if cumulative:
            for info in years_info:
                info[2] = np.cumsum(np.array(info[2])).tolist()

        return years_info


def init():
    for line in lines:
        line.set_data([], [])
    return lines


def animate(i):
        global max_y, background_text, scatter_point

        for _ in range(repeat_per_iter):
            for ano_i in range(amount_of_years):
                if len(y_data[ano_i]) < len(years_info[ano_i][2]):
                    y = years_info[ano_i][2][len(y_data[ano_i])]
                    y_data[ano_i].append(y)

                    x = years_info[ano_i][1][len(x_data[ano_i])]
                    x_data[ano_i].append(x)

                    max_y = max(max_y, round(1.1 * max(y_data[ano_i])))
                    ax1.set_ylim(0, max_y)

                    if background_text:
                        background_text.remove()
                        background_text = None

                    background_text = ax1.text(
                        0.5, 0.5, s=years_info[ano_i][0], fontweight="bold", size=60, color="#d0d0d0",
                        ha="center",va="center", alpha=0.5, transform=ax1.transAxes, zorder=1
                    )

                    if scatter_point:
                        scatter_point.remove()
                        scatter_point = None

                    scatter_point = ax1.scatter(x, y, c="black", s=40, zorder=10)
                    break

        for lnum, line in enumerate(lines):
            line.set_data(x_data[lnum], y_data[lnum])

        return lines


if __name__ == "__main__":
    years_info = load_deaths_by_year(True, True)
    amount_of_years = len(years_info)
    repeat_per_iter = 5

    year_color = [
        "#b3b3ff", "#000099", "#66e0ff", "#008fb3",
        "#cc80ff", "#6b00b3", "#4dff4d", "#008000",
        "#cc9966", "#734d26", "#ff8566", "#ff3300",
    ]

    assert len(year_color) == amount_of_years

    wait_after_end = 150  # amount of frames to wait after end drawing.
    frames = round(sum([len(e[1]) for e in years_info]) / repeat_per_iter) + wait_after_end
    max_y = 100  # default value, will be updated.

    # --- Definitions end here. ---

    x_data = [[] for _ in range(amount_of_years)]
    y_data = [[] for _ in range(amount_of_years)]

    fig = plt.figure(figsize=(10, 10))
    ax1 = plt.axes(xlim=(years_info[-1][1][0], years_info[-1][1][-1]), ylim=(0, max_y)) 
    line, = ax1.plot([], [])

    plt.xlabel("Meses", fontsize=15)
    plt.ylabel("Óbitos", fontsize=15)

    lines = []
    for i in range(amount_of_years):
        lines.append(
            ax1.plot([], [], lw=2, label=years_info[i][0], c=year_color[i])[0]
        )

    background_text = None
    scatter_point = None

    ax1.yaxis.tick_right()
    ax1.yaxis.set_label_position("right")
    ax1.text(0.0, 1.05, "Óbitos* Cumulativos Por SRAG: 2009-2020", color="#4d4d4d", transform=ax1.transAxes, size=20)
    ax1.text(0.0, -0.1, "Fonte: DATASUS SRAG.", color="#4d4d4d", transform=ax1.transAxes, size=9)
    ax1.text(0.52, -0.1, "*Óbitos sem data ignorados.", color="#4d4d4d", transform=ax1.transAxes, size=9)
    ax1.xaxis.set_major_formatter(mdates.DateFormatter("%m"))
    ax1.legend(loc="upper left")

    anim = animation.FuncAnimation(fig, animate, init_func=init, frames=frames, interval=50, blit=False)

    # plt.show()
    writer = animation.writers["ffmpeg"](fps=20, bitrate=1800)
    anim.save("images/SragDeathsAnimation.mp4", writer=writer)
