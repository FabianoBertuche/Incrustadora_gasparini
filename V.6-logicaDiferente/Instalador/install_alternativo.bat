ECHO OFF
echo �######################################################�
echo �###          ACTUAL Montagens e Automacao          ###�
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
echo �###                Install Python  3.11            ###�
echo �###Lembrar de habilitar PHATH para todos users!!!!!###�
echo �###                                                ###�
echo �######################################################�
pause
start python-2.7.14.msi
pause
CLS
echo �######################################################�
echo �###                                                ###�
echo �###                                                ###�
echo �###      Configurando bibliotecas auxiliares       ###�
echo �###                                                ###�
echo �###                                                ###�
echo �######################################################�
pip install matplotlib
pip install modbus_tk
pause
CLS
echo �######################################################�
echo �###                                                ###�
echo �###                                                ###�
echo �###               Instalando QT                    ###�
echo �###                                                ###�
echo �###                                                ###�
echo �######################################################�
pause
start PyQt4-4.10-gpl-Py2.7-Qt4.8.4-x32.exe
pause
CLS
echo �######################################################�
echo �###                                                ###�
echo �###         Copiando Arquivos para sistema         ###�
echo �###        Selecione a Op��o D = diretorio         ###�
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


