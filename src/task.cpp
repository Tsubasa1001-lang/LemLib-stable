#include "task.hpp"
#include "robot.hpp" // 引入電子元件宣告

// 底盤控制 Task
void chassis_control(void* param) {
    while (true) {
        int dir = Player1.get_analog(pros::E_CONTROLLER_ANALOG_LEFT_Y);   // 前後控制
        int turn = Player1.get_analog(pros::E_CONTROLLER_ANALOG_RIGHT_X); // 左右轉向

        LeftGroup.move(dir + turn);  // 左側馬達組
        RightGroup.move(dir - turn); // 右側馬達組

        pros::delay(20); // 延遲避免過度消耗資源
    }
}
// XDrive 控制 Task
void XDrive_control(void* param) {
    XDrive.opcontrol(Player1, expoCurve, 0.7); // 使用 XDrive 底盤控制
    }

// Intake 控制 Task
void intake_control(void* param) {
    while (true) {
        if (Player1.get_digital(pros::E_CONTROLLER_DIGITAL_R1)) {
            FrontIntake.move(127); // 向內吸入
            BackIntake.move(127); // 後方 intake 馬達也向內吸入
        } else if (Player1.get_digital(pros::E_CONTROLLER_DIGITAL_R2)) {
            FrontIntake.move(-127); // 向外推出
            BackIntake.move(-127); // 後方 intake 馬達也向外推出
        } else {
            FrontIntake.move(0); // 停止
            BackIntake.move(0); // 後方 intake 馬達也停止
        }
        pros::delay(20);
    }
}

// Conveyor 控制 Task
void conveyor_control(void* param) {
    while (true) {
        if (Player1.get_digital(pros::E_CONTROLLER_DIGITAL_R1)) {
            Conveyor.move(127); // 正向運轉
        } else if (Player1.get_digital(pros::E_CONTROLLER_DIGITAL_R2)) {
            Conveyor.move(-127); // 反向運轉
        } else {
            Conveyor.move(0); // 停止
        }
        pros::delay(20);
    }
}

void display_position_task() {
    while (true) {
        // 獲取機器人的當前位置資訊
        lemlib::Pose currentPose = chassis.getPose(); // 假設 chassis 有 getPose() 方法
        float x = currentPose.x;
        float y = currentPose.y;
        float theta = currentPose.theta;

        // 在 LCD 上顯示位置資訊
        pros::lcd::print(0, "X: %.2f Y: %.2f", x, y);
        pros::lcd::print(1, "Theta: %.2f", theta);

        pros::delay(100); // 每 100 毫秒更新一次
    }
}