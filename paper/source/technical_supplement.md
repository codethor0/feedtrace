---
title: "FeedTrace Technical Supplement: Data, Models, and Reproducibility"
author: "Isaac Thor"
---

# FeedTrace Technical Supplement: Data, Models, and Reproducibility

This supplement provides the methodological record for the paper "FeedTrace: Reach, Ranking, and Black Visibility in 1,174 LinkedIn Posts": data dictionary, sample construction, exact transformations, model equations, estimation settings, seeds, sensitivity tables, software versions, execution commands, and the post-validation race-analysis plan. The accompanying sanitized archive supports direct reproduction of the corrected R9 non-race predictive benchmark and verification of aggregate outputs and frozen race specifications. Broader analysis code and privacy-sensitive source data remain in the private project repository and are not represented as independently executable from the public research archive.

## S1. Scope and sample construction

The study window is September 6, 2025, through July 18, 2026. The inventory contains 1,192 records from one LinkedIn account: 1,174 creator-owned original posts and 18 reposts. Detailed creator analytics were collected on July 18, 2026, for a purposefully selected pilot; analytics were retrievable for 29 originals, while the 2 repost records tested returned no creator analytics because the account was not the original author.

Sample construction for the inferential dataset applies three filters in order: (1) keep records flagged `is_original_post`; (2) keep records with a parseable `created_at` timestamp (one original lacks a timestamp and is excluded only from time-indexed analyses, which therefore use n = 1,173 weekly/monthly observations aggregated from posts with dates; all cross-sectional analyses use n = 1,174); (3) keep records with strictly positive `feed_impressions`. All 1,174 originals satisfy filter 3.

Reposts are excluded because the distribution process for reshared third-party content is not comparable to original-post distribution and no creator analytics exist for them.

Inventory reconciliation: 1,192 total records = 1,174 originals + 18 reposts; 1,174 originals = 29 with detailed analytics + 1,145 without; 1,174 texts = 29 verified full text + 1,145 possibly truncated previews; 459 race-review candidates were queued by the automated screen, 0 have been human-approved, and 0 structured moderation records exist in the archive. Every one of these counts appears verbatim in the paper's Table 2, and any future data collection that changes them requires a new revision with a new frozen checkpoint rather than an in-place edit.

## S2. Data dictionary

Processed analysis fields from the private analysis table (withheld; public sanitized subset is `data/sanitized/R9_SANITIZED_NON_RACE_ANALYTIC_DATA.csv`):

| Field | Type | Definition |
|---|---|---|
| post_id | string | De-identified stable post identifier |
| created_at | timestamp (UTC) | Publication time parsed from platform export |
| is_original_post | bool | True for creator-owned originals |
| feed_impressions | int | Recorded impressions from the feed-level snapshot |
| feed_impressions_post_age_hours | float | Hours between publication and the impression snapshot |
| post_type | enum | image, text, video, article, document, poll |
| has_image / has_video / has_document / has_poll | bool | Format flags |
| has_external_link | bool | Link presence; exactly collinear with article format in this sample |
| word_count | int | Words in available analysis text (preview for 1,145 posts, verified full text for 29) |
| hashtag_count | int | Hashtags in available analysis text |

Detailed-analytics fields were captured in a private creator-analytics table (withheld): `analytics_impressions`, `members_reached`, `followers_reached` (percent), `nonfollowers_reached` (percent, the out-of-network share), `reactions`, `comments`, `reposts`, `saves`, `profile_views`, `new_followers`, `link_clicks`, plus `analytics_available` and `analytics_unavailable_reason`. Field-level availability and exact denominators are tabulated in `data/aggregate/detailed_analytics/DETAILED_ANALYTICS_FIELD_COVERAGE.csv`; members reached and out-of-network share are available for 28 of 29 pilot originals, and every statistic in the paper uses the field-specific denominator.

Date handling: all timestamps are stored in UTC. Monthly aggregation uses calendar-month period ends; weekly aggregation uses ISO weeks ending Sunday. Post age is computed at snapshot time, not at analysis time. One original post lacks a parseable timestamp; it is retained in all cross-sectional analyses (n = 1,174) and excluded from time-indexed aggregation only. Missing numeric covariates (word count, hashtag count) are set to zero only where the underlying text field is verifiably empty; otherwise the record's text-derived fields come from the preview capture.

## S2.1. Collection provenance

