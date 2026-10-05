/-
Worked example: the mean-variance portfolio problem.

Paper statement (LaTeX label `prop:mv-optimum`):
  An investor with risk aversion γ > 0 chooses the risky share x to maximise
  U(x) = μ x − (γ σ² / 2) x², with σ² > 0. The unique maximiser is x* = μ / (γ σ²),
  and x* is increasing in μ and decreasing in γ (for μ > 0).

Each paper result gets one Lean declaration; its name goes in `lean/ledger.json`.
-/
import Mathlib

namespace Cloco.Examples.MeanVariance

/-- Mean-variance utility of holding share `x` in the risky asset. -/
noncomputable def utility (μ γ σ2 x : ℝ) : ℝ := μ * x - γ * σ2 / 2 * x ^ 2

/-- The candidate optimum `x* = μ / (γ σ²)`. -/
noncomputable def optShare (μ γ σ2 : ℝ) : ℝ := μ / (γ * σ2)

/-- `prop:mv-optimum` (i): `x*` maximises utility, strictly. -/
theorem optShare_isMax {μ γ σ2 : ℝ} (hγ : 0 < γ) (hσ : 0 < σ2) (x : ℝ) (hx : x ≠ optShare μ γ σ2) :
    utility μ γ σ2 x < utility μ γ σ2 (optShare μ γ σ2) := by
  have hk : 0 < γ * σ2 := mul_pos hγ hσ
  -- U(x*) − U(x) = (γσ²/2)(x − x*)², and the square is positive off the optimum.
  have key : utility μ γ σ2 (optShare μ γ σ2) - utility μ γ σ2 x
      = γ * σ2 / 2 * (x - optShare μ γ σ2) ^ 2 := by
    unfold utility optShare
    field_simp
    ring
  have hsq : 0 < (x - optShare μ γ σ2) ^ 2 := by
    have : x - optShare μ γ σ2 ≠ 0 := sub_ne_zero.mpr hx
    positivity
  have : 0 < γ * σ2 / 2 * (x - optShare μ γ σ2) ^ 2 := by positivity
  linarith

/-- `prop:mv-optimum` (ii): the optimal share is increasing in the expected excess return. -/
theorem optShare_strictMono_mu {γ σ2 : ℝ} (hγ : 0 < γ) (hσ : 0 < σ2) :
    StrictMono (fun μ => optShare μ γ σ2) := by
  intro a b hab
  exact div_lt_div_of_pos_right hab (mul_pos hγ hσ)

/-- `prop:mv-optimum` (iii): for `μ > 0`, the optimal share is decreasing in risk aversion. -/
theorem optShare_antitone_gamma {μ σ2 : ℝ} (hμ : 0 < μ) (hσ : 0 < σ2) :
    StrictAntiOn (fun γ => optShare μ γ σ2) (Set.Ioi 0) := by
  intro a ha b hb hab
  simp only [Set.mem_Ioi] at ha hb
  exact div_lt_div_of_pos_left hμ (mul_pos ha hσ) (mul_lt_mul_of_pos_right hab hσ)

end Cloco.Examples.MeanVariance
