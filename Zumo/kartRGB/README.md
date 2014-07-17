# kartRGB

Port of my (Ross) RC Zumo code which uses WS2821B RGB LED strip for brake / reverse. Have done a little mod for Mario Kart which implements power up

Serial protocol is

Start: `*i\r\n`
Set speed and direction: `*s,speed,direction\r\n`
Boost: `*b\r\n`

Also included is a some state machine helper code to implement timed events.