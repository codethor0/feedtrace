---
title: "FeedTrace: Reach, Ranking, and Black Visibility in 1,174 LinkedIn Posts"
subtitle: "A longitudinal study of impression concentration, audience expansion, Feed mechanisms, and preliminary racial-visibility differences"
author: "Isaac Thor"
---

# FeedTrace: Reach, Ranking, and Black Visibility in 1,174 LinkedIn Posts

*A longitudinal study of impression concentration, audience expansion, Feed mechanisms, and preliminary racial-visibility differences*

**Author.** Isaac Thor (public research identity: Thor Thor), Independent Researcher. This is independent research and is not affiliated with, endorsed by, or conducted on behalf of any employer or platform.

**Manuscript date.** July 18, 2026.

**Keywords.** algorithm audit; recommender systems; LinkedIn Feed; exposure inequality; heavy-tailed distributions; mixture models; racial visibility; platform transparency; black-box audit.

**Conflict of interest.** The author owns the LinkedIn account whose posts are analyzed and authored the posts under study. No financial conflicts exist. No compensation was received from any platform.

**Funding.** This research received no external funding.

**Data availability.** The accompanying public research archive includes aggregate analysis outputs, model specifications, figure data, checksums, and a sanitized non-race analytic table sufficient to reproduce the corrected R9 predictive benchmark. Row-level post text, viewer information, race-label candidate records, and private account records are withheld to protect privacy.

**Code availability.** The accompanying public research archive includes executable code, environment specifications, and commands for the corrected R9 non-race predictive benchmark. Code for the broader analysis is retained in the private project repository and is not represented as independently executable from this sanitized archive.

**Ethics and privacy.** Data collection was limited to the author's own posts and read-only, creator-visible analytics that LinkedIn exposes to the account owner. No viewer identities, private messages, or authentication data were collected. No third-party content is reproduced. Race-related labels apply to post topics, not to any person.

## 1. Abstract

This study analyzes 1,174 original posts published from a single LinkedIn account between September 6, 2025, and July 18, 2026, together with feed-level recorded impressions for every original post and detailed creator analytics for a purposefully selected pilot of 29 posts. The central question is what these posts reveal about impression concentration, audience expansion, ranking behavior, content-level variation, and the visibility of Black-centered and racial-justice content.

Recorded impressions are highly concentrated. The median original post received 53 impressions and the mean was 226, a mean-to-median ratio of 4.3 reflecting strong right skew. The Gini coefficient is 0.799 (bootstrap 95 percent CI 0.648 to 0.874). The top 1 percent of posts account for 63.5 percent of all recorded impressions and the bottom half of posts for 7.3 percent. The effective number of equally weighted posts is 11.9 out of 1,174. Concentration is not an artifact of young posts: restricting to posts at least 7 days old leaves the Gini essentially unchanged (0.810, n = 1,118).

No tested single continuous family reproduces both the body and the extreme upper tail. The fitted lognormal underpredicts the empirical 95th percentile and substantially underpredicts the empirical 99th percentile. Finite lognormal mixtures materially improve in-sample information criteria and held-out log likelihood, and the preference for multiple components survives exclusion of the maximum post and of the entire top 1 percent. These components are descriptive reach regimes, not identified platform stages.

In the 29-post detailed-analytics pilot, higher impression counts are associated with higher out-of-network share (Spearman rho 0.71, p = 2.6e-05, n = 28) and lower repeat-exposure ratios (rho -0.62, p = 4.4e-04, n = 28). This pattern is consistent with audience expansion playing a larger role among higher-impression posts, but the purposefully selected cumulative subset does not identify a causal distribution pathway. These tests form an exploratory pilot family; no multiplicity adjustment was applied.

Direct Black-centered content (n = 61, preliminary automated labels) had higher unadjusted median recorded impressions (82 versus 52), while adjusted log-scale models estimated approximately 24 percent lower conditional recorded impressions (95 percent CI -37.8 to -6.3 percent, raw p = 0.0098). Across the frozen eight-topic primary-model family, the Benjamini-Hochberg q-value is 0.078, the Holm-adjusted p-value is 0.078, and the Bonferroni-adjusted p-value is 0.078. Stratified within-month and within-format comparisons did not reproduce the reduction, and achieved power for the raw contrast was 0.69. The account-level racial-visibility signal is serious and unresolved: the evidence neither confirms nor rejects an impression penalty, and it does not identify a mechanism.

The study specifies the human-validated labels, fixed-age snapshots, matched designs, and multi-account counterfactuals that would be required to distinguish retrieval, ranking, audience, and moderation explanations, and includes a preregistration draft for the post-validation analyses.

## 2. Introduction

LinkedIn distributes posts through a Feed that most creators experience only through its outputs. A creator can observe how many recorded impressions a post received, and sometimes how those impressions decomposed into in-network and out-of-network audiences, but cannot observe the candidate pool a post entered, the ranking score it was assigned, its recommendation eligibility, or the counterfactual reach it would have received under different conditions. Visibility is therefore governed by a system whose internal decisions are not directly inspectable by the people it distributes.

This study builds an independent evidence record from the outputs that are exposed. It uses 1,174 original posts from one account, collected over ten months, to characterize how recorded impressions are distributed, how concentrated recorded impressions are, how observable factors relate to recorded impressions, and whether Black-centered and racial-justice content show different visibility patterns. The methodological stance is that of an external outcome-based black-box audit: the system is not observed directly, so its behavior is inferred from recorded outputs and compared against publicly documented architecture (Sandvig et al. 2014; Metaxa et al. 2021). This is a fundamental identification problem in external platform research, not a correctable omission in this dataset. No outside observer can fully inspect a changing production recommender without platform access to candidate sets, scores, eligibility decisions, experiments, and model versions.

A single-account study cannot estimate a platform-wide effect, but it offers a form of evidence that aggregate platform studies generally cannot: a dense longitudinal record from one creator, repeated across formats, topics, and time. Holding the creator identity fixed removes between-creator differences from the comparison and makes within-account conditional patterns observable. This granularity narrows the estimand to an account-level visibility difference rather than claiming representativeness it does not have.

The analysis treats platform documentation as a description of intended or documented behavior, not as a validation of outcomes. It treats the absence of a recorded moderation event as information about documented enforcement only, not as evidence about covert retrieval or ranking. It treats nonsignificant coefficients as uncertainty rather than as demonstrations of equal treatment. These commitments are applied symmetrically: the study does not presume the platform acted unfairly, and it does not presume the platform acted neutrally.

The paper proceeds in five movements. Sections 5 through 9 characterize the data and the shape of the recorded-impression distribution. Sections 10 through 12 summarize the publicly documented Feed architecture and the difference between explicit moderation and covert distribution reduction. Sections 13 through 18 analyze measurement age, sequence, format, semantics, structural breaks, detailed analytics, and predictive structure. Sections 19 through 23 report the frozen preliminary race-related results and the competing explanations for them. Sections 24 through 29 place the findings against external evidence, specify what stronger evidence would require, and conclude.

## 3. Related Work

**Black-box and outcome-based algorithm audits.** Sandvig et al. (2014) established the taxonomy of audit designs available to outside researchers, from code audits to scraping and sockpuppet audits, and identified the outcome-based audit, in which system behavior is inferred from observed outputs, as the primary tool available when internals are inaccessible. Metaxa et al. (2021) systematized this method across search, advertising, and recommendation systems and emphasized that audits estimate output disparities rather than internal intent. The present study is an outcome-based audit of a single account's Feed distribution, and inherits both the strengths (real production outputs, longitudinal density) and the identification limits (no candidate sets, scores, or counterfactuals) of that design.

**Recommender retrieval and ranking.** Modern industrial feeds are multi-stage systems: candidate retrieval narrows an enormous corpus to hundreds of items, one or more ranking models score candidates against predicted engagement objectives, and re-ranking layers apply diversity, integrity, and freshness adjustments. LinkedIn's own engineering publications document this structure for its Feed, including large-scale ranking models (Borisyuk et al. 2024), the FishDB retrieval engine (LinkedIn Engineering 2025), causal-language-model retrieval for out-of-network content (Naghiaei et al. 2026), dwell-time objectives (LinkedIn Engineering 2020, 2024), and a sequential Generative Recommender for Feed ranking (Hertel et al. 2026; LinkedIn Engineering 2026). These sources describe intended architecture; none of them exposes per-post scores or eligibility decisions to creators.

**Exposure inequality and popularity concentration.** Heavy-tailed, winner-take-most outcome distributions are ubiquitous in cultural markets and social media reach, and arise from cumulative-advantage dynamics, popularity-biased recommendation, and heterogeneous content quality (Salganik, Dodds, and Watts 2006; Clauset, Shalizi, and Newman 2009). Recommender-system research documents popularity bias as a systematic property of collaborative and engagement-optimized rankers (Abdollahpouri et al. 2019). The concentration this study measures within one account echoes, at small scale, the concentration those literatures document across creators.

**Sociotechnical fairness without direct protected-class inputs.** Ranking systems can produce disparate exposure without any explicit protected attribute in the feature set, through proxies, network structure, and feedback loops (Selbst et al. 2019). Geyik, Ambler, and Kenthapadi (2019) demonstrated fairness-aware re-ranking in LinkedIn Talent Search, establishing that representation in ranked LinkedIn products is measurable and adjustable; the product boundary matters, because Talent Search is not the organic Feed and findings do not transfer across products.

**Network homophily and audience availability.** Reach through a networked feed depends on the composition of the poster's network and on how retrieval expands beyond it. Homophily in professional networks shapes which audiences are reachable for which topics, a mechanism this study can hypothesize but not measure without network-composition data.

**Creator reports on LinkedIn.** Black creators and anti-racist campaigners have publicly reported low reach, disappearing posts, removals, and suspected topic-linked effects on LinkedIn (Joseph 2020; Digiday 2020; Gilmer 2021). These reports are a documented and contested pattern, distinct from a measured platform-wide disparity, and they motivate the account-level tests conducted here.

**Positioning.** Against this literature, the contribution of this study is a dense, single-account, output-based audit that (a) quantifies concentration with uncertainty, (b) tests distributional families and mixtures rather than assuming one, (c) connects observed patterns to specific documented Feed stages without equating statistical components to production systems, and (d) reports a preliminary race-related conditional difference under explicit frozen controls that prevent overclaiming in either direction.

## 4. Research Questions and Evidence-Strength Map

**Central question.** What do 1,174 original posts from one LinkedIn account reveal about impression concentration, audience expansion, ranking behavior, content-level variation, and the visibility of Black-centered and racial-justice content?

**Integrated questions.**

1. How unequal and heavy-tailed are recorded impressions?
2. Does one probability family describe the data, or are multiple descriptive recorded-impression regimes needed?
3. How do measurement age, time, posting sequence, format, semantic context, and detailed analytics relate to impressions?
4. Which publicly documented Feed stages are consistent with the observed patterns, and which stages remain unidentified?
5. What do the frozen preliminary race results establish, fail to establish, and require next?

