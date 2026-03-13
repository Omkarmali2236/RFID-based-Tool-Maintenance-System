-- This script removes CASCADE DELETE constraints to preserve maintenance history
-- when tools are deleted from the registered tools list

-- Step 1: Drop existing foreign key constraints (if they exist)
ALTER TABLE maintenance_tools DROP FOREIGN KEY IF EXISTS maintenance_tools_ibfk_1;
ALTER TABLE received_tools DROP FOREIGN KEY IF EXISTS received_tools_ibfk_1;

-- Step 2: Re-add foreign key constraints WITHOUT CASCADE DELETE
-- This allows deletion from tools table while preserving history records

-- For maintenance_tools: Set to SET NULL to keep records even if tool is deleted
ALTER TABLE maintenance_tools 
ADD CONSTRAINT maintenance_tools_ibfk_1 
FOREIGN KEY (rfid_uid) REFERENCES tools(rfid_uid) 
ON DELETE SET NULL 
ON UPDATE CASCADE;

-- For received_tools: Set to SET NULL to keep records even if tool is deleted
ALTER TABLE received_tools 
ADD CONSTRAINT received_tools_ibfk_1 
FOREIGN KEY (rfid_uid) REFERENCES tools(rfid_uid) 
ON DELETE SET NULL 
ON UPDATE CASCADE;

-- Verify the changes
SHOW CREATE TABLE maintenance_tools;
SHOW CREATE TABLE received_tools;
