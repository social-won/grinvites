import os
import sqlite3
import sys
import tempfile
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path
from unittest.mock import patch

import requests

# Make imports work when this file is run through the root Makefile target:
#     make test-scraper
API_DIR = Path(__file__).resolve().parent
if str(API_DIR) not in sys.path:
    sys.path.insert(0, str(API_DIR))

from api import scraper


def announce(message):
    """Print a visible test step when pytest is run with -s."""
    print(f"\n[SCRAPER TEST] {message}")


def count_database_events(db_path):
    """Return the number of rows currently stored in the events table."""
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()
    cursor.execute("SELECT COUNT(*) FROM events")
    count = cursor.fetchone()[0]
    connection.close()
    return count


def first_database_event(db_path):
    """Return one database event row so tests can verify required fields."""
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()
    cursor.execute(
        """
        SELECT event_id, title, start_time, creation_time_stamp, location, summary
        FROM events
        ORDER BY id
        LIMIT 1
        """
    )
    event = cursor.fetchone()
    connection.close()
    return event


class ScraperDatabaseTestCase(unittest.TestCase):
    """Shared setup that keeps scraper tests away from the real app database."""

    def setUp(self):
        # Each test gets a temporary SQLite database so test runs are isolated.
        self.temp_dir = tempfile.TemporaryDirectory()
        self.db_path = os.path.join(self.temp_dir.name, "test_scraper.db")
        self.old_db_path = os.environ.get("DB_PATH")
        os.environ["DB_PATH"] = self.db_path

    def tearDown(self):
        # Restore the user's DB_PATH after each test, even if a test fails.
        if self.old_db_path is None:
            os.environ.pop("DB_PATH", None)
        else:
            os.environ["DB_PATH"] = self.old_db_path
        self.temp_dir.cleanup()


# ============================================================
# BASIC TESTING
# ============================================================
# These tests exercise the real scraper helper functions and the real scraper
# database path. They do not replace the LiveWhale API with fake responses.


class TestBasicScraperFunctionality(ScraperDatabaseTestCase):
    def test_text_cleaning_removes_extra_whitespace(self):
        announce("Basic test: clean_text removes leading, trailing, and repeated whitespace.")

        cleaned = scraper.clean_text("   Grinnell     Events\n\tCalendar   ")

        self.assertEqual(cleaned, "Grinnell Events Calendar")
        announce("PASS: clean_text returned a single clean sentence.")

    def test_html_cleaning_removes_tags_and_handles_empty_html(self):
        announce("Basic test: clean_html strips HTML tags and handles missing HTML safely.")

        cleaned_html = scraper.clean_html("<p>Join <strong>student orgs</strong> today.</p>")
        empty_html = scraper.clean_html(None)

        self.assertEqual(cleaned_html, "Join student orgs today.")
        self.assertEqual(empty_html, "")
        announce("PASS: clean_html removed markup and returned an empty string for None.")

    def test_name_sanitizing_normalizes_case_quotes_and_accents(self):
        announce("Basic test: sanitize_name normalizes organization names for matching.")

        sanitized = scraper.sanitize_name("  L’Équipe “Student” Organization’s  ")

        self.assertEqual(sanitized, "lequipe student organizations")
        announce("PASS: sanitize_name removed curly quotes, accents, and extra casing.")

    def test_recurrence_detection_combines_nearby_duplicate_titles(self):
        announce("Basic test: occurance_finder combines duplicate event titles within 30 days.")

        first_start = iso_days_from_now(3, hour=9)
        first_end = iso_days_from_now(3, hour=10)
        second_start = iso_days_from_now(10, hour=9)
        second_end = iso_days_from_now(10, hour=10)
        unique_start = iso_days_from_now(12, hour=14)
        far_future_start = iso_days_from_now(45, hour=9)

        events = {
            0: scraper_event(0, "Weekly Study Hall", first_start, first_end),
            1: scraper_event(1, "Weekly Study Hall", second_start, second_end),
            2: scraper_event(2, "One-Time Workshop", unique_start, iso_days_from_now(12, hour=15)),
            3: scraper_event(3, "Weekly Study Hall", far_future_start, iso_days_from_now(45, hour=10)),
        }

        scraper.occurance_finder(events)

        self.assertIn(0, events)
        self.assertNotIn(1, events)
        self.assertIn(2, events)
        self.assertIn(3, events)
        self.assertEqual(
            events[0]["occurances"],
            [
                {"start": first_start, "end": first_end},
                {"start": second_start, "end": second_end},
            ],
        )
        announce("PASS: nearby recurring events were grouped, while unique/far-future events stayed separate.")

    def test_real_scraper_populates_database_with_live_events(self):
        announce("Basic integration test: real scraper fetches live events and writes them to SQLite.")

        try:
            scraped_events = scraper.scrape_events()
        except requests.exceptions.RequestException as error:
            self.skipTest(f"Live Grinnell events API is unavailable right now: {error}")

        database_event_count = count_database_events(self.db_path)
        first_event = first_database_event(self.db_path)

        self.assertGreater(len(scraped_events), 0)
        self.assertGreater(database_event_count, 0)
        self.assertGreaterEqual(database_event_count, len(scraped_events))
        self.assertIsNotNone(first_event)

        event_id, title, start_time, creation_time_stamp, _location, _summary = first_event
        self.assertTrue(event_id)
        self.assertTrue(title)
        self.assertTrue(start_time)
        self.assertTrue(creation_time_stamp)

        announce(
            "PASS: real scraper returned "
            f"{len(scraped_events)} event(s), and the database contains {database_event_count} event row(s)."
        )


