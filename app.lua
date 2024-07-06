-- Function to prompt for server URL, username, and password
local function promptForInputs()
    print("Please enter the server URL:")
    local serverUrl = read()
    
    print("Please enter your username:")
    local username = read()
    
    print("Please enter your password:")
    local password = read("*")  -- Masked input
    
    return serverUrl, username, password
end

local serverUrl, username, password = 0 , 0 , 0

local function Login()
    serverUrl, username, password = promptForInputs()
end

-- Main function to execute the login and fetch data
local function FetchData()
    -- Prompt for server URL, username, and password
    
    
    -- Prepare POST data (adjust as per your server's requirements)
    local postData = "username=" .. username .. "&password=" .. password
    
    -- Make the HTTP POST request asynchronously
    local requestHandle = http.post(serverUrl, postData)
      
    -- Wait for the HTTP request to complete
    local event, url, handle = requestHandle

    
          
        http.post(serverUrl,postData)
        sleep(1)
        local responseData = requestHandle .readAll()
        print(responseData)

        
        -- Assuming the server responds with some Lua code or data
        
        

        end 

-- Entry point
Login()
FetchData()
