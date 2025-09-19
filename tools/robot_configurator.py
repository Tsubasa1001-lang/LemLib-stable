#!/usr/bin/env python3
"""Interactive CLI for configuring robot components and generating robot source files."""
from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any, Dict, List, Optional

REPO_ROOT = Path(__file__).resolve().parents[1]
CONFIG_PATH = REPO_ROOT / "tools" / "robot_config.json"
ROBOT_CPP_PATH = REPO_ROOT / "src" / "robot.cpp"
ROBOT_HPP_PATH = REPO_ROOT / "include" / "robot.hpp"


def default_config() -> Dict[str, Any]:
    """Return the default configuration for the robot."""
    return {
        "motors": [
            {
                "name": "LeftFront",
                "port": -1,
                "gearset": "pros::v5::MotorGears::blue",
                "comment": "左前方馬達",
                "enabled": True,
            },
            {
                "name": "LeftBack",
                "port": -3,
                "gearset": "pros::v5::MotorGears::blue",
                "comment": "左後方馬達",
                "enabled": True,
            },
            {
                "name": "RightFront",
                "port": 2,
                "gearset": "pros::v5::MotorGears::blue",
                "comment": "右前方馬達",
                "enabled": True,
            },
            {
                "name": "RightBack",
                "port": 4,
                "gearset": "pros::v5::MotorGears::blue",
                "comment": "右後方馬達",
                "enabled": True,
            },
            {
                "name": "FrontIntake",
                "port": -15,
                "gearset": "pros::v5::MotorGears::blue",
                "comment": "前方 intake 馬達",
                "enabled": True,
            },
        ],
        "motor_groups": [
            {
                "name": "LeftGroup",
                "ports": [-5, 6, -7],
                "gearset": "pros::v5::MotorGears::blue",
                "units": "pros::v5::MotorUnits::degrees",
                "comment": "左側馬達組設定",
                "enabled": True,
            },
            {
                "name": "RightGroup",
                "ports": [8, -9, 10],
                "gearset": "pros::v5::MotorGears::blue",
                "units": "pros::v5::MotorUnits::degrees",
                "comment": "右側馬達組設定",
                "enabled": True,
            },
            {
                "name": "BackIntake",
                "ports": [12, -13, -14],
                "gearset": "pros::v5::MotorGears::blue",
                "units": "pros::v5::MotorUnits::degrees",
                "comment": "後方 intake 馬達群組",
                "enabled": True,
            },
        ],
        "drivetrain": {
            "name": "drivetrain",
            "left_group": "LeftGroup",
            "right_group": "RightGroup",
            "track_width": 10,
            "wheel_type": "lemlib::Omniwheel::NEW_275",
            "rpm": 480,
            "horizontal_drift": 2,
            "comment": "底盤配置",
            "enabled": True,
        },
        "sensors": [
            {"name": "Op", "type": "pros::Optical", "args": [11], "comment": "", "enabled": True},
            {"name": "GPS", "type": "pros::Gps", "args": [20, -100, 70], "comment": "", "enabled": True},
            {"name": "FDistance", "type": "pros::Distance", "args": [21], "comment": "", "enabled": True},
            {"name": "imu", "type": "pros::Imu", "args": [16], "comment": "", "enabled": True},
            {"name": "horizontal_encoder", "type": "pros::Rotation", "args": [18], "comment": "", "enabled": True},
            {"name": "left_vertical_encoder", "type": "pros::Rotation", "args": [17], "comment": "", "enabled": True},
            {"name": "right_vertical_encoder", "type": "pros::Rotation", "args": [-19], "comment": "", "enabled": True},
        ],
        "controllers": [
            {
                "name": "Player1",
                "type": "pros::Controller",
                "args": ["pros::E_CONTROLLER_MASTER"],
                "comment": "",
                "enabled": True,
            },
            {
                "name": "Player2",
                "type": "pros::Controller",
                "args": ["pros::E_CONTROLLER_PARTNER"],
                "comment": "",
                "enabled": True,
            },
        ],
        "expo_drive_curve": {
            "name": "expoCurve",
            "deadband": 10,
            "min_output": 10,
            "curve": 1.02,
            "comment": "控制搖桿輸入的 Expo 曲線（死區10，最小輸出10，曲線增益1.02，可依手感調整）",
        },
        "digital_outputs": [
            {"name": "Clamp", "port": "'A'", "comment": "", "enabled": True},
            {"name": "Arm1stg", "port": "'B'", "comment": "", "enabled": True},
            {"name": "Arm2stg", "port": "'C'", "comment": "", "enabled": True},
            {"name": "Arm2stgBack", "port": "'D'", "comment": "", "enabled": True},
            {"name": "Wing", "port": "'E'", "comment": "", "enabled": True},
            {"name": "Climb", "port": "'F'", "comment": "", "enabled": True},
            {"name": "IntakeUp", "port": "'G'", "comment": "", "enabled": True},
        ],
        "tracking_wheels": [
            {
                "name": "horizontal_tracking_wheel",
                "encoder": "horizontal_encoder",
                "wheel_enum": "lemlib::Omniwheel::NEW_2",
                "offset": 0,
                "comment": "horizontal tracking wheel",
                "enabled": True,
            },
            {
                "name": "left_vertical_tracking_wheel",
                "encoder": "left_vertical_encoder",
                "wheel_enum": "lemlib::Omniwheel::NEW_2",
                "offset": -2.5,
                "comment": "vertical tracking wheel",
                "enabled": True,
            },
        ],
        "odom_sensors": {
            "name": "sensors",
            "vertical1": "left_vertical_tracking_wheel",
            "vertical2": None,
            "horizontal1": "horizontal_tracking_wheel",
            "horizontal2": None,
            "inertial": "imu",
        },
        "controller_settings": {
            "lateral": {
                "name": "lateral_controller",
                "kP": 20,
                "kI": 0,
                "kD": 3,
                "anti_windup": 3,
                "small_error": 1,
                "small_timeout": 100,
                "large_error": 3,
                "large_timeout": 500,
                "slew": 20,
            },
            "angular": {
                "name": "angular_controller",
                "kP": 8,
                "kI": 0,
                "kD": 10,
                "anti_windup": 3,
                "small_error": 1,
                "small_timeout": 100,
                "large_error": 3,
                "large_timeout": 500,
                "slew": 0,
            },
        },
        "chassis": {
            "name": "chassis",
            "drivetrain": "drivetrain",
            "lateral": "lateral_controller",
            "angular": "angular_controller",
            "sensors": "sensors",
        },
        "pid": [
            {
                "name": "distancePID",
                "kP": 0.5,
                "kI": 0,
                "kD": 0,
                "comment": "請根據實際需求調整參數",
                "enabled": True,
            },
            {
                "name": "anglePID",
                "kP": 2.0,
                "kI": 0,
                "kD": 0,
                "comment": "請根據實際需求調整參數",
                "enabled": True,
            },
        ],
        "x_drive": {
            "name": "XDrive",
            "motors": ["LeftFront", "RightFront", "LeftBack", "RightBack"],
            "length": 10,
            "width": 4,
            "wheel_diameter": 360,
            "drift": 2,
            "sensors": "sensors",
            "comment": "X-Drive 底盤實例",
        },
    }