Feed-level impression counts and post metadata were captured from the account's own activity views in a logged-in browser session, exported as structured JSON with capture timestamps, and parsed deterministically into private processed analysis tables; the parser records, per post, the capture time used to compute `feed_impressions_post_age_hours`. Detailed creator analytics were read from the per-post analytics screens LinkedIn exposes to the post author, captured on July 18, 2026. Two repost records were attempted and returned no creator analytics because the account was not the original author, which is the source of the "2 additional pilot repost records without creator analytics" inventory line. No scraping of other members' content occurred; every record originates from the account owner's own views of their own posts. Raw captures and private processed tables are retained privately and are excluded from the public repository (S16). The public package exposes only the sanitized non-race analytic table and aggregate result tables.

## S3. Transformations, estimands, and model equations

The non-race pipeline models ln(y) on the strictly positive impression counts. The frozen race pipeline (executed earlier and not rerun) modeled ln(1 + y). Both transformations are recorded per model in the private model-specification registry; no caption or table in the paper labels a model with a transformation other than the one in its source code. For log-scale coefficients b, percentage effects are reported as 100(exp(b) - 1), and confidence limits are transformed by the same monotone map. This back-transformation targets the conditional geometric mean, not the conditional arithmetic mean; because the residual variance may differ across groups, no smearing correction is applied, and no arithmetic-mean effect is claimed anywhere in the paper.

**Primary adjusted regression (non-race).** For post i with impressions y_i, age a_i in hours, word count w_i, hashtag count h_i, and format flags F_i (image, video, document; text is the reference):

ln(y_i) = b0 + b1 ln(1 + a_i) + b2 w_i + b3 h_i + F_i'g + e_i

estimated by OLS with HC3 covariance, and re-estimated with Newey-West HAC (10 lags) and a moving-block bootstrap for dependence-aware uncertainty (S8).

**Frozen race regression.** ln(1 + y_i) = b0 + d G_i + b1 ln(1 + a_i) + b2 w_i + b3 h_i + L_i + F_i'g + e_i, where G_i is the group indicator and L_i the external-link flag; variants add month fixed effects and format-by-month structure. d is reported as 100(exp(d) - 1).

