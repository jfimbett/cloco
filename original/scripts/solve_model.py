"""
Solve the delegated management model under a baseline parameterization and export
publication-quality figures to ../images/.

Figures:
  1) flow_performance.png     – Flow–performance curve (piecewise quadratic)
  2) ic_fee_curve.png         – IC fee φ(σ_d) across target volatility, by f2
  3) opt_sigma_vs_f2.png      – Optimal σ_d*(f2) from investor problem
    4) compstats_f2.png          – Optimal σ_d* and φ(σ_d*) vs f2
    5) compstats_scale.png       – Optimal σ_d* and φ(σ_d*) vs A0 and f1
    6) compstats_sharpe.png      – Optimal σ_d* and φ(σ_d*) vs Sharpe ratio S
    7) compstats_risk.png        – Optimal σ_d* and φ(σ_d*) vs γ and η

Notes:
- Uses Gaussian tail blocks. For Δ_quad we provide the exact formula from the appendix.
- Baseline parameters (calibrated to empirical literature): S=0.35, rf=0.0370, gamma=5, eta=3,
  A0=1 (normalized), f1=1.5, f2=25, with sweeps for comparative statics.
- Do not run from LaTeX; run separately after creating a conda env and installing requirements.
"""
from __future__ import annotations
import os
import math
from dataclasses import dataclass
from typing import Callable, Tuple

import numpy as np
from numpy.typing import NDArray
from scipy import optimize
import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn as sns

# --- Publication style ---
sns.set_theme(context="talk", style="whitegrid")
mpl.rcParams.update({
    "figure.dpi": 150,
    "savefig.dpi": 300,
    "font.family": "serif",
    "font.size": 12,
    "axes.titlesize": 14,
    "axes.labelsize": 12,
    "legend.fontsize": 11,
    "axes.spines.top": False,
    "axes.spines.right": False,
})

# --- Standard normal helpers ---
from math import erf, sqrt, exp, pi

def stdnorm_cdf(x: float) -> float:
    return 0.5 * (1.0 + erf(x / sqrt(2.0)))

def stdnorm_pdf(x: float) -> float:
    return (1.0 / sqrt(2.0 * pi)) * math.exp(-0.5 * x * x)

# --- Model structures ---
@dataclass
class Params:
    S: float = 0.35       # Sharpe ratio (annualized, baseline active mutual fund)
    rf: float = 0.0370    # risk-free rate (annual, 3.70% based on 3-month T-bill)
    gamma: float = 5.0    # investor risk aversion
    eta: float = 3.0      # manager risk aversion over fee revenue
    A0: float = 1.0       # initial AUM (normalized)
    f1: float = 1.5       # linear flow slope (annual, excess return in decimals)
    f2: float = 25.0      # convex flow parameter (annual, excess return in decimals)

    # Plotting domains
    sigma_min: float = 0.01
    sigma_max: float = 0.40

    # Grid resolution
    n_sigma: int = 200

# Comparative-statics sweep defaults
@dataclass
class SweepRanges:
    # Ranges automatically centered around baseline parameter values
    @staticmethod
    def from_params(params: Params) -> 'SweepRanges':
        return SweepRanges(
            f2_min=max(5.0, params.f2 * 0.2),
            f2_max=min(60.0, params.f2 * 2.4),
            f1_min=max(0.5, params.f1 * 0.33),
            f1_max=min(3.0, params.f1 * 2.0),
            S_min=0.10,
            S_max=1.00,
            gamma_min=2.0,
            gamma_max=10.0,
            eta_min=1.0,
            eta_max=8.0,
            A0_min=params.A0 * 0.5,
            A0_max=params.A0 * 3.0
        )
    
    f2_min: float = 5.0
    f2_max: float = 60.0
    f2_n: int = 16

    A0_min: float = 0.5
    A0_max: float = 3.0
    A0_n: int = 16

    f1_min: float = 0.5
    f1_max: float = 3.0
    f1_n: int = 16

    S_min: float = 0.10
    S_max: float = 1.00
    S_n: int = 19

    gamma_min: float = 2.0
    gamma_max: float = 10.0
    gamma_n: int = 17

    eta_min: float = 1.0
    eta_max: float = 8.0
    eta_n: int = 15