def load_config() -> Dict[str, Any]:
    if CONFIG_PATH.exists():
        with CONFIG_PATH.open("r", encoding="utf-8") as fp:
            return json.load(fp)
    return default_config()


def save_config(config: Dict[str, Any]) -> None:
    with CONFIG_PATH.open("w", encoding="utf-8") as fp:
        json.dump(config, fp, indent=2, ensure_ascii=False)
        fp.write("\n")


def parse_value(text: str) -> Any:
    text = text.strip()
    if not text:
        return None
    if text.lower() == "none" or text.lower() == "null":
        return None
    try:
        return int(text)
    except ValueError:
        try:
            return float(text)
        except ValueError:
            return text


def prompt(message: str, default: Optional[Any] = None) -> Optional[str]:
    if default is None:
        raw = input(f"{message}: ")
    else:
        raw = input(f"{message} [{default}]: ")
    if raw.strip() == "":
        return None
    return raw


def prompt_number(message: str, default: Optional[float] = None, is_int: bool = False) -> Optional[float]:
    while True:
        raw = prompt(message, default)
        if raw is None:
            return default
        try:
            return int(raw) if is_int else float(raw)
        except ValueError:
            print("請輸入數字。")


def prompt_bool(message: str, default: bool) -> bool:
    default_str = "Y" if default else "N"
    while True:
        raw = prompt(f"{message} (Y/N)", default_str)
        if raw is None:
            return default
        if raw.lower() in {"y", "yes"}:
            return True
        if raw.lower() in {"n", "no"}:
            return False
        print("請輸入 Y 或 N。")


def prompt_list(message: str, default: List[Any]) -> List[Any]:
    raw = prompt(message, ", ".join(str(x) for x in default))
    if raw is None:
        return default
    if raw.strip() == "":
        return []
    return [parse_value(part) for part in raw.split(",")]


def generate_motor_lines(config: Dict[str, Any]) -> List[str]:
    lines = ["// 馬達初始化"]
    for motor in config.get("motors", []):
        line = f"pros::Motor {motor['name']}({motor['port']}, {motor['gearset']});"
        if motor.get("comment"):
            line += f" // {motor['comment']}"
        if not motor.get("enabled", True):
            line = "// " + line
        lines.append(line)
    lines.append("")
    return lines


def generate_motor_group_lines(config: Dict[str, Any]) -> List[str]:
    lines = ["// 馬達群組初始化"]
    for group in config.get("motor_groups", []):
        ports = ", ".join(str(p) for p in group.get("ports", []))
        line = (
            f"pros::MotorGroup {group['name']}({{{ports}}}, {group['gearset']}, {group['units']});"
        )
        if group.get("comment"):
            line += f" // {group['comment']}"
        if not group.get("enabled", True):
            line = "// " + line
        lines.append(line)
    lines.append("")
    return lines


def generate_drivetrain_lines(config: Dict[str, Any]) -> List[str]:
    drivetrain = config.get("drivetrain", {})
    lines = []
    if drivetrain.get("comment"):
        lines.append(f"// {drivetrain['comment']}")
    if drivetrain.get("enabled", True):
        lines.append(
            f"lemlib::Drivetrain {drivetrain['name']}("
            f"&{drivetrain['left_group']}, // left motor group"
        )
        lines.append(f"                              &{drivetrain['right_group']}, // right motor group")
        lines.append(
            f"                              {drivetrain['track_width']}, // track width"
        )
        lines.append(
            f"                              {drivetrain['wheel_type']}, // wheel type"
        )
        lines.append(f"                              {drivetrain['rpm']}, // drivetrain rpm")
        lines.append(
            f"                              {drivetrain['horizontal_drift']} // horizontal drift"
        )
        lines.append(");")
    else:
        lines.append("// lemlib::Drivetrain 設定已停用")
    lines.append("")
    return lines


def generate_sensor_lines(config: Dict[str, Any]) -> List[str]:
    lines = ["// 感測器初始化"]
    for sensor in config.get("sensors", []):
        args = ", ".join(str(a) for a in sensor.get("args", []))
        line = f"{sensor['type']} {sensor['name']}({args});"
        if sensor.get("comment"):
            line += f" // {sensor['comment']}"
        if not sensor.get("enabled", True):
            line = "// " + line
        lines.append(line)
    lines.append("")
    return lines


