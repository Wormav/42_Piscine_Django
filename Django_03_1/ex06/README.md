# Exercice 06 : Automatisation et réputation

## 🎯 Objectif
Implémenter un système de réputation automatique qui attribue des privilèges aux utilisateurs en fonction de leurs performances. Les permissions ne sont plus gérées manuellement mais calculées automatiquement selon la réputation.

## 🏆 Système de Réputation

### Calcul de la Réputation
- **Point de départ** : Tous les nouveaux utilisateurs commencent avec 0 point de réputation
- **Upvote reçu** : +5 points par upvote sur vos tips
- **Downvote reçu** : -2 points par downvote sur vos tips
- **Suppression de tip** : La suppression d'un tip supprime l'influence de tous ses votes sur la réputation

### Seuils de Déblocage
- **👤 User (0-14 points)** : Peut uniquement voter et gérer ses propres tips
- **🔑 Moderator (15-29 points)** : Peut downvoter les tips des autres utilisateurs
- **⭐ Elite (30+ points)** : Peut downvoter ET supprimer tous les tips
- **👑 Admin** : Superuser avec tous les privilèges

## 🛠️ Fonctionnalités Implémentées

### Automatisation des Permissions
- **Signaux Django** : Les permissions sont mises à jour automatiquement à chaque changement de vote
- **Calcul en temps réel** : La réputation est recalculée dynamiquement
- **Gestion des seuils** : Les permissions sont automatiquement accordées/retirées selon la réputation

### Interface Utilisateur
- **Affichage de la réputation** : La réputation apparaît entre crochets à côté du nom de chaque utilisateur
- **Badges de niveau** : Indicateurs visuels du niveau de l'utilisateur dans la navbar
- **Styling moderne** : Badges colorés avec dégradés et effects hover

### Administration
- **Vue d'ensemble** : L'admin affiche la réputation et le niveau de permission de chaque utilisateur
- **Actions en masse** : Mise à jour des permissions pour plusieurs utilisateurs à la fois
- **Monitoring** : Suivi du nombre de tips et de la réputation par utilisateur

## 🎨 Améliorations Visuelles

### Badges de Réputation
- **Design moderne** : Dégradés colorés avec ombres portées
- **Responsive** : Adaptation automatique à la taille de l'écran
- **Consistant** : Style uniforme entre les différentes pages

### Niveaux Visuels
- **👤 User** : Badge gris secondaire
- **🔑 Moderator** : Badge orange avec icône clé
- **⭐ Elite** : Badge vert avec étoile
- **👑 Admin** : Badge rouge avec couronne

## 🧪 Tests et Données de Test

### Scripts de Test
- `test_reputation.py` : Crée des utilisateurs et tips de test avec différents niveaux de réputation
- `boost_reputation.py` : Ajoute des votes pour faire atteindre le niveau Elite

### Scénarios de Test
1. **Utilisateur débutant** : 0 point, permissions de base
2. **Moderateur** : 15+ points, peut downvoter les autres
3. **Elite** : 30+ points, peut downvoter et supprimer
4. **Réputation négative** : Test avec des downvotes

## 🔧 Architecture Technique

### Modèles
- **CustomUser** : Méthodes `calculate_reputation()`, `update_permissions()`, `can_downvote_others_tips()`, `can_delete_tips()`
- **Propriété reputation** : Accès facile à la réputation dans les templates
- **Signaux** : Mise à jour automatique des permissions lors des changements de votes

### Vues
- **Logique de permission mise à jour** : Les vues respectent les nouvelles règles de réputation
- **Downvote restreint** : Les utilisateurs avec permission ne peuvent downvoter QUE les tips des autres

### Templates
- **Affichage de réputation** : Intégré dans tous les affichages d'utilisateur
- **Badges conditionnels** : Affichage dynamique selon le niveau de l'utilisateur
- **Responsive design** : Adaptation mobile et desktop

## 🚀 Installation et Utilisation

1. **Activez l'environnement virtuel** :
   ```bash
   source script.sh
   ```

2. **Lancez le serveur** :
   ```bash
   cd lpt_project
   python manage.py runserver
   ```

3. **Créez des données de test** (optionnel) :
   ```bash
   python test_reputation.py
   python boost_reputation.py
   ```

4. **Accédez à l'application** : http://127.0.0.1:8000/

## 📊 Fonctionnement

1. **Inscription** : Nouvel utilisateur avec 0 point de réputation
2. **Publication de tips** : Les utilisateurs partagent leurs conseils
3. **Votes communautaires** : La communauté vote sur les tips
4. **Calcul automatique** : La réputation se met à jour en temps réel
5. **Déblocage de privilèges** : Les permissions s'activent automatiquement selon les seuils

## 🏅 Résultat

Un système de gamification complet qui encourage la participation de qualité et récompense les contributeurs méritants avec des privilèges supplémentaires, le tout géré automatiquement sans intervention manuelle.
