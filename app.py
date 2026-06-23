import streamlit as st
import os
import pandas as pd
from aligner import VerseAligner

st.set_page_config(page_title="Alineamiento Multilingüe", layout="wide")

st.title("Alineamiento Multilingüe de Poesía")

st.markdown("""
Esta herramienta te permite alinear versos originales en ruso con sus distintas traducciones.
El modelo usa IA (LaBSE) para entender el significado en cada idioma y alinear los textos automáticamente.
""")

DATA_FOLDER = 'data'
RESULTS_FOLDER = 'resultados'

if not os.path.exists(RESULTS_FOLDER):
    os.makedirs(RESULTS_FOLDER)

@st.cache_resource
def get_aligner():
    return VerseAligner()

try:
    aligner = get_aligner()
except Exception as e:
    st.error(f"Error al cargar el modelo: {e}")
    st.stop()

if os.path.exists(DATA_FOLDER):
    files = os.listdir(DATA_FOLDER)
    poem_ids = set()
    for f in files:
        if 'original.txt' in f:
            poem_ids.add(f.replace(' original.txt', '').strip())
    poem_ids = sorted(list(poem_ids))
else:
    st.error("No se encontró la carpeta 'data'.")
    st.stop()

if not poem_ids:
    st.warning("No se encontraron archivos con el formato '<ID> original.txt' en la carpeta 'data'.")
    st.stop()

selected_poem = st.selectbox("Selecciona el poema a alinear/revisar:", poem_ids)

saved_csv = os.path.join(RESULTS_FOLDER, f"alineamiento_{selected_poem}.csv")
saved_xlsx = os.path.join(RESULTS_FOLDER, f"alineamiento_{selected_poem}.xlsx")

if 'editor_key' not in st.session_state:
    st.session_state['editor_key'] = 0

# Lógica de carga
if 'df_aligned' not in st.session_state or st.session_state.get('selected_poem') != selected_poem:
    st.session_state['selected_poem'] = selected_poem
    st.session_state['editor_key'] += 1 # Reset editor on poem change
    
    # Intentar cargar si ya existe uno guardado
    if os.path.exists(saved_xlsx):
        st.session_state['df_aligned'] = pd.read_excel(saved_xlsx)
        st.session_state['is_loaded'] = True
    elif os.path.exists(saved_csv):
        st.session_state['df_aligned'] = pd.read_csv(saved_csv)
        st.session_state['is_loaded'] = True
    else:
        st.session_state['df_aligned'] = None
        st.session_state['is_loaded'] = False

col1, col2 = st.columns([1, 1])

with col1:
    if st.session_state['df_aligned'] is None:
        if st.button("Alinear Versos (Primera vez)"):
            with st.spinner("Alineando textos con IA..."):
                try:
                    df_aligned = aligner.process_folder(DATA_FOLDER, selected_poem)
                    st.session_state['df_aligned'] = df_aligned
                    st.session_state['is_loaded'] = False
                    st.session_state['editor_key'] += 1
                    st.success("Alineamiento automático completado.")
                    st.rerun()
                except Exception as e:
                    st.error(f"Error durante el alineamiento: {e}")
    else:
        if st.session_state.get('is_loaded', False):
            st.info(" Mostrando el alineamiento guardado previamente. Si editas algo, no olvides darle a Guardar Cambios.")
        
        if st.button("Forzar Re-Alineamiento Automático (Sobrescribe)"):
            with st.spinner("Re-alineando textos con IA..."):
                try:
                    df_aligned = aligner.process_folder(DATA_FOLDER, selected_poem)
                    st.session_state['df_aligned'] = df_aligned
                    st.session_state['is_loaded'] = False
                    st.session_state['editor_key'] += 1 # Reset editor to show new AI data
                    st.success("Re-alineamiento completado.")
                    st.rerun()
                except Exception as e:
                    st.error(f"Error durante el alineamiento: {e}")

if st.session_state.get('df_aligned') is not None:
    st.subheader("Resultados")
    st.markdown("Revisa la tabla. **Puedes editar cualquier celda haciendo doble clic en ella.**")
    
    current_key = f"data_editor_{st.session_state['selected_poem']}_{st.session_state['editor_key']}"
    edited_df = st.data_editor(st.session_state['df_aligned'], use_container_width=True, num_rows="dynamic", key=current_key)
    
    st.markdown("---")
    export_format = st.radio("Formato de guardado:", ("Excel (.xlsx)", "CSV (.csv)"))
    
    if st.button("Guardar Cambios"):
        if export_format == "Excel (.xlsx)":
            edited_df.to_excel(saved_xlsx, index=False)
            if os.path.exists(saved_csv): os.remove(saved_csv)
            st.success(f"Archivo guardado en: `{saved_xlsx}`")
        else:
            edited_df.to_csv(saved_csv, index=False, encoding='utf-8')
            if os.path.exists(saved_xlsx): os.remove(saved_xlsx)
            st.success(f"Archivo guardado en: `{saved_csv}`")
            
        st.session_state['df_aligned'] = edited_df
        st.session_state['is_loaded'] = True