# Tail blocks

def C1(S: float) -> float:
    return (S*S + 1.0) * stdnorm_cdf(S) + S * stdnorm_pdf(S)

def tail_moments(S: float) -> Tuple[float, float, float]:
    """Return (P_plus, m1, m2) and we can extend when needed."""
    P_plus = stdnorm_cdf(S)
    m1 = stdnorm_pdf(S)
    m2 = P_plus - S * m1
    return P_plus, m1, m2

# Variance components from appendix

def moments_for_variance(S: float) -> Tuple[float, float, float]:
    E_X2I = C1(S)
    E_X3I = (S**3 + 3*S) * stdnorm_cdf(S) + (S**2 + 2) * stdnorm_pdf(S)
    E_X4I = (S**4 + 6*S**2 + 3) * stdnorm_cdf(S) + (S**3 + 5*S) * stdnorm_pdf(S)
    return E_X2I, E_X3I, E_X4I


def delta_quad(S: float, K: float, f2: float, sigma: float) -> float:
    E_X2I, E_X3I, E_X4I = moments_for_variance(S)
    cov_X_X2I = E_X3I - S * E_X2I
    var_X2I = E_X4I - E_X2I**2
    return 6.0 * K * f2 * sigma**2 * cov_X_X2I + 4.0 * f2**2 * sigma**3 * var_X2I

# Manager FOC components

def dEAdsigma(S: float, K: float, f2: float, sigma: float) -> float:
    return K * S + 2.0 * f2 * sigma * C1(S)

def dVAdsigma(S: float, K: float, f2: float, sigma: float) -> float:
    return 2.0 * K * K * sigma + delta_quad(S, K, f2, sigma)

# IC fee at a target sigma

def phi_ic_at_sigma(params: Params, sigma: float) -> float:
    K = params.A0 + params.f1
    num = dEAdsigma(params.S, K, params.f2, sigma)
    den = params.eta * dVAdsigma(params.S, K, params.f2, sigma)
    return num / den

# Investor utility and first-order condition components

def investor_UI(params: Params, sigma: float, phi: float) -> float:
    S, rf, gamma = params.S, params.rf, params.gamma
    # U_I = E[r_net] - (gamma/2) Var[r_net]
    # r_net = (1-phi) r - phi, r = rf + S sigma + sigma Z
    Er = rf + S * sigma
    Var_r = sigma * sigma
    Er_net = (1.0 - phi) * Er - phi
    Var_r_net = (1.0 - phi) ** 2 * Var_r
    return Er_net - 0.5 * gamma * Var_r_net


def phi_prime_sigma(params: Params, sigma: float) -> float:
    S, f2, eta = params.S, params.f2, params.eta
    K = params.A0 + params.f1
    # N, D, and derivatives
    N = dEAdsigma(S, K, f2, sigma)
    D = eta * dVAdsigma(S, K, f2, sigma)
    # derivatives w.r.t sigma
    dN = 2.0 * f2 * C1(S)
    dD = eta * (2.0 * K * K + (delta_quad(S, K, f2, sigma + 1e-6) - delta_quad(S, K, f2, sigma - 1e-6)) / (2e-6))
    return (dN * D - N * dD) / (D * D)


def affine_ic_phi(params: Params, sigma0: float) -> Tuple[float, float]:
    """Return (alpha, beta) for the local affine approximation
    phi(sigma) approx alpha + beta * sigma around sigma0.
    """
    phi0 = phi_ic_at_sigma(params, sigma0)
    slope = phi_prime_sigma(params, sigma0)
    alpha = phi0 - slope * sigma0
    beta = slope
    return alpha, beta


