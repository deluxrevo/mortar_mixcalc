import streamlit as st
import pandas as pd

st.set_page_config(page_title="Mortar Cost Calculator", layout="centered")
st.title("💰 Mortier Sec – Calculateur de Coût Personnalisé")
st.caption("Par Omar 🇲🇦 — entrez vos prix, quantités, et options")

# 📥 Batch size input (sera recalculé si on customise les quantités)
batch_kg = st.number_input(
    "⚖️ Taille du lot (kg)", min_value=0.0, value=1000.0, step=25.0
)

# 🧱 Prix des matériaux (MAD/tonne)
st.subheader("🔧 Prix des matériaux (MAD/tonne)")
cement_price = st.number_input("💠 Ciment (CEM I 42.5)", value=1300.0)
lime_price   = st.number_input("🟩 Chaux aérienne CL90",   value=1800.0)
sand_price   = st.number_input("🪨 Sable lavé 0–2 mm",     value=120.0)
hpmc_price   = st.number_input("📌 HPMC ou TYLOSE®",       value=3600.0)

# 📦 Coûts fixes (MAD/tonne)
st.subheader("📦 Coûts fixes")
packaging_cost = st.number_input("📦 Emballage", value=150.0)
labor_cost     = st.number_input("👷 Main d'œuvre", value=100.0)
transport_cost = st.number_input("🚚 Transport",    value=150.0)

# 🧪 Additif Hydrofuge (optionnel)
st.subheader("🧪 Additif Hydrofuge")
use_hydrofuge  = st.toggle("✅ Ajouter Sika Poudre Hydrofuge", value=False)
hydrofuge_price = st.number_input(
    "💧 Prix Sika Poudre Hydrofuge (MAD/tonne)", value=3800.0
)
hydrofuge_dosage = st.number_input(
    "🧪 Dosage (kg/tonne)", value=1.2
)

# ⚙️ Ratios de recette par défaut (basés sur 1000 kg)
cement_pct = 0.27
lime_pct   = 0.04
sand_pct   = 0.685
hpmc_pct   = 0.0035

# quantités par défaut
cement_kg   = batch_kg * cement_pct
lime_kg     = batch_kg * lime_pct
sand_kg     = batch_kg * sand_pct
hpmc_kg     = batch_kg * hpmc_pct
hydrofuge_kg = batch_kg * (hydrofuge_dosage / 1000) if use_hydrofuge else 0.0

# ⚖️ Permet de personnaliser chaque quantité
st.subheader("⚖️ Quantités personnalisées (kg)")
cement_kg = st.number_input("💠 Ciment (kg)", min_value=0.0, value=cement_kg)
lime_kg   = st.number_input("🟩 Chaux (kg)",   min_value=0.0, value=lime_kg)
sand_kg   = st.number_input("🪨 Sable (kg)",   min_value=0.0, value=sand_kg)
hpmc_kg   = st.number_input("📌 HPMC (kg)",    min_value=0.0, value=hpmc_kg)

if use_hydrofuge:
    hydrofuge_kg = st.number_input(
        "💧 Hydrofuge (kg)", min_value=0.0, value=hydrofuge_kg
    )
else:
    hydrofuge_kg = 0.0

# recalcul du batch total en fonction des quantités saisies
batch_kg = cement_kg + lime_kg + sand_kg + hpmc_kg + hydrofuge_kg

# 💰 Calcul des coûts matières
items = [
    ("Ciment", cement_kg, cement_price),
    ("Chaux",  lime_kg,   lime_price),
    ("Sable",  sand_kg,   sand_price),
    ("HPMC",   hpmc_kg,   hpmc_price),
]

if use_hydrofuge:
    items.append(("Hydrofuge", hydrofuge_kg, hydrofuge_price))

rows = []
for name, qty, price in items:
    cost = (qty / 1000) * price
    rows.append({
        "Ingrédient": name,
        "Quantité (kg)": round(qty, 2),
        "Prix (MAD/t)": round(price, 2),
        "Coût (MAD)": round(cost, 2)
    })

df = pd.DataFrame(rows)

# coûts fixes totaux (MAD)
fixed_per_ton = packaging_cost + labor_cost + transport_cost
fixed_total   = fixed_per_ton * (batch_kg / 1000)

material_cost = df["Coût (MAD)"].sum()
total_cost    = material_cost + fixed_total
cost_per_25   = total_cost / batch_kg * 25

# 📊 Affichage
st.subheader("📊 Détail des coûts matière")
st.table(df)

st.subheader("📦 Coûts fixes")
st.write(f"Coût fixe par tonne : {round(fixed_per_ton,2)} MAD")
st.write(f"Coût fixe total pour {round(batch_kg,2)} kg : {round(fixed_total,2)} MAD")

st.subheader("💰 Résultat global")
st.write(f"Coût total pour {round(batch_kg,2)} kg : **{round(total_cost,2)} MAD**")
st.write(f"≈ **{round(cost_per_25,2)} MAD** par sac de 25 kg")
