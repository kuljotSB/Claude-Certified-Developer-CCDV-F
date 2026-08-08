from typing import Any, Dict
from mcp.server.fastmcp import FastMCP
import json

# Initialize FastMCP server
mcp = FastMCP(
    name="kuljot-mcp-server",
    host="0.0.0.0",
    port=8000
)

@mcp.tool(
    name="get_recipes_by_name",
    description="Get recipes based on the name provided by the user.",
    structured_output=True
)
def get_recipes(name: str) -> Dict[str, Any]:
    with open("recipes.json", "r") as file:
        recipes = json.load(file)
    for recipe in recipes:
        if recipe["name"].lower() == name.lower():
            return recipe
    return {"error": "Recipe not found"}


@mcp.tool(
    name="get_recipes_by_id",
    description="Get recipes based on the ID provided by the user.",
    structured_output=True
)
def get_recipes_by_id(id: int) -> Dict[str, Any]:
    with open("recipes.json", "r") as file:
        recipes = json.load(file)
    for recipe in recipes:
        if recipe["id"] == id:
            return recipe
    return {"error": "Recipe not found"}

@mcp.tool(
    name="get_courses",
    description="Get courses based on the title provided by the user.",
    structured_output=True
)
def get_courses(title: str) -> Dict[str, Any]:
    with open("courses.json", "r") as file:
        courses = json.load(file)
    matched_courses = [course for course in courses if title.lower() in course["title"].lower()]
    return {"courses": matched_courses}

@mcp.tool(
    name="get_course_by_id",
    description="Get course based on the ID provided by the user.",
    structured_output=True
)
def get_course_by_id(id: int) -> Dict[str, Any]:
    with open("courses.json", "r") as file:
        courses = json.load(file)
    for course in courses:
        if course["id"] == id:
            return course
    return {"error": "Course not found"}

@mcp.tool(
    name = "get_course_by_rating",
    description = "Get courses based on the minimum rating provided by the user.",
    structured_output = True
)
def get_course_by_rating(min_rating: float) -> Dict[str, Any]:
    with open("courses.json", "r") as file:
        courses = json.load(file)
    matched_courses = [course for course in courses if course["rating"] >= min_rating]
    return {"courses": matched_courses}

@mcp.tool(
    name="get_ufb_courses",
    description="Get all UFB courses.",
    structured_output=True
)
def get_ufb_courses() -> Dict[str, Any]:
    with open("courses.json", "r") as file:
        courses = json.load(file)
    ufb_courses = [course for course in courses if course.get("is_ufb")]
    return {"ufb_courses": ufb_courses}

if __name__ == "__main__":
    mcp.run(transport="streamable-http", mount_path="/mcp")