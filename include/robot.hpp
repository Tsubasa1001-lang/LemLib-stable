#ifndef ROBOT_HPP
#define ROBOT_HPP

#include "main.h"
#include "lemlib/chassis/XDrivetrain.hpp"
#include "lemLib/chassis/chassis.hpp"
// 馬達宣告
extern pros::Motor Intake;
extern pros::Motor Conveyor;
extern pros::Motor LeftFront; // 左前方馬達
extern pros::Motor LeftBack; // 左後方馬達
extern pros::Motor RightFront; // 右前方馬達
extern pros::Motor RightBack; // 右後方馬達
extern pros::Motor FrontIntake; // 前方 intake 馬達
extern pros::Motor BackLeftIntake; // 後方中間 intake 馬達
extern pros::Motor BackMiddleIntake; // 後方中間 intake 馬達
extern pros::Motor BackRightIntake; // 後方右邊 intake 馬達

// 馬達群組
extern pros::MotorGroup LeftGroup;
extern pros::MotorGroup RightGroup;
extern pros::MotorGroup BackIntake;
// 底盤配置
extern lemlib::Chassis chassis;
extern XDrivetrain XDrive;
extern lemlib::ExpoDriveCurve expoCurve;
// PID 控制器初始化
extern lemlib::PID distancePID;
extern lemlib::PID anglePID;
// 感測器宣告
extern pros::Optical Op;
extern pros::Imu imu;
extern pros::Gps GPS;
extern pros::Distance FDistance;
extern pros::Distance BDistance;

// 控制器宣告
extern pros::Controller Player1;
extern pros::Controller Player2;

// 數位輸出宣告
extern pros::ADIDigitalOut Clamp;
extern pros::ADIDigitalOut Arm1stg;
extern pros::ADIDigitalOut Arm2stg;
extern pros::ADIDigitalOut Arm2stgBack;
extern pros::ADIDigitalOut Wing;
extern pros::ADIDigitalOut Climb;
extern pros::ADIDigitalOut IntakeUp;

#endif