Table 1 summarizes research-question evidence-strength map.

**Table 1. Research-question evidence-strength map.**

| Research question | What the current data answer | What remains unidentified |
|---|---|---|
| Concentration | Gini, top shares, quantiles, decomposition by month, format, age, and period, with bootstrap uncertainty | Whether concentration is produced by retrieval, ranking, audience response, or all three |
| One or multiple recorded-impression regimes | Mixtures materially improve in-sample criteria and held-out likelihood; preference survives tail exclusions | Whether statistical components correspond to production stages |
| Measurement age and time | Nonlinear age association, exclusion sensitivity, structural-break location and stability | Fixed-age growth trajectories; deployment timing of platform changes |
| Sequence, semantics, format | Reduced-form adjusted associations and time-respecting predictive checks | Viewer-level exposure paths and counterfactual posts |
| Audience expansion | Within-pilot associations between impressions, out-of-network share, and repeat exposure, with exact denominators | Causal distribution pathways; generalization beyond the selected pilot |
| Black-centered recorded-impression patterns | Raw, adjusted, threshold, quantile, and stratified frozen summaries | Validated labels and a causal topic effect |
| Stability across estimands | Sign agreement and disagreement across frozen model specifications | Robustness after human validation and preregistration |
| Hidden mechanisms | Mechanisms consistent with the observed outputs | Which mechanism, if any, produced a particular outcome |
| Evidence to distinguish mechanisms | A concrete measurement and preregistration agenda | Candidate, score, eligibility, and viewer-level data unavailable here |

## 5. Data Collection, Provenance, and Measurement

The dataset comprises 1,192 total inventoried records from one account: 1,174 creator-owned original posts and 18 reposts. The original posts span September 6, 2025, through July 18, 2026. Detailed creator analytics were collected on July 18, 2026. Feed-level recorded impressions are available for all 1,174 originals. Reposts are excluded from the inferential sample because the account was not the original author and creator analytics were unavailable for the two reposts tested, making their distribution and measurement process non-comparable.

Table 2 summarizes dataset composition and field completeness.

**Table 2. Dataset composition and field completeness.**

| Component | Count | Notes |
|---|---:|---|
| Total inventoried records | 1,192 | one account, full study window |
| Creator-owned original posts | 1,174 | inferential sample; recorded impressions available for all |
| Reposts | 18 | excluded from inference; not authored by the account |
| Detailed-analytics originals | 29 | purposefully selected pilot |
| Pilot repost records without analytics | 2 | analytics unavailable; excluded |
| Verified full text | 29 | same posts as the analytics pilot |
| Classified from possibly truncated previews | 1,145 | preview text may truncate long posts |
| Manual race-review candidates | 459 | 0 human-approved at analysis time |
| Confirmed structured moderation records | 0 | explicit enforcement only; see Section 12 |

Table 3 summarizes measurement definitions.

**Table 3. Measurement definitions.**

| Term | Definition |
|---|---|
| Recorded impressions | The feed-level impression count LinkedIn displays for a post; the primary outcome. LinkedIn's Help documentation describes impressions as the number of times a post was displayed |
| Members reached | LinkedIn's estimate of unique members who saw a post, available only in detailed analytics |
| Out-of-network share | The percentage of impressions delivered to members outside the account's follower network, as reported in detailed analytics |
| Repeat-exposure ratio | Analytics impressions divided by members reached; the average number of displays per unique member |
| Post age at collection | Hours between publication and the impression snapshot; impressions are cumulative, so age is a measured confounder |

Impressions are analyzed on the original scale and on the natural-log scale. Log-scale models in the non-race analysis pipeline use ln(y) on the strictly positive impression counts; the frozen race-analysis pipeline used ln(1 + y). The technical supplement's model registry records the exact outcome and transformation for every model, and every table and figure in this paper labels the transformation actually used by the underlying code.

Detailed creator analytics, including out-of-network share and members reached, are available for 29 originals. This was a purposefully selected pilot, not a probability sample: collection covered multiple formats, low- and high-impression cases, and posts relevant to the project's mechanism and content questions, followed by one additional full-run case. Section 17 quantifies how the pilot differs from the remaining originals. Field-level denominators vary within the pilot: analytics impressions are available for 29 posts, while members reached and out-of-network share are available for 28 (Table 12). Every pilot statistic in this paper states the exact denominator used.

Racial-visibility labels were produced by a transparent, deterministic keyword taxonomy rather than a supervised model with training and validation splits. The taxonomy keeps Direct Black-centered content, Black creator issues, Black history, Black excellence, civil rights, racial justice, anti-racism, police violence, and race-linked immigration content distinct. Because no human-validated reference set yet exists, precision, recall, and classification error rates cannot be estimated. A human-review protocol identified 459 race-review candidates; 0 have been human-approved at the time of this analysis. The analysis label for all race-related results is PRELIMINARY_AUTOMATED_LABEL_ANALYSIS. No confirmed structured moderation record appears in the dataset.

## 6. Empirical Impression Distribution

Recorded impressions per original post range from single digits to 67,349, with a median of 53 and a mean of 226. The interquartile range is 61 and the median absolute deviation is 25. Central tendency depends heavily on the estimator: the geometric mean is 60.1, the 10 percent trimmed mean is 63.5, and the 5 percent winsorized mean is 76.0. The distribution is strongly right-skewed (moment skewness 24.7, excess kurtosis 704); these moment-based estimates are dominated by the maximum observation and are descriptive sample summaries, not stable population parameters.

Figure 1 shows the distribution on a linear scale with the main panel truncated at the 99.5th percentile and the complete range, including the maximum, in an inset; Figure 2 shows the log-scale distribution with the median, 95th, and 99th percentiles marked.

![Figure 1. Recorded impressions on a linear scale. Main panel truncated at p99.5; inset shows the complete range on a log count axis, including the maximum of 67,349. n = 1,174.](figures/fig03_distribution_linear.png)

![Figure 2. Natural log of recorded impressions with median, p95, and p99 reference lines. n = 1,174.](figures/fig04_distribution_log.png)

Table 4 summarizes empirical quantiles and concentration (n = 1,174; outcome: recorded impressions; percentile bootstrap, 2,000 replicates, posts resampled).

**Table 4. Empirical quantiles and concentration (n = 1,174; outcome: recorded impressions; percentile bootstrap, 2,000 replicates, posts resampled).**

| Quantity | Estimate | 95% CI |
|---|---:|---|
| Median | 53 | 50 to 56 |
| p75 | 93 | 87 to 101 |
| p90 | 172 | 153 to 197 |
| p95 | 254 | 217 to 327 |
| p99 | 1,518 | 642 to 5,966 |
| Gini | 0.799 | 0.648 to 0.874 |
| Top 1% share | 63.5% | 37.6% to 75.2% |

Figure 3 presents the upper quantiles as a forest plot on a log axis. The p99 interval is wide because the top of the distribution is dominated by a few posts; the technical supplement documents the bootstrap type, replicate count, seed, interpolation rule, and a second valid resampling run whose interval differs in the upper limit, which is why the percentile method above was designated the primary method before comparison.

Quantile-based summaries are preferred to moment-based summaries throughout this paper for a specific reason: with a maximum observation more than 1,200 times the median, sample moments are functions of a handful of points. The sample mean changes by roughly 25 percent if the single largest post is removed, whereas the median and all reported quantiles up to p95 are unchanged to the displayed precision. Any claim in this paper that depends on a mean is therefore accompanied by a robust counterpart, and the estimand named in each table states which functional is being estimated.

![Figure 3. Bootstrap 95 percent intervals for upper quantiles of recorded impressions on a log axis. n = 1,174; percentile bootstrap, 2,000 replicates.](figures/fig06_quantile_bootstrap.png)

## 7. Concentration and Exposure Inequality

Impressions are concentrated in a small number of posts. The Gini coefficient is 0.799 (95 percent CI 0.648 to 0.874); the interval's width reflects genuine upper-tail sampling sensitivity, not uncertainty in reading the recorded counts. The top 1 percent of posts capture 63.5 percent of recorded impressions, the top 5 percent capture 72.2 percent, the top 10 percent capture 76.8 percent, and the top 20 percent capture 82.7 percent. The bottom 50 percent of posts together account for 7.3 percent. The effective number of equally sized posts (inverse Herfindahl) is 11.9: the recorded exposure of 1,174 posts behaves like roughly a dozen equally weighted posts.

Figure 4 presents lorenz curve of recorded impressions across all 1,174 original posts.

![Figure 4. Lorenz curve of recorded impressions across all 1,174 original posts. Gini 0.799 (95 percent CI 0.648 to 0.874).](figures/fig01_lorenz_curve.png)

Figure 5 presents the cumulative impression shares captured by the top 0.1, 1, 5, 10, and 20 percent of posts.

![Figure 5. Cumulative share of recorded impressions captured by the highest-impression posts, with the top 0.1, 1, 5, 10, and 20 percent labeled. n = 1,174.](figures/fig02_top_share_curve.png)

Concentration is not uniform across the dataset's strata. Table 5 summarizes the decomposition computed for this study (full table with bootstrap intervals in the archive file CONCENTRATION_BY_STRATUM_R8.csv).

**Table 5. Concentration decomposition (Gini with bootstrap 95 percent CI; strata under 20 posts not estimated).**

| Stratum | n | Gini | 95% CI | Top 1% share |
|---|---:|---:|---|---:|
| All posts | 1,174 | 0.80 | 0.64 to 0.87 | 63.5% |
| Mature (age at or above median) | 587 | 0.67 | 0.42 to 0.79 | 47.3% |
| Young (age below median) | 587 | 0.83 | 0.62 to 0.90 | 65.1% |
| Before June 2026 | 937 | 0.81 | 0.53 to 0.89 | 68.7% |
| June 2026 onward | 236 | 0.70 | 0.45 to 0.79 | 45.8% |
| Image format | 597 | 0.85 | 0.62 to 0.92 | 72.9% |
| Text format | 366 | 0.67 | 0.46 to 0.77 | 42.6% |
| Video format | 116 | 0.43 | 0.35 to 0.50 | 11.8% |
| Article format | 88 | 0.84 | 0.50 to 0.90 | 59.7% |

Three observations follow. First, concentration is present in every stratum large enough to estimate; it is not created by pooling heterogeneous months. Second, monthly Gini values range from 0.36 (April 2026) to 0.91 (May 2026), so inequality itself varies through time, and the May 2026 month that contains the largest post is also the most concentrated. Third, video posts show markedly lower concentration (Gini 0.43) than image posts (0.85), consistent with format-dependent recorded-impression dynamics, though format is entangled with topic and time. Restricting to mature posts at least 7 days old leaves overall concentration essentially unchanged (Gini 0.810, top 1 percent share 64.9 percent, n = 1,118), so concentration is not an artifact of measurement age.

