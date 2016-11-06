require 'io'

local U = {}

--- See if the file exists
-- @param file Path to the file
-- @returns bool True if file exists else False
function U.fileExists(filename)
  local f = io.open(filename, "rb")
  if f then f:close() end
  return f ~= nil
end


--- Get all lines from a file, returns an empty
-- list/table if the file does not exist
function U.readFile(filename)
  if not U.fileExists(filename) then return {} end
  lines = {}
  for line in io.lines(filename) do
    lines[#lines+1] = line
  end
  return lines
end

return U