# ============================================================
# MOCK TESTING
# ============================================================
# These tests replace the LiveWhale API with controlled fake pages. This lets
# us verify edge cases without depending on the network or current campus data.


class FakeResponse:
    """Small response object that behaves like requests.get(...).json()."""

    def __init__(self, payload):
        self.payload = payload

    def json(self):
        return self.payload


class FakeLiveWhaleAPI:
    """Mock LiveWhale API that returns known pages for predictable tests."""

    def __init__(self, pages):
        self.pages = pages
        self.requested_pages = []

    def get(self, url):
        # The scraper requests URLs ending in "?page=N"; this extracts N.
        page = int(url.rsplit("page=", 1)[1])
        self.requested_pages.append(page)
        return FakeResponse(self.pages[page])


def iso_days_from_now(days, hour=12):
    """Build a timezone-aware ISO timestamp relative to test run time."""
    dt = datetime.now(timezone.utc) + timedelta(days=days)
    return dt.replace(hour=hour, minute=0, second=0, microsecond=0).isoformat()


def scraper_event(event_id, title, start_time, end_time):
    """Build the event dictionary shape used inside scraper.occurance_finder."""
    return {
        "id": event_id,
        "event_id": f"event-{event_id}",
        "creation_time_stamp": datetime.now(timezone.utc).isoformat(),
        "title": title,
        "start_time": start_time,
        "end_time": end_time,
        "location": "Test Location",
        "summary": "Test Summary",
        "categories": "",
        "tags": "",
        "org_name": "",
        "occurances": None,
    }


def livewhale_event(
    event_id,
    title,
    start_time,
    end_time,
    location="JRC 101",
    summary="<p>Default summary</p>",
    event_types=None,
    tags=None,
    organization="Student Government Association",
):
    """Build the raw JSON event shape returned by the LiveWhale endpoint."""
    return {
        "id": event_id,
        "title": title,
        "date_iso": start_time,
        "date2_time": "1:00pm",
        "date2_iso": end_time,
        "location": location,
        "summary": summary,
        "event_types": event_types or [],
        "tags": tags or [],
        "custom_organization": organization,
    }


