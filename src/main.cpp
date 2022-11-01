// Code By: Luan Gabriel Vidal
// Studant IFMG 
// Project VSS

//                       !!!!!!  :!!!!!!: !!!!!!!                       
//                       !!!!!!! :!!!!!!: !!!!!!!                       
//                       .......  :...::                                
//                       !!!!!!! :!!!!!!:                               
//                       !!!!!!! :!!!!!!:                               
//                       !!!!!!! .!!!!!!. !!!!!!!                       
//                       !!!!!!! :!!!!!!: !!!!!!!                       
//                       !!!!!!! :!!!!!!: !!!!!!!                       
//                       !!!!!!! :!!!!!!:                               
//                       !!!!!!! :!!!!!!:                               
//                       ::::::: .::::::.   

#define ROSSERIAL_ARDUINO_TCP

#include <WiFi.h>
#include <Arduino.h> 
#include <ros.h>
#include <geometry_msgs/Twist.h>

// Ultilizar o ssid e password do wifi 
const char* ssid = "==============";
const char* password = "===========";

float v = 0.0;
float w = 0.0;

// callback da mensagem 

void callback(const geometry_msgs::Twist &msg){
  
  v = msg.linear.x;
  w = msg.angular.z;
  
}

// Defina o endereço IP do servidor do soquete (rosserial)
IPAddress server(192,168,0,108);

// Defina a porta do servidor do soquete (rosserial)
const uint16_t serverPort = 11411;

ros::NodeHandle nh;

// habilitando a mensagem a ser enviada
geometry_msgs::Twist msg;

// start da msg
ros::Publisher pub("esp32/cmd_vel", &msg);
ros::Subscriber<geometry_msgs::Twist> sub("/robot0/cmd_vel/", &callback);

void setup(){
  // Usando o monitor serial do ESP
  Serial.begin(9600);
  Serial.println();
  Serial.print("Conectando em ");
  Serial.println(ssid);

  // conecta o ESP ao wifi
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("");
  Serial.println("WiFi conectado");
  Serial.println("Endereço IP: ");
  Serial.println(WiFi.localIP());

  // Definindo a conexão com o servidor do soquete (rosserial)
  nh.getHardware() -> setConnection(server, serverPort);
  nh.initNode();

  // Outra maneira de conseguir um IP
  Serial.print("IP = ");
  Serial.println(nh.getHardware() -> getLocalIP());

  // star da msg
  nh.advertise(pub);
  nh.subscribe(sub);

}

void loop(){

  if (nh.connected()) {

    Serial.println("Conectado");

    // envio da mensagem
    pub.publish( &msg );
    Serial.print("ok");
    Serial.println(v);
    Serial.println(w);
  } else {
    Serial.println("Não conectado");
  }

  nh.spinOnce();

  // Loop para perfomace
  delay(10);
}
