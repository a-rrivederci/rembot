@ECHO off

set "script_path=%~dp0"
set "script_path=%script_path%/interface/test/rcode_test.py"

python %script_path% %*