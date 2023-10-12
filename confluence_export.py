import os
import re
import requests
import json
from lxml import html
from datetime import datetime
from typing import Dict
from copy import deepcopy
from common import Projects

CONFLUENCE_TOKEN = os.environ["CONFLUENCE_TOKEN"]

projects_confluence_names = {
    Projects.General: "General",
    Projects.D3_Assets: "3D Assets",
    Projects.Android_Streaming_SDK: "Android / Streaming SDK",
    Projects.Unreal_Engine: "Unreal Engine",
}


def _request_two_last_reports() -> tuple:
    url = "https://luxproject.luxoft.com/confluence/rest/api/content/search"
    headers = {
        "Accept": "application/json",
        "Authorization": f"Bearer {CONFLUENCE_TOKEN}",
    }

    response = requests.get(
        f'{url}/?cql=type = Page AND title ~ "VR Project meeting " order by created desc&limit=2&expand=body.storage',
        headers=headers,
    )

    results = response.json()["results"]
    old = html.fromstring(results[1]["body"]["storage"]["value"])
    new = html.fromstring(results[0]["body"]["storage"]["value"])
    return (old, new)



def _get_projects_info(html_report: html.Element):
    projects_info: Dict = {}

    for project in projects_confluence_names:
        project_name = projects_confluence_names[project]
        projects_info[project] = []

        # find project block
        project_name_el = html_report.xpath(
            f"//strong[contains(text(),'{project_name}:')] | //strong/span[contains(text(),'{project_name}:')]"
        )[0]
        project_name_el = project_name_el.xpath("ancestor::p[1]")[0]

        # find project tasks list
        task_list_el = project_name_el.xpath("./following-sibling::task-list")[0]

        # enumerate all project tasks
        for task_el in task_list_el.xpath("./task"):
            # get task info
            task_body = html.tostring(task_el.xpath("./task-body")[0]).decode()
            task_body = re.findall(r'<task-body>(.*?)</task-body>$', task_body)[0]
            while "</span>" in task_body:
                task_body = "".join(re.findall(r'>(.*?)</span>(.*)$', task_body)[0])

            # remove weird character
            task_body = task_body.replace("\u00a0", "")
            task_body = task_body.replace("&#160;", " ")

            # split task description and status
            task_status = task_body.split(" - ")[1].strip()
            task_body = task_body.split(" - ")[0].strip()

            # remove part with time from status
            task_status = task_status.split(",")[0]

            # if deadline mentioned, add it to the description
            deadline_element = task_el.xpath(".//time")
            if deadline_element:
                task_deadline = datetime.strptime(deadline_element[0].get('datetime'), "%Y-%m-%d")
                task_body += f", ETA {task_deadline.strftime('%d %b %Y')}"

            projects_info[project].append(
                {"description": task_body, "status": task_status}
            )

    return projects_info


def get_tasks():
    # get info about projects on this week and previous
    old, new = _request_two_last_reports()

    old_projects_info = _get_projects_info(old)
    new_projects_info = _get_projects_info(new)

    # combine info
    # filter previous week tasks (only completed)

    all_projects_info = deepcopy(new_projects_info)

    for project in old_projects_info:
        all_project_info = all_projects_info[project]
        new_tasks = set([task["description"] for task in all_project_info])

        for task in old_projects_info[project]:
            if task["status"] == "done" and task["description"] not in new_tasks:
                all_project_info.append(task)

    return all_projects_info


if __name__ == "__main__":
    # Tasks
    print("Tasks:")
    tasks = get_tasks()
    for project in projects_confluence_names:
        print(projects_confluence_names[project] + ":")
        print(json.dumps(tasks[project], indent=4))


