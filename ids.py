from common import Projects

DONE_TASK_LIST = {
    Projects.General: "DONE_TASK_LIST_GENERAL",
    Projects.D3_Assets: "DONE_TASK_LIST_3D_ASSETS",
    Projects.Android_Streaming_SDK: "DONE_TASK_LIST_ANDROID",
    Projects.Unreal_Engine: "DONE_TASK_LIST_UNREAL",
}
IN_PROGRESS_TASK_LIST = {
    Projects.General: "IN_PROGRESS_TASK_LIST_GENERAL",
    Projects.D3_Assets: "IN_PROGRESS_TASK_LIST_3D_ASSETS",
    Projects.Android_Streaming_SDK: "IN_PROGRESS_TASK_LIST_ANDROID",
    Projects.Unreal_Engine: "IN_PROGRESS_TASK_LIST_UNREAL",
}
PLANNED_TASK_LIST = {
    Projects.General: "PLANNED_TASK_LIST_GENERAL",
    Projects.D3_Assets: "PLANNED_TASK_LIST_3D_ASSETS",
    Projects.Android_Streaming_SDK: "PLANNED_TASK_LIST_ANDROID",
    Projects.Unreal_Engine: "PLANNED_TASK_LIST_UNREAL",
}


IDS = [
    DONE_TASK_LIST[Projects.General],
    DONE_TASK_LIST[Projects.D3_Assets],
    DONE_TASK_LIST[Projects.Android_Streaming_SDK],
    DONE_TASK_LIST[Projects.Unreal_Engine],
    IN_PROGRESS_TASK_LIST[Projects.General],
    IN_PROGRESS_TASK_LIST[Projects.D3_Assets],
    IN_PROGRESS_TASK_LIST[Projects.Android_Streaming_SDK],
    IN_PROGRESS_TASK_LIST[Projects.Unreal_Engine],
    PLANNED_TASK_LIST[Projects.General],
    PLANNED_TASK_LIST[Projects.D3_Assets],
    PLANNED_TASK_LIST[Projects.Android_Streaming_SDK],
    PLANNED_TASK_LIST[Projects.Unreal_Engine],
]

# footer ids
REPORT_PERIOD_FIELD_ID = "REPORT_PERIOD_FIELD"
