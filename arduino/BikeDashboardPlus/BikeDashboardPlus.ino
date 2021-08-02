/*
MIT License

Copyright (c) 2021 jonyboi396825

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
*/

#define LED1 2
#define LED2 3
#define BUTTON1 4
#define BUTTON2 5
#define INTERVAL 500

#define ROWS 2
#define COLS 10

#include <ArduinoJson.h>
#include <Wire.h>

typedef unsigned long long ull;

// LED display
const int row[ROWS] = {6, 7};
const int col[COLS] = {8, 9, 10, 11, 12, 13, A2, A3, A4, A5};
bool disp[ROWS][COLS];

// serial communication with RPi
StaticJsonDocument<128> send_doc;
StaticJsonDocument<256> receive_doc;

// Cfg
uint8_t led, dtm, bc1, bc2, bc3;

// states of buttons (cur state, prev state)
bool s1, s2, ps1, ps2; 
uint8_t unit; // 0 = mph, 1 = km/h, 2 = m/s

// blinking the LED
ull blinkPrevMillis = 0;
bool states[] = {0, 0, 0, 0};

void setup(void){
    Serial.begin(115200);

    // get configurations from RPi
    send_doc["REQ"] = 0;
    send_doc["BUTTON1"] = false;
    send_doc["BUTTON2"] = false;

    String buf;
    serializeJson(send_doc, buf);
    Serial.println(buf);
    
    while (not Serial.available());
    if (Serial.available()){
        buf = Serial.readStringUntil('\n'); 
    }
    deserializeJson(receive_doc, buf);

    if (receive_doc.containsKey("LED") and receive_doc.containsKey("DTM")){
        led = receive_doc["LED"];
        dtm = receive_doc["DTM"];
        unit = receive_doc["UNT"];
    }

    // pins 
    pinMode(LED1, OUTPUT);
    pinMode(LED2, OUTPUT);
    
    pinMode(BUTTON1, INPUT);
    pinMode(BUTTON2, INPUT);

    for (auto i: row) pinMode(i, OUTPUT);
    for (auto i: col){
        pinMode(i, OUTPUT);
        digitalWrite(i, HIGH);
    }
}

void loop(void){
    send_doc["REQ"] = 1;

    // get states 
    s1 = digitalRead(BUTTON1);
    s2 = digitalRead(BUTTON2);
    
    // on release
    if (not s1 and ps1) send_doc["BUTTON1"] = true;
    if (not s2 and ps2) send_doc["BUTTON2"] = true;

    // get data from serial and send states to serial
    String buf = Serial.readStringUntil('\n');
    deserializeJson(receive_doc, buf);

    buf = "";
    serializeJson(send_doc, buf);
    
    Serial.println(buf);
    delay(0.01);

    if (receive_doc.containsKey("GPS")){
        // B1RCV/B2RCV alg
        if (receive_doc["B1RCV"]) send_doc["BUTTON1"] = false;
        if (receive_doc["B2RCV"]) send_doc["BUTTON2"] = false;

        // arrays in the JSON doc
        JsonArray gpsArr = receive_doc["GPS"].as<JsonArray>();
        JsonArray ledArr = receive_doc["LED"].as<JsonArray>();

        // String test = "";
        // serializeJson(ledArr, test);
        // Serial.println(test);

        // toggle LEDs
        if (ledArr[0] == 0){
            digitalWrite(LED1, LOW);
        }
        else if (ledArr[0] == 1){
            toggleLED(LED1);
        }
        else if (ledArr[0] == 2){
            digitalWrite(LED1, HIGH);
        }

        if (ledArr[1] == 0){
            digitalWrite(LED2, LOW);
        }
        else if (ledArr[1] == 1){
            toggleLED(LED2);
        }
        else if (ledArr[1] == 2){
            digitalWrite(LED2, HIGH);
        }

        // convert units
        gpsArr[2] = convToUnit(gpsArr[2]);

        // 1 LED = 2 units of speed if config[LED] is 1, so we can divide by 2
        if (led == 1) gpsArr[2] = (gpsArr[2].as<int>())/2;
        
        // display speed on LED panel according to configuration
        if (gpsArr[2] <= 0) clearScrn();
        else if (gpsArr[2] >= 20) {
            clearScrn();
            numToArr(19, HIGH);
        }
        else {
            clearScrn();
            numToArr(round(gpsArr[2].as<double>())-1, HIGH); // 1mph should be LED0
        }
        modDisp(); // put arr to LED
    } else{
        // turn everything off

        digitalWrite(LED1, LOW);
        digitalWrite(LED2, LOW);
        
        clearScrn();
        modDisp();
    }

    // prev states
    ps1 = s1;
    ps2 = s2;
}

// modifies arr to value (HIGH or LOW) based on LED num
void numToArr(int lnum, bool val){
    if (lnum < 0 or lnum > 19) return;

    if (lnum >= 0 and lnum < 10) disp[0][lnum] = val;
    if (lnum >= 10 and lnum < 20) disp[1][lnum-10] = val;
}

// sets all values to LOW
void clearScrn(void){
    for (int r = 0; r < ROWS; r++){
        for (int c = 0; c < COLS; c++){
            disp[r][c] = LOW;  
        }  
    }  
}

// sets all values to HIGH
void allScrn(void){
    for (int r = 0; r < ROWS; r++){
        for (int c = 0; c < COLS; c++){
            disp[r][c] = HIGH;  
        }  
    }  
}

// modifies display based on disp[][] matrix
void modDisp(void){ // HIGH = on, LOW = off
/*    2x10 LED matrix
//
//        8  9  10 11 12 13 A2 A3 A4 A5    
//      |-------------------------------|
//  6 R |  0  1  2  3  4  5  6  7  8  9 |
//      |                               |
//  7 R | 10 11 12 13 14 15 16 17 18 19 |
//      |-------------------------------|
//    R = 220 ohms
//
//    Numbers represent LEDs and 
//    the numbers on the side represent pins
//    R represents resistors
*/
    for (int r = 0; r < ROWS; r++){
        bool hasOn = false;
        for (int c = 0; c < COLS; c++){
            hasOn = (hasOn || disp[r][c]);
        }

        digitalWrite(row[r], hasOn);
        for (int c = 0; c < COLS && hasOn; c++){
            digitalWrite(col[c], not disp[r][c]);
        }
    }
}

int convToUnit(int sp){
    /*
    Assumes that default is given in mph because the
    default speed for the Neo6M is mph
    */

    if (unit == 0) return sp; // mph
    else if (unit == 1) return ((int) (sp/1.0)*1.609); // km/h
    else return ((int) (sp/1.0)/2.237); // mph
}

void toggleLED(int led){
    if (millis() - blinkPrevMillis >= INTERVAL){
        blinkPrevMillis = millis();

        if (states[led] == LOW){
            states[led] = HIGH;
        } else{
            states[led] = LOW;
        }
    }

    digitalWrite(led, states[led]);
}
