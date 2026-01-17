'''Feature description mapping'''

FEATURE_DESCRIPTIONS = {
    "Amount_scaled": "Transaction amount (scaled)",
    "Time_scaled": "Transaction time since first transaction (scaled)",
    **{f"V{i}": f"PCA component {i}" for i in range(1, 29)}
}
