# Jewishtory

Histoires du soir bilingues français · hébreu pour les enfants de familles franco-israéliennes. L'enfant est le héros, chaque épisode suit la paracha de la semaine et fait répéter cinq mots d'hébreu.

## Le site

`index.html` est un mini-lecteur statique, sans build : il lit `episodes/<id>/story.mp3` et `episodes/<id>/cues.json` (texte synchronisé) et affiche la fiche parent de chaque épisode. Il se déploie tel quel sur Vercel (projet « Other », sans commande de build, dossier racine).

Épisodes actuels :

| # | Paracha | Dossier | Durée |
|---|---------|---------|-------|
| 1 | Noa'h | `episodes/noah` | 6 min 22 |
| 2 | Lekh Lekha | `episodes/lekh-lekha` | 6 min 07 |

Un lien direct vers un épisode : `/#noah` ou `/#lekh-lekha`.

## Le générateur audio

`generator/` transforme un script d'histoire en MP3 mixé (voix, carillons entre les scènes, boîte à musique, pluie ou vent) et en `cues.json`.

```bash
cd generator
pip install -r requirements.txt
./fetch_models.sh
python gen.py story_lekh_lekha ../episodes/lekh-lekha
```

Le script d'une histoire (`story_*.py`) est une liste de répliques `(personnage, texte)`. Un mot hébreu s'écrit `[[hébreu|translittération|prononciation]]` : le lecteur affiche la translittération et l'hébreu, la voix lit la prononciation. `~` marque un changement de scène.

Les voix sont des modèles Piper libres (français). Il n'y a pas encore de voix hébraïque : les mots hébreux sont lus par les voix françaises à partir d'une orthographe phonétique (par exemple `No-ar` pour Noa'h). Pour vérifier une orthographe, regardez sa transcription espeak : un `(en)` veut dire que le mot est lu à l'anglaise.

| Personnage | Voix |
|------------|------|
| Conteuse | Piper siwis |
| Noa'h | Piper tom |
| Avram | Piper gilles |
| Saraï | Piper upmc (Jessica) |
| Eydel, Arié, Hillel | Piper upmc / siwis, voix montées de 2,5 à 4,5 demi-tons |