This concentration is the central descriptive fact of the dataset. It is an observed property of the recorded outputs and does not, by itself, identify whether concentration arises from content differences, audience structure, retrieval, ranking, or a combination.

## 8. Candidate Distributions and Tail Behavior

On the log scale the body of the distribution is approximately Gaussian, but the upper tail is heavier than a single lognormal predicts. A quantile-quantile plot against a fitted lognormal shows systematic departure in the right tail (Figure 6), and the ratio of the 99th to the 95th percentile is 6.0 (95 percent CI 2.6 to 24.9), far larger than a lognormal body would generate.

![Figure 6. Quantile-quantile plot of log impressions against a fitted lognormal with the upper 5 percent tail distinguished. Equal axis scales. n = 1,174.](figures/fig05_qq_lognormal.png)

Equation 1 gives the quantile function implied by a lognormal model for impressions:

<div style="text-align:center;font-size:1.08em;margin:0.8em 0;"><i>Q</i>(<i>p</i>) = exp[<i>&mu;</i> + <i>&sigma;</i> &Phi;<sup>&minus;1</sup>(<i>p</i>)]&nbsp;&nbsp;&nbsp;&nbsp;(Equation 1)</div>

where &Phi;<sup>&minus;1</sup> is the standard normal quantile function. Equation 2 evaluates this function at p = 0.95 after fitting the body of the log-impression distribution gives approximately &mu; = 3.77 and &sigma; = 0.82, which implies a 95th percentile near

<div style="text-align:center;font-size:1.08em;margin:0.8em 0;"><i>Q</i>(0.95) = exp[3.77 + 0.82 &times; 1.645] &asymp; 167.&nbsp;&nbsp;&nbsp;&nbsp;(Equation 2)</div>

In plain text: the p-th quantile equals exp(mu + sigma times the inverse standard-normal quantile of p). The empirical 95th percentile is 254 (95 percent CI 217 to 327). The fitted lognormal underpredicts the empirical p95, whose displayed bootstrap interval excludes 167, and substantially underpredicts the empirical p99 of 1,518, indicating that a fit that appears adequate near the center does not reproduce the upper tail.

Table 6 summarizes candidate distribution comparison (n = 1,174; maximum likelihood; AICc; calibrated KS via 1,000-replicate parametric bootstrap).

**Table 6. Candidate distribution comparison (n = 1,174; maximum likelihood; AICc; calibrated KS via 1,000-replicate parametric bootstrap).**

| Family | Parameters | AICc | Delta AICc | Calibrated KS p |
|---|---:|---:|---:|---:|
| Burr XII | 3 | 12,513 | 0 | 0.020 |
| Log-logistic | 2 | 12,616 | +103 | 0.001 |
| Lognormal | 2 | 12,812 | +299 | 0.001 |
| Generalized gamma | 3 | 13,034 | +521 | 0.001 |
| Pareto | 2 | 13,768 | +1,255 | 0.001 |
| Weibull | 2 | 13,815 | +1,302 | 0.001 |
| Gamma | 2 | 14,508 | +1,995 | 0.001 |

The conclusion is not an artifact of choosing lognormal over one flexible alternative. Burr XII gives the best in-sample AICc and five-fold held-out log likelihood among the expanded continuous-family comparison, yet a 1,000-replicate fitted-model bootstrap still gives KS p = 0.020: the best available single family is still rejected at conventional levels. Figure 7 displays the information-criterion comparison; the caption states explicitly that the figure shows information criteria, and the best AICc does not imply adequate fit.

![Figure 7. Delta corrected AIC across candidate families, sorted; the best family (Burr XII) still fails a calibrated goodness-of-fit test (KS p = 0.020), so best AICc does not imply adequate fit. n = 1,174.](figures/fig07_distribution_comparison.png)

Tail-index estimation is threshold-unstable. Hill estimates decline from 1.59 at 25 upper-order observations to 0.76 at 300, and generalized Pareto shape estimates move materially as the threshold rises (Balkema and de Haan 1974; Pickands 1975; Hill 1975; Clauset, Shalizi, and Newman 2009). The direction of the instability is itself informative: estimates computed deeper into the tail imply progressively heavier behavior, so any single reported tail index would be an artifact of the threshold choice. A Hill index below 1 would imply an infinite-mean regime if taken literally, which illustrates why the estimates should be read as diagnostics of instability rather than as parameters. Because the tail index is unstable in the observed range, this paper reports the instability itself and observed-range uncertainty, and does not report extrapolated long-range return levels (for example a 99.9th percentile), which would inherit the instability without disclosing it.

Two summary statements survive all of the tail diagnostics. First, the upper tail is heavier than every two-parameter family tested, including on the log scale. Second, the data cannot distinguish among heavy-tailed generating stories (a stable power-law tail, a mixture of lognormal regimes, or a time-varying process with occasional wide-distribution events), and the mixture analysis in the next section should be read as one defensible description among these, chosen for interpretability rather than proven uniqueness.

## 9. Mixture Models and Descriptive Reach Regimes

Finite lognormal mixtures were fitted with one, two, and three components (EM with 20 random initializations, fixed seed, convergence verified). Table 7 reports the diagnostics required to evaluate them.

**Table 7. Mixture-model diagnostics (outcome ln(y); n = 1,174; 5-fold cross-validated held-out log likelihood; posterior entropy in nats).**

| Components | AIC | BIC | Held-out log lik | Posterior entropy | Weights | Log means | Log SDs |
|---:|---:|---:|---:|---:|---|---|---|
| 1 | 3,193 | 3,204 | -1.365 | 0.00 | 1.00 | 4.10 | 0.94 |
| 2 | 2,912 | 2,938 | -1.247 | 0.26 | 0.87 / 0.13 | 3.94 / 5.16 | 0.66 / 1.60 |
| 3 | 2,879 | 2,920 | -1.227 | 0.42 | 0.62 / 0.35 / 0.03 | 3.64 / 4.66 / 7.24 | 0.52 / 0.63 / 1.76 |

Both multi-component models decisively beat the single lognormal on every criterion. The three-component model has the lowest BIC and the best held-out likelihood, but its improvement over two components is modest, its assignment uncertainty is higher (entropy 0.42 versus 0.26), and its smallest component contains roughly 3 percent of posts centered far into the tail. The two-component model is therefore used as the descriptive reference: a dominant body regime (weight 0.87, log mean 3.94, roughly 51 median impressions) and a high-impression regime (weight 0.13, log mean 5.16, roughly 174) with much larger dispersion. Standard likelihood-ratio comparisons between mixtures with different component counts have nonregular boundary conditions, so model selection here relies on information criteria with exact parameter counts, held-out likelihood, and stability diagnostics rather than a naive test (Akaike 1974; Schwarz 1978).

The preference for multiple components is not driven by the extreme tail: after excluding the maximum post, BIC still favors two components over one (2,931 versus 3,145), and after excluding the entire top 1 percent it still does (2,738 versus 2,776).

Figure 8 presents the high-impression component posterior over its full range and for probabilities above 0.5.

![Figure 8. Posterior probability of the high-impression component: ECDF over the full range (left) and histogram of posts with probability above 0.5 (right; n = 62). Component weights 0.87/0.13; posterior entropy 0.26.](figures/fig08_mixture_posterior.png)

Posterior high-regime probability varies across observable strata. By format, articles have the highest mean posterior high-regime probability (0.21, n = 88), followed by video (0.13, n = 116), text (0.12, n = 366), and image (0.11, n = 597); the document (n = 5) and poll (n = 2) formats are too sparse for stable estimates and are flagged accordingly in Figure 9. Younger posts have higher mean high-regime probability than mature posts (0.16 versus 0.09), consistent with recent-period reach shifts described in Section 16 rather than with any single mechanism.

![Figure 9. Mean posterior high-regime probability by format with bootstrap 95 percent intervals and group sizes; sparse groups flagged. n = 1,174.](figures/fig09_regime_by_format.png)

Figure 10 presents mean posterior high-regime probability by month on a date axis with bootstrap 95 percent intervals; the data-selected May 2026 break is marked without causal attribution.

![Figure 10. Mean posterior high-regime probability by month on a date axis with bootstrap 95 percent intervals; the data-selected May 2026 break is marked without causal attribution. Months with n of at least 3.](figures/fig10_regime_by_month.png)

A mixture component is a descriptive cluster in outcome space. It is consistent with recorded-impression-regime heterogeneity, including thresholded audience expansion, but it is not evidence that the platform contains a discrete gate, and no component is equated with any proprietary Feed stage.

## 10. Publicly Documented LinkedIn Feed Architecture

LinkedIn publicly describes a Feed that assembles and orders content through several stages. LinkedIn Engineering (2025) describes FishDB, a retrieval engine for scaling the Feed's candidate generation. Naghiaei et al. (2026) describe large-scale retrieval for the Feed using causal language models, applied to out-of-network content. Borisyuk et al. (2024) describe LiRank, the platform's large-scale ranking models. LinkedIn Engineering (2020, 2024) describe dwell-time signals used as ranking objectives alongside click and interaction predictions. Hertel et al. (2026) describe Feed-SR, an industrial-scale sequential recommender for Feed ranking, and LinkedIn Engineering (2026) announced a next-generation Feed combining unified retrieval with a Generative Recommender. LinkedIn Help documentation describes how the Feed ranks content for members and defines the analytics fields creators see. Each of these citations attaches to a specific system; no single generic source is used for multiple distinct systems, and the citation-claim map in the archive records which source supports which sentence.

The documented architecture includes retrieval of a candidate set from the viewer's network and beyond, scoring of candidates against predicted interactions, and a re-ranking layer that can adjust ordering for diversity, integrity, and freshness. LinkedIn publicly states that protected demographic fields are not direct Feed-ranking signals. This is a platform description of intended or documented inputs, not an independent validation of outcome neutrality or of the absence of proxy-mediated effects. The production behavior for this specific account is not observable; the documentation may not reflect every current implementation detail, rollout cohort, or experiment serving this account.

**Pathways to unequal visibility without direct race inputs.** A system does not need an explicit race variable to produce racialized visibility outcomes. Proxy variables, network structure, content semantics, differential user responses, and optimization objectives can generate unequal exposure even when protected-class fields are absent from the documented feature set. The following mechanisms are testable hypotheses; none is claimed to have been proven in this account:

1. Semantic clustering, in which text embeddings route topically similar content to similar and possibly smaller audiences.
2. Network homophily, in which an account's connections shape the reachable audience for a topic.
3. Unequal audience size available for a given topic within and beyond the network.
4. Popularity-weighted retrieval that favors content resembling previously high-engagement posts.
5. Engagement optimization that rewards content eliciting fast, high-volume interaction.
6. Differential reporting behavior by viewers toward particular content.
7. Professional-relevance classification that treats some topics as less on-platform.
8. Recommendation eligibility rules that gate out-of-network distribution.
9. Safety and quality classifiers that reduce distribution of flagged content.
10. Negative-feedback loops in which early low impressions depress later impressions.
11. Unequal out-of-network expansion across topics.
12. Unequal repeat exposure to the same members.
13. Content-language proxies correlated with topic or author identity.
14. Historical interaction feedback that encodes prior audience behavior.
15. Audience-mediated controversy that changes downstream ranking.

