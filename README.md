# Jewishtory

Histoires du soir bilingues français · hébreu pour les enfants de familles franco-israéliennes. L'enfant est le héros, chaque épisode suit la paracha de la semaine et fait répéter cinq mots d'hébreu.

## Le site

`public/index.html` est un mini-lecteur statique, sans build : il lit `public/episodes/<id>/story.mp3` et `public/episodes/<id>/cues.json` (texte synchronisé) et affiche la fiche parent de chaque épisode. Il se déploie tel quel sur Vercel : `vercel.json` désactive la détection de framework et sert le dossier `public/`.

Épisodes actuels :

| # | Paracha | Dossier | Durée |
|---|---------|---------|-------|
| 1 | Noa'h | `public/episodes/noah` | 10 min 34 |
| 2 | Lekh Lekha | `public/episodes/lekh-lekha` | 9 min 31 |
| 3 | Vayera | `public/episodes/vayera` | 12 min 14 |

Un lien direct vers un épisode : `/#noah`, `/#lekh-lekha` ou `/#vayera`.

## Le générateur audio

`generator/` transforme un script d'histoire en MP3 mixé (voix, carillons entre les scènes, boîte à musique, pluie ou vent) et en `cues.json`.

```bash
cd generator
pip install -r requirements.txt
./fetch_models.sh
python gen.py story_lekh_lekha ../public/episodes/lekh-lekha
```

Le script d'une histoire (`story_*.py`) est une liste de répliques `(personnage, texte)`. Un mot hébreu s'écrit `[[hébreu|translittération|prononciation]]` : le lecteur affiche la translittération et l'hébreu, la voix lit la prononciation. `~` marque un changement de scène.

Les épisodes du site sont générés avec ElevenLabs (`TTS_ENGINE=elevenlabs`, modèle v3, clé dans `ELEVENLABS_API_KEY`). La conteuse, Nath et deux voix d'enfants sont des voix clonées de la famille. Les mots hébreux sont lus depuis la translittération (deuxième champ), et `ELEVEN_SAY` corrige ceux que v3 lit mal (`Noa'h` devient `No-arr`, sinon il dit « No-a »). v3 ignore le réglage de vitesse : une consigne `[slowly, gently]` ralentit les rôles de Nath. Un épisode coûte environ 5 000 crédits.

```bash
TTS_ENGINE=elevenlabs python gen.py story_noah ../public/episodes/noah
python qa_elevenlabs.py story_noah ../public/episodes/noah --retake   # Gemini réécoute chaque réplique
```

v3 saute parfois un bout de phrase : `qa_elevenlabs.py` (qui utilise `GEMINI_API_KEY`) compare chaque réplique au texte, et `--retake` efface du cache celles qui posent problème pour qu'une relance de `gen.py` les refasse.

| Personnage | Voix ElevenLabs |
|------------|-----------------|
| Conteuse | Perla (clonée) |
| Noa'h, Avram, Avraham | Nath (clonée) |
| Saraï, Sarah | Lucie |
| Le malakh (l'ange) | Jon |
| Eydel | voix clonée « Arié », montée de 3 demi-tons |
| Arié | Philippine, montée de 4 demi-tons |
| Hillel | voix clonée « Eydel », montée de 2 demi-tons |

Avec `GEMINI_API_KEY` et sans `TTS_ENGINE`, le générateur utilise Gemini TTS (Google AI Studio) : chaque réplique part avec une consigne de style et les mots hébreux en écriture hébraïque, pour environ 0,10 $ par histoire. Voix : conteuse Achernar, Noa'h Algenib, Avram Orus, Saraï Vindemiatrix, malakh Iapetus, enfants Leda, Puck et Achird montés de 3 demi-tons. Les clips sont mis en cache dans `generator/.tts-cache/`, donc une relance ne repaie que les répliques modifiées.

Sans clé, ou avec `TTS_ENGINE=piper`, le générateur reprend les voix Piper libres (françaises, après `./fetch_models.sh`) : les mots hébreux sont alors lus à partir de l'orthographe phonétique du troisième champ (par exemple `No-ar` pour Noa'h). Pour vérifier une orthographe, regardez sa transcription espeak : un `(en)` veut dire que le mot est lu à l'anglaise.
