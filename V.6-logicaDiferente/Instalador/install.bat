ECHO OFF
echo �######################################################�
echo �###                   Pinhalense                   ###�
echo �###         ==============================         ###�
echo �###                                                ###�
echo �###     SCRIPT Para instalacao do supervisorio     ###�
echo �###     Vc precisa estar conectado a internet!!    ###�
echo �###                                                ###�
echo �######################################################�
pause
CLS
echo �######################################################�
echo �###                                                ###�
echo �###  Vamos iniciar configurando a base do sistema  ###�
echo �###                Install Python 3.11             ###�
echo �###Lembrar de habilitar PHATH para todos users!!!!!###�
echo �###                                                ###�
echo �######################################################�
pause
start python-3.11.4-amd64.exe
pause
CLS
echo �######################################################�
echo �###                                                ###�
echo �###                                                ###�
echo �###      Configurando bibliotecas auxiliares       ###�
echo �###                                                ###�
echo �###                                                ###�
echo �######################################################�
pause
python -mpip install modbus_tk xlwt tkcalendar pystray Pillow
pause
CLS
echo �######################################################�
echo �###                                                ###�
echo �###         Copiando Arquivos para sistema         ###�
echo �###        Selecione a Opcao D = diretorio         ###�
echo �###                                                ###�
echo �######################################################�
pause
xcopy Sup c:\Sup /E /K
cd \sup
copy Supervisorio.lnk  "%homepath%/desktop/Supervisorio.lnk"
CLS
echo �######################################################�
echo �###                                                ###�
echo �###                                                ###�
echo �###   Parabens seu sistema esta pronto para o uso  ###�
echo �###                                                ###�
echo �###                                                ###�
echo �######################################################�
pause


