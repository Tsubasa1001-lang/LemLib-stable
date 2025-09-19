#include "robot.hpp"

// 馬達初始化
pros::Motor LeftFront(-1, pros::v5::MotorGears::blue); // 左前方馬達
pros::Motor LeftBack(-3, pros::v5::MotorGears::blue); // 左後方馬達
pros::Motor RightFront(2, pros::v5::MotorGears::blue); // 右前方馬達
pros::Motor RightBack(4, pros::v5::MotorGears::blue); // 右後方馬達
pros::Motor FrontIntake(-15, pros::v5::MotorGears::blue); // 前方 intake 馬達
// pros::Motor BackLeftIntake(12, pros::v5::MotorGears::blue); // 後方中間 intake 馬達
// pros::Motor BackMiddleIntake(-13, pros::v5::MotorGears::blue); // 後方中間 intake 馬達
// pros::Motor BackRightIntake(-14, pros::v5::MotorGears::blue); // 後方右邊 intake 馬達
pros::Motor Conveyor(5, pros::v5::MotorGears::blue);

// 馬達群組初始化
pros::MotorGroup LeftGroup({-5, 6, -7}, pros::v5::MotorGears::blue, pros::v5::MotorUnits::degrees); // 左側馬達組設定
pros::MotorGroup RightGroup({8, -9, 10}, pros::v5::MotorGears::blue, pros::v5::MotorUnits::degrees); // 右側馬達組設定
pros::MotorGroup BackIntake({12, -13, -14}, pros::v5::MotorGears::blue,
                            pros::v5::MotorUnits::degrees); // 左前方馬達群組
// 控制器初始化
pros::Controller Player1(pros::E_CONTROLLER_MASTER);
pros::Controller Player2(pros::E_CONTROLLER_PARTNER);
// 控制搖桿輸入的 Expo 曲線（死區10，最小輸出10，曲線增益1.05，可依手感調整）
lemlib::ExpoDriveCurve expoCurve(10, 10, 1.02);

// 數位輸出初始化
pros::ADIDigitalOut Clamp('A');
pros::ADIDigitalOut Arm1stg('B');
pros::ADIDigitalOut Arm2stg('C');
pros::ADIDigitalOut Arm2stgBack('D');
pros::ADIDigitalOut Wing('E');
pros::ADIDigitalOut Climb('F');
pros::ADIDigitalOut IntakeUp('G');

