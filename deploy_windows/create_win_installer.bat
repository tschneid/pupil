cd "..\deploy_capture\"
bundle.sh


cd "..\deploy_player\"
bundle.sh

cd "..\deploy_windows\"
set WIX_BIN="c:\Program Files (x86)\WiX Toolset v3.9\bin\"
echo Wix Toolset Bin Path: %WIX_BIN%
%WIX_BIN%\heat.exe dir "..\deploy_player\dist\Pupil Player" -o player.wxs -cg PupilPlayer -sfrag -gg -g1 -sreg
%WIX_BIN%\heat.exe dir "..\deploy_capture\dist\Pupil Capture" -o capture.wxs -cg PupilCapture -sfrag -gg -g1 -sreg