# Workshop 4 — FocusBoard (Python Flask)

> **Application volontairement vulnérable pour un atelier DevSecOps.**
> Les secrets sont fictifs et invalides. Utilisation locale uniquement : ne pas exposer sur Internet.

## Présentation
FocusBoard est une petite application web de gestion de tâches : frontend HTML/CSS, backend Python Flask et base SQLite.

## Lancer avec Docker
```powershell
docker build -t workshop4-web:before .
docker run --rm --name workshop4-web -p 5000:5000 workshop4-web:before
```
Ouvrir http://localhost:5000. Arrêter avec `Ctrl+C`.

## Fonctionnalités
- Voir les tâches et statistiques.
- Ajouter une tâche et choisir sa catégorie.
- Marquer une tâche terminée.
- Supprimer une tâche.
- Endpoint de santé `/api/health`.

## Scans initiaux
```powershell
docker run --rm -v /var/run/docker.sock:/var/run/docker.sock aquasec/trivy:latest image workshop4-web:before
docker run --rm -v ${PWD}:/project aquasec/trivy:latest config /project
docker run --rm -v ${PWD}:/project aquasec/trivy:latest fs --scanners secret /project
```
Compléter avec les résultats réellement obtenus.

## Faiblesses intentionnelles
- Image de base ancienne et tag non fixé par digest.
- Dépendances Python anciennes.
- Exécution en root et mode debug activé.
- Secrets fictifs exposés dans les fichiers et variables Docker.
- `.env` et `config.py` absents du `.dockerignore`.

## Remédiation
Mettre à jour l'image et les dépendances, créer un utilisateur non-root, désactiver debug, retirer les secrets, compléter `.dockerignore`, puis refaire les scans et comparer avant/après.

## Captures à ajouter
Interface web, build Docker, scans image/config/secrets, Dockerfile corrigé, scans après correction et exécution GitHub Actions.
