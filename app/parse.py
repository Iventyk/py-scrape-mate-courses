import csv
from dataclasses import dataclass, fields, astuple
import requests
from bs4 import BeautifulSoup, Tag

BASE_URL = "https://mate.academy/"


@dataclass
class Course:
    name: str
    short_description: str
    duration: str


COURSE_FIELDS = [field.name for field in fields(Course)]


def parse_single_course(course_block: Tag) -> Course | None:
    """Parse a single course block from Mate Academy page."""
    try:
        name_element = course_block.select_one(".ProfessionCard_title__m7uno")
        description_element = course_block.select_one(
            ".ProfessionCard_description__K8weo"
        )
        duration_element = course_block.select_one(
            ".ProfessionCard_duration__13PwX"
        )

        if not name_element:
            return None

        name = name_element.get_text(strip=True)
        short_description = description_element.get_text(strip=True) \
            if description_element else ""
        duration = duration_element.get_text(strip=True) \
            if duration_element else ""

        return Course(
            name=name,
            short_description=short_description,
            duration=duration,
        )
    except Exception:
        return None


def get_all_courses() -> list[Course]:
    """Get all courses from Mate Academy landing page."""
    response = requests.get(BASE_URL, timeout=10)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")

    course_blocks = soup.select(".ProfessionsListSectionTemplate_card__ZNsgf")
    courses = [parse_single_course(block) for block in course_blocks]
    return [course for course in courses if course is not None]


def write_courses_to_csv(courses: list[Course], output_csv_path: str) -> None:
    """Write list of Course objects to CSV file."""
    with open(output_csv_path, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(COURSE_FIELDS)
        writer.writerows([astuple(course) for course in courses])


def main(output_csv_path: str) -> None:
    courses = get_all_courses()
    write_courses_to_csv(courses, output_csv_path)


if __name__ == "__main__":
    main("courses.csv")
