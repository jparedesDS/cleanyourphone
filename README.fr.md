<p align="center">
  <a href="https://cleanyourphone.org/">
    <img src="assets/banner.png" alt="CleanYourPhone — votre téléphone, sans le superflu" width="100%">
  </a>
</p>

<p align="center">
  <a href="README.md">English</a> ·
  <a href="README.es.md">Español</a> ·
  <a href="README.pt-BR.md">Português (BR)</a> ·
  <b>Français</b> ·
  <a href="README.de.md">Deutsch</a> ·
  <a href="README.it.md">Italiano</a> ·
  <a href="README.ja.md">日本語</a> ·
  <a href="README.zh-CN.md">简体中文</a> ·
  <a href="README.zh-TW.md">繁體中文</a> ·
  <a href="README.ko.md">한국어</a>
</p>

<p align="center">
  <a href="https://github.com/jparedesDS/cleanyourphone/actions/workflows/ci.yml"><img src="https://github.com/jparedesDS/cleanyourphone/actions/workflows/ci.yml/badge.svg" alt="CI"></a>
  <img src="https://img.shields.io/badge/license-MIT-a78bfa?labelColor=121316" alt="MIT">
  <img src="https://img.shields.io/badge/python-3.10%2B-a78bfa?labelColor=121316" alt="Python 3.10+">
  <img src="https://img.shields.io/badge/telemetry-none-a78bfa?labelColor=121316" alt="Sans télémétrie">
  <img src="https://img.shields.io/badge/profiles-157-a78bfa?labelColor=121316" alt="157 profils">
  <a href="https://github.com/jparedesDS/cleanyourphone/releases"><img src="https://img.shields.io/github/v/release/jparedesDS/cleanyourphone?color=a78bfa&labelColor=121316" alt="release"></a>
  <a href="https://github.com/jparedesDS/cleanyourphone-app/releases"><img src="https://img.shields.io/github/v/release/jparedesDS/cleanyourphone-app?color=a78bfa&label=app&labelColor=121316" alt="app release"></a>
</p>

# CleanYourPhone

**Votre téléphone, sans le superflu.** Une skill open source et réversible pour alléger Android,
pensée pour les agents de code. Elle désactive les applis et services préinstallés via ADB : sans
root, sans ROM personnalisée, rien de désinstallé, et une commande pour restaurer les changements
enregistrés par le CLI.