def generate_controller_lines(config: Dict[str, Any]) -> List[str]:
    lines = ["// 控制器初始化"]
    for controller in config.get("controllers", []):
        args = ", ".join(str(a) for a in controller.get("args", []))
        line = f"{controller['type']} {controller['name']}({args});"
        if controller.get("comment"):
            line += f" // {controller['comment']}"
        if not controller.get("enabled", True):
            line = "// " + line
        lines.append(line)
    lines.append("")
    return lines


def generate_expo_curve_lines(config: Dict[str, Any]) -> List[str]:
    curve = config.get("expo_drive_curve", {})
    lines = []
    comment = curve.get("comment")
    if comment:
        lines.append(f"// {comment}")
    lines.append(
        f"lemlib::ExpoDriveCurve {curve['name']}({curve['deadband']}, {curve['min_output']}, {curve['curve']});"
    )
    lines.append("")
    return lines


def generate_digital_output_lines(config: Dict[str, Any]) -> List[str]:
    lines = ["// 數位輸出初始化"]
    for dio in config.get("digital_outputs", []):
        line = f"pros::ADIDigitalOut {dio['name']}({dio['port']});"
        if dio.get("comment"):
            line += f" // {dio['comment']}"
        if not dio.get("enabled", True):
            line = "// " + line
        lines.append(line)
    lines.append("")
    return lines


def generate_tracking_wheel_lines(config: Dict[str, Any]) -> List[str]:
    lines: List[str] = []
    tracking = config.get("tracking_wheels", [])
    if tracking:
        lines.append("// 追蹤輪設定")
    for wheel in tracking:
        line = (
            f"lemlib::TrackingWheel {wheel['name']}(&{wheel['encoder']}, {wheel['wheel_enum']}, {wheel['offset']});"
        )
        if wheel.get("comment"):
            line += f" // {wheel['comment']}"
        if not wheel.get("enabled", True):
            line = "// " + line
        lines.append(line)
    if tracking:
        lines.append("")
    return lines


def generate_odom_sensors_lines(config: Dict[str, Any]) -> List[str]:
    odom = config.get("odom_sensors", {})
    if not odom:
        return []
    name = odom["name"]
    lines = ["// odometry settings"]
    v1 = odom.get("vertical1")
    v2 = odom.get("vertical2")
    h1 = odom.get("horizontal1")
    h2 = odom.get("horizontal2")
    imu_name = odom.get("inertial")
    def fmt(value: Optional[str]) -> str:
        return f"&{value}" if value else "nullptr"

    lines.append(
        f"lemlib::OdomSensors {name}({fmt(v1)}, // vertical tracking wheel 1"
    )
    lines.append(
        f"                            {fmt(v2)}, // vertical tracking wheel 2"
    )
    lines.append(
        f"                            {fmt(h1)}, // horizontal tracking wheel 1"
    )
    lines.append(
        f"                            {fmt(h2)}, // horizontal tracking wheel 2"
    )
    lines.append(f"                            &{imu_name} // inertial sensor")
    lines.append(");")
    lines.append("")
    return lines


def generate_controller_settings_lines(config: Dict[str, Any]) -> List[str]:
    settings = config.get("controller_settings", {})
    lines: List[str] = []
    if settings:
        lines.append("// PID 控制器設定")
    for key in ("lateral", "angular"):
        if key not in settings:
            continue
        cfg = settings[key]
        lines.append(
            f"lemlib::ControllerSettings {cfg['name']}({cfg['kP']}, // proportional gain (kP)"
        )
        lines.append(f"                                              {cfg['kI']}, // integral gain (kI)")
        lines.append(f"                                              {cfg['kD']}, // derivative gain (kD)")
        lines.append(f"                                              {cfg['anti_windup']}, // anti windup")
        unit = "inches" if key == "lateral" else "degrees"
        lines.append(f"                                              {cfg['small_error']}, // small error range, in {unit}")
        lines.append(
            f"                                              {cfg['small_timeout']}, // small error range timeout, in milliseconds"
        )
        lines.append(f"                                              {cfg['large_error']}, // large error range, in {unit}")
        lines.append(
            f"                                              {cfg['large_timeout']}, // large error range timeout, in milliseconds"
        )
        lines.append(
            f"                                              {cfg['slew']} // maximum acceleration (slew)"
        )
        lines.append(");")
        lines.append("")
    return lines


def generate_chassis_lines(config: Dict[str, Any]) -> List[str]:
    chassis = config.get("chassis", {})
    if not chassis:
        return []
    lines = ["// 底盤建立"]
    lines.append(
        f"lemlib::Chassis {chassis['name']}({chassis['drivetrain']}, // drivetrain settings"
    )
    lines.append(
        f"                        {chassis['lateral']}, // lateral PID settings"
    )
    lines.append(
        f"                        {chassis['angular']}, // angular PID settings"
    )
    lines.append(f"                        {chassis['sensors']} // odometry sensors")
    lines.append(");")
    lines.append("")
    return lines


def generate_pid_lines(config: Dict[str, Any]) -> List[str]:
    lines = ["// PID 控制器初始化"]
    for pid in config.get("pid", []):
        line = f"lemlib::PID {pid['name']}({pid['kP']}, {pid['kI']}, {pid['kD']});"
        if pid.get("comment"):
            line += f" // {pid['comment']}"
        if not pid.get("enabled", True):
            line = "// " + line
        lines.append(line)
    lines.append("")
    return lines


def generate_xdrive_lines(config: Dict[str, Any]) -> List[str]:
    x_drive = config.get("x_drive", {})
    if not x_drive:
        return []
    motor_list = [str(m) for m in x_drive.get("motors", []) if str(m)]
    motor_args = ", ".join(f"&{m}" for m in motor_list)
    prefix = f"{motor_args}, " if motor_args else ""
    lines = [
        f"XDrivetrain {x_drive['name']}({prefix}{x_drive['length']}, {x_drive['width']}, {x_drive['wheel_diameter']}, {x_drive['drift']}, &{x_drive['sensors']});"
    ]
    if x_drive.get("comment"):
        lines[0] += f" // {x_drive['comment']}"
    lines.append("")
    return lines


