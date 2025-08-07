import streamlit as st
import pandas as pd

# 1. Configuration de la page
st.set_page_config(page_title="Mortar Cost Calculator", layout="centered")
st.title("💰 Mortier Sec – Calculateur de Coût Personnalisé")
st.caption("Par Omar 🇲🇦 — Prix en MAD/t, quantités en kg")

# 2. Taille du lot cible
batch_target_kg = st.number_input(
    "⚖️ Taille du lot cible (kg)",
    min_value=0.0, value=1000.0, step=25.0
)

# 3. Prix par ingrédient (MAD/tonne)
st.subheader("🔧 Prix des matériaux")
material_names  = ["Ciment", "Chaux", "Sable", "HPMC"]
material_labels = [
    "💠 Ciment (CEM I 42.5)",
    "🟩 Chaux aérienne CL90",
    "🪨 Sable lavé 0–2 mm",
    "📌 HPMC ou TYLOSE®"
]
default_prices  = [1300.0, 1800.0, 120.0, 3600.0]

prices = {
    name: st.number_input(label, value=price)
    for name, label, price in zip(material_names, material_labels, default_prices)
}

# Option hydrophuge
add_hydro = st.checkbox("✅ Ajouter Sika Poudre Hydrofuge")
if add_hydro:
    prices["Hydrofuge"] = st.number_input(
        "💧 Sika Poudre Hydrofuge (MAD/tonne)", value=3800.0
    )
    hydro_pct = st.number_input(
        "🧪 Dosage hydrophuge (kg/tonne)", value=1.2, step=0.1
    ) / 1000

# 4. Pourcentages de recette par tonne
ratios = {
    "Ciment": 0.27,
    "Chaux":  0.04,
    "Sable":  0.685,
    "HPMC":   0.0035
}
if add_hydro:
    ratios["Hydrofuge"] = hydro_pct

# 5. Quantités par ingrédient (kg/tonne) — personnalisables
st.subheader("⚖️ Quantités par ingrédient (kg/tonne)")
quantities = {}
for name, pct in ratios.items():
    default_qty     = 1000 * pct
    quantities[name] = st.number_input(
        f"{name} (kg/tonne)",
        min_value=0.0, value=round(default_qty, 2), step=0.1
    )

# 6. Calcul des coûts matière par tonne
rows = []
for name, qty in quantities.items():
    cost = qty / 1000 * prices[name]
    rows.append({
        "Ingrédient":    name,
        "Quantité (kg/t)": round(qty, 2),
        "Prix (MAD/t)":  round(prices[name], 2),
        "Coût (MAD/t)":  round(cost, 2)
    })
df_material     = pd.DataFrame(rows)
material_cost_t = df_material["Coût (MAD/t)"].sum()

# 7. Coûts fixes
st.subheader("📦 Coûts fixes")
overhead_labels   = ["Emballage", "Main d'œuvre", "Transport"]
overhead_defaults = [150.0, 100.0, 150.0]
overheads = {
    label: st.number_input(f"📦 {label} (MAD/tonne)", value=val)
    for label, val in zip(overhead_labels, overhead_defaults)
}

batch_fixed_cost = st.number_input(
    "🛠️ Coût fixe par lot (MAD, ex: mise en route)", value=0.0, step=100.0
)

# 8. Calculs
fixed_per_ton        = sum(overheads.values())
fixed_variable_total = fixed_per_ton * (batch_target_kg / 1000)
fixed_total          = fixed_variable_total + batch_fixed_cost

total_cost_per_ton   = material_cost_t + fixed_per_ton
cost_per_25kg        = total_cost_per_ton / 1000 * 25
total_batch_cost     = total_cost_per_ton * (batch_target_kg / 1000) + batch_fixed_cost

# 9. Affichage
st.subheader("📊 Détail des coûts matière par tonne")
st.table(df_material)

st.write(f"🔧 Coût matière par tonne : **{material_cost_t:.2f} MAD**")
st.write(f"📦 Coût fixe par tonne : **{fixed_per_ton:.2f} MAD**")
st.write(f"💰 Coût total par tonne : **{total_cost_per_ton:.2f} MAD**")
st.write(f"📦 ≈ **{cost_per_25kg:.2f} MAD** par sac de 25 kg")

st.subheader("📦 Coûts pour le lot cible")
st.write(f"Taille du lot : **{batch_target_kg:.2f} kg**")
st.write(f"Coût total du lot : **{total_batch_cost:.2f} MAD**")
st.write(f"Coût fixe additionnel par lot : **{batch_fixed_cost:.2f} MAD**")