class TestMockScraperWithFakeAPI(ScraperDatabaseTestCase):
    def test_mock_scrape_events_handles_event_without_end_time(self):
        announce("Mock test: fake API event without an end time does not crash the scraper.")

        event_without_end_time = livewhale_event(
            event_id="no-end-time-1",
            title="Mock Open-Ended Event",
            start_time=iso_days_from_now(5, hour=13),
            end_time="",
            summary="<p>This event has no listed end time.</p>",
        )
        event_without_end_time.pop("date2_time")
        event_without_end_time.pop("date2_iso")

        fake_api = FakeLiveWhaleAPI(
            {
                1: {
                    "meta": {"total_pages": 1},
                    "data": [event_without_end_time],
                }
            }
        )

        with patch.object(scraper.requests, "get", side_effect=fake_api.get):
            events = scraper.scrape_events()

        self.assertEqual(len(events), 1)
        self.assertEqual(events[0]["title"], "Mock Open-Ended Event")
        self.assertEqual(events[0]["end_time"], "")

        announce("PASS: missing end-time data is stored as an empty string.")

    def test_mock_scrape_events_reads_expected_event_components_from_fake_api(self):
        announce("Mock test: fake API pages are converted into scraper event dictionaries.")

        first_event = livewhale_event(
            event_id="livewhale-101",
            title="Mock Board Game Night",
            start_time=iso_days_from_now(2, hour=18),
            end_time=iso_days_from_now(2, hour=20),
            location="Harris Center",
            summary="<p>Play games with <strong>friends</strong>.</p>",
            event_types=["Social", "Student Event"],
            tags=["games", "community"],
            organization="Student Government Association",
        )
        second_event = livewhale_event(
            event_id="livewhale-202",
            title="Mock Research Talk",
            start_time=iso_days_from_now(4, hour=16),
            end_time=iso_days_from_now(4, hour=17),
            location="Noyce 2022",
            summary="<div>Faculty research presentation.</div>",
            event_types=["Academic"],
            tags=["research"],
            organization="Computer Science",
        )
        fake_api = FakeLiveWhaleAPI(
            {
                1: {"meta": {"total_pages": 2}, "data": [first_event]},
                2: {"meta": {"total_pages": 2}, "data": [second_event]},
            }
        )

        with patch.object(scraper.requests, "get", side_effect=fake_api.get):
            events = scraper.scrape_events()

        self.assertEqual(fake_api.requested_pages, [1, 1, 2])
        self.assertEqual(len(events), 2)

        scraped = events[0]
        self.assertEqual(scraped["event_id"], "livewhale-101")
        self.assertEqual(scraped["title"], "Mock Board Game Night")
        self.assertEqual(scraped["start_time"], first_event["date_iso"])
        self.assertEqual(scraped["end_time"], first_event["date2_iso"])
        self.assertEqual(scraped["location"], "Harris Center")
        self.assertEqual(scraped["summary"], "Play games with friends .")
        self.assertEqual(scraped["categories"], "Social,Student Event")
        self.assertEqual(scraped["tags"], "games,community")
        self.assertEqual(scraped["org_name"], "Student Government Association")

        announce("PASS: fake API data was scraped into the expected event fields.")

    def test_mock_scrape_events_combines_recurring_events_with_same_title(self):
        announce("Mock test: fake recurring events with the same title are grouped.")

        first_start = iso_days_from_now(3, hour=9)
        first_end = iso_days_from_now(3, hour=10)
        second_start = iso_days_from_now(10, hour=9)
        second_end = iso_days_from_now(10, hour=10)
        fake_api = FakeLiveWhaleAPI(
            {
                1: {
                    "meta": {"total_pages": 1},
                    "data": [
                        livewhale_event("repeat-1", "Weekly Mock Meetup", first_start, first_end),
                        livewhale_event("repeat-2", "Weekly Mock Meetup", second_start, second_end),
                    ],
                }
            }
        )

        with patch.object(scraper.requests, "get", side_effect=fake_api.get):
            events = scraper.scrape_events()

        self.assertEqual(len(events), 1)
        self.assertEqual(events[0]["title"], "Weekly Mock Meetup")
        self.assertEqual(
            events[0]["occurances"],
            [
                {"start": first_start, "end": first_end},
                {"start": second_start, "end": second_end},
            ],
        )

        announce("PASS: recurring fake API events were combined into one event with occurances.")


if __name__ == "__main__":
    unittest.main(verbosity=2)