def generate_robot_cpp(config: Dict[str, Any]) -> str:
    lines: List[str] = ["#include \"robot.hpp\"", ""]
    lines.extend(generate_motor_lines(config))
    lines.extend(generate_motor_group_lines(config))
    lines.extend(generate_drivetrain_lines(config))
    lines.extend(generate_sensor_lines(config))
    lines.extend(generate_controller_lines(config))
    lines.extend(generate_expo_curve_lines(config))
    lines.extend(generate_digital_output_lines(config))
    lines.extend(generate_tracking_wheel_lines(config))
    lines.extend(generate_odom_sensors_lines(config))
    lines.extend(generate_controller_settings_lines(config))
    lines.extend(generate_chassis_lines(config))
    lines.extend(generate_pid_lines(config))
    lines.extend(generate_xdrive_lines(config))
    return "\n".join(lines).rstrip() + "\n"


def generate_robot_hpp(config: Dict[str, Any]) -> str:
    lines: List[str] = [
        "#ifndef ROBOT_HPP",
        "#define ROBOT_HPP",
        "",
        "#include \"main.h\"",
        "#include \"lemlib/chassis/XDrivetrain.hpp\"",
        "#include \"lemlib/chassis/chassis.hpp\"",
        "#include \"lemlib/chassis/odom.hpp\"",
        "#include \"lemlib/chassis/trackingWheel.hpp\"",
        "",
    ]
    motors = [motor for motor in config.get("motors", []) if motor.get("enabled", True)]
    if motors:
        lines.append("// 馬達宣告")
        for motor in motors:
            decl = f"extern pros::Motor {motor['name']};"
            if motor.get("comment"):
                decl += f" // {motor['comment']}"
            lines.append(decl)
        lines.append("")
    groups = [group for group in config.get("motor_groups", []) if group.get("enabled", True)]
    if groups:
        lines.append("// 馬達群組宣告")
        for group in groups:
            decl = f"extern pros::MotorGroup {group['name']};"
            if group.get("comment"):
                decl += f" // {group['comment']}"
            lines.append(decl)
        lines.append("")
    drivetrain = config.get("drivetrain", {})
    if drivetrain.get("enabled", True):
        lines.append("// 底盤設定宣告")
        lines.append(f"extern lemlib::Drivetrain {drivetrain['name']};")
        lines.append("")
    sensors = [sensor for sensor in config.get("sensors", []) if sensor.get("enabled", True)]
    if sensors:
        lines.append("// 感測器宣告")
        for sensor in sensors:
            lines.append(f"extern {sensor['type']} {sensor['name']};")
        lines.append("")
    controllers = [c for c in config.get("controllers", []) if c.get("enabled", True)]
    if controllers:
        lines.append("// 控制器宣告")
        for controller in controllers:
            lines.append(f"extern {controller['type']} {controller['name']};")
        lines.append("")
    lines.append(f"extern lemlib::ExpoDriveCurve {config['expo_drive_curve']['name']};")
    lines.append("")
    digital_outputs = [dio for dio in config.get("digital_outputs", []) if dio.get("enabled", True)]
    if digital_outputs:
        lines.append("// 數位輸出宣告")
        for dio in digital_outputs:
            lines.append(f"extern pros::ADIDigitalOut {dio['name']};")
        lines.append("")
    tracking = [wheel for wheel in config.get("tracking_wheels", []) if wheel.get("enabled", True)]
    if tracking:
        lines.append("// 追蹤輪宣告")
        for wheel in tracking:
            lines.append(f"extern lemlib::TrackingWheel {wheel['name']};")
        lines.append("")
    odom = config.get("odom_sensors", {})
    if odom:
        lines.append("// 里程感測器宣告")
        lines.append(f"extern lemlib::OdomSensors {odom['name']};")
        lines.append("")
    controller_settings = config.get("controller_settings", {})
    if controller_settings:
        lines.append("// PID 控制器設定宣告")
        for key in ("lateral", "angular"):
            if key in controller_settings:
                lines.append(
                    f"extern lemlib::ControllerSettings {controller_settings[key]['name']};"
                )
        lines.append("")
    chassis = config.get("chassis", {})
    if chassis:
        lines.append("// 底盤物件宣告")
        lines.append(f"extern lemlib::Chassis {chassis['name']};")
        lines.append("")
    pid_list = [pid for pid in config.get("pid", []) if pid.get("enabled", True)]
    if pid_list:
        lines.append("// PID 控制器宣告")
        for pid in pid_list:
            lines.append(f"extern lemlib::PID {pid['name']};")
        lines.append("")
    x_drive = config.get("x_drive", {})
    if x_drive:
        lines.append("// X-Drive 底盤宣告")
        lines.append(f"extern XDrivetrain {x_drive['name']};")
        lines.append("")
    lines.append("#endif")
    lines.append("")
    return "\n".join(lines)


def write_robot_files(config: Dict[str, Any]) -> None:
    ROBOT_CPP_PATH.write_text(generate_robot_cpp(config), encoding="utf-8")
    ROBOT_HPP_PATH.write_text(generate_robot_hpp(config), encoding="utf-8")


def list_entries(entries: List[Dict[str, Any]], fields: List[str]) -> None:
    for idx, entry in enumerate(entries):
        status = "啟用" if entry.get("enabled", True) else "停用"
        summary = ", ".join(f"{field}={entry.get(field)}" for field in fields)
        print(f"[{idx}] {entry.get('name', '<未命名>')} ({status}) -> {summary}")