def G_of_sigma(params: Params, sigma: float) -> float:
    phi = phi_ic_at_sigma(params, sigma)
    S, gamma, rf = params.S, params.gamma, params.rf
    direct = (1.0 - phi) * S - gamma * (1.0 - phi) ** 2 * sigma
    phi_prime = phi_prime_sigma(params, sigma)
    contract_adj = (-(1.0 + rf + S * sigma) + gamma * (1.0 - phi) * sigma * sigma) * phi_prime
    return direct + contract_adj


def solve_investor_sigma(params: Params, bounds: Tuple[float, float] | None = None) -> float:
    a = params.sigma_min if bounds is None else bounds[0]
    b = params.sigma_max if bounds is None else bounds[1]
    # Ensure sign change; expand if needed
    Ga = G_of_sigma(params, a)
    Gb = G_of_sigma(params, b)
    expand = 0
    while Ga * Gb > 0 and expand < 5:
        b *= 1.25
        Gb = G_of_sigma(params, b)
        expand += 1
    root = optimize.bisect(lambda x: G_of_sigma(params, x), a, b, maxiter=200, xtol=1e-6)
    return root


def equilibrium_sigma_phi(params: Params) -> Tuple[float, float]:
    try:
        sigma_star = solve_investor_sigma(params)
        phi_star = phi_ic_at_sigma(params, sigma_star)
        return sigma_star, phi_star
    except Exception:
        return np.nan, np.nan

# --- Plotting ---

def ensure_images_dir() -> str:
    here = os.path.abspath(os.path.dirname(__file__))
    outdir = os.path.normpath(os.path.join(here, "..", "images"))
    os.makedirs(outdir, exist_ok=True)
    return outdir


def plot_flow_performance(params: Params, outdir: str) -> None:
    S, rf = params.S, params.rf
    # Use baseline convexity for the illustration
    f2_visual = params.f2
    sigma = 0.15  # illustrative vol for the shape
    z = np.linspace(-3.5, 3.5, 400)
    x = S + z
    r_minus_rf = sigma * x
    F = np.where(x >= 0.0, params.f1 * r_minus_rf + f2_visual * r_minus_rf**2, params.f1 * r_minus_rf)

    fig, ax = plt.subplots(figsize=(7,4.2))
    ax.plot(r_minus_rf, F, color="#1b9e77", lw=2.5)
    ax.axvline(0, color="#555", lw=1.2, ls="--")
    ax.set_title("Flow–performance relation (piecewise quadratic)")
    ax.set_xlabel("Excess return r - r_f")
    ax.set_ylabel("Flow F(r)")
    ax.annotate("Quadratic kicker active", xy=(0.03, F[x>=0].mean()), xytext=(0.08, F.max()*0.6),
                arrowprops=dict(arrowstyle="->", lw=1.0, color="#333"), color="#333")
    sns.despine()
    fig.tight_layout()
    fig.savefig(os.path.join(outdir, "flow_performance.png"))
    plt.close(fig)


def plot_ic_fee_curve(params: Params, outdir: str) -> None:
    sigmas = np.linspace(params.sigma_min, params.sigma_max, params.n_sigma)
    fig, ax = plt.subplots(figsize=(7,4.2))
    # Plot only the baseline curve (no sweep over f2)
    p = Params(**params.__dict__)
    phi_vals = np.array([phi_ic_at_sigma(p, s) for s in sigmas])
    ax.plot(sigmas, phi_vals, lw=2.2, color="#2979ff", label=fr"baseline $f_2={p.f2:.2f}$")
    # Overlay the affine approximation for the baseline parameterization (f2 as in params)
    sigma0 = 0.10  # 10% reference target
    p_base = Params(**params.__dict__)
    alpha, beta = affine_ic_phi(p_base, sigma0)
    phi_affine = alpha + beta * sigmas
    ax.plot(sigmas, phi_affine, lw=2.0, ls="--", color="#333333",
            label=r"Affine approx (baseline)")
    ax.set_title("IC fee $\\phi(\\sigma_d)$ across target volatility")
    ax.set_xlabel(r"Target volatility $\sigma_d$")
    ax.set_ylabel(r"IC fee $\phi$")
    ax.legend(frameon=True)
    sns.despine()
    fig.tight_layout()
    fig.savefig(os.path.join(outdir, "ic_fee_curve.png"))
    plt.close(fig)


