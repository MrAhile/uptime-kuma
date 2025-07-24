## Déploiement Kubernetes de Uptime Kuma

Ce projet fournit un script Python simple pour gérer le cycle de vie (démarrage, arrêt, statut) d'une application Uptime Kuma déployée sur Kubernetes.

----
#### Qu'est-ce que Uptime Kuma ?

**Uptime Kuma** est un moniteur d'uptime auto-hébergeable, **open-source** et **facile à utiliser**, qui se présente comme une alternative moderne aux services de surveillance payants. Il vous permet de surveiller la disponibilité de vos services via différentes méthodes (HTTP(s), TCP, Ping, DNS, etc.) et de recevoir des notifications (Team, Telegram, slack..etc) instantanées en cas de panne.

##### À quoi ça sert ?
Uptime Kuma est essentiel pour toute personne ou équipe souhaitant s'assurer que ses sites web, API, serveurs ou autres services sont toujours en ligne et fonctionnent correctement. Il vous aide à :

* **Détecter les pannes rapidement** : Soyez alerté dès qu'un service tombe en panne, vous permettant d'agir immédiatement.

* **Surveiller les performances** : Gardez un œil sur les temps de réponse de vos services.

* **Obtenir un aperçu visuel** : Son interface utilisateur attrayante fournit des graphiques clairs et des tableaux de bord pour visualiser l'état de vos moniteurs.

* **Recevoir des notifications diverses** : Il supporte de nombreux services de notification comme Telegram, Discord, Email, Webhooks, et bien d'autres, pour vous prévenir où que vous soyez.

* **Créer des pages de statut publiques** : Vous pouvez générer des pages de statut personnalisables pour informer vos utilisateurs de l'état de vos services.

En bref, Uptime Kuma est votre œil vigilant sur la disponibilité de vos applications et infrastructures, vous offrant tranquillité d'esprit et réactivité en cas de problème.

----

#### Prérequis

Avant d'utiliser ce script, assurez-vous d'avoir les éléments suivants installés et configurés :

* **Python 3**
* **kubectl** : Configuré pour interagir avec votre cluster Kubernetes.

----

#### Structure du Projet

* **manage_kuma.py** : Le script Python principal pour gérer Uptime Kuma.

* **config.yaml** : Fichier de configuration spécifiant les fichiers Kubernetes et le namespace.

* **namespace.yaml** : Définition du Namespace Kubernetes pour Uptime Kuma.

* **uptime-kuma-deployment.yaml** : Définition du Deployment Kubernetes pour Uptime Kuma.

* **uptime-kuma-pvc.yaml** : Définition du Persistent Volume Claim pour Uptime Kuma.

----

#### Configuration (config.yaml)

Le fichier config.yaml liste les fichiers Kubernetes à appliquer ou supprimer et spécifie le namespace cible.

```yaml
kubernetes_files:
  - namespace.yaml
  - uptime-kuma-pvc.yaml
  - uptime-kuma-deployment.yaml
  - uptime-kuma-service.yaml
namespace: uptime
```

----

#### Utilisation

Pour utiliser le script, naviguez dans le répertoire du projet et exécutez les commandes suivantes :

* Démarrer Uptime Kuma :

```bash
python manage_kuma.py start
```

Cette commande appliquera tous les fichiers .yaml listés dans config.yaml et affichera ensuite le statut des pods.

* Arrêter Uptime Kuma :

```bash
python manage_kuma.py stop
```
Cette commande supprimera toutes les ressources Kubernetes définies dans les fichiers .yaml listés dans config.yaml.

* Vérifier le statut des Pods :

```bash
python manage_kuma.py status
```
Cette commande affichera le statut actuel des pods Uptime Kuma dans le namespace spécifié.

----
#### Accessibilité

Vous pouvez acceder à votre application via l'adresse suivante : http://localhost:3442/