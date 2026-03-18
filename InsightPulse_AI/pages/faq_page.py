import streamlit as st

def render():
    st.markdown("<h2 style='margin-bottom:0;'>❓ Internal Knowledge Base</h2>", unsafe_allow_html=True)
    st.caption("Search for data dictionary definitions, business terms, and user guides.")
    
    from faq.internal_faq import search_faq, get_faq_by_category, get_all_categories
    
    q = st.text_input("🔍 Search FAQ. Try 'What is claims paid ratio?' or 'Aegon'")
    
    if q:
        results = search_faq(q)
        if not results:
            st.info("No matching answers found in the internal knowledge base.")
        else:
            for r in results:
                st.markdown(f"**Q: {r['question']}**")
                st.markdown(f"A: {r['answer']}")
                st.caption(f"Category: {r['category']}")
                st.divider()
    else:
        st.write("Or browse by category:")
        try:
            cats = get_all_categories()
            if not cats:
                st.info("No FAQ categories found.")
                return

            tabs = st.tabs([c.title().replace("_"," ") for c in cats])
            for i, cat in enumerate(cats):
                with tabs[i]:
                    faqs = get_faq_by_category(cat)
                    for f in faqs:
                        with st.expander(f["question"]):
                            st.markdown(f["answer"])
                            st.caption(f"Keywords: {', '.join(f.get('keywords', []))}")
        except Exception as e:
            st.error(f"Error loading FAQ: {e}")