def plot_opt_sigma_vs_f2(params: Params, outdir: str) -> None:
    sweeps = SweepRanges.from_params(params)
    f2_grid = np.linspace(sweeps.f2_min, sweeps.f2_max, sweeps.f2_n)
    sigmas = np.array([equilibrium_sigma_phi(Params(**{**params.__dict__, "f2": float(f2)}))[0]
                       for f2 in f2_grid])

    fig, ax = plt.subplots(figsize=(7,4.2))
    ax.plot(f2_grid, sigmas, marker="o", lw=2.2, color="#d95f02")
    ax.set_title(r"Optimal target volatility $\sigma_d^*$ vs convexity $f_2$")
    ax.set_xlabel(r"Convexity $f_2$")
    ax.set_ylabel(r"Optimal $\sigma_d^*$")
    sns.despine()
    fig.tight_layout()
    fig.savefig(os.path.join(outdir, "opt_sigma_vs_f2.png"))
    plt.close(fig)


def plot_compstats_f2(params: Params, outdir: str) -> None:
    sweeps = SweepRanges.from_params(params)
    f2_grid = np.linspace(sweeps.f2_min, sweeps.f2_max, sweeps.f2_n)
    sigma_star = []
    phi_star = []
    for f2 in f2_grid:
        s, p = equilibrium_sigma_phi(Params(**{**params.__dict__, "f2": float(f2)}))
        sigma_star.append(s)
        phi_star.append(p)
    sigma_star = np.array(sigma_star)
    phi_star = np.array(phi_star)

    fig, axes = plt.subplots(1, 2, figsize=(10.5, 4.0), sharex=True)
    ax1, ax2 = axes
    ax1.plot(f2_grid, sigma_star, marker="o", lw=2.0, color="#d95f02")
    ax1.set_title(r"Optimal target $\sigma_d^*$ vs $f_2$")
    ax1.set_xlabel(r"Convexity $f_2$")
    ax1.set_ylabel(r"$\sigma_d^*$")

    ax2.plot(f2_grid, phi_star, marker="o", lw=2.0, color="#1b9e77")
    ax2.set_title(r"IC fee at optimum $\phi(\sigma_d^*)$ vs $f_2$")
    ax2.set_xlabel(r"Convexity $f_2$")
    ax2.set_ylabel(r"$\phi(\sigma_d^*)$")

    sns.despine()
    fig.tight_layout()
    fig.savefig(os.path.join(outdir, "compstats_f2.png"))
    plt.close(fig)


def plot_compstats_scale(params: Params, outdir: str) -> None:
    sweeps = SweepRanges.from_params(params)
    A0_grid = np.linspace(sweeps.A0_min, sweeps.A0_max, sweeps.A0_n)
    f1_grid = np.linspace(sweeps.f1_min, sweeps.f1_max, sweeps.f1_n)

    sigma_A0 = []
    phi_A0 = []
    for A0 in A0_grid:
        s, p = equilibrium_sigma_phi(Params(**{**params.__dict__, "A0": float(A0)}))
        sigma_A0.append(s)
        phi_A0.append(p)

    sigma_f1 = []
    phi_f1 = []
    for f1 in f1_grid:
        s, p = equilibrium_sigma_phi(Params(**{**params.__dict__, "f1": float(f1)}))
        sigma_f1.append(s)
        phi_f1.append(p)

    fig, axes = plt.subplots(2, 2, figsize=(10.5, 7.2))
    (ax11, ax12), (ax21, ax22) = axes

    ax11.plot(A0_grid, sigma_A0, marker="o", lw=2.0, color="#377eb8")
    ax11.set_title(r"$\sigma_d^*$ vs $A_0$")
    ax11.set_xlabel(r"Initial AUM $A_0$")
    ax11.set_ylabel(r"$\sigma_d^*$")

    ax21.plot(A0_grid, phi_A0, marker="o", lw=2.0, color="#4daf4a")
    ax21.set_title(r"$\phi(\sigma_d^*)$ vs $A_0$")
    ax21.set_xlabel(r"Initial AUM $A_0$")
    ax21.set_ylabel(r"$\phi(\sigma_d^*)$")

    ax12.plot(f1_grid, sigma_f1, marker="o", lw=2.0, color="#377eb8")
    ax12.set_title(r"$\sigma_d^*$ vs $f_1$")
    ax12.set_xlabel(r"Linear flow slope $f_1$")
    ax12.set_ylabel(r"$\sigma_d^*$")

    ax22.plot(f1_grid, phi_f1, marker="o", lw=2.0, color="#4daf4a")
    ax22.set_title(r"$\phi(\sigma_d^*)$ vs $f_1$")
    ax22.set_xlabel(r"Linear flow slope $f_1$")
    ax22.set_ylabel(r"$\phi(\sigma_d^*)$")

    sns.despine()
    fig.tight_layout()
    fig.savefig(os.path.join(outdir, "compstats_scale.png"))
    plt.close(fig)


