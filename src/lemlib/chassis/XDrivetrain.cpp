#include "lemlib/chassis/XDrivetrain.hpp"
#include "robot.hpp"
#include "lemlib/pid.hpp" // 假設你有這個PID類別
#ifndef M_PI
#define M_PI 3.14159265358979323846
#endif
// 建構子實作
XDrivetrain::XDrivetrain(pros::Motor* frontLeft, pros::Motor* frontRight, pros::Motor* backLeft, pros::Motor* backRight,
                         float trackWidth, float wheelDiameter, float rpm, float horizontalDrift,
                         lemlib::OdomSensors* sensors)
    : frontLeft(frontLeft),
      frontRight(frontRight),
      backLeft(backLeft),
      backRight(backRight),
      trackWidth(trackWidth),
      wheelDiameter(wheelDiameter),
      rpm(rpm),
      horizontalDrift(horizontalDrift),
      sensors(sensors) {}

// 設定四顆馬達的力量（電壓）
void XDrivetrain::setMotorPowers(int fl, int fr, int bl, int br) {
    if (frontLeft) frontLeft->move(fl);
    if (frontRight) frontRight->move(fr);
    if (backLeft) backLeft->move(bl);
    if (backRight) backRight->move(br);
}

// 移動 X-Drive 底盤
void XDrivetrain::move(float distance, float moveDirectionDeg, float finalHeadingDeg) {
    // 將角度轉為弧度
    float moveDirectionRad = moveDirectionDeg * M_PI / 180.0f;
    float finalHeadingRad = finalHeadingDeg * M_PI / 180.0f;

    // 計算目標X, Y位移
    float targetX = distance * cos(moveDirectionRad);
    float targetY = distance * sin(moveDirectionRad);

    // 這裡你可以呼叫你現有的PID控制或移動邏輯
    // 例如: moveTo(targetX, targetY, finalHeadingRad);
    // 或者你可以直接實作移動控制

    // 範例: 只設定馬達功率，實際應用請用PID控制
    // 這裡僅為佔位
    setMotorPowers(0, 0, 0, 0);
}

void XDrivetrain::opcontrol(pros::Controller& controller, lemlib::ExpoDriveCurve& expoCurve, double rotateWeight) {
    while (true) {
        // 取得IMU角度（場地方向，單位：弧度）
        double robotHeadingRad = (sensors && sensors->imu) ? sensors->imu->get_rotation() * M_PI / 180.0 : 0;

        // 取得搖桿輸入
        int rawForward = controller.get_analog(pros::E_CONTROLLER_ANALOG_LEFT_Y);
        int rawStrafe = controller.get_analog(pros::E_CONTROLLER_ANALOG_LEFT_X);
        int rawRotate = controller.get_analog(pros::E_CONTROLLER_ANALOG_RIGHT_X);

        double forward = expoCurve.curve(rawForward);
        double strafe = expoCurve.curve(rawStrafe);
        double rotate = expoCurve.curve(rawRotate);

        // 依照你原本的 X-Drive 場地導向分配公式
        double fl = forward * cos(M_PI / 4 + robotHeadingRad) / 0.7 + rotate * rotateWeight +
                    strafe * sin(M_PI / 4 + robotHeadingRad) / 0.7;
        double bl = forward * cos(-M_PI / 4 + robotHeadingRad) / 0.7 + rotate * rotateWeight +
                    strafe * sin(-M_PI / 4 + robotHeadingRad) / 0.7;
        double fr = forward * cos(-M_PI / 4 + robotHeadingRad) / 0.7 - rotate * rotateWeight +
                    strafe * sin(-M_PI / 4 + robotHeadingRad) / 0.7;
        double br = forward * cos(M_PI / 4 + robotHeadingRad) / 0.7 - rotate * rotateWeight +
                    strafe * sin(M_PI / 4 + robotHeadingRad) / 0.7;

        // 等比例縮放馬達輸出，確保最大值不超過127
        double maxVal = std::max({std::abs(fl), std::abs(fr), std::abs(bl), std::abs(br)});
        if (maxVal > 127.0) {
            double scale = 127.0 / maxVal;
            fl *= scale;
            fr *= scale;
            bl *= scale;
            br *= scale;
        }

        setMotorPowers(static_cast<int>(fl), static_cast<int>(fr), static_cast<int>(bl), static_cast<int>(br));

        pros::delay(20);
    }
}