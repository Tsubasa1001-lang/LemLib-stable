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
// 底盤配置
lemlib::Drivetrain drivetrain(&LeftGroup, // left motor group
                              &RightGroup, // right motor group
                              10, // 10 inch track width
                              lemlib::Omniwheel::NEW_275, // using new 275" omnis
                              480, // drivetrain rpm is 480
                              2 // horizontal drift is 2 (for now)
);

// 感測器初始化
pros::Optical Op(11);
// pros::Imu Gy(12);
pros::Gps GPS(20, -100, 70);
pros::Distance FDistance(21);
// pros::Distance BDistance(13);

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

// imu
pros::Imu imu(16);
// horizontal tracking wheel encoder
pros::Rotation horizontal_encoder(18);
// vertical tracking wheel encoder
pros::Rotation left_vertical_encoder(17);
pros::Rotation right_vertical_encoder(-19);
// pros::adi::Encoder vertical_encoder('C', 'D', true);
//  horizontal tracking wheel
lemlib::TrackingWheel horizontal_tracking_wheel(&horizontal_encoder, lemlib::Omniwheel::NEW_2, 0);
// vertical tracking wheel
lemlib::TrackingWheel left_vertical_tracking_wheel(&left_vertical_encoder, lemlib::Omniwheel::NEW_2, -2.5);

// odometry settings
lemlib::OdomSensors sensors(&left_vertical_tracking_wheel, // vertical tracking wheel 1, set to null
                            nullptr, // vertical tracking wheel 2, set to nullptr as we are using IMEs
                            &horizontal_tracking_wheel, // horizontal tracking wheel 1
                            nullptr, // horizontal tracking wheel 2, set to nullptr as we don't have a second one
                            &imu // inertial sensor
);

// lateral PID controller
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

// angular PID controller
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

// create the chassis
lemlib::Chassis chassis(drivetrain, // drivetrain settings
                        lateral_controller, // lateral PID settings
                        angular_controller, // angular PID settings
                        sensors // odometry sensors
);

// PID 控制器初始化
lemlib::PID distancePID(0.5, 0, 0); // 請根據實際需求調整參數
lemlib::PID anglePID(2.0, 0, 0); // 請根據實際需求調整參數
XDrivetrain XDrive(&LeftFront, &RightFront, &LeftBack, &RightBack, 10, 4, 360, 2, &sensors); // X-Drive 底盤實例