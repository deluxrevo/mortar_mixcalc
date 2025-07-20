import streamlit as st

st.set_page_config(page_title="Mortar Cost Calculator", layout="centered")
st.title("💰 Mortier Sec – Calculateur de Coût Personnalisé")
st.caption("Par Omar 🇲🇦 — entrez vos prix, quantités, et options")

# 📥 Batch size input
batch_kg = st.number_input("⚖️ Taille du lot (kg)", min_value=25, value=1000, step=25)

# 🧱 Material prices
st.subheader("🔧 Prix des matériaux (MAD/tonne)")
cement_price = st.number_input("💠 Ciment (CEM II 42.5)", value=1300)
hpmc_price = st.number_input("🌿 HPMC", value=4000)
sand_price = st.number_input("🪨 Sable concassé", value=120)

# 📦 Overhead costs
st.subheader("📦 Coûts fixes")
packaging_cost = st.number_input("📦 Emballage (par tonne)", value=150)
labor_cost = st.number_input("👷 Main d'œuvre (par tonne)", value=100)
transport_cost = st.number_input("🚚 Transport (par tonne)", value=150)

# 🧪 Plasticizer toggle
st.subheader("🧪 Additifs Plastifiants (optionnels)")
use_plastifier = st.toggle("✅ Ajouter plastifiant Sika (ex: Plastiment-60 M)", value=False)

plastifier_price = st.number_input("💧 Prix plastifiant (MAD/25kg bidon)", value=550)
plastifier_dosage = st.number_input("🧪 Dosage utilisé (kg/tonne)", value=0.5)

# ⚙️ Recipe ratios
cement_pct = 0.25
hpmc_pct = 0.015
sand_pct = 0.735

cement_kg = batch_kg * cement_pct
hpmc_kg = batch_kg * hpmc_pct
sand_kg = batch_kg * sand_pct

# 💰 Cost calculations
material_cost = (
    (cement_kg / 1000) * cement_price +
    (hpmc_kg / 1000) * hpmc_price +
    (sand_kg / 1000) * sand_price
)

fixed_costs = packaging_cost + labor_cost + transport_cost

additive_cost = 0
if use_plastifier:
    additive_cost = (plastifier_dosage / 25) * plastifier_price  # cost per kg from 25kg price

total_cost = material_cost + fixed_costs + additive_cost

# 📊 Output
st.subheader("📊 Résultat")
st.write(f"💰 Coût total pour {batch_kg} kg : **{round(total_cost, 2)} MAD**")
st.write(f"📦 ≈ **{round(total_cost / batch_kg * 25, 2)} MAD** par sac de 25 kg")
