import csv
from dataclasses import dataclass, fields, astuple
import requests
from bs4 import BeautifulSoup, Tag

BASE_URL = "https://mate.academy/"


@dataclass
class Course:
    name: str
    description: str
    duration: str


COURSE_FIELDS = [field.name for field in fields(Course)]


def parse_single_course(course_block: Tag) -> Course:
    """Parse a single course block from Mate Academy page."""
    return Course(
    name=course_block.select_one(".ProfessionCard_title__m7uno").text,
    description=course_block.select_one(".ProfessionCard_description__K8weo").text,
    duration=course_block.select_one(".ProfessionCard_duration__13PwX").text,
    )


def get_all_courses() -> list[Course]:
    """Get all courses from Mate Academy landing page."""
    response = requests.get(BASE_URL, timeout=10)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")

    course_blocks = soup.select(".ProfessionsListSectionTemplate_card__ZNsgf")
    return [parse_single_course(block) for block in course_blocks]


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