Section 23 consolidates these into eight empirically distinguishable hypotheses and specifies the next observation needed for each.

## 11. From Publication to Recorded Impression

Between the moment a post is published and the moment an impression is recorded, several documented stages intervene. In stylized notation, a post j published at time t enters an eligibility filter E(j), joins candidate sets C(v) for viewers v retrieved by in-network and out-of-network retrieval, receives ranking scores s(j, v) from engagement- and dwell-prediction models, passes a re-ranking stage R(j, v) applying integrity, diversity, and freshness adjustments, and finally accumulates recorded impressions Y(j) as the count of delivered displays D(j, v). Equation 3 formalizes the recorded impression count as the terminal output of this chain:

<div style="text-align:center;font-size:1.05em;margin:0.8em 0;">Y(j) = &Sigma;<sub>v</sub> D(j, v), &nbsp;where&nbsp; D(j, v) = f(E(j), C(v), s(j, v), R(j, v)).&nbsp;&nbsp;&nbsp;&nbsp;(Equation 3)</div>

Because the intermediate quantities (candidate membership, rank scores, eligibility decisions, and viewer-level delivery) are not exposed, a regression of Y(j) on post covariates estimates a reduced-form association across the entire pipeline, not the effect of any single stage. Figure 11 encodes this identification structure: observed variables appear as white rounded nodes, unobserved platform stages as gray squares, and partially observed post-treatment quantities (engagement, out-of-network share, members reached) with red edges.

![Figure 11. Mechanism diagram relating documented Feed stages to the recorded impression outcome. White rounded nodes are observed; gray squares are unobserved; red-edged nodes are partially observed and post-treatment. Every arrow reflects the identification argument in the text.](figures/fig23_mechanism_dag.png)

Table 8 summarizes external-evidence and observability boundaries.

**Table 8. External-evidence and observability boundaries.**

| Quantity | Observability in this study | Consequence |
|---|---|---|
| Post content, format, timing | Directly observed | Usable as covariates |
| Post age at collection | Directly observed | Measured confounder; controlled |
| Recorded impressions | Directly observed | Primary outcome |
| Engagement counts | Partially observed (pilot) | Post-treatment; not used as controls |
| Members reached, out-of-network share | Partially observed (pilot, n = 28) | Post-treatment; descriptive only |
| Candidate sets, rank scores, eligibility | Unobserved | Stage-specific effects unidentified |
| Viewer identities and reactions | Unobserved (by design) | Audience mechanisms unidentified |
| Moderation actions | Observed only if explicit | Covert reduction unobservable |

## 12. Explicit Moderation and Covert Distribution Reduction

Explicit moderation and covert distribution reduction are distinct phenomena that the data address differently. Explicit moderation includes content removal, warnings, labeling, account restriction, and other visible enforcement. Covert distribution reduction includes recommendation ineligibility, retrieval exclusion, ranking demotion, reduced out-of-network expansion, and limited repeated exposure, none of which produces a visible notice.

The structured dataset contains no confirmed explicit moderation event. That finding constrains only the explicit-enforcement question. It does not answer whether any post received reduced candidate retrieval, reduced ranking priority, reduced recommendation eligibility, reduced audience expansion, or reduced repeat exposure. A platform can reduce exposure without removing content, and such a reduction would leave no explicit trace in the data collected here. This distinction is central to the study rather than a limitation noted in passing.

## 13. Post Age and Cumulative Measurement

Impressions accumulate over a post's life, and posts were observed at very different ages: the age at collection ranges from 9 hours to 7,573 hours, with quartiles at 1,502, 4,000, and 5,132 hours. Age is therefore a measured confounder, and every adjusted model controls for log age. Because each post contributes one cumulative snapshot, no growth trajectory is observed for most posts, and the analyses in this section are cross-sectional age adjustments, not fixed-age standardization.

The age association is nonlinear. A natural cubic spline on log age (5 degrees of freedom, with format controls) raises R-squared from 0.200 (linear log-age term) to 0.266, and the fitted curve in Figure 12 shows the steepest differences among the youngest posts. Quantile-regression profiles (Section 18) estimate the log-age slope between -0.32 and -0.38 across the 10th to 90th percentiles, so the age gradient is present across the entire conditional distribution, not only at the mean. Interactions are not distinguishable from zero in this sample: log-age by recent-period (p = 0.23) and log-age by image-format (p = 0.11).

Sensitivity analyses exclude the youngest posts. Restricting to posts at least 24 hours old (n = 1,172), at least 72 hours old (n = 1,166), and at least 7 days old (n = 1,118) leaves the median (53, 53, 51) and the concentration profile (Gini 0.800, 0.801, 0.810) essentially unchanged. The dataset's descriptive conclusions are not artifacts of very young posts still accumulating impressions.

The negative cross-sectional age association deserves careful reading, because a naive interpretation (posts lose impressions as they age) is impossible for a cumulative count. Older posts in this dataset were published earlier in the account's history, so the age gradient confounds three things: the mechanical accumulation of impressions with time, secular changes in the account's reach across the study window (including the Section 16 break, which raised recorded impressions for recent posts), and any change in the account's content mix over time. The negative sign indicates that the second and third components dominate: recent posts record more impressions despite having had less time to accumulate. This is exactly why age appears as a control in every adjusted model rather than as a quantity of interest, and why fixed-age snapshots are listed as the decisive future measurement.

![Figure 12. Post age at collection versus recorded impressions on log axes, with a bootstrap-banded cubic fit and posts under 7 days old distinguished. Cross-sectional cumulative measurement, not a growth trajectory. n = 1,174.](figures/fig11_age_vs_impressions.png)

## 14. Sequence Context and Posting Density

After adjusting for age and format, several sequence-context variables show measurable associations with recorded impressions on the log scale. Table 9 reports the frozen estimates; each row is a separate model, and the family of sequence and semantic tests is exploratory.

**Table 9. Sequence and semantic variables (outcome ln(y); HC3 errors; each row a separate adjusted model; exploratory family).**

| Variable | n | Adjusted association | p | Interpretation |
|---|---:|---:|---:|---|
| Posts in previous 24 hours | 1,174 | +1.86% per post | 0.0006 | Modest positive local posting-density association |
| Posts in previous 7 days | 1,174 | -0.03% per post | 0.860 | No distinguishable association |
| Hours since previous post | 1,172 | -0.35% per hour | 0.020 | Small negative spacing association |
| Recent mean impressions (prior 10) | 1,173 | +0.015% per impression | 0.00006 | Positive recorded-impression persistence |
| Same-format streak | 1,174 | -2.14% per step | 0.006 | Fewer recorded impressions in longer same-format runs |
| Semantic novelty vs history | 1,173 | +18.8% per unit | 0.148 | Not distinguishable |
| Similarity to previous 5 posts | 1,173 | +99.8% per unit | 0.039 | Positive; unit is full 0-to-1 similarity range |
| Similarity to prior top-decile posts | 1,154 | positive, wide CI | 0.37 | Not distinguishable |
| Near-duplicate score | 1,173 | small negative | 0.62 | Not distinguishable |
| Local semantic density | 1,173 | -22.5% per unit | 0.004 | Negative crowding association |

These are conditional associations in observational data. They are consistent with sequence-sensitive distribution but do not establish that any sequence variable causes recorded impressions. Recorded-impression persistence (the recent-mean association) is especially ambiguous: it is consistent with autocorrelated audience behavior, topical streaks, or state-dependent ranking, and Section 18's residual-dependence analysis shows that serial correlation must be accounted for when computing uncertainty for any of these estimates.

Figure 13 presents adjusted sequence (left) and semantic (right) associations with ln(impressions), with 95 percent intervals and exact transformation labels.

![Figure 13. Adjusted sequence (left) and semantic (right) associations with ln(impressions), with 95 percent intervals and exact transformation labels. Exploratory family; multiplicity applies.](figures/fig12_sequence_semantic_effects.png)

## 15. Format, Semantic Context, and Aliasing

Text-similarity proxies were computed by fitting a TF-IDF vectorizer to the chronological corpus of all 1,174 available analysis-text fields, consisting mostly of feed previews. Cosine similarities compare each post with its preceding posts, previous high-impression posts, and local semantic neighborhood. Similarity to the previous five posts is positively associated with recorded impressions (p = 0.039), while higher local semantic density is negatively associated with recorded impressions (-22.5 percent, p = 0.004). Because most documents are previews rather than verified full text, these are lexical retrieval proxies, not measurements of LinkedIn's embeddings. Time-respecting validation cautions against overclaiming: adding the sequence and semantic features raises expanding-window mean squared error from 0.906 to 0.969, so these features describe in-sample structure better than they predict out of sample.

Table 10 summarizes format composition (n = 1,174).

**Table 10. Format composition (n = 1,174).**

| Format | Posts | Share |
|---|---:|---:|
| Image | 597 | 50.9% |
| Text | 366 | 31.2% |
| Video | 116 | 9.9% |
| Article | 88 | 7.5% |
| Document | 5 | 0.4% |
| Poll | 2 | 0.2% |

Recorded impressions vary by format, but the design matrix has an exact collinearity: external-link presence and article format are perfectly correlated (correlation 1.00), so their separate effects are not identified and they are treated as aliased. The design matrix of eight standard covariates has rank 7 and a standardized condition number above 10^15. This is a data-design problem: every observed article carries the link indicator, leaving no independent variation with which to estimate separate article and link coefficients. This aliasing is also why external-link status cannot serve as an instrumental variable for any format effect in this dataset: there is no first-stage variation independent of format, and the exclusion restriction (links affecting impressions only through the instrumented channel) is implausible because link presence can affect distribution through multiple direct pathways. A future study would need linked and unlinked posts within comparable formats, specified before observing reach. Document and poll contrasts are too sparse for stable magnitude estimates. The paper therefore reports format composition and identification limits rather than promoting unstable format coefficients.

Figure 14 presents absolute-correlation map of the design matrix with the exact link-article alias highlighted; rank 7 of 8 columns; standardized condition number above 10^15.

![Figure 14. Absolute-correlation map of the design matrix with the exact link-article alias highlighted; rank 7 of 8 columns; standardized condition number above 10^15. n = 1,174.](figures/fig20_alias_map.png)

## 16. Public System Chronology and Structural Breaks

