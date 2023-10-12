import os
import shutil
from datetime import datetime, timedelta
from typing import List
from common import WORKING_DIR_PATH, TEMPLATE_PATH
from confluence_export import get_tasks
import word
import ids
from lxml import etree

REPORT_FILE_PATH = "./VR Demo Project report {date}.docx"

def template_validation(tree) -> bool:
    # validate presence of all ids in template
    for id in ids.IDS:
        if word.find_by_id(tree, id) is None:
            return False

    return True


def prepare_working_directory(report_file_path: str):
    # remove tmp dir if exists
    if os.path.exists(WORKING_DIR_PATH):
        shutil.rmtree(WORKING_DIR_PATH)

    # remove report if exists
    if os.path.exists(report_file_path):
        os.remove(report_file_path)

    # copy template to the working directory
    shutil.copytree(TEMPLATE_PATH, WORKING_DIR_PATH)


def clean_working_dir():
    # remove tmp directories
    shutil.rmtree(WORKING_DIR_PATH)


def finalize_report(report_file_path: str):
    # archive directory
    shutil.make_archive(
        "report",
        "zip",
        WORKING_DIR_PATH,
    )
    # change it's extension to ".docx" and move to the right directory
    os.rename("report.zip", report_file_path)


def append_bullet_list_element_after(
    element: etree.Element, content: str, list_id
) -> etree.Element:
    bullet = word.create_bullet(list_id=list_id, lvl=0, content=content)

    # append this bullet element after specified
    word.append_element_after(new_el=bullet, after=element)

    # return new bullet element
    return bullet


def fill_task_list(tree: etree.Element, task_list_id: str, tasks: List):
    task_list_header = word.find_by_id(tree, task_list_id)

    # fill completed tasks list
    if tasks:  # fill list with tasks
        element = task_list_header
        for task in tasks:
            element = append_bullet_list_element_after(element, task, list_id=1)
    else:  # remove empty list header
        word.remove_element(task_list_header)

    
def highlight_links(text: str) -> list:
    content_list = []
    desc = text.split('<link>') 
    for _ in range(len(desc)-1):
        content_list.append(desc)
        content_list.append(word.Text("<link>", True, None, "yellow"))
    content_list.append(desc[-1])

    return content_list


def main():
    # eval report dates
    report_date = datetime.today()
    report_path = REPORT_FILE_PATH.format(date=report_date.strftime("%d-%m-%Y"))

    prepare_working_directory(report_path)

    # load document.xml (main xml file)
    tree = word.load_xml(word.DOCUMENT_PATH)

    # validate template
    if not template_validation(tree):
        print("Template is invalid! Some IDs are missing!")
        exit()

    ##################################################################
    # Update tasks
    print("Step 1/3 - Constructing task list...")

    tasks = get_tasks()

    for project in tasks:
        for task in tasks[project]:
            if "<link>" in task['description']:
                task['description'] = highlight_links(task['description'])

        # filter
        done = [task['description'] for task in tasks[project] if task['status'] == 'done']
        in_progress = [task['description'] for task in tasks[project] if task['status'] == 'in progress']
        planned = [task['description'] for task in tasks[project] if task['status'] == 'planned']

        ### DONE
        if done:
            fill_task_list(tree, ids.DONE_TASK_LIST[project], done)
        else:
            task_list = word.find_by_id(tree, ids.DONE_TASK_LIST[project])
            word.remove_element(task_list)

        ### IN PROGRESS
        if in_progress: 
            fill_task_list(tree, ids.IN_PROGRESS_TASK_LIST[project], in_progress)
        else:
            task_list = word.find_by_id(tree, ids.IN_PROGRESS_TASK_LIST[project])
            word.remove_element(task_list)

        ### PLANNED
        if planned:
            fill_task_list(tree, ids.PLANNED_TASK_LIST[project], planned)
        else:
            task_list = word.find_by_id(tree, ids.PLANNED_TASK_LIST[project])
            word.remove_element(task_list)

    ##################################################################
    # save report document.xml

    word.write_xml(tree, word.DOCUMENT_PATH)

    ##################################################################
    # update footer
    print("Step 2/3 - Updating footer...")

    # load footer.xml
    footer_tree = word.load_xml(word.FOOTER_PATH)

    report_start_date = report_date - timedelta(weeks=1) + timedelta(days=1)

    report_period_field = word.find_by_id(footer_tree, ids.REPORT_PERIOD_FIELD_ID)
    report_period_field.text = "{from_date} — {to_date}".format(
        from_date=report_start_date.strftime("%d-%B-%y"),
        to_date=report_date.strftime("%d-%B-%y"),
    )

    word.write_xml(footer_tree, word.FOOTER_PATH)

    ##################################################################
    # combine files into docx
    print("Step 3/3 - Saving report...")

    finalize_report(report_path)

    print(f"Report '{report_path}' generated!")

    clean_working_dir()


if __name__ == "__main__":
    main()
