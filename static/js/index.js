let values = document.querySelector('.values');
let input = document.querySelector('#message');
let send = document.querySelector('#send');
let identify = document.querySelector('#identify');
let help = document.querySelector('#help');
let status_cmd = document.querySelector('#status');
let light_mode_on = document.querySelector('#light-mode-on');
let light_mode_off = document.querySelector('#light-mode-off');
let aku_charging_mode_on = document.querySelector('#aku-charging-mode-on');
let aku_charging_mode_off = document.querySelector('#aku-charging-mode-off');
let freezer_mode_on = document.querySelector('#freezer-mode-on');
let freezer_mode_off = document.querySelector('#freezer-mode-off');
let charging_on = document.querySelector('#charging-on');
let charging_off = document.querySelector('#charging-off');
let fan_on = document.querySelector('#fan-on');
let fan_off = document.querySelector('#fan-off');
let pumps_on = document.querySelector('#pumps-on');
let pumps_off = document.querySelector('#pumps-off');
let charger1_on = document.querySelector('#charger1-on');
let charger1_off = document.querySelector('#charger1-off');
let charger2_on = document.querySelector('#charger2-on');
let charger2_off = document.querySelector('#charger2-off');
let audio2_on = document.querySelector('#audio-on');
let audio2_off = document.querySelector('#audio-off');
let light_power_button = document.querySelector('#light-power-button');
let light_power = document.querySelector('#light-power');
let freezer_power_button = document.querySelector('#freezer-power-button');
let freezer_power = document.querySelector('#freezer-power');
let status_container = document.querySelector('.status-container');
let socket = io();
socket.on('connect', function() {
    console.log('Connected to server');
    socket.emit('message', 'hello');
    p = document.createElement('div');
    p.innerHTML = 'connected';
    p.classList.add('msg');
    p.classList.add('system');
    values.appendChild(p);
});
socket.on('sending', function(msg) {
    console.log(msg);
    p = document.createElement('div');
    p.innerHTML = msg;
    p.classList.add('msg');
    p.classList.add('sending');
    values.insertBefore(p, values.firstChild);
});
socket.on('recieving', function(msg) {
    console.log(msg);
    p = document.createElement('div');
    p.innerHTML = msg;
    p.classList.add('msg');
    p.classList.add('recieving');
    values.insertBefore(p, values.firstChild);
});
socket.on('status', function(msg) {
    console.log(msg);
    let data = JSON.parse(msg);
    console.log(data);
    status_container.innerHTML = '';
    for (let key in data) {
        let p = document.createElement('div');
        let p1 = document.createElement('div');
        let p2 = document.createElement('div');
        p1.innerHTML = key + ':';
        p2.innerHTML = data[key];
        p.classList.add('stat');
        p1.classList.add('key');
        p2.classList.add('value');
        status_container.appendChild(p);
        p.appendChild(p1);
        p.appendChild(p2);
    }
});
send.addEventListener('click', function()                  {socket.emit('command', input.value);});
light_power_button.addEventListener('click', function()    {
    if (light_power.value > 100) {
        light_power.value = 100;
    }
    if (light_power.value < 0) {
        light_power.value = 0;
    }
    socket.emit('command', 'LIGHT_FORCE ' + light_power.value);
});
freezer_power_button.addEventListener('click', function()  {
    if (freezer_power.value > 100) {
        freezer_power.value = 100;
    }
    if (freezer_power.value < 0) {
        freezer_power.value = 0;
    }
    socket.emit('command', 'FREEZER_SET ' + freezer_power.value);
});
identify.addEventListener('click', function()              {socket.emit('command', 'IDN?');});
help.addEventListener('click', function()                  {socket.emit('command', 'HELP');});
status_cmd.addEventListener('click', function()            {socket.emit('command', 'GET_STATUS');});
light_mode_on.addEventListener('click', function()         {socket.emit('command', 'LIGHT_MODE 1');});
light_mode_off.addEventListener('click', function()        {socket.emit('command', 'LIGHT_MODE 0');});
aku_charging_mode_on.addEventListener('click', function()  {socket.emit('command', 'AUTO_CHARGING 1');});
aku_charging_mode_off.addEventListener('click', function() {socket.emit('command', 'AUTO_CHARGING 0');});
freezer_mode_on.addEventListener('click', function()       {socket.emit('command', 'FREEZER_AUTO 1');});
freezer_mode_off.addEventListener('click', function()      {socket.emit('command', 'FREEZER_AUTO 0');});
charging_on.addEventListener('click', function()           {socket.emit('command', 'FORCE_CHARGING 1');});
charging_off.addEventListener('click', function()          {socket.emit('command', 'FORCE_CHARGING 0');});
fan_on.addEventListener('click', function()                {socket.emit('command', 'FREEZER_FAN 1');});
fan_off.addEventListener('click', function()               {socket.emit('command', 'FREEZER_FAN 0');});
pumps_on.addEventListener('click', function()              {socket.emit('command', 'FREEZER_PUMPS 1');});
pumps_off.addEventListener('click', function()             {socket.emit('command', 'FREEZER_PUMPS 0');});
charger1_on.addEventListener('click', function()           {socket.emit('command', 'CHARGER1 1');});
charger1_off.addEventListener('click', function()          {socket.emit('command', 'CHARGER1 0');});
charger2_on.addEventListener('click', function()           {socket.emit('command', 'CHARGER2 1');});
charger2_off.addEventListener('click', function()          {socket.emit('command', 'CHARGER2 0');});
audio2_on.addEventListener('click', function()             {socket.emit('command', 'AUDIO 1');});
audio2_off.addEventListener('click', function()            {socket.emit('command', 'AUDIO 0');});