**Change-point estimates.** A single change-point search on the monthly mean of log impressions identifies a break at May 31, 2026, and this location is stable in 95.6 percent of 1,000 bootstrap resamples. The same month is selected when the top 1 percent of posts is excluded and when the maximum post is excluded. Multiple-break procedures on weekly aggregates broadly agree: PELT (Killick, Fearnhead, and Eckley 2012) on the weekly median and weekly mean of log impressions selects a single break in the week ending May 17, 2026, and binary segmentation with two breaks adds a second candidate in late June 2026. A weekly 90th-percentile series places its break earlier (late April 2026), consistent with tail reach moving before central reach. One honesty check tempers the weekly evidence: in placebo permutations that shuffle the weekly series, PELT finds at least one break in about 31 percent of shuffles, so the weekly detection alone is not strongly distinguished from noise; the monthly-mean break with its 95.6 percent bootstrap stability and the covariate-adjusted shift below carry the evidential weight.

Table 11 summarizes structural-break sensitivity (log-impression series; full detail in STRUCTURAL_BREAK_SENSITIVITY_R8.

**Table 11. Structural-break sensitivity (log-impression series; full detail in STRUCTURAL_BREAK_SENSITIVITY_R8.csv).**

| Series | Method | Break location | Stability check |
|---|---|---|---|
| Monthly mean (11 points) | Variance-minimizing single split | 2026-05-31 | 95.6% of 1,000 bootstraps |
| Monthly mean, excl. top 1% | Same | 2026-05-31 | Unchanged |
| Monthly mean, excl. maximum | Same | 2026-05-31 | Unchanged |
| Weekly median (44 points) | PELT (BIC-scaled penalty, min segment 3) | week of 2026-05-17 | Placebo shuffles yield a break 31% of the time |
| Weekly mean (44 points) | PELT | week of 2026-05-17 | Placebo 31% |
| Weekly p90 (42 points) | PELT | week of 2026-04-26 | Tail moves earlier than center |

**Two estimands, not one.** Two magnitudes circulate for the size of the May 2026 shift, and they answer different questions. The unadjusted descriptive estimand compares monthly aggregate mean-log levels: exp(4.77 - 3.76), approximately 2.74, meaning the average monthly mean of log impressions after the break corresponds to roughly 2.7 times higher geometric-mean recorded impressions with no covariate adjustment and monthly aggregation. The covariate-adjusted estimand comes from a post-level segmented model of ln(y) on an after-break indicator with log-age, length, hashtag, and format controls with HC3 errors: a factor of 1.59 (95 percent CI 1.22 to 2.06, p = 0.0005). The descriptive value includes everything that changed across the boundary, including posting composition, format mix, and age structure; the adjusted value estimates the shift holding measured covariates fixed. They are not contradictory, and both are reported with their definitions. Outlier exclusions do not move the break location; age, format, and posting-density controls are what reduce 2.74 toward 1.59.

Figure 15 presents weekly median (top) and monthly mean (bottom) of log impressions with detected breaks, bootstrap stability, and exclusion sensitivity noted in panel titles.

![Figure 15. Weekly median (top) and monthly mean (bottom) of log impressions with detected breaks, bootstrap stability, and exclusion sensitivity noted in panel titles.](figures/fig13_changepoint_series.png)

**Public chronology.** LinkedIn publicly described a Feed redesign on March 12, 2026, combining unified retrieval with a sequential Generative Recommender that processes long interaction histories (LinkedIn Engineering 2026). This announcement precedes the data-selected break by approximately eleven weeks. An announcement date is not an account-level deployment date; production rollouts are typically staged, and no rollout schedule for this account is observable. A segmented model at the announcement date itself estimates a smaller, marginal shift (factor 1.21, p = 0.057). The account's posting volume and composition also changed near this period. The change point is therefore consistent with a system change, a behavior change, or both; the data locate the shift and quantify its stability, and do not attribute it to a specific cause.

Figure 16 presents timeline of publicly documented system publications and the data-selected break, with events staggered above and below the axis.

![Figure 16. Timeline of publicly documented system publications and the data-selected break, with events staggered above and below the axis. Publication dates are not account-level deployment dates.](figures/fig14_public_chronology.png)

## 17. Detailed Analytics: Members Reached, Repetition, and Audience Expansion

**Selection profile of the pilot.** The 29 detailed-analytics posts are a purposefully selected pilot. Compared with the other 1,145 originals, pilot posts are longer (mean 143 versus 60 words, standardized difference 0.68), somewhat younger at collection (standardized difference -0.43), higher in log recorded impressions (standardized difference +0.32; median 78 versus 53; Mann-Whitney p = 0.063), heavier in hashtags (standardized difference +0.29), and twice as likely to sit in the account's top recorded-impression decile (20.7 percent versus 9.8 percent). The pilot's format mix overweights images (17 of 29) and includes single instances of sparse formats. The pilot spans November 2025 through July 2026. These standardized differences establish that the subset is not representative, and no weighting scheme is used to generalize its mechanism estimates, because overlap on text length is poor and stable weights are not available.

**Table 12. Detailed-analytics field availability (from DETAILED_ANALYTICS_FIELD_COVERAGE_R8.csv; 31 pilot records inventoried, 2 reposts excluded, 29 originals attempted).**

| Field | Type | Available | Missing | Denominator used |
|---|---|---:|---:|---:|
| Analytics impressions | count | 29 | 0 | 29 |
| Members reached | count (estimate) | 28 | 1 | 28 |
| Out-of-network share | percentage | 28 | 1 | 28 |
| Reactions, comments, saves | counts | 29 | 0 | 29 |
| Reposts of post | count | 28 | 1 | 28 |
| Profile views, new followers | counts | 29 | 0 | 29 |
| Link clicks | count | 1 | 28 | 1 (link posts only; not analyzed) |

**Feed versus analytics agreement.** For all 29 pilot posts the later analytics impression count is greater than or equal to the earlier feed snapshot, exactly as accumulation implies. The median ratio is 1.005 and the median absolute difference is 1 impression. A Bland-Altman analysis on the log scale gives a mean log difference of 0.040 with limits of agreement -0.218 to 0.297 (Table 13; Figure 17). The log difference declines with post age (Spearman rho -0.45, p = 0.014, n = 29): younger posts gained proportionally more between the two measurements, which is what continuing accumulation predicts. In this purposefully selected pilot, the earlier feed snapshot and later creator-analytics counts show close agreement after accounting for cumulative growth. This comparison does not establish general agreement between measurement systems outside the pilot.

**Table 13. Feed-versus-analytics agreement (n = 29).**

| Quantity | Value |
|---|---|
| Analytics greater than or equal to feed | 29 of 29 |
| Median analytics/feed ratio | 1.005 |
| Median absolute difference | 1 impression |
| Bland-Altman mean log difference | 0.040 |
| Limits of agreement (log) | -0.218 to 0.297 |
| Log difference vs age | rho -0.45, p = 0.014 |

![Figure 17. Feed snapshot versus later analytics impressions with identity line (left) and Bland-Altman log-difference plot with mean and limits of agreement (right). n = 29.](figures/fig15_feed_vs_analytics.png)

**Members reached and repeat exposure.** For the 28 posts with members-reached data, the median repeat-exposure ratio (analytics impressions divided by members reached) is 7.1 (interquartile range 2.7 to 10.8, maximum 27), so a typical pilot post was displayed several times per member reached. The median out-of-network share is 10 percent (interquartile range 3.5 to 47.5 percent, n = 28).

Within this pilot, analytics impressions correlate positively with out-of-network share (Spearman rho 0.71, p = 2.6e-05, n = 28) and negatively with the repeat-exposure ratio (rho -0.62, p = 4.4e-04, n = 28). Posts in the top recorded-impression quartile had a median out-of-network share 52 percentage points higher than the rest (permutation p = 0.040, 5,000 permutations, n = 28).

Within the available detailed-analytics subset, higher impression counts are associated with higher out-of-network share and lower impressions-per-member ratios. This pattern is consistent with audience expansion playing a larger role among higher-impression posts, but the purposefully selected cumulative subset does not identify a causal distribution pathway. Out-of-network share is measured after distribution begins and is jointly determined with impressions, so it is a post-treatment description of how reach decomposed, not an instrument or mediator; no mediation model is estimated, and no imputation of these fields to the remaining 1,145 posts is performed, because a model trained on 28 selected observations has no defensible validation sample and would manufacture mechanism measurements.

*Exploratory pilot analysis; no multiplicity adjustment was applied across these tests.*

Figure 18 presents analytics impressions versus members reached on clean log axes with the one-impression-per-member reference line.

![Figure 18. Analytics impressions versus members reached on clean log axes with the one-impression-per-member reference line. n = 28.](figures/fig16_impressions_vs_reached.png)

Figure 19 presents repeat-exposure ratio against analytics impressions with the bootstrap median band and influential observations marked.

![Figure 19. Repeat-exposure ratio against analytics impressions with the bootstrap median band and influential observations marked. n = 28.](figures/fig17_repeat_exposure.png)

Figure 20 presents out-of-network share against analytics impressions with clean log ticks.

![Figure 20. Out-of-network share against analytics impressions with clean log ticks. Associational; purposefully selected pilot; n = 28.](figures/fig18_oon_vs_impressions.png)

## 18. Predictive Models, Residuals, and Influence

**Residual dependence.** The primary non-race model (ln(y) on log age, length, hashtags, and format; HC3 errors following MacKinnon and White 1985) leaves strongly autocorrelated residuals in posting order: lag-1 autocorrelation 0.29, and Ljung-Box tests reject independence decisively at lags 5, 10, and 20 (all p below 1e-40). Serial dependence matters for inference: the HAC (Newey-West, 10 lags) standard error for the log-age coefficient is 0.045, nearly double the HC3 value of 0.024, and a moving-block bootstrap (block length 25, 1,000 replicates) gives a 95 percent interval of -0.50 to -0.27 around the point estimate -0.33. Non-race uncertainty statements in this paper therefore treat iid-bootstrap and HC3 intervals as lower bounds on uncertainty; the frozen race intervals are not recomputed, and the dependence finding is flagged in Section 19 as a caveat that applies to their nominal precision.

**Predictive benchmark.** A non-causal benchmark asks how predictable recorded impressions are from observable covariates under a chronological three-way split. The one post without a parseable timestamp is excluded: the first 703 posts (September 6, 2025, through March 10, 2026) form the training period, the next 235 (March 16 through June 1, 2026) form a separate calibration period, and the last 235 (June 2 through July 18, 2026) form an untouched test period. Table 14 reports test-set results.

**Table 14. Predictive benchmark (outcome ln recorded impressions; chronological n = 703 training, 235 calibration, 235 test; 90 percent split-conformal intervals calibrated only on separate calibration residuals).**

| Model | MAE | RMSE | Pinball q50 | Pinball q90 | 90% coverage | Mean interval width |
|---|---:|---:|---:|---:|---:|---:|
| Median baseline | 1.223 | not applicable | not applicable | not applicable | not applicable | not applicable |
| Ridge regression | 0.940 | 1.220 | 0.388 | 0.220 | 0.694 | 2.138 |
| Random forest | 0.829 | 1.137 | 0.403 | 0.242 | 0.753 | 2.223 |
| Gradient boosting | 0.915 | 1.208 | 0.454 | 0.238 | 0.915 | 4.435 |

The corrected design fits models only on training observations, computes absolute-residual nonconformity scores only on calibration observations, uses the finite-sample 213th order statistic for nominal 90 percent coverage (Vovk, Gammerman, and Shafer 2005), and evaluates only on test observations. Gradient boosting reaches nominal test coverage with a much wider interval; ridge and random forest remain below nominal coverage. Four contiguous calibration-block sensitivities produce coverage ranges of 0.340 to 0.953 (ridge), 0.634 to 0.911 (random forest), and 0.864 to 0.966 (gradient boosting), showing strong sensitivity to calibration timing. This pattern is compatible with a changing residual scale, but undercoverage alone is not proof of distribution shift. The usual distribution-free marginal coverage guarantee requires exchangeability between calibration and test observations, which a serially dependent chronological platform series may violate. Full dates, widths, order statistics, and sensitivity values are reported in the technical supplement and `R9_PREDICTIVE_INTERVAL_METHOD_NOTE.md`.

**Anomalies and influence.** Age-, time-, and format-adjusted residuals identify 12 posts below the 1st percentile and 12 above the 99th, as expected by construction; the extreme negative residuals are examined individually in the archive without being labeled suppression, because a large negative residual is equally consistent with audience mismatch, timing, or unmodeled content factors. Following Cook (1977), the maximum Cook's distance is 0.041, far below 1, but 49 observations exceed the conventional 4/n screening threshold. Coefficient paths remain sign-stable, indicating distributed rather than single-observation influence (Figure 21). A frozen earlier analysis of 22 author-flagged posts found their mean residual was -0.10 with none below -1.96 standard deviations, so the account owner's suspicion flags were not overrepresented among extreme negative residuals in that frozen result.

![Figure 21. Cook's distance with the 4/n threshold (left) and log-age DFBETA (right), with the most influential posts labeled by index. n = 1,174.](figures/fig19_influence.png)

**Distributional structure.** Quantile-regression profiles (Koenker and Bassett 1978) describe how covariates relate to different parts of the conditional distribution (15 exploratory tests; Benjamini-Hochberg within this family). The log-age gradient is stable across quantiles (-0.32 to -0.38 from q10 to q90, all q-values below 0.001). The text-length association nearly doubles between the median and the 90th percentile (+0.0033 versus +0.0058 per word), meaning longer posts are disproportionately associated with upper-tail reach. The video-format association shows the opposite shape: strongly positive at the 10th percentile (+0.39 log points) and indistinguishable from zero at the 90th (p = 0.66), so video is associated with a higher reach floor rather than a higher ceiling. These are descriptive distributional-regression contrasts, not identified retrieval or ranking effects.

## 19. Direct Black-Centered Content

*All results in Sections 19 through 22 are frozen preliminary results computed from automated labels (PRELIMINARY_AUTOMATED_LABEL_ANALYSIS). The frozen race pipeline used outcome ln(1 + y); no race-dependent model was rerun for this revision.*

Direct Black-centered content was identified by the preliminary classifier in 61 of 1,174 posts. The raw median recorded-impression count is 82 versus 52 for other posts, a median ratio of 1.58, and the geometric means are 80.7 versus 59.5. 62.3 percent of Direct Black-centered posts had recorded impressions at or above the account median, and 13.1 percent met the account 90th-percentile impression threshold versus 9.9 percent of other posts. On unadjusted marginal measures these posts were not low-performing.

The adjusted picture differs. Controlling for measured post characteristics on the log scale:

Table 15 summarizes direct Black-centered frozen results (n = 61 versus 1,113; outcome ln(1 + y) for log models; preliminary labels; frozen).

**Table 15. Direct Black-centered frozen results (n = 61 versus 1,113; outcome ln(1 + y) for log models; preliminary labels; frozen).**

| Model | Estimated effect | 95% CI | Raw p | Across-topic adjustment |
|---|---|---|---:|---:|
| OLS, adjusted (log) | -23.7% | -37.8% to -6.3% | 0.0098 | BH q = 0.078; Holm p = 0.078; Bonferroni p = 0.078 |
| OLS, adjusted + month | -26.2% | -39.8% to -9.5% | 0.0035 | not in the across-topic primary-model family |
| OLS, adjusted + format + month | -26.4% | -39.9% to -9.7% | 0.0033 | not in the across-topic primary-model family |
| Quantile (median) | -24.3% | not retained | 0.0077 | not in the across-topic primary-model family |
| Quantile (p90) | -26.5% | not retained | 0.185 | not in the across-topic primary-model family |
| Logistic, recorded impressions at or above p90 (odds ratio) | 0.45 | 0.17 to 1.20 | 0.108 | not in the across-topic primary-model family |
| Negative binomial, historical frozen sensitivity model with fixed alpha = 1; not the preferred count model | -65.9% | -74.1% to -55.1% | 2.2e-14 | historical sensitivity; not in primary family |

*Precision caveat.* Frozen race intervals use HC3 errors and do not model the serial dependence identified in the non-race residual analysis. Their nominal precision may therefore be greater than a dependence-aware analysis would support. The models remain frozen.

Across the adjusted linear specifications the estimate is approximately -24 percent, with the month-adjusted estimate at -26.2 percent (95 percent CI -39.8 to -9.5, p = 0.0035) and the format-and-month estimate at -26.4 percent (95 percent CI -39.9 to -9.7, p = 0.0033). Following the count-model framework of McCullagh and Nelder (1989), the negative-binomial row is a historical frozen sensitivity model with fixed alpha = 1 and is not the preferred count model: non-race count diagnostics on the full dataset estimate severe overdispersion (Cameron-Trivedi alpha of roughly 50 under the quadratic test; NB2 maximum likelihood alpha = 1.44), so a count model with dispersion fixed at 1 assigns a mean-variance relationship the data reject, and estimated-dispersion results would differ. It is displayed separately in Figure 22 and never averaged with the preferred log-scale models.

Across the frozen family of eight topic-level primary OLS tests, the Direct Black-centered result has a Benjamini-Hochberg q-value of 0.078, a Holm-adjusted p-value of 0.078, and a Bonferroni-adjusted p-value of 0.078. None crosses 0.05. In eight within-month strata, the median within-stratum median difference is +2.25 impressions and the Direct group is lower in 25 percent of strata. In four within-format strata, the corresponding difference is +12.75 impressions and the Direct group is lower in 50 percent. These descriptive stratified summaries do not reproduce the adjusted reduction and are not matched-post counterfactuals. Post-hoc achieved power for the standardized raw-group contrast is 0.69, and the minimum detectable standardized effect at 80 percent power is 0.37; the power calculation addresses the raw contrast, not the adjusted regression estimand, and is contextual only.

![Figure 22. Frozen Direct Black-centered estimates. Left: preferred log-scale models with exact 95 percent CIs and raw p-values; across the eight-topic primary-model family, BH q = 0.078, Holm-adjusted p = 0.078, and Bonferroni-adjusted p = 0.078. Right: historical frozen sensitivity model with fixed alpha = 1, not the preferred count model. Frozen intervals use HC3 errors and omit the serial dependence identified in the non-race residual analysis; nominal precision may exceed dependence-aware precision. Models remain frozen.](figures/fig21_frozen_race_models.png)

The raw and conditional results answer different questions. The higher marginal median shows that the observed Direct Black-centered posts were not uniformly low-performing. The negative adjusted estimates show that, among posts with similar measured characteristics, the model assigns fewer conditional recorded impressions to the Direct Black-centered category. The mechanics of such a sign reversal are worth stating concretely. If Direct Black-centered posts are, on average, longer or otherwise carry covariate values associated with more recorded impressions, then their marginal median can exceed the comparison group's while their conditional estimate is negative: the adjusted model asks whether these posts received the impressions predicted for similar posts and estimates that they fell short of that covariate-implied benchmark. The reversal is therefore evidence that the group's covariate profile differs from the comparison group's, which is itself measurable after validation through balance diagnostics. The data do not currently determine whether the conditional shortfall reflects covariate imbalance beyond the modeled set, omitted variables, label error, model misspecification, heterogeneous effects, or a real conditional recorded-impression difference.

The primary account-level racial-visibility signal is unresolved. Black-centered posts had higher unadjusted median recorded impressions, but several adjusted models estimated approximately 24 percent fewer conditional recorded impressions after controlling for measured post characteristics. That estimate did not survive multiple-testing correction, the analysis had moderate statistical power, and within-month and within-format comparisons did not reproduce the reduction. Because the labels are preliminary and most source text is truncated, the result should be treated as a serious hypothesis for preregistered follow-up rather than evidence confirming or rejecting suppression.

Figure 23 presents uncertainty around the primary frozen estimate, with the zero line, raw p, and Benjamini-Hochberg q-value shown without a binary threshold, plus group sizes and achieved power.

![Figure 23. Uncertainty around the primary frozen estimate, with the zero line, raw p, and Benjamini-Hochberg q-value shown without a binary threshold, plus group sizes and achieved power. Frozen HC3 intervals omit detected serial dependence and may have greater nominal precision than a dependence-aware analysis would support. Verdict: Unresolved; model frozen.](figures/fig22_claimB_uncertainty.png)

## 20. Composite Black-Visibility Group

Table 16 summarizes composite group frozen results (n = 83; union of Direct Black-centered, Black creator or professional issues, Black history, and Black excellence flags; outcome ln(1 + y); preliminary labels; frozen).

**Table 16. Composite group frozen results (n = 83; union of Direct Black-centered, Black creator or professional issues, Black history, and Black excellence flags; outcome ln(1 + y); preliminary labels; frozen).**

| Model | Estimated effect | 95% CI | p |
|---|---|---|---:|
| OLS, adjusted (log) | -10.9% | -27.9% to +10.1% | 0.286 |
| OLS, adjusted + month | -13.9% | -29.8% to +5.7% | 0.154 |
| OLS, adjusted + format + month | -13.9% | -30.0% to +5.9% | 0.156 |
| Negative binomial, historical frozen sensitivity model with fixed alpha = 1; not the preferred count model | -52% | not retained | 3.2e-09 |

The composite group's raw median recorded impressions is 83 versus 52, a ratio of 1.60. Expanding the definition attenuates the estimated negative association. That attenuation may reflect heterogeneity among the added categories, classification differences, or changes in covariate composition. The interval and adjusted inference remain uncertain. The result does not establish a penalty, and it does not establish equal treatment.

## 21. Racial-Justice Content

Racial-justice content was identified in 153 posts. Raw median recorded impressions is 72 versus 51 (ratio 1.41), and 17.0 percent reached the account 90th percentile versus 9.0 percent.

Table 17 summarizes racial-justice group frozen results (n = 153; outcome ln(1 + y); preliminary labels; frozen).

**Table 17. Racial-justice group frozen results (n = 153; outcome ln(1 + y); preliminary labels; frozen).**

| Model | Estimated effect | 95% CI | p |
|---|---|---|---:|
| OLS, adjusted (log) | +3.1% | -11.4% to +19.9% | 0.697 |
| OLS, adjusted + month | -2.1% | -15.5% to +13.5% | 0.782 |
| Quantile (median) | +3.0% | not retained | 0.696 |
| Negative binomial, historical frozen sensitivity model with fixed alpha = 1; not the preferred count model | -25.8% | -38.9% to -9.9% | 0.003 |

The adjusted estimates disagree in sign across specifications. The count model can produce a small p-value with a large coefficient because it assigns a different mean-variance relationship and is highly responsive to the extreme right tail; its fixed alpha = 1 is inconsistent with the estimated full-data dispersion, and it is retained only as the historical sensitivity row. The preliminary broad-group models do not produce a directionally stable racial-justice effect. This result does not establish a recorded-impression penalty, and it does not establish equal treatment. Human classification and stronger mechanism-level measurements remain necessary.

## 22. Black History, Unity, and Culture

Table 18 summarizes narrow subgroup frozen results (n = 19; independently reproduced; outcome ln(1 + y); preliminary labels; frozen).

**Table 18. Narrow subgroup frozen results (n = 19; independently reproduced; outcome ln(1 + y); preliminary labels; frozen).**

| Specification | Estimated effect | p |
|---|---|---:|
| Unadjusted | +32.0% | 0.163 |
| Format and length adjusted | +0.5% | 0.978 |
| Plus month | -10.8% | 0.489 |
| Top outlier excluded | +8.2% | 0.665 |

An exploratory subgroup of 19 posts covering Black history, unity, culture, excellence, and named historical figures had a raw median of 89 versus 53 and a raw mean of approximately 110 versus 228: the subgroup's median is higher while its mean is lower, a mean-median reversal produced by the extreme upper tail of the comparison group. Across specifications the adjusted direction is unstable. Confidence intervals were not retained in the frozen subgroup result and are not reconstructed here, because doing so would require rerunning a race-dependent model.

With only 19 posts, this subgroup is powered (0.25) to detect only large effects; the minimum detectable standardized effect at 80 percent power is 0.65. A null result here is unresolved rather than evidence of equal treatment.

## 23. Competing Explanations

The observed pattern is a divergence between higher unadjusted median recorded impressions and a negative adjusted conditional estimate for Direct Black-centered content. The following explanations are stated as competing hypotheses. None is ranked as most likely, because the current data do not directly compare them.

**Hypothesis 1: Measurement-age and timing differences.** Supporting: Black-centered posts may differ in post age at collection or posting month, and age drives cumulative impressions. Against: the adjusted models control for log age and month, and the negative estimate persists. Next test: repeated analytics snapshots at fixed post ages.

**Hypothesis 2: Format and content-structure differences.** Supporting: Black-centered posts may use formats or lengths associated with lower reach. Against: format- and length-adjusted models retain a negative central estimate; within-format stratified comparisons, however, did not reproduce the reduction. Next test: matched posts of identical format and comparable length differing only in topic.

**Hypothesis 3: Semantic retrieval and audience matching.** Supporting: semantic-density and similarity proxies are associated with reach, and topical content may fall in crowded or poorly matched semantic neighborhoods. Against: semantic proxies are account-level, not category-specific; no candidate-set data exist. Next test: controlled wording substitutions holding topic salience constant.

**Hypothesis 4: Network homophily and audience composition.** Supporting: the account's network composition may limit the out-of-network audience available for Black-centered topics. Against: detailed analytics exist for only 28-29 posts and cannot resolve topic-specific audience availability. Next test: network-composition measurement and multi-account panels.

**Hypothesis 5: Engagement and controversy-mediated effects.** Supporting: differential engagement or controversy could change downstream ranking. Against: engagement decomposition is available only in the pilot and shows no clear category-specific pattern. Next test: viewer-level engagement and reporting traces linked to topic.

**Hypothesis 6: Recommendation eligibility or quality filtering.** Supporting: quality or eligibility classifiers could reduce out-of-network distribution of some topics. Against: eligibility decisions are not exposed; no confirmed enforcement record exists. Next test: platform eligibility or candidate-pool records, or a transparency interface.

**Hypothesis 7: Covert topic-linked ranking reduction.** Supporting: a ranking-stage demotion linked to topic could reduce conditional reach without any visible notice. Against: rank scores are unavailable; the adjusted estimate is equally consistent with covariate imbalance or label error. Next test: rank-score or candidate-set access, or matched-account experiments isolating topic.

**Hypothesis 8: Classification error or model misspecification.** Supporting: preliminary automated labels and truncated source text could misclassify posts, and model form could bias the estimate. Against: the estimate is stable across several linear specifications; but labels are unvalidated and text is mostly truncated. Next test: completion of human-validated labels and specification-robustness checks on validated data.

## 24. Broader Evidence and Product Boundaries

External evidence is presented after the account-level results and is used to identify possible mechanisms and situate the findings, not to determine whether the platform acted fairly.

**LinkedIn creator reports.** Black creators and anti-racist campaigners have publicly reported low reach, posts that appeared to disappear, removals, failed uploads, and suspected topic-linked effects. Joseph (2020) documented concerns from Black professionals on LinkedIn; contemporaneous reporting described similar accounts from multiple creators and LinkedIn's responses (Digiday 2020; Gilmer 2021). These reports constitute a documented and contested pattern. They are not causal proof of suppression, and they are not irrelevant anecdote; they motivate the mechanism tests specified above.

**Independent LinkedIn research.** Geyik, Ambler, and Kenthapadi (2019) documented a fairness-aware re-ranking intervention in LinkedIn Talent Search and its deployment to Recruiter users. That work demonstrates that representation in ranked LinkedIn products can be measured and altered, but it does not establish a disparity in the organic Feed; Talent Search and Recruiter are different products with different inputs and objectives. Research on sociotechnical fairness likewise shows why exposure is a system outcome rather than a property of one score (Selbst et al. 2019). Product boundaries are explicit throughout this paper: adjacent-product findings establish methods and plausible pathways, not findings about the organic Feed or this account.

**Cross-platform evidence.** Independent evidence concerning other platforms documents recommendation disparities, algorithmic moderation effects, and racialized differences in engagement and reporting. This evidence indicates that racialized visibility outcomes occur across recommender systems and can arise without explicit race inputs. It does not establish that any specific mechanism operated on this account, and no claim about broad political causation is made, because the current data do not document a direct, timing-aligned, mechanism-relevant, authoritatively sourced platform change affecting LinkedIn Feed distribution.

## 25. What Stronger Evidence Would Require

**Stronger account-level evidence.** Repeated analytics snapshots at fixed post ages; matched posts differing only in topic; controlled wording substitutions; human-validated labels; preregistration of the account-level test. The archive accompanying this study includes a preregistration draft specifying the post-validation estimands, models, balance diagnostics, sensitivity analyses, and multiple-testing plan.

**Stronger mechanism evidence.** Out-of-network distribution and candidate-pool or eligibility records; account-level network-composition measurement; viewer-level exposure data that separate retrieval, ranking, and audience effects.

**Stronger platform-wide evidence.** Matched accounts and multi-account panels; independent replication across creators and networks; platform transparency or regulator and researcher access sufficient to estimate population-level effects.

**Evidence of intent.** None of the above establishes intent. Intent would require internal documentation, policy records, or system specifications showing a deliberate topic- or identity-linked distribution decision. The current data cannot address intent, and no claim of intent is made.

## 26. Discussion

The dataset supports several robust descriptive conclusions and one unresolved inferential one.

**Concentration is the governing fact.** A Gini near 0.80, a top-1-percent share above 63 percent, and an effective post count of 11.9 mean that recorded exposure is dominated by a handful of posts. The decomposition shows this is not a pooling artifact: concentration appears within months, within formats, and within age strata, while its intensity varies (video posts spread reach much more evenly than image posts). For a single account, the practical meaning is that average reach is nearly meaningless as a planning quantity; the distribution of outcomes, not its mean, is the object a creator experiences.

**The reach process is heterogeneous.** No single tested family fits both body and tail; mixtures improve fit robustly to tail exclusions; and the high-regime share varies by format, month, and age. Together with the pilot's audience-expansion pattern, in which higher impression counts are associated with higher out-of-network share and lower repeat-exposure ratios, the observations are consistent with a reach process in which most posts circulate within a bounded audience while a minority experience qualitatively wider distribution. The documented architecture (retrieval from network and beyond, engagement- and dwell-based ranking, re-ranking) is consistent with such heterogeneity, but consistency is not identification: the mixture components are descriptive, and no component is mapped to a production stage.

**Time and dependence matter.** The May 2026 break (adjusted factor 1.59; descriptive monthly factor 2.74; different estimands) and the strong residual autocorrelation mean that posts are not independent draws. Recorded-impression persistence, posting-density associations, and the predictive models' undercoverage on future data all point to a system, and an account, whose behavior drifts. Uncertainty statements that ignore this dependence are too narrow, which this study addresses for non-race results with HAC errors and block bootstraps, and flags as a caveat for the frozen race intervals.

**Prediction has a ceiling.** Observable covariates halve baseline predictive error, yet substantial residual variation remains, and the most upper-tail-relevant covariate (text length) roughly doubles its association between the median and the 90th percentile. Whatever separates ordinary from exceptional reach in this account is mostly not in the observable covariate set. That is exactly the regime in which unobserved platform-side variables, audience response, or both dominate outcomes, and in which output-only audits reach their identification limit.

**The race signal is genuinely mixed, and reporting it both ways is the finding.** Direct Black-centered content shows higher unadjusted medians and a stable negative adjusted conditional estimate near -24 percent that does not survive family-level correction and is not reproduced in stratified comparisons. The sign reversal between marginal and conditional summaries is not a contradiction to be resolved rhetorically; it is a measured property of the data whose explanation (covariate imbalance, label error, heterogeneous effects, or a real conditional difference) is precisely what the post-validation protocol is designed to distinguish. Applying equal evidentiary standards, the evidence neither confirms nor rejects a recorded-impression penalty.

**Creator-perspective audit value.** For creators, the observability deficit is the central practical fact: a final impression count cannot reveal whether a post entered fewer candidate sets, ranked lower, failed recommendation eligibility, reached a smaller responsive audience, or accumulated fewer repeat displays. Platform transparency that reported standardized-age reach, recommendation eligibility, unique reach, and network decomposition would convert several currently competing hypotheses into testable questions. For researchers, the immediate program is concrete: complete blinded label validation, preregister the primary estimand, collect fixed-age snapshots, and replicate across accounts with measured network composition.

## 27. Limitations

**Measurement.** Impressions are platform-reported display counts whose internal definition is controlled by LinkedIn; the feed-versus-analytics agreement analysis (Section 17) bounds but does not eliminate measurement concerns. Affected results: all. Reduced by: platform measurement documentation and repeated snapshots.

**Selection.** The 29-post analytics pilot is purposefully selected, with quantified standardized differences from the remaining posts. Affected results: all pilot associations. Reduced by: representative analytics collection.

**Text truncation.** 1,145 posts were classified from possibly truncated previews; only 29 have verified full text. Affected results: semantic proxies and all preliminary labels. Reduced by: full-text capture and human review.

**Preliminary labels.** Race-related labels are automated and unvalidated; 459 candidates await review and none is approved. Affected results: Sections 19 through 22. Reduced by: completing the human-review protocol.

**Model uncertainty.** No tested single family fits; mixture component counts are selection-dependent; regression estimates vary across reasonable specifications. Affected results: distributional and adjusted estimates. Reduced by: preregistered specifications.

**Tail uncertainty.** Tail-index estimates are threshold-unstable, and upper-quantile intervals are wide. Affected results: p99 and beyond. Reduced by: more data; no extrapolation is offered.

**Time-varying system.** The platform changed during the window (documented redesign; data-selected break), and residuals are serially dependent. Affected results: any pooled-window estimate. Reduced by: dependence-aware intervals (applied to non-race results) and fixed-age snapshots.

**Post-treatment engagement.** Engagement, out-of-network share, and members reached are downstream of distribution and are never used as controls. Affected results: mechanism interpretation. Reduced by: viewer-level or platform-side data.

**Network unobservability.** Audience composition and homophily are unmeasured. Affected results: audience-based hypotheses. Reduced by: network-composition measurement.

**External validity.** One account, one creator, one network. Affected results: all; nothing here estimates a platform-wide effect. Reduced by: multi-account replication.

**Platform documentation.** Public engineering sources describe intended architecture at publication time, not the configuration serving this account. Affected results: mechanism mapping. Reduced by: transparency or researcher access.

## 28. Future Research

The sequenced program implied by these limits is concrete. First, complete the blinded human review of the 459 race-label candidates under the documented protocol, then execute the preregistered post-validation analyses specified in the archive draft: label agreement and Cohen's kappa; classifier precision, recall, and error rates; approved-label models with the preregistered primary estimand; quantile-effect profiles; balance diagnostics with a matched sensitivity analysis and no causal overclaim; a doubly robust estimator if overlap permits; omitted-variable sensitivity analysis appropriate for continuous log outcomes; and label-uncertainty propagation. Second, collect repeated fixed-age snapshots so growth trajectories replace cumulative cross-sections, enabling the survival-type and trajectory analyses this dataset cannot support. Third, expand detailed-analytics collection toward representativeness so that audience-expansion mechanisms can be estimated with known selection. Fourth, field matched multi-account panels with measured network composition, which are the minimal design for separating audience availability from platform treatment. Fifth, pursue platform or regulator transparency interfaces exposing candidate-set membership, eligibility, and standardized-age reach, which would convert most of Section 23's hypotheses into directly testable questions.

## 29. Conclusion

Recorded impressions for this account are highly concentrated, and a small fraction of posts account for most recorded exposure. Mixture-model and detailed-analytics results are consistent with uneven audience expansion rather than a single global reach process. Public documentation identifies retrieval, semantic matching, sequential ranking, multi-objective optimization, and re-ranking as plausible hidden stages between publication and impression. The account-level racial-visibility signal remains unresolved: Direct Black-centered content shows higher unadjusted medians and a negative adjusted estimate that does not survive correction and is not reproduced in stratified comparisons. The absence of an explicit moderation record does not resolve covert ranking or retrieval questions. Human-validated labels, standardized observation windows, repeated analytics snapshots, and multi-account counterfactuals are required to move further, and independent scrutiny is necessary because creators cannot directly inspect candidate pools, scores, or eligibility decisions.

FeedTrace does not ask readers to accept LinkedIn's assurances or the author's suspicions as the final answer. It creates an independent evidence record from the outputs the platform exposes. That record shows extreme concentration, unequal audience expansion, strong model dependence, and an unresolved conditional difference involving Direct Black-centered content. The next stage is not to declare the platform cleared or guilty. It is to validate the labels, strengthen the counterfactuals, and test the mechanisms capable of producing the observed visibility pattern.

## 30. References

1. Abdollahpouri, H., Burke, R., and Mobasher, B. (2019). Managing popularity bias in recommender systems with personalized re-ranking. Proceedings of FLAIRS 2019. https://arxiv.org/abs/1901.07555
2. Akaike, H. (1974). A new look at the statistical model identification. IEEE Transactions on Automatic Control, 19(6), 716-723.
3. Balkema, A. A., and de Haan, L. (1974). Residual life time at great age. Annals of Probability, 2(5), 792-804. https://doi.org/10.1214/aop/1176996548
4. Benjamini, Y., and Hochberg, Y. (1995). Controlling the false discovery rate: a practical and powerful approach to multiple testing. Journal of the Royal Statistical Society: Series B, 57(1), 289-300.
5. Bland, J. M., and Altman, D. G. (1986). Statistical methods for assessing agreement between two methods of clinical measurement. The Lancet, 327(8476), 307-310.
6. Borisyuk, F., et al. (2024). LiRank: Industrial large scale ranking models at LinkedIn. Proceedings of KDD 2024. https://arxiv.org/abs/2402.06859
7. Cameron, A. C., and Trivedi, P. K. (2013). Regression Analysis of Count Data (2nd ed.). Cambridge University Press.
8. Clauset, A., Shalizi, C. R., and Newman, M. E. J. (2009). Power-law distributions in empirical data. SIAM Review, 51(4), 661-703. https://doi.org/10.1137/070710111
9. Cook, R. D. (1977). Detection of influential observation in linear regression. Technometrics, 19(1), 15-18.
10. Digiday. (2020). On LinkedIn, Black anti-racist campaigners worry they are being censored. https://digiday.com/media/on-linkedin-black-anti-racist-campaigners-worry-theyre-being-censored/
11. Geyik, S. C., Ambler, S., and Kenthapadi, K. (2019). Fairness-aware ranking in search and recommendation systems with application to LinkedIn Talent Search. Proceedings of KDD 2019, 2221-2231. https://doi.org/10.1145/3292500.3330691
12. Gilmer, M. (2021, August 24). As Black users complain of censorship, LinkedIn faces a perception problem. Fast Company. https://www.fastcompany.com/90669854/linkedin-black-censorship-perception-problem
13. Gini, C. (1912). Variabilita e mutabilita. Reprinted in Memorie di metodologia statistica.
14. Hertel, L., et al. (2026). An industrial-scale sequential recommender for LinkedIn Feed ranking. https://arxiv.org/abs/2602.12354
15. Hill, B. M. (1975). A simple general approach to inference about the tail of a distribution. Annals of Statistics, 3(5), 1163-1174.
16. Holm, S. (1979). A simple sequentially rejective multiple test procedure. Scandinavian Journal of Statistics, 6(2), 65-70.
17. Joseph, A. (2020). LinkedIn: The moderator of the Black professional voice? We need answers. https://www.linkedin.com/pulse/linkedin-moderator-black-professional-voice-we-need-answers-joseph
18. Killick, R., Fearnhead, P., and Eckley, I. A. (2012). Optimal detection of changepoints with a linear computational cost. Journal of the American Statistical Association, 107(500), 1590-1598.
19. Koenker, R., and Bassett, G. (1978). Regression quantiles. Econometrica, 46(1), 33-50.
20. LinkedIn Engineering. (2020, May 12). Understanding dwell time to improve LinkedIn Feed ranking. https://www.linkedin.com/blog/engineering/feed/understanding-feed-dwell-time
21. LinkedIn Engineering. (2024). Leveraging dwell time to improve member experiences on the LinkedIn Feed. https://www.linkedin.com/blog/engineering/feed/leveraging-dwell-time-to-improve-member-experiences-on-the-linkedin-feed
22. LinkedIn Engineering. (2025). FishDB: A generic retrieval engine for scaling LinkedIn's Feed. https://www.linkedin.com/blog/engineering/infrastructure/fishdb-a-generic-retrieval-engine-for-scaling-linkedins-feed
23. LinkedIn Engineering. (2026, March 12). Engineering the next generation of LinkedIn's Feed. https://www.linkedin.com/blog/engineering/feed/engineering-the-next-generation-of-linkedins-feed
24. LinkedIn Help. Combined post analytics. https://www.linkedin.com/help/linkedin/answer/a701208
25. LinkedIn Help. How the Feed ranks content. https://www.linkedin.com/help/linkedin/answer/a9554004
26. MacKinnon, J. G., and White, H. (1985). Some heteroskedasticity-consistent covariance matrix estimators with improved finite sample properties. Journal of Econometrics, 29(3), 305-325.
27. McCullagh, P., and Nelder, J. A. (1989). Generalized Linear Models (2nd ed.). Chapman and Hall.
28. Metaxa, D., Park, J. S., Robertson, R. E., Karahalios, K., Wilson, C., Hancock, J., and Sandvig, C. (2021). Auditing algorithms: Understanding algorithmic systems from the outside in. Foundations and Trends in Human-Computer Interaction, 14(4), 272-344.
29. Naghiaei, M., et al. (2026). Large scale retrieval for the LinkedIn Feed using causal language models. Proceedings of AAAI 2026. https://doi.org/10.1609/aaai.v40i47.41445
30. Newey, W. K., and West, K. D. (1987). A simple, positive semi-definite, heteroskedasticity and autocorrelation consistent covariance matrix. Econometrica, 55(3), 703-708.
31. Pickands, J. III. (1975). Statistical inference using extreme order statistics. Annals of Statistics, 3(1), 119-131. https://doi.org/10.1214/aos/1176343003
32. Salganik, M. J., Dodds, P. S., and Watts, D. J. (2006). Experimental study of inequality and unpredictability in an artificial cultural market. Science, 311(5762), 854-856.
33. Sandvig, C., Hamilton, K., Karahalios, K., and Langbort, C. (2014). Auditing algorithms: Research methods for detecting discrimination on internet platforms. Data and Discrimination: Converting Critical Concerns into Productive Inquiry.
34. Schwarz, G. (1978). Estimating the dimension of a model. Annals of Statistics, 6(2), 461-464.
35. Selbst, A. D., boyd, d., Friedler, S. A., Venkatasubramanian, S., and Vertesi, J. (2019). Fairness and abstraction in sociotechnical systems. Proceedings of FAT* 2019, 59-68. https://doi.org/10.1145/3287560.3287598
36. Vovk, V., Gammerman, A., and Shafer, G. (2005). Algorithmic Learning in a Random World. Springer.
