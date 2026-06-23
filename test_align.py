from aligner import VerseAligner
import pandas as pd

aligner = VerseAligner()
df = aligner.process_folder('data', '104')
df.to_csv('resultados/test_104.csv', index=False)
print("Hecho")
