import streamlit as st

st.set_page_config(page_title="Mortar Cost Calculator", layout="centered")
st.title("💰 Mortier Sec – Calculateur de Coût Personnalisé")
st.caption("Par Omar 🇲🇦 — entrez vos prix, quantités, et options")

# 📥 Batch size input
batch_kg = st.number_input("⚖️ Taille du lot (kg)", min_value=25, value=1000, step=25)

# 🧱 Material prices
st.subheader("🔧 Prix des matériaux (MAD/tonne)")
cement_price = st.number_input("💠 Ciment (CEM II 42.5)", value=1300)
lime_price = st.number_input("🟩 Chaux aérienne", value=1800)
sand_price = st.number_input("🪨 Sable concassé", value=120)
kaolin_price = st.number_input("🧼 Kaolin (Argile blanche)", value=150)

# 📦 Overhead costs
st.subheader("📦 Coûts fixes")
packaging_cost = st.number_input("📦 Emballage (par tonne)", value=150)
labor_cost = st.number_input("👷 Main d'œuvre (par tonne)", value=100)
transport_cost = st.number_input("🚚 Transport (par tonne)", value=150)

# 🧪 Additive toggle
st.subheader("🧪 Additif Hydrofuge (optionnel)")
use_hydrofuge = st.toggle("✅ Ajouter Sika Poudre Hydrofuge", value=False)
hydrofuge_price = st.number_input("💧 Prix Sika Poudre Hydrofuge (MAD/tonne)", value=3800)
hydrofuge_dosage = st.number_input("🧪 Dosage utilisé (kg/tonne)", value=10.0)

# ⚙️ Recipe ratios based on 1000 kg batch
cement_pct = 0.25      # 250 kg
lime_pct = 0.015       # 15 kg
kaolin_pct = 0.005     # 5 kg
sand_pct = 0.73        # 730 kg

cement_kg = batch_kg * cement_pct
lime_kg = batch_kg * lime_pct
kaolin_kg = batch_kg * kaolin_pct
sand_kg = batch_kg * sand_pct
hydrofuge_kg = batch_kg * (hydrofuge_dosage / 1000) if use_hydrofuge else 0

# 💰 Cost calculations
material_cost = (
    (cement_kg / 1000) * cement_price +
    (lime_kg / 1000) * lime_price +
    (kaolin_kg / 1000) * kaolin_price +
    (sand_kg / 1000) * sand_price +
    (hydrofuge_kg / 1000) * hydrofuge_price
)

fixed_costs = packaging_cost + labor_cost + transport_cost
total_cost = material_cost + fixed_costs

# 📊 Output
st.subheader("📊 Résultat")
st.write(f"💰 Coût total pour {batch_kg} kg : **{round(total_cost, 2)} MAD**")
st.write(f"📦 ≈ **{round(total_cost / batch_kg * 25, 2)} MAD** par sac de 25 kg")