def configure_motors(config: Dict[str, Any]) -> None:
    motors = config.setdefault("motors", [])
    while True:
        print("\n目前的馬達設定：")
        list_entries(motors, ["port", "gearset"])
        print("選項: [E]編輯  [A]新增  [D]刪除  [Q]返回")
        choice = input("請選擇: ").strip().lower()
        if choice == "q":
            break
        if choice == "a":
            name = input("名稱: ").strip() or f"Motor{len(motors)+1}"
            port_input = prompt_number("Port", 1, is_int=True)
            port = 1 if port_input is None else int(port_input)
            gearset = input("Gearset (例如 pros::v5::MotorGears::blue) [pros::v5::MotorGears::blue]: ").strip()
            if not gearset:
                gearset = "pros::v5::MotorGears::blue"
            comment = input("備註(可留空): ").strip()
            enabled = prompt_bool("是否啟用", True)
            motors.append(
                {
                    "name": name,
                    "port": int(port),
                    "gearset": gearset,
                    "comment": comment,
                    "enabled": enabled,
                }
            )
            continue
        if choice == "d":
            idx = prompt_number("輸入要刪除的索引", None, is_int=True)
            if idx is None or idx < 0 or idx >= len(motors):
                print("索引無效。")
            else:
                motors.pop(int(idx))
            continue
        if choice == "e":
            idx = prompt_number("輸入要編輯的索引", None, is_int=True)
            if idx is None or idx < 0 or idx >= len(motors):
                print("索引無效。")
                continue
            motor = motors[int(idx)]
            name = prompt("名稱", motor["name"])
            if name is not None:
                motor["name"] = name
            port = prompt_number("Port", motor["port"], is_int=True)
            if port is not None:
                motor["port"] = int(port)
            gearset = prompt("Gearset", motor["gearset"])
            if gearset is not None:
                motor["gearset"] = gearset
            comment = prompt("備註", motor.get("comment", ""))
            if comment is not None:
                motor["comment"] = comment
            motor["enabled"] = prompt_bool("是否啟用", motor.get("enabled", True))
            continue
        print("無效的選項。")


def configure_motor_groups(config: Dict[str, Any]) -> None:
    groups = config.setdefault("motor_groups", [])
    while True:
        print("\n目前的馬達群組設定：")
        list_entries(groups, ["ports", "gearset", "units"])
        print("選項: [E]編輯  [A]新增  [D]刪除  [Q]返回")
        choice = input("請選擇: ").strip().lower()
        if choice == "q":
            break
        if choice == "a":
            name = input("名稱: ").strip() or f"Group{len(groups)+1}"
            ports = prompt_list("輸入 Port 列表 (以逗號分隔)", [1, 2, 3])
            gearset = input("Gearset [pros::v5::MotorGears::blue]: ").strip()
            if not gearset:
                gearset = "pros::v5::MotorGears::blue"
            units = input("單位 [pros::v5::MotorUnits::degrees]: ").strip()
            if not units:
                units = "pros::v5::MotorUnits::degrees"
            comment = input("備註(可留空): ").strip()
            enabled = prompt_bool("是否啟用", True)
            groups.append(
                {
                    "name": name,
                    "ports": [int(p) if isinstance(p, (int, float)) and float(p).is_integer() else p for p in ports],
                    "gearset": gearset,
                    "units": units,
                    "comment": comment,
                    "enabled": enabled,
                }
            )
            continue
        if choice == "d":
            idx = prompt_number("輸入要刪除的索引", None, is_int=True)
            if idx is None or idx < 0 or idx >= len(groups):
                print("索引無效。")
            else:
                groups.pop(int(idx))
            continue
        if choice == "e":
            idx = prompt_number("輸入要編輯的索引", None, is_int=True)
            if idx is None or idx < 0 or idx >= len(groups):
                print("索引無效。")
                continue
            group = groups[int(idx)]
            name = prompt("名稱", group["name"])
            if name is not None:
                group["name"] = name
            ports = prompt_list("輸入 Port 列表 (以逗號分隔)", group.get("ports", []))
            if ports is not None:
                new_ports = []
                for p in ports:
                    if isinstance(p, float) and p.is_integer():
                        new_ports.append(int(p))
                    else:
                        new_ports.append(int(p) if isinstance(p, int) else p)
                group["ports"] = new_ports
            gearset = prompt("Gearset", group["gearset"])
            if gearset is not None:
                group["gearset"] = gearset
            units = prompt("單位", group["units"])
            if units is not None:
                group["units"] = units
            comment = prompt("備註", group.get("comment", ""))
            if comment is not None:
                group["comment"] = comment
            group["enabled"] = prompt_bool("是否啟用", group.get("enabled", True))
            continue
        print("無效的選項。")


def configure_drivetrain(config: Dict[str, Any]) -> None:
    drivetrain = config.setdefault("drivetrain", default_config()["drivetrain"])
    print("\n目前的底盤設定：")
    for key, value in drivetrain.items():
        print(f"  {key}: {value}")
    name = prompt("名稱", drivetrain["name"])
    if name is not None:
        drivetrain["name"] = name
    left_group = prompt("左側馬達群組名稱", drivetrain["left_group"])
    if left_group is not None:
        drivetrain["left_group"] = left_group
    right_group = prompt("右側馬達群組名稱", drivetrain["right_group"])
    if right_group is not None:
        drivetrain["right_group"] = right_group
    track_width = prompt_number("輪距 (inch)", drivetrain["track_width"], is_int=False)
    if track_width is not None:
        drivetrain["track_width"] = track_width
    wheel_type = prompt("輪子型號", drivetrain["wheel_type"])
    if wheel_type is not None:
        drivetrain["wheel_type"] = wheel_type
    rpm = prompt_number("RPM", drivetrain["rpm"], is_int=True)
    if rpm is not None:
        drivetrain["rpm"] = int(rpm)
    drift = prompt_number("水平漂移", drivetrain["horizontal_drift"], is_int=False)
    if drift is not None:
        drivetrain["horizontal_drift"] = drift
    comment = prompt("備註", drivetrain.get("comment", ""))
    if comment is not None:
        drivetrain["comment"] = comment
    drivetrain["enabled"] = prompt_bool("是否啟用", drivetrain.get("enabled", True))


