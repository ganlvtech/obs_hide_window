import win32gui
try:
    import obspython
except ImportError:
    pass

WS_MINIMIZE = 0x20000000
GWL_STYLE = -16

def obs_frontend_get_current_scene_name():
    current_scene = obspython.obs_frontend_get_current_scene()
    if current_scene is None:
        return ""
    current_scene_name = obspython.obs_source_get_name(current_scene)
    obspython.obs_source_release(current_scene)
    return current_scene_name

def obs_frontend_set_current_scene(name):
    current_scene_name = obs_frontend_get_current_scene_name()
    if current_scene_name == "" or current_scene_name == name:
        return
    scenes = obspython.obs_frontend_get_scenes()
    for scene in scenes:
        scene_name = obspython.obs_source_get_name(scene)
        if scene_name == name:
            obspython.obs_frontend_set_current_scene(scene)
            print("Set scene", name)
            break
    obspython.source_list_release(scenes)

def is_window_visible(class_name, window_name):
    hwnd = 0
    while True:
        hwnd = win32gui.FindWindowEx(0, hwnd, class_name, window_name)
        if hwnd == 0:
            break
        if win32gui.IsWindowVisible(hwnd) != 0:
            window_style = win32gui.GetWindowLong(hwnd, GWL_STYLE);
            if window_style & WS_MINIMIZE == 0:
                return True
    return False

current_scene_name = obs_frontend_get_current_scene_name()

def set_current_scene(name):
    global current_scene_name
    if current_scene_name != name:
        obs_frontend_set_current_scene(name)
        current_scene_name = obs_frontend_get_current_scene_name()

def on_timer():
    if is_window_visible('TXGuiFoundation', None) or is_window_visible('CASCADIA_HOSTING_WINDOW_CLASS', None) or is_window_visible('Chrome_WidgetWin_0', '飞书') or is_window_visible('Chrome_WidgetWin_0', '飞书会议'):
        set_current_scene('模糊')
    else:
        set_current_scene('场景')

sum_seconds = 0
def script_tick(seconds):
    global sum_seconds
    sum_seconds += seconds
    if sum_seconds > 0.2:
        sum_seconds = 0
        on_timer()