L’histoire et le modèle de sécurité sont sur
**[cleanyourphone.org](https://cleanyourphone.org/)**.

Il existe aussi une **app Windows facultative** pour ceux qui préfèrent les boutons aux prompts :
**[télécharger l’Early MVP](https://github.com/jparedesDS/cleanyourphone-app/releases/latest)**. C’est
une GUI au-dessus du même CLI. La skill reste le produit principal et la voie pour les téléphones
sans profil.

C’est la version téléphone de [cleanyour.tv](https://cleanyour.tv), construite de la même façon : un
prompt, une commande, réversible, open source, et la personne garde le contrôle.

[SKILL.md](SKILL.md) · [PROMPT.md](PROMPT.md) · [App](https://github.com/jparedesDS/cleanyourphone-app) · [Sécurité](docs/SAFETY.md) · [157 profils](docs/PROFILES.md) · [Retours](docs/FEEDBACK.md) · [Changelog](CHANGELOG.md)

## Commencez ici

| Vous avez | Commencez par |
|---|---|
| Un téléphone et un agent de code | Le démarrage rapide ci-dessous. |
| Une préférence pour les boutons | [Téléchargez l’app Windows](https://github.com/jparedesDS/cleanyourphone-app/releases/latest) (Early MVP). |
| Envie de voir d’abord | [Le site](https://cleanyourphone.org/). |
| Besoin des règles de sécurité | [docs/SAFETY.md](docs/SAFETY.md). |
| Besoin d’un profil pour votre modèle | [Parcourir les 157 profils](profiles/README.md). |
| Un téléphone non listé | Utilisez la skill manuellement ou envoyez une [demande de profil](docs/FEEDBACK.md). |
| Une préférence pour le terminal | [Installez le CLI](docs/CLI.md). |

| Partie | État |
|---|---|
| **Skill** | Produit principal, dans ce dépôt. |
| **CLI** | `0.3.4`, publié sur PyPI sous `cleanyourphone` / `cyp`. |
| **App Windows** | `0.2.1` Early MVP, facultative, non signée. |
| **Site** | Disponible en 10 langues sur [cleanyourphone.org](https://cleanyourphone.org/). |
| **Retours** | Formulaire facultatif web/app/skill vers Discord ; aucune télémétrie automatique. |

---

## Pourquoi la skill passe avant

Une app qui désactive d’autres apps a besoin de root, Shizuku ou de privilèges device-owner. C’est
beaucoup de pouvoir et beaucoup de risque pour quelque chose qu’une commande shell sait faire. Une
skill n’est que du texte : l’agent de la personne la lit, exécute `adb`, affiche un plan et demande
avant de toucher quoi que ce soit. Rien à installer sur le téléphone, rien qui tourne en
arrière-plan, rien qui envoie des données.

Il existe désormais une app Windows facultative, mais elle ne remplace pas la skill. C’est une GUI
au-dessus du même CLI, et elle ne continue que si elle trouve un profil `device` exact avec une build
testée, ou un profil `documented` après une confirmation explicite et un paquet par lot. Si elle ne
reconnaît pas le téléphone, elle s’arrête et renvoie ici. La skill peut toujours inspecter la liste
des paquets, poser la question pour chaque app et continuer manuellement.

Le téléphone est l’appareil du quotidien, donc la skill est volontairement prudente :

- **Désactiver, jamais désinstaller.** Uniquement `pm disable-user --user 0`. `pm enable` est
  l’annulation.
- **Sauvegarder d’abord.** Listes de paquets, réglages, rôles, claviers (IME) et `getprop` avant le
  premier changement.
- **Liste protégée.** Android de base, téléphonie, Play Services, WebView, permission controller,
  alertes d’urgence, IME/télécom, NFC/SE et paquets de sécurité des fabricants sont refusés par le
  CLI.
- **Vérification des rôles.** Elle ne vous laissera pas sans dialer, app SMS, app Home ni clavier.
- **Petits lots.** Cinq paquets à la fois, vérification, puis on continue.
- **Demander d’abord.** Banque, paiements, WhatsApp, appareil photo, réveil, VPN, authentificateur,
  montre connectée, eSIM, VoLTE/appels Wi-Fi et applis pro relèvent d’une liste de vérification, pas
  d’un choix par défaut.

## Comment ça marche

1. **Sur le téléphone :** activez Options pour les développeurs et Débogage USB. Branchez-le en USB.
2. **Sur l’ordinateur :** donnez `SKILL.md` à votre agent (ou collez `PROMPT.md`).
3. **Suivez le déroulé :** l’agent identifie le téléphone, sauvegarde, affiche un tableau des paquets,
   demande ce que vous utilisez, désactive par lots, redémarre et vérifie.
   `python tools/phone.py restore` annule tout.

```text
$ python tools/phone.py doctor
ADB ......... C:\platform-tools\adb.exe
ADB version . Android Debug Bridge version 1.0.41
Devices ..... <serial> (device)

Device ...... Google Pixel 8 (shiba)
Android ..... 16 (SDK 36)
Managed ..... no
Users ....... 1
Battery ..... 82%
Backup ...... none (run: python tools/phone.py backup)
Profiles .... google-pixel-8
Auto-apply .. google-pixel-8

$ python tools/phone.py plan --profile google-pixel-8
Profile: google-pixel-8 (Google Pixel 8)
Phone:   Google Pixel 8 (shiba), Android 16
Match:   yes
Auto-apply: yes

DISABLE  com.google.android.apps.wellbeing
         why: Digital Wellbeing: screen-time tracking and telemetry
         breaks: Screen-time dashboard and app timers
ASK      com.google.android.apps.turbo
         why: Adaptive Battery and Device Health
         breaks: Adaptive Battery, battery diagnostics
```

## L’app Windows facultative

Pour ceux qui préfèrent les boutons, l’app encapsule le même CLI dans un parcours Windows guidé :
connecter, vérifier, sauvegarder, relire, appliquer, vérifier et annuler.

<p align="center">
  <a href="https://github.com/jparedesDS/cleanyourphone-app/releases/latest">
    <img src="assets/app-review.png" alt="Écran de relecture de l’app CleanYourPhone avec un avertissement de profil documented et une app sélectionnée" width="760">
  </a>
</p>

- **Connexion en Wi-Fi ou USB.** L’app trouve le téléphone, vérifie la build et affiche le profil
  exact.
- **Les profils `device` exacts** suivent le parcours testé. Les **profils `documented`** sont
  manuels : avertissement visible, confirmation explicite et une app par lot. Sans profil, on
  s’arrête et on utilise la skill.
- **La sauvegarde est obligatoire.** Relisez chaque paquet, appliquez par lots, vérifiez et annulez
  tout le journal.
- **Options facultatives :** blocage des pubs par DNS privé (pas YouTube) et benchmark local
  avant/après.
- **Retours facultatifs :** une liste de vérification modifiable peut être envoyée au mainteneur
  après consentement. Aucune télémétrie automatique.
- **Pas de root, pas de désinstallation, aucune app installée sur le téléphone.** L’installateur n’est
  pas signé ; vérifiez le SHA-256 avant de l’exécuter.

[Télécharger `v0.2.1`](https://github.com/jparedesDS/cleanyourphone-app/releases/latest) ·
[Source](https://github.com/jparedesDS/cleanyourphone-app) ·
[Guide de connexion](docs/CONNECT.md).

## Démarrage rapide

### 1. Installer ADB

Téléchargez [Android SDK Platform-Tools](https://developer.android.com/tools/releases/platform-tools)
pour Windows, macOS ou Linux, décompressez-le et ajoutez-le au `PATH`. Vérifiez avec :

```bash
adb version
```

### 2. Préparer le téléphone

Réglages → À propos du téléphone → appuyez 7 fois sur **Numéro de build** → retour → **Options pour
les développeurs** → activez **Débogage USB**. Branchez le téléphone en USB et acceptez l’invite
**Autoriser le débogage USB ?**. Gardez le téléphone déverrouillé et avec plus de 30 % de batterie.

Android 11 et versions ultérieures peuvent utiliser le **Débogage sans fil** à la place : activez-le,
appuyez sur le texte (pas seulement sur l’interrupteur), choisissez **Associer l’appareil avec un code
d’association** et laissez cette boîte de dialogue ouverte. La boîte d’association a son propre port ;
ce n’est pas le port de connexion de l’écran principal. Voir [docs/CONNECT.md](docs/CONNECT.md) pour
le guide de première connexion et les correctifs courants.

### 3. Cloner et vérifier

```bash
git clone https://github.com/jparedesDS/cleanyourphone
cd cleanyourphone
python tools/phone.py doctor
```

Le CLI est facultatif. `SKILL.md` contient aussi les commandes `adb` brutes, donc un agent peut
travailler sans Python. Le CLI existe pour que l’agent n’improvise pas les garde-fous.

Vous préférez le terminal ? Installez la commande avec [pipx](https://pipx.pypa.io/) :

```bash
pipx install cleanyourphone
cleanyourphone doctor
```

Cela ajoute `cleanyourphone` et l’alias court `cyp`. [docs/CLI.md](docs/CLI.md) couvre le wizard,
l’emplacement des fichiers installés et les règles de sécurité. `python tools/phone.py` continue de
fonctionner.

### 4. Donner la skill à votre agent

| Agent | Où le placer |
|---|---|
| **Claude Code** | `~/.claude/skills/cleanyourphone/SKILL.md` (personnel) ou `.claude/skills/cleanyourphone/SKILL.md` (projet) |
| **OpenCode** | `~/.config/opencode/skills/cleanyourphone/SKILL.md` (global) ou `.opencode/skills/cleanyourphone/SKILL.md` (projet) |
| **Codex** | `AGENTS.md` dans le projet, ou `~/.codex/AGENTS.md` ; collez `PROMPT.md` si votre version ne charge pas les skills |
| **Cursor** | `.cursor/rules/cleanyourphone.mdc` avec le contenu de `SKILL.md` |
| **Gemini CLI** | `GEMINI.md` dans le projet |
| **N’importe quel agent de chat** | Collez `PROMPT.md`, puis `SKILL.md` quand il le demande |

Prompt espagnol : [PROMPT.es.md](PROMPT.es.md). La skill répond dans la langue dans laquelle la
personne écrit.

La configuration la plus simple est de cloner le dépôt et d’ouvrir votre agent dans ce dossier :
`SKILL.md` est déjà à la racine, donc `python tools/phone.py` fonctionne. Si votre agent charge les
skills depuis un dossier global, copiez-y `SKILL.md` ; installez le CLI avec pipx (ci-dessus) et vous
n’avez plus besoin de garder le dépôt cloné :

```bash
mkdir -p ~/.claude/skills/cleanyourphone
cp SKILL.md ~/.claude/skills/cleanyourphone/SKILL.md
```

Sans le dépôt, la skill fonctionne quand même : elle inclut les commandes `adb` brutes et demande à
l’agent de les utiliser.

Demandez ensuite : **« Nettoie mon téléphone »** ou **« Utilise cleanyourphone sur mon Pixel »**.

## Ce qu’elle fait

- Désactive la télémétrie des fabricants, les surfaces publicitaires, les rangées de recommandations,
  les navigateurs et magasins d’applis en double, et les préchargements inutilisés.
- Configure facultativement le DNS privé avec des préréglages (`adguard`, `adguard-family`, `controld`,
  `mullvad`) ou votre propre résolveur, et vérifie si les pubs sont réellement bloquées. Ce n’est pas
  un bloqueur de pubs YouTube ; voir [docs/ADS.md](docs/ADS.md).
- Produit un rapport : ce qui a changé, pourquoi, ce qui a été conservé, le chemin de la sauvegarde et
  la commande d’annulation.
- Traite les profils `documented` comme des preuves manuelles : pas de liste `disable`, pas
  d’application automatique, un paquet à la fois après relecture.
- Propose une GUI Windows facultative pour le même parcours (`device` automatique, `documented`
  manuel, tout le reste s’arrête et renvoie ici).
- Mesure la RAM libre, les processus et le nombre de paquets avant/après avec `bench snapshot` et
  `bench compare` ; approximatif, local et sans lien de causalité. Voir [docs/BENCH.md](docs/BENCH.md).
- Établit une base de référence pour la batterie avant/après (`docs/BATTERY.md`), sans promettre de
  miracles.

## Retours et demandes de profil

Si un téléphone n’est pas couvert, la personne peut demander un profil ou signaler un bug sans
partager de numéro de série, d’adresse IP, d’IMEI ni d’adresse MAC :

- **Web :** [formulaire de retour CleanYourPhone](https://cleanyourphone.org/#feedback).
- **App :** **Feedback** dans l’en-tête ; la liste de vérification est préremplie et modifiable.
- **Skill :** `python scripts/feedback.py --kind profile --checklist-file feedback.txt` prévisualise
  le payload ; ajoutez `--yes` seulement après approbation de la personne.

Le message passe par un Worker Cloudflare puis arrive sur le Discord du mainteneur. Rien n’est envoyé
au démarrage ni pendant une analyse. L’app et le site utilisent le même Worker ; `tools/phone.py`
reste sans réseau. Voir [docs/FEEDBACK.md](docs/FEEDBACK.md) pour le payload, l’occultation des données
et la limite de débit.

## Bloquer les pubs (facultatif)

Le DNS privé peut bloquer de nombreux domaines publicitaires et de traqueurs intégrés aux apps. Ce
n’est pas un bloqueur YouTube, pas un VPN, et cela peut casser les portails captifs. Les préréglages
sont :

```bash
python tools/phone.py dns providers
python tools/phone.py dns set adguard
python tools/phone.py dns check
python tools/phone.py dns restore
```

`dns check` distingue « bloqué » de « impossible à tester » quand le domaine de contrôle ne se résout
pas. Voir [docs/ADS.md](docs/ADS.md) pour la liste des réglages anti-pubs par fabricant et les mises
en garde.

## Mesurer le résultat

Enregistrez un instantané local avant/après ; aucun numéro de série ni empreinte n’est stocké :

```bash
python tools/phone.py bench snapshot --label before
# appliquer, redémarrer et vérifier
python tools/phone.py bench snapshot --label after
python tools/phone.py bench compare <before.json> <after.json>
```

La comparaison est approximative et n’établit pas de causalité. Voir [docs/BENCH.md](docs/BENCH.md).

## Ce qu’elle ne fait pas

- **Aucune app installée sur le téléphone.** L’app Windows facultative tourne sur l’ordinateur ; le
  téléphone ne reçoit que `pm disable-user` / `pm enable`.
- **Pas de root, pas de Magisk, pas besoin de Shizuku.**
- **Pas de ROM personnalisée, pas de déverrouillage du bootloader, pas de flash.**
- **Pas de désinstallation.** `pm disable-user` est réversible ; `pm uninstall` ne l’est pas.
- **Aucune modification du profil professionnel ni du MDM.** Si le téléphone est géré, elle s’arrête.
- **Pas de blocage des pubs YouTube.** Le DNS privé ne touche pas les pubs du même domaine.
  `docs/FAQ.md` l’explique.
- **Aucune télémétrie automatique.** Le CLI est local ; le formulaire de retour facultatif n’envoie
  qu’après un clic sur Envoyer. Un agent hébergé reçoit quand même la session (modèle, noms de
  paquets, empreinte), donc utilisez un modèle local si cela compte.
- **Aucune promesse de « double batterie ».** Le gain réaliste en veille grâce au débloatage est de
  0 à 10 % ; les gros gains viennent des restrictions d’arrière-plan, de la luminosité/taux de
  rafraîchissement et du DNS.

## Sécurité

Lisez [docs/SAFETY.md](docs/SAFETY.md) avant la première exécution. En bref :

- Le CLI refuse les paquets de la liste protégée, les paquets qui occupent un rôle et tout changement
  sans sauvegarde.
- Chaque désactivation est enregistrée. `python tools/phone.py restore` réactive exactement ce que
  l’outil a désactivé et ne touche pas à ce que vous aviez déjà désactivé.
- Si le téléphone entre en bootloop, [docs/RESTORE.md](docs/RESTORE.md) donne la procédure de
  récupération. Ne faites pas de réinitialisation d’usine en premier réflexe.
- Le débloatage est réversible, mais votre fabricant peut voir les choses autrement. Cela n’annule
  pas à soi seul une garantie légale dans l’UE, mais un centre de réparation peut refuser
  d’intervenir sur un logiciel modifié. Soyez honnête avec la personne.

## Profils

Un profil est soit une liste de paquets testée sur un vrai téléphone (`device`), soit une liste
construite à partir d’un dump de firmware primaire (`documented`). Les profils documentés ne sont
jamais appliqués automatiquement et n’ont pas de liste `disable` ; servez-vous-en pour demander
paquet par paquet. `apply` ne s’exécute que pour un profil `device` sur une build listée dans
`tested`. Les profils de tablette définissent `form_factor: tablet` ; un rôle dialer/SMS manquant est
un avertissement, pas un échec.

L’app Windows suit la même règle : les profils `device` peuvent utiliser le parcours testé, les
profils `documented` exigent un avertissement et une confirmation explicite, et l’application se fait
un paquet par lot. Si aucun profil ne correspond, l’app s’arrête et renvoie vers cette skill au lieu
de deviner.

Le catalogue complet, modèle par modèle, est dans [docs/PROFILES.md](docs/PROFILES.md).

| Marque | Profils | Testés sur appareil | Tablettes |
|---|---|---|---|
| **Google** | 5 | 1 | 0 |
| **Samsung** | 55 | 1 | 7 |
| **Xiaomi** | 15 | 1 | 2 |
| **Redmi** | 56 | 0 | 1 |
| **POCO** | 16 | 0 | 0 |
| **OnePlus** | 8 | 1 | 0 |
| **Motorola** | 1 | 0 | 0 |
| **Générique** | 1 | 0 | 0 |

Vous voulez ajouter le vôtre ? Lisez [profiles/README.md](profiles/README.md). Un profil `device`
exige un vrai test ; un profil `documented` exige un dump de firmware primaire ou un inventaire
collecté par le propriétaire de l’appareil, ainsi qu’au moins une URL de source.

## La question de l’OS open source

Oui, ça existe. Non, ce n’est pas la première chose à faire. [docs/ROMS.md](docs/ROMS.md) explique les
vrais compromis :

- **GrapheneOS** est excellent, mais uniquement sur Pixel 6–10 (octobre 2026). Meilleure sécurité et
  confidentialité ; Play Services isolés en sandbox ; bootloader verrouillé.
- **/e/OS** a la liste d’installation facile la plus large, avec microG à la place de Google.
- **LineageOS** est large mais demande plus de maintenance ; les builds officielles varient selon
  l’appareil.
- **CalyxOS** couvre Pixel, Fairphone et certains modèles Motorola.

Les coûts sont réels : déverrouiller le bootloader efface le téléphone, Play Integrity peut casser la
banque/Wallet et faire tomber Netflix en SD, certains opérateurs perdent la VoLTE/les appels Wi-Fi,
et vous devenez le mainteneur des correctifs de sécurité. Sur Samsung, le déverrouillage déclenche
Knox définitivement. C’est pourquoi la skill reste sur la ROM d’usine : elle retire les surfaces
publicitaires et de télémétrie que la plupart des gens remarquent, sans ces coûts. Ce n’est pas un OS
durci et ce n’est pas un substitut à GrapheneOS sur un Pixel.

## FAQ

**Est-ce que cela annule ma garantie ?**
Le débloatage relève de la configuration logicielle, pas d’une modification matérielle, et il est
réversible. Dans l’UE, une garantie légale n’est pas automatiquement annulée, mais un centre de
réparation peut refuser d’intervenir sur un logiciel modifié. La skill ne déverrouille pas le
bootloader.

**Puis-je bricker mon téléphone ?**
Désactiver un mauvais paquet système peut provoquer une boucle de démarrage. C’est pourquoi le CLI
refuse les paquets de la liste protégée, vérifie les rôles, sauvegarde d’abord et vérifie par lots.
`restore` annule exactement ce que l’outil a désactivé ; si son journal est perdu,
`restore --from-backup` reconstruit le changement à partir de la sauvegarde. La procédure de
récupération complète, mode sans échec inclus, est dans [docs/RESTORE.md](docs/RESTORE.md).

**Est-ce que cela supprime les pubs de YouTube ?**
Non. Un résolveur avec blocage via DNS privé bloque beaucoup de pubs et de traqueurs dans les apps,
mais YouTube sert les pubs depuis le même domaine que la vidéo. La skill n’installe pas d’applis
patchées.

**Est-ce que ça marche sur un téléphone professionnel ?**
Non. Si `dumpsys device_policy` montre un device owner ou un profile owner, ou si `pm list users`
montre plus d’un utilisateur, la skill s’arrête.

**Est-ce que ça marche sur Samsung/Xiaomi/Huawei ?**
La méthode fonctionne sur n’importe quel téléphone Android 8+. Les noms de paquets et la liste sûre
diffèrent. Utilisez un profil pour votre modèle exact, ou laissez l’agent classer manuellement et
demander avant chaque paquet. Sur Huawei/Honor sans services Google, beaucoup de paquets
`com.google.*` n’existent pas.

**Ai-je besoin de Python ?**
Non. La skill inclut les commandes `adb` brutes. Le CLI est un garde-fou et un confort ; il n’utilise
que la bibliothèque standard et n’a aucune dépendance. L’app Windows embarque le CLI et ne nécessite
pas Python.

**Y a-t-il une GUI ?**
Oui, une app Windows facultative dans
[cleanyourphone-app](https://github.com/jparedesDS/cleanyourphone-app). C’est un Early MVP, non
signé, qui ne continue qu’avec un profil connu. La skill reste la voie pour tous les autres
téléphones.

**Comment signaler un téléphone ou envoyer un retour ?**
Utilisez le [formulaire web](https://cleanyourphone.org/#feedback), **Feedback**
dans l’app, ou `scripts/feedback.py` depuis la skill. L’envoi est volontaire, le payload est
prévisualisé et le numéro de série, l’IP, l’IMEI et les adresses MAC sont exclus. Voir
[docs/FEEDBACK.md](docs/FEEDBACK.md).

## Contribuer

- Un profil testé (`device`) pour un nouveau modèle : ouvrez une PR avec
  `profiles/<brand>/<model>.json` et les détails du test.
- Un profil `documented` : utilisez `scripts/dump_inventory.py`, citez le dump primaire dans
  `sources` et laissez `disable` vide.
- Un correctif de garde-fou, de parser ou du CLI : ajoutez un test dans `tests/`.
- Un changement de règle de sécurité : ouvrez d’abord une issue. Ces règles sont le produit.
- Un téléphone que vous ne pouvez pas tester vous-même : envoyez une
  [demande de profil](https://cleanyourphone.org/#feedback) avec modèle, Android,
  build et empreinte. Sans numéro de série ni IP.
- Changements de marque ou de logo : lisez [docs/BRAND.md](docs/BRAND.md) avant de modifier les
  assets.
- Lisez [AGENTS.md](AGENTS.md) avant de modifier le dépôt.

## Licence

MIT. Voir [LICENSE](LICENSE).