def configure_sensors(config: Dict[str, Any]) -> None:
    sensors = config.setdefault("sensors", [])
    while True:
        print("\n目前的感測器設定：")
        list_entries(sensors, ["type", "args"])
        print("選項: [E]編輯  [A]新增  [D]刪除  [Q]返回")
        choice = input("請選擇: ").strip().lower()
        if choice == "q":
            break
        if choice == "a":
            name = input("名稱: ").strip() or f"Sensor{len(sensors)+1}"
            sensor_type = input("型態(例如 pros::Imu): ").strip() or "pros::Imu"
            args = prompt_list("建構子參數 (以逗號分隔)", [])
            comment = input("備註(可留空): ").strip()
            enabled = prompt_bool("是否啟用", True)
            sensors.append(
                {
                    "name": name,
                    "type": sensor_type,
                    "args": args,
                    "comment": comment,
                    "enabled": enabled,
                }
            )
            continue
        if choice == "d":
            idx = prompt_number("輸入要刪除的索引", None, is_int=True)
            if idx is None or idx < 0 or idx >= len(sensors):
                print("索引無效。")
            else:
                sensors.pop(int(idx))
            continue
        if choice == "e":
            idx = prompt_number("輸入要編輯的索引", None, is_int=True)
            if idx is None or idx < 0 or idx >= len(sensors):
                print("索引無效。")
                continue
            sensor = sensors[int(idx)]
            name = prompt("名稱", sensor["name"])
            if name is not None:
                sensor["name"] = name
            sensor_type = prompt("型態", sensor["type"])
            if sensor_type is not None:
                sensor["type"] = sensor_type
            args = prompt_list("建構子參數 (以逗號分隔)", sensor.get("args", []))
            if args is not None:
                sensor["args"] = args
            comment = prompt("備註", sensor.get("comment", ""))
            if comment is not None:
                sensor["comment"] = comment
            sensor["enabled"] = prompt_bool("是否啟用", sensor.get("enabled", True))
            continue
        print("無效的選項。")


def configure_controllers(config: Dict[str, Any]) -> None:
    controllers = config.setdefault("controllers", [])
    while True:
        print("\n目前的手把/控制器設定：")
        list_entries(controllers, ["type", "args"])
        print("選項: [E]編輯  [A]新增  [D]刪除  [Q]返回")
        choice = input("請選擇: ").strip().lower()
        if choice == "q":
            break
        if choice == "a":
            name = input("名稱: ").strip() or f"Controller{len(controllers)+1}"
            controller_type = input("型態(例如 pros::Controller): ").strip() or "pros::Controller"
            args = prompt_list("建構子參數 (以逗號分隔)", [])
            comment = input("備註(可留空): ").strip()
            enabled = prompt_bool("是否啟用", True)
            controllers.append(
                {
                    "name": name,
                    "type": controller_type,
                    "args": args,
                    "comment": comment,
                    "enabled": enabled,
                }
            )
            continue
        if choice == "d":
            idx = prompt_number("輸入要刪除的索引", None, is_int=True)
            if idx is None or idx < 0 or idx >= len(controllers):
                print("索引無效。")
            else:
                controllers.pop(int(idx))
            continue
        if choice == "e":
            idx = prompt_number("輸入要編輯的索引", None, is_int=True)
            if idx is None or idx < 0 or idx >= len(controllers):
                print("索引無效。")
                continue
            controller = controllers[int(idx)]
            name = prompt("名稱", controller["name"])
            if name is not None:
                controller["name"] = name
            controller_type = prompt("型態", controller["type"])
            if controller_type is not None:
                controller["type"] = controller_type
            args = prompt_list("建構子參數 (以逗號分隔)", controller.get("args", []))
            if args is not None:
                controller["args"] = args
            comment = prompt("備註", controller.get("comment", ""))
            if comment is not None:
                controller["comment"] = comment
            controller["enabled"] = prompt_bool("是否啟用", controller.get("enabled", True))
            continue
        print("無效的選項。")


def configure_expo_curve(config: Dict[str, Any]) -> None:
    curve = config.setdefault("expo_drive_curve", default_config()["expo_drive_curve"])
    print("\n目前的 Expo 曲線設定：")
    for key, value in curve.items():
        print(f"  {key}: {value}")
    name = prompt("名稱", curve["name"])
    if name is not None:
        curve["name"] = name
    deadband = prompt_number("死區", curve["deadband"], is_int=True)
    if deadband is not None:
        curve["deadband"] = int(deadband)
    min_output = prompt_number("最小輸出", curve["min_output"], is_int=True)
    if min_output is not None:
        curve["min_output"] = int(min_output)
    curve_value = prompt_number("曲線增益", curve["curve"], is_int=False)
    if curve_value is not None:
        curve["curve"] = curve_value
    comment = prompt("備註", curve.get("comment", ""))
    if comment is not None:
        curve["comment"] = comment


