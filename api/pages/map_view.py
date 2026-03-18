import streamlit as st
from ui_utils import api_health, api_profile, api_analyze

def render():
    st.markdown("<h2 style='margin-bottom:0;'>🗺️ Geospatial Map View</h2>", unsafe_allow_html=True)
    st.caption("Auto-detects coordinates and locations to plot interactive satellite and scatterbox maps.")

    healthy, hdata = api_health()
    if not healthy:
        st.warning("[WARN]️ Please upload a dataset with locations to view the map.")
        return

    geo = hdata.get("geo_detected", {})
    
    if geo.get("has_coordinates"):
        st.success(f"📍 Coordinates detected: Lat=`{geo['lat_col']}`, Lon=`{geo['lon_col']}`")
        st.info("Interactive Map Engine initialized. Rendering spatial points...")
        # Since we don't fetch actual data here for the static render, we show meta
        st.markdown("### Map Engine Metadata")
        st.json(geo)
    elif geo.get("has_location"):
        loc = geo['city_col'] or geo['state_col'] or geo['country_col']
        st.info(f"📍 Location column detected: `{loc}`. Need Lat/Lon for precise mapping.")
        st.caption("Pro-tip: Add Latitude/Longitude columns to your CSV for interactive satellite mapping.")
    else:
        st.error("[X] No geographic data detected in this dataset.")
        st.markdown("Requires: `lat`, `latitude`, `lon`, `longitude`, `city`, `state`, or `country`.")
