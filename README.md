# Jewishtory

Histoires du soir bilingues français · hébreu pour les enfants de familles franco-israéliennes. L'enfant est le héros, chaque épisode suit la paracha de la semaine et fait répéter cinq mots d'hébreu.

## Le site

`public/index.html` est un mini-lecteur statique, sans build : il lit `public/episodes/<id>/story.mp3` et `public/episodes/<id>/cues.json` (texte synchronisé) et affiche la fiche parent de chaque épisode. Il se déploie tel quel sur Vercel : `vercel.json` désactive la détection de framework et sert le dossier `public/`.

Épisodes actuels :

| # | Paracha | Dossier | Durée |
|---|---------|---------|-------|
| 1 | Noa'h | `public/episodes/noah` | 10 min 34 |
| 2 | Lekh Lekha | `public/episodes/lekh-lekha` | 9 min 31 |

Un lien direct vers un épisode : `/#noah` ou `/#lekh-lekha`.

## Le générateur audio

`generator/` transforme un script d'histoire en MP3 mixé (voix, carillons entre les scènes, boîte à musique, pluie ou vent) et en `cues.json`.

```bash
cd generator
pip install -r requirements.txt
./fetch_models.sh
python gen.py story_lekh_lekha ../public/episodes/lekh-lekha
```

Le script d'une histoire (`story_*.py`) est une liste de répliques `(personnage, texte)`. Un mot hébreu s'écrit `[[hébreu|translittération|prononciation]]` : le lecteur affiche la translittération et l'hébreu, la voix lit la prononciation. `~` marque un changement de scène.

Les voix viennent de Gemini TTS (Google AI Studio) dès que `GEMINI_API_KEY` est défini : chaque réplique est envoyée avec une consigne de style (conteuse douce, enfant de 4 ans…), et les mots hébreux sont envoyés en écriture hébraïque pour être prononcés à l'israélienne. Les clips sont mis en cache dans `generator/.tts-cache/`, donc une relance ne repaie que les répliques modifiées. Une histoire coûte environ 0,10 $.

```bash
GEMINI_API_KEY=... python gen.py story_noah ../public/episodes/noah
```

| Personnage | Voix Gemini |
|------------|-------------|
| Conteuse | Achernar |
| Noa'h | Algenib |
| Avram | Orus |
| Saraï | Vindemiatrix |
| Eydel | Leda, montée de 3 demi-tons |
| Arié | Puck, montée de 3 demi-tons |
| Hillel | Achird, montée de 3 demi-tons |

Sans clé, ou avec `TTS_ENGINE=piper`, le générateur reprend les voix Piper libres (françaises, après `./fetch_models.sh`) : les mots hébreux sont alors lus à partir de l'orthographe phonétique du troisième champ (par exemple `No-ar` pour Noa'h). Pour vérifier une orthographe, regardez sa transcription espeak : un `(en)` veut dire que le mot est lu à l'anglaise.
