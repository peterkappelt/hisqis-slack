# %%
import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
from datetime import datetime
import numpy as np
import os
# %%


def new_session() -> requests.Session:
  s = requests.Session()
  s.headers.update({
      "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36"
  })

  return s


def request_and_parse(session, method, url, data=None):
  if method == "GET":
    res = session.get(url, data=data)
  elif method == "POST":
    res = session.post(url, data=data)
  else:
    raise Exception("Unknown method!")

  if res.status_code != 200:
    raise Exception("Request failed with non-200")

  return (
      res.text,
      BeautifulSoup(res.content, "html.parser")
  )


def login(session):
  _, loginp = request_and_parse(
      session,
      "POST",
      f"https://qis.dez.tu-dresden.de/qisserver/servlet/de.his.servlet.RequestDispatcherServlet;jsessionid={session.cookies.get('JSESSIONID')}?state=user&type=1&category=auth.login&startpage=portal.vm",
      data={
          "submit": " Anmelden ",
          "asdf": os.environ["HISQIS_USER"],
          "fdsa": os.environ["HISQIS_PASSWORD"]
      }
  )
  login_error_msg = loginp.find_all("span", class_="newSessionMsg")
  if len(login_error_msg):
    raise Exception("Anmeldung fehlgeschlagen, stimmen Nutzername und Passwort?")
  targetlink = loginp.find_all(
      "a", class_="auflistung", string=re.compile("Prüfungsbescheinigungen "))
  if len(targetlink) != 1:
    raise Exception("Ziellink Prüfungsübersicht nicht gefunden")
  return targetlink[0]["href"]


def navigate_notenspiegel(session, pruefungsuebersicht_url):
  _, pagep = request_and_parse(session, "GET", pruefungsuebersicht_url)
  targetlink = pagep.find_all(
      "a", title="Leistungen für Abschluss 11 Diplom anzeigen")
  if len(targetlink) != 1:
    raise Exception("Ziellink Notenspiegel nicht gefunden")
  return targetlink[0]["href"]


def parse_notenspiegel(session, notenspiegel_url):
  page, _ = request_and_parse(session, "GET", notenspiegel_url)
  l = pd.read_html(page, decimal=",", thousands="|", converters={
                   "Prüfungsdatum": lambda x: print(x)})
  l = l[2]
  l.columns = ["Prüfungsnr", "Prüfungstext", "Semester", "Note", "Punkte",
               "Status", "SWS", "Bonus", "Vermerk", "Versuch", "Prüfungsdatum"]
  l.set_index("Prüfungsnr", inplace=True)
  l["Prüfungsdatum"] = l.apply(lambda x: datetime.strptime(
      x["Prüfungsdatum"], "%d.%m.%Y") if not pd.isnull(x["Prüfungsdatum"]) else np.nan, axis=1)
  l["hash"] = l.apply(lambda x: hash(str(tuple(x))), axis=1)
  return l


# %%
def get_grades():
  # %%
  s = new_session()

  pruefungsuebersicht = login(s)
  notenspiegel = navigate_notenspiegel(s, pruefungsuebersicht)
  noten = parse_notenspiegel(s, notenspiegel)
  # %%
  return noten

#%%
def get_grade_delta(old, new):
  changed_idx = pd.concat([old, new]).drop_duplicates(
      keep=False).index.unique()
  return new.loc[changed_idx]