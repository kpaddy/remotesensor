require'socket.http'
require'ltn12'
#define LUA_USE_MODULES_WIFI
hosturl = "http://54.85.111.126:12000/sensor"
sensorid = 1000
previousstate = "unavailable"
tempfile = "/tmp/t.dat"
function connecttowifi(ssid, password)
    wifi.sta.config(ssid,password)
    end

function sleep(n)
  os.execute("sleep " .. tonumber(n))
end

function check()
    print("i am alive")
    end

function main()
    while true do
        readfromsensor()

        if checkWifiStatus() == 1 then
            if previousstate == "unavailable" then
                flushtoserver()
            end
            writetoserver(sensorid, 22.33, os.time())
            previousstate = "available"
        else
            writetolocalfile(sensorid, 83.45)
            previousstate = "unavailable"
        end
        print("going to sleep for 60secs")
        sleep(60)
    end
    end
function readfromsensor()

    end

function writetoserver(sensorid, t, time)
    response_body = {}
    request_body = "{\"id\": " .. sensorid  .. ",\"t\":" .. t .. ",\"time\":" time "}"
    --request_body = "{\"id\": " + tostring(sensorid) + ",\"t\":" + tostring(t) + "}"
    socket.http.request{
        url = hosturl,
        method = "POST",
        headers = {
             ["Content-Length"] = string.len(request_body)
         },
         source = ltn12.source.string(request_body),
         sink = ltn12.sink.table(response_body)
    }
    table.foreach(response_body,print)
    end

function checkWifiStatus()
    return 0
    end

function writetolocalfile(sensorid, temp)

    file = io.open (tempfile, "a+")
    io.output(file)
    io.write(sensorid .. "," .. temp .. "," .. os.time() .. "\n")
    io.close()
    end

function split(s, delimiter)
    result = {};
    for match in (s..delimiter):gmatch("(.-)"..delimiter) do
        table.insert(result, match);
    end
    return result;
end

function flushtoserver()
    file = io.open(tempfile, "r")
    for line in file:lines() do
        tokens = split(line, ",")
        print(tokens[1], tokens[2])
        --writeToServer(tokens[1], tokens[2], tokens[3])
    end
    file:close()
    emptylocalfile()
    end

function emptylocalfile()
    print("removing local file")
    os.remove(tempfile)
    end

--writetolocalfile(1000, 75.55)
--flushtoserver()
--main()
--connecttowifi("SWC6006", "ABCABC1234")
