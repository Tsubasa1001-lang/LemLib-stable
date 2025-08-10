#pragma once

#include "pros/rtos.hpp"
#include "pros/imu.hpp"
#include "lemlib/asset.hpp"
#include "lemlib/chassis/trackingWheel.hpp"
#include "lemlib/pose.hpp"
#include "lemlib/pid.hpp"
#include "lemlib/exitcondition.hpp"
#include "lemlib/driveCurve.hpp"
#include <cmath>
#include "chassis.hpp"
#include <algorithm>

/**
 * @brief class containing constants for an X-Drive drivetrain
 */
class XDrivetrain {
    public:
        /**
         * @brief XDrivetrain constructor
         *
         * @param frontLeft pointer to the front left motors
         * @param frontRight pointer to the front right motors
         * @param backLeft pointer to the back left motors
         * @param backRight pointer to the back right motors
         * @param trackWidth 機器人左右輪中心距離（英吋）
         * @param wheelDiameter 輪子直徑（英吋）
         * @param rpm 輪子轉速
         * @param horizontalDrift X-Drive 橫向補償參數
         * @param imu 指向 IMU 的指標，用於姿態感測
         *
         * @b Example
         * @code {.cpp}
         * pros::Motor fl(1), fr(2), bl(3), br(4);
         * pros::MotorGroup frontLeft({fl});
         * pros::MotorGroup frontRight({fr});
         * pros::MotorGroup backLeft({bl});
         * pros::MotorGroup backRight({br});
         * lemlib::XDrivetrain xdrivetrain(&frontLeft, &frontRight, &backLeft, &backRight, 10, 4, 360, 2);
         * @endcode
         */

        XDrivetrain(pros::Motor* frontLeft, pros::Motor* frontRight, pros::Motor* backLeft,
                    pros::Motor* backRight, float trackWidth, float wheelDiameter, float rpm,
                    float horizontalDrift, lemlib::OdomSensors* sensors);

        /**
         * @brief 設定四顆馬達的力量（電壓）
         * @param fl 前左馬達力量，範圍 -127 ~ 127
         * @param fr 前右馬達力量，範圍 -127 ~ 127
         * @param bl 後左馬達力量，範圍 -127 ~ 127
         * @param br 後右馬達力量，範圍 -127 ~ 127
         */
        void setMotorPowers(int fl, int fr, int bl, int br);
        /**
         * @brief 控制 X-Drive 底盤移動到指定座標並朝向特定角度
         * @param targetX 目標 X 座標（公分）
         * @param targetY 目標 Y 座標（公分）
         * @param final_heading_deg 移動結束時的朝向角度（度，0 為正前方）
         */
        void move(float targetX, float targetY, float final_heading_deg);
        /**
         * @brief 手動控制模式，讀取控制器與IMU進行場地導向X-Drive控制
         * @param controller 控制器物件參考
         */
        void opcontrol(pros::Controller& controller, lemlib::ExpoDriveCurve& expoCurve,double rotateWeight );

        pros::Motor* frontLeft;
        pros::Motor* frontRight;
        pros::Motor* backLeft;
        pros::Motor* backRight;
        float trackWidth;
        float wheelDiameter;
        float rpm;
        float horizontalDrift;
        lemlib::OdomSensors* sensors;
};
