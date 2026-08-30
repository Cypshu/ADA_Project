"""Independent consistency checks and rubric diagnostics for the Santander project.

The script does not tune on the stored hold-out. It verifies saved metrics and uses the
existing training/validation split for the learning-size and PCA diagnostics.
"""

from __future__ import annotations

import json
import time
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.stats import ttest_ind
from sklearn.decomposition import PCA
from sklearn.metrics import (
    average_precision_score,
    balanced_accuracy_score,
    brier_score_loss,
    confusion_matrix,
    f1_score,
    matthews_corrcoef,
    precision_recall_curve,
    precision_score,
    recall_score,
    roc_auc_score,
)
from sklearn.naive_bayes import GaussianNB
from sklearn.preprocessing import StandardScaler


RANDOM_STATE = 42
RUN_NAME = "20260815_030409_NB_ANN"
MODEL_NAMES = [
    "NB | standard",
    "NB | EDA-adapted",
    "ANN | small",
    "ANN | EDA-adapted",
]

CYP_ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = CYP_ROOT / "data" / "santander_customer_transaction_prediction.csv"
RUN_DIR = CYP_ROOT / "ML" / "runs" / RUN_NAME
OUTPUT_DIR = CYP_ROOT / "ML" / "verification"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def benjamini_hochberg(p_values: pd.Series) -> pd.Series:
    """Return BH-adjusted p-values while preserving feature labels."""

    values = p_values.to_numpy(dtype=float)
    order = np.argsort(values)
    ranked = values[order]
    adjusted_ranked = np.minimum.accumulate(
        (ranked * len(values) / np.arange(1, len(values) + 1))[::-1]
    )[::-1]
    adjusted = np.empty_like(adjusted_ranked)
    adjusted[order] = np.minimum(adjusted_ranked, 1.0)
    return pd.Series(adjusted, index=p_values.index, name="p_value_fdr_bh")


def recompute_test_metrics(y_true: np.ndarray, probability: np.ndarray, threshold: float) -> dict:
    prediction = (probability >= threshold).astype(int)
    tn, fp, fn, tp = confusion_matrix(y_true, prediction, labels=[0, 1]).ravel()
    return {
        "roc_auc": roc_auc_score(y_true, probability),
        "average_precision": average_precision_score(y_true, probability),
        "brier_score": brier_score_loss(y_true, probability),
        "balanced_accuracy": balanced_accuracy_score(y_true, prediction),
        "precision": precision_score(y_true, prediction, zero_division=0),
        "recall": recall_score(y_true, prediction, zero_division=0),
        "f1": f1_score(y_true, prediction, zero_division=0),
        "mcc": matthews_corrcoef(y_true, prediction),
        "specificity": tn / (tn + fp),
        "tn": int(tn),
        "fp": int(fp),
        "fn": int(fn),
        "tp": int(tp),
    }


def prediction_filename(model_name: str, split: str) -> Path:
    slug = model_name.replace(" | ", "_").replace(" ", "_")
    return RUN_DIR / "predictions" / f"{slug}_{split}.csv"


