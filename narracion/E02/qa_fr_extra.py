"""Añade a qa/fr_qa.txt el resultado de las 5 frases francesas repetidas (la pista completa se transcribió con las tomas anteriores)."""
import json
W = json.load(open('qa/fr_repetidas_words.json')); W = W.get('words', W)
txt = ' '.join(w['text'] for w in W if w.get('type', 'word') == 'word')
add = ["", "── Frases repetidas (transcripción aparte de las tomas nuevas) ──",
       "En la primera toma la voz decía «Pipou» en lugar de «Pipo». Se repitieron CANAL_INICIO, C04, C14, C21 y C29;",
       "en las 5 tomas nuevas Scribe oye «Pippo» (misma pronunciación que «Pipo»). Las 5 coinciden con el guion.",
       "E02_C03 conserva la primera toma («Pipou»): su repetición no se generó.",
       "E02_L3: «Frotte tes mains» se oye igual que «Frottez main»; es la transcripción, no un error de la voz.",
       "oído (tomas nuevas): " + txt]
open('qa/fr_qa.txt', 'a').write('\n'.join(add) + '\n')
