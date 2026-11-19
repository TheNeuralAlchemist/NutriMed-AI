import json
import pandas as pd
import streamlit as st
import ai
import chat
import history
from pdf_utils import make_pdf
from utils import check_image, IMAGE_TYPES

FLAGS = {"ok": "🟢", "caution": "🟡", "avoid": "🔴"}

LABEL_PROMPT = (
    ai.SAFETY
    + "Read this packaged food label photo (OCR). Reply ONLY with JSON in this shape:\n"
      '{"readable": true, "product_name": "", "serving_size": "", '
      '"ingredients": [{"name": "", "what_it_is": "simple one-line meaning", '
      '"flag": "ok|caution|avoid"}], '
      '"nutrition": [{"nutrient": "", "amount": "", "daily_value": ""}], '
      '"allergens": [""], "summary": "3 simple sentences"}\n'
      'flag: "caution" for lots of sugar, salt, artificial colours or preservatives; '
      '"avoid" only for something many people must avoid; otherwise "ok". '
      'If the photo is too blurry or has no label, reply {"readable": false}. '
      "Never invent values that you cannot see."
)


def show():
    st.title("🥗 NutriLens")
    st.caption("Food label assistant. Use a real photo of a packaged food label.")
    metrics = st.container()

    tab_scan, tab_ing, tab_chat = st.tabs(["📷 Scan label", "🧪 Ingredients & nutrition", "💬 Chat"])

    # ---------- Phase 5: upload + OCR ----------
    with tab_scan:
        f = st.file_uploader("Upload a label photo (PNG, JPG, WEBP, max 10 MB)",
                             type=IMAGE_TYPES, key="label_uploader")
        if f is not None:
            data, mime, err = check_image(f)
            if err:
                st.error(err)
            else:
                st.image(data, caption=f.name, width=350)
                if st.button("🔍 Read this label", type="primary"):
                    with st.spinner("Reading the label..."):
                        raw, err = ai.ask(LABEL_PROMPT, image=data, mime=mime, json_mode=True)
                    if err:
                        st.error(err)
                    else:
                        result = ai.parse_json(raw)
                        if not isinstance(result, dict):
                            st.error("Could not understand the AI answer. Try again.")
                        elif not result.get("readable", True) or not result.get("ingredients"):
                            st.warning("The label could not be read. Please take a clearer, "
                                       "well-lit photo of the ingredients and nutrition panel.")
                        else:
                            st.session_state["label_data"] = result
                            st.session_state["labels_scanned"] = st.session_state.get("labels_scanned", 0) + 1
                            st.session_state["chat_nutrilens"] = []
                            history.add("NutriLens", result.get("product_name") or f.name,
                                        json.dumps(result, ensure_ascii=False, indent=2))
                            st.success("Done! Open the 'Ingredients & nutrition' tab.")

    data = st.session_state.get("label_data")

    # ---------- Phase 6: ingredient cards + nutrition table ----------
    with tab_ing:
        if not data:
            st.info("Scan a label first in the 'Scan label' tab.")
        else:
            st.subheader(data.get("product_name") or "Product")
            if data.get("serving_size"):
                st.caption(f"Serving size: {data['serving_size']}")
            if data.get("summary"):
                st.write(data["summary"])
            if data.get("allergens"):
                st.warning("Allergens: " + ", ".join(a for a in data["allergens"] if a))

            st.markdown("### Ingredients")
            ingredients = data.get("ingredients", [])
            cols = st.columns(3)
            for i, ing in enumerate(ingredients):
                with cols[i % 3].container(border=True):
                    icon = FLAGS.get(str(ing.get("flag", "ok")).lower(), "🟢")
                    st.markdown(f"**{icon} {ing.get('name', '')}**")
                    st.caption(ing.get("what_it_is", ""))

            st.markdown("### Nutrition table")
            rows = data.get("nutrition", [])
            if rows:
                df = pd.DataFrame(rows).rename(columns={
                    "nutrient": "Nutrient", "amount": "Amount", "daily_value": "% Daily value"})
                st.dataframe(df, use_container_width=True, hide_index=True)
            else:
                st.info("No nutrition table was found on this label.")

            # ---------- Phase 9: downloads ----------
            ing_text = "\n".join(f"- {x.get('name', '')}: {x.get('what_it_is', '')} "
                                 f"[{x.get('flag', 'ok')}]" for x in ingredients)
            nut_text = "\n".join(f"- {r.get('nutrient', '')}: {r.get('amount', '')} "
                                 f"({r.get('daily_value', '')})" for r in rows)
            sections = [("Summary", data.get("summary", "")),
                        ("Ingredients", ing_text), ("Nutrition", nut_text)]
            st.download_button("⬇️ Download PDF",
                               make_pdf(f"NutriLens - {data.get('product_name', 'Label')}", sections),
                               file_name="nutrilens_label.pdf", mime="application/pdf")

    # ---------- Phase 7: chat ----------
    with tab_chat:
        if not data:
            st.info("Scan a label first in the 'Scan label' tab.")
        else:
            chat.chat_ui("nutrilens", json.dumps(data, ensure_ascii=False), "food label")

    with metrics:
        c1, c2, c3 = st.columns(3)
        c1.metric("Labels scanned", st.session_state.get("labels_scanned", 0))
        c2.metric("Ingredients found", len(data.get("ingredients", [])) if data else 0)
        c3.metric("Nutrition rows", len(data.get("nutrition", [])) if data else 0)
