#include "robot.hpp"

// 馬達初始化
pros::Motor LeftFront(-1, pros::v5::MotorGears::blue); // 左前方馬達
pros::Motor LeftBack(-3, pros::v5::MotorGears::blue); // 左後方馬達
pros::Motor RightFront(2, pros::v5::MotorGears::blue); // 右前方馬達
pros::Motor RightBack(4, pros::v5::MotorGears::blue); // 右後方馬達
pros::Motor FrontIntake(-15, pros::v5::MotorGears::blue); // 前方 intake 馬達

// 馬達群組初始化
pros::MotorGroup LeftGroup({-5, 6, -7}, pros::v5::MotorGears::blue, pros::v5::MotorUnits::degrees); // 左側馬達組設定
pros::MotorGroup RightGroup({8, -9, 10}, pros::v5::MotorGears::blue, pros::v5::MotorUnits::degrees); // 右側馬達組設定
pros::MotorGroup BackIntake({12, -13, -14}, pros::v5::MotorGears::blue, pros::v5::MotorUnits::degrees); // 後方 intake 馬達群組

// 底盤配置
lemlib::Drivetrain drivetrain(&LeftGroup, // left motor group
                              &RightGroup, // right motor group
                              10, // track width
                              lemlib::Omniwheel::NEW_275, // wheel type
                              480, // drivetrain rpm
                              2 // horizontal drift
);

// 感測器初始化
pros::Optical Op(11);
pros::Gps GPS(20, -100, 70);
pros::Distance FDistance(21);
pros::Imu imu(16);
pros::Rotation horizontal_encoder(18);
pros::Rotation left_vertical_encoder(17);
pros::Rotation right_vertical_encoder(-19);

// 控制器初始化
pros::Controller Player1(pros::E_CONTROLLER_MASTER);
pros::Controller Player2(pros::E_CONTROLLER_PARTNER);

// 控制搖桿輸入的 Expo 曲線（死區10，最小輸出10，曲線增益1.02，可依手感調整）
lemlib::ExpoDriveCurve expoCurve(10, 10, 1.02);

// 數位輸出初始化
pros::ADIDigitalOut Clamp('A');
pros::ADIDigitalOut Arm1stg('B');
pros::ADIDigitalOut Arm2stg('C');
pros::ADIDigitalOut Arm2stgBack('D');
pros::ADIDigitalOut Wing('E');
pros::ADIDigitalOut Climb('F');
pros::ADIDigitalOut IntakeUp('G');

// 追蹤輪設定
lemlib::TrackingWheel horizontal_tracking_wheel(&horizontal_encoder, lemlib::Omniwheel::NEW_2, 0); // horizontal tracking wheel
lemlib::TrackingWheel left_vertical_tracking_wheel(&left_vertical_encoder, lemlib::Omniwheel::NEW_2, -2.5); // vertical tracking wheel

// odometry settings
lemlib::OdomSensors sensors(&left_vertical_tracking_wheel, // vertical tracking wheel 1
                            nullptr, // vertical tracking wheel 2
                            &horizontal_tracking_wheel, // horizontal tracking wheel 1
                            nullptr, // horizontal tracking wheel 2
                            &imu // inertial sensor
);

// PID 控制器設定
lemlib::ControllerSettings lateral_controller(20, // proportional gain (kP)
                                              0, // integral gain (kI)
                                              3, // derivative gain (kD)
                                              3, // anti windup
                                              1, // small error range, in inches
                                              100, // small error range timeout, in milliseconds
                                              3, // large error range, in inches
                                              500, // large error range timeout, in milliseconds
                                              20 // maximum acceleration (slew)
);

lemlib::ControllerSettings angular_controller(8, // proportional gain (kP)
                                              0, // integral gain (kI)
                                              10, // derivative gain (kD)
                                              3, // anti windup
                                              1, // small error range, in degrees
                                              100, // small error range timeout, in milliseconds
                                              3, // large error range, in degrees
                                              500, // large error range timeout, in milliseconds
                                              0 // maximum acceleration (slew)
);

// 底盤建立
lemlib::Chassis chassis(drivetrain, // drivetrain settings
                        lateral_controller, // lateral PID settings
                        angular_controller, // angular PID settings
                        sensors // odometry sensors
);

// PID 控制器初始化
lemlib::PID distancePID(0.5, 0, 0); // 請根據實際需求調整參數
lemlib::PID anglePID(2.0, 0, 0); // 請根據實際需求調整參數

XDrivetrain XDrive(&LeftFront, &RightFront, &LeftBack, &RightBack, 10, 4, 360, 2, &sensors); // X-Drive 底盤實例
