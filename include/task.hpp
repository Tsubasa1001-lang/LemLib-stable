#ifndef TASKS_HPP
#define TASKS_HPP

#include "main.h"

// 任務函數宣告
void chassis_control(void* param); // 底盤控制
void XDrive_control(void* param);//XDrive 底盤控制
void intake_control(void* param);  // Intake 控制
void conveyor_control(void* param); // Conveyor 控制
void display_position_task(); // 顯示位置資訊的任務
#endif