def plot_compstats_sharpe(params: Params, outdir: str) -> None:
    sweeps = SweepRanges.from_params(params)
    S_grid = np.linspace(sweeps.S_min, sweeps.S_max, sweeps.S_n)
    sigma_star = []
    phi_star = []
    for S in S_grid:
        s, p = equilibrium_sigma_phi(Params(**{**params.__dict__, "S": float(S)}))
        sigma_star.append(s)
        phi_star.append(p)
    sigma_star = np.array(sigma_star)
    phi_star = np.array(phi_star)

    fig, axes = plt.subplots(1, 2, figsize=(10.5, 4.0), sharex=True)
    ax1, ax2 = axes
    ax1.plot(S_grid, sigma_star, marker="o", lw=2.0, color="#756bb1")
    ax1.set_title(r"Optimal target $\sigma_d^*$ vs Sharpe $S$")
    ax1.set_xlabel(r"Sharpe ratio $S$")
    ax1.set_ylabel(r"$\sigma_d^*$")

    ax2.plot(S_grid, phi_star, marker="o", lw=2.0, color="#e6550d")
    ax2.set_title(r"IC fee at optimum $\phi(\sigma_d^*)$ vs $S$")
    ax2.set_xlabel(r"Sharpe ratio $S$")
    ax2.set_ylabel(r"$\phi(\sigma_d^*)$")

    sns.despine()
    fig.tight_layout()
    fig.savefig(os.path.join(outdir, "compstats_sharpe.png"))
    plt.close(fig)


def plot_compstats_risk(params: Params, outdir: str) -> None:
    sweeps = SweepRanges.from_params(params)
    gamma_grid = np.linspace(sweeps.gamma_min, sweeps.gamma_max, sweeps.gamma_n)
    eta_grid = np.linspace(sweeps.eta_min, sweeps.eta_max, sweeps.eta_n)

    sigma_gamma = []
    phi_gamma = []
    for gamma in gamma_grid:
        s, p = equilibrium_sigma_phi(Params(**{**params.__dict__, "gamma": float(gamma)}))
        sigma_gamma.append(s)
        phi_gamma.append(p)

    sigma_eta = []
    phi_eta = []
    for eta in eta_grid:
        s, p = equilibrium_sigma_phi(Params(**{**params.__dict__, "eta": float(eta)}))
        sigma_eta.append(s)
        phi_eta.append(p)

    fig, axes = plt.subplots(2, 2, figsize=(10.5, 7.2))
    (ax11, ax12), (ax21, ax22) = axes

    ax11.plot(gamma_grid, sigma_gamma, marker="o", lw=2.0, color="#3182bd")
    ax11.set_title(r"$\sigma_d^*$ vs investor risk aversion $\gamma$")
    ax11.set_xlabel(r"Investor risk aversion $\gamma$")
    ax11.set_ylabel(r"$\sigma_d^*$")

    ax21.plot(gamma_grid, phi_gamma, marker="o", lw=2.0, color="#31a354")
    ax21.set_title(r"$\phi(\sigma_d^*)$ vs $\gamma$")
    ax21.set_xlabel(r"Investor risk aversion $\gamma$")
    ax21.set_ylabel(r"$\phi(\sigma_d^*)$")

    ax12.plot(eta_grid, sigma_eta, marker="o", lw=2.0, color="#3182bd")
    ax12.set_title(r"$\sigma_d^*$ vs manager risk aversion $\eta$")
    ax12.set_xlabel(r"Manager risk aversion $\eta$")
    ax12.set_ylabel(r"$\sigma_d^*$")

    ax22.plot(eta_grid, phi_eta, marker="o", lw=2.0, color="#31a354")
    ax22.set_title(r"$\phi(\sigma_d^*)$ vs $\eta$")
    ax22.set_xlabel(r"Manager risk aversion $\eta$")
    ax22.set_ylabel(r"$\phi(\sigma_d^*)$")

    sns.despine()
    fig.tight_layout()
    fig.savefig(os.path.join(outdir, "compstats_risk.png"))
    plt.close(fig)


