import os
import sys
import tempfile
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path
from unittest.mock import patch

API_DIR = Path(__file__).resolve().parent
if str(API_DIR) not in sys.path:
    sys.path.insert(0, str(API_DIR))

from api import scraper


class FakeResponse:
    def __init__(self, payload):
        self.payload = payload

    def json(self):
        return self.payload


class FakeLiveWhaleAPI:
    """Small fake for the LiveWhale paginated JSON API."""

    def __init__(self, pages):
        self.pages = pages
        self.requested_pages = []

    def get(self, url):
        page = int(url.rsplit("page=", 1)[1])
        self.requested_pages.append(page)
        return FakeResponse(self.pages[page])


def iso_days_from_now(days, hour=12):
    dt = datetime.now(timezone.utc) + timedelta(days=days)
    return dt.replace(hour=hour, minute=0, second=0, microsecond=0).isoformat()


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


class TestScraperWithFakeAPI(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.db_path = os.path.join(self.temp_dir.name, "test_scraper.db")
        self.old_db_path = os.environ.get("DB_PATH")
        os.environ["DB_PATH"] = self.db_path

    def tearDown(self):
        if self.old_db_path is None:
            os.environ.pop("DB_PATH", None)
        else:
            os.environ["DB_PATH"] = self.old_db_path
        self.temp_dir.cleanup()

    def test_scrape_events_reads_expected_event_components_from_fake_api(self):
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

    def test_scrape_events_combines_recurring_events_with_same_title(self):
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


if __name__ == "__main__":
    unittest.main()
