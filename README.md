# HISQIS zu Slack

Ein Python-Skript, was den [HISQIS-Notenspiegel](https://qis.dez.tu-dresden.de/) der TU-Dresden automatisch einliest und eine Slack-Benachrichtigung versendet, sobald neue Noten oder Einträge vorliegen

# Wie funktionierts?
Das Skript nutzt das Python-Paket `BeautifulSoup`, um regelmäßig HISQIS aufzurufen, dich anzumelden und die Notenübersicht abzurufen. Wenn eine Änderung in der Tabelle erkannt wurde (z.B. eine neu eingetragene Prüfung), wirst du über Slack über die Inhalte der Prüfung benachrichtigt. 

# Voraussetzungen
Um das Tool zu benutzen benötigst du:
* einen [HISQIS-Account](https://qis.dez.tu-dresden.de/) der TU Dresden
* einen Slack-Account und Workspace, in dem du Administrator bist
* einen Server oder Computer, der `Docker` unterstützt und dabei dauerhaft läuft

# Nutzung
## Slack-Bot einrichten
Folge der [Slack-Anleitung zu "Incoming Webhooks"](https://api.slack.com/messaging/webhooks) bis einschließlich zu dem Schritt "Create an Incoming Webhook". Dabei erstellst du eine neue Slack-App und wählst aus, in welchem Channel die Benachrichtigungen gepostet werden. Am Ende bekommst du eine `Webhook-URL` in diesem Format angezeigt:
```
https://hooks.slack.com/services/T00000000/B00000000/XXXXXXXXXXXXXXXXXXXXXXXX
```
Merke dir diese für später!
## Konfiguration vorbereiten
Erstelle auf dem Rechner/ Server, auf dem das Tool laufen soll, einen neuen Ordner. Erstelle in diesem Ordner eine Datei `.env` und fülle sie mit dem Beispielinhalt von [`.env.example`](.env.example).

Ändere die Parameter ab und ergänze:
* `HISQIS_USER`: Der Nutzername, mit dem du dich bei HISQIS anmeldest
* `HISQIS_PASSWORD`: Das Passwort, dass du für die Anmeldung nutzt
* `SLACK_WEBHOOK`: Die URL des Slack-Webhooks, den du im vorherigen Schritt erstellt hast

Optional kannst du auch die Zeile `DBG_DUMP_HISQIS=1` auskommentieren (die `#` am Anfang der Zeile entfernen). So sendet das Tool ein paar Test-Benachrichtigungen für Prüfungen, die schon im HISQIS stehen aber nicht verändert wurden, sodass du die Funktion der Slack-Anbindung austesten kannst (auch ohne auf neue Noten zu warten...)
## Container ausführen
Nun kannst du den Docker-Container starten:
```
docker run --env-file=.env ghcr.io/peterkappelt/hisqis-slack:main
```
Das Programm läuft nun!