def plot_affine_approximation_quality(params: Params, outdir: str) -> None:
    """Plot average absolute error (%) of affine approximation vs f2 to assess approximation quality."""
    # Use range around baseline f2 value (±40% of baseline)
    sweeps = SweepRanges.from_params(params)
    f2_values = np.linspace(sweeps.f2_min, sweeps.f2_max, 16)
    
    mae_pct_list = []
    
    for f2 in f2_values:
        p = Params(**{**params.__dict__, "f2": float(f2)})
        
        # Get optimal sigma_d for this f2
        try:
            sigma_opt = solve_investor_sigma(p)
        except Exception:
            mae_pct_list.append(np.nan)
            continue
        
        # Evaluate approximation in ±5% range around optimal sigma_d
        sigma_grid = np.linspace(sigma_opt * 0.95, sigma_opt * 1.05, 50)
        
        # Get exact IC fees
        phi_exact = np.array([phi_ic_at_sigma(p, s) for s in sigma_grid])
        
        # Get affine approximation around optimal sigma_d
        alpha, beta = affine_ic_phi(p, sigma_opt)
        phi_affine = alpha + beta * sigma_grid
        
        # Compute average absolute error as percentage
        mae_pct = np.mean(np.abs((phi_exact - phi_affine) / phi_exact)) * 100.0
        mae_pct_list.append(mae_pct)
    
    mae_pct_list = np.array(mae_pct_list)
    
    fig, ax = plt.subplots(figsize=(7, 4.2))
    ax.plot(f2_values, mae_pct_list, marker="o", lw=2.2, color="#e7298a")
    ax.set_title(r"Quality of affine approximation vs convexity $f_2$")
    ax.set_xlabel(r"Convexity parameter $f_2$")
    ax.set_ylabel(r"Average absolute error (\%)")
    ax.axvline(params.f2, color="#555", lw=1.2, ls="--", label=f"Baseline $f_2={params.f2}$")
    ax.legend(frameon=True)
    # Set y-axis limit with some headroom
    ymax = np.nanmax(mae_pct_list)
    ax.set_ylim(0, ymax * 1.15)
    sns.despine()
    fig.tight_layout()
    fig.savefig(os.path.join(outdir, "affine_approx_quality.png"))
    plt.close(fig)


def main():
    params = Params()
    outdir = ensure_images_dir()

    plot_flow_performance(params, outdir)
    plot_ic_fee_curve(params, outdir)
    plot_opt_sigma_vs_f2(params, outdir)
    plot_compstats_f2(params, outdir)
    plot_compstats_scale(params, outdir)
    plot_compstats_sharpe(params, outdir)
    plot_compstats_risk(params, outdir)
    plot_affine_approximation_quality(params, outdir)

    print(f"Figures exported to: {outdir}")


if __name__ == "__main__":
    main()
