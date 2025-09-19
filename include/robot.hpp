#ifndef ROBOT_HPP
#define ROBOT_HPP

#include "main.h"
#include "lemlib/chassis/XDrivetrain.hpp"
#include "lemlib/chassis/chassis.hpp"
#include "lemlib/chassis/odom.hpp"
#include "lemlib/chassis/trackingWheel.hpp"

// 馬達宣告
extern pros::Motor LeftFront; // 左前方馬達
extern pros::Motor LeftBack; // 左後方馬達
extern pros::Motor RightFront; // 右前方馬達
extern pros::Motor RightBack; // 右後方馬達
extern pros::Motor FrontIntake; // 前方 intake 馬達

// 馬達群組宣告
extern pros::MotorGroup LeftGroup; // 左側馬達組設定
extern pros::MotorGroup RightGroup; // 右側馬達組設定
extern pros::MotorGroup BackIntake; // 後方 intake 馬達群組

// 底盤設定宣告
extern lemlib::Drivetrain drivetrain;

// 感測器宣告
extern pros::Optical Op;
extern pros::Gps GPS;
extern pros::Distance FDistance;
extern pros::Imu imu;
extern pros::Rotation horizontal_encoder;
extern pros::Rotation left_vertical_encoder;
extern pros::Rotation right_vertical_encoder;

// 控制器宣告
extern pros::Controller Player1;
extern pros::Controller Player2;

extern lemlib::ExpoDriveCurve expoCurve;

// 數位輸出宣告
extern pros::ADIDigitalOut Clamp;
extern pros::ADIDigitalOut Arm1stg;
extern pros::ADIDigitalOut Arm2stg;
extern pros::ADIDigitalOut Arm2stgBack;
extern pros::ADIDigitalOut Wing;
extern pros::ADIDigitalOut Climb;
extern pros::ADIDigitalOut IntakeUp;

// 追蹤輪宣告
extern lemlib::TrackingWheel horizontal_tracking_wheel;
extern lemlib::TrackingWheel left_vertical_tracking_wheel;

// 里程感測器宣告
extern lemlib::OdomSensors sensors;

// PID 控制器設定宣告
extern lemlib::ControllerSettings lateral_controller;
extern lemlib::ControllerSettings angular_controller;

// 底盤物件宣告
extern lemlib::Chassis chassis;

// PID 控制器宣告
extern lemlib::PID distancePID;
extern lemlib::PID anglePID;

// X-Drive 底盤宣告
extern XDrivetrain XDrive;

#endif
