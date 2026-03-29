import numpy as np
import matplotlib.pyplot as plt
from scipy.special import jn_zeros, jnp_zeros

C_CONST = 299792458  # speed of light in a vacuum [m/s]
EPS0 = 8.854187818814e-12  # permittivity of free space [F*m^-1]
MU0 = 4 * np.pi * 1e-7  # permeability of free space [H/m]
Z0 = 376.73031341259  # impedance of free space [Ohm]

def plot_dispersion_curves(kc_sq_tm, kc_sq_te, a, b=0, waveguide_type='rectangular'):
    plt.figure()

    if waveguide_type == "rectangular":
        te_labels = ["TE$_{10}$", "TE$_{01}$/TE$_{20}$", "TE$_{11}$/TM$_{11}$"]
        tm_labels = ["TE$_{21}$/TM$_{21}$", "TE$_{31}$/TM$_{31}$", "TE$_{12}$/TM$_{12}$"]

        kc_te = np.array([
            np.sqrt((1 * np.pi / a) ** 2 + (0 * np.pi / b) ** 2),
            np.sqrt((0 * np.pi / a) ** 2 + (1 * np.pi / b) ** 2),
            np.sqrt((1 * np.pi / a) ** 2 + (1 * np.pi / b) ** 2),
        ])

        kc_tm = np.array([
            np.sqrt((2 * np.pi / a) ** 2 + (1 * np.pi / b) ** 2),
            np.sqrt((3 * np.pi / a) ** 2 + (1 * np.pi / b) ** 2),
            np.sqrt((1 * np.pi / a) ** 2 + (2 * np.pi / b) ** 2),
        ])

    if waveguide_type == "circular":
        te_labels = ["TE$_{11}$", "TE$_{21}$", "TE$_{31}$"]
        tm_labels = ["TM$_{01}$", "TE$_{01}$/TM$_{11}$", "TM$_{21}$"]

        kc_te = np.array([
            jnp_zeros(1, 1)[0] / a,
            jnp_zeros(2, 1)[0] / a,
            jnp_zeros(3, 1)[0] / a,
        ])

        kc_tm = np.array([
            jn_zeros(0, 1)[0] / a,
            jn_zeros(1, 1)[0] / a,
            jn_zeros(2, 1)[0] / a,
        ])

    kc_all = np.concatenate((kc_te, kc_tm))
    kc_fem_all = np.concatenate((np.sqrt(kc_sq_te), np.sqrt(kc_sq_tm)))
    labels_all = te_labels + tm_labels

    ka_min = 0.95 * np.min(kc_all * a)
    ka_max = 2.0 * np.max(kc_all * a)
    ka = np.linspace(ka_min, ka_max, 500)

    for i in range(6):
        beta_over_k = np.sqrt(1 - (kc_all[i] * a / ka) ** 2)
        beta_over_k[ka < kc_all[i] * a] = np.nan

        line, = plt.plot(ka, beta_over_k, label=labels_all[i])

        ka_cutoff_num = kc_fem_all[i] * a
        ka_num = np.linspace(1.02 * ka_cutoff_num, ka_max, 10)
        beta_over_k_num = np.sqrt(1 - (ka_cutoff_num / ka_num) ** 2)

        plt.plot(
            ka_num,
            beta_over_k_num,
            marker="o",
            markersize=7,
            markerfacecolor="none",
            markeredgecolor=line.get_color(),
            linestyle="None"
        )

    plt.xlabel(r"$k a$")
    plt.ylabel(r"$\beta / k$")
    plt.suptitle(f"Dispersion Curves for a {waveguide_type.capitalize()} Waveguide:")
    plt.title("Analytical vs. FEM Results")
    plt.ylim(0, 1.05)
    plt.xlim(left=0)
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.savefig(f"figures/{waveguide_type}_dispersion_curves.png", dpi=300, bbox_inches="tight")
    plt.show()


def plot_mode_distribution(nodes, elements, field, mode_label, value_type='real', quantity_label=None, levels=40,
                           cmap='viridis', save_path=None):