def configure_digital_outputs(config: Dict[str, Any]) -> None:
    digital_outputs = config.setdefault("digital_outputs", [])
    while True:
        print("\n目前的數位輸出設定：")
        list_entries(digital_outputs, ["port"])
        print("選項: [E]編輯  [A]新增  [D]刪除  [Q]返回")
        choice = input("請選擇: ").strip().lower()
        if choice == "q":
            break
        if choice == "a":
            name = input("名稱: ").strip() or f"DigitalOut{len(digital_outputs)+1}"
            port = input("Port (例如 'A'): ").strip() or "'A'"
            comment = input("備註(可留空): ").strip()
            enabled = prompt_bool("是否啟用", True)
            digital_outputs.append(
                {"name": name, "port": port, "comment": comment, "enabled": enabled}
            )
            continue
        if choice == "d":
            idx = prompt_number("輸入要刪除的索引", None, is_int=True)
            if idx is None or idx < 0 or idx >= len(digital_outputs):
                print("索引無效。")
            else:
                digital_outputs.pop(int(idx))
            continue
        if choice == "e":
            idx = prompt_number("輸入要編輯的索引", None, is_int=True)
            if idx is None or idx < 0 or idx >= len(digital_outputs):
                print("索引無效。")
                continue
            dio = digital_outputs[int(idx)]
            name = prompt("名稱", dio["name"])
            if name is not None:
                dio["name"] = name
            port = prompt("Port", dio["port"])
            if port is not None:
                dio["port"] = port
            comment = prompt("備註", dio.get("comment", ""))
            if comment is not None:
                dio["comment"] = comment
            dio["enabled"] = prompt_bool("是否啟用", dio.get("enabled", True))
            continue
        print("無效的選項。")


def configure_tracking_wheels(config: Dict[str, Any]) -> None:
    tracking = config.setdefault("tracking_wheels", [])
    while True:
        print("\n目前的追蹤輪設定：")
        list_entries(tracking, ["encoder", "wheel_enum", "offset"])
        print("選項: [E]編輯  [A]新增  [D]刪除  [Q]返回")
        choice = input("請選擇: ").strip().lower()
        if choice == "q":
            break
        if choice == "a":
            name = input("名稱: ").strip() or f"Tracking{len(tracking)+1}"
            encoder = input("對應的編碼器名稱: ").strip() or "horizontal_encoder"
            wheel_enum = input("輪子型號 (例如 lemlib::Omniwheel::NEW_2): ").strip() or "lemlib::Omniwheel::NEW_2"
            offset_input = prompt_number("偏移量", 0, is_int=False)
            offset = 0 if offset_input is None else offset_input
            comment = input("備註(可留空): ").strip()
            enabled = prompt_bool("是否啟用", True)
            tracking.append(
                {
                    "name": name,
                    "encoder": encoder,
                    "wheel_enum": wheel_enum,
                    "offset": offset,
                    "comment": comment,
                    "enabled": enabled,
                }
            )
            continue
        if choice == "d":
            idx = prompt_number("輸入要刪除的索引", None, is_int=True)
            if idx is None or idx < 0 or idx >= len(tracking):
                print("索引無效。")
            else:
                tracking.pop(int(idx))
            continue
        if choice == "e":
            idx = prompt_number("輸入要編輯的索引", None, is_int=True)
            if idx is None or idx < 0 or idx >= len(tracking):
                print("索引無效。")
                continue
            wheel = tracking[int(idx)]
            name = prompt("名稱", wheel["name"])
            if name is not None:
                wheel["name"] = name
            encoder = prompt("對應的編碼器名稱", wheel["encoder"])
            if encoder is not None:
                wheel["encoder"] = encoder
            wheel_enum = prompt("輪子型號", wheel["wheel_enum"])
            if wheel_enum is not None:
                wheel["wheel_enum"] = wheel_enum
            offset = prompt_number("偏移量", wheel["offset"], is_int=False)
            if offset is not None:
                wheel["offset"] = offset
            comment = prompt("備註", wheel.get("comment", ""))
            if comment is not None:
                wheel["comment"] = comment
            wheel["enabled"] = prompt_bool("是否啟用", wheel.get("enabled", True))
            continue
        print("無效的選項。")


def configure_odom_sensors(config: Dict[str, Any]) -> None:
    odom = config.setdefault("odom_sensors", default_config()["odom_sensors"])
    print("\n目前的 Odom 感測器設定：")
    for key, value in odom.items():
        print(f"  {key}: {value}")
    name = prompt("名稱", odom["name"])
    if name is not None:
        odom["name"] = name
    for field in ["vertical1", "vertical2", "horizontal1", "horizontal2", "inertial"]:
        value = prompt(field, odom.get(field))
        if value is not None:
            odom[field] = value if value else None


def configure_controller_settings(config: Dict[str, Any]) -> None:
    settings = config.setdefault("controller_settings", default_config()["controller_settings"])
    for key in ("lateral", "angular"):
        if key not in settings:
            continue
        cfg = settings[key]
        print(f"\n目前的 {key} PID 設定：")
        for field, value in cfg.items():
            print(f"  {field}: {value}")
        name = prompt("名稱", cfg["name"])
        if name is not None:
            cfg["name"] = name
        value = prompt_number("kP", cfg["kP"], is_int=False)
        if value is not None:
            cfg["kP"] = value
        value = prompt_number("kI", cfg["kI"], is_int=False)
        if value is not None:
            cfg["kI"] = value
        value = prompt_number("kD", cfg["kD"], is_int=False)
        if value is not None:
            cfg["kD"] = value
        value = prompt_number("Anti windup", cfg["anti_windup"], is_int=False)
        if value is not None:
            cfg["anti_windup"] = value
        value = prompt_number("小誤差範圍", cfg["small_error"], is_int=False)
        if value is not None:
            cfg["small_error"] = value
        value = prompt_number("小誤差逾時(ms)", cfg["small_timeout"], is_int=True)
        if value is not None:
            cfg["small_timeout"] = int(value)
        value = prompt_number("大誤差範圍", cfg["large_error"], is_int=False)
        if value is not None:
            cfg["large_error"] = value
        value = prompt_number("大誤差逾時(ms)", cfg["large_timeout"], is_int=True)
        if value is not None:
            cfg["large_timeout"] = int(value)
        value = prompt_number("最大加速度", cfg["slew"], is_int=False)
        if value is not None:
            cfg["slew"] = value


