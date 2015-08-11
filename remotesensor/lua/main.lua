hostaddr = "54.85.111.126"
sid = 1000
pin = 6
ow.setup(pin)

function bxor(a,b)
	local r = 0
	for i = 0, 31 do
		if ( a % 2 + b % 2 == 1 ) then
			r = r + 2^i
		end
		a = a / 2
		b = b / 2
	end
	return r
end
function getTemp()
	addr = ow.reset_search(pin)
    repeat
		if (addr ~= nil) then
			crc = ow.crc8(string.sub(addr,1,7))
			if (crc == addr:byte(8)) then
				if ((addr:byte(1) == 0x10) or (addr:byte(1) == 0x28)) then
					ow.reset(pin)
					ow.select(pin, addr)
					ow.write(pin, 0x44, 1)
					tmr.delay(1000000)
					present = ow.reset(pin)
					ow.select(pin, addr)
					ow.write(pin,0xBE, 1)
					data = nil
					data = string.char(ow.read(pin))
					for i = 1, 8 do
						data = data .. string.char(ow.read(pin))
					end
					crc = ow.crc8(string.sub(data,1,8))
					if (crc == data:byte(9)) then
						t = (data:byte(1) + data:byte(2) * 256)
						if (t > 32768) then
							t = (bxor(t, 0xffff)) + 1
							t = (-1) * t
						end
						t = t * 625
						lasttemp = t
						print("Last temp: " .. lasttemp)
						return t
					end                   
				end
			end
		end
		addr = ow.search(pin)
		if (addr == nil) then
			addr = ow.search(pin)
		end 
	until(addr == nil)
	return lasttemp
end

function wtserver(sid, t, ctime)
	sk=net.createConnection(net.TCP, 0)
    request_body = "{\"id\": " ..sid.. ",\"t\":" ..t.. ",\"time\":" ..ctime.. "}"
	--print(request_body)
	post_length=string.len(request_body)
    sk:on("receive", function(sck, c) print(c) end )
    sk:connect(12000, hostaddr)
    sk:send("POST /sensor HTTP/1.1\r\nHost: "..hostaddr.."\r\nConnection: keep-alive\r\nContent-Length: "..post_length.."\r\nAccept: */*\r\n\r\n"..request_body )
 end

wifi.sta.config("", "")
wifi.sta.connect()
tmr.alarm(1, 1000, 1, function()
	if wifi.sta.getip()== nil then
		print("IP unavaiable, Waiting...")
	else
		tmr.stop(1)
	end
	end
)
print("Config done, IP is "..wifi.sta.getip())
print("ESP8266 mode is: " .. wifi.getmode())
print("The module MAC address is: " .. wifi.ap.getmac())

repeat 
	tt = getTemp()
	wtserver(sid, tt, tmr.now())
	tmr.delay(30000000)
until  1 > 100
