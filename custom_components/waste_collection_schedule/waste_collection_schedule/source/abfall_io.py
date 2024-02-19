import datetime
import logging
import re
from html.parser import HTMLParser

import requests
from waste_collection_schedule import Collection  # type: ignore[attr-defined]
from waste_collection_schedule.service.AbfallIO import SERVICE_MAP
from waste_collection_schedule.service.ICS import ICS

TITLE = "Abfall.IO / AbfallPlus"
DESCRIPTION = (
    "Source for AbfallPlus.de waste collection. Service is hosted on abfall.io."
)
URL = "https://www.abfallplus.de"
COUNTRY = "de"


def EXTRA_INFO():
    return [{"title": s["title"], "url": s["url"]} for s in SERVICE_MAP]


TEST_CASES = {
    "Waldenbuch": {
        "key": "8215c62763967916979e0e8566b6172e",
        "f_id_kommune": 2999,
        "f_id_strasse": 1087,
        # "f_abfallarten": [50, 53, 31, 299, 328, 325]
    },
    "Landshut": {
        "key": "bd0c2d0177a0849a905cded5cb734a6f",
        "f_id_kommune": 2655,
        "f_id_bezirk": 2655,
        "f_id_strasse": 763,
        # "f_abfallarten": [31, 17, 19, 218]
    },
    "Schoenmackers": {
        "key": "e5543a3e190cb8d91c645660ad60965f",
        "f_id_kommune": 3682,
        "f_id_strasse": "3682adenauerplatz",
        "f_id_strasse_hnr": "20417",
        # "f_abfallarten": [691,692,696,695,694,701,700,693,703,704,697,699],
    },
    "Freudenstadt": {
        "key": "595f903540a36fe8610ec39aa3a06f6a",
        "f_id_kommune": 3447,
        "f_id_bezirk": 22017,
        "f_id_strasse": 22155,
    },
    "Ludwigshafen am Rhein": {
        "key": "6efba91e69a5b454ac0ae3497978fe1d",
        "f_id_kommune": "5916",
        "f_id_strasse": "5916abteistrasse",
        "f_id_strasse_hnr": 33,
    },
    "Traunstein": {
        "key": "279cc5db4db838d1cfbf42f6f0176a90",
        "f_id_kommune": "2911",
        "f_id_strasse": "2374",
    },
    "AWB Limburg-Weilburg": {
        "key": "0ff491ffdf614d6f34870659c0c8d917",
        "f_id_kommune": 6031,
        "f_id_strasse": 621,
        "f_id_strasse_hnr": 872,
        "f_abfallarten": [27, 28, 17, 67],
    },
    "ALBA Berlin": {
        "key": "9583a2fa1df97ed95363382c73b41b1b",
        "f_id_kommune": 3227,
        "f_id_strasse": 3475,
        "f_id_strasse_hnr": 185575,
    },
}
_LOGGER = logging.getLogger(__name__)

MODUS_KEY = "d6c5855a62cf32a4dadbc2831f0f295f"
HEADERS = {"user-agent": "Mozilla/5.0 (xxxx Windows NT 10.0; Win64; x64)"}


# Parser for HTML input (hidden) text
class HiddenInputParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self._args = {}

    @property
    def args(self):
        return self._args

    def handle_starttag(self, tag, attrs):
        if tag == "input":
            d = dict(attrs)
            if d["type"] == "hidden":
                self._args[d["name"]] = d["value"]


class Source:
    def __init__(
        self,
        key,
        f_id_kommune,
        f_id_strasse,
        f_id_bezirk=None,
        f_id_strasse_hnr=None,
        f_abfallarten=[],
    ):
        self._key = key
        self._kommune = f_id_kommune
        self._bezirk = f_id_bezirk
        self._strasse = f_id_strasse
        self._strasse_hnr = f_id_strasse_hnr
        self._abfallarten = f_abfallarten  # list of integers
        self._ics = ICS()

    def fetch(self):
        # get token
        params = {"key": self._key, "modus": MODUS_KEY, "waction": "init"}

        r = requests.post("https://api.abfall.io", params=params, headers=HEADERS)

        # add all hidden input fields to form data
        # There is one hidden field which acts as a token:
        # It consists of a UUID key and a UUID value.
        p = HiddenInputParser()
        p.feed(r.text)
        args = p.args

        args["f_id_kommune"] = self._kommune
        args["f_id_strasse"] = self._strasse

        if self._bezirk is not None:
            args["f_id_bezirk"] = self._bezirk

        if self._strasse_hnr is not None:
            args["f_id_strasse_hnr"] = self._strasse_hnr

        for i in range(len(self._abfallarten)):
            args[f"f_id_abfalltyp_{i}"] = self._abfallarten[i]

        args["f_abfallarten_index_max"] = len(self._abfallarten)
        args["f_abfallarten"] = ",".join(map(lambda x: str(x), self._abfallarten))

        now = datetime.datetime.now()
        date2 = now.replace(year=now.year + 1)
        args["f_zeitraum"] = f"{now.strftime('%Y%m%d')}-{date2.strftime('%Y%m%d')}"

        params = {"key": self._key, "modus": MODUS_KEY, "waction": "export_ics"}

        # get csv file
        r = requests.post(
            "https://api.abfall.io", params=params, data=args, headers=HEADERS
        )

        # parse ics file
        r.encoding = "utf-8"  # requests doesn't guess the encoding correctly
        ics_file = r.text

        # Remove all lines starting with <b
        # This warning are caused for customers which use an extra radiobutton
        # list to add special waste types:
        # - AWB Limburg-Weilheim uses this list to select a "Sonderabfall <city>"
        #   waste type. The warning could be removed by adding the extra config
        #   option "f_abfallarten" with the following values [27, 28, 17, 67]
        html_warnings = re.findall(r"\<b.*", ics_file)
        if html_warnings:
            ics_file = re.sub(r"\<br.*|\<b.*", "\\r", ics_file)
            # _LOGGER.warning("Html tags removed from ics file: " + ', '.join(html_warnings))

        dates = self._ics.convert(ics_file)

        entries = []
        for d in dates:
            entries.append(Collection(d[0], d[1]))
        return entries