def configure_chassis(config: Dict[str, Any]) -> None:
    chassis = config.setdefault("chassis", default_config()["chassis"])
    print("\n目前的底盤物件設定：")
    for key, value in chassis.items():
        print(f"  {key}: {value}")
    for field in ["name", "drivetrain", "lateral", "angular", "sensors"]:
        value = prompt(field, chassis[field])
        if value is not None:
            chassis[field] = value


def configure_pid(config: Dict[str, Any]) -> None:
    pid_list = config.setdefault("pid", [])
    while True:
        print("\n目前的 PID 設定：")
        list_entries(pid_list, ["kP", "kI", "kD"])
        print("選項: [E]編輯  [A]新增  [D]刪除  [Q]返回")
        choice = input("請選擇: ").strip().lower()
        if choice == "q":
            break
        if choice == "a":
            name = input("名稱: ").strip() or f"pid{len(pid_list)+1}"
            kP_input = prompt_number("kP", 0.0, is_int=False)
            kP = 0.0 if kP_input is None else kP_input
            kI_input = prompt_number("kI", 0.0, is_int=False)
            kI = 0.0 if kI_input is None else kI_input
            kD_input = prompt_number("kD", 0.0, is_int=False)
            kD = 0.0 if kD_input is None else kD_input
            comment = input("備註(可留空): ").strip()
            enabled = prompt_bool("是否啟用", True)
            pid_list.append(
                {
                    "name": name,
                    "kP": kP,
                    "kI": kI,
                    "kD": kD,
                    "comment": comment,
                    "enabled": enabled,
                }
            )
            continue
        if choice == "d":
            idx = prompt_number("輸入要刪除的索引", None, is_int=True)
            if idx is None or idx < 0 or idx >= len(pid_list):
                print("索引無效。")
            else:
                pid_list.pop(int(idx))
            continue
        if choice == "e":
            idx = prompt_number("輸入要編輯的索引", None, is_int=True)
            if idx is None or idx < 0 or idx >= len(pid_list):
                print("索引無效。")
                continue
            pid = pid_list[int(idx)]
            name = prompt("名稱", pid["name"])
            if name is not None:
                pid["name"] = name
            kP = prompt_number("kP", pid["kP"], is_int=False)
            if kP is not None:
                pid["kP"] = kP
            kI = prompt_number("kI", pid["kI"], is_int=False)
            if kI is not None:
                pid["kI"] = kI
            kD = prompt_number("kD", pid["kD"], is_int=False)
            if kD is not None:
                pid["kD"] = kD
            comment = prompt("備註", pid.get("comment", ""))
            if comment is not None:
                pid["comment"] = comment
            pid["enabled"] = prompt_bool("是否啟用", pid.get("enabled", True))
            continue
        print("無效的選項。")


def configure_xdrive(config: Dict[str, Any]) -> None:
    x_drive = config.setdefault("x_drive", default_config()["x_drive"])
    print("\n目前的 X-Drive 設定：")
    for key, value in x_drive.items():
        print(f"  {key}: {value}")
    name = prompt("名稱", x_drive["name"])
    if name is not None:
        x_drive["name"] = name
    motors_input = prompt_list("馬達名稱 (以逗號分隔)", x_drive.get("motors", []))
    if motors_input is not None:
        x_drive["motors"] = [str(m).strip() for m in motors_input]
    length = prompt_number("長度", x_drive["length"], is_int=False)
    if length is not None:
        x_drive["length"] = length
    width = prompt_number("寬度", x_drive["width"], is_int=False)
    if width is not None:
        x_drive["width"] = width
    wheel_diameter = prompt_number("輪徑", x_drive["wheel_diameter"], is_int=False)
    if wheel_diameter is not None:
        x_drive["wheel_diameter"] = wheel_diameter
    drift = prompt_number("漂移", x_drive["drift"], is_int=False)
    if drift is not None:
        x_drive["drift"] = drift
    sensors_name = prompt("感測器物件名稱", x_drive["sensors"])
    if sensors_name is not None:
        x_drive["sensors"] = sensors_name
    comment = prompt("備註", x_drive.get("comment", ""))
    if comment is not None:
        x_drive["comment"] = comment


def main() -> None:
    config = load_config()
    while True:
        print("""
======= Robot Configurator =======
1. 設定馬達
2. 設定馬達群組
3. 設定底盤(drivetrain)
4. 設定感測器
5. 設定手把/控制器
6. 設定 Expo 曲線
7. 設定數位輸出
8. 設定追蹤輪
9. 設定 Odom 感測器
10. 設定 PID 控制器參數 (lateral/angular)
11. 設定底盤物件 (Chassis)
12. 設定 PID 物件列表
13. 設定 X-Drive
14. 儲存並產生 robot.cpp/robot.hpp
0. 離開 (不儲存)
=================================
""")
        choice = input("請選擇功能: ").strip()
        if choice == "1":
            configure_motors(config)
        elif choice == "2":
            configure_motor_groups(config)
        elif choice == "3":
            configure_drivetrain(config)
        elif choice == "4":
            configure_sensors(config)
        elif choice == "5":
            configure_controllers(config)
        elif choice == "6":
            configure_expo_curve(config)
        elif choice == "7":
            configure_digital_outputs(config)
        elif choice == "8":
            configure_tracking_wheels(config)
        elif choice == "9":
            configure_odom_sensors(config)
        elif choice == "10":
            configure_controller_settings(config)
        elif choice == "11":
            configure_chassis(config)
        elif choice == "12":
            configure_pid(config)
        elif choice == "13":
            configure_xdrive(config)
        elif choice == "14":
            save_config(config)
            write_robot_files(config)
            print("設定已儲存並更新 robot.cpp/robot.hpp。")
        elif choice == "0":
            print("離開且不儲存變更。")
            break
        else:
            print("未知的選項，請重新輸入。")


if __name__ == "__main__":
    main()