**Quantile regressions.** For quantile tau, coefficients minimize the sum of the check loss rho_tau(ln y_i - x_i'b), rho_tau(u) = u(tau - 1{u < 0}); asymptotic covariance via the statsmodels quantreg default (kernel-based sparsity estimate).

**Logistic threshold models (frozen).** logit P(y_i >= t) = x_i'b for t equal to the account median and p90; reported as odds ratios.

**Negative binomial (frozen sensitivity).** NB GLM with log link and variance mu + alpha mu^2, alpha fixed at 1 by software default. Non-race dispersion diagnostics (S6.1) reject that mean-variance assumption, which is why the model is labeled a historical sensitivity result.

**Gaussian mixture on logs.** Density f(z) = sum_k w_k phi(z; m_k, s_k^2) on z = ln y, fitted by EM; the posterior probability that post i belongs to component k is w_k phi(z_i; m_k, s_k^2) / f(z_i).

**Concentration.** Primary quantiles use linear interpolation (NumPy `quantile`, method "linear"). The Gini coefficient is computed on sorted values s as (n + 1 - 2 sum(cumsum(s))/sum(s)) / n. Top-p shares use the smallest integer k with k at least n p. The effective number of equal posts is the inverse Herfindahl index 1 / sum(w_i^2) with w_i the impression shares. The Lorenz curve plots cumulative impression share against cumulative post share after ascending sort.

**Tail estimators.** With order statistics y_(1) <= ... <= y_(n), the Hill estimator at k upper-order observations is the reciprocal of the mean of ln(y_(n-i+1)/y_(n-k)) for i = 1..k; Pickands uses quantile spacings; both are evaluated on the grid in S5 and reported as threshold-instability diagnostics.

**Agreement.** Bland-Altman on logs: differences d_i = ln(analytics_i) - ln(feed_i) against means (ln(analytics_i) + ln(feed_i))/2; limits of agreement mean(d) plus or minus 1.96 SD(d).

**Conformal intervals.** R8's same-sample training-residual intervals were not valid split conformal and are withdrawn. R9 uses disjoint chronological training, calibration, and test periods. Models are fit only on training observations; absolute residual scores are computed only on calibration observations; and a symmetric 90 percent interval uses the finite-sample order statistic \(\lceil(n_c+1)(1-\alpha)\rceil\) with \(\alpha=0.10\). Coverage and width are evaluated only on the untouched test period. The algorithm has a valid split and quantile construction, but the usual distribution-free marginal guarantee additionally requires exchangeability between calibration and test observations, which may fail in this serially dependent chronological series.

## S4. Bootstrap procedures

All bootstraps resample posts (the resampling unit) with replacement, iid, unless stated otherwise.

Primary quantile and concentration intervals (paper Table 4): nonparametric percentile bootstrap, 2,000 replicates, seed 42 in the frozen r5 pipeline; quantile interpolation "linear"; percentile method (2.5th and 97.5th percentile of replicate estimates). A second valid run with seed 20260719 reproduces every interval to displayed precision except the extreme p99 upper limit (5,966 versus 11,394), which is expected for an extreme quantile whose replicate distribution is driven by a handful of tail observations. The percentile method with the frozen seed was designated primary before the comparison; both runs are recorded here, and the divergence is disclosed in the paper. BCa was considered and not used as primary because the acceleration constant is estimated from a jackknife that is itself dominated by the maximum observation.

Stratum-level concentration intervals: 1,000 replicates per stratum, seed 20260719 (file `data/aggregate/concentration/CONCENTRATION_BY_STRATUM.csv`; strata with n under 20 not estimated).

Dependence-aware uncertainty (Section S8): moving-block bootstrap in posting order, block length 25, 1,000 replicates, seed 20260719.

Permutation tests: the pilot top-quartile out-of-network contrast uses 5,000 label permutations, seed 20260719, two-sided exceedance of the observed absolute median difference.

## S5. Distribution and tail models

Candidate families fitted by maximum likelihood on the original scale: lognormal, log-logistic, Weibull, gamma, Pareto, generalized Pareto (full-data), Burr XII, and Fréchet where numerically stable. For each family the registry records parameter estimates, exact estimated-parameter counts, log likelihood, AIC, AICc, BIC, naive and parametric-bootstrap-calibrated Kolmogorov-Smirnov statistics (1,000 bootstrap replicates refitting under the null), Cramér-von Mises statistics, Anderson-Darling PIT statistics, and 5-fold cross-validated held-out log likelihood.

Key values: Burr XII attains the best AICc (12,565) and best held-out log likelihood but calibrated KS p = 0.020; log-logistic AICc 12,616, calibrated KS p = 0.005; lognormal AICc 12,812, calibrated KS p = 0.001. Equation 1 of the paper gives the lognormal quantile function; the body-fit parameters mu = 3.77, sigma = 0.82 imply Q(0.95) of about 167 against the empirical 254 (bootstrap CI 217 to 327), the underprediction stated in the paper.

Tail diagnostics: Hill estimator over upper-order counts k in {25, 50, 75, 100, 150, 200, 300} yields 1.59, 1.15, 1.04, 0.88, 0.84, 0.77, 0.76; Pickands estimates over the same grid range 0.83 to 0.27; the mean-excess function increases with threshold. Generalized-Pareto shape estimates over the same thresholds are threshold-dependent. No return level beyond the observed range is reported anywhere in the paper.

## S6. Mixture models

Gaussian mixtures on ln(y) with k in {1, 2, 3}: EM with 20 random initializations (10 for the sensitivity fits), maximum 500 iterations, tolerance 1e-3, seed 20260719, full convergence verified for all fits. Exact parameter counts: 2, 5, 8. Diagnostics per k (file `data/aggregate/mixture_models/MIXTURE_DIAGNOSTICS.csv`): log likelihood, AIC, BIC, 5-fold cross-validated held-out log likelihood (KFold shuffle, seed 20260719), posterior entropy (mean over posts of the entropy of the component posterior, nats), weights, component log means, component log SDs.

Selection logic: k = 2 and k = 3 both dominate k = 1 on all criteria; k = 3 improves BIC (2,920 versus 2,938) and held-out likelihood (-1.227 versus -1.247) over k = 2, at the cost of higher assignment entropy (0.42 versus 0.26) and a 2.6 percent component centered at log mean 7.24. The paper uses k = 2 as the descriptive reference and reports the k = 3 diagnostics. Standard likelihood-ratio and Vuong-type tests are not used because mixture comparisons violate the regularity conditions those tests require (boundary parameters, label non-identifiability); selection rests on information criteria with exact counts, held-out likelihood, and stability.

Stability: with the maximum excluded, BIC(k=2) = 2,931 versus BIC(k=1) = 3,145; with the top 1 percent excluded (n = 1,162), 2,738 versus 2,776. Posterior high-regime probabilities by month, format, and age stratum, with group sizes, are retained in the private frozen analysis checkpoint under mixture posterior strata; the format-level means are: article 0.210 (n = 88), document 0.174 (n = 5, sparse), video 0.125 (n = 116), text 0.116 (n = 366), image 0.111 (n = 597), poll 0.049 (n = 2, sparse); age-stratum means are 0.156 (young half) and 0.087 (mature half).

## S6.1. Count-model dispersion diagnostics (non-race)

Poisson regression of impressions on the standard covariates yields a Pearson-statistic overdispersion ratio of about 14,385 and a variance-to-mean ratio of about 22,125, both catastrophically far from the Poisson assumption. The Cameron-Trivedi auxiliary regression estimates alpha of about 50 under the quadratic variance specification, and full NB2 maximum likelihood estimates alpha = 1.44 (converged). Two implications follow. First, any count model with dispersion fixed at 1 (the frozen race NB sensitivity model) imposes a mean-variance relationship the data reject; its estimates are retained for the frozen record but are not preferred. Second, even estimated-dispersion count models are dominated in fit by log-scale linear models for this outcome, which is why the paper's preferred specifications are log-scale.

## S6.2. Concentration decomposition values

From `data/aggregate/concentration/CONCENTRATION_BY_STRATUM.csv` (Gini, bootstrap 95 percent CI, top 1 percent share; strata under 20 posts not estimated): all posts 0.799 [0.645, 0.872], 63.5 percent; mature half 0.667 [0.423, 0.786], 47.3 percent; young half 0.826 [0.625, 0.898], 65.1 percent; before June 2026 (n = 937) 0.808 [0.530, 0.895], 68.7 percent; June 2026 onward (n = 236) 0.700 [0.454, 0.790], 45.8 percent; image (n = 597) 0.849 [0.619, 0.915]; text (n = 366) 0.667 [0.458, 0.775]; video (n = 116) 0.431 [0.352, 0.495]; article (n = 88) 0.842 [0.503, 0.899]. Monthly Gini ranges from 0.358 (April 2026, n = 70) to 0.913 (May 2026, n = 131). Effective post counts range from 2.2 (May 2026) to 54.1 (video format).

## S7. Change points and structural breaks

Monthly series: mean of ln(y) per calendar month, months with at least 3 posts (11 aggregates). Single break selected by variance-minimizing split (the frozen r4/r5 method); location 2026-05-31; bootstrap stability 95.6 percent over 1,000 post-level resamples; identical location with the top 1 percent excluded and with the maximum excluded.

Weekly series: median, mean, and p90 of ln(y) per ISO week with at least 3 posts (44, 44, and 42 points). PELT (l2 cost, minimum segment 3, penalty var(y) * ln(n)) and binary segmentation (2 breaks) as a sensitivity method. Detected: week ending 2026-05-17 (median and mean series); p90 series breaks earlier (2026-04-26). Placebo permutations (200 shuffles per series) find at least one PELT break in 31 percent of shuffles, so weekly-level detection is weak evidence by itself; this is stated in the paper.

Estimand reconciliation (paper Section 16): descriptive factor exp(4.77 - 3.76) = 2.74 from unadjusted monthly aggregate means; adjusted factor 1.59 (95 percent CI 1.22 to 2.06, p = 0.0005) from post-level OLS of ln(y) on an after-2026-06-01 indicator plus log-age, word count, hashtag count, and format flags with HC3 errors. A segmented model at the March 12, 2026 announcement date gives 1.21 (95 percent CI 0.99 to 1.48, p = 0.057). Placebo break dates in 2025 produce no comparable shift.

## S8. Residual dependence and dependence-aware inference

Primary non-race model: OLS of ln(y) on log1p(age hours), word count, hashtag count, image, video, and document flags; HC3 covariance; n = 1,174. Residuals in posting order show lag-1 autocorrelation 0.288 (PACF lag 1: 0.288) and Ljung-Box statistics 212 (5 lags), 272 (10), 358 (20), all p below 1e-40. Consequences quantified for the log-age coefficient (-0.326): HC3 SE 0.024; Newey-West HAC SE with 10 lags 0.045; moving-block bootstrap (block 25, 1,000 reps) 95 percent interval -0.50 to -0.27. Non-race conclusions in the paper rely on the dependence-aware intervals where the distinction matters. Frozen race intervals are not recomputed; the paper flags that their nominal precision does not account for serial dependence.

## S9. Measurement-age analyses

Age distribution at snapshot: min 9.4 hours, quartiles 1,502 / 4,000 / 5,132, max 7,573. Nonlinear fit: natural cubic spline basis on log age (5 df, patsy `cr`), plus format flags; R-squared 0.266 versus 0.200 linear. Interactions: log-age by recent-period (post-2026-05-01) beta -0.109, p = 0.226; log-age by image beta +0.081, p = 0.114. Exclusion sensitivity (24h / 72h / 7d): n = 1,172 / 1,166 / 1,118; medians 53 / 53 / 51; Gini 0.800 / 0.801 / 0.810; top 1 percent share 0.635 / 0.636 / 0.649. No fixed-age standardization is claimed anywhere; each post contributes one cumulative snapshot.

## S10. Detailed-analytics computations

Selection analysis (29 pilot originals versus 1,145 others): standardized mean differences computed with pooled SDs: log impressions +0.32, age hours -0.43, word count +0.68, hashtag count +0.29; Mann-Whitney p = 0.063 on impressions; top-decile membership 20.7 versus 9.8 percent; pilot format counts image 17, text 8, poll 1, video 1, article 1, document 1; pilot months November 2025 through July 2026. No selection weighting is applied: overlap on word count is poor and weights would be unstable.

Agreement (n = 29): later analytics impressions greater than or equal to earlier feed counts in 29 of 29; median ratio 1.005; median absolute difference 1; Bland-Altman on logs: mean difference 0.0396, SD 0.1315, limits of agreement -0.218 to 0.297; Spearman rho of log difference against age -0.452, p = 0.014.

Members reached and out-of-network share (n = 28 each): repeat-exposure ratio median 7.08, IQR 2.67 to 10.81, max 27.0; out-of-network share median 0.10, IQR 0.035 to 0.475. Spearman: impressions versus out-of-network share rho 0.707, p = 2.6e-05; impressions versus repeat ratio rho -0.620, p = 4.4e-04. Top-quartile contrast: median out-of-network difference +0.52; permutation p = 0.040 (5,000 permutations, seed 20260719; the frozen r5 run reported 0.037 with its own seed; both are recorded). These tests constitute an exploratory pilot family; no multiplicity adjustment was applied across them. In this purposefully selected pilot, the earlier feed snapshot and later creator-analytics counts show close agreement after accounting for cumulative growth; no general cross-system agreement claim is made.

Prohibited analyses documented in the private unsupported-inference audit: causal mediation through out-of-network share (post-treatment, jointly determined, selected, n too small, sequential ignorability not credible) and imputation of analytics fields to the 1,145 non-pilot posts (no validation sample; transportability unknown).

## S11. Predictive benchmark

Features: log1p age, word count, hashtag count, image/video/document flags, posts in previous 24 hours. The one post lacking a timestamp is excluded. Chronological split: training n = 703 (2025-09-06 01:56:58 UTC to 2026-03-10 20:09:10 UTC); calibration n = 235 (2026-03-16 19:33:37 UTC to 2026-06-01 00:04:42 UTC); untouched test n = 235 (2026-06-02 03:08:40 UTC to 2026-07-18 05:31:32 UTC). Models: RidgeCV (25 log-spaced alphas 1e-3 to 1e3); random forest (500 trees, minimum leaf 5, seed 20260719); gradient boosting (300 trees, depth 3, learning rate 0.05, seed 20260719). Models use training data only. Quantile shifts and absolute-residual nonconformity scores use calibration data only. For nominal 90 percent coverage, the half-width is calibration absolute-residual order statistic 213 of 235. Test MAE / RMSE / coverage / mean interval width are: ridge 0.940 / 1.220 / 0.694 / 2.138; random forest 0.829 / 1.137 / 0.753 / 2.223; gradient boosting 0.915 / 1.208 / 0.915 / 4.435. Four contiguous calibration-block sensitivities yield test-coverage ranges 0.340-0.953, 0.634-0.911, and 0.864-0.966 respectively. The timing sensitivity is compatible with a changing residual scale, but undercoverage is not treated as proof of distribution shift. Complete output and interpretation are in `R9_PREDICTIVE_BENCHMARK.csv`, `R9_PREDICTIVE_INTERVAL_BLOCK_SENSITIVITY.csv`, and `R9_PREDICTIVE_INTERVAL_METHOD_NOTE.md`.

## S12. Quantile and distributional regression

Quantile regressions of ln(y) at tau in {0.10, 0.25, 0.50, 0.75, 0.90} for log-age (univariable) and for word count and video (each with log-age control): 15 exploratory tests, Benjamini-Hochberg within the family. Full profiles:

| tau | log-age beta (p) | word count beta (p) | video beta (p) |
|---:|---|---|---|
| 0.10 | -0.324 (2.8e-27) | +0.0033 (1.1e-13) | +0.389 (2.3e-06) |
| 0.25 | -0.347 (1.7e-48) | +0.0028 (9.6e-18) | +0.266 (3.0e-04) |
| 0.50 | -0.364 (2.0e-58) | +0.0033 (1.7e-21) | +0.220 (0.006) |
| 0.75 | -0.380 (1.7e-50) | +0.0037 (3.2e-33) | +0.172 (0.063) |
| 0.90 | -0.359 (4.7e-17) | +0.0058 (2.7e-25) | +0.078 (0.655) |

Reported as descriptive distributional contrasts, not identified mechanism effects. The age exclusion sensitivity in S9 and the concentration decomposition in S6.2 use these same subsets and are internally consistent with the profiles above.

## S12.1. Selection and agreement sensitivity values

Pilot selection standardized differences (pooled-SD): impressions (raw) -0.05, log impressions +0.32, age hours -0.43, word count +0.68, hashtag count +0.29. Pilot top-decile membership 20.7 percent versus 9.8 percent. Pilot format counts: image 17, text 8, poll 1, video 1, article 1, document 1 (versus 580 / 358 / 1 / 115 / 87 / 4 among the remaining 1,145). Mann-Whitney p = 0.063 on raw impressions. The age exclusion table (S9) and the agreement age relation (S10) jointly imply that pilot-versus-rest differences partly reflect collection timing, which is one reason no weighting-based generalization is attempted.

## S12.2. Anomaly and influence values

Primary-model residual SD 0.801. Cook's distance (from the frozen private influence diagnostics): maximum 0.041, far below 1, while 49 of 1,174 posts exceed the conventional 4/n screening threshold of 0.0034. Coefficient paths remain sign-stable, indicating distributed rather than single-observation influence; the three largest values are annotated in Figure 21 by chronological index. Extreme residuals by construction: 12 posts below the 1st percentile and 12 above the 99th. The frozen earlier analysis of the account owner's 22 suspicion-flagged posts found mean residual -0.097 (random-set permutation p = 0.552) with zero posts below -1.96 residual SDs against a chance expectation of about 0.55; that analysis is frozen and quoted, not recomputed, because the flag set is not part of the current processed dataset.

## S13. Frozen race-analysis specification (not rerun)

Source: private frozen race-results checkpoint (withheld from the public repository; SHA-256 retained in the private audit record). Outcome: ln(1 + feed impressions). Controls in the adjusted OLS: log1p age hours, word count, hashtag count, link, image, and video flags; HC3 errors. Additional specifications: plus month fixed effects; plus format and month; median and p90 quantile regressions; logistic models for exceeding the account median and p90; negative binomial GLM with the software-default fixed dispersion alpha = 1 (labeled throughout as: historical frozen sensitivity model with fixed alpha = 1; not the preferred count model). Non-race dispersion diagnostics estimate NB2 alpha = 1.44 and Cameron-Trivedi overdispersion far above 1, so the fixed-alpha model's mean-variance assumption is rejected by the data; estimated-dispersion results would differ. No race model was rerun in this revision; every race number in the paper was transcribed from the frozen checkpoint and verified against it programmatically. The public multiplicity table under `data/aggregate/multiplicity/` preserves the adjusted p-values and q-values without exposing private paths.

Groups and frozen headline values, transcribed from the frozen JSON:

**Direct Black-centered (n = 61 versus 1,113).** Raw medians 82 versus 52 (ratio 1.58); geometric means 80.7 versus 59.5; 62.3 percent at or above the account median; 13.1 versus 9.9 percent at or above p90. Adjusted OLS -23.7 percent (CI -37.8 to -6.3, p = 0.0098); plus month -26.2 percent (CI -39.8 to -9.5, p = 0.0035); plus format and month -26.4 percent (CI -39.9 to -9.7, p = 0.0033); median quantile -24.3 percent (p = 0.0077); p90 quantile -26.5 percent (p = 0.185); logistic p90 odds ratio 0.45 (CI 0.17 to 1.20, p = 0.108); fixed-alpha NB -65.9 percent (CI -74.1 to -55.1, p = 2.2e-14). Across the frozen eight-topic primary OLS family, the Benjamini-Hochberg q-value is 0.078, the Holm-adjusted p-value is 0.078, and the Bonferroni-adjusted p-value is 0.078. The alternative within-topic specifications are not members of that across-topic primary-model family. Within-month median difference +2.25 with the group lower in 25 percent of 8 strata; within-format +12.75, lower in 50 percent of 4 strata. Achieved power 0.691 for the raw standardized contrast; minimum detectable d = 0.369 at 80 percent power. Frozen race intervals use HC3 errors and do not model detected serial dependence; their nominal precision may exceed dependence-aware precision. Models remain frozen.

**Composite Black-visibility group (n = 83).** Raw medians 83 versus 52 (ratio 1.60). Adjusted OLS -10.9 percent (CI -27.9 to +10.1, p = 0.286); plus month -13.9 percent (CI -29.8 to +5.7, p = 0.154); plus format and month -13.9 percent (CI -30.0 to +5.9, p = 0.156); fixed-alpha NB -52 percent (p = 3.2e-09).

**Racial-justice group (n = 153).** Raw medians 72 versus 51 (ratio 1.41); 17.0 versus 9.0 percent at or above p90. Adjusted OLS +3.1 percent (CI -11.4 to +19.9, p = 0.697); plus month -2.1 percent (CI -15.5 to +13.5, p = 0.782); median quantile +3.0 percent (p = 0.696); fixed-alpha NB -25.8 percent (CI -38.9 to -9.9, p = 0.003).

**Narrow subgroup, Black history / unity / culture (n = 19; independently reproduced).** Raw median 89 versus 53; raw means approximately 110 versus 228 (mean-median reversal driven by the comparison group's extreme tail). Unadjusted +32.0 percent (p = 0.163); format and length +0.5 percent (p = 0.978); plus month -10.8 percent (p = 0.489); top outlier excluded +8.2 percent (p = 0.665). Confidence intervals were not retained in the frozen subgroup output and are not reconstructed. Power 0.25; minimum detectable d = 0.65. An earlier count of 21 in a working note reflected two records later excluded by the frozen filter chain; the reproduced frozen result uses 19, and the reconciliation is recorded here rather than in the paper.

Verdicts: Claim B Unresolved; B-sub Unresolved. Labels: PRELIMINARY_AUTOMATED_LABEL_ANALYSIS; 459 manual-review candidates; 0 approved; 0 confirmed structured moderation records.

**Label taxonomy.** The deterministic keyword taxonomy assigns non-exclusive topic flags from case-normalized post text: direct Black-centered content; Black creator or professional issues; Black history; Black excellence; civil rights; racial justice; anti-racism; police violence; race-linked immigration. The composite group is the union of the first four flags. Because 1,145 of 1,174 texts are possibly truncated previews, flags derived from text beyond the preview boundary are systematically unavailable, a limitation that human review of the full candidate set is designed to quantify.

## S13.1. Verification of frozen reporting

Because no race model was rerun, the accuracy of race reporting is itself an auditable claim. A private numerical-claim audit compared every numerical claim in the paper against its authoritative machine-readable source: each row lists the claim identifier, the value printed in the paper, the value read from the frozen private checkpoint or public aggregate tables, the source class, and a match flag computed under a stated numeric tolerance. The audit covers 67 claims spanning concentration, quantiles, mixtures, agreement, breaks, residual dependence, prediction, influence, and all four frozen race groups, and reports zero mismatches. The same discipline applies to prose: the claim-classification conventions from the prior revision are retained, and each of Sections 19 through 22 carries the frozen-result banner stating the label status and that no race-dependent model was rerun.

## S14. Semantic proxies

TF-IDF vectorizer fitted on the chronological corpus of 1,174 analysis-text fields (previews for 1,145, verified text for 29): lowercase, English stopwords removed, unigrams and bigrams, min document frequency 2. Derived variables: novelty versus history, similarity to previous 5 posts, similarity to prior top-decile posts, near-duplicate score, local semantic density; exact formulas remain in the private derived-variable dictionary. Sensitivity runs on the verified-full-text subset and short-post subset are retained in the frozen private outputs; the truncation caveat is stated wherever semantic variables appear. No transformer embedding model was added in this revision: the planned open-embedding sensitivity requires a pinned model artifact to be reproducible, and none was available in the frozen environment, so the item is recorded as NOT EXECUTED: REQUIRED INPUT UNAVAILABLE rather than approximated. Semantic models are never used to generate or revise race labels.

## S14.1. Structural-break sensitivity values

From `data/aggregate/structural_breaks/STRUCTURAL_BREAK_SENSITIVITY.csv`: weekly median series (44 points) PELT break in the week ending 2026-05-17, binary segmentation with two breaks adds 2026-06-21; weekly mean series identical; weekly p90 series (42 points) breaks at 2026-04-26 (binseg adds 2026-03-22). Placebo permutations: mean PELT break count under shuffling 0.44 (median series), 0.39 (mean series), 0.37 (p90 series); the share of shuffles with at least as many breaks as observed is 0.31, 0.31, and 0.27 respectively, which is why the weekly detections are labeled weak evidence in the paper. Monthly variance-minimizing split: 2026-05-31 in the full series, unchanged after excluding the top 1 percent and after excluding the maximum. Segmented-model placebo dates in 2025 produce no shift comparable to the May 2026 estimate; the March 2026 announcement-date model estimates a factor of 1.21 (CI 0.99 to 1.48, p = 0.057) versus 1.59 (CI 1.22 to 2.06, p = 0.0005) at the data-selected break.

## S15. Software, seeds, and execution

Python 3.12 virtual environment. The public repository pins runtime dependencies in `pyproject.toml` and, when present, `pylock.toml`. Frozen private analyses additionally used scipy, statsmodels, ruptures, matplotlib, and related scientific libraries recorded in the private computation provenance. Global seed for all new computations: 20260719. Public reproduction commands:

```
.venv/bin/python scripts/reproduce_benchmark.py \
  --data data/sanitized/R9_SANITIZED_NON_RACE_ANALYTIC_DATA.csv \
  --output-dir reproduced
.venv/bin/python scripts/verify_numeric.py --reproduced reproduced
.venv/bin/python scripts/verify_checksums.py
```

Private figure-generation and manuscript-rendering scripts are withheld. Public SHA-256 checksums for the repository tree are recorded in `release/SHA256SUMS.txt`.

## S15.1. Figure data provenance

Rendered figures in `figures/rendered/` are frozen publication assets. Private generation code is withheld. `figures/source_data/R9_FIGURE_RENUMBERING_MAP.csv` and `data/aggregate/renumbering/R9_FIGURE_RENUMBERING_MAP.csv` preserve the source-filename mapping. Figures 1-2 are the linear and log recorded-impression distributions; Figure 3 is the quantile forest plot; Figures 4-5 are the Lorenz and top-share curves; Figure 6 is the Q-Q plot; Figure 7 compares distribution information criteria; Figures 8-10 report mixture posterior diagnostics; Figure 11 is the mechanism diagram; Figure 12 is the age curve; Figure 13 reports sequence and semantic associations; Figure 14 is the alias map; Figure 15 reports break series; Figure 16 is the public chronology; Figures 17-20 use detailed analytics with field-specific denominators; Figure 21 reports influence diagnostics; and Figures 22-23 transcribe frozen race results from the private race-results checkpoint. Public figure hashes appear in `release/SHA256SUMS.txt`.

## S16. Privacy exclusions

The review bundle excludes raw post text, reviewer packet CSVs, private messages, viewer identities, browser profiles, cookies, tokens, credentials, Level B records, and full-page raw captures. The supplied sanitized non-race analytic table omits post text, preliminary race labels, review-candidate status, and direct platform identifiers; its row key is a sequential analytic index. Post identifiers in diagnostic outputs are de-identified indices. Aggregate tables contain no free-text content. Two additional controls apply to this archive specifically: the private correction-history document is excluded from the public bundle and from all public manifests, so the checksum list validates exactly against the shipped files; and the narrow-subgroup reconciliation note (the 21-versus-19 count difference, S13) is recorded in this supplement rather than in any file that quotes post content. A privacy scan and secret scan are run over every bundled file before packaging, and both must return zero findings.

## S17. Post-validation race-analysis plan

The complete plan, with estimands, models, diagnostics, and the multiple-testing scheme, is in `POST_VALIDATION_ANALYSIS_PREREGISTRATION_DRAFT.md`. Summary: after blinded human review of the 459 candidates, the first stage is label-quality measurement (rater agreement and Cohen's kappa against a second blinded pass; classifier precision, recall, false-positive and false-negative rates against approved labels). The primary analysis is the approved-label analogue of the frozen adjusted log model with a preregistered single primary estimand: the percentage difference in conditional geometric-mean impressions for approved Direct Black-centered posts, with the frozen covariate set and HC3 errors, evaluated once at a fixed alpha within a preregistered family. Secondary analyses include quantile-effect profiles, balance diagnostics, a matched sensitivity analysis without causal claims, a doubly robust estimator conditional on demonstrated overlap, omitted-variable sensitivity appropriate for continuous log outcomes, label-uncertainty propagation using the measured classifier error rates, and a sign-reversal decomposition separating covariate-composition effects from conditional differences. The trigger condition, the testing family, and the error-rate control are fixed in the draft before any validated-label analysis is run, and the draft states explicitly which frozen results it supersedes and which it leaves standing. None of these analyses has been executed, and nothing in the draft modifies any frozen result.
