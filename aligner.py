import os
import re
from sentence_transformers import SentenceTransformer
import scipy.spatial.distance
import pandas as pd

class VerseAligner:
    def __init__(self, model_name='sentence-transformers/LaBSE'):
        self.model = SentenceTransformer(model_name)

    def load_text(self, file_path, is_translation=False):
        """Carga el archivo y divide por puntuación si es traducción."""
        with open(file_path, 'r', encoding='utf-8') as f:
            text = f.read()
            
        if is_translation:
            # Dividir por puntuaciones mayores para aislar frases
            phrases = re.split(r'(?<=[.?!;])\s+', text)
            
            final_phrases = []
            for p in phrases:
                for sub_p in p.split('\n'):
                    cleaned = sub_p.strip()
                    if cleaned:
                        final_phrases.append(cleaned)
            verses = final_phrases
        else:
            lines = text.split('\n')
            verses = [line.strip() for line in lines if line.strip()]
            
        return verses

    def align_texts(self, src_verses, tgt_verses):
        if not src_verses or not tgt_verses:
            return []

        src_emb = self.model.encode(src_verses)
        tgt_emb = self.model.encode(tgt_verses)

        dist_matrix = scipy.spatial.distance.cdist(src_emb, tgt_emb, metric='cosine')

        n = len(src_verses)
        m = len(tgt_verses)
        
        dp = [[float('inf')] * (m + 1) for _ in range(n + 1)]
        dp[0][0] = 0
        pointers = [[None] * (m + 1) for _ in range(n + 1)]
        
        # gap_penalty de 0.65 hace que el algoritmo sea muy tolerante a diferencias 
        # léxicas antes de decidir que el verso "falta" o "sobra".
        gap_src = 0.65
        gap_tgt = 0.65
        
        for i in range(1, n + 1):
            dp[i][0] = dp[i-1][0] + gap_src
            pointers[i][0] = (i-1, 0)
            
        for j in range(1, m + 1):
            dp[0][j] = dp[0][j-1] + gap_tgt
            pointers[0][j] = (0, j-1)
            
        for i in range(1, n + 1):
            for j in range(1, m + 1):
                c1 = dp[i-1][j-1] + dist_matrix[i-1, j-1]  # Match
                c2 = dp[i-1][j] + gap_src                  # Fila vacía (Missing translation for src)
                c3 = dp[i][j-1] + gap_tgt                  # Agrupar (Extra translation phrase)
                
                costs = [c1, c2, c3]
                min_c = min(costs)
                dp[i][j] = min_c
                
                if min_c == c1:
                    pointers[i][j] = (i-1, j-1)
                elif min_c == c2:
                    pointers[i][j] = (i-1, j)
                else:
                    pointers[i][j] = (i, j-1)
                    
        i, j = n, m
        mapping = {}
        while i > 0 or j > 0:
            pi, pj = pointers[i][j]
            if pi == i - 1 and pj == j - 1:
                # 1 a 1
                if i-1 not in mapping: mapping[i-1] = []
                mapping[i-1].append(j-1)
            elif pi == i - 1 and pj == j:
                # 1 a 0 (Verso ruso no tiene traducción)
                if i-1 not in mapping: mapping[i-1] = []
            elif pi == i and pj == j - 1:
                # 0 a 1 (Frase extra en la traducción, se agrupa al verso ruso actual)
                idx = max(0, i-1)
                if idx not in mapping: mapping[idx] = []
                mapping[idx].append(j-1)
            i, j = pi, pj
            
        for k in mapping:
            mapping[k].reverse()
            
        aligned_tgt = []
        for s in range(n):
            if s in mapping and len(mapping[s]) > 0:
                texts = [tgt_verses[t] for t in mapping[s]]
                aligned_tgt.append(" / ".join(texts))
            else:
                aligned_tgt.append("")
                
        return aligned_tgt

    def process_folder(self, data_folder, poem_id):
        files = os.listdir(data_folder)
        original_file = f"{poem_id} original.txt"
        
        if original_file not in files:
            raise FileNotFoundError(f"No se encontró el archivo {original_file}")
            
        original_path = os.path.join(data_folder, original_file)
        src_verses = self.load_text(original_path, is_translation=False)
        
        trad_files = [f for f in files if f.startswith(str(poem_id)) and 'trad' in f]
        trad_files.sort()
        
        results = {"Verso Ruso (Original)": src_verses}
        
        for trad_file in trad_files:
            trad_path = os.path.join(data_folder, trad_file)
            tgt_verses = self.load_text(trad_path, is_translation=True)
            aligned_tgt = self.align_texts(src_verses, tgt_verses)
            
            col_name = trad_file.replace(str(poem_id), "").replace(".txt", "").strip()
            results[col_name] = aligned_tgt
            
        return pd.DataFrame(results)

if __name__ == "__main__":
    aligner = VerseAligner()
    df = aligner.process_folder('data', '104')
    print("Alineamiento exitoso.")