def main() -> None:
    started = time.perf_counter()
    data = pd.read_csv(DATA_PATH)
    feature_columns = [column for column in data.columns if column != "target"]
    x = data[feature_columns].astype(np.float32)
    y = data["target"].astype(int).to_numpy()

    data_checks = {
        "rows": int(len(data)),
        "features": int(len(feature_columns)),
        "positive_count": int(y.sum()),
        "positive_share": float(y.mean()),
        "missing_cells": int(data.isna().sum().sum()),
        "non_finite_feature_cells": int((~np.isfinite(x.to_numpy())).sum()),
        "constant_features": int((x.nunique(dropna=False) <= 1).sum()),
    }

    # Independent EDA check: keep p-values keyed by feature name throughout.
    false_values = x.loc[y == 0]
    true_values = x.loc[y == 1]
    n_false, n_true = len(false_values), len(true_values)
    pooled_std = np.sqrt(
        (
            (n_false - 1) * false_values.var(ddof=1)
            + (n_true - 1) * true_values.var(ddof=1)
        )
        / (n_false + n_true - 2)
    )
    cohens_d = (true_values.mean() - false_values.mean()) / pooled_std
    raw_p = pd.Series(
        {
            feature: ttest_ind(
                false_values[feature], true_values[feature], equal_var=False
            ).pvalue
            for feature in feature_columns
        },
        name="p_value_welch",
    )
    fdr_table = pd.DataFrame(
        {
            "cohens_d": cohens_d,
            "abs_cohens_d": cohens_d.abs(),
            "p_value_welch": raw_p,
            "p_value_fdr_bh": benjamini_hochberg(raw_p),
        }
    )
    fdr_table["significant_fdr_0.05"] = fdr_table["p_value_fdr_bh"] < 0.05
    fdr_table.sort_values("p_value_fdr_bh").to_csv(
        OUTPUT_DIR / "eda_welch_fdr_corrected.csv"
    )

    split_indices = pd.read_csv(RUN_DIR / "split_indices.csv")
    idx_train = split_indices.loc[split_indices["split"] == "train", "row_index"].to_numpy()
    idx_val = split_indices.loc[
        split_indices["split"] == "validation", "row_index"
    ].to_numpy()
    idx_test = split_indices.loc[split_indices["split"] == "test", "row_index"].to_numpy()

    saved_results = pd.read_csv(RUN_DIR / "results.csv").set_index("model")
    metric_rows = []
    threshold_checks = []
    for model_name in MODEL_NAMES:
        test_predictions = pd.read_csv(prediction_filename(model_name, "test"))
        threshold = float(test_predictions["tuned_threshold"].iloc[0])
        recalculated = recompute_test_metrics(
            test_predictions["true_label"].to_numpy(),
            test_predictions["probability_target_1"].to_numpy(),
            threshold,
        )
        row = {"model": model_name, "threshold": threshold, **recalculated}
        comparable = [
            "roc_auc",
            "average_precision",
            "brier_score",
            "balanced_accuracy",
            "precision",
            "recall",
            "f1",
            "mcc",
            "specificity",
        ]
        row["max_abs_difference_to_results_csv"] = max(
            abs(float(recalculated[key]) - float(saved_results.loc[model_name, key]))
            for key in comparable
        )
        metric_rows.append(row)

        validation_predictions = pd.read_csv(prediction_filename(model_name, "validation"))
        precision, recall, thresholds = precision_recall_curve(
            validation_predictions["true_label"],
            validation_predictions["probability_target_1"],
        )
        f1_values = np.divide(
            2 * precision[:-1] * recall[:-1],
            precision[:-1] + recall[:-1],
            out=np.zeros_like(thresholds),
            where=(precision[:-1] + recall[:-1]) > 0,
        )
        recalculated_threshold = float(thresholds[int(np.argmax(f1_values))])
        threshold_checks.append(
            {
                "model": model_name,
                "saved_threshold": threshold,
                "recalculated_validation_f1_threshold": recalculated_threshold,
                "absolute_difference": abs(threshold - recalculated_threshold),
            }
        )

    metric_verification = pd.DataFrame(metric_rows)
    metric_verification.to_csv(OUTPUT_DIR / "ml_metric_verification.csv", index=False)
    threshold_verification = pd.DataFrame(threshold_checks)
    threshold_verification.to_csv(
        OUTPUT_DIR / "ml_threshold_verification.csv", index=False
    )

    # Requirement-oriented learning-size diagnostic, using validation only.
    x_train = x.iloc[idx_train]
    y_train = y[idx_train]
    x_val = x.iloc[idx_val]
    y_val = y[idx_val]
    rng = np.random.default_rng(RANDOM_STATE)
    learning_rows = []
    for fraction in [0.01, 0.05, 0.10, 0.25, 0.50, 1.00]:
        if fraction == 1.0:
            selected = np.arange(len(x_train))
        else:
            negative = np.flatnonzero(y_train == 0)
            positive = np.flatnonzero(y_train == 1)
            selected = np.concatenate(
                [
                    rng.choice(negative, max(1, round(len(negative) * fraction)), replace=False),
                    rng.choice(positive, max(1, round(len(positive) * fraction)), replace=False),
                ]
            )
            rng.shuffle(selected)
        model = GaussianNB().fit(x_train.iloc[selected], y_train[selected])
        probability = model.predict_proba(x_val)[:, 1]
        learning_rows.append(
            {
                "training_fraction": fraction,
                "training_rows": int(len(selected)),
                "validation_average_precision": average_precision_score(y_val, probability),
                "validation_roc_auc": roc_auc_score(y_val, probability),
            }
        )
    learning_curve = pd.DataFrame(learning_rows)
    learning_curve.to_csv(OUTPUT_DIR / "nb_learning_curve.csv", index=False)

    fig, ax = plt.subplots(figsize=(8.5, 5.2))
    ax.plot(
        learning_curve["training_rows"],
        learning_curve["validation_average_precision"],
        marker="o",
        label="Validation Average Precision",
    )
    ax.plot(
        learning_curve["training_rows"],
        learning_curve["validation_roc_auc"],
        marker="o",
        label="Validation ROC-AUC",
    )
    ax.axhline(y_val.mean(), color="grey", linestyle="--", label="AP-Nullreferenz")
    ax.set_xscale("log")
    ax.set_xlabel("Anzahl Trainingsbeobachtungen (log-Skala)")
    ax.set_ylabel("Metrik")
    ax.set_title("GaussianNB: Einfluss der Trainingsmenge")
    ax.grid(alpha=0.25)
    ax.legend()
    fig.tight_layout()
    fig.savefig(OUTPUT_DIR / "nb_learning_curve.png", dpi=200, bbox_inches="tight")
    plt.close(fig)

    # Train-only PCA diagnostic: does linear compression improve validation AP?
    scaler = StandardScaler()
    x_train_scaled = scaler.fit_transform(x_train).astype(np.float32)
    x_val_scaled = scaler.transform(x_val).astype(np.float32)
    pca = PCA(n_components=100, svd_solver="randomized", random_state=RANDOM_STATE)
    x_train_pca = pca.fit_transform(x_train_scaled).astype(np.float32)
    x_val_pca = pca.transform(x_val_scaled).astype(np.float32)

    pca_rows = [
        {
            "components": 200,
            "variant": "ohne PCA",
            "cumulative_explained_variance": 1.0,
            "validation_average_precision": float(
                saved_results.loc["NB | standard", "average_precision"]
            ),
            "validation_roc_auc": np.nan,
        }
    ]
    # The saved results.csv contains test metrics; recompute the no-PCA validation reference.
    raw_reference = GaussianNB().fit(x_train, y_train).predict_proba(x_val)[:, 1]
    pca_rows[0]["validation_average_precision"] = average_precision_score(
        y_val, raw_reference
    )
    pca_rows[0]["validation_roc_auc"] = roc_auc_score(y_val, raw_reference)
    for components in [10, 25, 50, 100]:
        model = GaussianNB().fit(x_train_pca[:, :components], y_train)
        probability = model.predict_proba(x_val_pca[:, :components])[:, 1]
        pca_rows.append(
            {
                "components": components,
                "variant": f"PCA {components}",
                "cumulative_explained_variance": float(
                    pca.explained_variance_ratio_[:components].sum()
                ),
                "validation_average_precision": average_precision_score(y_val, probability),
                "validation_roc_auc": roc_auc_score(y_val, probability),
            }
        )
    pca_validation = pd.DataFrame(pca_rows).sort_values("components")
    pca_validation.to_csv(OUTPUT_DIR / "nb_pca_validation.csv", index=False)

    fig, ax = plt.subplots(figsize=(8.5, 5.2))
    pca_only = pca_validation[pca_validation["variant"] != "ohne PCA"]
    ax.plot(
        pca_only["components"],
        pca_only["validation_average_precision"],
        marker="o",
        label="GaussianNB mit PCA",
    )
    raw_ap = float(
        pca_validation.loc[pca_validation["variant"] == "ohne PCA", "validation_average_precision"].iloc[0]
    )
    ax.axhline(raw_ap, color="black", linestyle="--", label=f"ohne PCA: AP={raw_ap:.3f}")
    ax.axhline(y_val.mean(), color="grey", linestyle=":", label="AP-Nullreferenz")
    ax.set_xlabel("Anzahl PCA-Komponenten")
    ax.set_ylabel("Validation Average Precision")
    ax.set_title("Train-only PCA: Prüfung der Dimensionsreduktion")
    ax.grid(alpha=0.25)
    ax.legend()
    fig.tight_layout()
    fig.savefig(OUTPUT_DIR / "nb_pca_validation.png", dpi=200, bbox_inches="tight")
    plt.close(fig)

    summary = {
        "data_checks": data_checks,
        "eda": {
            "fdr_significant_features": int(fdr_table["significant_fdr_0.05"].sum()),
            "max_abs_cohens_d": float(fdr_table["abs_cohens_d"].max()),
            "top_abs_cohens_d_feature": str(fdr_table["abs_cohens_d"].idxmax()),
        },
        "ml": {
            "max_metric_recalculation_difference": float(
                metric_verification["max_abs_difference_to_results_csv"].max()
            ),
            "max_threshold_recalculation_difference": float(
                threshold_verification["absolute_difference"].max()
            ),
            "learning_curve_best_validation_ap": float(
                learning_curve["validation_average_precision"].max()
            ),
            "pca_best_validation_ap": float(
                pca_validation.loc[
                    pca_validation["variant"] != "ohne PCA",
                    "validation_average_precision",
                ].max()
            ),
            "no_pca_validation_ap": raw_ap,
        },
        "methodological_limit": (
            "The ML hold-out indices are identical to the split already scored by the EDA "
            "logistic reference; results are internally reproducible but not fully blind "
            "with respect to the complete project analysis."
        ),
        "runtime_seconds": time.perf_counter() - started,
    }
    (OUTPUT_DIR / "verification_summary.json").write_text(
        json.dumps(summary, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    print(json.dumps(summary, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
