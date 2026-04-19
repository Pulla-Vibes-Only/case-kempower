# Tests for translations.py
# PullA Vibes
# Tests cover English, Finnish and Swedish translations for key strings,
# fallback behavior for missing keys and unknown languages,
# and a parity check that all three languages have identical keys.

import sys
import pytest

sys.path.insert(0, "..")

from translations import Translations


class TestTranslationsEnglish:
    def test_welcome(self):
        # English welcome message should match expected string
        assert Translations.translate("ENG", "welcome") == "WELCOME TO OUR HOTEL!"

    def test_login(self):
        # English login label should match expected string
        assert Translations.translate("ENG", "login") == "LOGIN"

    def test_zone_names(self):
        # English zone names should return untranslated plain English strings
        assert Translations.translate("ENG", "main") == "main"
        assert Translations.translate("ENG", "bedroom") == "bedroom"
        assert Translations.translate("ENG", "bathroom") == "bathroom"

    def test_on_off(self):
        # English on/off strings should be "on" and "off"
        assert Translations.translate("ENG", "on") == "on"
        assert Translations.translate("ENG", "off") == "off"

    def test_brightness_limits(self):
        # English brightness limit messages should mention min and max
        assert "min" in Translations.translate("ENG", "brightness_min").lower()
        assert "max" in Translations.translate("ENG", "brightness_max").lower()


class TestTranslationsFinnish:
    def test_welcome(self):
        # Finnish welcome message should match expected string
        assert Translations.translate("FIN", "welcome") == "TERVETULOA HOTELLIIMME!"

    def test_login(self):
        # Finnish login label should match expected string
        assert Translations.translate("FIN", "login") == "KIRJAUDU"

    def test_zone_names(self):
        # Finnish zone names should return correct Finnish translations
        assert Translations.translate("FIN", "main") == "pää"
        assert Translations.translate("FIN", "bedroom") == "makuuhuone"
        assert Translations.translate("FIN", "bathroom") == "kylpyhuone"

    def test_on_off(self):
        # Finnish on/off strings should be "päälle" and "pois"
        assert Translations.translate("FIN", "on") == "päälle"
        assert Translations.translate("FIN", "off") == "pois"


class TestTranslationsSwedish:
    def test_welcome(self):
        # Swedish welcome message should match expected string
        assert Translations.translate("SWE", "welcome") == "VÄLKOMMEN TILL VÅRT HOTELL!"

    def test_login(self):
        # Swedish login label should match expected string
        assert Translations.translate("SWE", "login") == "LOGGA IN"

    def test_zone_names(self):
        # Swedish zone names should return correct Swedish translations
        assert Translations.translate("SWE", "sauna") == "bastu"
        assert Translations.translate("SWE", "balcony") == "balkong"

    def test_on_off(self):
        # Swedish on/off strings should be "på" and "av"
        assert Translations.translate("SWE", "on") == "på"
        assert Translations.translate("SWE", "off") == "av"


class TestTranslationsFallback:
    def test_missing_key_returns_key(self):
        # A key that does not exist should be returned as-is
        assert Translations.translate("ENG", "nonexistent_key_xyz") == "nonexistent_key_xyz"

    def test_unknown_language_returns_key(self):
        # An unsupported language code should return the key as-is
        assert Translations.translate("DEU", "welcome") == "welcome"

    def test_all_languages_have_same_keys(self):
        # All three languages should have exactly the same set of translation keys
        eng_keys = set(Translations._translations["ENG"].keys())
        fin_keys = set(Translations._translations["FIN"].keys())
        swe_keys = set(Translations._translations["SWE"].keys())
        assert eng_keys == fin_keys, f"FIN missing keys: {eng_keys - fin_keys}"
        assert eng_keys == swe_keys, f"SWE missing keys: {eng_keys - swe_keys}"